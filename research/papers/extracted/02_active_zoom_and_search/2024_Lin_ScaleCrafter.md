# Machine Extraction: Multi-Scale Vision-Language Modeling via Dynamic Re-Tiling

- **BibTeX Key**: `lin2024scalecrafter`
- **Authors**: Ting Lin, Chengyuan Dong, Yufeng Cui
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2406.09450](https://arxiv.org/abs/2406.09450)
- **Code**: https://github.com/PKU-Lin/ScaleCrafter
- **Category**: 02_active_zoom_and_search
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
Static image tiling creates sharp boundary discontinuities. ScaleCrafter introduces dynamic re-tiling, shifting tile offsets during multi-pass evaluation to blend boundary features and eliminate grid seams.

## Key Empirical Findings
1. Shifting tile grids by 50% stride smooths seam boundary artifacts.
2. Boosts object detection at tile borders by +7.8%.
3. Doubles inference compute due to overlapping passes.

## Authors' Stated Conclusions
Overlapping tiles or shifted grids resolve edge seam clipping at the cost of additional compute.

## Open Challenges & Future Scope
Single-pass boundary feature blending.

## Architectural Profile
- **Vision**: Swin-Large
- **Projector**: MLP
- **LLM**: Llama-3-8B
- **Tokens**: Variable
