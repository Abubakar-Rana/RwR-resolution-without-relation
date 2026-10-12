# Machine Extraction: Crop Boundary Discontinuities: The Impact of Patch Partitioning on Relational Attention

- **BibTeX Key**: `zhao2024cropboundaryartifacts`
- **Authors**: Liang Zhao, Pengfei Chen, Bo Du
- **Venue**: IEEE GRSL 2024 (2024)
- **arXiv**: [2408.06789](https://arxiv.org/abs/2408.06789)
- **Code**: https://github.com/WHU-Geo/CropBoundaries
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Domain Analysis)

## Abstract
We analyze cross-patch attention in multi-crop remote sensing models. We discover that self-attention weights drop by over 80% across crop boundaries, treating adjacent pixels on opposite sides of a seam as unrelated entities and severing cross-crop spatial relations.

## Key Empirical Findings
1. Attention across tile seams drops by 82% compared to continuous intra-tile attention.
2. Slicing an image severs semantic and geometric connectivity in transformer attention matrices.
3. Explains why models cannot reason about spatial relationships between objects in different crops.

## Authors' Stated Conclusions
Multi-crop tiling creates an artificial attention barrier at crop boundaries that blocks relational message passing.

## Open Challenges & Future Scope
Cross-crop attention bridges.

## Architectural Profile
- **Vision**: SigLIP-SO400M with Multi-Crop Tiling
- **Projector**: MLP
- **LLM**: Qwen-VL
- **Tokens**: Multi-crop sequences
