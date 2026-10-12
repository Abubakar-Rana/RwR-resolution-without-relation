# Machine Extraction: Simple Open-Vocabulary Object Detection with Vision Transformers

- **BibTeX Key**: `minderer2024owlvit`
- **Authors**: Matthias Minderer, Alexey Gritsenko, Austin Stone, Maxim Neumann, Dirk Weissenborn, Alexey Dosovitskiy, Aravindh Mahendran, Anurag Arnab, Mostafa Dehghani, Zhai Xiaohua, Thomas Kipf, Neil Houlsby
- **Venue**: ECCV 2022 (2022)
- **arXiv**: [2205.06230](https://arxiv.org/abs/2205.06230)
- **Code**: https://github.com/google-research/scenic/tree/main/scenic/projects/owl_vit
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (High Open-Vocabulary Prior)

## Abstract
We present OWL-ViT, demonstrating that standard Vision Transformers pretrained with image-text contrastive objectives can be transferred directly to open-vocabulary object detection with minimal architectural modifications.

## Key Empirical Findings
1. Removing classification token pooling unlocks dense spatial patch features in pretrained CLIP.
2. Lightweight MLP heads perform open-vocabulary detection from image-level pretraining.
3. Simple, highly scalable open-vocabulary detector architecture.

## Authors' Stated Conclusions
Standard CLIP backbones contain strong spatial localization signals that can be tapped with simple linear heads.

## Open Challenges & Future Scope
Self-training on web images (achieved in OWLv2).

## Architectural Profile
- **Vision**: CLIP ViT-B/16 & ViT-L/14
- **Projector**: MLP Box & Class Heads
- **LLM**: CLIP Text Encoder
- **Tokens**: Dense patch tokens
