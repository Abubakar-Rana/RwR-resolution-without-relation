# Machine Extraction: Look Closer to See Better: Recurrent Zoom in Visual Question Answering

- **BibTeX Key**: `ren2024lookcloser`
- **Authors**: Jianing Ren, Mengdi Wang, Chen Sun
- **Venue**: ICLR 2024 (2024)
- **arXiv**: [2310.08584](https://arxiv.org/abs/2310.08584)
- **Code**: https://github.com/brown-vl/LookCloser
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Algorithmic Relevance)

## Abstract
We formulate high-resolution visual question answering as an entropy-driven recurrent zoom process. The model starts at low resolution and recurrently zooms into informative regions until prediction entropy is minimized.

## Key Empirical Findings
1. Entropy thresholding prevents unnecessary zoom on simple questions (saves 40% compute).
2. Improves fine object recognition significantly.
3. Sequential recurrent loops increase latency on hard items.

## Authors' Stated Conclusions
Entropy-based confidence thresholding provides an effective early-exit trigger.

## Open Challenges & Future Scope
Non-recurrent feedforward zoom gating.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Recurrent Bounding Box Head
- **Projector**: MLP
- **LLM**: LLaMA-7B
- **Tokens**: Variable
