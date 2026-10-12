"""Question-conditioned tile selection (plan section 5.2).

Three scorers are provided, and they compose:

  SaliencyScorer  - question-agnostic. Pure numpy edge/variance energy on the
                    overview. Cheap, and a useful control: it isolates "looked
                    at busy regions" from "looked at question-relevant regions".
  ClipScorer      - question-conditioned. Cosine similarity between the CLIP text
                    embedding of the question and the CLIP image embedding of each
                    tile thumbnail. Uses the standard transformers CLIP API, and a
                    remote-sensing CLIP checkpoint can be dropped in via config.
  VLMScorer       - question-conditioned, strongest but most expensive: asks the
                    VLM itself to rate each tile thumbnail 0-10 for relevance.
                    Its VLM calls are counted in the compute budget.

HybridScorer is the default: a weighted sum of normalised saliency and CLIP
scores, which keeps the selection question-aware without adding VLM calls.

IMPORTANT for the ablation: tile selection is shared by Baseline 3 and the
proposed method. They must select the *same* tiles for the same sample, so the
scorer is deterministic and selection is a pure function of
(image, question, config). Do not make it depend on run order.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..utils.errors import ErrorCollector, stage
from ..utils.logging_utils import get_logger
from .tiler import TileSpec, TiledImage

LOG = get_logger("ctsr.tiling.selection")

_STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "to", "and", "or", "is", "are",
    "was", "were", "how", "many", "what", "which", "where", "this", "that",
    "there", "image", "images", "picture", "photo", "following", "based",
    "please", "answer", "question", "options", "option", "you", "your", "it",
    "for", "from", "with", "by", "be", "can", "does", "do", "any", "most",
}


@dataclass
class TileScore:
    tile_id: int
    score: float
    components: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tile_id": self.tile_id,
            "score": round(float(self.score), 5),
            "components": {k: round(float(v), 5) for k, v in self.components.items()},
        }


def question_keywords(question: str, options: Optional[Sequence[str]] = None,
                      max_terms: int = 12) -> List[str]:
    """Content words from the question (and options), for text-side conditioning."""
    text = str(question or "")
    if options:
        text += " " + " ".join(str(o) for o in options)
    words = re.findall(r"[A-Za-z][A-Za-z\-]{2,}", text.lower())
    out: List[str] = []
    for w in words:
        if w in _STOPWORDS or w in out:
            continue
        out.append(w)
        if len(out) >= max_terms:
            break
    return out


def _minmax(values: Sequence[float]) -> List[float]:
    """Scale to [0,1]; a constant vector maps to all-0.5 (no information)."""
    if not values:
        return []
    lo, hi = min(values), max(values)
    if not math.isfinite(lo) or not math.isfinite(hi) or hi - lo < 1e-12:
        return [0.5] * len(values)
    return [(v - lo) / (hi - lo) for v in values]


class TileScorer:
    name = "abstract"
    uses_vlm = False

    def score(self, ti: TiledImage, tiles: Sequence[TileSpec], question: str,
              options: Optional[Sequence[str]] = None,
              meter: Any = None) -> List[TileScore]:
        raise NotImplementedError

    def describe(self) -> Dict[str, Any]:
        return {"scorer": self.name}


class SaliencyScorer(TileScorer):
    """Question-agnostic visual energy, computed on the overview.

    Reading tile statistics from the downsampled overview instead of full-res
    crops is what makes this affordable: one decode per image rather than one per
    tile. Score = w_edge * mean |gradient| + w_var * pixel std.
    """

    name = "saliency"

    def __init__(self, overview_side: int = 1024, w_edge: float = 0.7,
                 w_var: float = 0.3) -> None:
        self.overview_side = int(overview_side)
        self.w_edge = float(w_edge)
        self.w_var = float(w_var)

    def score(self, ti: TiledImage, tiles: Sequence[TileSpec], question: str,
              options: Optional[Sequence[str]] = None,
              meter: Any = None) -> List[TileScore]:
        import numpy as np

        ov = ti.overview(self.overview_side)
        gray = np.asarray(ov.convert("L"), dtype=np.float32) / 255.0
        oh, ow = gray.shape[:2]
        sx = ow / float(ti.width)
        sy = oh / float(ti.height)

        gy, gx = np.gradient(gray)
        grad = np.abs(gx) + np.abs(gy)

        edges: List[float] = []
        variances: List[float] = []
        for t in tiles:
            x0 = max(0, min(ow - 1, int(t.x0 * sx)))
            x1 = max(x0 + 1, min(ow, int(math.ceil(t.x1 * sx))))
            y0 = max(0, min(oh - 1, int(t.y0 * sy)))
            y1 = max(y0 + 1, min(oh, int(math.ceil(t.y1 * sy))))
            patch_g = grad[y0:y1, x0:x1]
            patch_i = gray[y0:y1, x0:x1]
            edges.append(float(patch_g.mean()) if patch_g.size else 0.0)
            variances.append(float(patch_i.std()) if patch_i.size else 0.0)

        ne, nv = _minmax(edges), _minmax(variances)
        return [
            TileScore(
                tile_id=t.tile_id,
                score=self.w_edge * ne[i] + self.w_var * nv[i],
                components={"edge": ne[i], "var": nv[i]},
            )
            for i, t in enumerate(tiles)
        ]

    def describe(self) -> Dict[str, Any]:
        return {"scorer": self.name, "overview_side": self.overview_side,
                "w_edge": self.w_edge, "w_var": self.w_var}


class ClipScorer(TileScorer):
    """Question-conditioned CLIP similarity over tile thumbnails.

    Defaults to `openai/clip-vit-base-patch32` via transformers. For remote
    sensing, a domain checkpoint usually helps; set `model_id` to one that
    exposes the same CLIPModel interface. If the model cannot be loaded, `score`
    raises and the caller falls back to saliency-only (recorded as a stage error
    rather than silently changing the method).
    """

    name = "clip"

    def __init__(
        self,
        model_id: str = "openai/clip-vit-base-patch32",
        device: Optional[str] = None,
        thumb_size: int = 224,
        batch_size: int = 32,
        prompt_template: str = "a satellite image showing {}",
    ) -> None:
        self.model_id = model_id
        self.device = device
        self.thumb_size = int(thumb_size)
        self.batch_size = int(batch_size)
        self.prompt_template = prompt_template
        self._model = None
        self._processor = None

    def load(self) -> "ClipScorer":
        if self._model is not None:
            return self
        import torch
        from transformers import AutoProcessor, CLIPModel

        if self.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        LOG.info("Loading CLIP scorer %s on %s", self.model_id, self.device)
        self._model = CLIPModel.from_pretrained(self.model_id).to(self.device).eval()
        self._processor = AutoProcessor.from_pretrained(self.model_id)
        return self

    def unload(self) -> None:
        self._model = None
        self._processor = None

    def _text_queries(self, question: str, options: Optional[Sequence[str]]) -> List[str]:
        kws = question_keywords(question, options, max_terms=8)
        queries = [str(question).strip()[:300]] if question else []
        queries += [self.prompt_template.format(k) for k in kws[:6]]
        return queries or ["a satellite image"]

    def score(self, ti: TiledImage, tiles: Sequence[TileSpec], question: str,
              options: Optional[Sequence[str]] = None,
              meter: Any = None) -> List[TileScore]:
        import torch

        self.load()
        queries = self._text_queries(question, options)

        # Thumbnails are cut from the overview, not from full-res crops: CLIP
        # sees 224px anyway, so a full-res decode per tile would be wasted work.
        ov = ti.overview(max(self.thumb_size * 4, 1024))
        ow, oh = ov.size
        sx, sy = ow / float(ti.width), oh / float(ti.height)
        thumbs = []
        for t in tiles:
            x0 = max(0, min(ow - 1, int(t.x0 * sx)))
            x1 = max(x0 + 1, min(ow, int(math.ceil(t.x1 * sx))))
            y0 = max(0, min(oh - 1, int(t.y0 * sy)))
            y1 = max(y0 + 1, min(oh, int(math.ceil(t.y1 * sy))))
            thumbs.append(ov.crop((x0, y0, x1, y1)).resize(
                (self.thumb_size, self.thumb_size)))

        with torch.inference_mode():
            tin = self._processor(text=queries, return_tensors="pt",
                                  padding=True, truncation=True).to(self.device)
            tfeat = self._model.get_text_features(**tin)
            tfeat = tfeat / tfeat.norm(dim=-1, keepdim=True).clamp_min(1e-8)

            sims: List[float] = []
            for i in range(0, len(thumbs), self.batch_size):
                batch = thumbs[i:i + self.batch_size]
                iin = self._processor(images=batch, return_tensors="pt").to(self.device)
                ifeat = self._model.get_image_features(**iin)
                ifeat = ifeat / ifeat.norm(dim=-1, keepdim=True).clamp_min(1e-8)
                # Max over query phrasings: one strong match is enough.
                sim = (ifeat @ tfeat.T).max(dim=-1).values
                sims.extend(sim.float().cpu().tolist())

        norm = _minmax(sims)
        return [
            TileScore(tile_id=t.tile_id, score=norm[i],
                      components={"clip_raw": sims[i], "clip": norm[i]})
            for i, t in enumerate(tiles)
        ]

    def describe(self) -> Dict[str, Any]:
        return {"scorer": self.name, "model_id": self.model_id,
                "thumb_size": self.thumb_size}


class VLMScorer(TileScorer):
    """Ask the VLM to rate each tile 0-10 for relevance to the question.

    Accurate but adds one VLM call per scoring batch; those calls are charged to
    the compute meter, so a fair comparison must give the baselines the same
    budget. Off by default for that reason.
    """

    name = "vlm"
    uses_vlm = True

    def __init__(self, backend: Any, batch_tiles: int = 6, thumb_size: int = 336,
                 max_new_tokens: int = 64) -> None:
        self.backend = backend
        self.batch_tiles = max(1, int(batch_tiles))
        self.thumb_size = int(thumb_size)
        self.max_new_tokens = int(max_new_tokens)

    def score(self, ti: TiledImage, tiles: Sequence[TileSpec], question: str,
              options: Optional[Sequence[str]] = None,
              meter: Any = None) -> List[TileScore]:
        from ..prompts.templates import tile_relevance_prompt

        ov = ti.overview(max(self.thumb_size * 4, 1024))
        ow, oh = ov.size
        sx, sy = ow / float(ti.width), oh / float(ti.height)

        raw: Dict[int, float] = {}
        for start in range(0, len(tiles), self.batch_tiles):
            batch = list(tiles[start:start + self.batch_tiles])
            thumbs = []
            for t in batch:
                x0 = max(0, min(ow - 1, int(t.x0 * sx)))
                x1 = max(x0 + 1, min(ow, int(math.ceil(t.x1 * sx))))
                y0 = max(0, min(oh - 1, int(t.y0 * sy)))
                y1 = max(y0 + 1, min(oh, int(math.ceil(t.y1 * sy))))
                thumbs.append(ov.crop((x0, y0, x1, y1)).resize(
                    (self.thumb_size, self.thumb_size)))
            prompt = tile_relevance_prompt(question, len(batch))
            try:
                resp = self.backend.generate(prompt, images=thumbs,
                                             max_new_tokens=self.max_new_tokens)
                if meter is not None:
                    meter.record_call(resp.prompt_tokens, resp.completion_tokens,
                                      resp.n_images, resp.pixels)
                nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", resp.text)]
            except Exception as exc:
                LOG.warning("VLM tile scoring failed for batch at %d: %s", start, exc)
                if meter is not None:
                    meter.record_call(failed=True)
                nums = []
            for i, t in enumerate(batch):
                raw[t.tile_id] = nums[i] if i < len(nums) else 0.0

        vals = [raw.get(t.tile_id, 0.0) for t in tiles]
        norm = _minmax(vals)
        return [
            TileScore(tile_id=t.tile_id, score=norm[i],
                      components={"vlm_raw": vals[i], "vlm": norm[i]})
            for i, t in enumerate(tiles)
        ]

    def describe(self) -> Dict[str, Any]:
        return {"scorer": self.name, "batch_tiles": self.batch_tiles,
                "thumb_size": self.thumb_size}


class HybridScorer(TileScorer):
    """Weighted combination of sub-scorers, with graceful degradation.

    If a component scorer fails (e.g. CLIP weights cannot be downloaded on an
    offline node), its failure is recorded and the remaining components are
    renormalised. The set of components that actually contributed is returned in
    `last_components` so the run manifest can state what was really used.
    """

    name = "hybrid"

    def __init__(self, scorers: Sequence[Tuple[TileScorer, float]]) -> None:
        self.scorers = [(s, float(w)) for s, w in scorers if w != 0]
        self.uses_vlm = any(s.uses_vlm for s, _ in self.scorers)
        self.last_components: List[str] = []

    def score(self, ti: TiledImage, tiles: Sequence[TileSpec], question: str,
              options: Optional[Sequence[str]] = None,
              meter: Any = None) -> List[TileScore]:
        collector = ErrorCollector()
        acc: Dict[int, float] = {t.tile_id: 0.0 for t in tiles}
        comps: Dict[int, Dict[str, float]] = {t.tile_id: {} for t in tiles}
        used_weight = 0.0
        used: List[str] = []

        for scorer, weight in self.scorers:
            with stage("scorer:" + scorer.name, collector) as box:
                box["value"] = scorer.score(ti, tiles, question, options, meter=meter)
            result = box["value"]
            if result is None:
                continue
            used_weight += weight
            used.append(scorer.name)
            for ts in result:
                acc[ts.tile_id] = acc.get(ts.tile_id, 0.0) + weight * ts.score
                comps.setdefault(ts.tile_id, {}).update(ts.components)

        self.last_components = used
        if used_weight <= 0:
            LOG.error("All tile scorers failed; falling back to uniform scores. "
                      "Selection will be position-based, not question-aware.")
            return [TileScore(tile_id=t.tile_id, score=0.0,
                              components={"fallback_uniform": 1.0}) for t in tiles]

        return [
            TileScore(tile_id=t.tile_id, score=acc[t.tile_id] / used_weight,
                      components=comps.get(t.tile_id, {}))
            for t in tiles
        ]

    def describe(self) -> Dict[str, Any]:
        return {
            "scorer": self.name,
            "components": [{"weight": w, **s.describe()} for s, w in self.scorers],
            "last_used": self.last_components,
        }


def select_tiles(
    scores: Sequence[TileScore],
    tiles: Sequence[TileSpec],
    top_k: int,
    min_score: Optional[float] = None,
    spatial_diversity: bool = True,
    diversity_radius_frac: float = 0.0,
    image_size: Optional[Tuple[int, int]] = None,
) -> List[TileSpec]:
    """Pick the top-k tiles, deterministically.

    `spatial_diversity` suppresses near-duplicate picks: after choosing a tile,
    other tiles whose centres fall within `diversity_radius_frac * image
    diagonal` are demoted one round. This matters because the highest-scoring
    tiles are often overlapping neighbours covering the same object, which would
    waste the budget. Set the fraction to 0 to disable.

    Ties are broken by tile_id so the selection is reproducible.
    """
    by_id = {t.tile_id: t for t in tiles}
    ranked = sorted(
        (s for s in scores if s.tile_id in by_id),
        key=lambda s: (-float(s.score), s.tile_id),
    )
    if min_score is not None:
        kept = [s for s in ranked if s.score >= min_score]
        # Never return nothing: a question with no confident region still needs
        # at least one high-resolution look.
        ranked = kept if kept else ranked[:1]

    top_k = max(1, int(top_k))
    if not spatial_diversity or diversity_radius_frac <= 0 or not ranked:
        return [by_id[s.tile_id] for s in ranked[:top_k]]

    if image_size is None:
        first = by_id[ranked[0].tile_id]
        image_size = (first.x1, first.y1)
    diag = math.hypot(float(image_size[0]), float(image_size[1]))
    radius = diversity_radius_frac * diag

    chosen: List[TileSpec] = []
    deferred: List[TileScore] = []
    for s in ranked:
        if len(chosen) >= top_k:
            break
        cand = by_id[s.tile_id]
        cx, cy = cand.center
        if any(math.hypot(cx - c.center[0], cy - c.center[1]) < radius for c in chosen):
            deferred.append(s)
            continue
        chosen.append(cand)

    for s in deferred:
        if len(chosen) >= top_k:
            break
        chosen.append(by_id[s.tile_id])

    return chosen[:top_k]


def build_scorer(cfg: Dict[str, Any], backend: Any = None) -> TileScorer:
    """Construct a scorer from the `selection` config block."""
    mode = str(cfg.get("scorer", "hybrid")).lower()
    ov = int(cfg.get("overview_side", 1024))

    sal = SaliencyScorer(
        overview_side=ov,
        w_edge=float(cfg.get("w_edge", 0.7)),
        w_var=float(cfg.get("w_var", 0.3)),
    )
    if mode == "saliency":
        return sal
    if mode == "clip":
        return ClipScorer(model_id=str(cfg.get("clip_model", "openai/clip-vit-base-patch32")),
                          thumb_size=int(cfg.get("thumb_size", 224)))
    if mode == "vlm":
        if backend is None:
            raise ValueError("selection.scorer='vlm' requires a VLM backend")
        return VLMScorer(backend, batch_tiles=int(cfg.get("vlm_batch_tiles", 6)),
                         thumb_size=int(cfg.get("thumb_size", 336)))
    if mode == "uniform":
        # Control condition: no question conditioning at all.
        return SaliencyScorer(overview_side=ov, w_edge=0.0, w_var=0.0)
    if mode != "hybrid":
        LOG.warning("Unknown selection.scorer=%r; using 'hybrid'.", mode)

    parts: List[Tuple[TileScorer, float]] = [(sal, float(cfg.get("weight_saliency", 0.35)))]
    w_clip = float(cfg.get("weight_clip", 0.65))
    if w_clip > 0:
        parts.append((ClipScorer(
            model_id=str(cfg.get("clip_model", "openai/clip-vit-base-patch32")),
            thumb_size=int(cfg.get("thumb_size", 224)),
        ), w_clip))
    w_vlm = float(cfg.get("weight_vlm", 0.0))
    if w_vlm > 0 and backend is not None:
        parts.append((VLMScorer(backend, batch_tiles=int(cfg.get("vlm_batch_tiles", 6))), w_vlm))
    return HybridScorer(parts)
