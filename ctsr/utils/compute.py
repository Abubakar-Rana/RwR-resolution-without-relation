"""Compute accounting.

Section 9 of the research plan requires reporting performance alongside
inference cost so that gains can be attributed to the reasoning mechanism
rather than to simply looking at more pixels. Every pipeline shares this meter,
which records, per sample:

  * number of VLM calls
  * prompt / completion tokens
  * number of image tiles actually encoded, and their total pixel count
  * wall-clock time per stage
  * peak GPU memory

`pixels_encoded` is the key budget variable for the compute-matched comparison
between Baseline 3 and the proposed method: both must see the same pixels, and
only the relation block should differ.
"""
from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def peak_vram_mb() -> Optional[float]:
    """Peak allocated CUDA memory in MiB since the last reset, or None on CPU."""
    try:
        import torch
        if not torch.cuda.is_available():
            return None
        return float(torch.cuda.max_memory_allocated()) / (1024.0 ** 2)
    except Exception:
        return None


def reset_peak_vram() -> None:
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
    except Exception:
        pass


def cuda_sync() -> None:
    """Synchronise before reading a timer, so GPU time is not under-counted."""
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.synchronize()
    except Exception:
        pass


@dataclass
class ComputeMeter:
    """Accumulator for one sample's compute footprint."""

    n_vlm_calls: int = 0
    n_vlm_failures: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    n_images_encoded: int = 0
    pixels_encoded: int = 0
    stage_seconds: Dict[str, float] = field(default_factory=lambda: defaultdict(float))
    t_start: float = field(default_factory=time.perf_counter)

    def record_call(self, prompt_tokens: int = 0, completion_tokens: int = 0,
                    n_images: int = 0, pixels: int = 0, failed: bool = False) -> None:
        self.n_vlm_calls += 1
        if failed:
            self.n_vlm_failures += 1
        self.prompt_tokens += int(prompt_tokens or 0)
        self.completion_tokens += int(completion_tokens or 0)
        self.n_images_encoded += int(n_images or 0)
        self.pixels_encoded += int(pixels or 0)

    def timer(self, name: str) -> "_StageTimer":
        return _StageTimer(self, name)

    @property
    def wall_seconds(self) -> float:
        return time.perf_counter() - self.t_start

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def to_dict(self) -> Dict[str, Any]:
        return {
            "n_vlm_calls": self.n_vlm_calls,
            "n_vlm_failures": self.n_vlm_failures,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "n_images_encoded": self.n_images_encoded,
            "pixels_encoded": self.pixels_encoded,
            "megapixels_encoded": round(self.pixels_encoded / 1e6, 4),
            "wall_seconds": round(self.wall_seconds, 4),
            "stage_seconds": {k: round(v, 4) for k, v in sorted(self.stage_seconds.items())},
            "peak_vram_mb": (lambda v: round(v, 1) if v is not None else None)(peak_vram_mb()),
        }


class _StageTimer:
    """Context manager accumulating wall time into meter.stage_seconds[name]."""

    def __init__(self, meter: ComputeMeter, name: str) -> None:
        self.meter = meter
        self.name = name
        self.t0 = 0.0

    def __enter__(self) -> "_StageTimer":
        cuda_sync()
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, *exc) -> None:
        cuda_sync()
        self.meter.stage_seconds[self.name] += time.perf_counter() - self.t0


def env_info() -> Dict[str, Any]:
    """Environment fingerprint stored in every run manifest for reproducibility."""
    import platform
    import sys

    info: Dict[str, Any] = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor(),
    }
    try:
        import torch
        info["torch"] = torch.__version__
        info["cuda_available"] = bool(torch.cuda.is_available())
        info["cuda_version"] = getattr(torch.version, "cuda", None)
        if torch.cuda.is_available():
            info["gpu_count"] = torch.cuda.device_count()
            info["gpus"] = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
            try:
                props = torch.cuda.get_device_properties(0)
                info["gpu0_total_mem_gb"] = round(props.total_memory / (1024 ** 3), 2)
            except Exception:
                pass
    except Exception as exc:
        info["torch"] = "unavailable: {}".format(exc)
    for mod in ("transformers", "accelerate", "PIL", "numpy", "pandas"):
        try:
            m = __import__(mod)
            info[mod] = getattr(m, "__version__", "unknown")
        except Exception:
            info[mod] = None
    return info
