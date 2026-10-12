"""Geometric spatial relations over globally-registered objects.

Plan section 5.4 asks for "direction, distance, adjacency, containment, and
intersection where applicable". Each is computed here from geometry alone - no
learned component, no VLM call. That is deliberate: the claim under test is that
*explicit* geometry helps, so the relation module must be cheap and auditable.

Conventions, stated because they are easy to get wrong:

  * Image coordinates run y-downwards, so in a north-up remote sensing image
    DECREASING y is NORTH. Compass naming uses this; `use_compass=False` falls
    back to image-relative wording ("above"/"below") when the image is not known
    to be north-up.
  * Direction is measured between box CENTRES.
  * Adjacency uses the gap between box BORDERS, not centre distance, so that two
    large neighbouring regions are correctly called adjacent.
  * Distances are reported in normalised units (fraction of the image diagonal)
    and in pixels. If a ground sample distance is supplied, metres are added -
    otherwise no metric distance is stated, because inventing one would be a
    fabricated quantity.

Complexity: all-pairs is O(n^2). With `max_neighbours` each object keeps only its
k nearest partners, which bounds both compute and the prompt token count.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..data.schema import DetectedObject
from ..utils.logging_utils import get_logger
from .coords import center_distance, edge_gap, intersection_area, ioa, iou

LOG = get_logger("ctsr.spatial.relations")

# 8-point compass, image y-down. Index = round(angle / 45) where angle is
# measured clockwise from north.
_COMPASS = ["north", "north-east", "east", "south-east",
            "south", "south-west", "west", "north-west"]
_IMAGE_REL = ["above", "upper-right", "right", "lower-right",
              "below", "lower-left", "left", "upper-left"]


def direction_between(a: DetectedObject, b: DetectedObject,
                      use_compass: bool = True,
                      deadzone_px: float = 1.0) -> Optional[str]:
    """Direction of `b` relative to `a` ("b is <dir> of a").

    Returns None when the centres are essentially coincident, since a direction
    would then be noise.
    """
    dx = b.cx - a.cx
    dy = b.cy - a.cy
    if math.hypot(dx, dy) < deadzone_px:
        return None
    # Clockwise angle from north. North is -y, east is +x.
    angle = math.degrees(math.atan2(dx, -dy)) % 360.0
    idx = int((angle + 22.5) // 45) % 8
    return (_COMPASS if use_compass else _IMAGE_REL)[idx]


def bearing_between(a: DetectedObject, b: DetectedObject) -> float:
    """Clockwise bearing in degrees from north, for the quantitative record."""
    return math.degrees(math.atan2(b.cx - a.cx, -(b.cy - a.cy))) % 360.0


@dataclass
class Relation:
    """One directed edge: subject -> object."""

    subject: int
    object: int
    predicate: str          # direction | adjacent | contains | inside | intersects | near
    value: Optional[str] = None      # e.g. the compass term
    distance_px: Optional[float] = None
    distance_norm: Optional[float] = None
    distance_m: Optional[float] = None
    bearing_deg: Optional[float] = None
    iou: Optional[float] = None
    containment: Optional[float] = None
    cross_tile: bool = False

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "subject": self.subject,
            "object": self.object,
            "predicate": self.predicate,
            "cross_tile": self.cross_tile,
        }
        if self.value is not None:
            d["value"] = self.value
        for k in ("distance_px", "distance_norm", "distance_m", "bearing_deg",
                  "iou", "containment"):
            v = getattr(self, k)
            if v is not None:
                d[k] = round(float(v), 4)
        return d


@dataclass
class RelationConfig:
    """Thresholds for relation construction.

    Fractions are of the image diagonal, so a threshold means the same thing on
    an 8500px and a 10000px scene.
    """

    max_neighbours: int = 6
    adjacency_gap_frac: float = 0.012
    near_dist_frac: float = 0.06
    containment_thresh: float = 0.85
    intersect_iou_thresh: float = 0.05
    # IoU alone misses the most important intersection case in remote sensing:
    # two ELONGATED features crossing. A road (1000x50 px) crossing a river
    # (50x300 px) shares 2500 px^2, which is 17% of the river but only IoU 0.04 -
    # below any sensible IoU threshold, so the pair would be reported merely as
    # "adjacent". Triggering on the overlap as a fraction of the SMALLER object
    # catches crossings while staying well under the containment threshold.
    intersect_min_overlap_frac: float = 0.05
    include_direction: bool = True
    include_distance: bool = True
    include_adjacency: bool = True
    include_containment: bool = True
    include_intersection: bool = True
    use_compass: bool = True
    gsd_m_per_px: Optional[float] = None
    max_relations: int = 220
    symmetric_direction: bool = False  # emit only one direction edge per pair

    def to_dict(self) -> Dict[str, Any]:
        return dict(vars(self))


def build_relations(
    objects: Sequence[DetectedObject],
    image_size: Tuple[int, int],
    cfg: Optional[RelationConfig] = None,
) -> List[Relation]:
    """Construct the geometric relation set for one image.

    Returns edges sorted so that the most informative ones survive truncation:
    containment and intersection first (they are rare and highly constraining),
    then adjacency, then direction/distance by increasing distance.
    """
    cfg = cfg or RelationConfig()
    n = len(objects)
    if n < 2:
        return []

    W, H = float(image_size[0]), float(image_size[1])
    diag = math.hypot(W, H) or 1.0
    adj_gap = cfg.adjacency_gap_frac * diag
    near_dist = cfg.near_dist_frac * diag

    # Neighbour restriction: for each object keep the k nearest by centre
    # distance. Pairs are unordered, so a pair survives if either endpoint
    # nominates it.
    pairs = _candidate_pairs(objects, cfg.max_neighbours)

    relations: List[Relation] = []
    for i, j in pairs:
        a, b = objects[i], objects[j]
        sid = a.obj_id if a.obj_id is not None else i
        oid = b.obj_id if b.obj_id is not None else j
        cross = _is_cross_tile(a, b)

        d_px = center_distance(a.bbox_global, b.bbox_global)
        d_norm = d_px / diag
        d_m = (d_px * cfg.gsd_m_per_px) if cfg.gsd_m_per_px else None
        gap = edge_gap(a.bbox_global, b.bbox_global)
        ov = iou(a.bbox_global, b.bbox_global)
        c_ab = ioa(a.bbox_global, b.bbox_global)   # a inside b
        c_ba = ioa(b.bbox_global, a.bbox_global)   # b inside a

        # -- containment (strongest, checked first) -------------------------
        if cfg.include_containment and max(c_ab, c_ba) >= cfg.containment_thresh:
            if c_ab >= c_ba:
                relations.append(Relation(subject=sid, object=oid, predicate="inside",
                                          containment=c_ab, iou=ov, cross_tile=cross))
            else:
                relations.append(Relation(subject=sid, object=oid, predicate="contains",
                                          containment=c_ba, iou=ov, cross_tile=cross))
            continue

        # -- intersection ---------------------------------------------------
        # Either a substantial IoU, or a meaningful bite out of the smaller
        # object (the crossing-elongated-features case).
        overlap_frac = max(c_ab, c_ba)
        if cfg.include_intersection and (
            ov >= cfg.intersect_iou_thresh
            or overlap_frac >= cfg.intersect_min_overlap_frac
        ):
            relations.append(Relation(subject=sid, object=oid, predicate="intersects",
                                      iou=ov, containment=overlap_frac,
                                      distance_px=d_px, distance_norm=d_norm,
                                      distance_m=d_m, cross_tile=cross))
            continue

        # -- adjacency ------------------------------------------------------
        if cfg.include_adjacency and gap <= adj_gap:
            relations.append(Relation(
                subject=sid, object=oid, predicate="adjacent",
                value=direction_between(a, b, cfg.use_compass) if cfg.include_direction else None,
                distance_px=d_px, distance_norm=d_norm, distance_m=d_m,
                bearing_deg=bearing_between(a, b), cross_tile=cross,
            ))
            continue

        # -- direction / proximity -----------------------------------------
        if cfg.include_direction:
            value = direction_between(a, b, cfg.use_compass)
            if value is not None:
                predicate = "near" if (cfg.include_distance and d_px <= near_dist) else "direction"
                relations.append(Relation(
                    subject=sid, object=oid, predicate=predicate, value=value,
                    distance_px=d_px, distance_norm=d_norm, distance_m=d_m,
                    bearing_deg=bearing_between(a, b), cross_tile=cross,
                ))

    relations = _prioritise(relations, cfg.max_relations)
    return relations


_PREDICATE_RANK = {"contains": 0, "inside": 0, "intersects": 1,
                   "adjacent": 2, "near": 3, "direction": 4}


def _prioritise(relations: List[Relation], max_relations: int) -> List[Relation]:
    """Sort by informativeness, then truncate.

    Cross-tile edges are promoted within their predicate class, because those are
    precisely the relations the baselines cannot represent and are therefore the
    ones the experiment is about.
    """
    relations.sort(key=lambda r: (
        _PREDICATE_RANK.get(r.predicate, 9),
        0 if r.cross_tile else 1,
        r.distance_norm if r.distance_norm is not None else 0.0,
        r.subject, r.object,
    ))
    if max_relations > 0 and len(relations) > max_relations:
        LOG.debug("Truncating %d relations to %d", len(relations), max_relations)
        return relations[:max_relations]
    return relations


def _candidate_pairs(objects: Sequence[DetectedObject], k: int) -> List[Tuple[int, int]]:
    n = len(objects)
    if k <= 0 or k >= n - 1:
        return [(i, j) for i in range(n) for j in range(i + 1, n)]

    keep = set()
    for i in range(n):
        dists = sorted(
            ((center_distance(objects[i].bbox_global, objects[j].bbox_global), j)
             for j in range(n) if j != i),
            key=lambda t: (t[0], t[1]),
        )
        for _, j in dists[:k]:
            keep.add((min(i, j), max(i, j)))
    return sorted(keep)


def _is_cross_tile(a: DetectedObject, b: DetectedObject) -> bool:
    """Whether this pair spans tiles, i.e. a relation independent tiling cannot see.

    Uses the merge provenance: an object merged from several tiles belongs to all
    of them, so a pair is same-tile only if their tile sets intersect.
    """
    ta = set(a.merged_from or ([a.tile_id] if a.tile_id is not None else []))
    tb = set(b.merged_from or ([b.tile_id] if b.tile_id is not None else []))
    if not ta or not tb:
        return False
    return not (ta & tb)


def relation_stats(relations: Sequence[Relation]) -> Dict[str, Any]:
    """Diagnostics recorded per sample: how much cross-tile structure was found.

    `cross_tile_fraction` is the key descriptive statistic for the paper: it
    quantifies how much of the relational structure is invisible to independent
    tiling.
    """
    from collections import Counter

    by_pred = Counter(r.predicate for r in relations)
    n_cross = sum(1 for r in relations if r.cross_tile)
    return {
        "n_relations": len(relations),
        "n_cross_tile": n_cross,
        "cross_tile_fraction": round(n_cross / len(relations), 4) if relations else 0.0,
        "by_predicate": dict(by_pred.most_common()),
    }
