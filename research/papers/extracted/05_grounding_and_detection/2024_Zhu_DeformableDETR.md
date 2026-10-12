# Machine Extraction: Deformable DETR: Deformable Transformers for End-to-End Object Detection

- **BibTeX Key**: `zhu2024deformabledetr`
- **Authors**: Xizhou Zhu, Weijie Su, Lewei Lu, Bin Li, Xiaogang Wang, Jifeng Dai
- **Venue**: ICLR 2021 (2021)
- **arXiv**: [2010.04159](https://arxiv.org/abs/2010.04159)
- **Code**: https://github.com/fundamentalvision/Deformable-DETR
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Detection Architecture)

## Abstract
We propose Deformable DETR. Its deformable attention module focuses on a small, sparse set of sampling points around reference points, enabling multi-scale feature processing at high resolution with linear computational complexity.

## Key Empirical Findings
1. Multi-scale deformable attention processes high-resolution feature maps efficiently.
2. Boosts small object detection by +10.5 AP over vanilla DETR.
3. Converges 10x faster than standard DETR.

## Authors' Stated Conclusions
Sparse deformable attention is essential for processing high-resolution visual features without quadratic compute explosion.

## Open Challenges & Future Scope
Open-vocabulary grounding.

## Architectural Profile
- **Vision**: ResNet-50 + Multi-Scale Deformable Attention
- **Projector**: Deformable Transformer Decoder
- **LLM**: None
- **Tokens**: 300 queries
