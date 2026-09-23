#!/usr/bin/env python
"""Aggregate results into statistics, tables and figures.

Reads every `<results>/<arm>/predictions.jsonl`, restricts to the samples common
to all arms, and writes the paper's tables and figures.

By default this REFUSES to aggregate runs produced by the stub backend. Pass
--allow-stub only to check the plumbing; the output is then stamped as such.

    python scripts/03_aggregate_results.py --results results/main
    python scripts/03_aggregate_results.py --results results/main --out report/main
    python scripts/03_aggregate_results.py --results results_smoke --allow-stub

    # roll up the ablation tree into one table
    python scripts/03_aggregate_results.py --results results/main \
        --ablation-root results/ablation
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ctsr.config import load_config, relational_tasks  # noqa: E402
from ctsr.eval.aggregate import (ARM_LABELS, RunSet, aggregate_all,  # noqa: E402
                                 main_table)
from ctsr.report import figures as figmod  # noqa: E402
from ctsr.report import tables as tabmod  # noqa: E402
from ctsr.report.error_taxonomy import (build_taxonomy,  # noqa: E402
                                        detection_quality_correlation,
                                        write_report)
from ctsr.utils.io_utils import atomic_write_json, ensure_dir  # noqa: E402
from ctsr.utils.logging_utils import get_logger  # noqa: E402


def collect_ablation(ablation_root: str, relational, n_boot: int,
                     baseline_value=None, log=None) -> list:
    """One row per ablation variant directory, for the ablation table."""
    root = Path(ablation_root)
    rows = []
    if not root.exists():
        if log:
            log.warning("Ablation root %s does not exist; skipping.", root)
        return rows

    for variant_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        try:
            rs = RunSet(str(variant_dir), allow_stub=False)
        except Exception as exc:
            if log:
                log.warning("Skipping %s: %s", variant_dir.name, exc)
            continue
        if not rs.runs:
            continue
        for arm in rs.arms:
            table = main_table(rs, metric="correct", relational=relational,
                               paired_only=False, n_boot=min(n_boot, 2000))
            row = next((r for r in table if r["arm"] == arm), None)
            if row is None:
                continue
            overall = row.get("overall_value")
            rows.append({
                "variant": "{}::{}".format(variant_dir.name, arm),
                "n": row.get("overall_n"),
                "overall": overall,
                "relational": row.get("relational_value"),
                "non_relational": row.get("non_relational_value"),
                "delta_vs_baseline": (overall - baseline_value)
                if (overall is not None and baseline_value is not None) else None,
            })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description="Aggregate CTSR results")
    ap.add_argument("--results", required=True, help="directory containing <arm>/ subdirs")
    ap.add_argument("--out", default=None, help="output directory (default: <results>/report)")
    ap.add_argument("--config", default=None,
                    help="config used for the run, to read eval.relational_tasks")
    ap.add_argument("--set", dest="overrides", action="append", default=[])
    ap.add_argument("--baseline-arm", default="b3_selected")
    ap.add_argument("--proposed-arm", default="proposed_ctsr")
    ap.add_argument("--metric", default="correct",
                    help="primary metric for the main table (correct | iou | rouge_l)")
    ap.add_argument("--n-bootstrap", type=int, default=None)
    ap.add_argument("--allow-stub", action="store_true",
                    help="include stub runs (plumbing check only, never a result)")
    ap.add_argument("--no-figures", action="store_true")
    ap.add_argument("--ablation-root", default=None)
    ap.add_argument("--fraction", action="store_true",
                    help="report metrics as fractions rather than percentages")
    args = ap.parse_args()

    out = ensure_dir(args.out or (Path(args.results) / "report"))
    log = get_logger("aggregate", logfile=out / "aggregate.log")

    cfg = load_config(args.config, args.overrides) if args.config else {}
    rel = relational_tasks(cfg) if cfg else None
    n_boot = args.n_bootstrap or int((cfg.get("eval") or {}).get("n_bootstrap", 10000))
    pct = not args.fraction

    log.info("Aggregating %s (bootstrap=%d, allow_stub=%s)",
             args.results, n_boot, args.allow_stub)

    try:
        agg = aggregate_all(
            args.results,
            metric=args.metric,
            baseline_arm=args.baseline_arm,
            proposed_arm=args.proposed_arm,
            relational=rel,
            allow_stub=args.allow_stub,
            n_boot=n_boot,
            seed=int(cfg.get("seed", 1234)) if cfg else 1234,
        )
    except Exception as exc:
        log.exception("Aggregation failed")
        print("\nAggregation failed: {}: {}".format(type(exc).__name__, exc))
        return 1

    atomic_write_json(out / "aggregate.json", agg)

    coverage = agg.get("coverage") or {}
    log.info("Coverage: %s", coverage.get("n_per_arm"))
    log.info("Paired samples across all arms: %s", coverage.get("n_common"))
    for w in coverage.get("warnings") or []:
        log.warning(w)

    # -- tables ------------------------------------------------------------
    log.info("Writing tables...")
    table_paths = tabmod.write_all(agg, out, pct=pct)

    # -- error analysis ----------------------------------------------------
    taxonomy = None
    try:
        taxonomy = build_taxonomy(args.results, arm=args.proposed_arm,
                                  comparison_arms=(args.baseline_arm, args.proposed_arm))
        write_report(taxonomy, out)
        log.info("Error taxonomy: %s", taxonomy.get("counts"))
    except Exception as exc:
        log.warning("Error taxonomy skipped: %s", exc)

    try:
        corr = detection_quality_correlation(args.results, arm=args.proposed_arm)
        atomic_write_json(out / "detection_quality.json", corr)
        log.info("Detection-quality association: %s", corr.get("accuracy_by_n_objects"))
    except Exception as exc:
        log.warning("Detection-quality analysis skipped: %s", exc)

    # -- ablation ----------------------------------------------------------
    ablation_rows = []
    if args.ablation_root:
        base_row = next((r for r in (agg.get("main") or [])
                         if r.get("arm") == args.baseline_arm), None)
        base_val = base_row.get("overall_value") if base_row else None
        ablation_rows = collect_ablation(args.ablation_root, rel, n_boot, base_val, log)
        if ablation_rows:
            tabmod.ablation_table(ablation_rows, out, pct=pct)
            log.info("Ablation variants collected: %d", len(ablation_rows))
        else:
            log.warning("No ablation variants found under %s", args.ablation_root)

    # -- figures -----------------------------------------------------------
    if not args.no_figures:
        log.info("Writing figures...")
        fig_paths = figmod.write_all(agg, out, results_dir=args.results,
                                     taxonomy=taxonomy,
                                     ablation_rows=ablation_rows or None, pct=pct)
        log.info("Figures: %s", {k: (len(v) if isinstance(v, list) else v)
                                 for k, v in fig_paths.items()})

    # -- console summary ---------------------------------------------------
    print("\n" + "=" * 78)
    print("AGGREGATE SUMMARY")
    print("=" * 78)
    if agg.get("contains_stub_runs"):
        print("!! These results include STUB runs. They are not findings.\n")
    print("Paired samples across all arms: {}".format(coverage.get("n_common")))
    print("Per-arm sample counts:          {}".format(coverage.get("n_per_arm")))

    scale = 100.0 if pct else 1.0
    unit = "%" if pct else ""
    print("\nAccuracy ({}):".format("percent" if pct else "fraction"))
    print("  {:<46} {:>10} {:>12} {:>14}".format(
        "Arm", "Overall", "Relational", "Non-relational"))
    for r in agg.get("main", []):
        def f(key):
            v = r.get(key)
            return "{:.2f}{}".format(v * scale, unit) if v is not None else "--"
        print("  {:<46} {:>10} {:>12} {:>14}".format(
            ARM_LABELS.get(r["arm"], r["arm"])[:46],
            f("overall_value"), f("relational_value"), f("non_relational_value")))

    sig = agg.get("significance") or {}
    print("\nConfirmatory tests ({} vs {}):".format(args.baseline_arm, args.proposed_arm))
    if sig.get("note"):
        print("  {}".format(sig["note"]))
    for group in ("relational", "non_relational"):
        res = (sig.get("primary") or {}).get(group) or {}
        if not res or res.get("n_pairs") in (None, 0):
            print("  {:<16} no paired samples".format(group))
            continue
        d = res.get("delta")
        p = res.get("p_value")
        print("  {:<16} N={:<5} delta={:>8} [{}, {}]  p={:<10} {}".format(
            group, res.get("n_pairs"),
            "{:+.2f}{}".format(d * scale, unit) if d is not None else "--",
            "{:+.2f}".format(res["ci_lo"] * scale) if res.get("ci_lo") is not None else "--",
            "{:+.2f}".format(res["ci_hi"] * scale) if res.get("ci_hi") is not None else "--",
            "{:.2g}".format(p) if p is not None else "--",
            "SIGNIFICANT" if (p is not None and p < 0.05) else "",
        ))
        print("     wins={} losses={} (discordant pairs)".format(
            res.get("b01_only_b_correct"), res.get("b10_only_a_correct")))

    comp = {r["arm"]: r for r in agg.get("compute", [])}
    b, p_ = comp.get(args.baseline_arm), comp.get(args.proposed_arm)
    if b and p_ and b.get("mean_vlm_calls") and p_.get("mean_vlm_calls"):
        print("\nCompute match ({} vs {}):".format(args.baseline_arm, args.proposed_arm))
        print("  VLM calls/sample:  {:.2f} vs {:.2f}".format(
            b["mean_vlm_calls"], p_["mean_vlm_calls"]))
        if b.get("mean_megapixels") and p_.get("mean_megapixels"):
            print("  MPix encoded:      {:.2f} vs {:.2f}".format(
                b["mean_megapixels"], p_["mean_megapixels"]))
        if b.get("mean_prompt_tokens") and p_.get("mean_prompt_tokens"):
            print("  Prompt tokens:     {:.0f} vs {:.0f}  <- the relation block's cost".format(
                b["mean_prompt_tokens"], p_["mean_prompt_tokens"]))
        gap = abs(b["mean_vlm_calls"] - p_["mean_vlm_calls"])
        if gap > 0.05 * max(b["mean_vlm_calls"], 1):
            print("  WARNING: call counts differ by {:.2f}; the comparison is not "
                  "compute-matched. Check that both arms used the same selection "
                  "and detection settings.".format(gap))

    diag = {r["arm"]: r for r in agg.get("diagnostics", [])}
    dp = diag.get(args.proposed_arm) or {}
    if dp.get("mean_cross_tile_fraction") is not None:
        print("\nCross-tile structure (proposed arm):")
        print("  mean relations/scene:            {}".format(
            _fmt(dp.get("mean_relations_built"))))
        print("  mean cross-tile relations:       {}".format(
            _fmt(dp.get("mean_cross_tile_relations"))))
        print("  mean cross-tile fraction:        {}".format(
            _fmt(dp.get("mean_cross_tile_fraction"))))
        print("  mean duplicate detections merged:{}".format(
            _fmt(dp.get("mean_duplicate_rate"))))

    print("\nWritten to: {}".format(out.resolve()))
    print("=" * 78)
    return 0


def _fmt(v, nd=3):
    return "--" if v is None else "{:.{}f}".format(float(v), nd)


if __name__ == "__main__":
    raise SystemExit(main())
