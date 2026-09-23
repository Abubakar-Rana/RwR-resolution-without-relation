"""Local object extraction: crop -> objects in global coordinates.

Two proposers share one interface:

  VLMProposer           the default. Asks the VLM itself to list objects with
                        crop-relative boxes, which are then lifted to global
                        coordinates in code. No extra dependencies, and the
                        extraction is question-conditioned.

  OpenVocabProposer     optional. Wraps a transformers zero-shot detector
                        (e.g. Grounding DINO) driven by question keywords.
                        Disabled by default: its availability and exact API
                        depend on the installed transformers version, which we
                        have not verified for your environment. Enable it only
                        after `scripts/00_check_env.py` reports it as loadable.

Plan section 10 asks for the relationship between detection quality and final
reasoning performance, so both proposers report per-tile diagnostics (how many
raw items, how many survived parsing, how many touched a tile border).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..data.schema import DetectedObject
from ..spatial.coords import lift_to_global, to_local_pixels, touches_tile_border
from ..tiling.tiler import TileSpec
from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.models.detector")


@dataclass
class ExtractionResult:
    objects: List[DetectedObject] = field(default_factory=list)
    n_raw: int = 0
    n_parse_failed: int = 0
    n_border_touching: int = 0
    n_tiles_processed: int = 0
    n_tiles_failed: int = 0
    raw_texts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_objects": len(self.objects),
            "n_raw": self.n_raw,
            "n_parse_failed": self.n_parse_failed,
            "n_border_touching": self.n_border_touching,
            "n_tiles_processed": self.n_tiles_processed,
            "n_tiles_failed": self.n_tiles_failed,
        }


# --------------------------------------------------------------------------
# JSON extraction from a model response
# --------------------------------------------------------------------------

def _extract_json_blob(text: str) -> Optional[Any]:
    """Recover a JSON value from model output.

    Handles the usual contamination: ```json fences, a preamble sentence, a
    trailing explanation, and truncated output (we attempt a repair by closing
    open brackets, which recovers the objects that did finish).
    """
    if not text:
        return None
    s = text.strip()

    fence = re.search(r"```(?:json)?\s*(.+?)```", s, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        s = fence.group(1).strip()

    candidates: List[str] = []
    # Widest balanced-looking object, then array.
    for opener, closer in (("{", "}"), ("[", "]")):
        start = s.find(opener)
        end = s.rfind(closer)
        if start != -1 and end > start:
            candidates.append(s[start:end + 1])
    candidates.append(s)

    for cand in candidates:
        try:
            return json.loads(cand)
        except (json.JSONDecodeError, TypeError):
            pass

    # Truncation repair: close whatever is still open.
    start = s.find("{")
    if start == -1:
        start = s.find("[")
    if start != -1:
        frag = s[start:]
        opens = []
        for ch in frag:
            if ch in "{[":
                opens.append(ch)
            elif ch in "}]" and opens:
                opens.pop()
        repaired = frag.rstrip().rstrip(",")
        for ch in reversed(opens):
            repaired += "}" if ch == "{" else "]"
        try:
            return json.loads(repaired)
        except (json.JSONDecodeError, TypeError):
            pass
    return None


def _iter_object_dicts(blob: Any):
    """Yield candidate object dicts from any of the shapes models actually emit."""
    if blob is None:
        return
    if isinstance(blob, dict):
        for key in ("objects", "items", "detections", "results", "data", "output"):
            val = blob.get(key)
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        yield item
                return
        # A single bare object.
        if any(k in blob for k in ("bbox", "box", "bbox_2d", "coordinates")):
            yield blob
        return
    if isinstance(blob, list):
        for item in blob:
            if isinstance(item, dict):
                yield item


_BBOX_KEYS = ("bbox", "box", "bbox_2d", "coordinates", "coords", "rect", "bounding_box")
_LABEL_KEYS = ("label", "name", "category", "class", "object", "type", "text")


def _get_bbox(d: Dict[str, Any]) -> Optional[List[float]]:
    for k in _BBOX_KEYS:
        if k in d:
            v = d[k]
            if isinstance(v, (list, tuple)) and len(v) >= 4:
                try:
                    return [float(x) for x in list(v)[:4]]
                except (TypeError, ValueError):
                    return None
            if isinstance(v, dict):
                for keys in (("x1", "y1", "x2", "y2"), ("left", "top", "right", "bottom")):
                    if all(kk in v for kk in keys):
                        try:
                            return [float(v[kk]) for kk in keys]
                        except (TypeError, ValueError):
                            return None
                if all(kk in v for kk in ("x", "y", "w", "h")):
                    try:
                        x, y = float(v["x"]), float(v["y"])
                        return [x, y, x + float(v["w"]), y + float(v["h"])]
                    except (TypeError, ValueError):
                        return None
            if isinstance(v, str):
                nums = re.findall(r"-?\d+(?:\.\d+)?", v)
                if len(nums) >= 4:
                    return [float(n) for n in nums[:4]]
    # Flat x1/y1/x2/y2 on the object itself.
    for keys in (("x1", "y1", "x2", "y2"), ("left", "top", "right", "bottom")):
        if all(k in d for k in keys):
            try:
                return [float(d[k]) for k in keys]
            except (TypeError, ValueError):
                return None
    return None


def _get_label(d: Dict[str, Any]) -> str:
    for k in _LABEL_KEYS:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()[:64]
        if isinstance(v, (int, float)):
            return str(v)
    return "object"


def _get_attributes(d: Dict[str, Any]) -> Dict[str, Any]:
    attrs = d.get("attributes")
    out: Dict[str, Any] = {}
    if isinstance(attrs, dict):
        for k, v in attrs.items():
            if isinstance(v, (str, int, float, bool)) and str(v).strip():
                out[str(k)[:24]] = v if not isinstance(v, str) else v.strip()[:48]
    elif isinstance(attrs, list):
        vals = [str(a).strip()[:48] for a in attrs if str(a).strip()]
        if vals:
            out["tags"] = ", ".join(vals[:6])
    # Attributes sometimes arrive as siblings rather than nested.
    for k in ("color", "colour", "condition", "state", "motion", "motion_state", "size"):
        v = d.get(k)
        if isinstance(v, (str, int, float)) and str(v).strip() and k not in out:
            out[k.replace("colour", "color")] = str(v).strip()[:48]
    return out


def parse_objects_from_text(
    text: str,
    tile: TileSpec,
    crop_size: Tuple[int, int],
    image_size: Tuple[int, int],
    max_objects: int = 32,
    default_score: float = 1.0,
) -> Tuple[List[DetectedObject], int, int]:
    """Parse a local-extraction response into globally-registered objects.

    Returns (objects, n_raw, n_parse_failed). Items whose box cannot be read are
    counted as parse failures and dropped rather than being given a made-up box.
    """
    blob = _extract_json_blob(text)
    raw = list(_iter_object_dicts(blob))

    # Fallback for models that answer in prose despite the JSON instruction.
    if not raw and text:
        raw = _parse_prose_objects(text)

    objects: List[DetectedObject] = []
    n_failed = 0
    for d in raw[:max_objects]:
        bbox = _get_bbox(d)
        if bbox is None:
            n_failed += 1
            continue
        local = to_local_pixels(bbox, crop_size)
        if local is None:
            n_failed += 1
            continue
        glob = lift_to_global(local, tile, crop_size=crop_size,
                              clamp=True, image_size=image_size)
        if glob is None:
            n_failed += 1
            continue
        score = d.get("score", d.get("confidence", default_score))
        try:
            score = float(score)
            if score > 1.0:  # a percentage
                score = min(1.0, score / 100.0)
        except (TypeError, ValueError):
            score = default_score
        objects.append(DetectedObject(
            label=_get_label(d),
            bbox_global=glob,
            score=score,
            tile_id=tile.tile_id,
            attributes=_get_attributes(d),
        ))
    return objects, len(raw), n_failed


def _parse_prose_objects(text: str) -> List[Dict[str, Any]]:
    """Last resort: 'label [x1, y1, x2, y2]' or 'label: (x1,y1,x2,y2)' lines."""
    out: List[Dict[str, Any]] = []
    pattern = re.compile(
        r"([A-Za-z][A-Za-z \-]{1,40}?)\s*[:=]?\s*[\[\(]\s*"
        r"(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*"
        r"(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*[\]\)]"
    )
    for m in pattern.finditer(text):
        out.append({
            "label": m.group(1).strip(" -:"),
            "bbox": [float(m.group(i)) for i in range(2, 6)],
        })
    return out


# --------------------------------------------------------------------------
# Proposers
# --------------------------------------------------------------------------

class RegionProposer:
    name = "abstract"
    uses_vlm = False

    def extract(self, ti: Any, tiles: Sequence[TileSpec], question: str,
                keywords: Optional[Sequence[str]] = None,
                meter: Any = None, collector: Any = None) -> ExtractionResult:
        raise NotImplementedError

    def describe(self) -> Dict[str, Any]:
        return {"proposer": self.name}


class VLMProposer(RegionProposer):
    """Default proposer: the VLM lists objects per crop.

    One VLM call per selected tile. Those calls dominate the proposed method's
    cost, which is precisely why the compute-matched comparison in plan section 9
    must give Baseline 3 the same number of calls - and it does, because Baseline 3
    uses this same proposer.
    """

    name = "vlm"
    uses_vlm = True

    def __init__(self, backend: Any, max_objects_per_tile: int = 12,
                 max_new_tokens: int = 640, crop_max_pixels: Optional[int] = None,
                 retry_attempts: int = 2) -> None:
        self.backend = backend
        self.max_objects_per_tile = int(max_objects_per_tile)
        self.max_new_tokens = int(max_new_tokens)
        self.crop_max_pixels = crop_max_pixels
        self.retry_attempts = int(retry_attempts)

    def extract(self, ti: Any, tiles: Sequence[TileSpec], question: str,
                keywords: Optional[Sequence[str]] = None,
                meter: Any = None, collector: Any = None) -> ExtractionResult:
        from ..prompts.templates import local_extraction_prompt
        from ..utils.errors import RetryConfig, retry_call

        res = ExtractionResult()
        image_size = (ti.width, ti.height)

        for tile in tiles:
            try:
                crop = ti.crop(tile)
            except Exception as exc:
                res.n_tiles_failed += 1
                if collector is not None:
                    collector.add("crop:tile{}".format(tile.tile_id), exc)
                LOG.error("Tile %d crop failed: %s", tile.tile_id, exc)
                continue

            prompt = local_extraction_prompt(
                question=question,
                tile_box=list(tile.box),
                image_size=list(image_size),
                max_objects=self.max_objects_per_tile,
                keywords=keywords,
            )

            try:
                resp = retry_call(
                    self.backend.generate,
                    prompt,
                    images=[crop],
                    max_new_tokens=self.max_new_tokens,
                    retry=RetryConfig(attempts=self.retry_attempts, base_delay=1.0),
                    stage_name="extract:tile{}".format(tile.tile_id),
                    collector=collector,
                    max_pixels_override=self.crop_max_pixels,
                )
            except Exception as exc:
                res.n_tiles_failed += 1
                if meter is not None:
                    meter.record_call(failed=True)
                LOG.error("Extraction failed for tile %d after retries: %s",
                          tile.tile_id, exc)
                continue

            res.n_tiles_processed += 1
            if meter is not None:
                meter.record_call(resp.prompt_tokens, resp.completion_tokens,
                                  resp.n_images, resp.pixels)
            res.raw_texts.append(resp.text)

            objs, n_raw, n_bad = parse_objects_from_text(
                resp.text, tile, crop.size, image_size,
                max_objects=self.max_objects_per_tile,
            )
            res.n_raw += n_raw
            res.n_parse_failed += n_bad
            for o in objs:
                if touches_tile_border(o.bbox_global, tile):
                    o.attributes["border"] = True
                    res.n_border_touching += 1
            res.objects.extend(objs)

            try:
                crop.close()
            except Exception:
                pass

        return res

    def describe(self) -> Dict[str, Any]:
        return {
            "proposer": self.name,
            "max_objects_per_tile": self.max_objects_per_tile,
            "max_new_tokens": self.max_new_tokens,
            "crop_max_pixels": self.crop_max_pixels,
        }


class OpenVocabProposer(RegionProposer):
    """Optional zero-shot detector proposer (e.g. Grounding DINO).

    NOT enabled by default and NOT verified against your installed transformers
    version. The class targets the standard
    `AutoModelForZeroShotObjectDetection` +
    `post_process_grounded_object_detection` interface. If either is missing or
    its signature differs, `load()` raises a clear ImportError and the pipeline
    falls back to VLMProposer rather than silently producing no objects.

    Value if it does work: it decouples detection from the VLM, letting you vary
    detection quality independently, which is what plan section 10's
    "relationship between object detection quality and final reasoning
    performance" needs.
    """

    name = "openvocab"
    uses_vlm = False

    def __init__(self, model_id: str = "IDEA-Research/grounding-dino-base",
                 box_threshold: float = 0.3, text_threshold: float = 0.25,
                 device: Optional[str] = None, max_objects_per_tile: int = 24,
                 default_queries: Optional[Sequence[str]] = None) -> None:
        self.model_id = model_id
        self.box_threshold = float(box_threshold)
        self.text_threshold = float(text_threshold)
        self.device = device
        self.max_objects_per_tile = int(max_objects_per_tile)
        self.default_queries = list(default_queries or
                                    ["building", "road", "vehicle", "water", "tree"])
        self._model = None
        self._processor = None

    def load(self) -> "OpenVocabProposer":
        if self._model is not None:
            return self
        try:
            import torch
            from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor
        except ImportError as exc:
            raise ImportError(
                "OpenVocabProposer needs transformers with "
                "AutoModelForZeroShotObjectDetection. Either upgrade transformers "
                "or set detection.proposer='vlm'."
            ) from exc
        if self.device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._processor = AutoProcessor.from_pretrained(self.model_id)
        self._model = AutoModelForZeroShotObjectDetection.from_pretrained(
            self.model_id).to(self.device).eval()
        if not hasattr(self._processor, "post_process_grounded_object_detection"):
            raise ImportError(
                "The processor for {} does not expose "
                "post_process_grounded_object_detection; this transformers version "
                "is not supported by OpenVocabProposer.".format(self.model_id)
            )
        return self

    def extract(self, ti: Any, tiles: Sequence[TileSpec], question: str,
                keywords: Optional[Sequence[str]] = None,
                meter: Any = None, collector: Any = None) -> ExtractionResult:
        import torch

        self.load()
        res = ExtractionResult()
        image_size = (ti.width, ti.height)
        queries = [k for k in (keywords or []) if str(k).strip()] or self.default_queries
        # Grounding DINO expects lowercase phrases separated by ". ".
        text = ". ".join(str(q).lower().strip() for q in queries[:12]) + "."

        for tile in tiles:
            try:
                crop = ti.crop(tile)
            except Exception as exc:
                res.n_tiles_failed += 1
                if collector is not None:
                    collector.add("crop:tile{}".format(tile.tile_id), exc)
                continue
            try:
                inputs = self._processor(images=crop, text=text,
                                         return_tensors="pt").to(self.device)
                with torch.inference_mode():
                    outputs = self._model(**inputs)
                processed = self._processor.post_process_grounded_object_detection(
                    outputs,
                    inputs["input_ids"],
                    threshold=self.box_threshold,
                    text_threshold=self.text_threshold,
                    target_sizes=[crop.size[::-1]],
                )[0]
            except Exception as exc:
                res.n_tiles_failed += 1
                if collector is not None:
                    collector.add("openvocab:tile{}".format(tile.tile_id), exc)
                LOG.error("Zero-shot detection failed on tile %d: %s", tile.tile_id, exc)
                continue

            res.n_tiles_processed += 1
            boxes = processed.get("boxes")
            scores = processed.get("scores")
            labels = processed.get("labels") or processed.get("text_labels") or []
            n = 0 if boxes is None else len(boxes)
            res.n_raw += n
            for i in range(min(n, self.max_objects_per_tile)):
                try:
                    bb = [float(v) for v in boxes[i].tolist()]
                except Exception:
                    res.n_parse_failed += 1
                    continue
                glob = lift_to_global(tuple(bb), tile, crop_size=crop.size,
                                      clamp=True, image_size=image_size)
                if glob is None:
                    res.n_parse_failed += 1
                    continue
                label = labels[i] if i < len(labels) else "object"
                obj = DetectedObject(
                    label=str(label)[:64] or "object",
                    bbox_global=glob,
                    score=float(scores[i]) if scores is not None else 1.0,
                    tile_id=tile.tile_id,
                )
                if touches_tile_border(glob, tile):
                    obj.attributes["border"] = True
                    res.n_border_touching += 1
                res.objects.append(obj)
            try:
                crop.close()
            except Exception:
                pass
        return res

    def describe(self) -> Dict[str, Any]:
        return {
            "proposer": self.name,
            "model_id": self.model_id,
            "box_threshold": self.box_threshold,
            "text_threshold": self.text_threshold,
        }


def build_proposer(cfg: Dict[str, Any], backend: Any) -> RegionProposer:
    """Construct a proposer from the `detection` config block.

    Falls back to the VLM proposer (with a warning) if an optional detector
    cannot be loaded, so a run never dies on an unavailable dependency.
    """
    mode = str(cfg.get("proposer", "vlm")).lower()
    if mode in ("openvocab", "grounding_dino", "dino"):
        prop = OpenVocabProposer(
            model_id=str(cfg.get("model_id", "IDEA-Research/grounding-dino-base")),
            box_threshold=float(cfg.get("box_threshold", 0.3)),
            text_threshold=float(cfg.get("text_threshold", 0.25)),
            max_objects_per_tile=int(cfg.get("max_objects_per_tile", 24)),
        )
        try:
            prop.load()
            return prop
        except Exception as exc:
            LOG.error("Falling back to the VLM proposer: %s", exc)
    return VLMProposer(
        backend,
        max_objects_per_tile=int(cfg.get("max_objects_per_tile", 12)),
        max_new_tokens=int(cfg.get("max_new_tokens", 640)),
        crop_max_pixels=cfg.get("crop_max_pixels"),
    )
