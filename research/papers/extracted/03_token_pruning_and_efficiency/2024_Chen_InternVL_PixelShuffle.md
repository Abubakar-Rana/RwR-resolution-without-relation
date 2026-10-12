# Machine Extraction: InternVL: Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks

- **BibTeX Key**: `chen2024internvlpixelshuffle`
- **Authors**: Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Zhong Muyan, Qinglong Zhang, Xizhou Zhu, Lewei Lu, Tong Lu, Ping Luo, Yu Qiao, Jifeng Dai
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2312.14238](https://arxiv.org/abs/2312.14238)
- **Code**: https://github.com/OpenGVLab/InternVL
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 5 / 5 (Foundational VLM Architecture)

## Abstract
We present InternVL, scaling vision foundation models to 6B parameters and aligning them with large language models. InternVL introduces a Pixel Shuffle downsampling projector that groups 2x2 spatial patches into channels, reducing visual token sequence length by 4x while strictly maintaining 2D spatial topology.

## Key Empirical Findings
1. Pixel Shuffle 2x2 downsampling reduces visual tokens from 1,024 to 256 per tile (75% reduction).
2. Strictly maintains 2D spatial adjacency, avoiding the coordinate corruption of parametric resamplers.
3. Enables InternVL to process up to 12 dynamic tiles within standard LLM context windows.

## Authors' Stated Conclusions
Pixel Shuffle is the gold standard for spatial-preserving visual token compression in multi-crop VLMs.

## Open Challenges & Future Scope
Adaptive pixel shuffle scales based on target density.

## Architectural Profile
- **Vision**: InternViT-6B-448
- **Projector**: Pixel Shuffle (2x2 downsample) + Two-layer MLP
- **LLM**: InternLM2-20B / Qwen-7B
- **Tokens**: 256 tokens per 448x448 tile
