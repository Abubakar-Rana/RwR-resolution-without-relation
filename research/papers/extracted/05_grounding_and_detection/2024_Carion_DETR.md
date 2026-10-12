# Machine Extraction: End-to-End Object Detection with Transformers

- **BibTeX Key**: `carion2024detr`
- **Authors**: Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, Sergey Zagoruyko
- **Venue**: ECCV 2020 (2020)
- **arXiv**: [2005.12872](https://arxiv.org/abs/2005.12872)
- **Code**: https://github.com/facebookresearch/detr
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Detection Architecture)

## Abstract
We present DETR, viewing object detection as a direct set prediction problem. By combining a transformer encoder-decoder with a bipartite matching loss, DETR eliminates hand-crafted components like anchor generation and non-maximum suppression.

## Key Empirical Findings
1. Set-based bipartite matching eliminates duplicate detections without hand-crafted NMS.
2. Global self-attention models relations between objects naturally.
3. Early DETR converges slowly and performs poorly on small objects due to computational limits of dense attention.

## Authors' Stated Conclusions
Direct set prediction with transformers is elegant, but standard global attention struggles with small dense targets.

## Open Challenges & Future Scope
Multi-scale attention and deformable attention for small objects (solved in Deformable DETR).

## Architectural Profile
- **Vision**: ResNet-50 + Transformer Encoder
- **Projector**: Transformer Decoder (100 object queries)
- **LLM**: None
- **Tokens**: 100 queries
