"""Error analysis (plan section 10).

The plan names five failure categories. Each is operationalised below as a
checkable condition on the recorded artifacts, so the classification is
reproducible rather than an impression:

  fine_grained_loss        the arm that saw only low resolution failed, while an
                           arm that saw high-resolution crops succeeded
  tile_boundary            the supporting object touched a tile border, so it was
                           probably truncated in the crop that was analysed
  incorrect_relation       relations were present and the answer was still wrong,
                           on a relational task - the relation set was unhelpful
                           or misleading
  duplicate_objects        the deduplicator merged little while the same label
                           appeared many times, the signature of inflated counts
  localisation_propagation  no objects survived extraction, or extraction parse
                           failures dominated, so the downstream answer had
                           nothing reliable to work from
  parse_failure            the model answered but in an unreadable format
  infrastructure           the sample failed for a recorded technical reason
                           (OOM degradation, crop failure, VLM call failure)
  unexplained              wrong, and none of the above conditions held

The categories are assigned in priority order and a sample gets exactly one, so
the counts sum to the number of failures. Co-occurring conditions are also
recorded separately in `conditions`, since those are what a reader will want.

A sample is only classified when its ground truth was scorable. Unscorable
samples are counted apart and never enter the taxonomy.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from ..data.taxonomy import canonical_task, relational_group
from ..utils.io_utils import load_jsonl
from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.report.error_taxonomy")

CATEGORY_ORDER = [
    "infrastructure",
    "parse_failure",
    "localisation_propagation",
    "duplicate_objects",
    "tile_boundary",
    "incorrect_relation",
    "fine_grained_loss",
    "unexplained",
]


def _conditions(rec: Dict[str, Any],
                comparison: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, bool]:
    """Evaluate every diagnostic condition for one failed prediction."""
    art = rec.get("artifacts") or {}
    errors = rec.get("errors") or []
    extraction = art.get("extraction") or []
    merge = art.get("merge") or []
    graph = art.get("graph_stats") or {}
    task = canonical_task(rec.get("task") or rec.get("category"))
    is_rel = relational_group(task) == "relational"

    n_objects = rec.get("n_objects") or 0
    n_relations = rec.get("n_relations") or 0
    n_extract_parse_failed = sum((e.get("n_parse_failed") or 0) for e in extraction)
    n_extract_raw = sum((e.get("n_raw") or 0) for e in extraction)
    n_border = sum((e.get("n_border_touching") or 0) for e in extraction)
    n_tiles_failed = sum((e.get("n_tiles_failed") or 0) for e in extraction)
    dup_merged = sum((m.get("n_merged") or 0) for m in merge)
    dup_input = sum((m.get("n_input") or 0) for m in merge)

    cond: Dict[str, bool] = {}
    cond["has_errors"] = bool(errors)
    cond["oom_degraded"] = bool(art.get("degradations"))
    cond["tiles_failed"] = n_tiles_failed > 0
    cond["no_answer"] = rec.get("status") != "ok"
    cond["parse_failed"] = bool(rec.get("parse_failed"))
    cond["no_objects"] = n_objects == 0
    cond["extraction_mostly_unparsed"] = (
        n_extract_raw > 0 and n_extract_parse_failed >= 0.5 * n_extract_raw
    )
    cond["border_objects"] = n_border > 0
    cond["border_dominant"] = n_objects > 0 and n_border >= max(1, 0.4 * n_objects)
    cond["relations_present"] = n_relations > 0
    cond["relational_task"] = is_rel
    cond["cross_tile_present"] = (graph.get("n_cross_tile") or 0) > 0
    cond["duplicates_likely"] = (
        dup_input > 0 and dup_merged == 0 and n_objects >= 6
    )
    cond["selection_fallback"] = any(
        s.get("fallback") for s in (art.get("selection") or [])
    )

    # Cross-arm condition: did a higher-resolution arm get this right?
    cond["fixed_by_high_res"] = False
    cond["fixed_by_relations"] = False
    if comparison:
        uid = rec.get("uid")
        b3 = (comparison.get("b3_selected") or {}).get(uid)
        prop = (comparison.get("proposed_ctsr") or {}).get(uid)
        if b3 is not None and bool(b3):
            cond["fixed_by_high_res"] = True
        if prop is not None and bool(prop):
            cond["fixed_by_relations"] = True
    return cond


def classify(rec: Dict[str, Any],
             comparison: Optional[Dict[str, Dict[str, Any]]] = None) -> str:
    """Assign exactly one category, in priority order."""
    c = _conditions(rec, comparison)

    if c["no_answer"] or c["oom_degraded"] or c["tiles_failed"]:
        return "infrastructure"
    if c["parse_failed"]:
        return "parse_failure"
    if c["no_objects"] or c["extraction_mostly_unparsed"]:
        return "localisation_propagation"
    if c["duplicates_likely"]:
        return "duplicate_objects"
    if c["border_dominant"]:
        return "tile_boundary"
    if c["relational_task"] and c["relations_present"]:
        return "incorrect_relation"
    if c["fixed_by_high_res"]:
        return "fine_grained_loss"
    return "unexplained"


def build_taxonomy(results_dir: str, arm: str = "proposed_ctsr",
                   comparison_arms: Sequence[str] = ("b3_selected", "proposed_ctsr"),
                   max_examples: int = 5) -> Dict[str, Any]:
    """Classify every failure of `arm` and summarise.

    `comparison_arms` supply the cross-arm conditions (was this sample fixed by
    more resolution, or by the relation block?). Missing arms simply disable those
    conditions rather than causing a failure.
    """
    root = Path(results_dir)
    path = root / arm / "predictions.jsonl"
    if not path.exists():
        raise FileNotFoundError("No predictions for arm {!r} at {}".format(arm, path))

    comparison: Dict[str, Dict[str, Any]] = {}
    for other in comparison_arms:
        p = root / other / "predictions.jsonl"
        if p.exists():
            comparison[other] = {
                r["uid"]: r.get("correct") for r in load_jsonl(p) if r.get("uid")
            }
        else:
            LOG.info("Comparison arm %s not present; its conditions are disabled.", other)

    records = load_jsonl(path)
    counts: Counter = Counter()
    by_task: Dict[str, Counter] = defaultdict(Counter)
    by_group: Dict[str, Counter] = defaultdict(Counter)
    cond_counts: Counter = Counter()
    examples: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

    n_total = len(records)
    n_unscorable = 0
    n_correct = 0
    n_failed = 0

    for rec in records:
        art = rec.get("artifacts") or {}
        if art.get("scorable") is False or rec.get("correct") is None:
            # Captioning and grounding have no boolean correctness under some
            # configurations; those are excluded from the taxonomy by design.
            n_unscorable += 1
            continue
        if rec.get("correct"):
            n_correct += 1
            continue
        n_failed += 1

        cat = classify(rec, comparison)
        counts[cat] += 1
        task = canonical_task(rec.get("task") or rec.get("category"))
        by_task[task][cat] += 1
        by_group[relational_group(task)][cat] += 1
        for k, v in _conditions(rec, comparison).items():
            if v:
                cond_counts[k] += 1
        if len(examples[cat]) < max_examples:
            examples[cat].append({
                "uid": rec.get("uid"),
                "task": task,
                "question": (art.get("question") or "")[:200],
                "prediction": str(rec.get("parsed"))[:120],
                "gt": str(rec.get("gt"))[:120],
                "n_objects": rec.get("n_objects"),
                "n_relations": rec.get("n_relations"),
                "raw_excerpt": str(rec.get("raw_text") or "")[:300],
            })

    ordered = {k: counts.get(k, 0) for k in CATEGORY_ORDER if counts.get(k, 0)}
    for k, v in counts.items():
        ordered.setdefault(k, v)

    return {
        "arm": arm,
        "n_total": n_total,
        "n_correct": n_correct,
        "n_failed": n_failed,
        "n_unscorable_excluded": n_unscorable,
        "counts": ordered,
        "fractions": {k: round(v / n_failed, 4) for k, v in ordered.items()} if n_failed else {},
        "conditions": dict(cond_counts.most_common()),
        "by_task": {t: dict(c.most_common()) for t, c in sorted(by_task.items())},
        "by_group": {g: dict(c.most_common()) for g, c in sorted(by_group.items())},
        "examples": {k: v for k, v in examples.items()},
        "comparison_arms_used": sorted(comparison),
    }


def detection_quality_correlation(results_dir: str,
                                  arm: str = "proposed_ctsr") -> Dict[str, Any]:
    """Relationship between extraction quality and final correctness.

    Plan section 10: "The relationship between object detection quality and final
    reasoning performance will also be investigated."

    Reports accuracy stratified by the number of objects recovered and by the
    extraction parse-failure rate, plus a point-biserial correlation. Correlation
    is reported only when both arms of the comparison have variance, and it is
    explicitly observational - detection quality is not manipulated here, so this
    is not a causal estimate.
    """
    path = Path(results_dir) / arm / "predictions.jsonl"
    if not path.exists():
        raise FileNotFoundError("No predictions for arm {!r}".format(arm))

    xs_obj: List[float] = []
    xs_fail: List[float] = []
    ys: List[float] = []
    bins: Dict[str, List[float]] = defaultdict(list)

    for rec in load_jsonl(path):
        if rec.get("correct") is None or rec.get("status") != "ok":
            continue
        y = 1.0 if rec.get("correct") else 0.0
        n_obj = rec.get("n_objects")
        if n_obj is None:
            continue
        art = rec.get("artifacts") or {}
        extraction = art.get("extraction") or []
        raw = sum((e.get("n_raw") or 0) for e in extraction)
        bad = sum((e.get("n_parse_failed") or 0) for e in extraction)
        fail_rate = (bad / raw) if raw else 0.0

        xs_obj.append(float(n_obj))
        xs_fail.append(float(fail_rate))
        ys.append(y)

        label = ("0" if n_obj == 0 else "1-5" if n_obj <= 5 else
                 "6-15" if n_obj <= 15 else "16-30" if n_obj <= 30 else "31+")
        bins[label].append(y)

    def _pearson(a: Sequence[float], b: Sequence[float]) -> Optional[float]:
        n = len(a)
        if n < 3:
            return None
        ma, mb = sum(a) / n, sum(b) / n
        va = sum((x - ma) ** 2 for x in a)
        vb = sum((x - mb) ** 2 for x in b)
        if va <= 0 or vb <= 0:
            return None
        cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
        return cov / ((va ** 0.5) * (vb ** 0.5))

    order = ["0", "1-5", "6-15", "16-30", "31+"]
    return {
        "arm": arm,
        "n": len(ys),
        "accuracy_by_n_objects": {
            k: {"n": len(bins[k]), "accuracy": round(sum(bins[k]) / len(bins[k]), 4)}
            for k in order if bins.get(k)
        },
        "corr_n_objects_vs_correct": _pearson(xs_obj, ys),
        "corr_extraction_parse_failure_vs_correct": _pearson(xs_fail, ys),
        "note": ("Observational: detection quality was not experimentally "
                 "manipulated, so these correlations describe association, not "
                 "effect. Use the tile-size / top-k sweeps for a manipulated "
                 "comparison."),
    }


def write_report(taxonomy: Dict[str, Any], out_dir: str) -> Dict[str, str]:
    """Write the taxonomy as JSON, CSV and a LaTeX table."""
    from ..utils.io_utils import atomic_write_json, ensure_dir, write_csv
    from .tables import fmt, latex_table

    out = ensure_dir(out_dir)
    atomic_write_json(out / "error_taxonomy.json", taxonomy)

    n_failed = taxonomy.get("n_failed") or 0
    rows = [
        {"category": k, "count": v,
         "share_of_failures": round(v / n_failed, 4) if n_failed else None}
        for k, v in (taxonomy.get("counts") or {}).items()
    ]
    write_csv(out / "table7_error_taxonomy.csv", rows)

    tex = latex_table(
        [[r["category"].replace("_", " "), str(r["count"]),
          fmt(r["share_of_failures"], 1, True)] for r in rows],
        ["Category", "Count", "Share of failures (\\%)"],
        caption="Error taxonomy for the proposed method.",
        label="tab:errors",
        notes=("Categories are mutually exclusive and assigned in priority order, "
               "so counts sum to the {} scored failures. {} samples were excluded "
               "as unscorable."
               .format(n_failed, taxonomy.get("n_unscorable_excluded", 0))),
    )
    (out / "table7_error_taxonomy.tex").write_text(tex, encoding="utf-8")
    return {
        "json": str(out / "error_taxonomy.json"),
        "csv": str(out / "table7_error_taxonomy.csv"),
        "tex": str(out / "table7_error_taxonomy.tex"),
    }
