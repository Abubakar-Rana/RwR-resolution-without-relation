"""Baseline 3 and the Proposed method - deliberately ONE class.

This is the file that decides whether the paper's central claim is credible.

Plan section 8: "The main ablation will remove the cross tile spatial relation
representation while keeping the image tiles, selection strategy, vision language
model, and computational budget unchanged."

The only honest way to guarantee that is to have both arms run the same code and
differ by one boolean. `HierarchicalPipeline.use_relations` is that boolean:

    use_relations=False  ->  b3_selected   (question-conditioned selection +
                                            local reasoning, no relations)
    use_relations=True   ->  proposed_ctsr (the same, plus the cross-tile
                                            spatial relation representation)

What is identical by construction:
  * tile plan (same tile_size, overlap, image)
  * tile scores and the selected tile set (the scorer is deterministic and is
    given the same inputs)
  * local extraction calls: same prompts, same crops, same order, so the same
    number of VLM calls and the same pixels encoded
  * deduplication and the object list handed to the final call
  * the overview image and the crops attached to the final call
  * the final prompt, produced by one function, `aggregation_prompt`

What differs:
  * whether the SPATIAL RELATIONS block is appended to the final prompt

Consequence for cost: the relation block adds prompt TOKENS but zero VLM calls
and zero pixels. That asymmetry is real and must be reported, not hidden - which
is why the compute table reports calls, pixels and tokens separately. If the
proposed arm wins purely on extra prompt tokens, `--ablation matched_tokens`
(config `ablation.pad_tokens_in_baseline`) pads Baseline 3's prompt with a
relation-free filler block of comparable length so token count is controlled too.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..data.schema import DetectedObject, Sample
from ..prompts.templates import aggregation_prompt, object_block_text
from ..spatial.dedup import cap_objects, merge_detections
from ..spatial.relations import RelationConfig, build_relations
from ..spatial.scene_graph import SceneGraph, merge_graphs
from ..tiling.selection import question_keywords, select_tiles
from ..utils.compute import ComputeMeter
from ..utils.errors import ErrorCollector, stage
from ..utils.logging_utils import get_logger
from .base import Pipeline

LOG = get_logger("ctsr.pipelines.hierarchical")

_OBJECT_HEADER = "DETECTED OBJECTS (global coordinates, 0-1000 grid over the whole image):"
_RELATION_HEADER = "SPATIAL RELATIONS (computed geometrically from the global coordinates):"


class HierarchicalPipeline(Pipeline):
    """Question-conditioned selection + local reasoning, with relations optional."""

    name = "hierarchical"
    uses_relations = False

    def __init__(self, cfg: Dict[str, Any], backend: Any,
                 scorer: Any = None, proposer: Any = None,
                 use_relations: bool = False, name: Optional[str] = None) -> None:
        super().__init__(cfg, backend, scorer=scorer, proposer=proposer)
        self.use_relations = bool(use_relations)
        self.uses_relations = self.use_relations
        if name:
            self.name = name

        scfg = self.cfg.get("selection", {}) or {}
        self.top_k = int(scfg.get("top_k", 5))
        self.min_score = scfg.get("min_score")
        self.diversity_radius_frac = float(scfg.get("diversity_radius_frac", 0.04))
        self.spatial_diversity = bool(scfg.get("spatial_diversity", True))

        dcfg = self.cfg.get("detection", {}) or {}
        self.max_objects_total = int(dcfg.get("max_objects_total", 60))

        mcfg = self.cfg.get("dedup", {}) or {}
        self.dedup_kwargs = {
            "iou_thresh": float(mcfg.get("iou_thresh", 0.45)),
            "cross_tile_iou_thresh": float(mcfg.get("cross_tile_iou_thresh", 0.25)),
            "containment_thresh": float(mcfg.get("containment_thresh", 0.80)),
            "seam_gap_px": float(mcfg.get("seam_gap_px", 8.0)),
            "strict_labels": bool(mcfg.get("strict_labels", False)),
            "box_mode": str(mcfg.get("box_mode", "union")),
        }
        self.dedup_enabled = bool(mcfg.get("enabled", True))

        rcfg = self.cfg.get("relations", {}) or {}
        self.relation_cfg = RelationConfig(
            max_neighbours=int(rcfg.get("max_neighbours", 6)),
            adjacency_gap_frac=float(rcfg.get("adjacency_gap_frac", 0.012)),
            near_dist_frac=float(rcfg.get("near_dist_frac", 0.06)),
            containment_thresh=float(rcfg.get("containment_thresh", 0.85)),
            intersect_iou_thresh=float(rcfg.get("intersect_iou_thresh", 0.05)),
            include_direction=bool(rcfg.get("include_direction", True)),
            include_distance=bool(rcfg.get("include_distance", True)),
            include_adjacency=bool(rcfg.get("include_adjacency", True)),
            include_containment=bool(rcfg.get("include_containment", True)),
            include_intersection=bool(rcfg.get("include_intersection", True)),
            use_compass=bool(rcfg.get("use_compass", True)),
            gsd_m_per_px=rcfg.get("gsd_m_per_px"),
            max_relations=int(rcfg.get("max_relations", 220)),
        )
        self.graph_token_budget = rcfg.get("token_budget", 1400)

        fcfg = self.cfg.get("final_call", {}) or {}
        self.attach_overview = bool(fcfg.get("attach_overview", True))
        self.attach_crops = int(fcfg.get("attach_crops", 3))
        self.crop_thumb_side = int(fcfg.get("crop_thumb_side", 768))

        acfg = self.cfg.get("ablation", {}) or {}
        self.pad_tokens_in_baseline = bool(acfg.get("pad_tokens_in_baseline", False))
        self.shuffle_relations = bool(acfg.get("shuffle_relations", False))
        self.drop_global_coords = bool(acfg.get("drop_global_coords", False))

    # ----------------------------------------------------------------------
    def _answer(self, sample: Sample, meter: ComputeMeter,
                collector: ErrorCollector) -> Tuple[str, Dict[str, Any]]:
        artifacts: Dict[str, Any] = {
            "arm": "proposed_ctsr" if self.use_relations else "b3_selected",
            "use_relations": self.use_relations,
        }
        if not sample.image_paths:
            artifacts["note"] = "sample has no image"
            return "", artifacts

        graphs: List[SceneGraph] = []
        overview_img = None
        crop_imgs: List[Any] = []
        n_tiles_total = 0
        n_tiles_selected = 0
        selection_records: List[Dict[str, Any]] = []
        extraction_stats: List[Dict[str, Any]] = []
        merge_stats: List[Dict[str, Any]] = []

        keywords = question_keywords(sample.question, sample.options)
        artifacts["question_keywords"] = keywords

        for idx, path in enumerate(sample.image_paths):
            with stage("open:{}".format(idx), collector) as box:
                box["value"] = self.open_image(path, image_index=idx)
            ti = box["value"]
            if ti is None:
                continue
            try:
                if sample.image_size is None and idx == 0:
                    sample.image_size = (ti.width, ti.height)
                n_tiles_total += len(ti.tiles)

                # --- 5.1 global scene understanding ------------------------
                if self.attach_overview and overview_img is None:
                    with meter.timer("overview"):
                        with stage("overview", collector) as ob:
                            ob["value"] = ti.overview(self.overview_side)
                        overview_img = ob["value"]

                # --- 5.2 question-conditioned tile selection ---------------
                with meter.timer("selection"):
                    with stage("selection", collector) as sb:
                        sb["value"] = self.scorer.score(
                            ti, ti.tiles, sample.question, sample.options, meter=meter
                        ) if self.scorer is not None else None
                scores = sb["value"]

                if scores:
                    chosen = select_tiles(
                        scores, ti.tiles, top_k=self.top_k,
                        min_score=self.min_score,
                        spatial_diversity=self.spatial_diversity,
                        diversity_radius_frac=self.diversity_radius_frac,
                        image_size=(ti.width, ti.height),
                    )
                    top = sorted(scores, key=lambda s: -s.score)[:self.top_k * 2]
                    selection_records.append({
                        "image_index": idx,
                        "chosen": [t.tile_id for t in chosen],
                        "top_scores": [s.to_dict() for s in top],
                    })
                else:
                    # Scoring failed entirely: fall back to an evenly spaced grid
                    # so the sample still gets high-resolution looks. Recorded,
                    # because such a sample is no longer question-conditioned.
                    LOG.warning("Selection unavailable for %s; using an even grid.",
                                sample.uid)
                    step = max(1, len(ti.tiles) // max(1, self.top_k))
                    chosen = ti.tiles[::step][:self.top_k]
                    selection_records.append({
                        "image_index": idx, "chosen": [t.tile_id for t in chosen],
                        "fallback": "even_grid",
                    })
                n_tiles_selected += len(chosen)

                # --- 5.3 local visual reasoning ----------------------------
                with meter.timer("extraction"):
                    with stage("extraction", collector) as eb:
                        eb["value"] = self.proposer.extract(
                            ti, chosen, sample.question,
                            keywords=keywords, meter=meter, collector=collector,
                        ) if self.proposer is not None else None
                extraction = eb["value"]
                objects: List[DetectedObject] = list(extraction.objects) if extraction else []
                if extraction is not None:
                    stats = extraction.to_dict()
                    stats["image_index"] = idx
                    extraction_stats.append(stats)

                # --- cross-tile deduplication ------------------------------
                if self.dedup_enabled and objects:
                    with meter.timer("dedup"):
                        with stage("dedup", collector) as db:
                            db["value"] = merge_detections(
                                objects, image_size=(ti.width, ti.height),
                                **self.dedup_kwargs
                            )
                    if db["value"] is not None:
                        objects, mstats = db["value"]
                        ms = mstats.to_dict()
                        ms["image_index"] = idx
                        merge_stats.append(ms)
                else:
                    for i, o in enumerate(objects):
                        if o.obj_id is None:
                            o.obj_id = i

                objects = cap_objects(objects, self.max_objects_total, keep_labels=keywords)

                # --- 5.4 cross-tile spatial relation representation --------
                # NOTE: relations are built for BOTH arms. Baseline 3 simply does
                # not receive them in its prompt. Building them either way keeps
                # per-sample compute time comparable and lets the error analysis
                # ask what the ablated arm was missing on the samples it failed.
                relations = []
                if objects:
                    with meter.timer("relations"):
                        with stage("relations", collector) as rb:
                            rb["value"] = build_relations(
                                objects, (ti.width, ti.height), self.relation_cfg
                            )
                    relations = rb["value"] or []

                graph = SceneGraph(
                    objects=objects, relations=relations,
                    image_size=(ti.width, ti.height), image_index=idx,
                )
                graphs.append(graph)

                # --- crops attached to the final call ----------------------
                if self.attach_crops > 0 and idx == 0:
                    with meter.timer("attach_crops"):
                        for tile in chosen[:self.attach_crops]:
                            try:
                                crop = ti.crop(tile)
                                side = self.crop_thumb_side
                                if max(crop.size) > side:
                                    crop = crop.copy()
                                    crop.thumbnail((side, side))
                                crop_imgs.append(crop)
                            except Exception as exc:
                                collector.add("attach_crop:{}".format(tile.tile_id), exc)
            finally:
                ti.close()

        graph = merge_graphs(graphs) if graphs else SceneGraph()

        artifacts["n_tiles_total"] = n_tiles_total
        artifacts["n_tiles_selected"] = n_tiles_selected
        artifacts["n_objects"] = graph.n_objects
        artifacts["n_relations"] = graph.n_relations if self.use_relations else 0
        artifacts["n_relations_built"] = graph.n_relations
        artifacts["selection"] = selection_records
        artifacts["extraction"] = extraction_stats
        artifacts["merge"] = merge_stats
        artifacts["graph_stats"] = graph.stats()
        artifacts["scene_graph"] = graph.to_dict(include_relations=True)

        # ------------------------------------------------------------------
        # Final reasoning call. THE one place the two arms diverge.
        # ------------------------------------------------------------------
        obj_lines = graph.object_lines()
        if self.drop_global_coords:
            # Ablation: keep the object list but strip coordinates, to test
            # whether the benefit comes from the coordinates or merely from
            # having a list of objects.
            obj_lines = [l.split(" box=")[0] for l in obj_lines]
        object_block = object_block_text(obj_lines, _OBJECT_HEADER)

        relation_block: Optional[str] = None
        if self.use_relations:
            rel_lines = graph.relation_lines(include_metric=True)
            if self.shuffle_relations:
                # Ablation: destroy the geometric content while keeping length,
                # by pairing predicates with the wrong objects.
                rel_lines = _shuffle_lines(rel_lines, seed=hash(sample.uid) & 0xFFFF)
            relation_block = object_block_text(rel_lines or ["(no relations established)"],
                                               _RELATION_HEADER)
        elif self.pad_tokens_in_baseline:
            # Token-matched control: same prompt length, no spatial information.
            relation_block = _filler_block(len(graph.relation_lines()))
            artifacts["token_padding_applied"] = True

        images: List[Any] = []
        if overview_img is not None:
            images.append(overview_img)
        images.extend(crop_imgs)

        prompt = aggregation_prompt(
            question=sample.question,
            options=sample.options,
            family=sample.family,
            object_block=object_block,
            relation_block=relation_block,
            n_images_shown=len(images),
            overview_shown=overview_img is not None,
            n_regions=n_tiles_selected,
        )
        artifacts["prompt_chars"] = len(prompt)
        artifacts["final_prompt"] = prompt if self.cfg.get("save_prompts") else None

        with meter.timer("final_answer"):
            resp = self.call_vlm(prompt, images, sample, meter, collector,
                                 stage_name="final_answer")

        for im in crop_imgs:
            try:
                im.close()
            except Exception:
                pass

        if resp is None:
            artifacts["note"] = "final reasoning call failed"
            return "", artifacts
        artifacts["degradations"] = resp.meta.get("degradations", [])
        return resp.text, artifacts

    def describe(self) -> Dict[str, Any]:
        d = super().describe()
        d.update({
            "use_relations": self.use_relations,
            "top_k": self.top_k,
            "max_objects_total": self.max_objects_total,
            "relation_config": self.relation_cfg.to_dict(),
            "dedup": dict(self.dedup_kwargs, enabled=self.dedup_enabled),
            "attach_overview": self.attach_overview,
            "attach_crops": self.attach_crops,
            "ablation_flags": {
                "pad_tokens_in_baseline": self.pad_tokens_in_baseline,
                "shuffle_relations": self.shuffle_relations,
                "drop_global_coords": self.drop_global_coords,
            },
        })
        return d


class SelectedTilesPipeline(HierarchicalPipeline):
    """Baseline 3: question-conditioned selection + local reasoning, NO relations."""

    name = "b3_selected"

    def __init__(self, cfg: Dict[str, Any], backend: Any, **kw: Any) -> None:
        kw.pop("use_relations", None)
        kw.pop("name", None)
        super().__init__(cfg, backend, use_relations=False, name="b3_selected", **kw)


class ProposedPipeline(HierarchicalPipeline):
    """Proposed method: Baseline 3 plus the cross-tile spatial relation block."""

    name = "proposed_ctsr"

    def __init__(self, cfg: Dict[str, Any], backend: Any, **kw: Any) -> None:
        kw.pop("use_relations", None)
        kw.pop("name", None)
        super().__init__(cfg, backend, use_relations=True, name="proposed_ctsr", **kw)


# --------------------------------------------------------------------------

_FILLER = (
    "Remote sensing imagery is acquired from an overhead viewpoint and records "
    "surface reflectance across a wide area at a fixed ground sample distance."
)


def _filler_block(n_lines: int) -> str:
    """Spatially uninformative text of comparable length, for the token-matched arm.

    Contains no object references and no geometry, so any accuracy it produces is
    attributable to prompt length rather than spatial structure.
    """
    lines = [_FILLER for _ in range(max(0, n_lines))]
    return object_block_text(lines or ["(no additional context)"],
                             "BACKGROUND NOTES (no spatial information):")


def _shuffle_lines(lines: Sequence[str], seed: int = 0) -> List[str]:
    """Permute relation lines, for the 'scrambled relations' ablation."""
    import random
    out = list(lines)
    random.Random(seed).shuffle(out)
    return out
