#!/usr/bin/env python
"""Publication figures for the manuscript.

Reads analysis/stats.json (produced by analyze.py) and writes vector PDFs (plus
300-dpi PNG previews) into ../figures/.

Style follows Springer artwork guidance (the venue publishes in Springer LNNS):
  * final size: full text width of the llncs class = 122 mm; no rescaling in LaTeX
  * sans-serif lettering (Arial), 7-8 pt, consistent across figures
  * line widths >= 0.5 pt (Springer minimum is 0.3 pt)
  * vector PDF with embedded TrueType fonts (pdf.fonttype = 42)
  * colour-blind-safe palette, with a secondary encoding (marker shape / label)
    so no figure relies on colour alone

Colour carries ONE meaning throughout the paper: task group
(blue = non-relational, orange = relational, grey = held out). Methods are
distinguished by position, marker and direct labels, never by hue.

    python analysis/make_figures.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
FIG = HERE.parent / "figures"
FIG.mkdir(parents=True, exist_ok=True)

MM = 1 / 25.4
FULL = 122 * MM          # llncs \textwidth

# Validated categorical slots (CVD-checked): slot 1 blue, slot 2 orange.
C_NON = "#2a78d6"
C_REL = "#eb6834"
C_HELD = "#8a8980"
INK = "#1a1a1a"
INK2 = "#4d4d4d"
MUTED = "#8a8980"
GRID = "#e3e3e3"
HILITE = "#fdf1d6"   # tint for the manipulated component in the schematic
HILITE_EDGE = "#c98500"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "font.size": 7.5,
    "axes.titlesize": 8,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.5,
    "ytick.major.size": 2.5,
    "lines.linewidth": 1.0,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "text.color": INK,
    "legend.frameon": False,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.dpi": 300,
    "figure.dpi": 150,
})

ARM_SHORT = {"b1_direct": "B1\nDirect", "b2_tiling": "B2\nTiling",
             "b3_selected": "B3\nSelection", "proposed_ctsr": "Proposed\n+relations"}
ARMS = ["b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"]

TASK_SHORT = {
    "Object Spatial Relationship": "Object spatial relationship",
    "Regional Counting": "Regional counting",
    "Counting with Complex Reasoning": "Counting w/ complex reasoning",
    "Route Planning": "Route planning",
    "Object Classification": "Object classification",
    "Object Color": "Object colour",
    "Object Motion State": "Object motion state",
    "Overall Counting": "Overall counting",
    "Regional Land Use Classification": "Regional land use",
    "Overall Land Use Classification": "Overall land use",
    "Environmental Condition Reasoning": "Environmental condition",
    "Anomaly Detection and Interpretation": "Anomaly detection",
    "Counting/Counting with changing detection": "Bi-temporal counting†",
}


def style(ax, grid_axis="y"):
    ax.set_axisbelow(True)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def panel(ax, letter, x=-0.02, y=1.02):
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=9, fontweight="bold",
            va="bottom", ha="right")


def save(fig, stem):
    for ext in ("pdf", "png"):
        fig.savefig(FIG / "{}.{}".format(stem, ext), bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print("wrote", stem)


def gcol(group):
    return {"relational": C_REL, "non_relational": C_NON}.get(group, C_HELD)


# ---------------------------------------------------------------------------
# Figure 1: pipeline schematic
# ---------------------------------------------------------------------------
def fig_pipeline(S):
    # Axis units are millimetres at final print size, so text widths can be
    # budgeted: 6 pt Arial is roughly 1.1 mm per character.
    W, H = 122, 50
    fig = plt.figure(figsize=(W * MM, H * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    def box(x, y, w, h, title, sub, fill="white", edge=INK2, ls="-", lw=0.7):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.5",
                                    fc=fill, ec=edge, lw=lw, ls=ls))
        ax.text(x + w / 2, y + h - 1.8, title, ha="center", va="top", fontsize=6.6,
                fontweight="bold")
        ax.text(x + w / 2, y + h - 5.6, sub, ha="center", va="top", fontsize=5.8,
                color=INK2, linespacing=1.2)

    def arrow(p0, p1, color=INK2, ls="-", rad=0.0):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=6,
                                     lw=0.7, color=color, ls=ls, shrinkA=0, shrinkB=0,
                                     connectionstyle="arc3,rad={}".format(rad)))

    E = S["extraction"]
    cfg = S.get("config") or {}
    tile = (cfg.get("tiling") or {}).get("tile_size", 1024)
    ov = (cfg.get("tiling") or {}).get("overlap", 128)
    topk = (cfg.get("selection") or {}).get("top_k", 5)

    # row 1: perception front end
    y1, h1, w = 30, 15, 26
    xs = [2, 33, 64, 95]
    box(xs[0], y1, w, h1, "Input", "UHR image (~8,500$^2$ px)\n+ question")
    box(xs[1], y1, w, h1, "Tiling", "{} px, overlap {}\n$\\approx${:.0f} tiles / scene".format(
        tile, ov, E["mean_tiles_total"]))
    box(xs[2], y1, w, h1, "Tile selection", "saliency + CLIP\nquestion score; top-{}".format(topk))
    box(xs[3], y1, w, h1, "Local extraction", "VLM on each crop:\nlabels + boxes\n({} calls)".format(topk))
    for i in range(3):
        arrow((xs[i] + w + 0.4, y1 + h1 / 2), (xs[i + 1] - 0.4, y1 + h1 / 2))

    # elbow from extraction down to registration
    ex = xs[3] + w / 2
    ax.plot([ex, ex, 15, 15], [y1 - 0.3, 26, 26, 24.6], color=INK2, lw=0.7)
    arrow((15, 24.8), (15, 22.4))

    # row 2: registration, relations, final call
    y2, h2 = 7, 15
    box(2, y2, w, h2, "Registration", "crop $\\rightarrow$ global pixels;\ncross-tile dedup")
    box(33, y2, 27, h2, "Relation graph", "direction, distance,\nadjacency, contain-\nment, intersection",
        fill=HILITE, edge=HILITE_EDGE, ls="--", lw=0.9)
    box(66, y2, 38, h2, "Final VLM call (1)",
        "overview + 3 crops +\nobject list (+ relations)")
    arrow((28.4, y2 + h2 / 2 + 2), (32.6, y2 + h2 / 2 + 2))
    arrow((60.4, y2 + h2 / 2 + 2), (65.6, y2 + h2 / 2 + 2), color=HILITE_EDGE, ls="--")
    # object list bypasses the relation block (this is what B3 receives)
    arrow((20, y2 - 0.3), (78, y2 - 0.3), rad=0.18)
    ax.text(46.5, 4.4, "object list (both Selection and Proposed)", ha="center", va="center", fontsize=5.6,
            color=INK2)
    ax.text(46.5, y2 + h2 + 1.0, "Proposed only", ha="center", fontsize=5.8,
            color=HILITE_EDGE, fontstyle="italic")
    arrow((104.4, y2 + h2 / 2), (109, y2 + h2 / 2))
    ax.text(110, y2 + h2 / 2, "answer", va="center", fontsize=6.6)
    save(fig, "fig1_pipeline")


# ---------------------------------------------------------------------------
# Figure 2: (a) accuracy by arm and group; (b) paired effects
# ---------------------------------------------------------------------------
def fig_crossover(S):
    """Two grouped bar charts: accuracy by method, then the paired effects."""
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL, 50 * MM),
                               gridspec_kw={"width_ratios": [1.25, 1.0], "wspace": 0.30})

    # (a) accuracy by method and task group
    A = S["accuracy"]
    w = 0.36
    xs = list(range(len(ARMS)))
    for g, off, hatch in (("non_relational", -w / 2, None), ("relational", w / 2, None)):
        v = [100 * A[arm][g]["acc"] for arm in ARMS]
        lo = [100 * (A[arm][g]["acc"] - A[arm][g]["lo"]) for arm in ARMS]
        hi = [100 * (A[arm][g]["hi"] - A[arm][g]["acc"]) for arm in ARMS]
        x = [i + off for i in xs]
        lab = "Non-relational" if g == "non_relational" else "Relational"
        a.bar(x, v, width=w, color=gcol(g), lw=0, label=lab, zorder=2)
        a.errorbar(x, v, yerr=[lo, hi], fmt="none", ecolor=INK2, elinewidth=0.6,
                   capsize=1.5, capthick=0.6, zorder=3)
        for xi, vi, hii in zip(x, v, hi):
            a.text(xi, vi + hii + 0.8, "{:.1f}".format(vi), ha="center", va="bottom",
                   fontsize=5.8, color=INK2)
    a.axhline(25, color=MUTED, lw=0.6, ls=":", zorder=1)
    a.text(-0.45, 25.6, "chance", fontsize=5.8, color=MUTED, ha="left", va="bottom")
    a.set_xticks(xs)
    a.set_xticklabels(["Direct", "Tiling", "Selection", "Proposed"], fontsize=6.6)
    a.set_xlim(-0.55, 3.55)
    a.set_ylim(0, 58)
    a.set_yticks([0, 10, 20, 30, 40, 50])
    a.set_ylabel("Accuracy (%)")
    a.legend(loc="upper left", ncol=2, handlelength=1.3, columnspacing=1.0,
             borderaxespad=0.1, fontsize=6.4)
    style(a)
    a.tick_params(axis="x", length=0)
    panel(a, "a", x=-0.12)

    # (b) paired changes, same colour code
    P = S["pairwise"]
    rows = [("b1_direct__b2_tiling", "Direct $\\rightarrow$\nTiling"),
            ("b1_direct__b3_selected", "Direct $\\rightarrow$\nSelection"),
            ("b3_selected__proposed_ctsr", "Selection $\\rightarrow$\nProposed")]
    w2 = 0.34
    for i, (key, _) in enumerate(rows):
        for g, off in (("non_relational", -w2 / 2), ("relational", w2 / 2)):
            e = P[key][g]
            d = 100 * e["delta"]
            err = [[d - 100 * e["lo"]], [100 * e["hi"] - d]]
            b.bar([i + off], [d], width=w2, color=gcol(g), lw=0, zorder=2)
            b.errorbar([i + off], [d], yerr=err, fmt="none", ecolor=INK2, elinewidth=0.6,
                       capsize=1.5, capthick=0.6, zorder=3)
            star = "***" if e["p"] < 1e-3 else ("**" if e["p"] < 1e-2 else
                                                ("*" if e["p"] < 0.05 else "n.s."))
            top = 100 * e["hi"] if d >= 0 else 100 * e["lo"]
            b.text(i + off, top + (0.5 if d >= 0 else -0.5), "{:+.1f} {}".format(d, star),
                   ha="center", va="bottom" if d >= 0 else "top", fontsize=5.6, color=INK2)
    b.axhline(0, color=INK, lw=0.7, zorder=4)
    b.set_xticks(range(len(rows)))
    b.set_xticklabels([r[1].replace("\\n", "\n") for r in rows], fontsize=6.0,
                      linespacing=1.3)
    b.set_xlim(-0.55, len(rows) - 0.45)
    b.set_ylim(-11, 10)
    b.set_yticks([-10, -5, 0, 5, 10])
    b.set_ylabel("Change in accuracy (pp)")
    style(b)
    b.tick_params(axis="x", length=0)
    panel(b, "b", x=-0.14)
    save(fig, "fig2_crossover")


# ---------------------------------------------------------------------------
# Figure 3: per-task paired effects
# ---------------------------------------------------------------------------
def fig_per_task(S, min_n=20):
    T = S["per_task"]
    items = [(t, r) for t, r in T.items() if r["b3_vs_p"] and r["b3_vs_p"]["n"] >= min_n]
    order = {"relational": 0, "non_relational": 1}
    items.sort(key=lambda kv: (order.get(kv[1]["group"], 2), -kv[1]["b1_vs_b3"]["delta"]))

    fig, axes = plt.subplots(1, 2, figsize=(FULL, 55 * MM), sharey=True,
                             gridspec_kw={"wspace": 0.08})
    for ax, key, title in ((axes[0], "b1_vs_b3", "Zoom: Direct $\\rightarrow$ Selection"),
                           (axes[1], "b3_vs_p", "Relations: Selection $\\rightarrow$ Proposed")):
        for i, (t, r) in enumerate(items):
            e = r[key]
            y = len(items) - 1 - i
            c = gcol(r["group"])
            ax.plot([100 * e["lo"], 100 * e["hi"]], [y, y], color=c, lw=1.1)
            mk = "s" if r["group"] == "relational" else ("o" if r["group"] == "non_relational" else "D")
            ax.plot(100 * e["delta"], y, marker=mk, color=c, ms=3.6, mec="white", mew=0.5)
            if e.get("p_holm") is not None and e["p_holm"] < 0.05:
                ax.text(100 * e["hi"] + 0.8, y, "*", va="center", fontsize=8, color=c)
        ax.axvline(0, color=INK2, lw=0.6)
        ax.set_title(title, fontsize=7.5, loc="left")
        ax.set_xlim(-26, 26)
        ax.set_xlabel("Paired change (pp), 95% CI")
        style(ax, grid_axis="x")
    axes[0].set_yticks(range(len(items)))
    axes[0].set_yticklabels(["{} (n={})".format(TASK_SHORT.get(t, t), r["b3_vs_p"]["n"])
                             for t, r in reversed(items)], fontsize=6.4)
    for tick, (t, r) in zip(axes[0].get_yticklabels(), list(reversed(items))):
        tick.set_color(gcol(r["group"]))
    axes[0].tick_params(axis="y", length=0)
    # separator between groups
    n_rel = sum(1 for _, r in items if r["group"] == "relational")
    for ax in axes:
        ax.axhline(len(items) - n_rel - 0.5, color=GRID, lw=0.8)
    save(fig, "fig3_per_task")


# ---------------------------------------------------------------------------
# Figure 4: why the relation block did not help
# ---------------------------------------------------------------------------
def fig_mechanism(S):
    fig = plt.figure(figsize=(FULL, 47 * MM))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.25, 1.0], wspace=0.55)
    a, b = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])

    # (a) zero-object extraction rate per task
    T = S["per_task"]
    items = [(t, r) for t, r in T.items() if r["b3_vs_p"] and r["b3_vs_p"]["n"] >= 20]
    items.sort(key=lambda kv: kv[1]["zero_object_rate"])
    ys = range(len(items))
    a.barh(list(ys), [100 * r["zero_object_rate"] for _, r in items], height=0.66,
           color=[gcol(r["group"]) for _, r in items], lw=0)
    for y, (_, r) in zip(ys, items):
        a.text(100 * r["zero_object_rate"] + 1.5, y, "{:.0f}".format(100 * r["zero_object_rate"]),
               va="center", fontsize=5.8, color=INK2)
    a.set_yticks(list(ys))
    a.set_yticklabels([TASK_SHORT.get(t, t) for t, _ in items], fontsize=6.3)
    a.set_xlim(0, 112)
    a.set_xticks([0, 25, 50, 75, 100])
    a.set_xlabel("Scenes with no object extracted (%)")
    style(a, grid_axis="x")
    a.tick_params(axis="y", length=0)
    zr = 100 * S["extraction"]["zero_object_rate"]
    a.axvline(zr, color=INK2, lw=0.6, ls="--")
    a.text(zr + 1.5, len(items) - 0.35, "all tasks: {:.0f}%".format(zr), fontsize=6.0,
           color=INK2, va="bottom")
    panel(a, "a", x=-0.02, y=1.03)

    # (b) B3 -> Proposed, stratified by what the relation block contained
    st = S["stratified_b3_vs_p"]
    strata = [("no_relations", "none"), ("has_relations", "any"),
              ("has_cross_tile", "cross-tile")]
    for i, (sk, _) in enumerate(strata):
        for g, mk, off in (("non_relational", "o", -0.13), ("relational", "s", 0.13)):
            e = st[sk][g]
            if not e:
                continue
            x = i + off
            b.plot([x, x], [100 * e["lo"], 100 * e["hi"]], color=gcol(g), lw=1.1)
            b.plot(x, 100 * e["delta"], marker=mk, color=gcol(g), ms=4, mec="white", mew=0.5)
    b.axhline(0, color=INK2, lw=0.6)
    labels = []
    for sk, lab in strata:
        o = st[sk]["overall"]
        labels.append("{}\nn={:,}\nΔans {:.0f}%".format(lab, o["n"], 100 * o["answer_change_rate"]))
    b.set_xticks(range(len(strata)))
    b.set_xticklabels(labels, fontsize=6.2, linespacing=1.15)
    b.set_xlabel("Relations available")
    b.set_ylim(-9, 9)
    b.set_xlim(-0.5, 2.5)
    b.set_ylabel("Selection $\\rightarrow$ Proposed (pp), 95% CI")
    b.plot([], [], color=C_NON, marker="o", ms=4, mec="white", mew=0.5, label="Non-relational")
    b.plot([], [], color=C_REL, marker="s", ms=4, mec="white", mew=0.5, label="Relational")
    b.legend(loc="upper left", fontsize=6.2, handlelength=1.4, borderaxespad=0.1)
    style(b)
    panel(b, "b", x=-0.05, y=1.03)
    save(fig, "fig4_mechanism")


def fig_objects_confound(S):
    """Appendix: accuracy rises with object count for every arm, including B1,
    which never receives objects -> the association reflects scene/task mix."""
    fig, c = plt.subplots(figsize=(80 * MM, 50 * MM))
    AB = S["acc_by_objects"]
    labs = list(AB.keys())
    x = list(range(len(labs)))
    specs = (("b1_direct", "^", ":", MUTED, "Direct (never sees objects)"),
             ("b3_selected", "o", "--", INK2, "Selection"),
             ("proposed_ctsr", "s", "-", INK, "Proposed"))
    for arm, mk, ls, col, name in specs:
        v = [100 * AB[l][arm]["acc"] for l in labs]
        c.plot(x, v, marker=mk, ls=ls, color=col, lw=0.9, ms=3.6, mec="white", mew=0.5,
               label=name)
    for i, l in enumerate(labs):
        c.text(i, 29.5, "n={}\n{:.0f}% rel.".format(AB[l]["n"], 100 * AB[l]["rel_share"]),
               ha="center", fontsize=5.4, color=MUTED, va="bottom")
    c.set_xticks(x)
    c.set_xticklabels(labs)
    c.set_ylim(29, 68)
    c.set_xlim(-0.45, len(labs) - 0.55)
    c.set_xlabel("Objects extracted per scene (Proposed)")
    c.set_ylabel("Accuracy (%)")
    c.legend(loc="upper left", fontsize=6.2, handlelength=2.2)
    style(c)
    save(fig, "figA_objects_confound")


# ---------------------------------------------------------------------------
# Appendix figure: qualitative overlays (raster, reused from the pipeline output)
# ---------------------------------------------------------------------------
def fig_qualitative(results_report: Path):
    try:
        from PIL import Image
    except ImportError:
        print("Pillow missing; skipping qualitative figure")
        return
    q = results_report / "qualitative"
    picks = [("qual_graph_wins_idx26_118e8cc4ea.png", "figA_qual_win.jpg"),
             ("qual_graph_losses_idx157_c703d23845.png", "figA_qual_loss.jpg")]
    for src, dst in picks:
        p = q / src
        if not p.exists():
            print("missing", p)
            continue
        im = Image.open(p).convert("RGB")
        im.thumbnail((1500, 1500))
        im.save(FIG / dst, quality=90, optimize=True)
        print("wrote", dst)


def main():
    import figs_v2
    S = json.loads((HERE / "stats.json").read_text(encoding="utf-8"))
    fig_pipeline(S)
    fig_crossover(S)
    figs_v2.fig_per_task(S, plt, save, style, TASK_SHORT, MM, FULL)
    figs_v2.fig_mechanism(S, plt, save, style, panel, TASK_SHORT, MM, FULL)
    fig_objects_confound(S)
    fig_qualitative(HERE.parent / "results" / "main" / "report")


if __name__ == "__main__":
    main()
