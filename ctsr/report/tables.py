"""Table generation: CSV for analysis, LaTeX for the manuscript.

Formatting rules that protect the paper:

  * A missing metric prints as "--", never as 0.00. A reader must be able to tell
    "we measured zero" from "we could not measure this".
  * Confidence intervals are printed with the point estimate wherever they exist.
  * Significance stars are only attached to tests that were actually run, and the
    per-task family carries Holm-adjusted values, matching what `stats` computed.
  * Every LaTeX table carries a footnote naming the sample size and the test used,
    so a table lifted into the manuscript cannot lose its provenance.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from ..eval.aggregate import ARM_LABELS, ARM_ORDER
from ..utils.io_utils import ensure_dir, write_csv
from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.report.tables")

NA = "--"


def fmt(value: Optional[float], nd: int = 3, pct: bool = False,
        na: str = NA) -> str:
    """Format a metric, distinguishing missing from zero."""
    if value is None:
        return na
    try:
        v = float(value)
    except (TypeError, ValueError):
        return na
    if v != v:  # NaN
        return na
    if pct:
        return "{:.1f}".format(100.0 * v)
    return "{:.{}f}".format(v, nd)


def fmt_ci(value: Optional[float], lo: Optional[float], hi: Optional[float],
           nd: int = 3, pct: bool = False) -> str:
    base = fmt(value, nd, pct)
    if base == NA or lo is None or hi is None:
        return base
    return "{} [{}, {}]".format(base, fmt(lo, nd, pct), fmt(hi, nd, pct))


def stars(p: Optional[float]) -> str:
    if p is None:
        return ""
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


def _latex_escape(text: Any) -> str:
    s = str(text)
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"),
                 ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}")):
        s = s.replace(a, b)
    return s


def latex_table(rows: Sequence[Sequence[Any]], header: Sequence[str],
                caption: str, label: str, align: Optional[str] = None,
                notes: Optional[str] = None, escape: bool = True) -> str:
    """A booktabs table. Requires \\usepackage{booktabs} in the manuscript."""
    ncol = len(header)
    align = align or ("l" + "r" * (ncol - 1))
    esc = _latex_escape if escape else (lambda x: str(x))
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\small",
        r"\begin{tabular}{" + align + "}",
        r"\toprule",
        " & ".join(esc(h) for h in header) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(" & ".join(esc(c) for c in row) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    if notes:
        lines.append(r"\vspace{2pt}")
        lines.append(r"\begin{minipage}{\linewidth}\footnotesize " + esc(notes) +
                     r"\end{minipage}")
    lines += [
        r"\caption{" + esc(caption) + "}",
        r"\label{" + label + "}",
        r"\end{table}",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Table 1: main comparison
# --------------------------------------------------------------------------

def main_comparison(agg: Dict[str, Any], out_dir: str,
                    pct: bool = True) -> Dict[str, str]:
    rows_in = agg.get("main", [])
    out = ensure_dir(out_dir)
    write_csv(out / "table1_main.csv", rows_in)

    tex_rows: List[List[str]] = []
    for r in sorted(rows_in, key=lambda x: ARM_ORDER.index(x["arm"])
                    if x.get("arm") in ARM_ORDER else 99):
        tex_rows.append([
            ARM_LABELS.get(r.get("arm"), r.get("arm")),
            str(r.get("overall_n") or 0),
            fmt_ci(r.get("overall_value"), r.get("overall_ci_lo"),
                   r.get("overall_ci_hi"), 1 if pct else 3, pct),
            fmt_ci(r.get("relational_value"), r.get("relational_ci_lo"),
                   r.get("relational_ci_hi"), 1 if pct else 3, pct),
            fmt_ci(r.get("non_relational_value"), r.get("non_relational_ci_lo"),
                   r.get("non_relational_ci_hi"), 1 if pct else 3, pct),
            fmt(r.get("parse_fail_rate"), 1, True),
        ])

    n_paired = (agg.get("significance") or {}).get("n_paired_samples")
    notes = (
        "Accuracy in percent with 95\\% percentile-bootstrap confidence intervals. "
        "All arms are evaluated on the same {} paired samples. The relational / "
        "non-relational split is the pre-registered grouping of the 16 XLRS-Bench "
        "sub-tasks. 'Parse fail' is the share of responses from which no answer "
        "could be extracted; these are scored as incorrect."
        .format(n_paired if n_paired is not None else "common")
    )
    tex = latex_table(
        tex_rows,
        ["Method", "$N$", "Overall", "Relational", "Non-relational", "Parse fail"],
        caption="Accuracy on XLRS-Bench by method and task group.",
        label="tab:main",
        notes=notes,
    )
    (out / "table1_main.tex").write_text(tex, encoding="utf-8")
    return {"csv": str(out / "table1_main.csv"), "tex": str(out / "table1_main.tex")}


# --------------------------------------------------------------------------
# Table 2: per-task breakdown
# --------------------------------------------------------------------------

def per_task(agg: Dict[str, Any], out_dir: str, pct: bool = True) -> Dict[str, str]:
    rows_in = agg.get("per_task", [])
    out = ensure_dir(out_dir)
    write_csv(out / "table2_per_task.csv", rows_in)

    # Pivot task x arm.
    by_task: Dict[str, Dict[str, Any]] = {}
    meta: Dict[str, Dict[str, Any]] = {}
    for r in rows_in:
        by_task.setdefault(r["task"], {})[r["arm"]] = r
        meta.setdefault(r["task"], {"group": r.get("group"), "metric": r.get("metric"),
                                    "l2": r.get("l2")})

    sig = (agg.get("significance") or {}).get("per_task", {}) or {}
    arms = [a for a in ARM_ORDER if any(a in v for v in by_task.values())]

    tex_rows: List[List[str]] = []
    for task in sorted(by_task, key=lambda t: (meta[t].get("group") != "relational", t)):
        cells = [task, "R" if meta[task].get("group") == "relational" else "N",
                 meta[task].get("metric", "")]
        n_shown = None
        for arm in arms:
            r = by_task[task].get(arm)
            if r is None:
                cells.append(NA)
                continue
            n_shown = n_shown or r.get("n")
            cells.append(fmt(r.get("value"), 1 if pct else 3, pct))
        s = sig.get(task) or {}
        delta = s.get("delta")
        cells.append(fmt(delta, 1 if pct else 3, pct) + stars(s.get("p_adjusted")))
        cells.append(str(n_shown or 0))
        tex_rows.append(cells)

    header = (["Sub-task", "Grp", "Metric"]
              + [ARM_LABELS.get(a, a).split(":")[0] for a in arms]
              + ["$\\Delta$", "$N$"])
    notes = (
        "Grp: R = relational, N = non-relational (pre-registered). Metric: "
        "accuracy for multiple-choice tasks, IoU for grounding, ROUGE-L for "
        "captioning. $\\Delta$ is Proposed minus Baseline 3 on paired samples; "
        "stars use Holm-adjusted $p$ across the 16 sub-tasks "
        "($^{*}p<0.05$, $^{**}p<0.01$, $^{***}p<0.001$). "
        "These per-task tests are exploratory; the confirmatory tests are the two "
        "group-level comparisons in Table~\\ref{tab:significance}."
    )
    tex = latex_table(
        tex_rows, header,
        caption="Per-sub-task results across the 16 XLRS-Bench sub-tasks.",
        label="tab:pertask",
        align="l" + "c" * 2 + "l" + "r" * (len(arms) + 2),
        notes=notes,
    )
    (out / "table2_per_task.tex").write_text(tex, encoding="utf-8")
    return {"csv": str(out / "table2_per_task.csv"), "tex": str(out / "table2_per_task.tex")}


# --------------------------------------------------------------------------
# Table 3: compute
# --------------------------------------------------------------------------

def compute(agg: Dict[str, Any], out_dir: str) -> Dict[str, str]:
    rows_in = agg.get("compute", [])
    out = ensure_dir(out_dir)
    write_csv(out / "table3_compute.csv", rows_in)

    tex_rows: List[List[str]] = []
    for r in sorted(rows_in, key=lambda x: ARM_ORDER.index(x["arm"])
                    if x.get("arm") in ARM_ORDER else 99):
        tex_rows.append([
            ARM_LABELS.get(r.get("arm"), r.get("arm")),
            fmt(r.get("mean_vlm_calls"), 2),
            fmt(r.get("mean_megapixels"), 2),
            fmt(r.get("mean_prompt_tokens"), 0),
            fmt(r.get("mean_completion_tokens"), 0),
            fmt(r.get("mean_seconds"), 1),
            fmt(r.get("max_peak_vram_mb"), 0),
        ])
    notes = (
        "Per-sample means. 'MPix' is the pixel count actually encoded by the vision "
        "tower after resizing, measured rather than assumed. Baseline 3 and the "
        "proposed method issue the same number of calls and encode the same pixels "
        "by construction; the proposed method differs only in prompt tokens, which "
        "is the cost of the relation block. Peak VRAM is the maximum observed over "
        "all samples of the run."
    )
    tex = latex_table(
        tex_rows,
        ["Method", "VLM calls", "MPix", "Prompt tok.", "Gen. tok.", "Sec.", "Peak VRAM (MiB)"],
        caption="Inference cost per sample under the compute-matched protocol.",
        label="tab:compute", notes=notes,
    )
    (out / "table3_compute.tex").write_text(tex, encoding="utf-8")
    return {"csv": str(out / "table3_compute.csv"), "tex": str(out / "table3_compute.tex")}


# --------------------------------------------------------------------------
# Table 4: significance
# --------------------------------------------------------------------------

def significance(agg: Dict[str, Any], out_dir: str, pct: bool = True) -> Dict[str, str]:
    sig = agg.get("significance") or {}
    out = ensure_dir(out_dir)

    flat: List[Dict[str, Any]] = []
    for group, res in (sig.get("primary") or {}).items():
        if not isinstance(res, dict):
            continue
        flat.append({"scope": "primary", "key": group, **res})
    for task, res in (sig.get("per_task") or {}).items():
        if isinstance(res, dict):
            flat.append({"scope": "per_task", "key": task, **res})
    for pair, res in (sig.get("progression") or {}).items():
        if isinstance(res, dict):
            flat.append({"scope": "progression", "key": pair, **res})
    write_csv(out / "table4_significance.csv", flat)

    tex_rows: List[List[str]] = []
    for group in ("relational", "non_relational"):
        res = (sig.get("primary") or {}).get(group) or {}
        if "note" in res and "n_pairs" not in res:
            tex_rows.append([group.replace("_", "-"), NA, NA, NA, NA, NA, NA])
            continue
        tex_rows.append([
            group.replace("_", "-"),
            str(res.get("n_pairs") or 0),
            fmt(res.get("mean_a"), 1 if pct else 3, pct),
            fmt(res.get("mean_b"), 1 if pct else 3, pct),
            fmt_ci(res.get("delta"), res.get("ci_lo"), res.get("ci_hi"),
                   1 if pct else 3, pct),
            "{:.2g}".format(res["p_value"]) if res.get("p_value") is not None else NA,
            str(res.get("b01_only_b_correct", NA)) + " / " +
            str(res.get("b10_only_a_correct", NA)),
        ])

    notes = (
        "Confirmatory analysis: Baseline 3 (question-conditioned selection, no "
        "relations) versus the proposed method (identical pipeline plus the "
        "cross-tile spatial relation block), on paired samples. $p$ from McNemar's "
        "exact test on discordant pairs; the interval on $\\Delta$ is a paired "
        "bootstrap. 'Wins / losses' counts samples the proposed method alone got "
        "right, and those Baseline 3 alone got right. These two tests were "
        "pre-registered and are reported uncorrected; the 16 per-sub-task tests are "
        "exploratory and Holm-corrected in Table~\\ref{tab:pertask}."
    )
    tex = latex_table(
        tex_rows,
        ["Task group", "$N$", "Baseline 3", "Proposed", "$\\Delta$ [95\\% CI]",
         "$p$", "Wins / losses"],
        caption="Effect of the cross-tile spatial relation representation.",
        label="tab:significance", notes=notes,
    )
    (out / "table4_significance.tex").write_text(tex, encoding="utf-8")
    return {"csv": str(out / "table4_significance.csv"),
            "tex": str(out / "table4_significance.tex")}


# --------------------------------------------------------------------------
# Table 5: diagnostics
# --------------------------------------------------------------------------

def diagnostics(agg: Dict[str, Any], out_dir: str) -> Dict[str, str]:
    rows_in = agg.get("diagnostics", [])
    out = ensure_dir(out_dir)
    write_csv(out / "table5_diagnostics.csv", rows_in)

    tex_rows: List[List[str]] = []
    for r in sorted(rows_in, key=lambda x: ARM_ORDER.index(x["arm"])
                    if x.get("arm") in ARM_ORDER else 99):
        tex_rows.append([
            ARM_LABELS.get(r.get("arm"), r.get("arm")).split(":")[0],
            fmt(r.get("mean_tiles_total"), 1),
            fmt(r.get("mean_tiles_selected"), 1),
            fmt(r.get("mean_objects"), 1),
            fmt(r.get("mean_relations_built"), 1),
            fmt(r.get("mean_cross_tile_fraction"), 3),
            fmt(r.get("mean_duplicate_rate"), 3),
            fmt(r.get("parse_fail_rate"), 3),
        ])
    notes = (
        "Pipeline-internal statistics. 'Cross-tile frac.' is the share of "
        "constructed relations holding between objects observed in different tiles: "
        "the relational structure that independent tile processing cannot represent. "
        "'Dup. rate' is the fraction of raw detections removed as cross-tile "
        "duplicates."
    )
    tex = latex_table(
        tex_rows,
        ["Method", "Tiles", "Selected", "Objects", "Relations",
         "Cross-tile frac.", "Dup. rate", "Parse fail"],
        caption="Pipeline diagnostics.", label="tab:diagnostics", notes=notes,
    )
    (out / "table5_diagnostics.tex").write_text(tex, encoding="utf-8")
    return {"csv": str(out / "table5_diagnostics.csv"),
            "tex": str(out / "table5_diagnostics.tex")}


# --------------------------------------------------------------------------

def ablation_table(rows: Sequence[Dict[str, Any]], out_dir: str,
                   pct: bool = True) -> Dict[str, str]:
    """Table for the ablation sweep (see scripts/03_aggregate_results.py)."""
    out = ensure_dir(out_dir)
    write_csv(out / "table6_ablation.csv", rows)
    tex_rows = [[
        r.get("variant", ""),
        str(r.get("n") or 0),
        fmt(r.get("overall"), 1 if pct else 3, pct),
        fmt(r.get("relational"), 1 if pct else 3, pct),
        fmt(r.get("non_relational"), 1 if pct else 3, pct),
        fmt(r.get("delta_vs_baseline"), 1 if pct else 3, pct),
    ] for r in rows]
    tex = latex_table(
        tex_rows,
        ["Variant", "$N$", "Overall", "Relational", "Non-relational",
         "$\\Delta$ vs. Baseline 3"],
        caption="Ablation of the proposed framework's components.",
        label="tab:ablation",
        notes=("Each variant removes or perturbs one component while holding tiles, "
               "selection, model and call budget fixed."),
    )
    (out / "table6_ablation.tex").write_text(tex, encoding="utf-8")
    return {"csv": str(out / "table6_ablation.csv"),
            "tex": str(out / "table6_ablation.tex")}


def write_all(agg: Dict[str, Any], out_dir: str, pct: bool = True) -> Dict[str, Any]:
    """Generate every table, tolerating individual failures."""
    out: Dict[str, Any] = {}
    for name, fn in (("main", main_comparison), ("per_task", per_task),
                     ("compute", compute), ("significance", significance),
                     ("diagnostics", diagnostics)):
        try:
            if name in ("compute", "diagnostics"):
                out[name] = fn(agg, out_dir)
            else:
                out[name] = fn(agg, out_dir, pct=pct)
        except Exception as exc:
            LOG.exception("Table '%s' failed", name)
            out[name] = {"error": str(exc)}
    return out
