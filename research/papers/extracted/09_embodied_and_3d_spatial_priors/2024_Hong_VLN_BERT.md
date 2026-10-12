# Machine Extraction: VLN-BERT: A Recurrent Vision-and-Language Navigation Model

- **BibTeX Key**: `hong2024vlnbert`
- **Authors**: Yicong Hong, Qi Wu, Yuankai Qi, Cristian Rodriguez-Opazo, Stephen Gould
- **Venue**: CVPR 2021 (2021)
- **arXiv**: [2011.13922](https://arxiv.org/abs/2011.13922)
- **Code**: https://github.com/YicongHong/Recurrent-VLN-BERT
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Moderate VLN Prior)

## Abstract
Standard transformers lack recurrent memory across long sequential trajectories. Recurrent VLN-BERT incorporates a recurrent state token that persists across navigation steps, maintaining temporal and spatial trajectory context.

## Key Empirical Findings
1. Recurrent state tokens maintain spatial navigation history across long paths.
2. Cross-modal attention between language instructions and panoramic visual candidate nodes.
3. SOTA navigation success rate on Room-to-Room benchmark.

## Authors' Stated Conclusions
Maintaining a persistent recurrent spatial state is necessary for tracking long-horizon trajectories.

## Open Challenges & Future Scope
Continuous action spaces.

## Architectural Profile
- **Vision**: ViT / ResNet panoramic features
- **Projector**: Multi-layer cross-attention
- **LLM**: BERT-Base with Recurrent State Token
- **Tokens**: Panorama nodes + state token
