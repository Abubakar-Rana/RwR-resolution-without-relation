#!/usr/bin/env python
"""Compute every number reported in the paper from the raw per-sample predictions.

Input : <results>/<arm>/predictions.jsonl  (arms: b1_direct, b2_tiling, b3_selected, proposed_ctsr)
Output: analysis/stats.json       (all statistics, machine-readable)
        analysis/numbers.tex      (LaTeX macros so the manuscript never hand-copies a number)

    python analysis/analyze.py --results ../Codebase/results/main

Confirmatory vs exploratory
---------------------------
The pre-registered test is Baseline 3 vs Proposed within the relational and the
non-relational groups. Everything else computed here (the B1-vs-B3 crossover, the
stratification by relation availability, answer-change rates, oracle bounds) is
EXPLORATORY and is labelled as such in the manuscript.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

try:
    from scipy.stats import binomtest
except Exception:  # pragma: no cover
    binomtest = None

ARMS = ["b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"]
SEED = 20260922
N_BOOT = 10000


# ---------------------------------------------------------------------------
def load(results: Path):
    data = {}
    for arm in ARMS:
        p = results / arm / "predictions.jsonl"
        if not p.exists():
            raise FileNotFoundError(p)
        recs = {}
        with p.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    recs[r["uid"]] = r
        data[arm] = recs
    return data


def scorable(r) -> bool:
    return (r.get("status") == "ok" and r.get("correct") is not None
            and (r.get("artifacts") or {}).get("scorable") is not False)


def acc_ci(x, rng, n_boot=N_BOOT):
    x = np.asarray(x, dtype=float)
    if x.size == 0:
        return None
    idx = rng.integers(0, x.size, size=(n_boot, x.size))
    boots = x[idx].mean(axis=1)
    return {"acc": float(x.mean()), "lo": float(np.percentile(boots, 2.5)),
            "hi": float(np.percentile(boots, 97.5)), "n": int(x.size)}


def mcnemar(a, b, rng, n_boot=N_BOOT):
    """Paired binary comparison. a, b: aligned 0/1 arrays. delta = mean(b) - mean(a)."""
    a = np.asarray(a, dtype=int)
    b = np.asarray(b, dtype=int)
    n01 = int(((a == 0) & (b == 1)).sum())   # b wins
    n10 = int(((a == 1) & (b == 0)).sum())   # b losses
    n = n01 + n10
    if n == 0:
        p = 1.0
    elif binomtest is not None:
        p = float(binomtest(min(n01, n10), n, 0.5).pvalue)
    else:
        p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(n01, n10) + 1)) / 2 ** n)
    d = (b - a).astype(float)
    idx = rng.integers(0, d.size, size=(n_boot, d.size))
    boots = d[idx].mean(axis=1)
    return {"n": int(a.size), "acc_a": float(a.mean()), "acc_b": float(b.mean()),
            "delta": float(d.mean()), "lo": float(np.percentile(boots, 2.5)),
            "hi": float(np.percentile(boots, 97.5)), "wins": n01, "losses": n10,
            "p": p}


def paired(data, arm_a, arm_b, uids):
    a, b = [], []
    for u in uids:
        ra, rb = data[arm_a].get(u), data[arm_b].get(u)
        if ra is None or rb is None or not scorable(ra) or not scorable(rb):
            continue
        a.append(int(bool(ra["correct"])))
        b.append(int(bool(rb["correct"])))
    return a, b


def holm(pvals: dict):
    items = sorted(((k, v) for k, v in pvals.items() if v is not None), key=lambda kv: kv[1])
    m = len(items)
    out, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = run
    return out


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="results/main")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent))
    args = ap.parse_args()

    results = Path(args.results)
    out = Path(args.out)
    rng = np.random.default_rng(SEED)
    data = load(results)

    ref = data["proposed_ctsr"]
    all_uids = sorted(set.intersection(*[set(d) for d in data.values()]))
    groups = defaultdict(list)
    tasks = defaultdict(list)
    for u in all_uids:
        r = ref[u]
        groups[r.get("rel_group") or "unknown"].append(u)
        tasks[r.get("task")].append(u)

    S = {"n_samples_loaded": len(all_uids),
         "group_sizes_loaded": {g: len(v) for g, v in groups.items()},
         "task_sizes_loaded": {t: len(v) for t, v in tasks.items()}}

    # scorable counts per task (identical across arms by construction; verify)
    sc = {arm: sum(scorable(data[arm][u]) for u in all_uids) for arm in ARMS}
    S["n_scorable_per_arm"] = sc
    S["unscorable_by_task"] = dict(Counter(
        ref[u]["task"] for u in all_uids if not scorable(ref[u])))

    # ---- A. accuracy by arm x group -------------------------------------
    S["accuracy"] = {}
    for arm in ARMS:
        row = {}
        for gname, uids in [("overall", all_uids), ("relational", groups["relational"]),
                            ("non_relational", groups["non_relational"]),
                            ("unknown", groups.get("unknown", []))]:
            x = [int(bool(data[arm][u]["correct"])) for u in uids if scorable(data[arm][u])]
            row[gname] = acc_ci(x, rng)
        pf = sum(1 for u in all_uids if data[arm][u].get("parse_failed"))
        row["parse_fail_rate"] = pf / len(all_uids)
        S["accuracy"][arm] = row

    # ---- B. pairwise McNemar by group -----------------------------------
    pairs = [("b1_direct", "b2_tiling"), ("b2_tiling", "b3_selected"),
             ("b1_direct", "b3_selected"), ("b3_selected", "proposed_ctsr"),
             ("b1_direct", "proposed_ctsr")]
    S["pairwise"] = {}
    for a_arm, b_arm in pairs:
        key = "{}__{}".format(a_arm, b_arm)
        S["pairwise"][key] = {}
        for gname, uids in [("overall", all_uids), ("relational", groups["relational"]),
                            ("non_relational", groups["non_relational"])]:
            a, b = paired(data, a_arm, b_arm, uids)
            S["pairwise"][key][gname] = mcnemar(a, b, rng)

    # ---- C. interaction: (B3 - B1) relational vs non-relational ---------
    def deltas(a_arm, b_arm, uids):
        a, b = paired(data, a_arm, b_arm, uids)
        return np.asarray(b, float) - np.asarray(a, float)

    dr = deltas("b1_direct", "b3_selected", groups["relational"])
    dn = deltas("b1_direct", "b3_selected", groups["non_relational"])
    obs = dr.mean() - dn.mean()
    br = dr[rng.integers(0, dr.size, (N_BOOT, dr.size))].mean(1)
    bn = dn[rng.integers(0, dn.size, (N_BOOT, dn.size))].mean(1)
    did = br - bn
    # permutation p-value: shuffle group labels of the paired differences
    pooled = np.concatenate([dr, dn])
    perm = np.empty(N_BOOT)
    for i in range(N_BOOT):
        rng.shuffle(pooled)
        perm[i] = pooled[:dr.size].mean() - pooled[dr.size:].mean()
    p_int = float((np.abs(perm) >= abs(obs) - 1e-12).mean())
    S["interaction_b3_minus_b1"] = {
        "delta_relational": float(dr.mean()), "delta_non_relational": float(dn.mean()),
        "diff_in_diff": float(obs), "lo": float(np.percentile(did, 2.5)),
        "hi": float(np.percentile(did, 97.5)), "p_perm": max(p_int, 1.0 / N_BOOT)}

    # ---- D. per-task B3 vs P and B1 vs B3 --------------------------------
    S["per_task"] = {}
    p_bp, p_13 = {}, {}
    for t, uids in sorted(tasks.items()):
        row = {"group": ref[uids[0]].get("rel_group"), "l2": ref[uids[0]].get("l2")}
        for arm in ARMS:
            x = [int(bool(data[arm][u]["correct"])) for u in uids if scorable(data[arm][u])]
            row[arm] = acc_ci(x, rng, 4000)
        a, b = paired(data, "b3_selected", "proposed_ctsr", uids)
        row["b3_vs_p"] = mcnemar(a, b, rng, 4000) if a else None
        a, b = paired(data, "b1_direct", "b3_selected", uids)
        row["b1_vs_b3"] = mcnemar(a, b, rng, 4000) if a else None
        # zero-object extraction rate on this task (proposed arm)
        n0 = sum(1 for u in uids if (ref[u].get("n_objects") or 0) == 0)
        row["zero_object_rate"] = n0 / len(uids)
        S["per_task"][t] = row
        if row["b3_vs_p"] and row["b3_vs_p"]["n"] >= 20:
            p_bp[t] = row["b3_vs_p"]["p"]
        if row["b1_vs_b3"] and row["b1_vs_b3"]["n"] >= 20:
            p_13[t] = row["b1_vs_b3"]["p"]
    for t, padj in holm(p_bp).items():
        S["per_task"][t]["b3_vs_p"]["p_holm"] = padj
    for t, padj in holm(p_13).items():
        S["per_task"][t]["b1_vs_b3"]["p_holm"] = padj

    # ---- E. extraction yield and graph statistics (proposed arm) --------
    nobj = np.array([ref[u].get("n_objects") or 0 for u in all_uids])
    nrel = np.array([(ref[u].get("artifacts") or {}).get("n_relations_built") or 0
                     for u in all_uids])
    ncross = np.array([((ref[u].get("artifacts") or {}).get("graph_stats") or {})
                       .get("n_cross_tile") or 0 for u in all_uids])
    nsel = np.array([ref[u].get("n_tiles_selected") or 0 for u in all_uids])
    ntot = np.array([ref[u].get("n_tiles_total") or 0 for u in all_uids])

    ext_raw = ext_bad = ext_border = tiles_proc = tiles_fail = 0
    dup_in = dup_merged = cross_merges = 0
    for u in all_uids:
        art = ref[u].get("artifacts") or {}
        for e in art.get("extraction") or []:
            ext_raw += e.get("n_raw") or 0
            ext_bad += e.get("n_parse_failed") or 0
            ext_border += e.get("n_border_touching") or 0
            tiles_proc += e.get("n_tiles_processed") or 0
            tiles_fail += e.get("n_tiles_failed") or 0
        for m in art.get("merge") or []:
            dup_in += m.get("n_input") or 0
            dup_merged += m.get("n_merged") or 0
            cross_merges += m.get("n_cross_tile_merges") or 0

    has_rel = nrel > 0
    frac = np.divide(ncross, np.maximum(nrel, 1))
    S["extraction"] = {
        "zero_object_rate": float((nobj == 0).mean()),
        "zero_relation_rate": float((~has_rel).mean()),
        "mean_objects": float(nobj.mean()),
        "median_objects_given_any": float(np.median(nobj[nobj > 0])) if (nobj > 0).any() else None,
        "mean_objects_given_any": float(nobj[nobj > 0].mean()) if (nobj > 0).any() else None,
        "mean_relations_given_any": float(nrel[has_rel].mean()) if has_rel.any() else None,
        "mean_cross_tile_given_any": float(ncross[has_rel].mean()) if has_rel.any() else None,
        "cross_tile_fraction_given_any": float(frac[has_rel].mean()) if has_rel.any() else None,
        "share_with_cross_tile": float((ncross > 0).mean()),
        "mean_tiles_selected": float(nsel.mean()),
        "mean_tiles_total": float(ntot.mean()),
        "raw_items": int(ext_raw), "raw_items_unparsed": int(ext_bad),
        "border_touching": int(ext_border),
        "tiles_processed": int(tiles_proc), "tiles_failed": int(tiles_fail),
        "dedup_input": int(dup_in), "dedup_merged": int(dup_merged),
        "cross_tile_merges": int(cross_merges),
        "objects_hist_bins": [0, 1, 6, 16, 31, 10 ** 6],
    }

    # ---- F. B3 vs P stratified by what the relation block contained -----
    strata = {
        "no_relations": [u for u, h in zip(all_uids, has_rel) if not h],
        "has_relations": [u for u, h in zip(all_uids, has_rel) if h],
        "has_cross_tile": [u for u, c in zip(all_uids, ncross) if c > 0],
    }
    S["stratified_b3_vs_p"] = {}
    for sname, uids in strata.items():
        entry = {"n_all": len(uids)}
        for gname, gset in [("overall", None), ("relational", set(groups["relational"])),
                            ("non_relational", set(groups["non_relational"]))]:
            sub = uids if gset is None else [u for u in uids if u in gset]
            a, b = paired(data, "b3_selected", "proposed_ctsr", sub)
            entry[gname] = mcnemar(a, b, rng) if a else None
            # answer-change rate between the two arms on this stratum
            ch = [data["b3_selected"][u].get("parsed") != data["proposed_ctsr"][u].get("parsed")
                  for u in sub if scorable(data["b3_selected"][u]) and scorable(data["proposed_ctsr"][u])]
            if entry[gname] is not None:
                entry[gname]["answer_change_rate"] = float(np.mean(ch)) if ch else None
        S["stratified_b3_vs_p"][sname] = entry

    # ---- G. accuracy vs number of objects, BOTH arms (confound check) ---
    bins = [(0, 0, "0"), (1, 5, "1-5"), (6, 15, "6-15"), (16, 30, "16-30"), (31, 10 ** 6, "31+")]
    S["acc_by_objects"] = {}
    for lo, hi, lab in bins:
        sub = [u for u, n in zip(all_uids, nobj) if lo <= n <= hi]
        row = {"n": len(sub)}
        for arm in ARMS:
            x = [int(bool(data[arm][u]["correct"])) for u in sub if scorable(data[arm][u])]
            row[arm] = acc_ci(x, rng, 4000)
        row["rel_share"] = (sum(1 for u in sub if ref[u].get("rel_group") == "relational")
                            / len(sub)) if sub else None
        row["task_mix"] = dict(Counter(ref[u]["task"] for u in sub).most_common(4))
        S["acc_by_objects"][lab] = row

    # ---- H. oracle complementarity B1 | B3 ------------------------------
    S["oracle"] = {}
    for gname, uids in [("overall", all_uids), ("relational", groups["relational"]),
                        ("non_relational", groups["non_relational"])]:
        a, b = paired(data, "b1_direct", "b3_selected", uids)
        a, b = np.array(a), np.array(b)
        S["oracle"][gname] = {"b1": float(a.mean()), "b3": float(b.mean()),
                              "either": float(np.maximum(a, b).mean()),
                              "both": float(np.minimum(a, b).mean()), "n": int(a.size)}

    # ---- I. compute ----------------------------------------------------
    S["compute"] = {}
    for arm in ARMS:
        comps = [data[arm][u].get("compute") or {} for u in all_uids]
        def m(k):
            v = [c.get(k) for c in comps if c.get(k) is not None]
            return float(np.mean(v)) if v else None
        stage = defaultdict(list)
        for c in comps:
            for k, v in (c.get("stage_seconds") or {}).items():
                stage[k].append(v)
        peaks = [c.get("peak_vram_mb") for c in comps if c.get("peak_vram_mb") is not None]
        tot_sec = sum((c.get("wall_seconds") or 0) for c in comps)
        S["compute"][arm] = {
            "calls": m("n_vlm_calls"), "mpix": m("megapixels_encoded"),
            "prompt_tokens": m("prompt_tokens"), "completion_tokens": m("completion_tokens"),
            "images": m("n_images_encoded"), "seconds": m("wall_seconds"),
            "gpu_hours": tot_sec / 3600.0,
            "peak_vram_gb": (max(peaks) / 1024.0) if peaks else None,
            "stage_seconds": {k: float(np.mean(v)) for k, v in stage.items()},
            "n_degraded": sum(1 for u in all_uids
                              if (data[arm][u].get("artifacts") or {}).get("degradations")),
        }
    S["total_gpu_hours"] = sum(v["gpu_hours"] for v in S["compute"].values())

    # ---- J. answer distribution sanity (letters used) -------------------
    S["gt_letters"] = dict(Counter(str(data["b1_direct"][u].get("gt")) for u in all_uids
                                   if scorable(data["b1_direct"][u])))
    S["parsed_letters"] = {arm: dict(Counter(str(data[arm][u].get("parsed"))
                                              for u in all_uids).most_common(8))
                           for arm in ARMS}

    # ---- K. error taxonomy (from the pipeline's own classification) ----
    tax = results / "report" / "error_taxonomy.json"
    if tax.exists():
        t = json.loads(tax.read_text(encoding="utf-8"))
        S["error_taxonomy"] = {"counts": t.get("counts"), "n_failed": t.get("n_failed")}

    manifest = json.loads((results / "proposed_ctsr" / "manifest.json").read_text(encoding="utf-8"))
    S["environment"] = manifest.get("environment", {})
    S["config"] = {k: manifest.get("config", {}).get(k) for k in
                   ("model", "tiling", "selection", "detection", "relations", "final_call",
                    "baseline2", "dedup")}

    (out / "stats.json").write_text(json.dumps(S, indent=1), encoding="utf-8")
    write_macros(S, out / "numbers.tex")
    print_summary(S)


# ---------------------------------------------------------------------------
def pct(x, nd=1):
    return "--" if x is None else "{:.{}f}".format(100 * x, nd)


def pp(x, nd=1):
    return "--" if x is None else "{:+.{}f}".format(100 * x, nd).replace("-", "$-$")


def pval(p):
    if p is None:
        return "--"
    if p < 0.001:
        return "{:.0e}".format(p).replace("e-0", "\\times10^{-").replace("e-", "\\times10^{-") + "}"
    return "{:.2f}".format(p) if p >= 0.01 else "{:.3f}".format(p)


def write_macros(S, path):
    L = ["% Auto-generated by analysis/analyze.py -- do not edit by hand."]

    def mac(name, val):
        L.append("\\newcommand{\\%s}{%s}" % (name, val))

    A = S["accuracy"]
    tag = {"b1_direct": "BOne", "b2_tiling": "BTwo", "b3_selected": "BThree", "proposed_ctsr": "Prop"}
    for arm, t in tag.items():
        for g, gt in [("overall", "All"), ("relational", "Rel"), ("non_relational", "Non")]:
            e = A[arm][g]
            mac("acc%s%s" % (t, gt), pct(e["acc"]))
            mac("ci%s%s" % (t, gt), "[%s, %s]" % (pct(e["lo"]), pct(e["hi"])))
    mac("nLoaded", "{:,}".format(S["n_samples_loaded"]))
    mac("nScored", "{:,}".format(S["n_scorable_per_arm"]["proposed_ctsr"]))
    mac("nRel", "{:,}".format(A["proposed_ctsr"]["relational"]["n"]))
    mac("nNon", "{:,}".format(A["proposed_ctsr"]["non_relational"]["n"]))

    pw = S["pairwise"]
    for key, t in [("b3_selected__proposed_ctsr", "BP"), ("b1_direct__b3_selected", "OT"),
                   ("b1_direct__b2_tiling", "OTw"), ("b2_tiling__b3_selected", "TwT")]:
        for g, gt in [("overall", "All"), ("relational", "Rel"), ("non_relational", "Non")]:
            e = pw[key][g]
            mac("d%s%s" % (t, gt), pp(e["delta"]))
            mac("dci%s%s" % (t, gt), "[%s, %s]" % (pp(e["lo"]), pp(e["hi"])))
            mac("p%s%s" % (t, gt), pval(e["p"]))
            mac("w%s%s" % (t, gt), str(e["wins"]))
            mac("l%s%s" % (t, gt), str(e["losses"]))

    I = S["interaction_b3_minus_b1"]
    mac("didVal", pp(I["diff_in_diff"]))
    mac("didCI", "[%s, %s]" % (pp(I["lo"]), pp(I["hi"])))
    mac("didP", pval(I["p_perm"]))

    E = S["extraction"]
    mac("zeroObj", pct(E["zero_object_rate"], 0))
    mac("zeroRel", pct(E["zero_relation_rate"], 0))
    mac("shareCross", pct(E["share_with_cross_tile"], 0))
    mac("crossFrac", pct(E["cross_tile_fraction_given_any"], 0))
    mac("meanObjAny", "{:.1f}".format(E["mean_objects_given_any"] or 0))
    mac("meanRelAny", "{:.1f}".format(E["mean_relations_given_any"] or 0))
    mac("tilesSel", "{:.1f}".format(E["mean_tiles_selected"]))
    mac("tilesTot", "{:.0f}".format(E["mean_tiles_total"]))

    st = S["stratified_b3_vs_p"]
    for s, t in [("no_relations", "NoR"), ("has_relations", "HasR"), ("has_cross_tile", "Cross")]:
        e = st[s]["overall"]
        mac("n%s" % t, "{:,}".format(e["n"]))
        mac("d%s" % t, pp(e["delta"]))
        mac("dci%s" % t, "[%s, %s]" % (pp(e["lo"]), pp(e["hi"])))
        mac("p%s" % t, pval(e["p"]))
        mac("chg%s" % t, pct(e.get("answer_change_rate"), 1))
        for gk, gs in (("relational", "Rel"), ("non_relational", "Non")):
            er = st[s][gk]
            if er:
                mac("n%s%s" % (t, gs), "{:,}".format(er["n"]))
                mac("d%s%s" % (t, gs), pp(er["delta"]))
                mac("dci%s%s" % (t, gs), "[%s, %s]" % (pp(er["lo"]), pp(er["hi"])))
                mac("p%s%s" % (t, gs), pval(er["p"]))
                mac("chg%s%s" % (t, gs), pct(er.get("answer_change_rate"), 1))

    O = S["oracle"]
    for g, gt in [("overall", "All"), ("relational", "Rel"), ("non_relational", "Non")]:
        mac("orc%s" % gt, pct(O[g]["either"]))

    C = S["compute"]
    for arm, t in tag.items():
        mac("calls%s" % t, "{:.2f}".format(C[arm]["calls"]))
        mac("sec%s" % t, "{:.1f}".format(C[arm]["seconds"]))
        mac("mpix%s" % t, "{:.2f}".format(C[arm]["mpix"]) if C[arm]["mpix"] is not None else "--")
        mac("tok%s" % t, "{:,.0f}".format(C[arm]["prompt_tokens"]))
        mac("gpuh%s" % t, "{:.1f}".format(C[arm]["gpu_hours"]))
    mac("gpuhTotal", "{:.1f}".format(S["total_gpu_hours"]))
    tokdiff = C["proposed_ctsr"]["prompt_tokens"] - C["b3_selected"]["prompt_tokens"]
    mac("tokDiff", "{:,.0f}".format(tokdiff))

    osr = S["per_task"].get("Object Spatial Relationship")
    if osr:
        for arm, t in tag.items():
            mac("osr%s" % t, pct(osr[arm]["acc"]))
        e = osr["b1_vs_b3"]
        mac("osrD", pp(e["delta"]))
        mac("osrDci", "[%s, %s]" % (pp(e["lo"]), pp(e["hi"])))
        mac("osrP", pval(e["p"]))
        mac("osrPholm", pval(e.get("p_holm")))
    col = S["per_task"].get("Object Color")
    if col:
        e = col["b1_vs_b3"]
        mac("colD", pp(e["delta"]))
        mac("colPholm", pval(e.get("p_holm")))
    E2 = S["extraction"]
    mac("rawItems", "{:,}".format(E2["raw_items"]))
    mac("rawUnparsed", "{:.1f}".format(100 * E2["raw_items_unparsed"] / max(1, E2["raw_items"])))
    mac("dupRate", "{:.1f}".format(100 * E2["dedup_merged"] / max(1, E2["dedup_input"])))
    mac("crossMerges", "{:,}".format(E2["cross_tile_merges"]))
    mac("borderShare", "{:.0f}".format(100 * E2["border_touching"] / max(1, E2["raw_items"] - E2["raw_items_unparsed"])))
    ext = S["compute"]["proposed_ctsr"]["stage_seconds"].get("extraction")
    mac("extSec", "{:.1f}".format(ext))
    mac("extShare", "{:.0f}".format(100 * ext / S["compute"]["proposed_ctsr"]["seconds"]))
    mac("timeRatio", "{:.1f}".format(S["compute"]["b3_selected"]["seconds"] / S["compute"]["b1_direct"]["seconds"]))
    mac("peakVram", "{:.0f}".format(max(v["peak_vram_gb"] or 0 for v in S["compute"].values())))
    mac("nUnscOLU", str(S["unscorable_by_task"].get("Overall Land Use Classification", 0)))
    mac("nHeld", str(S["accuracy"]["proposed_ctsr"]["unknown"]["n"]))
    pl = S["parsed_letters"]["b1_direct"]; tot = sum(v for k, v in pl.items() if k != "None")
    mac("shareCpred", "{:.0f}".format(100 * pl.get("C", 0) / tot))
    st_p = S["compute"]["proposed_ctsr"]["stage_seconds"]
    for k, name in (("overview", "Overview"), ("selection", "Selection"),
                    ("final_answer", "Final"), ("attach_crops", "Crops")):
        mac("stage%s" % name, "{:.1f}".format(st_p.get(k, 0.0)))
    mac("stageGraph", "{:.3f}".format(st_p.get("dedup", 0.0) + st_p.get("relations", 0.0)))
    shares = []
    for arm in ARMS:
        pl = S["parsed_letters"][arm]
        tot = sum(v for k, v in pl.items() if k != "None")
        shares.append(100 * pl.get("C", 0) / tot)
    mac("shareCmin", "{:.0f}".format(min(shares)))
    mac("shareCmax", "{:.0f}".format(max(shares)))
    g = S["gt_letters"]
    mac("shareCgt", "{:.0f}".format(100 * g.get("C", 0) / max(1, sum(g.values()))))
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    write_pertask_table(S, path.parent / "table_pertask.tex")


SHORT = {
    "Object Spatial Relationship": "Object spatial rel.",
    "Regional Counting": "Regional counting",
    "Counting with Complex Reasoning": "Complex counting",
    "Route Planning": "Route planning",
    "Object Classification": "Object class.",
    "Object Color": "Object colour",
    "Object Motion State": "Motion state",
    "Overall Counting": "Overall counting",
    "Regional Land Use Classification": "Regional land use",
    "Overall Land Use Classification": "Overall land use",
    "Environmental Condition Reasoning": "Environ. condition",
    "Anomaly Detection and Interpretation": "Anomaly detection",
    "Counting/Counting with changing detection": "Bi-temporal counting",
}


def write_pertask_table(S, path):
    order = {"relational": 0, "non_relational": 1}
    rows = sorted(S["per_task"].items(), key=lambda kv: (order.get(kv[1]["group"], 2), kv[0]))
    L = ["% Auto-generated by analysis/analyze.py",
         r"\begin{tabular}{@{}lcrrrrrrrr@{}}", r"\toprule",
         r"Task & Grp & $n$ & Direct & Tiling & Select. & Prop. & $\Delta_z$ & $\Delta_r$ & No obj. \\",
         r"\midrule"]
    for t, r in rows:
        grp = {"relational": "R", "non_relational": "N"}.get(r["group"], "H")
        n = r["b3_vs_p"]["n"] if r["b3_vs_p"] else 0

        def a(arm):
            e = r.get(arm)
            return pct(e["acc"]) if e else "--"

        def d(key):
            e = r.get(key)
            if not e:
                return "--"
            star = "$^{*}$" if (e.get("p_holm") is not None and e["p_holm"] < 0.05) else ""
            return pp(e["delta"]) + star

        name = SHORT.get(t, t)
        L.append("{} & {} & {} & {} & {} & {} & {} & {} & {} & {} \\\\".format(
            name, grp, n, a("b1_direct"), a("b2_tiling"), a("b3_selected"),
            a("proposed_ctsr"), d("b1_vs_b3"), d("b3_vs_p"), pct(r["zero_object_rate"], 0)))
    L += [r"\bottomrule", r"\end{tabular}"]
    path.write_text("\n".join(L) + "\n", encoding="utf-8")


def print_summary(S):
    A = S["accuracy"]
    print("\nACCURACY  overall / relational / non-relational")
    for arm in ARMS:
        print("  {:<14} {:>6} {:>6} {:>6}".format(
            arm, pct(A[arm]["overall"]["acc"]), pct(A[arm]["relational"]["acc"]),
            pct(A[arm]["non_relational"]["acc"])))
    print("\nPAIRWISE (delta pp, p)")
    for k, v in S["pairwise"].items():
        print("  {:<30}".format(k), "  ".join("{}: {:+.1f} [{:+.1f},{:+.1f}] p={:.3g} w/l={}/{}".format(
            g[:3], 100 * e["delta"], 100 * e["lo"], 100 * e["hi"], e["p"], e["wins"], e["losses"])
            for g, e in v.items()))
    I = S["interaction_b3_minus_b1"]
    print("\nINTERACTION (B3-B1) rel {:+.1f} vs non {:+.1f}: DiD {:+.1f} [{:+.1f},{:+.1f}] p={:.3g}".format(
        100 * I["delta_relational"], 100 * I["delta_non_relational"], 100 * I["diff_in_diff"],
        100 * I["lo"], 100 * I["hi"], I["p_perm"]))
    print("\nEXTRACTION", json.dumps(S["extraction"], indent=1))
    print("\nSTRATIFIED B3 vs P")
    for s, e in S["stratified_b3_vs_p"].items():
        for g in ("overall", "relational", "non_relational"):
            x = e[g]
            if x:
                print("  {:<15} {:<15} n={:<5} {:+.1f} [{:+.1f},{:+.1f}] p={:.3g} change={}".format(
                    s, g, x["n"], 100 * x["delta"], 100 * x["lo"], 100 * x["hi"], x["p"],
                    pct(x.get("answer_change_rate"))))
    print("\nACC BY OBJECTS")
    for lab, r in S["acc_by_objects"].items():
        print("  {:<6} n={:<5} rel%={} ".format(lab, r["n"], pct(r["rel_share"], 0)),
              " ".join("{}={}".format(a[:4], pct((r[a] or {}).get("acc"))) for a in ARMS),
              r["task_mix"])
    print("\nORACLE", json.dumps(S["oracle"]))
    print("\nCOMPUTE")
    for arm, c in S["compute"].items():
        print("  {:<14} calls={:.2f} mpix={} tok={:.0f} sec={:.1f} gpuh={:.1f} peak={} stages={}".format(
            arm, c["calls"], c["mpix"], c["prompt_tokens"], c["seconds"], c["gpu_hours"],
            c["peak_vram_gb"], {k: round(v, 2) for k, v in c["stage_seconds"].items()}))
    print("total GPU hours", round(S["total_gpu_hours"], 1))
    print("\nPER TASK (B3->P delta, B1->B3 delta, zero-obj rate)")
    for t, r in S["per_task"].items():
        bp, b13 = r["b3_vs_p"], r["b1_vs_b3"]
        print("  {:<44} {:<14} n={:<4} B3->P {:+.1f} (p={:.2g})  B1->B3 {:+.1f} (p={:.2g})  zero={}".format(
            t[:44], str(r["group"]), bp["n"], 100 * bp["delta"], bp["p"],
            100 * b13["delta"], b13["p"], pct(r["zero_object_rate"], 0)))
    print("\nunscorable by task", S["unscorable_by_task"])
    print("parsed letters", S["parsed_letters"])


if __name__ == "__main__":
    main()
