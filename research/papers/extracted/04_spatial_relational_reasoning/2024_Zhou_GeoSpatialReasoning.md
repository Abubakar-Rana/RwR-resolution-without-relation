# Machine Extraction: Cardinal and Distance Reasoning in Aerial Visual Question Answering

- **BibTeX Key**: `zhou2024geospatialreasoning`
- **Authors**: Yong Zhou, Fangrun Wang, Wen Yang
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2407.09812](https://arxiv.org/abs/2407.09812)
- **Code**: https://github.com/WHU-USI/GeoSpatialVQA
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We investigate how image downscaling alters geometric perception in remote sensing VQA. We find that downscaling non-linearly distorts perceived spatial density, leading models to overestimate distances and misjudge cardinal relationships between clustered targets.

## Key Empirical Findings
1. Downscaling distorts spatial density, causing models to systematically overestimate distances between clustered objects.
2. Tiling restores local distances but completely destroys global cardinal reference points.
3. Identifies the exact trade-off between local distance fidelity and global cardinal reference.

## Authors' Stated Conclusions
Neither downscaling nor tiling alone preserves both metric distance fidelity and cardinal orientation.

## Open Challenges & Future Scope
Unified dual-scale coordinate calibration.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Qwen-VL
- **Tokens**: 1,024 tokens
