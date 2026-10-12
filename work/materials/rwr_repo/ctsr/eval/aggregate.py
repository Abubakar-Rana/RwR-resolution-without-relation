"""Aggregation: run directories -> the tables the paper needs.

Produces, from the per-sample JSONL files:

  1. main comparison         accuracy per arm, overall and by relational group
  2. per-task breakdown      all 16 XLRS-Bench sub-tasks x arms
  3. compute table           VLM calls, tokens, pixels, seconds, peak VRAM
  4. significance table      paired tests, primarily b3_selected vs proposed_ctsr
  5. diagnostics             parse-failure rates, error rates, graph statistics

Two rules enforced here:

  * A stub run is flagged and, by default, refused. Reporting placeholder numbers
    as findings is the one failure mode worse than a crash.
  * Metrics that could not be computed stay None all the way into the table. They
    are never coerced to 0, because 0 reads as a measurement.
"""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from ..data.taxonomy import ALL_TASKS, DEFAULT_RELATIONAL_TASKS, canonical_task
from ..utils.io_utils import load_jsonl, read_json
from ..utils.logging_utils import get_logger
from .metrics import accuracy, mean
from .stats import (Estimate, PairedResult, bootstrap_ci, compare_arms,
                    holm_bonferroni)

LOG = get_logger("ctsr.eval.aggregate")

ARM_ORDER = ["b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"]
ARM_LABELS = {
    "b1_direct": "Baseline 1: Direct",
    "b2_tiling": "Baseline 2: Independent tiling",
    "b3_selected": "Baseline 3: Question-conditioned selection",
    "proposed_ctsr": "Proposed: + cross-tile spatial relations",
}

# Metric key used per task family when building tables.
FAMILY_METRIC = {
    "mcq": "correct",
    "mcq_counting": "correct",
    "counting": "correct",
    "grounding": "iou",
    "caption": "rouge_l",
}


class RunSet:
    """All runs found under a results root, indexed by arm name."""

    def __init__(self, results_dir: str, allow_stub: bool = False) -> None:
        self.root = Path(results_dir)
        self.allow_stub = allow_stub
        self.runs: Dict[str, List[Dict[str, Any]]] = {}
        self.manifests: Dict[str, Dict[str, Any]] = {}
        self.stub_runs: List[str] = []
        self.warnings: List[str] = []
        self._load()

    def _load(self) -> None:
        if not self.root.exists():
            raise FileNotFoundError("Results directory not found: {}".format(self.root))
        found = 0
        for run_dir in sorted(p for p in self.root.iterdir() if p.is_dir()):
            pred = run_dir / "predictions.jsonl"
            if not pred.exists():
                continue
            name = run_dir.name
            records = load_jsonl(pred)
            if not records:
                self.warnings.append("{}: predictions.jsonl is empty".format(name))
                continue
            manifest = read_json(run_dir / "manifest.json", default={}) or {}
            if not manifest:
                self.warnings.append(
                    "{}: no manifest.json; provenance for this run is unknown".format(name))
            is_stub = bool(manifest.get("backend_is_stub")
                           or any(r.get("backend_is_stub") for r in records[:20]))
            if is_stub:
                self.stub_runs.append(name)
                if not self.allow_stub:
                    self.warnings.append(
                        "{}: EXCLUDED - produced by a stub backend. Re-run with a real "
                        "model, or pass allow_stub=True to inspect the plumbing."
                        .format(name))
                    continue
            self.runs[name] = records
            self.manifests[name] = manifest
            found += 1
        LOG.info("Loaded %d run(s) from %s: %s", found, self.root, sorted(self.runs))
        for w in self.warnings:
            LOG.warning(w)

    # -- accessors ----------------------------------------------------------
    @property
    def arms(self) -> List[str]:
        known = [a for a in ARM_ORDER if a in self.runs]
        other = sorted(set(self.runs) - set(known))
        return known + other

    def records(self, arm: str) -> List[Dict[str, Any]]:
        return self.runs.get(arm, [])

    def common_uids(self, arms: Optional[Sequence[str]] = None) -> Set[str]:
        """uids present in every requested arm - the valid basis for comparison."""
        arms = list(arms or self.arms)
        sets = [set(r["uid"] for r in self.records(a) if r.get("uid")) for a in arms]
        if not sets:
            return set()
        common = sets[0]
        for s in sets[1:]:
            common &= s
        return common

    def coverage_report(self) -> Dict[str, Any]:
        """How comparable the arms actually are. Read this before any table."""
        per_arm = {a: set(r["uid"] for r in self.records(a) if r.get("uid"))
                   for a in self.arms}
        common = self.common_uids()
        return {
            "n_per_arm": {a: len(u) for a, u in per_arm.items()},
            "n_common": len(common),
            "missing_per_arm": {
                a: sorted(set().union(*per_arm.values()) - u)[:20] for a, u in per_arm.items()
            } if per_arm else {},
            "stub_runs": list(self.stub_runs),
            "warnings": list(self.warnings),
        }


# --------------------------------------------------------------------------
# Metric extraction
# --------------------------------------------------------------------------

def metric_value(record: Dict[str, Any], metric: str) -> Optional[float]:
    """Pull one metric from a prediction record, as a float or None.

    Unscorable samples return None so they are excluded rather than counted wrong.
    """
    if record.get("status") != "ok":
        return None
    art = record.get("artifacts") or {}
    if art.get("scorable") is False:
        return None

    if metric == "correct":
        v = record.get("correct")
        return None if v is None else (1.0 if v else 0.0)
    if metric == "iou":
        v = record.get("iou")
        return None if v is None else float(v)

    score = art.get("score") or {}
    if metric in score and score[metric] is not None:
        try:
            v = score[metric]
            return 1.0 if v is True else (0.0 if v is False else float(v))
        except (TypeError, ValueError):
            return None
    if metric in record and record[metric] is not None:
        try:
            return float(record[metric])
        except (TypeError, ValueError):
            return None
    return None


def per_sample_map(records: Iterable[Dict[str, Any]], metric: str,
                   uids: Optional[Set[str]] = None,
                   tasks: Optional[Set[str]] = None) -> Dict[str, Optional[float]]:
    """uid -> metric value, optionally restricted to uids and/or canonical tasks."""
    out: Dict[str, Optional[float]] = {}
    for r in records:
        uid = r.get("uid")
        if not uid:
            continue
        if uids is not None and uid not in uids:
            continue
        if tasks is not None and canonical_task(r.get("task") or r.get("category")) not in tasks:
            continue
        out[uid] = metric_value(r, metric)
    return out


def _group_of(record: Dict[str, Any],
              relational: Optional[Set[str]] = None) -> str:
    from ..data.taxonomy import relational_group
    stored = record.get("rel_group")
    if stored and relational is None:
        return str(stored)
    return relational_group(record.get("task") or record.get("category"), relational)


# --------------------------------------------------------------------------
# Tables
# --------------------------------------------------------------------------

def main_table(rs: RunSet, metric: str = "correct",
               relational: Optional[Set[str]] = None,
               paired_only: bool = True,
               n_boot: int = 10000, seed: int = 1234) -> List[Dict[str, Any]]:
    """Accuracy per arm: overall, relational, non-relational, with bootstrap CIs.

    `paired_only=True` restricts every cell to the uids present in all arms, which
    is what makes the columns comparable. Turning it off gives each arm its full
    sample and is reported separately, never mixed with the paired numbers.
    """
    uids = rs.common_uids() if paired_only else None
    rows: List[Dict[str, Any]] = []

    for arm in rs.arms:
        recs = [r for r in rs.records(arm) if uids is None or r.get("uid") in uids]
        row: Dict[str, Any] = {
            "arm": arm,
            "label": ARM_LABELS.get(arm, arm),
            "n": len(recs),
            "metric": metric,
        }
        buckets: Dict[str, List[float]] = defaultdict(list)
        for r in recs:
            v = metric_value(r, metric)
            if v is None:
                continue
            buckets["overall"].append(v)
            buckets[_group_of(r, relational)].append(v)

        for key in ("overall", "relational", "non_relational", "unknown"):
            vals = buckets.get(key, [])
            est = bootstrap_ci(vals, n_boot=n_boot, seed=seed) if vals else Estimate(None)
            row["{}_value".format(key)] = est.value
            row["{}_ci_lo".format(key)] = est.lo
            row["{}_ci_hi".format(key)] = est.hi
            row["{}_n".format(key)] = len(vals)

        row["parse_fail_rate"] = (
            sum(1 for r in recs if r.get("parse_failed")) / len(recs)) if recs else None
        row["error_rate"] = (
            sum(1 for r in recs if r.get("status") != "ok") / len(recs)) if recs else None
        rows.append(row)
    return rows


def per_task_table(rs: RunSet, paired_only: bool = True,
                   n_boot: int = 4000, seed: int = 1234) -> List[Dict[str, Any]]:
    """One row per (task, arm), with the metric appropriate to the task family."""
    uids = rs.common_uids() if paired_only else None
    rows: List[Dict[str, Any]] = []

    tasks_seen: Dict[str, str] = {}   # task -> family
    for arm in rs.arms:
        for r in rs.records(arm):
            t = canonical_task(r.get("task") or r.get("category"))
            tasks_seen.setdefault(t, str(r.get("family") or "mcq"))

    ordered_tasks = [t for t in ALL_TASKS if t in tasks_seen]
    ordered_tasks += sorted(set(tasks_seen) - set(ALL_TASKS))

    for task in ordered_tasks:
        family = tasks_seen.get(task, "mcq")
        metric = FAMILY_METRIC.get(family, "correct")
        for arm in rs.arms:
            vals = [
                v for v in (
                    metric_value(r, metric)
                    for r in rs.records(arm)
                    if canonical_task(r.get("task") or r.get("category")) == task
                    and (uids is None or r.get("uid") in uids)
                ) if v is not None
            ]
            est = bootstrap_ci(vals, n_boot=n_boot, seed=seed) if vals else Estimate(None)
            from ..data.taxonomy import l2_group, relational_group
            rows.append({
                "task": task,
                "l2": l2_group(task),
                "group": relational_group(task),
                "family": family,
                "metric": metric,
                "arm": arm,
                "n": len(vals),
                "value": est.value,
                "ci_lo": est.lo,
                "ci_hi": est.hi,
            })
    return rows


def compute_table(rs: RunSet, paired_only: bool = True) -> List[Dict[str, Any]]:
    """Cost per arm (plan section 9).

    `n_vlm_calls` and `megapixels_encoded` are the two figures that decide whether
    the comparison was compute-matched. `prompt_tokens` is reported separately
    because the relation block adds tokens without adding calls or pixels.
    """
    uids = rs.common_uids() if paired_only else None
    rows: List[Dict[str, Any]] = []
    for arm in rs.arms:
        recs = [r for r in rs.records(arm)
                if (uids is None or r.get("uid") in uids) and r.get("compute")]
        if not recs:
            rows.append({"arm": arm, "label": ARM_LABELS.get(arm, arm), "n": 0})
            continue
        comp = [r["compute"] for r in recs]

        def avg(key: str) -> Optional[float]:
            return mean([c.get(key) for c in comp])

        def total(key: str) -> float:
            return float(sum((c.get(key) or 0) for c in comp))

        peaks = [c.get("peak_vram_mb") for c in comp if c.get("peak_vram_mb") is not None]
        rows.append({
            "arm": arm,
            "label": ARM_LABELS.get(arm, arm),
            "n": len(recs),
            "mean_vlm_calls": avg("n_vlm_calls"),
            "mean_prompt_tokens": avg("prompt_tokens"),
            "mean_completion_tokens": avg("completion_tokens"),
            "mean_total_tokens": avg("total_tokens"),
            "mean_images_encoded": avg("n_images_encoded"),
            "mean_megapixels": avg("megapixels_encoded"),
            "mean_seconds": avg("wall_seconds"),
            "total_seconds": total("wall_seconds"),
            "total_vlm_calls": total("n_vlm_calls"),
            "max_peak_vram_mb": max(peaks) if peaks else None,
            "mean_vlm_failures": avg("n_vlm_failures"),
        })
    return rows


def significance_table(
    rs: RunSet,
    baseline_arm: str = "b3_selected",
    proposed_arm: str = "proposed_ctsr",
    relational: Optional[Set[str]] = None,
    alpha: float = 0.05,
    n_boot: int = 10000,
    seed: int = 1234,
) -> Dict[str, Any]:
    """The confirmatory analysis.

    Primary (pre-registered, 2 tests, reported uncorrected):
        relational group and non-relational group, proposed vs baseline.
    Secondary (exploratory, Holm-corrected as one family):
        each of the 16 sub-tasks.

    The primary/secondary split matters: correcting the two pre-registered tests
    together with 16 exploratory ones would needlessly destroy the power of the
    test the study was designed around.
    """
    out: Dict[str, Any] = {
        "baseline_arm": baseline_arm,
        "proposed_arm": proposed_arm,
        "alpha": alpha,
        "primary": {},
        "per_task": {},
        "note": "",
    }
    if baseline_arm not in rs.runs or proposed_arm not in rs.runs:
        out["note"] = ("Cannot test: missing run(s) {}. Available: {}".format(
            [a for a in (baseline_arm, proposed_arm) if a not in rs.runs],
            sorted(rs.runs)))
        LOG.warning(out["note"])
        return out

    uids = rs.common_uids([baseline_arm, proposed_arm])
    if not uids:
        out["note"] = "No overlapping samples between the two arms; no paired test possible."
        LOG.warning(out["note"])
        return out
    out["n_paired_samples"] = len(uids)

    rel_set = relational or DEFAULT_RELATIONAL_TASKS
    out["relational_tasks_used"] = sorted(rel_set)

    # -- primary: the two pre-registered group tests ------------------------
    for group in ("relational", "non_relational"):
        group_uids = {
            r["uid"] for r in rs.records(proposed_arm)
            if r.get("uid") in uids and _group_of(r, rel_set) == group
        }
        if not group_uids:
            out["primary"][group] = {"note": "no samples in this group"}
            continue
        a = per_sample_map(rs.records(baseline_arm), "correct", uids=group_uids)
        b = per_sample_map(rs.records(proposed_arm), "correct", uids=group_uids)
        res = compare_arms(a, b, metric="correct", n_boot=n_boot, seed=seed)
        out["primary"][group] = res.to_dict()

    # -- secondary: per-task, Holm-corrected ------------------------------
    p_values: Dict[str, Optional[float]] = {}
    details: Dict[str, Any] = {}
    task_families: Dict[str, str] = {}
    for r in rs.records(proposed_arm):
        t = canonical_task(r.get("task") or r.get("category"))
        task_families.setdefault(t, str(r.get("family") or "mcq"))

    for task, family in sorted(task_families.items()):
        metric = FAMILY_METRIC.get(family, "correct")
        task_uids = {
            r["uid"] for r in rs.records(proposed_arm)
            if r.get("uid") in uids
            and canonical_task(r.get("task") or r.get("category")) == task
        }
        if not task_uids:
            p_values[task] = None
            details[task] = {"note": "no samples"}
            continue
        a = per_sample_map(rs.records(baseline_arm), metric, uids=task_uids)
        b = per_sample_map(rs.records(proposed_arm), metric, uids=task_uids)
        res = compare_arms(a, b, metric=metric, n_boot=min(n_boot, 4000), seed=seed)
        p_values[task] = res.p_value
        details[task] = res.to_dict()
        details[task]["metric"] = metric

    corrected = holm_bonferroni(p_values, alpha=alpha)
    for task, info in corrected.items():
        details.setdefault(task, {}).update(
            {"p_adjusted": info.get("p_adjusted"), "reject_holm": info.get("reject")}
        )
    out["per_task"] = details
    out["holm"] = corrected

    # -- the progression narrative (plan: B1 -> B2 -> B3 -> proposed) -------
    out["progression"] = {}
    for i in range(len(ARM_ORDER) - 1):
        lo, hi = ARM_ORDER[i], ARM_ORDER[i + 1]
        if lo in rs.runs and hi in rs.runs:
            pu = rs.common_uids([lo, hi])
            a = per_sample_map(rs.records(lo), "correct", uids=pu)
            b = per_sample_map(rs.records(hi), "correct", uids=pu)
            out["progression"]["{}_vs_{}".format(lo, hi)] = compare_arms(
                a, b, metric="correct", n_boot=n_boot, seed=seed).to_dict()
    return out


def diagnostics_table(rs: RunSet) -> List[Dict[str, Any]]:
    """Pipeline-internal statistics: selection, detection, dedup, graph size.

    These are the numbers that explain *why* an arm behaved as it did, and several
    are reportable results in their own right - in particular
    `mean_cross_tile_fraction`, which quantifies how much relational structure
    independent tiling cannot see.
    """
    rows: List[Dict[str, Any]] = []
    for arm in rs.arms:
        recs = rs.records(arm)
        if not recs:
            continue
        arts = [r.get("artifacts") or {} for r in recs]
        graph_stats = [a.get("graph_stats") or {} for a in arts]
        merges = [m for a in arts for m in (a.get("merge") or [])]
        extractions = [e for a in arts for e in (a.get("extraction") or [])]

        rows.append({
            "arm": arm,
            "label": ARM_LABELS.get(arm, arm),
            "n": len(recs),
            "mean_tiles_total": mean([r.get("n_tiles_total") for r in recs]),
            "mean_tiles_selected": mean([r.get("n_tiles_selected") for r in recs]),
            "mean_objects": mean([r.get("n_objects") for r in recs]),
            "mean_relations": mean([r.get("n_relations") for r in recs]),
            "mean_relations_built": mean([a.get("n_relations_built") for a in arts]),
            "mean_cross_tile_fraction": mean([g.get("cross_tile_fraction") for g in graph_stats]),
            "mean_cross_tile_relations": mean([g.get("n_cross_tile") for g in graph_stats]),
            "mean_multi_tile_objects": mean([g.get("n_multi_tile_objects") for g in graph_stats]),
            "mean_duplicate_rate": mean([m.get("duplicate_rate") for m in merges]),
            "mean_cross_tile_merges": mean([m.get("n_cross_tile_merges") for m in merges]),
            "mean_extraction_parse_failed": mean([e.get("n_parse_failed") for e in extractions]),
            "mean_border_touching": mean([e.get("n_border_touching") for e in extractions]),
            "mean_tiles_failed": mean([e.get("n_tiles_failed") for e in extractions]),
            "n_selection_fallback": sum(
                1 for a in arts
                for s in (a.get("selection") or []) if s.get("fallback")
            ),
            "n_degraded_oom": sum(1 for a in arts if a.get("degradations")),
            "parse_fail_rate": sum(1 for r in recs if r.get("parse_failed")) / len(recs),
            "parse_strategies": _strategy_counts(recs),
        })
    return rows


def _strategy_counts(records: Sequence[Dict[str, Any]]) -> Dict[str, int]:
    from collections import Counter
    c = Counter()
    for r in records:
        strat = ((r.get("artifacts") or {}).get("score") or {}).get("parse_strategy")
        if strat:
            c[str(strat)] += 1
    return dict(c.most_common())


def aggregate_all(
    results_dir: str,
    metric: str = "correct",
    baseline_arm: str = "b3_selected",
    proposed_arm: str = "proposed_ctsr",
    relational: Optional[Set[str]] = None,
    allow_stub: bool = False,
    n_boot: int = 10000,
    seed: int = 1234,
) -> Dict[str, Any]:
    """Build every table in one call. Returns a dict ready to serialise."""
    rs = RunSet(results_dir, allow_stub=allow_stub)
    if not rs.runs:
        raise RuntimeError(
            "No usable runs found in {}. {}".format(
                results_dir,
                "All discovered runs were stub runs; re-run with model.backend='qwen'."
                if rs.stub_runs else "Check that predictions.jsonl files exist.")
        )
    return {
        "results_dir": str(results_dir),
        "coverage": rs.coverage_report(),
        "main": main_table(rs, metric=metric, relational=relational,
                           n_boot=n_boot, seed=seed),
        "per_task": per_task_table(rs, n_boot=min(n_boot, 4000), seed=seed),
        "compute": compute_table(rs),
        "significance": significance_table(
            rs, baseline_arm=baseline_arm, proposed_arm=proposed_arm,
            relational=relational, n_boot=n_boot, seed=seed),
        "diagnostics": diagnostics_table(rs),
        "manifests": {k: {kk: vv for kk, vv in v.items() if kk != "config"}
                      for k, v in rs.manifests.items()},
        "contains_stub_runs": bool(rs.stub_runs) and allow_stub,
    }
