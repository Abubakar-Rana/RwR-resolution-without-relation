# Machine Extraction: RoI Transformer for Oriented Object Detection in Aerial Images

- **BibTeX Key**: `han2024roitransformer`
- **Authors**: Jiaming Han, Jian Ding, Nan Xue, Gui-Song Xia
- **Venue**: CVPR 2019 (2019)
- **arXiv**: [1812.00155](https://arxiv.org/abs/1812.00155)
- **Code**: https://github.com/dingjiansw101/RoITransformer_DOTA
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Aerial Detection)

## Abstract
Horizontal RoI pooling extracts excessive background noise on rotated aerial objects. We propose RoI Transformer, which learns spatial transformations from horizontal proposals to rotated proposals, enabling lightweight and accurate oriented object detection.

## Key Empirical Findings
1. Transforming horizontal proposals to rotated proposals improves aerial detection by +7.4 mAP.
2. Eliminates background contamination in dense ports and airfields.
3. Minimal computational overhead over standard two-stage detectors.

## Authors' Stated Conclusions
Spatial geometric transformation inside the detection head resolves rotational misalignment.

## Open Challenges & Future Scope
Single-stage oriented transformers.

## Architectural Profile
- **Vision**: ResNet-101 with FPN
- **Projector**: RoI Transformer + Rotated RoIAlign
- **LLM**: None
- **Tokens**: N/A
