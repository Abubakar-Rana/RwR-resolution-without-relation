"""Cross-tile duplicate removal.

Overlapping tiles mean the same physical object can be reported two to four
times. If those duplicates survive, two things break:

  * counting answers inflate, and
  * the scene graph gains phantom "adjacent to" edges between an object and
    itself, which is exactly the kind of spurious relation that would discredit
    the method.

"Duplicate objects across overlapping tiles" is an explicit error category in
plan section 10, so the merge statistics are recorded per sample rather than
being an invisible implementation detail.

Strategy: label-aware greedy merging by descending confidence. Two detections
merge when their labels are compatible AND (IoU >= iou_thresh OR one is largely
contained in the other). Boxes from different tiles are additionally allowed to
merge on a looser threshold, because a seam-truncated object yields two partial
boxes whose IoU is low even though they are the same object.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..data.schema import DetectedObject
from ..utils.logging_utils import get_logger
from .coords import edge_gap, ioa, iou

LOG = get_logger("ctsr.spatial.dedup")

# Label synonyms treated as the same class when merging. Deliberately
# conservative: merging genuinely different classes would corrupt counts.
_SYNONYM_GROUPS: List[set] = [
    {"car", "cars", "vehicle", "vehicles", "automobile", "sedan"},
    {"truck", "trucks", "lorry"},
    {"bus", "buses"},
    {"building", "buildings", "house", "houses", "structure", "structures"},
    {"road", "roads", "street", "streets", "highway", "roadway"},
    {"tree", "trees"},
    {"plane", "planes", "aircraft", "airplane", "airplanes", "jet"},
    {"ship", "ships", "boat", "boats", "vessel", "vessels"},
    {"water", "waterbody", "water body", "lake", "pond", "river"},
    {"field", "fields", "farmland", "cropland", "agricultural land"},
    {"parkinglot", "parking lot", "parking", "car park"},
    {"bridge", "bridges"},
    {"storagetank", "storage tank", "tank", "tanks", "silo", "silos"},
]


def normalise_label(label: Optional[str]) -> str:
    s = re.sub(r"[^a-z0-9 ]+", " ", str(label or "").lower()).strip()
    s = re.sub(r"\s+", " ", s)
    return s


def label_key(label: Optional[str]) -> str:
    """Canonical class key: a synonym-group representative, else the plural-stripped label."""
    s = normalise_label(label)
    if not s:
        return "object"
    compact = s.replace(" ", "")
    for group in _SYNONYM_GROUPS:
        if s in group or compact in {g.replace(" ", "") for g in group}:
            return sorted(group)[0]
    if s.endswith("es") and len(s) > 4:
        return s[:-2]
    if s.endswith("s") and not s.endswith("ss") and len(s) > 3:
        return s[:-1]
    return s


def labels_compatible(a: Optional[str], b: Optional[str], strict: bool = False) -> bool:
    ka, kb = label_key(a), label_key(b)
    if ka == kb:
        return True
    if strict:
        return False
    # A generic label should not block a merge with a specific one.
    if ka in ("object", "unknown") or kb in ("object", "unknown"):
        return True
    return ka in kb or kb in ka


@dataclass
class MergeStats:
    n_input: int = 0
    n_output: int = 0
    n_merged: int = 0
    n_cross_tile_merges: int = 0
    n_dropped_degenerate: int = 0
    n_dropped_oversize: int = 0

    @property
    def duplicate_rate(self) -> float:
        return (self.n_merged / self.n_input) if self.n_input else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_input": self.n_input,
            "n_output": self.n_output,
            "n_merged": self.n_merged,
            "n_cross_tile_merges": self.n_cross_tile_merges,
            "n_dropped_degenerate": self.n_dropped_degenerate,
            "n_dropped_oversize": self.n_dropped_oversize,
            "duplicate_rate": round(self.duplicate_rate, 4),
        }


def _merge_boxes(objs: Sequence[DetectedObject], mode: str = "union") -> Tuple[float, float, float, float]:
    """Combine boxes of a duplicate cluster.

    "union" is right for seam-truncated objects (two halves make the whole);
    "highest" keeps the most confident box, which is safer when the cluster may
    contain a false positive.
    """
    if mode == "highest":
        best = max(objs, key=lambda o: o.score)
        return best.bbox_global
    if mode == "mean":
        n = float(len(objs))
        return (
            sum(o.bbox_global[0] for o in objs) / n,
            sum(o.bbox_global[1] for o in objs) / n,
            sum(o.bbox_global[2] for o in objs) / n,
            sum(o.bbox_global[3] for o in objs) / n,
        )
    return (
        min(o.bbox_global[0] for o in objs),
        min(o.bbox_global[1] for o in objs),
        max(o.bbox_global[2] for o in objs),
        max(o.bbox_global[3] for o in objs),
    )


def merge_detections(
    objects: Sequence[DetectedObject],
    iou_thresh: float = 0.45,
    cross_tile_iou_thresh: float = 0.25,
    containment_thresh: float = 0.80,
    seam_gap_px: float = 8.0,
    strict_labels: bool = False,
    box_mode: str = "union",
    image_size: Optional[Tuple[int, int]] = None,
    max_area_frac: float = 0.98,
    min_side_px: float = 2.0,
) -> Tuple[List[DetectedObject], MergeStats]:
    """Greedy, label-aware, confidence-ordered merge.

    Returns deduplicated objects with fresh sequential `obj_id`s (the ids the
    scene graph and the prompt will use) and the merge statistics.
    """
    stats = MergeStats(n_input=len(objects))

    # 1) Drop degenerate and implausibly huge boxes before merging.
    kept: List[DetectedObject] = []
    img_area = float(image_size[0] * image_size[1]) if image_size else None
    for o in objects:
        if o.width < min_side_px or o.height < min_side_px:
            stats.n_dropped_degenerate += 1
            continue
        if img_area and o.area > max_area_frac * img_area:
            # A box covering the whole scene carries no localisation information
            # and would dominate every containment relation.
            stats.n_dropped_oversize += 1
            continue
        kept.append(o)

    # 2) Greedy clustering, most confident first (ties by area then label for
    #    determinism).
    order = sorted(kept, key=lambda o: (-float(o.score), -o.area, label_key(o.label)))
    clusters: List[List[DetectedObject]] = []

    for obj in order:
        placed = False
        for cluster in clusters:
            rep = cluster[0]
            if not labels_compatible(rep.label, obj.label, strict=strict_labels):
                continue
            ov = iou(rep.bbox_global, obj.bbox_global)
            same_tile = (rep.tile_id == obj.tile_id)
            thresh = iou_thresh if same_tile else cross_tile_iou_thresh
            contained = max(ioa(obj.bbox_global, rep.bbox_global),
                            ioa(rep.bbox_global, obj.bbox_global)) >= containment_thresh
            # Seam case: two partial boxes of one object nearly touch across a
            # tile boundary and are roughly aligned on the shared axis.
            seam = (
                not same_tile
                and edge_gap(rep.bbox_global, obj.bbox_global) <= seam_gap_px
                and _axis_aligned(rep.bbox_global, obj.bbox_global)
            )
            if ov >= thresh or contained or seam:
                cluster.append(obj)
                placed = True
                if not same_tile:
                    stats.n_cross_tile_merges += 1
                break
        if not placed:
            clusters.append([obj])

    # 3) Emit one object per cluster.
    out: List[DetectedObject] = []
    for i, cluster in enumerate(clusters):
        rep = cluster[0]
        merged = DetectedObject(
            label=_best_label(cluster),
            bbox_global=_merge_boxes(cluster, box_mode) if len(cluster) > 1 else rep.bbox_global,
            score=max(o.score for o in cluster),
            tile_id=rep.tile_id,
            attributes=_merge_attributes(cluster),
            obj_id=i,
            merged_from=sorted({o.tile_id for o in cluster if o.tile_id is not None}),
        )
        merged.attributes["n_observations"] = len(cluster)
        out.append(merged)
        stats.n_merged += len(cluster) - 1

    stats.n_output = len(out)
    return out, stats


def _axis_aligned(a, b, tol_frac: float = 0.5) -> bool:
    """Whether two boxes overlap substantially on one axis (seam heuristic)."""
    ox = min(a[2], b[2]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[1], b[1])
    min_w = min(a[2] - a[0], b[2] - b[0])
    min_h = min(a[3] - a[1], b[3] - b[1])
    x_ok = min_w > 0 and ox >= tol_frac * min_w
    y_ok = min_h > 0 and oy >= tol_frac * min_h
    return bool(x_ok or y_ok)


def _best_label(cluster: Sequence[DetectedObject]) -> str:
    """Prefer the most specific label in the cluster, then the most frequent."""
    from collections import Counter

    labels = [str(o.label) for o in cluster if str(o.label).strip()]
    if not labels:
        return "object"
    specific = [l for l in labels if normalise_label(l) not in ("object", "unknown", "")]
    pool = specific or labels
    counts = Counter(normalise_label(l) for l in pool)
    best_norm, _ = max(counts.items(), key=lambda kv: (kv[1], len(kv[0])))
    for l in pool:
        if normalise_label(l) == best_norm:
            return l
    return pool[0]


def _merge_attributes(cluster: Sequence[DetectedObject]) -> Dict[str, Any]:
    """Union of attributes; first non-empty value wins per key."""
    out: Dict[str, Any] = {}
    for o in cluster:
        for k, v in (o.attributes or {}).items():
            if k not in out and v not in (None, "", []):
                out[k] = v
    return out


def cap_objects(objects: Sequence[DetectedObject], max_objects: int,
                keep_labels: Optional[Sequence[str]] = None) -> List[DetectedObject]:
    """Limit the object list to a token budget, keeping the most useful ones.

    Priority: objects whose label matches a question keyword, then by confidence,
    then by area. Re-assigns `obj_id` so ids in the prompt stay contiguous.
    """
    if max_objects <= 0 or len(objects) <= max_objects:
        return list(objects)

    wanted = {label_key(k) for k in (keep_labels or [])}

    def priority(o: DetectedObject) -> tuple:
        relevant = 1 if (wanted and any(w in label_key(o.label) or label_key(o.label) in w
                                        for w in wanted)) else 0
        return (-relevant, -float(o.score), -o.area)

    chosen = sorted(objects, key=priority)[:max_objects]
    # Restore a stable reading order (top-to-bottom, left-to-right) for the prompt.
    chosen = sorted(chosen, key=lambda o: (o.cy, o.cx))
    for i, o in enumerate(chosen):
        o.obj_id = i
    return chosen
