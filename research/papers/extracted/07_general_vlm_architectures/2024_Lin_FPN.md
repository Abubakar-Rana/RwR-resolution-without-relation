# Machine Extraction: Feature Pyramid Networks for Object Detection

- **BibTeX Key**: `lin2024fpn`
- **Authors**: Tsung-Yi Lin, Piotr Dollar, Ross Girshick, Kaiming He, Bharath Hariharan, Serge Belongie
- **Venue**: CVPR 2017 (2017)
- **arXiv**: [1612.03144](https://arxiv.org/abs/1612.03144)
- **Code**: https://github.com/facebookresearch/detectron2
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Multi-Scale Architecture)

## Abstract
Feature pyramids are a basic component in recognition systems. We present Feature Pyramid Networks (FPN), exploiting the inherent multi-scale hierarchical pyramid of deep convolutional networks to construct feature pyramids with marginal extra computation.

## Key Empirical Findings
1. Top-down feature propagation enriches high-resolution shallow layers with deep semantics.
2. Lateral connections preserve fine spatial coordinates.
3. Foundational architecture of modern object detection and dense perception.

## Authors' Stated Conclusions
Combining top-down semantic pathways with lateral high-resolution skip connections is essential for multi-scale perception.

## Open Challenges & Future Scope
Feature pyramids in pure vision transformers.

## Architectural Profile
- **Vision**: ResNet-50 with Top-Down FPN
- **Projector**: Lateral 1x1 convs
- **LLM**: None
- **Tokens**: Multi-scale feature maps
