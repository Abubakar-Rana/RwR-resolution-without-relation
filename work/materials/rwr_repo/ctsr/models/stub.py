"""Offline stub backend.

Purpose: exercise every code path (tiling, selection, detection parsing,
coordinate lifting, relation building, prompt assembly, metric computation,
table and figure generation) on a laptop with no GPU and no model weights, so
that the only thing left to debug on the GPU machine is the model itself.

This backend produces DETERMINISTIC, CONTENT-FREE output. It is not a model.
`is_stub = True` propagates into every results file and every generated table,
and the report writer refuses to emit a findings section from stub runs. Never
report a number produced by this backend.
"""
from __future__ import annotations

import hashlib
import json
import re
import time
from typing import Any, Dict, List, Optional, Sequence

from .base import VLMBackend, VLMResponse


def _h(text: str, mod: int) -> int:
    """Deterministic hash in [0, mod)."""
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:12], 16) % max(1, mod)


class StubBackend(VLMBackend):
    """Deterministic fake VLM for dry runs."""

    name = "stub"
    is_stub = True

    def __init__(self, max_new_tokens: int = 256, latency_s: float = 0.0,
                 fail_every: int = 0, n_fake_objects: int = 4) -> None:
        self.max_new_tokens = max_new_tokens
        self.latency_s = float(latency_s)
        # fail_every > 0 injects a synthetic exception on every Nth call so the
        # retry / error-isolation paths get exercised too.
        self.fail_every = int(fail_every)
        self.n_fake_objects = int(n_fake_objects)
        self._calls = 0

    def generate(
        self,
        prompt: str,
        images: Optional[Sequence[Any]] = None,
        max_new_tokens: Optional[int] = None,
        system: Optional[str] = None,
        **kwargs: Any,
    ) -> VLMResponse:
        self._calls += 1
        if self.fail_every and self._calls % self.fail_every == 0:
            raise RuntimeError("StubBackend injected failure (call {})".format(self._calls))
        if self.latency_s:
            time.sleep(self.latency_s)

        imgs = [im for im in (images or []) if im is not None]
        pixels = 0
        for im in imgs:
            size = getattr(im, "size", None)
            if size and len(size) == 2:
                pixels += int(size[0]) * int(size[1])

        text = self._answer(prompt)
        return VLMResponse(
            text=text,
            prompt_tokens=max(1, len(prompt) // 4),
            completion_tokens=max(1, len(text) // 4),
            n_images=len(imgs),
            pixels=pixels,
            latency_s=self.latency_s,
            meta={"stub": True, "call": self._calls},
        )

    # -- deterministic response shaping -------------------------------------
    def _answer(self, prompt: str) -> str:
        """Return something the corresponding parser can actually consume."""
        low = prompt.lower()

        # Local object-extraction prompts expect a JSON object list.
        if "json" in low and ("bbox" in low or "objects" in low):
            objs: List[Dict[str, Any]] = []
            labels = ["building", "vehicle", "road", "tree", "water body", "aircraft"]
            for i in range(self.n_fake_objects):
                seed = "{}|{}".format(prompt[-256:], i)
                x = _h(seed + "x", 700)
                y = _h(seed + "y", 700)
                w = 20 + _h(seed + "w", 120)
                hh = 20 + _h(seed + "h", 120)
                objs.append({
                    "label": labels[_h(seed + "l", len(labels))],
                    "bbox": [x, y, min(999, x + w), min(999, y + hh)],
                    "attributes": {"color": ["grey", "white", "dark"][_h(seed + "c", 3)]},
                })
            return json.dumps({"objects": objs}, ensure_ascii=False)

        # Grounding prompts expect a single box.
        if "bounding box" in low or "bbox" in low:
            seed = prompt[-256:]
            x = _h(seed + "gx", 800)
            y = _h(seed + "gy", 800)
            return "[{}, {}, {}, {}]".format(x, y, x + 120, y + 120)

        # MCQ prompts: pick a letter from those actually offered.
        letters = self._offered_letters(prompt)
        if letters:
            return letters[_h(prompt[-512:], len(letters))]

        # Tile relevance scoring prompts expect a number.
        if "relevance" in low and "0" in low and "10" in low:
            return str(_h(prompt[-256:], 11))

        # Otherwise: a caption-shaped sentence.
        return ("A remote sensing scene containing several structures and "
                "transport corridors distributed across the image.")

    @staticmethod
    def _offered_letters(prompt: str) -> List[str]:
        found = re.findall(r"^\s*([A-H])[.)]\s+\S", prompt, flags=re.MULTILINE)
        seen: List[str] = []
        for f in found:
            if f not in seen:
                seen.append(f)
        return seen

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_stub": True,
            "warning": "Deterministic placeholder output. Never report these numbers.",
            "fail_every": self.fail_every,
        }
