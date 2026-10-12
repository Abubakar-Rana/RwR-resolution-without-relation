# Machine Extraction: Cross-Scale Feature Pooling for Efficient Visual Reasoning

- **BibTeX Key**: `zhu2024crossscalepooling`
- **Authors**: Zicong Zhu, Peijin Wang, Xian Sun
- **Venue**: IEEE GRSL 2024 (2024)
- **arXiv**: [2408.06190](https://arxiv.org/abs/2408.06190)
- **Code**: https://github.com/AIR-CAS/CrossScalePool
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
We explore cross-scale feature pooling for remote sensing imagery. By pooling features from multi-resolution feature pyramids into a shared token space, our model captures both micro targets and macro geographic layout.

## Key Empirical Findings
1. Multi-scale pooling outperforms single-scale pooling by +4.6% on aerial scene classification.
2. Reduces token count by 3x compared to dense tiling.

## Authors' Stated Conclusions
Multi-scale feature pooling captures multi-granularity aerial semantics efficiently.

## Open Challenges & Future Scope
Multimodal conversational reasoning.

## Architectural Profile
- **Vision**: Swin-B
- **Projector**: Pyramid Pooling
- **LLM**: None
- **Tokens**: N/A
