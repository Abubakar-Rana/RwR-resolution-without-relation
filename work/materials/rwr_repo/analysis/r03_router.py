#!/usr/bin/env python
"""Suggestion 2: an offline router between the global view (Direct) and zooming (Selection).

Uses only information available BEFORE answering an item:
  * the task label that XLRS-Bench supplies with every item
  * the keywords extracted from the question text

Every router is evaluated with repeated stratified K-fold cross-validation: routing rules are
learned on training folds and applied only to held-out items, so no item's own answer is used
to route it. Reported: accuracy (mean and s.d. over repeats), VLM calls and seconds per item,
and a paired McNemar test against the best single method on one fixed repeat.
"""
import warnings
from collections import Counter

import numpy as np

# One category (Overall Land Use) has only 3 scorable items, fewer than K; stratification
# still works, sklearn just warns about it.
warnings.filterwarnings("ignore", message="The least populated class")
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

from common import (NAME, PREREGISTERED_RELATIONAL, SEED, correct, fmt_p, load, mcnemar, pct,
                    pp, write_json, write_text)

K, REPEATS = 5, 20


def main():
    rng = np.random.default_rng(SEED)
    data, uids = load()
    n = len(uids)
    task = np.array([data["proposed_ctsr"][u]["task"] for u in uids])
    group = np.array(["rel" if t in PREREGISTERED_RELATIONAL else "non" for t in task])
    kws = [data["b3_selected"][u]["artifacts"].get("question_keywords") or [] for u in uids]
    C = {m: correct(data, m, uids) for m in ("b1_direct", "b3_selected", "proposed_ctsr")}
    calls = {m: np.array([(data[m][u].get("compute") or {}).get("n_vlm_calls") or 0 for u in uids], float)
             for m in C}
    secs = {m: np.array([(data[m][u].get("compute") or {}).get("wall_seconds") or 0 for u in uids], float)
            for m in C}

    def best_per_key(keys, idx, cands):
        """For each key value, the candidate method with the highest training accuracy."""
        choice = {}
        for k in set(keys[idx]):
            sub = idx[keys[idx] == k]
            accs = {m: C[m][sub].mean() for m in cands}
            choice[k] = max(cands, key=lambda m: (accs[m], m == "b3_selected"))
        fallback = max(cands, key=lambda m: C[m][idx].mean())
        return choice, fallback

    def router_by_key(keys, cands):
        def fit_apply(tr, te):
            choice, fb = best_per_key(keys, tr, cands)
            return np.array([choice.get(keys[i], fb) for i in te])
        return fit_apply

    def make_keyword_router(use_task):
        """Logistic regression: does Selection beat Direct on this item?

        use_task=False routes from the question's keywords alone, i.e. without the
        benchmark's task label -- the setting a deployed system would face.
        """
        def fit_apply(tr, te):
            disc = tr[C["b1_direct"][tr] != C["b3_selected"][tr]]
            y = C["b3_selected"][disc]                   # 1 = Selection right, Direct wrong
            feats = []
            for i in range(n):
                f = {f"kw={w}": 1 for w in kws[i]}
                if use_task:
                    f[f"task={task[i]}"] = 1
                feats.append(f)
            vec = DictVectorizer()
            X = vec.fit_transform([feats[i] for i in disc])
            clf = LogisticRegression(C=0.5, max_iter=2000).fit(X, y)
            p = clf.predict_proba(vec.transform([feats[i] for i in te]))[:, 1]
            return np.where(p >= 0.5, "b3_selected", "b1_direct")
        return fit_apply

    routers = {
        "group router (pre-registered split)": router_by_key(group, ["b1_direct", "b3_selected"]),
        "task router (Direct / Selection)": router_by_key(task, ["b1_direct", "b3_selected"]),
        "task router (Direct / Selection / Proposed)": router_by_key(task, ["b1_direct", "b3_selected", "proposed_ctsr"]),
        "keyword + task router (logistic)": make_keyword_router(True),
        "keyword-only router (no task label)": make_keyword_router(False),
    }

    results = {}
    fixed_route = {}
    for rname, fn in routers.items():
        accs, cl, sc, share = [], [], [], []
        for rep in range(REPEATS):
            skf = StratifiedKFold(n_splits=K, shuffle=True, random_state=SEED + rep)
            route = np.empty(n, dtype=object)
            for tr, te in skf.split(np.zeros(n), task):
                route[te] = fn(tr, te)
            acc = np.array([C[route[i]][i] for i in range(n)])
            accs.append(acc.mean())
            cl.append(np.mean([calls[route[i]][i] for i in range(n)]))
            sc.append(np.mean([secs[route[i]][i] for i in range(n)]))
            share.append(dict(Counter(route)))
            if rep == 0:
                fixed_route[rname] = route
        r0 = fixed_route[rname]
        routed0 = np.array([C[r0[i]][i] for i in range(n)])
        results[rname] = {
            "acc_mean": float(np.mean(accs)), "acc_sd": float(np.std(accs)),
            "calls": float(np.mean(cl)), "seconds": float(np.mean(sc)),
            "route_share": {NAME[m]: float(np.mean([s.get(m, 0) for s in share]) / n) for m in C},
            "vs_selection": mcnemar(C["b3_selected"], routed0, rng),
            "vs_direct": mcnemar(C["b1_direct"], routed0, rng),
            "by_group": {g: float(routed0[group == g].mean()) for g in ("rel", "non")},
        }

    singles = {NAME[m]: {"acc": float(C[m].mean()), "calls": float(calls[m].mean()),
                         "seconds": float(secs[m].mean()),
                         "by_group": {g: float(C[m][group == g].mean()) for g in ("rel", "non")}}
               for m in C}
    oracle2 = np.maximum(C["b1_direct"], C["b3_selected"])
    oracle3 = np.maximum(oracle2, C["proposed_ctsr"])
    out = {"n": n, "folds": K, "repeats": REPEATS, "singles": singles, "routers": results,
           "oracle_direct_selection": float(oracle2.mean()),
           "oracle_all_three": float(oracle3.mean())}
    write_json("r03_router.json", out)

    md = ["# A3. Offline router between global view and zooming", "",
          f"{n} scored items, {K}-fold stratified cross-validation repeated {REPEATS} times. "
          "Routing uses only the benchmark's task label and the question keywords. "
          "McNemar p on repeat 0.", "",
          "| Method | Accuracy (%) | Relational | Non-rel. | VLM calls | s/item | vs Selection (pp) | p |",
          "|---|---|---|---|---|---|---|---|"]
    for name, s in singles.items():
        md.append(f"| {name} | {pct(s['acc'])} | {pct(s['by_group']['rel'])} | {pct(s['by_group']['non'])} "
                  f"| {s['calls']:.2f} | {s['seconds']:.1f} | | |")
    for rname, r in results.items():
        v = r["vs_selection"]
        md.append(f"| {rname} | {pct(r['acc_mean'])} ± {100 * r['acc_sd']:.1f} | {pct(r['by_group']['rel'])} "
                  f"| {pct(r['by_group']['non'])} | {r['calls']:.2f} | {r['seconds']:.1f} | "
                  f"{pp(v['delta'])} [{pp(v['lo'])}, {pp(v['hi'])}] | {fmt_p(v['p'])} |")
    md += ["", f"Oracle (best of Direct / Selection per item): {pct(out['oracle_direct_selection'])}%; "
               f"best of all three: {pct(out['oracle_all_three'])}%.", ""]
    for rname, r in results.items():
        md.append(f"- {rname}: routes " + ", ".join(f"{k} {100 * v:.0f}%" for k, v in r["route_share"].items() if v))
    write_text("r03_router.md", "\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
