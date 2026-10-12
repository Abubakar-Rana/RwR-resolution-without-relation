# Machine Extraction: Scaling Open-Vocabulary Object Detection

- **BibTeX Key**: `minderer2024owlv2`
- **Authors**: Matthias Minderer, Alexey Gritsenko, Neil Houlsby
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2306.09683](https://arxiv.org/abs/2306.09683)
- **Code**: https://github.com/google-research/scenic/tree/main/scenic/projects/owl_vit
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (High Open-Vocabulary Prior)

## Abstract
We scale open-vocabulary detection by self-training on large, diverse web datasets. We use an existing detector to generate pseudo-annotations on unannotated images, creating a large-scale training corpus that dramatically boosts zero-shot detection.

## Key Empirical Findings
1. Web-scale self-training improves zero-shot detection by +7.2 AP over OWL-ViT.
2. Exceptional generalization to rare and domain-specific object classes.
3. Strong performance on aerial infrastructure categories.

## Authors' Stated Conclusions
Large-scale self-training closes the domain gap for open-vocabulary detection.

## Open Challenges & Future Scope
Interactive video grounding.

## Architectural Profile
- **Vision**: CLIP ViT-L/14 with Self-Training
- **Projector**: MLP heads
- **LLM**: CLIP Text Encoder
- **Tokens**: Dense grid
