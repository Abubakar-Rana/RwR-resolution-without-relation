# Machine Extraction: Investigating Spatial Reasoning Blind Spots in Vision-Language Models

- **BibTeX Key**: `patel2024blindspotsinspatial`
- **Authors**: Mitesh Patel, Arpit Sharma, David Doermann
- **Venue**: CVPRW 2024 (2024)
- **arXiv**: [2404.15201](https://arxiv.org/abs/2404.15201)
- **Code**: https://github.com/UB-Vision/SpatialBlindSpots
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 3 / 5 (Moderate Diagnostic Prior)

## Abstract
We dissect the pipeline of modern MLLMs to identify where spatial information is lost. We show that early image resizing distorts aspect ratios, patch tokenization removes sub-patch coordinates, and transformer pooling flattens relational distance vectors.

## Key Empirical Findings
1. Resizing non-square aerial images into square 336x336 inputs distorts angles by up to 35 degrees.
2. Sub-patch coordinate information is completely unrecoverable after initial patch projection.
3. Deep attention heads exhibit uniform attention over spatial distance.

## Authors' Stated Conclusions
Spatial distortion starts at image preprocessing and is magnified throughout transformer layers.

## Open Challenges & Future Scope
Aspect-ratio-preserving tokenization.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
