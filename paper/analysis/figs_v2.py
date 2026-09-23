"""Revised Figures 3 and 4 (grouped bars; rotated axis labels with value labels).

Imported by make_figures.py, which calls fig_per_task and fig_mechanism from here.
"""
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

SERIES_ZOOM = "#5b6b7f"      # slate: effect of zooming (Direct -> Selection)
SERIES_REL = "#c98500"       # amber: effect of the relation block (same accent as Fig. 1)
C_NON = "#2a78d6"
C_REL = "#eb6834"
C_HELD = "#8a8980"
INK, INK2, GRID = "#1a1a1a", "#4d4d4d", "#e3e3e3"


def _gcol(g):
    return {"relational": C_REL, "non_relational": C_NON}.get(g, C_HELD)


def fig_per_task(S, plt, save, style, TASK_SHORT, MM, FULL, min_n=20):
    T = S["per_task"]
    order = {"relational": 0, "non_relational": 1}
    items = [(t, r) for t, r in T.items() if r["b3_vs_p"] and r["b3_vs_p"]["n"] >= min_n]
    items.sort(key=lambda kv: (order.get(kv[1]["group"], 2), -kv[1]["b1_vs_b3"]["delta"]))

    fig, ax = plt.subplots(figsize=(FULL, 60 * MM))
    h = 0.36
    y = 0.0
    ypos, labels, seps, heads = [], [], [], []
    last = None
    for t, r in items:
        g = r["group"]
        if g != last:
            if last is not None:
                seps.append(y + 0.35)
                y -= 0.45
            heads.append((y + 0.05, {"relational": "Relational tasks",
                                     "non_relational": "Non-relational tasks"}.get(g, "Held out")))
            y -= 0.55
            last = g
        ypos.append(y)
        labels.append("{} (n={})".format(TASK_SHORT.get(t, t), r["b3_vs_p"]["n"]))
        y -= 1.0

    for yy, (t, r) in zip(ypos, items):
        for key, off, col in (("b1_vs_b3", h / 2, SERIES_ZOOM), ("b3_vs_p", -h / 2, SERIES_REL)):
            e = r[key]
            d, lo, hi = 100 * e["delta"], 100 * e["lo"], 100 * e["hi"]
            ax.barh(yy + off, d, height=h * 0.92, color=col, lw=0)
            ax.plot([lo, hi], [yy + off] * 2, color=INK2, lw=0.6, zorder=3)
            ax.plot([lo, lo], [yy + off - 0.07, yy + off + 0.07], color=INK2, lw=0.6, zorder=3)
            ax.plot([hi, hi], [yy + off - 0.07, yy + off + 0.07], color=INK2, lw=0.6, zorder=3)
            if e.get("p_holm") is not None and e["p_holm"] < 0.05:
                x_txt = hi + 0.8 if d >= 0 else lo - 0.8
                ax.text(x_txt, yy + off, "*", va="center",
                        ha="left" if d >= 0 else "right", fontsize=7, color=INK2)

    ax.axvline(0, color=INK, lw=0.7)
    ax.set_yticks(ypos)
    ax.set_yticklabels(labels, fontsize=6.4)
    for tick, (t, r) in zip(ax.get_yticklabels(), items):
        tick.set_color(INK)
    for yy, txt in heads:
        ax.text(-33.5, yy, txt, fontsize=6.6, fontweight="bold", va="center", ha="left",
                color=_gcol("relational" if txt.startswith("Relational") else
                            "non_relational" if txt.startswith("Non") else "held"),
                transform=ax.get_yaxis_transform() if False else ax.transData)
    for s in seps:
        ax.axhline(s - 0.4, color=GRID, lw=0.8)
    ax.set_xlim(-33.5, 33.5)
    ax.set_ylim(min(ypos) - 0.7, 0.4)
    ax.set_xlabel("Paired change in accuracy (pp), 95% CI")
    style(ax, grid_axis="x")
    ax.tick_params(axis="y", length=0)
    handles = [Patch(color=SERIES_ZOOM, label="Zoom: Direct $\\rightarrow$ Selection"),
               Patch(color=SERIES_REL, label="Relations: Selection $\\rightarrow$ Proposed"),
               Line2D([], [], color=INK2, lw=0.6, label="95% CI")]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3,
              frameon=False, fontsize=6.3, handlelength=1.6)
    save(fig, "figA_per_task")


def fig_mechanism(S, plt, save, style, panel, TASK_SHORT, MM, FULL):
    fig = plt.figure(figsize=(FULL, 50 * MM))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.45, 1.0], wspace=0.38)
    a, b = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])

    # (a) vertical bars, rotated task labels, value on each bar
    T = S["per_task"]
    items = [(t, r) for t, r in T.items() if r["b3_vs_p"] and r["b3_vs_p"]["n"] >= 20]
    items.sort(key=lambda kv: -kv[1]["zero_object_rate"])
    xs = list(range(len(items)))
    vals = [100 * r["zero_object_rate"] for _, r in items]
    a.bar(xs, vals, width=0.7, color=[_gcol(r["group"]) for _, r in items], lw=0)
    for x, v in zip(xs, vals):
        a.text(x, v + 1.5, "{:.0f}".format(v), ha="center", va="bottom", fontsize=5.6, color=INK2)
    a.set_xticks(xs)
    SHORT = {"Object Motion State": "Motion state", "Object Color": "Colour",
             "Object Classification": "Classification", "Regional Counting": "Regional count",
             "Counting with Complex Reasoning": "Complex count",
             "Counting/Counting with changing detection": "Bi-temporal count",
             "Object Spatial Relationship": "Spatial relation", "Route Planning": "Route planning",
             "Anomaly Detection and Interpretation": "Anomaly", "Overall Counting": "Overall count",
             "Regional Land Use Classification": "Regional land use",
             "Environmental Condition Reasoning": "Environment"}
    a.set_xticklabels([SHORT.get(t, t) for t, _ in items],
                      rotation=40, ha="right", rotation_mode="anchor", fontsize=6.0)
    a.set_ylim(0, 112)
    a.set_yticks([0, 25, 50, 75, 100])
    a.set_ylabel("Scenes with no object extracted (%)")
    zr = 100 * S["extraction"]["zero_object_rate"]
    a.axhline(zr, color=INK2, lw=0.6, ls="--")
    a.text(len(items) - 0.5, zr + 1.5, "all tasks: {:.0f}%".format(zr), ha="right",
           va="bottom", fontsize=5.8, color=INK2)
    style(a)
    a.tick_params(axis="x", length=0)
    a.legend(handles=[Patch(color=C_REL, label="relational"),
                      Patch(color=C_NON, label="non-relational"),
                      Patch(color=C_HELD, label="held out")],
             loc="upper right", bbox_to_anchor=(1.0, 0.93), fontsize=5.8, frameon=False,
             handlelength=1.1)
    panel(a, "a", x=-0.02, y=1.02)

    # (b) stratified Selection -> Proposed, as grouped bars with 95% CIs
    st = S["stratified_b3_vs_p"]
    strata = [("no_relations", "none"), ("has_relations", "any"), ("has_cross_tile", "cross-tile")]
    wb = 0.34
    for i, (sk, _) in enumerate(strata):
        for g, off in (("non_relational", -wb / 2), ("relational", wb / 2)):
            e = st[sk][g]
            if not e:
                continue
            d = 100 * e["delta"]
            err = [[d - 100 * e["lo"]], [100 * e["hi"] - d]]
            b.bar([i + off], [d], width=wb, color=_gcol(g), lw=0, zorder=2)
            b.errorbar([i + off], [d], yerr=err, fmt="none", ecolor=INK2, elinewidth=0.6,
                       capsize=1.5, capthick=0.6, zorder=3)
            top = 100 * e["hi"] if d >= 0 else 100 * e["lo"]
            b.text(i + off, top + (0.3 if d >= 0 else -0.3), "{:+.1f}".format(d), ha="center",
                   va="bottom" if d >= 0 else "top", fontsize=5.4, color=INK2)
    b.axhline(0, color=INK, lw=0.7, zorder=4)
    labels = []
    for sk, lab in strata:
        o = st[sk]["overall"]
        labels.append("{}\nn={:,}".format(lab, o["n"]))
    b.set_xticks(range(len(strata)))
    b.set_xticklabels(labels, fontsize=5.8, linespacing=1.3)
    b.set_xlabel("Relations available", labelpad=3)
    b.set_ylim(-11, 11)
    b.set_yticks([-10, -5, 0, 5, 10])
    b.set_xlim(-0.6, 2.6)
    b.set_ylabel("Selection $\\rightarrow$ Proposed (pp)")
    b.legend(handles=[Patch(color=C_NON, label="non-relational"),
                      Patch(color=C_REL, label="relational")],
             loc="upper left", fontsize=5.8, handlelength=1.1, borderaxespad=0.1)
    style(b)
    b.tick_params(axis="x", length=0)
    panel(b, "b", x=-0.05, y=1.02)
    save(fig, "figA_mechanism")
