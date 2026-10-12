# Machine Extraction: DINO: DETR with Improved DeNoising Anchor Boxes for End-to-End Object Detection

- **BibTeX Key**: `zhang2024dino`
- **Authors**: Hao Zhang, Feng Li, Shilong Liu, Lei Zhang, Hang Su, Jun Zhu, Lionel M. Ni, Heung-Yeung Shum
- **Venue**: ICLR 2023 (2023)
- **arXiv**: [2203.03605](https://arxiv.org/abs/2203.03605)
- **Code**: https://github.com/IDEA-Research/DINO
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Detection Architecture)

## Abstract
We present DINO (DETR with Improved deNoising anchor boxes). By using contrastive denoising training, mixed query selection, and look-forward-twice box refinement, DINO achieves 63.3 AP on COCO, setting the gold standard for transformer detectors.

## Key Empirical Findings
1. Contrastive denoising stabilizes bipartite matching during training.
2. Anchor box initialization accelerates convergence.
3. Exceptional precision on dense and clustered targets.

## Authors' Stated Conclusions
Anchor-guided query initialization with contrastive denoising stabilizes transformer detection.

## Open Challenges & Future Scope
Open-vocabulary vision-language pretraining (achieved in Grounding DINO).

## Architectural Profile
- **Vision**: Swin-L with Deformable Attention
- **Projector**: DINO Decoder (900 queries)
- **LLM**: None
- **Tokens**: 900 queries
