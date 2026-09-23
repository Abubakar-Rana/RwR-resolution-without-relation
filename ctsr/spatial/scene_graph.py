"""The cross-tile scene graph and its textual serialisation.

The graph is what gets handed to the final reasoning call, so its serialisation
is a method component, not cosmetics: the same geometry rendered badly will not
help the model. Two design choices matter.

1. Coordinates are emitted on a 0-1000 grid over the WHOLE image, never in tile
   coordinates. A model that sees "building #3 at (812, 140)" and "road #7 at
   (806, 155)" can relate them; one that sees two tile-local (120, 140)s cannot.
   This normalisation is the concrete realisation of the "common global
   coordinate system" in plan section 5.4.

2. The text is budgeted. A 10000x10000 scene can yield hundreds of objects, and a
   relation list that overflows the context window silently truncates the
   evidence. `to_text` takes a token budget and prunes by relevance, reporting
   what it dropped.

The ablation in plan section 8 removes exactly the relation block produced here,
keeping objects, tiles, selection and budget identical.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from ..data.schema import DetectedObject
from ..utils.logging_utils import get_logger
from .coords import global_to_norm
from .dedup import label_key
from .relations import Relation, relation_stats

LOG = get_logger("ctsr.spatial.scene_graph")

# Rough characters-per-token, used only to keep the serialisation inside a
# budget. Deliberately conservative so we under-fill rather than overflow.
_CHARS_PER_TOKEN = 3.6

# Chars reserved for the section headers plus the truncation disclosure, so that
# pruning cannot push the output over the budget it was pruning to meet.
_SERIALISATION_OVERHEAD = 260


@dataclass
class SceneGraph:
    objects: List[DetectedObject] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)
    image_size: Tuple[int, int] = (0, 0)
    coord_scale: int = 1000
    image_index: int = 0
    notes: List[str] = field(default_factory=list)

    # -- basic views --------------------------------------------------------
    @property
    def n_objects(self) -> int:
        return len(self.objects)

    @property
    def n_relations(self) -> int:
        return len(self.relations)

    def by_id(self) -> Dict[int, DetectedObject]:
        return {(o.obj_id if o.obj_id is not None else i): o
                for i, o in enumerate(self.objects)}

    def stats(self) -> Dict[str, Any]:
        d = relation_stats(self.relations)
        d["n_objects"] = self.n_objects
        d["n_labels"] = len({label_key(o.label) for o in self.objects})
        d["n_multi_tile_objects"] = sum(1 for o in self.objects if len(o.merged_from or []) > 1)
        return d

    # -- serialisation ------------------------------------------------------
    def object_lines(self, scale: Optional[int] = None,
                     include_score: bool = False) -> List[str]:
        """One line per object: id, label, global box, optional attributes."""
        scale = scale or self.coord_scale
        lines: List[str] = []
        for i, o in enumerate(self.objects):
            oid = o.obj_id if o.obj_id is not None else i
            x1, y1, x2, y2 = global_to_norm(o.bbox_global, self.image_size, scale)
            parts = ["#{} {} box=({},{},{},{})".format(oid, o.label, x1, y1, x2, y2)]
            attrs = {k: v for k, v in (o.attributes or {}).items()
                     if k not in ("n_observations",) and v not in (None, "", [])}
            if attrs:
                parts.append("attrs={}".format(
                    ",".join("{}={}".format(k, v) for k, v in sorted(attrs.items()))))
            if include_score:
                parts.append("conf={:.2f}".format(float(o.score)))
            lines.append(" ".join(parts))
        return lines

    def relation_lines(self, include_metric: bool = True) -> List[str]:
        """One line per relation, in natural-ish but machine-regular phrasing."""
        by_id = self.by_id()
        lines: List[str] = []
        for r in self.relations:
            subj = by_id.get(r.subject)
            obj = by_id.get(r.object)
            if subj is None or obj is None:
                continue
            s_name = "#{} {}".format(r.subject, subj.label)
            o_name = "#{} {}".format(r.object, obj.label)

            if r.predicate == "contains":
                phrase = "{} contains {}".format(s_name, o_name)
            elif r.predicate == "inside":
                phrase = "{} is inside {}".format(s_name, o_name)
            elif r.predicate == "intersects":
                phrase = "{} overlaps {}".format(s_name, o_name)
            elif r.predicate == "adjacent":
                phrase = "{} is adjacent to {}".format(s_name, o_name)
                if r.value:
                    phrase += " (to its {})".format(r.value)
            elif r.predicate == "near":
                phrase = "{} is near {}, to its {}".format(s_name, o_name, r.value or "side")
            else:
                phrase = "{} is to the {} of {}".format(o_name, r.value or "side", s_name)

            if include_metric:
                bits: List[str] = []
                if r.distance_m is not None:
                    bits.append("{:.0f} m".format(r.distance_m))
                elif r.distance_px is not None:
                    bits.append("{:.0f} px".format(r.distance_px))
                if r.containment is not None and r.predicate in ("contains", "inside"):
                    bits.append("overlap {:.0%}".format(r.containment))
                elif r.predicate == "intersects":
                    # The overlap as a share of the smaller object is what tells
                    # the model how substantial a crossing is; a raw IoU between
                    # two elongated features is misleadingly small.
                    if r.containment is not None:
                        bits.append("overlap {:.0%} of the smaller".format(r.containment))
                    elif r.iou is not None:
                        bits.append("IoU {:.2f}".format(r.iou))
                if r.cross_tile:
                    bits.append("cross-tile")
                if bits:
                    phrase += " [{}]".format("; ".join(bits))
            lines.append(phrase)
        return lines

    def to_text(
        self,
        max_tokens: Optional[int] = None,
        include_objects: bool = True,
        include_relations: bool = True,
        include_metric: bool = True,
        question_keywords: Optional[Sequence[str]] = None,
    ) -> str:
        """Render the graph for the prompt, within a token budget.

        Pruning order when over budget: relations first (least-informative last,
        since `build_relations` already sorted them), then objects. Anything
        dropped is stated in the text itself, so the model is not misled into
        thinking it has seen an exhaustive list.
        """
        header = "IMAGE SIZE: {} x {} pixels. Coordinates are (x1,y1,x2,y2) on a 0-{} grid over the whole image; x increases eastward, y increases southward.".format(
            self.image_size[0], self.image_size[1], self.coord_scale)

        obj_lines = self.object_lines() if include_objects else []
        rel_lines = self.relation_lines(include_metric) if include_relations else []

        if question_keywords:
            obj_lines, rel_lines = self._reorder_by_relevance(
                obj_lines, rel_lines, question_keywords)

        budget_chars = int(max_tokens * _CHARS_PER_TOKEN) if max_tokens else None
        dropped_rel = dropped_obj = 0

        def total(o: List[str], r: List[str]) -> int:
            return len(header) + sum(len(x) + 1 for x in o) + sum(len(x) + 1 for x in r)

        if budget_chars:
            # Reserve room for the section headers AND for the truncation
            # disclosure this pruning is about to add. Without the reservation,
            # dropping lines can make the output LONGER than the budget, because
            # the "N omitted for length" and "may not be exhaustive" text costs
            # more than the lines it replaced.
            usable = budget_chars - _SERIALISATION_OVERHEAD
            while rel_lines and total(obj_lines, rel_lines) > usable:
                rel_lines.pop()
                dropped_rel += 1
            while len(obj_lines) > 1 and total(obj_lines, rel_lines) > usable:
                obj_lines.pop()
                dropped_obj += 1
            if total(obj_lines, rel_lines) > usable:
                # The header plus one object already exceeds the budget. Say so
                # rather than silently returning something over budget.
                LOG.debug(
                    "Scene graph minimum representation (%d chars) exceeds the "
                    "%d-char budget; emitting it anyway.",
                    total(obj_lines, rel_lines) + _SERIALISATION_OVERHEAD, budget_chars)

        blocks = [header]
        if include_objects:
            blocks.append("\nDETECTED OBJECTS ({} listed{}):".format(
                len(obj_lines), ", {} omitted for length".format(dropped_obj) if dropped_obj else ""))
            blocks.extend(obj_lines if obj_lines else ["(none detected)"])
        if include_relations:
            blocks.append("\nSPATIAL RELATIONS ({} listed{}):".format(
                len(rel_lines), ", {} omitted for length".format(dropped_rel) if dropped_rel else ""))
            blocks.extend(rel_lines if rel_lines else ["(no relations established)"])
        if dropped_obj or dropped_rel:
            blocks.append("\nNote: this list is truncated and may not be exhaustive.")
        if self.notes:
            blocks.append("\nNotes: " + " ".join(self.notes))
        return "\n".join(blocks)

    def _reorder_by_relevance(
        self, obj_lines: List[str], rel_lines: List[str],
        keywords: Sequence[str],
    ) -> Tuple[List[str], List[str]]:
        """Stable partition putting keyword-matching lines first.

        Only reorders; never drops. Pruning stays the caller's decision so the
        two effects remain separable.
        """
        keys = [label_key(k) for k in keywords if str(k).strip()]

        def hit(line: str) -> int:
            low = line.lower()
            return 1 if any(k and k in low for k in keys) else 0

        objs = sorted(range(len(obj_lines)), key=lambda i: (-hit(obj_lines[i]), i))
        rels = sorted(range(len(rel_lines)), key=lambda i: (-hit(rel_lines[i]), i))
        return [obj_lines[i] for i in objs], [rel_lines[i] for i in rels]

    def to_dict(self, include_relations: bool = True) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "image_size": list(self.image_size),
            "image_index": self.image_index,
            "coord_scale": self.coord_scale,
            "objects": [o.to_dict() for o in self.objects],
            "stats": self.stats(),
        }
        if include_relations:
            d["relations"] = [r.to_dict() for r in self.relations]
        if self.notes:
            d["notes"] = list(self.notes)
        return d

    def to_networkx(self):
        """Optional: a networkx DiGraph, for graph-level analysis in the notebook."""
        try:
            import networkx as nx
        except ImportError:
            LOG.warning("networkx is not installed; to_networkx() unavailable.")
            return None
        g = nx.DiGraph()
        for i, o in enumerate(self.objects):
            oid = o.obj_id if o.obj_id is not None else i
            g.add_node(oid, label=o.label, bbox=o.bbox_global, score=o.score,
                       tiles=list(o.merged_from or []))
        for r in self.relations:
            g.add_edge(r.subject, r.object, **r.to_dict())
        return g


def merge_graphs(graphs: Sequence[SceneGraph]) -> SceneGraph:
    """Concatenate per-image graphs for a multi-image (bi-temporal) sample.

    Object ids are re-based per image and prefixed in the label so the model can
    tell the two acquisitions apart. Relations are NOT created across images:
    a "relation" between two time points is a change, not a spatial relation, and
    conflating them would misrepresent the method.
    """
    if not graphs:
        return SceneGraph()
    if len(graphs) == 1:
        return graphs[0]

    out = SceneGraph(image_size=graphs[0].image_size, coord_scale=graphs[0].coord_scale)
    offset = 0
    for gi, g in enumerate(graphs):
        remap: Dict[int, int] = {}
        for i, o in enumerate(g.objects):
            old = o.obj_id if o.obj_id is not None else i
            new = offset + i
            remap[old] = new
            out.objects.append(DetectedObject(
                label="[img{}] {}".format(gi + 1, o.label),
                bbox_global=o.bbox_global,
                score=o.score,
                tile_id=o.tile_id,
                attributes=dict(o.attributes or {}, image_index=gi),
                obj_id=new,
                merged_from=list(o.merged_from or []),
            ))
        for r in g.relations:
            if r.subject in remap and r.object in remap:
                nr = Relation(**{**vars(r), "subject": remap[r.subject],
                                 "object": remap[r.object]})
                out.relations.append(nr)
        offset += len(g.objects)
    out.notes.append("Objects from {} separate acquisitions; the [imgN] prefix "
                     "gives the acquisition. Relations are within one acquisition only."
                     .format(len(graphs)))
    return out
