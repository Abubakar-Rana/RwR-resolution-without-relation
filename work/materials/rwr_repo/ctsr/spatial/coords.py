"""Coordinate transforms: tile-local -> global image space.

This is the mechanical heart of contribution #2 in the plan ("a lightweight
geometric relation representation that connects objects identified across
independently processed image tiles using a common global coordinate system").
Every relation downstream is only as correct as this transform, so the
conventions are stated explicitly and the tile-local input format is detected
rather than assumed.

Three coordinate spaces are in play:

  local-normalised   what a VLM emits for a crop. Qwen-family models are usually
                     prompted to emit either 0-1000 integers or 0-1 floats over
                     the *crop* it was shown.
  local-pixel        pixels within the crop that was shown to the model. Note
                     this is the crop's own size, which may differ from the tile
                     box if the crop was resized before being sent.
  global-pixel       absolute pixels of the full-resolution image. The canonical
                     space for all relations.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, Sequence, Tuple

from ..utils.logging_utils import get_logger
from ..tiling.tiler import TileSpec

LOG = get_logger("ctsr.spatial.coords")

BBox = Tuple[float, float, float, float]


def detect_bbox_scale(bbox: Sequence[float], crop_size: Optional[Tuple[int, int]] = None) -> str:
    """Infer which convention a model-emitted box uses.

    Returns "unit" (0-1), "thousand" (0-1000), or "pixel".

    The ordering of the checks matters: a box like [0.2, 0.3, 0.5, 0.6] is
    unambiguously unit-normalised, whereas [120, 300, 480, 640] could be either
    0-1000 normalised or raw pixels. When `crop_size` is known we prefer "pixel"
    if the values plausibly fit inside the crop, because that is the more common
    literal reading; otherwise we assume the 0-1000 convention that Qwen prompts
    typically elicit.
    """
    vals = [float(v) for v in bbox[:4]]
    if not vals:
        return "pixel"
    mx = max(abs(v) for v in vals)
    if mx <= 1.5:
        return "unit"
    if crop_size is not None:
        cw, ch = crop_size
        limit = max(cw, ch)
        if mx <= limit * 1.02:
            # Fits the crop. If the crop is much smaller than 1000 this is
            # almost certainly pixels; if the crop is ~1000px wide both readings
            # coincide anyway.
            return "pixel"
        if mx <= 1000.0 * 1.02:
            return "thousand"
        return "pixel"
    if mx <= 1000.0 * 1.02:
        return "thousand"
    return "pixel"


def to_local_pixels(
    bbox: Sequence[float],
    crop_size: Tuple[int, int],
    scale_hint: Optional[str] = None,
) -> Optional[BBox]:
    """Normalise any model-emitted box into pixels of the crop shown."""
    try:
        vals = [float(v) for v in list(bbox)[:4]]
    except (TypeError, ValueError):
        return None
    if len(vals) != 4:
        return None
    if not all(v == v for v in vals):  # reject NaN
        return None

    cw, ch = float(crop_size[0]), float(crop_size[1])
    if cw <= 0 or ch <= 0:
        return None

    mode = scale_hint or detect_bbox_scale(vals, (int(cw), int(ch)))
    if mode == "unit":
        x1, y1, x2, y2 = vals[0] * cw, vals[1] * ch, vals[2] * cw, vals[3] * ch
    elif mode == "thousand":
        x1, y1, x2, y2 = (vals[0] / 1000.0 * cw, vals[1] / 1000.0 * ch,
                          vals[2] / 1000.0 * cw, vals[3] / 1000.0 * ch)
    else:
        x1, y1, x2, y2 = vals

    # Models sometimes emit (x, y, w, h) or a reversed corner order.
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1
    return (x1, y1, x2, y2)


def lift_to_global(
    bbox_local: BBox,
    tile: TileSpec,
    crop_size: Optional[Tuple[int, int]] = None,
    clamp: bool = True,
    image_size: Optional[Tuple[int, int]] = None,
) -> Optional[BBox]:
    """Map a crop-local pixel box into absolute full-image pixels.

    `crop_size` is the size of the image *as shown to the model*. When the crop
    was resized (the usual case, because the VLM has a pixel budget), the box
    must be rescaled by tile_extent / crop_extent before translation - skipping
    this is the classic source of systematically shifted global coordinates.
    """
    x1, y1, x2, y2 = [float(v) for v in bbox_local]

    tw, th = float(tile.width), float(tile.height)
    if crop_size is not None:
        cw, ch = float(crop_size[0]), float(crop_size[1])
        if cw > 0 and ch > 0 and (abs(cw - tw) > 0.5 or abs(ch - th) > 0.5):
            sx, sy = tw / cw, th / ch
            x1, x2 = x1 * sx, x2 * sx
            y1, y2 = y1 * sy, y2 * sy

    gx1, gy1 = x1 + tile.x0, y1 + tile.y0
    gx2, gy2 = x2 + tile.x0, y2 + tile.y0

    if clamp:
        max_x = float(image_size[0]) if image_size else float(tile.x1)
        max_y = float(image_size[1]) if image_size else float(tile.y1)
        gx1 = min(max(0.0, gx1), max_x)
        gx2 = min(max(0.0, gx2), max_x)
        gy1 = min(max(0.0, gy1), max_y)
        gy2 = min(max(0.0, gy2), max_y)

    if gx2 - gx1 < 1e-6 or gy2 - gy1 < 1e-6:
        return None  # degenerate after clamping
    return (gx1, gy1, gx2, gy2)


def global_to_norm(bbox: BBox, image_size: Tuple[int, int],
                   scale: int = 1000) -> Tuple[int, int, int, int]:
    """Global pixels -> integer 0-`scale` coordinates, for putting back in a prompt.

    Feeding raw 8500-scale pixel numbers to the model wastes tokens and is harder
    for it to reason over than a consistent 0-1000 grid.
    """
    w, h = float(image_size[0]), float(image_size[1])
    if w <= 0 or h <= 0:
        return (0, 0, 0, 0)
    return (
        int(round(min(max(bbox[0] / w, 0.0), 1.0) * scale)),
        int(round(min(max(bbox[1] / h, 0.0), 1.0) * scale)),
        int(round(min(max(bbox[2] / w, 0.0), 1.0) * scale)),
        int(round(min(max(bbox[3] / h, 0.0), 1.0) * scale)),
    )


def norm_to_global(bbox: Sequence[float], image_size: Tuple[int, int],
                   scale: int = 1000) -> BBox:
    """Inverse of `global_to_norm`, for scoring a grounding answer in pixels."""
    w, h = float(image_size[0]), float(image_size[1])
    return (
        float(bbox[0]) / scale * w,
        float(bbox[1]) / scale * h,
        float(bbox[2]) / scale * w,
        float(bbox[3]) / scale * h,
    )


def iou(a: BBox, b: BBox) -> float:
    """Intersection over union of two axis-aligned boxes."""
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    iw, ih = ix2 - ix1, iy2 - iy1
    if iw <= 0 or ih <= 0:
        return 0.0
    inter = iw * ih
    area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
    area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
    union = area_a + area_b - inter
    return float(inter / union) if union > 0 else 0.0


def intersection_area(a: BBox, b: BBox) -> float:
    iw = min(a[2], b[2]) - max(a[0], b[0])
    ih = min(a[3], b[3]) - max(a[1], b[1])
    return float(iw * ih) if iw > 0 and ih > 0 else 0.0


def ioa(inner: BBox, outer: BBox) -> float:
    """Intersection over the area of `inner`: the containment measure."""
    area = max(0.0, inner[2] - inner[0]) * max(0.0, inner[3] - inner[1])
    if area <= 0:
        return 0.0
    return intersection_area(inner, outer) / area


def center(bbox: BBox) -> Tuple[float, float]:
    return (0.5 * (bbox[0] + bbox[2]), 0.5 * (bbox[1] + bbox[3]))


def center_distance(a: BBox, b: BBox) -> float:
    import math
    ca, cb = center(a), center(b)
    return math.hypot(ca[0] - cb[0], ca[1] - cb[1])


def edge_gap(a: BBox, b: BBox) -> float:
    """Shortest distance between box borders; 0 when they touch or overlap.

    Adjacency should use this rather than centre distance, otherwise two large
    neighbouring regions read as 'far apart' purely because they are big.
    """
    import math
    dx = max(0.0, max(a[0], b[0]) - min(a[2], b[2]))
    dy = max(0.0, max(a[1], b[1]) - min(a[3], b[3]))
    return math.hypot(dx, dy)


def tile_of_point(x: float, y: float, tiles: Sequence[TileSpec]) -> Optional[int]:
    for t in tiles:
        if t.x0 <= x < t.x1 and t.y0 <= y < t.y1:
            return t.tile_id
    return None


def touches_tile_border(bbox: BBox, tile: TileSpec, tol: float = 2.0) -> bool:
    """Whether a detection abuts the edge of its tile.

    Such detections are the ones most likely to be truncated objects, and are
    tracked separately in the error taxonomy ("tile boundary failures", plan
    section 10).
    """
    return (
        abs(bbox[0] - tile.x0) <= tol
        or abs(bbox[1] - tile.y0) <= tol
        or abs(bbox[2] - tile.x1) <= tol
        or abs(bbox[3] - tile.y1) <= tol
    )
