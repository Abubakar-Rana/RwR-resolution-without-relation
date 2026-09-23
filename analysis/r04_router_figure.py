#!/usr/bin/env python
"""Figure: accuracy against compute for the four methods and the cross-validated routers.

Same style rules as the paper's figures (Springer: 122 mm, Arial, >=0.5 pt lines, vector PDF,
embedded fonts). Identity is carried by direct labels, not colour.
"""
import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from common import OUT  # noqa: E402

MM = 1 / 25.4
NAVY, SLATE, AMBER, INK2, GRID = "#1f3a5f", "#5b6b7f", "#c98500", "#4d4d4d", "#e3e3e3"
plt.rcParams.update({"font.family": "sans-serif",
                     "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                     "font.size": 7, "axes.linewidth": 0.6, "pdf.fonttype": 42,
                     "savefig.dpi": 300})


def main():
    R = json.loads((OUT / "r03_router.json").read_text(encoding="utf-8"))
    from common import correct, load
    data, uids = load()
    tiling_acc = 100 * correct(data, "b2_tiling", uids).mean()
    tiling_calls = sum((data["b2_tiling"][u].get("compute") or {}).get("n_vlm_calls") or 0
                       for u in uids) / len(uids)

    fig, ax = plt.subplots(figsize=(90 * MM, 60 * MM))
    pts = [(k, v["calls"], 100 * v["acc"], SLATE, "o") for k, v in R["singles"].items()]
    pts.append(("Tiling", tiling_calls, tiling_acc, SLATE, "o"))
    label = {"group router (pre-registered split)": "Router (task group)",
             "task router (Direct / Selection)": "Router (task label)",
             "keyword-only router (no task label)": "Router (keywords only)"}
    for k, short in label.items():
        v = R["routers"][k]
        pts.append((short, v["calls"], 100 * v["acc_mean"], AMBER, "D"))
    # label anchor positions (data units), chosen so no two labels collide
    place = {"Direct": (1.35, 40.2), "Tiling": (7.3, 36.9), "Selection": (6.6, 43.9),
             "Proposed": (6.6, 42.0), "Router (task group)": (3.0, 47.0),
             "Router (task label)": (5.2, 45.4), "Router (keywords only)": (0.8, 45.1)}
    for name, x, y, c, m in pts:
        ax.scatter([x], [y], s=26, color=c, marker=m, edgecolor="white", linewidth=0.6, zorder=3)
        tx, ty = place.get(name, (x + 0.2, y + 0.3))
        ax.annotate(name, xy=(x, y), xytext=(tx, ty), fontsize=6, color=INK2, va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.4, color="#9a9a9a", shrinkA=1, shrinkB=3))
    ax.axhline(100 * R["oracle_direct_selection"], color=NAVY, lw=0.8, ls="--")
    ax.text(0.95, 100 * R["oracle_direct_selection"] + 0.35,
            "oracle: best of Direct / Selection per item", fontsize=5.8, color=NAVY)
    ax.set_xlabel("Mean VLM calls per item")
    ax.set_ylabel("Accuracy (%)")
    ax.set_xlim(0.5, 10.2)
    ax.set_ylim(36, 53)
    ax.grid(color=GRID, lw=0.5)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig_router_accuracy_vs_calls.{ext}", bbox_inches="tight", pad_inches=0.02)
    print("wrote outputs/fig_router_accuracy_vs_calls.pdf/.png")


if __name__ == "__main__":
    main()
