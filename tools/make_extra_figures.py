#!/usr/bin/env python
"""Extra figures, generated from the committed run in results/main.

    python make_additional.py

  1_scene_graph/     graph_spatial.*     node-link graph + graph-properties panel (real item)
                     graph_on_image.png  the same graph over the satellite image
                     relation_block.txt  exact object/relation text given to the Proposed arm
  2_input_snippets/  input_zoom_figure.* full scene with selected tiles (red) + native crops
                     <uid>_overview.png / <uid>_tileNN.png  clean image panels
  3_architecture/    architecture.*      illustrated architecture (layered, 3D-block style)
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import (FancyArrowPatch, FancyBboxPatch, Polygon,  # noqa: E402
                                Rectangle)
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent / "extra_figures"
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results" / "main"
QUAL = RESULTS / "report" / "qualitative"
sys.path.insert(0, str(ROOT))
from ctsr.tiling.tiler import plan_tiles  # noqa: E402  (the exact tiling used in the run)

MM = 1 / 25.4
FULL = 122 * MM
INK, INK2, MUTED, GRID = "#1a1a1a", "#4d4d4d", "#8a8980", "#e3e3e3"
BLUE, GREEN, ORANGE, PURPLE, RED = "#2a78d6", "#1baf7a", "#eb6834", "#4a3aa7", "#d62728"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"],
    "font.size": 7, "axes.linewidth": 0.6, "pdf.fonttype": 42, "ps.fonttype": 42,
    "savefig.dpi": 300, "text.color": INK,
})

EXAMPLE_UID = "idx26_118e8cc4ea"   # object spatial relationship; Proposed correct, B3 wrong


def save(fig, folder: Path, stem: str):
    folder.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(folder / f"{stem}.{ext}", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print("wrote", folder.name + "/" + stem)


def load_record(arm: str, uid: str):
    with (RESULTS / arm / "predictions.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            if f'"{uid}"' in line:
                r = json.loads(line)
                if r.get("uid") == uid:
                    return r
    raise KeyError(uid)


def mix(hex_color, t):
    """Blend a hex colour toward white (t>0) or black (t<0)."""
    if isinstance(hex_color, str):
        c = np.array([int(hex_color[i:i + 2], 16) for i in (1, 3, 5)], float) / 255
    else:
        c = np.array(hex_color[:3], float)
    c = c + (1 - c) * t if t > 0 else c * (1 + t)
    return tuple(np.clip(c, 0, 1))


# ===========================================================================
# 1. Scene graph
# ===========================================================================
def _layout(objs, min_sep):
    """True centroid positions, with a light repulsion so overlapping nodes stay legible."""
    ids = sorted(objs)
    pos = {}
    for i in ids:
        x0, y0, x1, y1 = objs[i]["bbox_global"]
        pos[i] = np.array([(x0 + x1) / 2, (y0 + y1) / 2], float)
    for _ in range(200):
        moved = False
        for a in ids:
            for b in ids:
                if a >= b:
                    continue
                d = pos[b] - pos[a]
                n = np.linalg.norm(d)
                if n < min_sep:
                    v = d / n if n > 1e-6 else np.array([1.0, 0.0])
                    push = (min_sep - n) / 2 + 1
                    pos[a] -= v * push
                    pos[b] += v * push
                    moved = True
        if not moved:
            break
    return pos


def scene_graph_figure():
    out = HERE / "1_scene_graph"
    rec = load_record("proposed_ctsr", EXAMPLE_UID)
    art = rec["artifacts"]
    g = art["scene_graph"]
    W, H = g["image_size"]
    objs = {o["obj_id"]: o for o in g["objects"]}
    rels = g["relations"]
    chosen = art["selection"][0]["chosen"]
    plan = {t.tile_id: t for t in plan_tiles(W, H, 1024, 128)}
    pos = _layout(objs, min_sep=260)

    deg = Counter()
    for r in rels:
        deg[r["subject"]] += 1
        deg[r["object"]] += 1

    fig = plt.figure(figsize=(FULL * 0.8, 58 * MM))
    ax = fig.add_subplot(1, 1, 1)



    # tiles the graph connects across
    for tid in chosen:
        t = plan[tid]
        ax.add_patch(Rectangle((t.x0, t.y0), t.width, t.height, fc=mix("#8a8980", 0.93),
                               ec=MUTED, lw=0.5, ls=(0, (3, 2)), zorder=0))
        ax.text(t.x0 + 30, t.y0 + 30, f"tile {tid}", fontsize=5.3, color=MUTED,
                va="top", ha="left", zorder=1)

    def edge(a, b, color, ls, lw, rad, z, head=True):
        ax.add_patch(FancyArrowPatch(
            tuple(pos[a]), tuple(pos[b]), arrowstyle="-|>" if head else "-",
            mutation_scale=5.5, lw=lw, color=color, ls=ls,
            connectionstyle=f"arc3,rad={rad}", shrinkA=7, shrinkB=7, zorder=z))

    topo = {"contains", "inside", "adjacent", "near", "intersects"}
    # cross-tile directional edges first, underneath
    for r in rels:
        if r["predicate"] in topo:
            continue
        cross = bool(r.get("cross_tile"))
        edge(r["subject"], r["object"], ACCENT if cross else SLATE, "-", 1.0,
             0.10, 2 if cross else 3)
    # topological edges on top, with labels
    for r in rels:
        if r["predicate"] not in topo:
            continue
        a, b = r["subject"], r["object"]
        ls = (0, (3, 1.6)) if r["predicate"] in ("contains", "inside") else (0, (1, 1.2))
        edge(a, b, INK, ls, 1.2, 0.0, 4, head=r["predicate"] in ("contains", "inside"))
        mid = (pos[a] + pos[b]) / 2
        lab = r["predicate"] + (f" {r['value'].upper().replace('NORTH', 'N').replace('SOUTH', 'S').replace('EAST', 'E').replace('WEST', 'W').replace('-', '')}"
                                if r.get("value") and r["predicate"] != "contains" else "")
        ax.text(mid[0] + 260, mid[1] + 40, lab, fontsize=5.0, color=INK, zorder=7,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))

    # nodes: size by degree, shape/colour by class
    for oid, o in objs.items():
        x, y = pos[oid]
        circ = "circular" in o["label"].lower()
        s = 60 + 14 * deg[oid]
        ax.scatter([x], [y], s=s, marker="o" if circ else "s",
                   color=SLATE if circ else NAVY, edgecolor="white", linewidth=1.0, zorder=6)
        ax.text(x, y, str(oid), fontsize=5.8, color="white", ha="center", va="center",
                fontweight="bold", zorder=8)

    ys = [p[1] for p in pos.values()]
    ax.set_xlim(0, W)
    ax.set_ylim(max(ys) + 450, min(ys) - 500)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.annotate("N", xy=(W - 170, min(ys) - 380), xytext=(W - 170, min(ys) - 60),
                ha="center", va="top", fontsize=6.5,
                arrowprops=dict(arrowstyle="-|>", lw=0.8, color=INK2))
    handles = [
        Line2D([], [], marker="s", ls="", color=NAVY, mec="white", ms=6, label="H-shaped building"),
        Line2D([], [], marker="o", ls="", color=SLATE, mec="white", ms=6, label="white circular building"),
        Line2D([], [], color=ACCENT, lw=1.0, label="direction, cross-tile"),
        Line2D([], [], color=SLATE, lw=1.0, label="direction, within tile"),
        Line2D([], [], color=INK, lw=1.2, ls=(0, (3, 1.6)), label="containment"),
        Line2D([], [], color=INK, lw=1.2, ls=(0, (1, 1.2)), label="adjacent / near"),
    ]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=3,
              frameon=False, fontsize=5.6, handlelength=2.0, columnspacing=1.2)

    save(fig, out, "graph_spatial")

    # exact text the Proposed arm received, via the pipeline's own serialiser
    from ctsr.data.schema import DetectedObject
    from ctsr.spatial.relations import Relation
    from ctsr.spatial.scene_graph import SceneGraph
    keys = ("subject", "object", "predicate", "value", "distance_px", "distance_norm",
            "distance_m", "bearing_deg", "iou", "containment", "cross_tile")
    sg = SceneGraph(
        objects=[DetectedObject(label=o["label"], bbox_global=tuple(o["bbox_global"]),
                                score=o.get("score", 1.0), tile_id=o.get("tile_id"),
                                obj_id=o["obj_id"], merged_from=o.get("merged_from", []))
                 for o in g["objects"]],
        relations=[Relation(**{k: r.get(k) for k in keys if k in r}) for r in rels],
        image_size=(W, H))
    txt = ["# Question keywords: " + ", ".join(art.get("question_keywords") or []),
           f"# Ground truth: {rec.get('gt')}   Proposed: {rec.get('parsed')}", "",
           "DETECTED OBJECTS (global coordinates, 0-1000 grid over the whole image):"]
    txt += sg.object_lines()
    txt += ["", "SPATIAL RELATIONS (computed geometrically from the global coordinates):"]
    txt += sg.relation_lines(include_metric=True)
    (out / "relation_block.txt").write_text("\n".join(txt) + "\n", encoding="utf-8")

    src = QUAL / f"qual_graph_wins_{EXAMPLE_UID}.png"
    if src.exists():
        im = Image.open(src).convert("RGB")
        im.thumbnail((2000, 2000))
        im.save(out / "graph_on_image.png", optimize=True)


# ===========================================================================
# 2. Input snippets
# ===========================================================================
def split_panels(png: Path):
    """Cut the clean image panels out of a side-by-side figure produced by the run."""
    im = np.asarray(Image.open(png).convert("RGB")).astype(int)
    bg = im[5, 5]
    diff = np.abs(im - bg).sum(axis=2) > 40
    h = im.shape[0]
    cols = diff[int(0.18 * h):int(0.95 * h)].mean(axis=0) > 0.5
    runs, start = [], None
    for x, v in enumerate(list(cols) + [False]):
        if v and start is None:
            start = x
        elif not v and start is not None:
            if x - start > 80:
                runs.append((start, x))
            start = None
    panels = []
    for x0, x1 in runs:
        rows = diff[:, x0:x1].mean(axis=1) > 0.9
        best, cur, s0 = (0, 0), 0, 0
        for y, v in enumerate(rows):
            if v:
                s0 = y if cur == 0 else s0
                cur += 1
                if cur > best[1] - best[0]:
                    best = (s0, y + 1)
            else:
                cur = 0
        panels.append(Image.fromarray(im[best[0]:best[1], x0:x1].astype(np.uint8)))
    return panels


def input_snippets():
    out = HERE / "2_input_snippets"
    out.mkdir(parents=True, exist_ok=True)
    idx = json.loads((QUAL / "qualitative_index.json").read_text(encoding="utf-8"))
    for uid in [u for v in idx.get("picks", {}).values() for u in v]:
        cand = list(QUAL.glob(f"qual_sbs_*_{uid}.png"))
        if not cand:
            continue
        chosen = load_record("proposed_ctsr", uid)["artifacts"]["selection"][0]["chosen"]
        panels = split_panels(cand[0])
        if len(panels) >= 2:
            panels[0].save(out / f"{uid}_overview.png")
            for tid, p in zip(chosen, panels[1:]):
                p.save(out / f"{uid}_tile{tid:02d}.png")

    rec = load_record("proposed_ctsr", EXAMPLE_UID)
    W, H = rec["artifacts"]["scene_graph"]["image_size"]
    chosen = rec["artifacts"]["selection"][0]["chosen"][:3]
    plan = {t.tile_id: t for t in plan_tiles(W, H, 1024, 128)}
    ov = Image.open(out / f"{EXAMPLE_UID}_overview.png")
    tiles = [Image.open(out / f"{EXAMPLE_UID}_tile{t:02d}.png") for t in chosen]

    fig = plt.figure(figsize=(FULL, 46 * MM))
    gs = fig.add_gridspec(1, 4, width_ratios=[1.45, 1, 1, 1], wspace=0.07)
    a = fig.add_subplot(gs[0, 0])
    a.imshow(ov, extent=(0, W, H, 0))
    a.set_xlim(0, W); a.set_ylim(H, 0)
    a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values():
        s.set_color(GRID)
    a.set_xlabel(f"Full scene, {W:,}$\\times${H:,} px", fontsize=4.8, fontweight="bold",
                 labelpad=2.5)
    for k, (tid, im) in enumerate(zip(chosen, tiles)):
        t = plan[tid]
        a.add_patch(Rectangle((t.x0, t.y0), t.width, t.height, fill=False, ec=RED, lw=1.2))
        a.text(t.x0 + 45, t.y0 + 60, str(k + 1), color="white", fontsize=6.2,
               fontweight="bold", va="top",
               bbox=dict(boxstyle="round,pad=0.15", fc=RED, ec="none"))
        b = fig.add_subplot(gs[0, k + 1])
        b.imshow(im)
        b.set_xticks([]); b.set_yticks([])
        for s in b.spines.values():
            s.set_color(RED); s.set_linewidth(1.4)
        b.set_title(f"({k + 1}) tile {tid}", fontsize=6.3, color=INK, pad=3)
        b.set_xlabel("1024$\\times$1024 px, native", fontsize=4.8, fontweight="bold",
                     labelpad=2.5)
    save(fig, out, "input_zoom_figure")


# ===========================================================================
# 3. Architecture (illustrated, layered style)
# ===========================================================================
class Canvas:
    def __init__(self, w=122, h=74):
        self.fig = plt.figure(figsize=(w * MM, h * MM))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w); self.ax.set_ylim(0, h); self.ax.axis("off")
        self.w, self.h = w, h

    def block3d(self, x, y, w, h, color, d=1.6, grid=None, z=3, lw=0.5):
        ax = self.ax
        front = mix(color, 0.25)
        ax.add_patch(Polygon([(x, y + h), (x + d, y + h + d), (x + w + d, y + h + d), (x + w, y + h)],
                             closed=True, fc=mix(color, 0.5), ec=mix(color, -0.35), lw=lw, zorder=z))
        ax.add_patch(Polygon([(x + w, y), (x + w + d, y + d), (x + w + d, y + h + d), (x + w, y + h)],
                             closed=True, fc=mix(color, -0.2), ec=mix(color, -0.35), lw=lw, zorder=z))
        ax.add_patch(Rectangle((x, y), w, h, fc=front, ec=mix(color, -0.35), lw=lw, zorder=z))
        if grid:
            nx, ny = grid
            for i in range(1, nx):
                ax.plot([x + w * i / nx] * 2, [y, y + h], color=mix(color, -0.3), lw=0.35, zorder=z + 0.1)
            for j in range(1, ny):
                ax.plot([x, x + w], [y + h * j / ny] * 2, color=mix(color, -0.3), lw=0.35, zorder=z + 0.1)

    def image(self, img, x, y, w, h, edge=INK2, lw=0.5, z=4):
        self.ax.imshow(img, extent=(x, x + w, y, y + h), zorder=z, aspect="auto")
        self.ax.add_patch(Rectangle((x, y), w, h, fill=False, ec=edge, lw=lw, zorder=z + 0.1))

    def nodes(self, x, y0, y1, n, color, r=0.75, gap_dots=True):
        ys = list(np.linspace(y1, y0, n))
        if gap_dots and n >= 6:
            mid = n // 2
            pts = ys[:mid - 1] + ys[mid + 1:]
            for dy in (-0.9, 0, 0.9):
                self.ax.plot(x, (ys[mid - 1] + ys[mid]) / 2 + dy, ".", ms=1.2, color=INK2, zorder=5)
        else:
            pts = ys
        for yy in pts:
            self.ax.add_patch(plt.Circle((x, yy), r, fc=mix(color, 0.35), ec=mix(color, -0.4),
                                         lw=0.45, zorder=6))
        return pts

    def dense(self, x0, ys0, x1, ys1, color, alpha=0.35):
        for a in ys0:
            for b in ys1:
                self.ax.plot([x0, x1], [a, b], color=mix(color, 0.35), lw=0.2, alpha=alpha, zorder=2)

    def arrow(self, p0, p1, color, rad=0.0, lw=1.0, ls="-"):
        self.ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=6, lw=lw,
                                          color=color, ls=ls, shrinkA=0, shrinkB=0,
                                          connectionstyle=f"arc3,rad={rad}", zorder=7))

    def text(self, x, y, s, size=5.6, color=INK2, weight="normal", ha="center", va="center",
             style="normal"):
        self.ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va,
                     fontstyle=style, zorder=9)


def mini_graph(cv, x, y, w, h):
    """Real relation graph of the example item, scaled into a box."""
    g = load_record("proposed_ctsr", EXAMPLE_UID)["artifacts"]["scene_graph"]
    objs = {o["obj_id"]: o for o in g["objects"]}
    pos = _layout(objs, 260)
    P = np.array(list(pos.values()))
    lo, hi = P.min(0), P.max(0)

    def tr(p):
        return (x + 1 + (p[0] - lo[0]) / (hi[0] - lo[0]) * (w - 2),
                y + h - 1 - (p[1] - lo[1]) / (hi[1] - lo[1]) * (h - 2))
    for r in g["relations"]:
        a, b = tr(pos[r["subject"]]), tr(pos[r["object"]])
        cv.ax.plot([a[0], b[0]], [a[1], b[1]], color=ORANGE if r.get("cross_tile") else INK2,
                   lw=0.45, alpha=0.8, zorder=5)
    for oid, p in pos.items():
        q = tr(p)
        circ = "circular" in objs[oid]["label"].lower()
        cv.ax.add_patch(plt.Circle(q, 0.75, fc=GREEN if circ else BLUE, ec="white", lw=0.4,
                                   zorder=6))


def architecture():
    out = HERE / "3_architecture"
    snip = HERE / "2_input_snippets"
    rec = load_record("proposed_ctsr", EXAMPLE_UID)
    chosen = rec["artifacts"]["selection"][0]["chosen"]
    ov = Image.open(snip / f"{EXAMPLE_UID}_overview.png")
    crops = [Image.open(snip / f"{EXAMPLE_UID}_tile{t:02d}.png") for t in chosen[:3]]

    cv = Canvas(122, 74)
    top, mid, bot = 57.0, 37.0, 12.0

    # column headers
    for x, s, c in [(8, "Input", INK), (28, "Selection", BLUE), (47, "Local extraction", GREEN),
                    (68, "Evidence", INK2), (92.5, "Final reasoning", PURPLE),
                    (113, "Output", ORANGE)]:
        cv.text(x, 71.5, s, 6.4, c, "bold")

    # ---- input: real scene with tile grid, plus question -----------------
    cv.image(ov, 1.5, 29, 13, 13)
    for k in range(1, 4):
        cv.ax.plot([1.5 + 13 * k / 4] * 2, [29, 42], color="white", lw=0.3, alpha=0.8, zorder=5)
        cv.ax.plot([1.5, 14.5], [29 + 13 * k / 4] * 2, color="white", lw=0.3, alpha=0.8, zorder=5)
    cv.text(8, 44.2, "UHR scene", 6.0, INK, "bold")
    cv.text(8, 27.2, "4K–10K px per side", 5.1)
    cv.ax.add_patch(FancyBboxPatch((1.5, 17.5), 13, 7, boxstyle="round,pad=0,rounding_size=1",
                                   fc="#f4f4f2", ec=MUTED, lw=0.4, zorder=4))
    cv.text(8, 22.6, "question", 5.4, INK, "bold")
    cv.text(8, 19.6, "+ options A–D", 5.1)

    # branches
    cv.arrow((15.2, 35.5), (19.5, top - 1), BLUE, rad=-0.3)
    cv.arrow((15.2, 35.5), (19.5, mid), GREEN)
    cv.arrow((14.7, 22.5), (20.6, mid - 4.5), GREEN, rad=0.2, lw=0.7)

    # ---- global row (blue) ----------------------------------------------
    cv.text(20, top + 8.8, "Global view", 6.0, BLUE, "bold", ha="left")
    cv.image(ov, 21, top - 5, 9, 9, edge=BLUE, lw=0.7)
    cv.text(25.5, top - 7.2, "overview, 1024 px", 5.1)
    cv.arrow((31, top - 0.5), (86.5, top - 0.5), BLUE)
    cv.text(68, top + 1.2, "downscaled whole scene", 5.1, BLUE, style="italic")

    # ---- local row (green) ----------------------------------------------
    cv.text(20, mid + 8.8, "Local evidence", 6.0, GREEN, "bold", ha="left")
    cv.block3d(21, mid - 5.5, 9, 9, BLUE, d=1.4, grid=(5, 5))
    for (i, j) in [(0, 1), (1, 2), (2, 1), (3, 3), (4, 2)]:   # illustrative top-5 cells
        cv.ax.add_patch(Rectangle((21 + 9 * i / 5, mid - 5.5 + 9 * j / 5), 9 / 5, 9 / 5,
                                  fc=RED, alpha=0.75, ec="none", zorder=4))
    cv.text(26.3, mid - 7.8, "saliency + CLIP", 4.9)
    cv.text(26.3, mid - 9.9, "→ top-5 tiles", 4.9)
    cv.arrow((32, mid - 1), (35.5, mid - 1), GREEN)
    for k, im in enumerate(reversed(crops)):          # stacked native crops
        o = (2 - k) * 1.4
        cv.image(im, 36 + o, mid - 5 - o, 8, 8, edge="white", lw=0.6)
    cv.text(41.5, mid - 9.2, "native crops", 5.1)
    cv.arrow((46.5, mid - 1), (49, mid - 1), GREEN)
    for k in range(3):                                  # frozen VLM layers
        cv.block3d(49.5 + k * 2.6, mid - 6.5, 1.8, 11, GREEN, d=1.2)
    cv.text(53.5, mid - 8.8, "Qwen2.5-VL ×5", 5.1, INK)
    cv.text(53.5, mid - 11.0, "frozen", 5.1, style="italic")
    cv.arrow((58.8, mid - 1), (61.5, mid - 1), GREEN)
    ys_a = cv.nodes(63, mid - 6, mid + 4, 7, GREEN)
    ys_b = cv.nodes(70, mid - 6, mid + 4, 7, GREEN)
    cv.dense(63, ys_a, 70, ys_b, GREEN)
    cv.text(66.5, mid + 6.6, "object list", 5.1, GREEN, "bold")
    cv.arrow((72, mid - 1), (86.5, mid - 1), GREEN)

    # ---- geometry row (orange, Proposed only) ---------------------------
    cv.ax.add_patch(FancyBboxPatch((47, bot - 9.5), 38.3, 21.5, boxstyle="round,pad=0,rounding_size=1.5",
                                   fc="none", ec=ORANGE, lw=0.7, ls=(0, (3, 2)), zorder=1))
    cv.text(20, bot + 8.8, "Cross-tile geometry", 6.0, ORANGE, "bold", ha="left")
    cv.text(20, bot + 5.6, "deterministic,", 5.1, ha="left")
    cv.text(20, bot + 3.4, "no learning", 5.1, ha="left")
    cv.arrow((70, mid - 6.8), (55, bot + 5.3), ORANGE, rad=-0.2, lw=0.8)
    cv.block3d(49.5, bot - 5, 9, 9, ORANGE, d=1.4, grid=(4, 4))
    cv.ax.add_patch(Rectangle((49.5 + 2.25, bot - 5 + 4.5), 2.25, 2.25, fill=False, ec=INK,
                              lw=0.6, zorder=5))
    cv.text(54, bot - 7.3, "global px + dedup", 5.1)
    cv.arrow((60.5, bot - 0.5), (62.5, bot - 0.5), ORANGE)
    cv.ax.add_patch(Rectangle((63, bot - 5.5), 14, 10, fc="white", ec=GRID, lw=0.4, zorder=4))
    mini_graph(cv, 63, bot - 5.5, 14, 10)
    cv.text(70, bot - 7.5, "relation graph", 5.1, ORANGE)
    cv.arrow((77.5, bot - 0.5), (86.5, bot - 0.5), ORANGE, ls=(0, (3, 1.5)))
    # the single experimental switch
    cv.ax.add_patch(FancyBboxPatch((78.8, bot + 2.2), 5.8, 2.8, boxstyle="round,pad=0,rounding_size=1.4",
                                   fc="white", ec=ORANGE, lw=0.6, zorder=8))
    cv.ax.add_patch(plt.Circle((83.2, bot + 3.6), 1.0, fc=ORANGE, ec="none", zorder=9))
    cv.text(80.6, bot + 8.4, "off: Selection", 4.7, INK2)
    cv.text(80.6, bot + 6.5, "on: Proposed", 4.7, ORANGE, "bold")

    # ---- final reasoning (purple): Qwen2.5-VL internals ------------------
    for i, (bw, lab) in enumerate([(3.2, "vision encoder (ViT, window attention)"),
                                   (2.6, "MLP merger (2×2 → 1 token)"),
                                   (3.6, "LLM decoder (Qwen2.5, 7B)")]):
        xx = 87.0 + sum([3.2, 2.6, 3.6][:i]) + i * 1.9
        cv.block3d(xx, 7, bw, 55, PURPLE if i != 1 else mix(PURPLE, 0.15), d=1.8)
        cv.ax.text(xx + bw / 2, 34.5, lab, rotation=90, ha="center", va="center",
                   fontsize=5.3, color="white", fontweight="bold", zorder=9)
    cv.text(97.5, 4.6, "Qwen2.5-VL-7B, frozen", 5.2, PURPLE, "bold")
    cv.text(97.5, 2.4, "≤1,280 visual tokens / image", 4.8, PURPLE)

    # ---- output ---------------------------------------------------------
    ys_o = cv.nodes(106, mid - 8, mid + 8, 7, ORANGE, r=0.7)
    cv.dense(101.8, list(np.linspace(mid - 14, mid + 14, 9)), 106, ys_o, PURPLE, alpha=0.25)
    for k, lab in enumerate(["A", "B", "C", "D"]):
        yy = mid + 9 - k * 6
        hit = lab == "C"
        cv.ax.add_patch(FancyBboxPatch((109, yy - 2.1), 11, 4.2, boxstyle="round,pad=0,rounding_size=1",
                                       fc=mix(ORANGE, 0.75) if hit else "white",
                                       ec=ORANGE if hit else MUTED, lw=0.8 if hit else 0.4, zorder=6))
        cv.text(114.5, yy, f"option {lab}", 5.6, INK, "bold" if hit else "normal")
        cv.ax.plot([106.8, 109], [ys_o[min(k * 2, len(ys_o) - 1)], yy], color=mix(ORANGE, 0.4),
                   lw=0.3, zorder=3)
    cv.text(114.5, mid - 17, "one answer letter", 5.1)
    cv.text(114.5, mid - 19.2, "(4-option MCQ)", 5.1)

    save(cv.fig, out, "architecture")


def main():
    scene_graph_figure()
    input_snippets()
    architecture()




# ===========================================================================
# 3b. Architecture, professional/compact version (used in the paper)
# ===========================================================================
NAVY = "#1f3a5f"
SLATE = "#5b6b7f"
FILL = "#eef2f7"
ACCENT = "#c98500"
ACCENT_FILL = "#fbf1dc"


def architecture_compact():
    out = HERE / "3_architecture"
    snip = HERE / "2_input_snippets"
    rec = load_record("proposed_ctsr", EXAMPLE_UID)
    chosen = rec["artifacts"]["selection"][0]["chosen"]
    ov = Image.open(snip / f"{EXAMPLE_UID}_overview.png")
    crops = [Image.open(snip / f"{EXAMPLE_UID}_tile{t:02d}.png") for t in chosen[:3]]

    W, H = 122, 36
    fig = plt.figure(figsize=(W * MM, H * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

    def box(x, y, w, h, fc=FILL, ec=NAVY, ls="-", lw=0.7):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                                    fc=fc, ec=ec, lw=lw, ls=ls, zorder=2))

    def title(x, y, s, c=NAVY):
        ax.text(x, y, s, ha="center", va="top", fontsize=5.5, fontweight="bold", color=c, zorder=5)

    def sub(x, y, s, c=SLATE):
        ax.text(x, y, s, ha="center", va="top", fontsize=4.9, color=c, zorder=5, linespacing=1.15)

    def arrow(p0, p1, c=NAVY, ls="-", rad=0.0, lw=0.7):
        ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=5.5, lw=lw, color=c,
                                     ls=ls, shrinkA=0, shrinkB=0, zorder=4,
                                     connectionstyle=f"arc3,rad={rad}"))

    y0, h = 7, 22
    # Input
    box(1, y0, 15, h)
    title(8.5, y0 + h - 1.4, "Input")
    ax.imshow(ov, extent=(3, 14, y0 + 5.2, y0 + 16.2), zorder=3)
    for k in range(1, 4):
        ax.plot([3 + 11 * k / 4] * 2, [y0 + 5.2, y0 + 16.2], color="white", lw=0.25, zorder=4)
        ax.plot([3, 14], [y0 + 5.2 + 11 * k / 4] * 2, color="white", lw=0.25, zorder=4)
    ax.add_patch(Rectangle((3 + 11 / 4, y0 + 5.2 + 11 / 4), 11 / 4, 11 / 4, fill=False,
                           ec=ACCENT, lw=0.7, zorder=5))
    sub(8.5, y0 + 4.4, "UHR scene\n+ question")

    # Selection
    xs = 19.5
    box(xs, y0, 15, h)
    title(xs + 7.5, y0 + h - 1.4, "Tile selection")
    sub(xs + 7.5, y0 + h - 5.0, "saliency + CLIP\nquestion score")
    for i in range(4):
        for j in range(3):
            hit = (i, j) in [(0, 1), (1, 0), (2, 2), (3, 1), (1, 2)]
            ax.add_patch(Rectangle((xs + 2.5 + i * 2.6, y0 + 3 + j * 2.6), 2.3, 2.3,
                                   fc=NAVY if hit else "white", ec=SLATE, lw=0.3, zorder=3))
    sub(xs + 7.5, y0 + 2.4, "top-5 tiles")

    # Local extraction
    xl = 38
    box(xl, y0, 15, h)
    title(xl + 7.5, y0 + h - 1.4, "Extraction")
    for k, im in enumerate(reversed(crops)):
        o = (2 - k) * 1.1
        ax.imshow(im, extent=(xl + 3.5 + o, xl + 10.5 + o, y0 + 5.3 - o + 2.2, y0 + 12.3 - o + 2.2),
                  zorder=3 + k * 0.1)
        ax.add_patch(Rectangle((xl + 3.5 + o, y0 + 7.5 - o), 7, 7, fill=False, ec="white", lw=0.4,
                               zorder=3.05 + k * 0.1))
    sub(xl + 7.5, y0 + 4.4, "frozen VLM ×5:\nobjects + boxes")

    # Registration
    xr = 56.5
    box(xr, y0, 15, h)
    title(xr + 7.5, y0 + h - 1.4, "Registration")
    ax.add_patch(Rectangle((xr + 3.5, y0 + 6.5), 8, 8, fc="white", ec=SLATE, lw=0.5, zorder=3))
    for (bx, by, bw, bh) in [(0.8, 4.5, 2.2, 1.6), (4.6, 5.6, 1.6, 1.4), (2.2, 1.2, 2.6, 1.8), (5.4, 1.8, 1.8, 1.4)]:
        ax.add_patch(Rectangle((xr + 3.5 + bx, y0 + 6.5 + by), bw, bh, fc="none", ec=NAVY,
                               lw=0.45, zorder=4))
    sub(xr + 7.5, y0 + 4.4, "global frame\n+ dedup")

    # Relation graph (accent: the only difference between B3 and Proposed)
    xg = 75
    box(xg, y0, 15, h, fc=ACCENT_FILL, ec=ACCENT, ls=(0, (3, 1.6)), lw=0.8)
    title(xg + 7.5, y0 + h - 1.4, "Relations", c=INK)
    g = rec["artifacts"]["scene_graph"]
    objs = {o["obj_id"]: o for o in g["objects"]}
    pos = _layout(objs, 260)
    P = np.array(list(pos.values()))
    lo, hi = P.min(0), P.max(0)

    def tr(p):
        return (xg + 2.5 + (p[0] - lo[0]) / (hi[0] - lo[0]) * 10,
                y0 + 15.5 - (p[1] - lo[1]) / (hi[1] - lo[1]) * 8.5)
    for r in g["relations"]:
        a, b = tr(pos[r["subject"]]), tr(pos[r["object"]])
        ax.plot([a[0], b[0]], [a[1], b[1]], color=ACCENT if r.get("cross_tile") else SLATE,
                lw=0.35, alpha=0.85, zorder=3)
    for p in pos.values():
        ax.add_patch(plt.Circle(tr(p), 0.55, fc=NAVY, ec="white", lw=0.3, zorder=4))
    sub(xg + 7.5, y0 + 4.4, "direction, distance,\ntopology", c=INK2)

    # Final reasoning
    xf = 93.5
    box(xf, y0, 15, h, fc=NAVY, ec=NAVY)
    title(xf + 7.5, y0 + h - 1.4, "Reasoning", c="white")
    sub(xf + 7.5, y0 + h - 5.0, "Qwen2.5-VL-7B\n(frozen, 1 call)", c="#dfe6ef")
    sub(xf + 7.5, y0 + 9.2, "overview\n+ 3 crops\n+ object list\n(+ relations)", c="#dfe6ef")

    # Output
    ax.text(114.5, y0 + h / 2 + 1.6, "answer", ha="center", va="center", fontsize=5.9,
            fontweight="bold", color=NAVY)
    ax.text(114.5, y0 + h / 2 - 1.4, "A / B / C / D", ha="center", va="center", fontsize=4.9,
            color=SLATE)

    # arrows along the pipeline
    for x0, x1 in [(16, 19.5), (34.5, 38), (53, 56.5), (71.5, 75), (90, 93.5), (108.5, 110.5)]:
        arrow((x0 + 0.3, y0 + h / 2), (x1 - 0.3, y0 + h / 2),
              c=ACCENT if x0 == 90 else NAVY, ls=(0, (3, 1.5)) if x0 == 90 else "-")
    # object list bypasses the relation graph (what B3 receives)
    ax.add_patch(FancyArrowPatch((xr + 7.5, y0 - 0.3), (xf + 5, y0 - 0.3), arrowstyle="-|>",
                                 mutation_scale=5.5, lw=0.6, color=NAVY, zorder=4,
                                 connectionstyle="arc3,rad=0.22", shrinkA=0, shrinkB=0))
    ax.text(83.5, 1.3, "object list (Selection and Proposed)", ha="center", fontsize=4.8, color=SLATE)
    # global overview path
    ax.add_patch(FancyArrowPatch((8.5, y0 + h + 0.3), (xf + 7.5, y0 + h + 0.3), arrowstyle="-|>",
                                 mutation_scale=5.5, lw=0.6, color=SLATE, zorder=4,
                                 connectionstyle="arc3,rad=-0.03", shrinkA=0, shrinkB=0))
    ax.text(55, y0 + h + 2.4, "global overview (whole scene, 1024 px)", ha="center", fontsize=4.8,
            color=SLATE)
    ax.text(xg + 7.5, y0 - 1.6, "Proposed only", ha="center", fontsize=4.9, color=ACCENT,
            fontstyle="italic", fontweight="bold")
    save(fig, out, "architecture")



def main():
    scene_graph_figure()
    input_snippets()
    architecture_compact()


if __name__ == "__main__":
    main()
