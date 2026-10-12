"""Pipeline base class and shared machinery.

Every arm subclasses `Pipeline` and implements `_answer`. The base class owns the
parts that MUST be identical across arms:

  * opening the image and planning tiles,
  * the answer-format contract and the scoring call,
  * compute accounting,
  * error isolation, so one bad sample degrades to a recorded failure rather than
    killing the run.

Keeping these in one place is what makes the comparison a comparison.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..data.schema import Prediction, Sample
from ..eval.metrics import score_sample
from ..tiling.tiler import TiledImage
from ..utils.compute import ComputeMeter, reset_peak_vram
from ..utils.errors import ErrorCollector, RetryConfig, retry_call, stage
from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.pipelines")


class Pipeline:
    """Abstract arm of the experiment."""

    name = "abstract"
    #: Set on subclasses that consume the relation representation, so the
    #: manifest can state unambiguously which arm produced a results file.
    uses_relations = False

    def __init__(self, cfg: Dict[str, Any], backend: Any,
                 scorer: Any = None, proposer: Any = None) -> None:
        self.cfg = cfg or {}
        self.backend = backend
        self.scorer = scorer
        self.proposer = proposer

        tcfg = self.cfg.get("tiling", {}) or {}
        self.tile_size = int(tcfg.get("tile_size", 1024))
        self.overlap = int(tcfg.get("overlap", 128))
        self.max_tiles = tcfg.get("max_tiles")
        self.overview_side = int(tcfg.get("overview_side", 1024))

        gcfg = self.cfg.get("generation", {}) or {}
        self.max_new_tokens = int(gcfg.get("max_new_tokens", 256))
        self.caption_max_new_tokens = int(gcfg.get("caption_max_new_tokens", 512))
        self.retry = RetryConfig(
            attempts=int(gcfg.get("retry_attempts", 3)),
            base_delay=float(gcfg.get("retry_base_delay", 2.0)),
        )

        ecfg = self.cfg.get("eval", {}) or {}
        self.iou_thresholds = tuple(ecfg.get("iou_thresholds", (0.5, 0.7)))
        self.primary_iou = float(ecfg.get("primary_iou", 0.5))

    # -- helpers ------------------------------------------------------------
    def tokens_for(self, sample: Sample) -> int:
        """Generation length by task family; captions need far more room."""
        return (self.caption_max_new_tokens
                if str(sample.family).startswith("caption") else self.max_new_tokens)

    def open_image(self, path: str, image_index: int = 0) -> TiledImage:
        return TiledImage(
            path, tile_size=self.tile_size, overlap=self.overlap,
            image_index=image_index, max_tiles=self.max_tiles,
        )

    def call_vlm(self, prompt: str, images: Sequence[Any], sample: Sample,
                 meter: ComputeMeter, collector: ErrorCollector,
                 stage_name: str = "answer",
                 max_new_tokens: Optional[int] = None) -> Optional[Any]:
        """One accounted, retried VLM call. Returns None on total failure."""
        try:
            resp = retry_call(
                self.backend.generate,
                prompt,
                images=list(images),
                max_new_tokens=max_new_tokens or self.tokens_for(sample),
                retry=self.retry,
                stage_name=stage_name,
                collector=collector,
            )
        except Exception as exc:
            meter.record_call(failed=True)
            LOG.error("[%s] %s failed for %s: %s", self.name, stage_name, sample.uid, exc)
            return None
        meter.record_call(resp.prompt_tokens, resp.completion_tokens,
                          resp.n_images, resp.pixels)
        return resp

    # -- template method ---------------------------------------------------
    def run_sample(self, sample: Sample) -> Prediction:
        """Answer one sample and score it. Never raises."""
        reset_peak_vram()
        meter = ComputeMeter()
        collector = ErrorCollector()

        pred = Prediction(
            uid=sample.uid, pipeline=self.name,
            category=sample.category, task=sample.task, l2=sample.l2,
            family=sample.family, rel_group=sample.rel_group(),
        )

        text = ""
        artifacts: Dict[str, Any] = {}
        try:
            text, artifacts = self._answer(sample, meter, collector)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001
            collector.add("run_sample", exc)
            LOG.exception("[%s] unrecoverable failure on %s", self.name, sample.uid)

        pred.raw_text = str(text or "")[:8000]
        pred.artifacts = artifacts or {}
        pred.n_tiles_total = artifacts.get("n_tiles_total") if artifacts else None
        pred.n_tiles_selected = artifacts.get("n_tiles_selected") if artifacts else None
        pred.n_objects = artifacts.get("n_objects") if artifacts else None
        pred.n_relations = artifacts.get("n_relations") if artifacts else None

        # Scoring is isolated too: a malformed ground-truth field must not lose
        # the prediction we just spent GPU time producing.
        with stage("scoring", collector) as box:
            box["value"] = score_sample(
                pred.raw_text, sample,
                thresholds=self.iou_thresholds,
                grounding_iou_primary=self.primary_iou,
            )
        score = box["value"]
        if score is not None:
            pred.parsed = score.parsed
            pred.gt = score.gt
            pred.correct = score.correct
            pred.iou = score.iou
            pred.parse_failed = score.parse_failed
            pred.artifacts["score"] = score.to_dict()
            pred.artifacts["scorable"] = score.scorable
        else:
            pred.artifacts["scorable"] = False

        pred.compute = meter.to_dict()
        pred.errors = collector.to_list()
        # "error" means we produced no answer at all; a degraded-but-answered
        # sample stays "ok" with its errors recorded, so partial failures are
        # visible without being excluded.
        pred.status = "ok" if pred.raw_text.strip() else "error"
        return pred

    def _answer(self, sample: Sample, meter: ComputeMeter,
                collector: ErrorCollector) -> Tuple[str, Dict[str, Any]]:
        raise NotImplementedError

    def describe(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "pipeline": self.name,
            "uses_relations": self.uses_relations,
            "tile_size": self.tile_size,
            "overlap": self.overlap,
            "overview_side": self.overview_side,
            "max_new_tokens": self.max_new_tokens,
            "backend": self.backend.describe() if hasattr(self.backend, "describe") else None,
        }
        if self.scorer is not None and hasattr(self.scorer, "describe"):
            d["scorer"] = self.scorer.describe()
        if self.proposer is not None and hasattr(self.proposer, "describe"):
            d["proposer"] = self.proposer.describe()
        return d
