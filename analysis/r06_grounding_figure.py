#!/usr/bin/env python
"""Figure: the relation effect under two grounding regimes, plus grounding coverage."""
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

from common import OUT  # noqa: E402

MM = 1 / 25.4
FULL = 122 * MM
NAVY, AMBER, SLATE, INK, INK2, GRID = "#1f3a5f", "#c98500", "#5b6b7f", "#1a1a1a", "#4d4d4d", "#e3e3e3"
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                     "font.size": 7, "axes.linewidth": 0.6, "pdf.fonttype": 42,
                     "savefig.dpi": 300, "legend.frameon": False})


def main():
    S = json.loads((OUT / "r05_detector_grounding.json").read_text(encoding="utf-8"))
    fig, (a, b) = plt.subplots(1, 2, figsize=(FULL, 46 * MM),
                               gridspec_kw={"width_ratios": [1.35, 1.0], "wspace": 0.42})

    # (a) relation effect, two regimes
    groups = ["relational", "non-relational", "all"]
    for i, g in enumerate(groups):
        for reg, col, off, mk in (("VLM objects", SLATE, 0.16, "o"),
                                  ("detector objects", AMBER, -0.16, "D")):
            r = S["relation_effect"][g][reg]
            y = len(groups) - 1 - i + off
            a.plot([100 * r["lo"], 100 * r["hi"]], [y, y], color=col, lw=1.2)
            a.plot(100 * r["delta"], y, mk, color=col, ms=4, mec="white", mew=0.5)
            a.text(100 * r["hi"] + 0.4, y, f"{100 * r['delta']:+.1f}", fontsize=5.8,
                   color=col, va="center")
    a.axvline(0, color=INK, lw=0.7)
    a.set_yticks(range(len(groups)))
    a.set_yticklabels([g.capitalize() for g in reversed(groups)], fontsize=7)
    a.set_xlabel("Effect of adding relations (pp), 95% CI")
    a.set_xlim(-5.5, 6.5)
    a.grid(axis="x", color=GRID, lw=0.5)
    a.set_axisbelow(True)
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
    a.tick_params(axis="y", length=0)
    a.legend(handles=[Patch(color=SLATE, label="VLM as extractor (52% of scenes empty)"),
                      Patch(color=AMBER, label="detector (0% empty)")],
             loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=1, fontsize=6.0)
    a.text(-0.24, 1.02, "a", transform=a.transAxes, fontsize=9, fontweight="bold", va="bottom")

    # (b) grounding coverage
    cats = ["no objects\nin scene", "cross-tile\nrelations", "objects match\nquestion"]
    vlm = [52, 25, float("nan")]
    det = [0, 99, 100 * S["detector_vocabulary"]["mean_share_objects_matching_question_keywords"]]
    x = range(len(cats))
    b.bar([i - 0.19 for i in x], vlm, width=0.36, color=SLATE, lw=0)
    b.bar([i + 0.19 for i in x], det, width=0.36, color=AMBER, lw=0)
    for i, (v, d) in enumerate(zip(vlm, det)):
        if v == v:
            b.text(i - 0.19, v + 2, f"{v:.0f}", ha="center", fontsize=5.8, color=INK2)
        b.text(i + 0.19, d + 2, f"{d:.0f}", ha="center", fontsize=5.8, color=INK2)
    b.set_xticks(list(x))
    b.set_xticklabels(cats, fontsize=5.8, linespacing=1.2)
    b.set_ylim(0, 112)
    b.set_ylabel("% of scenes / objects")
    b.grid(axis="y", color=GRID, lw=0.5)
    b.set_axisbelow(True)
    for s in ("top", "right"):
        b.spines[s].set_visible(False)
    b.tick_params(axis="x", length=0)
    b.text(-0.22, 1.02, "b", transform=b.transAxes, fontsize=9, fontweight="bold", va="bottom")

    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_tier2_grounding.{ext}", bbox_inches="tight", pad_inches=0.02)
    print("wrote outputs/fig_tier2_grounding.pdf/.png")


if __name__ == "__main__":
    main()
