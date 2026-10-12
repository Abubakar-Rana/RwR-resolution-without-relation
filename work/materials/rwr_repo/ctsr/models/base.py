"""VLM backend interface.

Every pipeline talks to the model only through `VLMBackend.generate`, so the
backend can be swapped (Qwen2.5-VL on GPU, or the offline stub used to validate
the plumbing) without touching pipeline code.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


@dataclass
class VLMResponse:
    text: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    n_images: int = 0
    pixels: int = 0
    latency_s: float = 0.0
    truncated: bool = False
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "n_images": self.n_images,
            "pixels": self.pixels,
            "latency_s": round(self.latency_s, 4),
            "truncated": self.truncated,
        }


class VLMBackend:
    """Abstract VLM.

    Subclasses implement `_generate`. `is_stub` must be True for any backend
    that does not run a real model, so the runner can stamp results as
    non-scientific and the report generator can refuse to present them as
    findings.
    """

    name: str = "abstract"
    is_stub: bool = False

    def generate(
        self,
        prompt: str,
        images: Optional[Sequence[Any]] = None,
        max_new_tokens: int = 256,
        system: Optional[str] = None,
        **kwargs: Any,
    ) -> VLMResponse:
        raise NotImplementedError

    def load(self) -> "VLMBackend":
        """Eagerly initialise weights. Optional; backends may load lazily."""
        return self

    def unload(self) -> None:
        """Release weights and GPU memory."""
        return None

    def describe(self) -> Dict[str, Any]:
        return {"name": self.name, "is_stub": self.is_stub}
