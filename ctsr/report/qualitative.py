"""Qualitative figures: what the method actually saw.

Three products, all for the paper's figure set:

  overlay_scene_graph   the overview image with selected tiles, detected objects
                        and cross-tile relation edges drawn on top. This is the
                        figure that makes the contribution legible: a reader sees
                        the edges spanning tile boundaries.
  side_by_side          the low-resolution overview next to the selected
                        high-resolution crops, showing what naive resizing loses.
  case_card             one sample's full trace - question, selected tiles,
                        objects, relations, both arms' answers - for the
                        failure-case analysis.

Cross-tile edges are drawn in the accent hue and same-tile edges in muted grey,
so the distinction the paper rests on is visible without reading a legend - and a
legend is present anyway.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..utils.io_utils import ensure_dir, load_jsonl
from ..utils.logging_utils import get_logger
from .figures import INK, INK_2, INK_MUTED, SERIES, SURFACE, _mpl, _save

LOG = get_logger("ctsr.report.qualitative")

TILE_COLOR = "#eda100"      # selected tile outline
OBJ_COLOR = "#2a78d6"       # object boxes
CROSS_COLOR = "#eb6834"     # cross-tile relation edges
SAME_COLOR = "#8a8980"      # within-tile relation edges


def _load_overview(path: str, max_side: int = 1400):
    """Downsampled image for drawing on, or None if it cannot be read."""
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        im = Image.open(path)
        try:
            im.draft("RGB", (max_side, max_side))
        except Exception:
            pass
        if im.mode != "RGB":
            im = im.convert("RGB")
        scale = min(1.0, float(max_side) / max(im.size))
        if scale < 1.0:
            im = im.resize((max(1, int(im.size[0] * scale)),
                            max(1, int(im.size[1] * scale))), Image.BICUBIC)
        return im
    except Exception as exc:
        LOG.error("Could not open %s for a qualitative figure: %s", path, exc)
        return None


def overlay_scene_graph(
    record: Dict[str, Any],
    image_path: str,
    out_dir: str,
    stem: Optional[str] = None,
    max_side: int = 1400,
    max_edges: int = 60,
    show_labels: bool = True,
) -> List[str]:
    """Draw selected tiles, objects and relation edges over the scene overview."""
    plt = _mpl()
    if plt is None:
        return []
    im = _load_overview(image_path, max_side)
    if im is None:
        return []

    art = record.get("artifacts") or {}
    graph = art.get("scene_graph") or {}
    objects = graph.get("objects") or []
    relations = graph.get("relations") or []
    img_size = graph.get("image_size") or []
    if len(img_size) != 2 or not img_size[0]:
        LOG.warning("overlay_scene_graph: no image_size recorded for %s",
                    record.get("uid"))
        return []

    ow, oh = im.size
    sx = ow / float(img_size[0])
    sy = oh / float(img_size[1])

    fig, ax = plt.subplots(figsize=(7.2, 7.2 * oh / max(1, ow)))
    ax.imshow(im)
    ax.set_xlim(0, ow)
    ax.set_ylim(oh, 0)
    ax.axis("off")

    # -- selected tiles ----------------------------------------------------
    import matplotlib.patches as mpatches

    tile_boxes: List[Tuple[int, List[int]]] = []
    for sel in (art.get("selection") or []):
        for tid in (sel.get("chosen") or []):
            tile_boxes.append((tid, []))
    # Tile geometry is recoverable from the tile plan; recompute it so the figure
    # does not depend on boxes having been serialised.
    n_total = record.get("n_tiles_total")
    if n_total and img_size:
        from ..tiling.tiler import plan_tiles
        tsize = (art.get("tile_size")
                 or (record.get("compute") or {}).get("tile_size") or 1024)
        tover = art.get("overlap") or 128
        try:
            plan = {t.tile_id: t for t in plan_tiles(int(img_size[0]), int(img_size[1]),
                                                     int(tsize), int(tover))}
        except Exception:
            plan = {}
        for tid, _ in tile_boxes:
            t = plan.get(tid)
            if t is None:
                continue
            ax.add_patch(mpatches.Rectangle(
                (t.x0 * sx, t.y0 * sy), t.width * sx, t.height * sy,
                fill=False, edgecolor=TILE_COLOR, linewidth=1.8, linestyle="--",
                zorder=2,
            ))

    # -- objects -----------------------------------------------------------
    centers: Dict[int, Tuple[float, float]] = {}
    for o in objects:
        bb = o.get("bbox_global") or []
        if len(bb) != 4:
            continue
        x0, y0, x1, y1 = [float(v) for v in bb]
        cx, cy = 0.5 * (x0 + x1) * sx, 0.5 * (y0 + y1) * sy
        oid = o.get("obj_id")
        if oid is not None:
            centers[int(oid)] = (cx, cy)
        ax.add_patch(mpatches.Rectangle(
            (x0 * sx, y0 * sy), max(2.0, (x1 - x0) * sx), max(2.0, (y1 - y0) * sy),
            fill=False, edgecolor=OBJ_COLOR, linewidth=1.2, zorder=3,
        ))
        if show_labels and oid is not None:
            ax.annotate("#{}".format(oid), (cx, cy), fontsize=6, color=SURFACE,
                        ha="center", va="center", zorder=5,
                        bbox=dict(boxstyle="round,pad=0.12", fc=OBJ_COLOR,
                                  ec="none", alpha=0.9))

    # -- relation edges ----------------------------------------------------
    n_cross = n_same = 0
    for r in relations[:max_edges]:
        a = centers.get(int(r.get("subject", -1)))
        b = centers.get(int(r.get("object", -1)))
        if a is None or b is None:
            continue
        cross = bool(r.get("cross_tile"))
        ax.plot([a[0], b[0]], [a[1], b[1]],
                color=CROSS_COLOR if cross else SAME_COLOR,
                linewidth=1.6 if cross else 0.9,
                alpha=0.95 if cross else 0.55,
                zorder=4 if cross else 3.5,
                solid_capstyle="round")
        if cross:
            n_cross += 1
        else:
            n_same += 1

    handles = [
        mpatches.Patch(facecolor="none", edgecolor=TILE_COLOR, linestyle="--",
                       label="Selected tile"),
        mpatches.Patch(facecolor="none", edgecolor=OBJ_COLOR, label="Detected object"),
        mpatches.Patch(color=CROSS_COLOR, label="Cross-tile relation ({})".format(n_cross)),
        mpatches.Patch(color=SAME_COLOR, label="Within-tile relation ({})".format(n_same)),
    ]
    ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.06),
              ncol=4, fontsize=7.5)

    title = "{}  |  {}".format(record.get("uid", "?"), record.get("task", ""))
    ax.set_title(title, loc="left", fontsize=9, color=INK)
    stem = stem or "qual_graph_{}".format(str(record.get("uid", "sample"))[:40])
    return _save(fig, out_dir, stem)


def side_by_side(
    image_path: str,
    record: Dict[str, Any],
    out_dir: str,
    stem: Optional[str] = None,
    n_crops: int = 3,
    overview_side: int = 700,
) -> List[str]:
    """Overview beside the selected high-resolution crops.

    Illustrates the premise of the study: at overview scale the target is a few
    pixels; at native scale it is legible.
    """
    plt = _mpl()
    if plt is None:
        return []
    art = record.get("artifacts") or {}
    graph = art.get("scene_graph") or {}
    img_size = graph.get("image_size") or []
    if len(img_size) != 2:
        return []

    chosen: List[int] = []
    for sel in (art.get("selection") or []):
        chosen.extend(sel.get("chosen") or [])
    if not chosen:
        LOG.warning("side_by_side: no selected tiles recorded for %s", record.get("uid"))
        return []

    from ..tiling.tiler import plan_tiles
    tsize = int(art.get("tile_size") or 1024)
    tover = int(art.get("overlap") or 128)
    try:
        plan = {t.tile_id: t for t in plan_tiles(int(img_size[0]), int(img_size[1]),
                                                 tsize, tover)}
    except Exception as exc:
        LOG.error("side_by_side: could not rebuild the tile plan: %s", exc)
        return []

    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        full = Image.open(image_path)
        crops = []
        for tid in chosen[:n_crops]:
            t = plan.get(tid)
            if t is None:
                continue
            c = full.crop(t.box)
            if c.mode != "RGB":
                c = c.convert("RGB")
            crops.append((tid, c))
    except Exception as exc:
        LOG.error("side_by_side: could not read crops from %s: %s", image_path, exc)
        return []

    overview = _load_overview(image_path, overview_side)
    if overview is None or not crops:
        return []

    n = 1 + len(crops)
    fig, axes = plt.subplots(1, n, figsize=(3.0 * n, 3.2))
    if n == 1:
        axes = [axes]

    axes[0].imshow(overview)
    axes[0].set_title("Overview {}x{}\n(what a direct call sees)".format(
        img_size[0], img_size[1]), fontsize=8, color=INK_2)
    axes[0].axis("off")

    for ax, (tid, crop) in zip(axes[1:], crops):
        ax.imshow(crop)
        ax.set_title("Tile {} at native scale\n{}x{}".format(
            tid, crop.size[0], crop.size[1]), fontsize=8, color=INK_2)
        ax.axis("off")

    fig.suptitle("{}  |  {}".format(record.get("uid", "?"), record.get("task", "")),
                 x=0.005, ha="left", fontsize=9, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    stem = stem or "qual_sbs_{}".format(str(record.get("uid", "sample"))[:40])
    return _save(fig, out_dir, stem)


def case_card(records_by_arm: Dict[str, Dict[str, Any]], uid: str,
              out_dir: str) -> Optional[str]:
    """A markdown trace of one sample across arms, for the failure-case analysis."""
    out = ensure_dir(out_dir)
    lines: List[str] = ["# Case: {}".format(uid), ""]

    any_rec = next((r for r in records_by_arm.values() if r), None)
    if any_rec is None:
        return None
    lines += [
        "- Task: **{}** ({})".format(any_rec.get("task"), any_rec.get("l2")),
        "- Group: **{}**".format(any_rec.get("rel_group")),
        "- Ground truth: `{}`".format(any_rec.get("gt")),
        "",
        "## Answers by arm",
        "",
        "| Arm | Parsed | Correct | VLM calls | Objects | Relations |",
        "|---|---|---|---|---|---|",
    ]
    for arm in ("b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"):
        r = records_by_arm.get(arm)
        if not r:
            continue
        comp = r.get("compute") or {}
        lines.append("| {} | `{}` | {} | {} | {} | {} |".format(
            arm, r.get("parsed"),
            "yes" if r.get("correct") else ("--" if r.get("correct") is None else "no"),
            comp.get("n_vlm_calls"), r.get("n_objects"), r.get("n_relations"),
        ))

    prop = records_by_arm.get("proposed_ctsr") or {}
    graph = (prop.get("artifacts") or {}).get("scene_graph") or {}
    objects = graph.get("objects") or []
    relations = graph.get("relations") or []
    if objects:
        lines += ["", "## Objects (global coordinates)", "",
                  "| id | label | bbox | tiles |", "|---|---|---|---|"]
        for o in objects[:40]:
            lines.append("| {} | {} | {} | {} |".format(
                o.get("obj_id"), o.get("label"), o.get("bbox_global"),
                o.get("merged_from")))
    if relations:
        lines += ["", "## Relations", "",
                  "| subject | predicate | object | value | cross-tile |",
                  "|---|---|---|---|---|"]
        for r in relations[:60]:
            lines.append("| #{} | {} | #{} | {} | {} |".format(
                r.get("subject"), r.get("predicate"), r.get("object"),
                r.get("value", ""), "yes" if r.get("cross_tile") else "no"))

    for arm in ("b3_selected", "proposed_ctsr"):
        r = records_by_arm.get(arm)
        if r and r.get("raw_text"):
            lines += ["", "## Raw response: {}".format(arm), "", "```",
                      str(r["raw_text"])[:2000], "```"]

    path = out / "case_{}.md".format(str(uid)[:60].replace("/", "_"))
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def pick_interesting_cases(results_dir: str, baseline_arm: str = "b3_selected",
                           proposed_arm: str = "proposed_ctsr",
                           n_each: int = 3) -> Dict[str, List[str]]:
    """Find the samples worth showing: wins, losses, and shared failures.

    'Wins' (baseline wrong, proposed right) on relational tasks with many
    cross-tile relations are the strongest qualitative evidence; 'losses' are
    required for an honest failure analysis and must appear in the paper too.
    """
    root = Path(results_dir)
    a_path = root / baseline_arm / "predictions.jsonl"
    b_path = root / proposed_arm / "predictions.jsonl"
    if not (a_path.exists() and b_path.exists()):
        LOG.warning("pick_interesting_cases: need both %s and %s",
                    baseline_arm, proposed_arm)
        return {"wins": [], "losses": [], "both_wrong": []}

    a = {r["uid"]: r for r in load_jsonl(a_path) if r.get("uid")}
    b = {r["uid"]: r for r in load_jsonl(b_path) if r.get("uid")}

    wins: List[Tuple[int, str]] = []
    losses: List[Tuple[int, str]] = []
    both: List[Tuple[int, str]] = []
    for uid in sorted(set(a) & set(b)):
        ca, cb = a[uid].get("correct"), b[uid].get("correct")
        if ca is None or cb is None:
            continue
        gs = ((b[uid].get("artifacts") or {}).get("graph_stats") or {})
        weight = int(gs.get("n_cross_tile") or 0)
        if (not ca) and cb:
            wins.append((weight, uid))
        elif ca and (not cb):
            losses.append((weight, uid))
        elif (not ca) and (not cb):
            both.append((weight, uid))

    for lst in (wins, losses, both):
        lst.sort(key=lambda t: (-t[0], t[1]))
    return {
        "wins": [u for _, u in wins[:n_each]],
        "losses": [u for _, u in losses[:n_each]],
        "both_wrong": [u for _, u in both[:n_each]],
    }


def write_qualitative_set(results_dir: str, out_dir: str,
                          image_lookup: Optional[Dict[str, str]] = None,
                          n_each: int = 3) -> Dict[str, Any]:
    """Generate the qualitative figure set for the interesting cases.

    `image_lookup` maps uid -> image path. Without it, overlays are skipped (the
    prediction records do not store image paths) but case cards are still written,
    since those need no pixels.
    """
    out = ensure_dir(out_dir)
    picks = pick_interesting_cases(results_dir, n_each=n_each)
    root = Path(results_dir)

    by_arm: Dict[str, Dict[str, Any]] = {}
    for arm_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        p = arm_dir / "predictions.jsonl"
        if p.exists():
            by_arm[arm_dir.name] = {r["uid"]: r for r in load_jsonl(p) if r.get("uid")}

    made: Dict[str, Any] = {"cases": {}, "picks": picks, "figures": []}
    for kind, uids in picks.items():
        for uid in uids:
            per_arm = {arm: recs.get(uid) for arm, recs in by_arm.items()}
            card = case_card(per_arm, uid, out)
            made["cases"].setdefault(kind, []).append(card)

            prop = per_arm.get("proposed_ctsr")
            img = (image_lookup or {}).get(uid)
            if prop and img:
                try:
                    made["figures"].extend(
                        overlay_scene_graph(prop, img, out,
                                            stem="qual_{}_{}".format(kind, str(uid)[:30]))
                    )
                    made["figures"].extend(
                        side_by_side(img, prop, out,
                                     stem="qual_sbs_{}_{}".format(kind, str(uid)[:30]))
                    )
                except Exception as exc:
                    LOG.error("Qualitative figure failed for %s: %s", uid, exc)
    if not image_lookup:
        LOG.info("No image_lookup supplied; overlays skipped. Pass the uid->path map "
                 "from the loaded dataset to enable them.")
    return made
