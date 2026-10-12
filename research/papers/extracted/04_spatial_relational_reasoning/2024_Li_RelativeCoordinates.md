# Machine Extraction: Relative Coordinate Embeddings for Grounded Multimodal Transformers

- **BibTeX Key**: `li2024relativecoordinates`
- **Authors**: Zhenshi Li, Diliyaer Muhtar, Xueliang Lu
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2405.04112](https://arxiv.org/abs/2405.04112)
- **Code**: https://github.com/NJU-LHRS/RelCoord
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We demonstrate that predicting absolute bounding coordinates $[x_1, y_1, x_2, y_2]$ is inherently difficult for autoregressive LLMs due to scale sensitivity. We propose Relative Coordinate Embeddings (RelCoord), parameterizing object locations as relative displacement vectors from anchor landmarks.

## Key Empirical Findings
1. Relative coordinates improve spatial reasoning by +11.8% over absolute coordinates.
2. Reduces coordinate token hallucination.
3. Aligns with human spatial description conventions ('50 meters north of the tower').

## Authors' Stated Conclusions
Relative displacement from landmark anchors is far more robust than absolute pixel coordinates.

## Open Challenges & Future Scope
Automated landmark selection in remote sensing.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: Relative MLP
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
