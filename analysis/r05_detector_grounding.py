#!/usr/bin/env python
"""Tier-2: did fixing grounding change what the relation block does?

Both regimes ran on the SAME 1,201 items, so the two relation effects can be compared
item by item:

    effect_VLM      = Proposed(VLM objects)      - Selection(VLM objects)
    effect_detector = Proposed(detector objects) - Selection(detector objects)
    improvement     = effect_detector - effect_VLM     (paired, same items)

Also reports how question-relevant the detector's objects were, since its vocabulary is
generic (trees dominate).
"""
import json
from collections import Counter
from pathlib import Path

import numpy as np

from common import (HELD_OUT, PREREGISTERED_RELATIONAL, RESULTS, SEED, fmt_p, mcnemar, pct,
                    pp, write_json, write_text)

TIER2 = Path(__file__).resolve().parent.parent / "results" / "detector_grounding"


def load_arm(path):
    return {r["uid"]: r for r in (json.loads(l) for l in open(path, encoding="utf-8") if l.strip())}


def ok(r):
    return r and r.get("status") == "ok" and r.get("correct") is not None \
        and (r.get("artifacts") or {}).get("scorable") is not False


def main():
    rng = np.random.default_rng(SEED)
    arms = {
        "Direct": load_arm(RESULTS / "b1_direct" / "predictions.jsonl"),
        "Selection (VLM objects)": load_arm(RESULTS / "b3_selected" / "predictions.jsonl"),
        "Proposed (VLM objects)": load_arm(RESULTS / "proposed_ctsr" / "predictions.jsonl"),
        "Selection (detector)": load_arm(TIER2 / "sel_det" / "predictions.jsonl"),
        "Proposed (detector)": load_arm(TIER2 / "prop_det" / "predictions.jsonl"),
    }
    uids = sorted(u for u in arms["Proposed (detector)"] if all(ok(a.get(u)) for a in arms.values()))
    task = {u: arms["Proposed (VLM objects)"][u]["task"] for u in uids}
    groups = {"all": uids,
              "relational": [u for u in uids if task[u] in PREREGISTERED_RELATIONAL],
              "non-relational": [u for u in uids if task[u] not in PREREGISTERED_RELATIONAL
                                 and task[u] not in HELD_OUT]}

    def vec(arm, us):
        return np.array([int(bool(arms[arm][u]["correct"])) for u in us])

    out = {"n_items": len(uids), "groups": {g: len(v) for g, v in groups.items()},
           "accuracy": {a: {g: float(vec(a, us).mean()) for g, us in groups.items()} for a in arms},
           "relation_effect": {}, "improvement": {}}

    for g, us in groups.items():
        e_vlm = vec("Proposed (VLM objects)", us) - vec("Selection (VLM objects)", us)
        e_det = vec("Proposed (detector)", us) - vec("Selection (detector)", us)
        out["relation_effect"][g] = {
            "VLM objects": mcnemar(vec("Selection (VLM objects)", us),
                                   vec("Proposed (VLM objects)", us), rng),
            "detector objects": mcnemar(vec("Selection (detector)", us),
                                        vec("Proposed (detector)", us), rng)}
        d = (e_det - e_vlm).astype(float)
        boots = d[rng.integers(0, d.size, (10000, d.size))].mean(1)
        # paired permutation on the sign of the per-item difference of differences
        signs = rng.choice([-1.0, 1.0], size=(10000, d.size))
        null = (signs * d).mean(1)
        out["improvement"][g] = {
            "n": int(d.size), "delta": float(d.mean()),
            "lo": float(np.percentile(boots, 2.5)), "hi": float(np.percentile(boots, 97.5)),
            "p_perm": float(max((np.abs(null) >= abs(d.mean()) - 1e-12).mean(), 1e-4))}

    # how question-relevant were the detector's objects?
    P = arms["Proposed (detector)"]
    share, labels = [], Counter()
    for u in uids:
        art = P[u].get("artifacts") or {}
        kws = [k.lower() for k in (art.get("question_keywords") or [])]
        objs = (art.get("scene_graph") or {}).get("objects") or []
        labels.update(o["label"] for o in objs)
        if objs:
            hit = sum(1 for o in objs if any(k in o["label"].lower() or o["label"].lower() in k
                                             for k in kws))
            share.append(hit / len(objs))
    out["detector_vocabulary"] = {
        "mean_share_objects_matching_question_keywords": float(np.mean(share)) if share else None,
        "top_labels": labels.most_common(12)}
    write_json("r05_detector_grounding.json", out)

    md = ["# A5. Tier-2: the relation block once grounding works", "",
          f"Same {len(uids)} items in both regimes ({out['groups']['relational']} relational, "
          f"{out['groups']['non-relational']} non-relational).", "",
          "## Accuracy (%)", "", "| Method | All | Relational | Non-relational |", "|---|---|---|---|"]
    for a, v in out["accuracy"].items():
        md.append(f"| {a} | {pct(v['all'])} | {pct(v['relational'])} | {pct(v['non-relational'])} |")
    md += ["", "## Effect of adding the relation block", "",
           "| Grounding | Group | Delta (pp) [95% CI] | p | wins/losses |", "|---|---|---|---|---|"]
    for g in groups:
        for reg in ("VLM objects", "detector objects"):
            r = out["relation_effect"][g][reg]
            md.append(f"| {reg} | {g} | {pp(r['delta'])} [{pp(r['lo'])}, {pp(r['hi'])}] | "
                      f"{fmt_p(r['p'])} | {r['wins']}/{r['losses']} |")
    md += ["", "## Did better grounding improve the relation effect? (paired, same items)", "",
           "| Group | Improvement (pp) [95% CI] | permutation p |", "|---|---|---|"]
    for g, r in out["improvement"].items():
        md.append(f"| {g} | {pp(r['delta'])} [{pp(r['lo'])}, {pp(r['hi'])}] | {r['p_perm']:.3g} |")
    dv = out["detector_vocabulary"]
    md += ["", "## Detector vocabulary", "",
           f"- objects matching a question keyword: {pct(dv['mean_share_objects_matching_question_keywords'])}% "
           "of the objects in a scene, on average",
           "- most frequent labels: " + ", ".join(f"{k} ({v})" for k, v in dv["top_labels"][:8])]
    write_text("r05_detector_grounding.md", "\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
