"""Config loading: YAML/JSON with inheritance, CLI overrides and validation.

A config file may declare `base: <path>` to inherit from another, which is how the
ablation configs stay one-liners: each says what it changes and nothing else. That
matters for the experiment's integrity - an ablation config that restates every
parameter can drift from the arm it is meant to be compared against.

Overrides are dotted: `--set selection.top_k=8 model.max_pixels_tokens=640`.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from .utils.logging_utils import get_logger

LOG = get_logger("ctsr.config")

DEFAULTS: Dict[str, Any] = {
    "seed": 1234,
    "save_prompts": False,
    "data": {
        "source": "hf",
        "name_or_path": "initiacms/XLRS-Bench-lite",
        "split": "train",
        "config_name": None,
        "image_root": None,
        "cache_dir": "data/image_cache",
        "field_map": {},
        "hf_kwargs": {},
        "materialise_images": True,
        "limit": None,
        "per_task_limit": None,
        "categories": None,
    },
    "model": {
        "backend": "qwen",                 # qwen | stub
        "model_id": "Qwen/Qwen2.5-VL-7B-Instruct",
        "torch_dtype": "bfloat16",
        "device_map": "auto",
        "attn_implementation": None,       # "flash_attention_2" if installed
        "min_pixels_tokens": 256,
        "max_pixels_tokens": 1280,
        "load_in_4bit": False,
        "trust_remote_code": False,
        "stub_fail_every": 0,
    },
    "generation": {
        "max_new_tokens": 256,
        "caption_max_new_tokens": 512,
        "retry_attempts": 3,
        "retry_base_delay": 2.0,
    },
    "tiling": {
        "tile_size": 1024,
        "overlap": 128,
        "max_tiles": 256,
        "overview_side": 1024,
    },
    "selection": {
        "scorer": "hybrid",                # hybrid | clip | saliency | vlm | uniform
        "clip_model": "openai/clip-vit-base-patch32",
        "thumb_size": 224,
        "weight_saliency": 0.35,
        "weight_clip": 0.65,
        "weight_vlm": 0.0,
        "vlm_batch_tiles": 6,
        "w_edge": 0.7,
        "w_var": 0.3,
        "overview_side": 1024,
        "top_k": 5,
        "min_score": None,
        "spatial_diversity": True,
        "diversity_radius_frac": 0.04,
    },
    "detection": {
        "proposer": "vlm",                 # vlm | openvocab
        "max_objects_per_tile": 12,
        "max_objects_total": 60,
        "max_new_tokens": 640,
        "crop_max_pixels": None,
        "model_id": "IDEA-Research/grounding-dino-base",
        "box_threshold": 0.3,
        "text_threshold": 0.25,
    },
    "dedup": {
        "enabled": True,
        "iou_thresh": 0.45,
        "cross_tile_iou_thresh": 0.25,
        "containment_thresh": 0.80,
        "seam_gap_px": 8.0,
        "strict_labels": False,
        "box_mode": "union",
    },
    "relations": {
        "max_neighbours": 6,
        "adjacency_gap_frac": 0.012,
        "near_dist_frac": 0.06,
        "containment_thresh": 0.85,
        "intersect_iou_thresh": 0.05,
        "include_direction": True,
        "include_distance": True,
        "include_adjacency": True,
        "include_containment": True,
        "include_intersection": True,
        "use_compass": True,
        "gsd_m_per_px": None,              # set only if you know the GSD
        "max_relations": 220,
        "token_budget": 1400,
    },
    "final_call": {
        "attach_overview": True,
        "attach_crops": 3,
        "crop_thumb_side": 768,
    },
    "baseline1": {
        "send_full_resolution": True,
        "pre_resize_pixels": None,
    },
    "baseline2": {
        "max_answer_tiles": 8,
        "tile_choice": "grid",
        "include_overview_in_vote": False,
    },
    "ablation": {
        "pad_tokens_in_baseline": False,
        "shuffle_relations": False,
        "drop_global_coords": False,
    },
    "eval": {
        "iou_thresholds": [0.5, 0.7],
        "primary_iou": 0.5,
        "n_bootstrap": 10000,
        "alpha": 0.05,
        "relational_tasks": None,          # null = the pre-registered default
    },
    "run": {
        "out_dir": "results",
        "resume": True,
        "retry_errors": True,
        "progress_every": 10,
        "arms": ["b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"],
    },
}


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive dict merge; `override` wins. Lists are replaced, not concatenated."""
    out = copy.deepcopy(base)
    for k, v in (override or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def _read_file(path) -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError("Config not found: {}".format(p))
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError as exc:
            raise ImportError(
                "Reading {} needs PyYAML: pip install pyyaml (or use a .json config)"
                .format(p.name)
            ) from exc
        data = yaml.safe_load(text) or {}
    else:
        data = json.loads(text) if text.strip() else {}
    if not isinstance(data, dict):
        raise ValueError("Config {} must contain a mapping at the top level".format(p))
    return data


def load_config(path: Optional[str] = None,
                overrides: Optional[Sequence[str]] = None,
                _seen: Optional[List[str]] = None) -> Dict[str, Any]:
    """Load DEFAULTS <- base chain <- file <- CLI overrides."""
    cfg = copy.deepcopy(DEFAULTS)

    if path:
        _seen = list(_seen or [])
        resolved = str(Path(path).resolve())
        if resolved in _seen:
            raise ValueError("Circular config inheritance at {}".format(path))
        _seen.append(resolved)

        data = _read_file(path)
        base = data.pop("base", None)
        if base:
            base_path = (Path(path).parent / base) if not Path(base).is_absolute() else Path(base)
            cfg = deep_merge(cfg, load_config(str(base_path), None, _seen))
        cfg = deep_merge(cfg, data)
        cfg["_config_path"] = str(path)

    for item in (overrides or []):
        cfg = apply_override(cfg, item)

    validate(cfg)
    return cfg


def apply_override(cfg: Dict[str, Any], item: str) -> Dict[str, Any]:
    """Apply one `dotted.key=value` override, parsing the value as JSON if possible."""
    if "=" not in item:
        raise ValueError("Override {!r} must be of the form key.path=value".format(item))
    key, raw = item.split("=", 1)
    keys = [k for k in key.strip().split(".") if k]
    if not keys:
        raise ValueError("Override {!r} has an empty key".format(item))

    try:
        value: Any = json.loads(raw)
    except json.JSONDecodeError:
        low = raw.strip().lower()
        if low in ("none", "null", ""):
            value = None
        elif low in ("true", "false"):
            value = (low == "true")
        else:
            value = raw

    node = cfg
    for k in keys[:-1]:
        nxt = node.get(k)
        if not isinstance(nxt, dict):
            nxt = {}
            node[k] = nxt
        node = nxt
    node[keys[-1]] = value
    LOG.info("Override: %s = %r", key, value)
    return cfg


def validate(cfg: Dict[str, Any]) -> None:
    """Fail fast on configurations that would produce meaningless results."""
    problems: List[str] = []

    backend = str((cfg.get("model") or {}).get("backend", "")).lower()
    if backend not in ("qwen", "stub"):
        problems.append("model.backend must be 'qwen' or 'stub', got {!r}".format(backend))

    t = cfg.get("tiling") or {}
    if int(t.get("tile_size", 0)) <= 0:
        problems.append("tiling.tile_size must be positive")
    if int(t.get("overlap", 0)) >= int(t.get("tile_size", 1)):
        problems.append("tiling.overlap must be smaller than tiling.tile_size")

    s = cfg.get("selection") or {}
    if int(s.get("top_k", 0)) <= 0:
        problems.append("selection.top_k must be at least 1")
    weights = [float(s.get("weight_saliency", 0)), float(s.get("weight_clip", 0)),
               float(s.get("weight_vlm", 0))]
    if str(s.get("scorer")) == "hybrid" and sum(weights) <= 0:
        problems.append("selection.scorer='hybrid' needs at least one non-zero weight")

    m = cfg.get("model") or {}
    if int(m.get("min_pixels_tokens", 1)) > int(m.get("max_pixels_tokens", 1)):
        problems.append("model.min_pixels_tokens must not exceed max_pixels_tokens")

    e = cfg.get("eval") or {}
    if not (0 < float(e.get("alpha", 0.05)) < 1):
        problems.append("eval.alpha must be between 0 and 1")

    arms = (cfg.get("run") or {}).get("arms") or []
    known = {"b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"}
    unknown = [a for a in arms if a not in known]
    if unknown:
        problems.append("run.arms contains unknown arm(s) {}; known: {}"
                        .format(unknown, sorted(known)))

    if problems:
        raise ValueError("Invalid configuration:\n  - " + "\n  - ".join(problems))

    # Warnings: legal but likely to mislead.
    if backend == "stub":
        LOG.warning("model.backend='stub': output is placeholder text. Use it to "
                    "validate the pipeline, never to produce results.")
    if str(s.get("scorer")) == "vlm" or float(s.get("weight_vlm", 0)) > 0:
        LOG.warning("VLM-based tile scoring is enabled. Those calls are charged to "
                    "the compute budget; keep the setting identical across arms.")
    if (cfg.get("ablation") or {}).get("shuffle_relations"):
        LOG.warning("ablation.shuffle_relations=True: relations are deliberately "
                    "scrambled. This is a control condition, not the method.")


def relational_tasks(cfg: Dict[str, Any]):
    """The relational task set from config, or the pre-registered default."""
    from .data.taxonomy import DEFAULT_RELATIONAL_TASKS, canonical_task

    custom = (cfg.get("eval") or {}).get("relational_tasks")
    if not custom:
        return set(DEFAULT_RELATIONAL_TASKS)
    return {canonical_task(t) for t in custom}


def build_backend(cfg: Dict[str, Any]):
    """Instantiate the VLM backend named by the config."""
    m = cfg.get("model") or {}
    backend = str(m.get("backend", "qwen")).lower()
    gen = cfg.get("generation") or {}

    if backend == "stub":
        from .models.stub import StubBackend
        return StubBackend(
            max_new_tokens=int(gen.get("max_new_tokens", 256)),
            fail_every=int(m.get("stub_fail_every", 0)),
        )

    from .models.qwen_vl import QwenVLBackend
    return QwenVLBackend(
        model_id=str(m.get("model_id", "Qwen/Qwen2.5-VL-7B-Instruct")),
        device_map=str(m.get("device_map", "auto")),
        torch_dtype=str(m.get("torch_dtype", "bfloat16")),
        attn_implementation=m.get("attn_implementation"),
        min_pixels_tokens=int(m.get("min_pixels_tokens", 256)),
        max_pixels_tokens=int(m.get("max_pixels_tokens", 1280)),
        max_new_tokens=int(gen.get("max_new_tokens", 256)),
        trust_remote_code=bool(m.get("trust_remote_code", False)),
        load_in_4bit=bool(m.get("load_in_4bit", False)),
    )


def build_dataset(cfg: Dict[str, Any]):
    """Instantiate the dataset loader from the `data` block."""
    from .data.xlrs import XLRSDataset

    d = cfg.get("data") or {}
    return XLRSDataset(
        source=str(d.get("source", "hf")),
        name_or_path=str(d.get("name_or_path", "initiacms/XLRS-Bench-lite")),
        split=str(d.get("split", "train")),
        config_name=d.get("config_name"),
        image_root=d.get("image_root"),
        cache_dir=str(d.get("cache_dir", "data/image_cache")),
        field_map=d.get("field_map") or {},
        hf_kwargs=d.get("hf_kwargs") or {},
        materialise_images=bool(d.get("materialise_images", True)),
    )


def load_samples(cfg: Dict[str, Any]):
    """Load, filter and subsample the dataset according to the config."""
    from .data.xlrs import stratified_subset, summarise

    d = cfg.get("data") or {}
    ds = build_dataset(cfg)
    samples = ds.load(limit=d.get("limit"), categories=d.get("categories"))

    per_task = d.get("per_task_limit")
    if per_task:
        before = len(samples)
        samples = stratified_subset(samples, int(per_task), seed=int(cfg.get("seed", 1234)))
        LOG.info("Stratified subset: %d -> %d samples (<= %d per task)",
                 before, len(samples), int(per_task))

    info = summarise(samples)
    info["field_map"] = ds.resolved_map
    info["columns"] = ds.columns
    info["source"] = d.get("source")
    info["name_or_path"] = d.get("name_or_path")
    return samples, info
