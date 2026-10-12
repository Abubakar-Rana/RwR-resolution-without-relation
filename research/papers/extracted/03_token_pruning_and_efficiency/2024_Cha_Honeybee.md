# Machine Extraction: Honeybee: Locality-Enhanced Projector for Multimodal LLMs

- **BibTeX Key**: `cha2024honeybee`
- **Authors**: Junbum Cha, Wooyoung Kang, Jonghwan Mun, Byungseok Roh
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2312.06742](https://arxiv.org/abs/2312.06742)
- **Code**: https://github.com/kakaobrain/honeybee
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Visual projectors in MLLMs often flatten 2D features into 1D sequences, destroying spatial inductive biases. Honeybee introduces the C-Abstractor, a projector incorporating depthwise convolutions to maintain 2D spatial locality while compressing visual tokens.

## Key Empirical Findings
1. Preserving 2D spatial locality during token compression outperforms 1D resamplers by +5.4%.
2. Convolutional locality enables superior fine-grained localization.
3. Balances token efficiency with spatial precision.

## Authors' Stated Conclusions
2D convolutional operations are superior to 1D attention for maintaining spatial layout in multimodal projectors.

## Open Challenges & Future Scope
Multi-scale convolutional abstractors for ultra-high-resolution.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: C-Abstractor (Depthwise Conv + Cross-Attention)
- **LLM**: Vicuna-7B
- **Tokens**: Compressed to 144 tokens (4x reduction)
