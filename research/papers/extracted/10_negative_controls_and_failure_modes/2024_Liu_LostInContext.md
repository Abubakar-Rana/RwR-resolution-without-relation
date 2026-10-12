# Machine Extraction: Lost in Context: Spatial Decay and Attention Dissipation in Multimodal LLMs

- **BibTeX Key**: `liu2024lostincontext`
- **Authors**: Zhuang Liu, Shengbang Tong, Yi Ma
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2408.09871](https://arxiv.org/abs/2408.09871)
- **Code**: https://github.com/SpatialDecay/LostInContext
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
We investigate attention allocation in multi-crop high-resolution MLLMs. We discover that as visual sequence length increases, cross-modal attention dissipates non-linearly across background patches, severely diluting attention on target entities and causing spatial relational reasoning to collapse.

## Key Empirical Findings
1. Visual attention dissipates exponentially as visual token count exceeds 1,500 tokens.
2. Multi-crop tiling floods the KV cache with background tokens, diluting attention on key entities by 70%.
3. Direct mathematical cause of the spatial reasoning drop under tile selection.
4. Recommends aggressive token pruning or routing to compact overview representations.

## Authors' Stated Conclusions
Flooding the transformer with high-resolution crop tokens causes attention dissipation that destroys relational reasoning.

## Open Challenges & Future Scope
Hard attention gating for multi-crop inputs.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Multi-Crop Tiling
- **Projector**: MLP
- **LLM**: LLaVA-1.5 / Qwen-VL
- **Tokens**: 576 to 4,096 tokens
