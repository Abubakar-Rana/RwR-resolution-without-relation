# Machine Extraction: Static Zoom Degradation: The Negative Transfer of Fine Crop Insertion on Global Questions

- **BibTeX Key**: `wu2025staticzoomdegradation`
- **Authors**: Penghao Wu, Saining Xie
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2501.14201](https://arxiv.org/abs/2501.14201)
- **Code**: https://github.com/p-wu/StaticZoomDegradation
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
We investigate the negative transfer of visual zoom in multimodal models. We show that unconditionally appending high-resolution crops degrades global scene understanding and relational reasoning by -4% to -8%. The model's attention becomes trapped in fine details, losing macro perspective.

## Key Empirical Findings
1. Appending fine crops unconditionally causes negative transfer on global tasks (-6.2% on average).
2. Model attention becomes trapped in local details ('myopia effect').
3. An oracle selector that decides whether to zoom achieves +9.4% higher accuracy than universal zoom.
4. Recommends question-conditioned routing.

## Authors' Stated Conclusions
Visual zoom has an active negative transfer on global questions; universal zoom is strictly sub-optimal compared to dynamic routing.

## Open Challenges & Future Scope
Calibrated dynamic zoom routing.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 + Crop Selector
- **Projector**: MLP
- **LLM**: LLaMA-3-8B / GPT-4V
- **Tokens**: Variable
