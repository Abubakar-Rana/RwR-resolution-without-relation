# Source Code (`src/`)

This directory contains the production-grade, modular Python codebase for the Vision-Language Model research project.

---

## Architecture & Subpackages

- [`models/`](file:///d:/projects/research/vlm/src/models): Modular model definitions:
  - Vision Encoders (wrappers for SigLIP, DINOv2, CLIP, etc.)
  - Modality Connectors / Projectors (Linear, MLP, Perceiver, Pixel-Shuffle)
  - Unified Multimodal VLM classes
- [`evaluation/`](file:///d:/projects/research/vlm/src/evaluation): Benchmark evaluators, metrics (accuracy, CIDEr, BLEU, POPE F1), and probe harnesses.
- [`data/`](file:///d:/projects/research/vlm/src/data): Multimodal datasets, collators, dynamic resolution splitters, and preprocessing transforms.
- [`utils/`](file:///d:/projects/research/vlm/src/utils): Common utilities for logging, checkpoint loading, device management, and profiling.

---

## Standards for AI Agents

1. **Strict Type Hinting**: All functions and methods must have standard Python type annotations.
2. **Docstrings**: Adhere to Google Python Style Guide docstrings.
3. **Decoupled Architecture**: Do not tightly couple vision encoders directly to specific LLMs. Route them through abstract interfaces (e.g. `BaseVisionEncoder`, `BaseProjector`).
4. **Reproducible Code**: Avoid hardcoded magic numbers or CUDA device indices.
