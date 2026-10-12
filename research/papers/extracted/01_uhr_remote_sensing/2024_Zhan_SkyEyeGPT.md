# Machine Extraction: SkyEyeGPT: Large Multimodal Model for Remote Sensing Vision-Language Tasks

- **BibTeX Key**: `zhan2024skyeyegpt`
- **Authors**: Yuan Zhan, Zhitong Xiong, Yuan Yuan
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2401.09712](https://arxiv.org/abs/2401.09712)
- **Code**: https://github.com/NWPU-SkyEye/SkyEyeGPT
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
Objects in Earth observation imagery appear in arbitrary orientations. SkyEyeGPT integrates oriented bounding box coordinates into autoregressive token generation, supporting rotated object detection and referring expression comprehension.

## Key Empirical Findings
1. Standard horizontal bounding boxes cause massive overlap in dense aerial parking lots.
2. Oriented coordinates $(x, y, w, h, 	heta)$ improve spatial grounding in overhead images.

## Authors' Stated Conclusions
Oriented representations are critical for overhead objects with high aspect ratios.

## Open Challenges & Future Scope
Scaling to gigapixel imagery and reducing autoregressive coordinate latency.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: Linear
- **LLM**: LLaMA-7B
- **Tokens**: 576 tokens
