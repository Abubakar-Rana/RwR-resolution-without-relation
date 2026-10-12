# Machine Extraction: SparseVLM: Visual Token Sparsification for Efficient Multimodal LLMs

- **BibTeX Key**: `liu2024sparsevlm`
- **Authors**: Yuan Liu, Siyuan Huang, Tianhe Ren, Junyi Chen
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2410.04512](https://arxiv.org/abs/2410.04512)
- **Code**: https://github.com/THU-Sparse/SparseVLM
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Efficiency Prior)

## Abstract
High-resolution MLLMs face severe memory pressure. SparseVLM introduces a spatial-aware token sparsification projector that clusters redundant visual tokens while protecting high-frequency boundary tokens essential for localization.

## Key Empirical Findings
1. Spatial boundary tokens are critical for object localization and must not be pruned.
2. Clustering background patches cuts visual tokens by 60% without hurting perception.
3. Preserves bounding box coordinate regression accuracy.

## Authors' Stated Conclusions
Selective preservation of spatial boundary tokens maintains localization performance under token compression.

## Open Challenges & Future Scope
Adaptive cluster numbers per image.

## Architectural Profile
- **Vision**: SigLIP-SO400M
- **Projector**: Boundary-Aware Clustering Resampler
- **LLM**: Llama-3-8B-Instruct
- **Tokens**: Variable (Compressed from 2,304 to 768 tokens)
