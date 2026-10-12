# Machine Extraction: Spatial-Preserving Token Pruning for High-Resolution Transformers

- **BibTeX Key**: `qiu2024spatialtokenpruning`
- **Authors**: Yuan Qiu, Siyuan Li, Di Wu
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2407.19201](https://arxiv.org/abs/2407.19201)
- **Code**: https://github.com/ZJU-Qiu/SpatialPrune
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Unstructured token pruning destroys 2D spatial adjacency, scrambling relative positional encodings. We introduce Spatial-Preserving Token Pruning (SPTP), which constrains token reduction to regular spatial strides (e.g. 2x2 or 3x3 block pooling), preserving intact 2D topology.

## Key Empirical Findings
1. Unstructured token dropping scrambles 2D RoPE positional encodings, degrading spatial relation tasks.
2. Structured strided pruning maintains intact 2D spatial coordinate frames.
3. Retains 98.5% spatial relational reasoning accuracy under 75% token reduction.

## Authors' Stated Conclusions
Structured spatial pruning is essential to prevent positional encoding breakdown in transformers.

## Open Challenges & Future Scope
Adaptive striding based on local density.

## Architectural Profile
- **Vision**: ViT with 2D-RoPE
- **Projector**: Strided Block Pooling
- **LLM**: Qwen2-7B
- **Tokens**: Pruned by 4x via strided blocks
