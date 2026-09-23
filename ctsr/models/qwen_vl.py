"""Qwen2.5-VL backend.

The inference recipe below follows the official model card for
`Qwen/Qwen2.5-VL-7B-Instruct` (verified):

    from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        "Qwen/Qwen2.5-VL-7B-Instruct", torch_dtype="auto", device_map="auto")
    processor = AutoProcessor.from_pretrained(..., min_pixels=..., max_pixels=...)
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(text=[text], images=image_inputs, videos=video_inputs,
                       padding=True, return_tensors="pt").to("cuda")
    out = model.generate(**inputs, max_new_tokens=128)

`min_pixels` / `max_pixels` are the knob that decides how much of an
ultra-high-resolution image actually survives the visual encoder, so they are
first-class config here and are recorded per call for the compute accounting.

OOM handling: the vision token count scales with pixels, so on an OOM we halve
`max_pixels` for the retry (down to a floor) and, if still failing, drop to the
single most important image. The degradation is recorded in the response meta so
it shows up in the results rather than silently changing the experiment.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Sequence

from ..utils.errors import free_gpu, is_oom
from ..utils.logging_utils import get_logger
from .base import VLMBackend, VLMResponse

LOG = get_logger("ctsr.models.qwen")

# Qwen's vision tower works in 28x28 patch units; pixel budgets are expressed as
# (number of visual tokens) * 28 * 28, matching the model card's convention.
PATCH_AREA = 28 * 28

DEFAULT_SYSTEM = (
    "You are a meticulous remote-sensing image analyst. "
    "Answer strictly in the format requested and do not invent objects you cannot see."
)


class QwenVLBackend(VLMBackend):
    is_stub = False

    def __init__(
        self,
        model_id: str = "Qwen/Qwen2.5-VL-7B-Instruct",
        device_map: str = "auto",
        torch_dtype: str = "bfloat16",
        attn_implementation: Optional[str] = None,
        min_pixels_tokens: int = 256,
        max_pixels_tokens: int = 1280,
        min_pixels_tokens_floor: int = 64,
        max_new_tokens: int = 256,
        do_sample: bool = False,
        temperature: float = 0.0,
        top_p: float = 1.0,
        trust_remote_code: bool = False,
        load_in_4bit: bool = False,
        use_fast_processor: bool = True,
    ) -> None:
        self.name = model_id
        self.model_id = model_id
        self.device_map = device_map
        self.torch_dtype = torch_dtype
        self.attn_implementation = attn_implementation
        # Stored in *pixels*, derived from the token budgets.
        self.min_pixels = int(min_pixels_tokens) * PATCH_AREA
        self.max_pixels = int(max_pixels_tokens) * PATCH_AREA
        self.max_pixels_default = self.max_pixels
        self.min_pixels_floor = int(min_pixels_tokens_floor) * PATCH_AREA
        self.max_new_tokens = int(max_new_tokens)
        self.do_sample = bool(do_sample)
        self.temperature = float(temperature)
        self.top_p = float(top_p)
        self.trust_remote_code = bool(trust_remote_code)
        self.load_in_4bit = bool(load_in_4bit)
        self.use_fast_processor = bool(use_fast_processor)

        self._model = None
        self._processor = None
        self._process_vision_info = None
        self._device = "cuda"

    # -- lifecycle ----------------------------------------------------------
    def load(self) -> "QwenVLBackend":
        if self._model is not None:
            return self
        try:
            import torch
            from transformers import AutoProcessor
        except ImportError as exc:
            raise ImportError(
                "The Qwen backend needs torch and transformers. Install a CUDA build of "
                "torch and a transformers version that ships Qwen2_5_VL "
                "(>= 4.49 or install from source)."
            ) from exc

        try:
            from transformers import Qwen2_5_VLForConditionalGeneration as ModelCls
        except ImportError as exc:
            raise ImportError(
                "transformers {} does not expose Qwen2_5_VLForConditionalGeneration. "
                "Upgrade transformers (pip install -U transformers, or install from "
                "git+https://github.com/huggingface/transformers)."
                .format(getattr(__import__('transformers'), '__version__', '?'))
            ) from exc

        dtype = {
            "bfloat16": torch.bfloat16, "bf16": torch.bfloat16,
            "float16": torch.float16, "fp16": torch.float16,
            "float32": torch.float32, "fp32": torch.float32,
            "auto": "auto",
        }.get(str(self.torch_dtype).lower(), torch.bfloat16)

        kwargs: Dict[str, Any] = {"device_map": self.device_map}
        # `torch_dtype` was renamed to `dtype`; pass whichever this version takes.
        import inspect
        try:
            sig = inspect.signature(ModelCls.from_pretrained)
            dtype_key = "dtype" if "dtype" in sig.parameters else "torch_dtype"
        except (TypeError, ValueError):
            dtype_key = "torch_dtype"
        kwargs[dtype_key] = dtype

        if self.trust_remote_code:
            kwargs["trust_remote_code"] = True
        if self.attn_implementation:
            kwargs["attn_implementation"] = self.attn_implementation
        if self.load_in_4bit:
            try:
                from transformers import BitsAndBytesConfig
                kwargs["quantization_config"] = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    bnb_4bit_quant_type="nf4",
                )
                kwargs.pop(dtype_key, None)
            except Exception as exc:
                LOG.warning("4-bit requested but bitsandbytes is unavailable (%s); "
                            "loading in %s instead.", exc, dtype)

        LOG.info("Loading %s (%s)", self.model_id, {k: str(v) for k, v in kwargs.items()})
        try:
            self._model = ModelCls.from_pretrained(self.model_id, **kwargs)
        except Exception as exc:
            if self.attn_implementation and "flash" in str(self.attn_implementation):
                LOG.warning("flash_attention_2 load failed (%s); retrying with the "
                            "default attention implementation.", exc)
                kwargs.pop("attn_implementation", None)
                self.attn_implementation = None
                self._model = ModelCls.from_pretrained(self.model_id, **kwargs)
            else:
                raise
        self._model.eval()

        proc_kwargs: Dict[str, Any] = {
            "min_pixels": self.min_pixels,
            "max_pixels": self.max_pixels,
        }
        if self.trust_remote_code:
            proc_kwargs["trust_remote_code"] = True
        if self.use_fast_processor:
            proc_kwargs["use_fast"] = True
        try:
            self._processor = AutoProcessor.from_pretrained(self.model_id, **proc_kwargs)
        except TypeError:
            proc_kwargs.pop("use_fast", None)
            self._processor = AutoProcessor.from_pretrained(self.model_id, **proc_kwargs)

        if getattr(self._processor, "tokenizer", None) is not None:
            tok = self._processor.tokenizer
            if tok.pad_token_id is None and tok.eos_token_id is not None:
                tok.pad_token = tok.eos_token
            # Left padding is required for correct batched decoder-only generation.
            tok.padding_side = "left"

        try:
            from qwen_vl_utils import process_vision_info
            self._process_vision_info = process_vision_info
        except ImportError:
            LOG.warning(
                "qwen_vl_utils is not installed; falling back to passing PIL images "
                "directly to the processor. Install it with "
                "`pip install qwen-vl-utils==0.0.8` for the officially supported path."
            )
            self._process_vision_info = None

        try:
            self._device = str(next(self._model.parameters()).device)
        except Exception:
            self._device = "cuda" if torch.cuda.is_available() else "cpu"
        LOG.info("Model ready on %s (max_pixels=%d px / %d visual tokens)",
                 self._device, self.max_pixels, self.max_pixels // PATCH_AREA)
        return self

    def unload(self) -> None:
        self._model = None
        self._processor = None
        free_gpu()

    # -- generation ---------------------------------------------------------
    def generate(
        self,
        prompt: str,
        images: Optional[Sequence[Any]] = None,
        max_new_tokens: Optional[int] = None,
        system: Optional[str] = None,
        max_pixels_override: Optional[int] = None,
        **kwargs: Any,
    ) -> VLMResponse:
        """Single-sample generation with in-call OOM degradation.

        Returns a VLMResponse whose `meta` records any degradation applied, so a
        sample that only succeeded at a reduced pixel budget is identifiable in
        the results.
        """
        self.load()
        imgs: List[Any] = [im for im in (images or []) if im is not None]
        budget = int(max_pixels_override or self.max_pixels)
        degradations: List[str] = []

        attempt = 0
        last_exc: Optional[BaseException] = None
        while attempt < 4:
            attempt += 1
            try:
                return self._generate_once(
                    prompt, imgs, max_new_tokens or self.max_new_tokens,
                    system or DEFAULT_SYSTEM, budget, degradations,
                )
            except (KeyboardInterrupt, SystemExit):
                raise
            except BaseException as exc:  # noqa: BLE001
                last_exc = exc
                if not is_oom(exc):
                    raise
                free_gpu()
                if budget > self.min_pixels_floor:
                    budget = max(self.min_pixels_floor, budget // 2)
                    degradations.append("max_pixels->{}".format(budget))
                    LOG.warning("OOM; retrying at max_pixels=%d (%d visual tokens)",
                                budget, budget // PATCH_AREA)
                    continue
                if len(imgs) > 1:
                    imgs = imgs[:1]
                    degradations.append("dropped_to_1_image")
                    LOG.warning("OOM at the pixel floor; retrying with a single image.")
                    continue
                break

        assert last_exc is not None
        raise last_exc

    def _generate_once(
        self,
        prompt: str,
        imgs: List[Any],
        max_new_tokens: int,
        system: str,
        max_pixels: int,
        degradations: List[str],
    ) -> VLMResponse:
        import torch

        content: List[Dict[str, Any]] = []
        for im in imgs:
            entry: Dict[str, Any] = {"type": "image", "image": im}
            # Per-message pixel bounds; qwen_vl_utils honours these and they
            # override the processor defaults for this call only.
            entry["min_pixels"] = min(self.min_pixels, max_pixels)
            entry["max_pixels"] = max_pixels
            content.append(entry)
        content.append({"type": "text", "text": prompt})

        messages = []
        if system:
            messages.append({"role": "system",
                             "content": [{"type": "text", "text": system}]})
        messages.append({"role": "user", "content": content})

        text = self._processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        if self._process_vision_info is not None:
            image_inputs, video_inputs = self._process_vision_info(messages)
        else:
            image_inputs, video_inputs = (imgs or None), None

        inputs = self._processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self._device)

        n_prompt = int(inputs["input_ids"].shape[-1])
        pixels = _count_pixels(image_inputs)

        gen_kwargs: Dict[str, Any] = {
            "max_new_tokens": int(max_new_tokens),
            "do_sample": self.do_sample,
        }
        if self.do_sample:
            gen_kwargs["temperature"] = self.temperature
            gen_kwargs["top_p"] = self.top_p
        pad_id = getattr(getattr(self._processor, "tokenizer", None), "pad_token_id", None)
        if pad_id is not None:
            gen_kwargs["pad_token_id"] = pad_id

        t0 = time.perf_counter()
        with torch.inference_mode():
            out_ids = self._model.generate(**inputs, **gen_kwargs)
        latency = time.perf_counter() - t0

        trimmed = out_ids[:, inputs["input_ids"].shape[-1]:]
        n_completion = int(trimmed.shape[-1])
        decoded = self._processor.batch_decode(
            trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        answer = (decoded[0] if decoded else "").strip()

        return VLMResponse(
            text=answer,
            prompt_tokens=n_prompt,
            completion_tokens=n_completion,
            n_images=len(imgs),
            pixels=pixels,
            latency_s=latency,
            truncated=n_completion >= int(max_new_tokens),
            meta={
                "max_pixels": max_pixels,
                "degradations": list(degradations),
                "attn": self.attn_implementation,
            },
        )

    def describe(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_stub": False,
            "model_id": self.model_id,
            "torch_dtype": self.torch_dtype,
            "attn_implementation": self.attn_implementation,
            "min_pixels": self.min_pixels,
            "max_pixels": self.max_pixels,
            "min_visual_tokens": self.min_pixels // PATCH_AREA,
            "max_visual_tokens": self.max_pixels // PATCH_AREA,
            "do_sample": self.do_sample,
            "max_new_tokens": self.max_new_tokens,
            "load_in_4bit": self.load_in_4bit,
            "qwen_vl_utils": self._process_vision_info is not None,
        }


def _count_pixels(image_inputs: Any) -> int:
    """Total pixels actually handed to the vision tower (post-resize).

    This is the budget variable for the compute-matched comparison, so it is
    measured rather than assumed.
    """
    if not image_inputs:
        return 0
    total = 0
    items = image_inputs if isinstance(image_inputs, (list, tuple)) else [image_inputs]
    for im in items:
        try:
            size = getattr(im, "size", None)
            if size and len(size) == 2:
                total += int(size[0]) * int(size[1])
                continue
            shape = getattr(im, "shape", None)
            if shape is not None and len(shape) >= 2:
                total += int(shape[-1]) * int(shape[-2])
        except Exception:
            continue
    return total
