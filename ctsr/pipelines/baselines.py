"""Baselines 1 and 2.

Baseline 1 - Direct inference.
    The whole image goes to the VLM in one call. Because the visual encoder has a
    pixel budget, this is in effect "resize the scene and hope the target survives".
    This is the arm the plan's background section describes as losing fine-grained
    information, and it is XLRS-Bench's own evaluation protocol.

Baseline 2 - Independent tiling.
    Overlapping tiles, each answered in isolation, then a text-only reconciliation
    call. This recovers detail but by construction cannot represent a relation
    between objects in different tiles: each tile answer is produced without
    knowledge of the others. It is the control that isolates the value of
    *structure* from the value of *resolution*.

Baseline 2 is the expensive arm (one call per tile), so `max_answer_tiles` caps
it. The cap is recorded in the results; when comparing costs, note that a capped
Baseline 2 is not "all tiles".
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..data.schema import Sample
from ..prompts.templates import direct_prompt, tile_answer_prompt, tile_vote_prompt
from ..tiling.selection import question_keywords, select_tiles
from ..tiling.tiler import resize_to_budget
from ..utils.compute import ComputeMeter
from ..utils.errors import ErrorCollector, stage
from ..utils.logging_utils import get_logger
from .base import Pipeline

LOG = get_logger("ctsr.pipelines.baselines")


class DirectPipeline(Pipeline):
    """Baseline 1: the full image (downscaled by the encoder) in one call."""

    name = "b1_direct"
    uses_relations = False

    def __init__(self, cfg: Dict[str, Any], backend: Any, **kw: Any) -> None:
        super().__init__(cfg, backend, **kw)
        bcfg = (self.cfg.get("baseline1", {}) or {})
        # When set, the image is pre-resized to this pixel count before being
        # handed over. Leaving it None lets the processor's own max_pixels do the
        # downscaling, which is the faithful "direct inference" condition.
        self.pre_resize_pixels = bcfg.get("pre_resize_pixels")
        self.send_full_resolution = bool(bcfg.get("send_full_resolution", True))

    def _answer(self, sample: Sample, meter: ComputeMeter,
                collector: ErrorCollector) -> Tuple[str, Dict[str, Any]]:
        artifacts: Dict[str, Any] = {"arm": "direct"}
        images: List[Any] = []
        sizes: List[List[int]] = []

        with meter.timer("load_images"):
            for idx, path in enumerate(sample.image_paths):
                with stage("open:{}".format(idx), collector) as box:
                    ti = self.open_image(path, image_index=idx)
                    box["value"] = ti
                ti = box["value"]
                if ti is None:
                    continue
                try:
                    if self.send_full_resolution and not self.pre_resize_pixels:
                        # Hand over the whole image and let the processor resize;
                        # this is what "direct" means in the benchmark protocol.
                        from PIL import Image
                        img = Image.open(path)
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                    else:
                        img = ti.overview(max(self.overview_side, 1024))
                        if self.pre_resize_pixels:
                            img = resize_to_budget(img, int(self.pre_resize_pixels))
                    images.append(img)
                    sizes.append([ti.width, ti.height])
                    if sample.image_size is None and idx == 0:
                        sample.image_size = (ti.width, ti.height)
                finally:
                    ti.close()

        if not images:
            artifacts["note"] = "no image could be opened"
            return "", artifacts

        artifacts["image_sizes"] = sizes
        artifacts["n_images_sent"] = len(images)

        prompt = direct_prompt(sample.question, sample.options, sample.family,
                               n_images=len(images))
        artifacts["prompt_chars"] = len(prompt)

        with meter.timer("vlm_answer"):
            resp = self.call_vlm(prompt, images, sample, meter, collector,
                                 stage_name="direct_answer")
        if resp is None:
            return "", artifacts
        artifacts["degradations"] = resp.meta.get("degradations", [])
        return resp.text, artifacts


class TilingPipeline(Pipeline):
    """Baseline 2: answer each tile independently, then reconcile."""

    name = "b2_tiling"
    uses_relations = False

    def __init__(self, cfg: Dict[str, Any], backend: Any, **kw: Any) -> None:
        super().__init__(cfg, backend, **kw)
        bcfg = (self.cfg.get("baseline2", {}) or {})
        self.max_answer_tiles = int(bcfg.get("max_answer_tiles", 8))
        self.include_overview_in_vote = bool(bcfg.get("include_overview_in_vote", False))
        # Selection strategy for which tiles get answered when capped.
        # "grid" = evenly spaced over the tile plan (question-independent, which
        # keeps this arm a genuine "no question conditioning" control).
        self.tile_choice = str(bcfg.get("tile_choice", "grid"))

    def _pick_tiles(self, tiles: Sequence[Any]) -> List[Any]:
        n = len(tiles)
        k = min(self.max_answer_tiles, n)
        if k >= n:
            return list(tiles)
        if self.tile_choice == "first":
            return list(tiles[:k])
        # Evenly spaced across the plan so coverage is spread over the scene.
        step = n / float(k)
        idxs = sorted({min(n - 1, int(i * step)) for i in range(k)})
        return [tiles[i] for i in idxs]

    def _answer(self, sample: Sample, meter: ComputeMeter,
                collector: ErrorCollector) -> Tuple[str, Dict[str, Any]]:
        artifacts: Dict[str, Any] = {"arm": "independent_tiling"}
        if not sample.image_paths:
            return "", artifacts

        tile_answers: List[str] = []
        tile_records: List[Dict[str, Any]] = []
        n_total = 0
        overview = None

        for idx, path in enumerate(sample.image_paths):
            with stage("open:{}".format(idx), collector) as box:
                box["value"] = self.open_image(path, image_index=idx)
            ti = box["value"]
            if ti is None:
                continue
            try:
                if sample.image_size is None and idx == 0:
                    sample.image_size = (ti.width, ti.height)
                n_total += len(ti.tiles)
                chosen = self._pick_tiles(ti.tiles)
                if overview is None and self.include_overview_in_vote:
                    with meter.timer("overview"):
                        overview = ti.overview(self.overview_side)

                with meter.timer("tile_answers"):
                    for t_i, tile in enumerate(chosen):
                        try:
                            crop = ti.crop(tile)
                        except Exception as exc:
                            collector.add("crop:tile{}".format(tile.tile_id), exc)
                            continue
                        prompt = tile_answer_prompt(
                            sample.question, sample.options, sample.family,
                            tile_index=t_i, n_tiles=len(chosen),
                            tile_box=None,  # withheld on purpose: independent tiles
                        )
                        resp = self.call_vlm(prompt, [crop], sample, meter, collector,
                                             stage_name="tile_answer:{}".format(tile.tile_id))
                        try:
                            crop.close()
                        except Exception:
                            pass
                        if resp is None:
                            continue
                        tile_answers.append(resp.text)
                        tile_records.append({
                            "tile_id": tile.tile_id, "box": list(tile.box),
                            "answer": resp.text[:400],
                        })
            finally:
                ti.close()

        artifacts["n_tiles_total"] = n_total
        artifacts["n_tiles_selected"] = len(tile_records)
        artifacts["tile_answers"] = tile_records
        artifacts["max_answer_tiles"] = self.max_answer_tiles

        if not tile_answers:
            artifacts["note"] = "no tile produced an answer"
            return "", artifacts

        # Reconciliation. Text-only by default, which is the faithful version of
        # "aggregate independent tile answers".
        prompt = tile_vote_prompt(sample.question, sample.options,
                                  sample.family, tile_answers)
        images = [overview] if (overview is not None) else []
        with meter.timer("vote"):
            resp = self.call_vlm(prompt, images, sample, meter, collector,
                                 stage_name="tile_vote")
        if resp is None:
            # Degrade to the most common tile answer rather than losing the sample.
            artifacts["note"] = "reconciliation call failed; fell back to tile plurality"
            return _plurality(tile_answers), artifacts
        return resp.text, artifacts


def _plurality(answers: Sequence[str]) -> str:
    """Most frequent non-UNKNOWN tile answer, as a fallback aggregator."""
    from collections import Counter

    cleaned = [str(a).strip() for a in answers
               if str(a).strip() and "unknown" not in str(a).lower()]
    if not cleaned:
        return str(answers[0]) if answers else ""
    return Counter(cleaned).most_common(1)[0][0]
