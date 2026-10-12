"""Paper figures (matplotlib).

Design rules applied throughout, so the figure set reads as one system:

  * Fixed categorical hue order, assigned per arm and never cycled, so an arm
    keeps its colour across every figure.
  * ONE axis per plot. No dual-axis charts anywhere.
  * A legend whenever there are two or more series, plus direct value labels on
    bars. The labels are not decoration: three of the palette's light-mode hues
    sit below 3:1 contrast on a white surface, and visible labels are the required
    relief so identity never rests on colour alone.
  * Recessive grid (light, behind the data), thin marks, no chartjunk.
  * Error bars are 95% bootstrap CIs wherever the aggregator supplied them.
  * Missing values are SKIPPED, never plotted as zero.

Figures are written as both PNG (300 dpi, for drafts) and PDF (vector, for the
camera-ready). Output is light-mode: these are print figures for a manuscript.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..eval.aggregate import ARM_LABELS, ARM_ORDER
from ..utils.io_utils import ensure_dir
from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.report.figures")

# Validated categorical palette, slots 1-4 (blue, orange, aqua, yellow).
# Passes the adjacent-pair CVD and normal-vision gates on a light surface;
# value labels supply the required contrast relief.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
ARM_COLOR: Dict[str, str] = {arm: SERIES[i % len(SERIES)]
                             for i, arm in enumerate(ARM_ORDER)}

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
INK_MUTED = "#8a8980"
GRID = "#e6e5e0"
POS = "#1baf7a"
NEG = "#e34948"


def _mpl():
    """Import and configure matplotlib, or return None with a clear warning."""
    try:
        import matplotlib
        matplotlib.use("Agg")  # headless: required on a GPU node with no display
        import matplotlib.pyplot as plt
    except ImportError as exc:
        LOG.error("matplotlib is unavailable (%s); no figures will be produced. "
                  "Install it with: pip install matplotlib", exc)
        return None
    plt.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "axes.edgecolor": INK_MUTED,
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK_2,
        "text.color": INK,
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.frameon": False,
        "legend.fontsize": 8,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "lines.linewidth": 2.0,
        "lines.markersize": 5,
        "figure.dpi": 110,
    })
    return plt


def _style_axes(ax, ygrid: bool = True, xgrid: bool = False) -> None:
    ax.set_axisbelow(True)
    ax.grid(axis="y" if ygrid else "x", visible=ygrid or xgrid)
    if xgrid:
        ax.grid(axis="x", visible=True)
    if ygrid and not xgrid:
        ax.grid(axis="x", visible=False)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(INK_MUTED)
    ax.spines["bottom"].set_color(INK_MUTED)


def _save(fig, out_dir, stem: str) -> List[str]:
    out = ensure_dir(out_dir)
    paths: List[str] = []
    for ext in ("png", "pdf"):
        p = out / "{}.{}".format(stem, ext)
        try:
            fig.savefig(p, dpi=300, bbox_inches="tight")
            paths.append(str(p))
        except Exception as exc:
            LOG.error("Could not write %s: %s", p, exc)
    try:
        import matplotlib.pyplot as plt
        plt.close(fig)
    except Exception:
        pass
    return paths


def _arm_label(arm: str, short: bool = True) -> str:
    label = ARM_LABELS.get(arm, arm)
    if not short:
        return label
    return {
        "b1_direct": "B1\nDirect",
        "b2_tiling": "B2\nTiling",
        "b3_selected": "B3\nSelection",
        "proposed_ctsr": "Proposed\n+ relations",
    }.get(arm, label.replace(": ", "\n"))


# --------------------------------------------------------------------------
# Figure 1: main comparison, grouped bars
# --------------------------------------------------------------------------

def fig_main(agg: Dict[str, Any], out_dir: str, pct: bool = True) -> List[str]:
    """Accuracy by arm for overall / relational / non-relational.

    Grouped bars with CI whiskers. Groups on the x axis, arms as the colour
    series, so the eye compares arms within a group - which is the comparison the
    study is about.
    """
    plt = _mpl()
    if plt is None:
        return []
    rows = {r["arm"]: r for r in agg.get("main", [])}
    arms = [a for a in ARM_ORDER if a in rows]
    if not arms:
        LOG.warning("fig_main: no arms to plot")
        return []

    groups = [("overall", "Overall"), ("relational", "Relational tasks"),
              ("non_relational", "Non-relational tasks")]
    scale = 100.0 if pct else 1.0

    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    n_arms = len(arms)
    width = 0.8 / n_arms

    for i, arm in enumerate(arms):
        xs: List[float] = []
        ys: List[float] = []
        err_lo: List[float] = []
        err_hi: List[float] = []
        for gi, (key, _) in enumerate(groups):
            v = rows[arm].get("{}_value".format(key))
            if v is None:
                continue  # skipped, never drawn as zero
            xs.append(gi - 0.4 + width * (i + 0.5))
            ys.append(v * scale)
            lo = rows[arm].get("{}_ci_lo".format(key))
            hi = rows[arm].get("{}_ci_hi".format(key))
            err_lo.append((v - lo) * scale if lo is not None else 0.0)
            err_hi.append((hi - v) * scale if hi is not None else 0.0)
        if not xs:
            continue
        bars = ax.bar(xs, ys, width=width * 0.92, color=ARM_COLOR.get(arm, SERIES[i]),
                      label=_arm_label(arm, short=False), linewidth=0)
        if any(e > 0 for e in err_lo + err_hi):
            ax.errorbar(xs, ys, yerr=[err_lo, err_hi], fmt="none",
                        ecolor=INK_2, elinewidth=0.9, capsize=2.5, alpha=0.75)
        # Direct value labels: required relief for the low-contrast hues.
        for b, y in zip(bars, ys):
            ax.annotate("{:.1f}".format(y), (b.get_x() + b.get_width() / 2, y),
                        textcoords="offset points", xytext=(0, 7 if err_hi else 3),
                        ha="center", fontsize=7, color=INK_2)

    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([g[1] for g in groups])
    ax.set_ylabel("Accuracy (%)" if pct else "Accuracy")
    ax.set_title("Accuracy by method and task group", loc="left", color=INK)
    _style_axes(ax)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
    return _save(fig, out_dir, "fig1_main_comparison")


# --------------------------------------------------------------------------
# Figure 2: per-task delta, proposed vs baseline 3
# --------------------------------------------------------------------------

def fig_per_task_delta(agg: Dict[str, Any], out_dir: str,
                       pct: bool = True) -> List[str]:
    """Horizontal diverging bars: the effect of the relation block per sub-task.

    This is the figure that tests the hypothesis' *shape*: the plan predicts gains
    concentrated on relational tasks and small changes elsewhere. Relational tasks
    are marked so a reader can see whether that pattern actually holds.

    Colour here encodes polarity (gain / loss), not identity, so it uses the
    diverging roles rather than the categorical slots.
    """
    plt = _mpl()
    if plt is None:
        return []
    sig = (agg.get("significance") or {}).get("per_task") or {}
    if not sig:
        LOG.warning("fig_per_task_delta: no per-task significance data")
        return []

    from ..data.taxonomy import relational_group

    items: List[Tuple[str, float, bool, Optional[float]]] = []
    for task, res in sig.items():
        if not isinstance(res, dict):
            continue
        d = res.get("delta")
        if d is None:
            continue
        items.append((task, float(d), relational_group(task) == "relational",
                      res.get("p_adjusted")))
    if not items:
        return []
    items.sort(key=lambda t: t[1])

    scale = 100.0 if pct else 1.0
    fig, ax = plt.subplots(figsize=(7.0, max(3.0, 0.32 * len(items) + 1.2)))
    ys = range(len(items))
    vals = [t[1] * scale for t in items]
    colors = [POS if v >= 0 else NEG for v in vals]
    ax.barh(list(ys), vals, color=colors, height=0.66, linewidth=0)

    labels = []
    for task, d, is_rel, p_adj in items:
        star = ""
        if p_adj is not None and p_adj < 0.05:
            star = " *"
        labels.append(("{}{}".format(task, star)) + ("  [R]" if is_rel else ""))
    ax.set_yticks(list(ys))
    ax.set_yticklabels(labels, fontsize=8)
    for tick, (_, _, is_rel, _) in zip(ax.get_yticklabels(), items):
        tick.set_color(INK if is_rel else INK_MUTED)
        if is_rel:
            tick.set_fontweight("bold")

    ax.axvline(0, color=INK_2, linewidth=0.9)
    for y, v in zip(ys, vals):
        ax.annotate("{:+.1f}".format(v), (v, y),
                    textcoords="offset points",
                    xytext=(5 if v >= 0 else -5, 0),
                    ha="left" if v >= 0 else "right", va="center",
                    fontsize=7, color=INK_2)

    ax.set_xlabel("Change in accuracy, percentage points (Proposed - Baseline 3)"
                  if pct else "Change (Proposed - Baseline 3)")
    ax.set_title("Effect of cross-tile spatial relations by sub-task",
                 loc="left", color=INK)
    pad = max(abs(min(vals)), abs(max(vals))) * 0.28 + 0.6
    ax.set_xlim(min(vals) - pad, max(vals) + pad)
    _style_axes(ax, ygrid=False, xgrid=True)
    ax.text(0.99, -0.14, "[R] = relational task (pre-registered).  * Holm-adjusted p < 0.05.",
            transform=ax.transAxes, ha="right", va="top", fontsize=7, color=INK_MUTED)
    return _save(fig, out_dir, "fig2_per_task_delta")


# --------------------------------------------------------------------------
# Figure 3: accuracy vs compute
# --------------------------------------------------------------------------

def fig_accuracy_vs_compute(agg: Dict[str, Any], out_dir: str,
                            pct: bool = True) -> List[str]:
    """Is the gain bought with compute or with structure? (plan section 9)

    Identity is carried by a direct text label on each point, not by colour, so
    the scatter needs only one hue - which also sidesteps the all-pairs colour
    gate that four categorical hues would fail.
    """
    plt = _mpl()
    if plt is None:
        return []
    main = {r["arm"]: r for r in agg.get("main", [])}
    comp = {r["arm"]: r for r in agg.get("compute", [])}
    arms = [a for a in ARM_ORDER if a in main and a in comp]
    if len(arms) < 2:
        LOG.warning("fig_accuracy_vs_compute: need >= 2 arms")
        return []

    scale = 100.0 if pct else 1.0
    xs, ys, names = [], [], []
    for arm in arms:
        x = comp[arm].get("mean_vlm_calls")
        y = main[arm].get("overall_value")
        if x is None or y is None:
            continue
        xs.append(float(x))
        ys.append(float(y) * scale)
        names.append(arm)
    if len(xs) < 2:
        return []

    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    # Connect in pipeline order to show the progression as a path.
    order = sorted(range(len(names)), key=lambda i: ARM_ORDER.index(names[i]))
    ax.plot([xs[i] for i in order], [ys[i] for i in order],
            color=INK_MUTED, linewidth=1.0, linestyle="--", zorder=1, alpha=0.8)
    ax.scatter(xs, ys, s=64, color=SERIES[0], zorder=3,
               edgecolor=SURFACE, linewidth=2.0)

    for x, y, name in zip(xs, ys, names):
        ax.annotate(_arm_label(name).replace("\n", " "), (x, y),
                    textcoords="offset points", xytext=(8, 5),
                    fontsize=7.5, color=INK_2)

    ax.set_xlabel("Mean VLM calls per sample")
    ax.set_ylabel("Overall accuracy (%)" if pct else "Overall accuracy")
    ax.set_title("Accuracy against inference cost", loc="left", color=INK)
    ax.set_xlim(left=0)
    _style_axes(ax)
    return _save(fig, out_dir, "fig3_accuracy_vs_compute")


# --------------------------------------------------------------------------
# Figure 4: progression
# --------------------------------------------------------------------------

def fig_progression(agg: Dict[str, Any], out_dir: str, pct: bool = True) -> List[str]:
    """B1 -> B2 -> B3 -> Proposed for the two task groups.

    Two series (relational, non-relational) on ONE axis. The plan's narrative
    predicts the two lines diverge at the final step; this figure is where that is
    either visible or not.
    """
    plt = _mpl()
    if plt is None:
        return []
    rows = {r["arm"]: r for r in agg.get("main", [])}
    arms = [a for a in ARM_ORDER if a in rows]
    if len(arms) < 2:
        return []

    scale = 100.0 if pct else 1.0
    fig, ax = plt.subplots(figsize=(6.0, 3.4))
    for si, (key, label) in enumerate((("relational", "Relational tasks"),
                                       ("non_relational", "Non-relational tasks"))):
        xs, ys = [], []
        for i, arm in enumerate(arms):
            v = rows[arm].get("{}_value".format(key))
            if v is None:
                continue
            xs.append(i)
            ys.append(v * scale)
        if not xs:
            continue
        ax.plot(xs, ys, marker="o", color=SERIES[si], label=label,
                markeredgecolor=SURFACE, markeredgewidth=1.6)
        # Label only the endpoints, not every point.
        for idx in ({0, len(xs) - 1} if len(xs) > 1 else {0}):
            ax.annotate("{:.1f}".format(ys[idx]), (xs[idx], ys[idx]),
                        textcoords="offset points", xytext=(0, 9),
                        ha="center", fontsize=7.5, color=INK_2)

    ax.set_xticks(range(len(arms)))
    ax.set_xticklabels([_arm_label(a) for a in arms], fontsize=8)
    ax.set_ylabel("Accuracy (%)" if pct else "Accuracy")
    ax.set_title("Experimental progression by task group", loc="left", color=INK)
    _style_axes(ax)
    ax.legend(loc="best")
    return _save(fig, out_dir, "fig4_progression")


# --------------------------------------------------------------------------
# Figure 5: cross-tile structure
# --------------------------------------------------------------------------

def fig_cross_tile_structure(results_dir: str, out_dir: str,
                             arm: str = "proposed_ctsr") -> List[str]:
    """Distribution of the cross-tile relation fraction per scene.

    A descriptive result that stands on its own: it measures how much of the
    relational structure in an ultra-high-resolution scene spans tiles, and
    therefore how much independent tiling structurally cannot see.
    """
    plt = _mpl()
    if plt is None:
        return []
    from ..utils.io_utils import load_jsonl

    path = Path(results_dir) / arm / "predictions.jsonl"
    if not path.exists():
        LOG.warning("fig_cross_tile_structure: %s not found", path)
        return []
    fracs: List[float] = []
    counts: List[int] = []
    for r in load_jsonl(path):
        gs = (r.get("artifacts") or {}).get("graph_stats") or {}
        f = gs.get("cross_tile_fraction")
        if f is not None and (gs.get("n_relations") or 0) > 0:
            fracs.append(float(f))
            counts.append(int(gs.get("n_cross_tile") or 0))
    if not fracs:
        LOG.warning("fig_cross_tile_structure: no graph statistics recorded")
        return []

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0))
    ax1.hist(fracs, bins=min(20, max(5, len(set(fracs)))), color=SERIES[0],
             edgecolor=SURFACE, linewidth=0.8)
    mean_f = sum(fracs) / len(fracs)
    ax1.axvline(mean_f, color=INK_2, linewidth=1.2, linestyle="--")
    ax1.annotate("mean {:.2f}".format(mean_f), (mean_f, ax1.get_ylim()[1] * 0.92),
                 textcoords="offset points", xytext=(6, 0), fontsize=7.5, color=INK_2)
    ax1.set_xlabel("Fraction of relations spanning tiles")
    ax1.set_ylabel("Scenes")
    ax1.set_title("Cross-tile relation share", loc="left", color=INK)
    _style_axes(ax1)

    ax2.hist(counts, bins=min(20, max(5, len(set(counts)))), color=SERIES[2],
             edgecolor=SURFACE, linewidth=0.8)
    mean_c = sum(counts) / len(counts)
    ax2.axvline(mean_c, color=INK_2, linewidth=1.2, linestyle="--")
    ax2.annotate("mean {:.1f}".format(mean_c), (mean_c, ax2.get_ylim()[1] * 0.92),
                 textcoords="offset points", xytext=(6, 0), fontsize=7.5, color=INK_2)
    ax2.set_xlabel("Number of cross-tile relations")
    ax2.set_ylabel("Scenes")
    ax2.set_title("Cross-tile relation count", loc="left", color=INK)
    _style_axes(ax2)

    fig.suptitle("Relational structure invisible to independent tiling",
                 x=0.005, ha="left", fontsize=10, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    return _save(fig, out_dir, "fig5_cross_tile_structure")


# --------------------------------------------------------------------------
# Figure 6: error taxonomy
# --------------------------------------------------------------------------

def fig_error_taxonomy(taxonomy: Dict[str, Any], out_dir: str) -> List[str]:
    """Error categories for the proposed method (plan section 10). One series."""
    plt = _mpl()
    if plt is None:
        return []
    counts = (taxonomy or {}).get("counts") or {}
    items = [(k, v) for k, v in counts.items() if v]
    if not items:
        LOG.warning("fig_error_taxonomy: no error counts")
        return []
    items.sort(key=lambda kv: kv[1])

    fig, ax = plt.subplots(figsize=(6.2, max(2.6, 0.34 * len(items) + 1.1)))
    labels = [k.replace("_", " ") for k, _ in items]
    vals = [v for _, v in items]
    ax.barh(range(len(items)), vals, color=SERIES[1], height=0.64, linewidth=0)
    ax.set_yticks(range(len(items)))
    ax.set_yticklabels(labels, fontsize=8)
    total = sum(vals) or 1
    for i, v in enumerate(vals):
        ax.annotate("{} ({:.0f}%)".format(v, 100.0 * v / total), (v, i),
                    textcoords="offset points", xytext=(5, 0), va="center",
                    fontsize=7.5, color=INK_2)
    ax.set_xlabel("Failed samples")
    ax.set_title("Error categories, proposed method", loc="left", color=INK)
    ax.set_xlim(0, max(vals) * 1.22)
    _style_axes(ax, ygrid=False, xgrid=True)
    return _save(fig, out_dir, "fig6_error_taxonomy")


# --------------------------------------------------------------------------
# Figure 7: ablation
# --------------------------------------------------------------------------

def fig_ablation(rows: Sequence[Dict[str, Any]], out_dir: str,
                 pct: bool = True) -> List[str]:
    """Ablation variants against the full method. One series; polarity by sign."""
    plt = _mpl()
    if plt is None:
        return []
    items = [(r.get("variant", "?"), r.get("relational"), r.get("non_relational"))
             for r in rows if r.get("relational") is not None]
    if not items:
        return []
    scale = 100.0 if pct else 1.0

    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    n = len(items)
    width = 0.38
    xs = list(range(n))
    rel = [(i[1] or 0) * scale for i in items]
    non = [(i[2] or 0) * scale for i in items]

    b1 = ax.bar([x - width / 2 for x in xs], rel, width=width * 0.94,
                color=SERIES[0], label="Relational tasks", linewidth=0)
    b2 = ax.bar([x + width / 2 for x in xs], non, width=width * 0.94,
                color=SERIES[1], label="Non-relational tasks", linewidth=0)
    for bars, vals in ((b1, rel), (b2, non)):
        for b, v in zip(bars, vals):
            ax.annotate("{:.1f}".format(v), (b.get_x() + b.get_width() / 2, v),
                        textcoords="offset points", xytext=(0, 3), ha="center",
                        fontsize=7, color=INK_2)

    ax.set_xticks(xs)
    ax.set_xticklabels([i[0].replace("_", "\n") for i in items], fontsize=7.5)
    ax.set_ylabel("Accuracy (%)" if pct else "Accuracy")
    ax.set_title("Component ablation", loc="left", color=INK)
    _style_axes(ax)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2)
    return _save(fig, out_dir, "fig7_ablation")


# --------------------------------------------------------------------------

def write_all(agg: Dict[str, Any], out_dir: str, results_dir: Optional[str] = None,
              taxonomy: Optional[Dict[str, Any]] = None,
              ablation_rows: Optional[Sequence[Dict[str, Any]]] = None,
              pct: bool = True) -> Dict[str, Any]:
    """Generate every figure, tolerating individual failures."""
    out: Dict[str, Any] = {}
    jobs = [
        ("fig1_main", lambda: fig_main(agg, out_dir, pct)),
        ("fig2_per_task_delta", lambda: fig_per_task_delta(agg, out_dir, pct)),
        ("fig3_accuracy_vs_compute", lambda: fig_accuracy_vs_compute(agg, out_dir, pct)),
        ("fig4_progression", lambda: fig_progression(agg, out_dir, pct)),
    ]
    if results_dir:
        jobs.append(("fig5_cross_tile", lambda: fig_cross_tile_structure(results_dir, out_dir)))
    if taxonomy:
        jobs.append(("fig6_error_taxonomy", lambda: fig_error_taxonomy(taxonomy, out_dir)))
    if ablation_rows:
        jobs.append(("fig7_ablation", lambda: fig_ablation(ablation_rows, out_dir, pct)))

    for name, fn in jobs:
        try:
            out[name] = fn()
        except Exception as exc:
            LOG.exception("Figure '%s' failed", name)
            out[name] = {"error": str(exc)}
    return out
