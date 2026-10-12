# Honeybee: Locality-Enhanced Projector for Multimodal LLMs

- **Authors**: Junbum Cha, Wooyoung Kang, Jonghwan Mun, Byungseok Roh
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2312.06784
- **URL**: https://arxiv.org/abs/2312.06784
- **BibTeX Key**: `cha2024honeybee`

## Abstract
The multimodal projector bridging the visual encoder and the language model plays a crucial role in Large Multimodal Models (LMMs). Existing projectors either preserve full tokens via simple MLPs (incurring heavy sequence costs) or compress tokens using abstract resamplers (destroying 2D spatial structures). We present Honeybee, an LMM family featuring locality-enhanced visual projection. We propose the Convolutional Abstractor (C-Abstractor), which incorporates 2D depthwise convolutions to maintain local geometric continuity during spatial downsampling. Honeybee achieves superior performance on vision-language benchmarks while using 4x fewer visual tokens than standard LLaVA architectures.

## Key Extracted Contributions
1. Standard Perceiver resamplers discard 2D spatial locality because cross-attention is permutation-invariant without strong positional bias.
2. C-Abstractor (using depthwise separable convolutions) retains spatial adjacency and fine boundaries while downsampling tokens by 4x.
3. Preserving spatial locality is decisive for spatial relationship and counting queries.
