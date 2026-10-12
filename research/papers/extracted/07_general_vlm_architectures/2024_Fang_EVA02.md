# Machine Extraction: EVA-02: A New Turn for Vision Transformers

- **BibTeX Key**: `fang2024eva02`
- **Authors**: Yuxin Fang, Quan Sun, Xinggang Wang, Tiejun Huang, Zhaoxiang Zhang, Yue Cao
- **Venue**: ICLR 2024 (2024)
- **arXiv**: [2303.11331](https://arxiv.org/abs/2303.11331)
- **Code**: https://github.com/baaivision/EVA
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Vision Backbone)

## Abstract
We present EVA-02, an advanced vision transformer architecture. By incorporating SwiGLU activations, sub-LayerNorm, and scaled masked image modeling pre-training, EVA-02 sets a new milestone in visual representation learning across classification, detection, and segmentation.

## Key Empirical Findings
1. SwiGLU feedforward networks significantly improve representation capacity in vision transformers.
2. Masked image modeling preserves high-frequency edge details better than pure contrastive learning.
3. Excellent transfer to dense aerial detection.

## Authors' Stated Conclusions
Modern architectural enhancements (SwiGLU, sub-LN) stabilize large vision transformer pretraining and enhance edge localization.

## Open Challenges & Future Scope
Multimodal pretraining integration.

## Architectural Profile
- **Vision**: EVA-02-CLIP-E/14 (4.4B parameters)
- **Projector**: Linear / MLP
- **LLM**: None
- **Tokens**: Native
