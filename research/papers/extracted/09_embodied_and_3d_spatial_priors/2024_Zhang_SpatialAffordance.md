# Machine Extraction: Spatial Affordance Grounding in Embodied Multimodal Models

- **BibTeX Key**: `zhang2024spatialaffordance`
- **Authors**: Haotian Zhang, Boyuan Chen, Fei Xia
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2407.16789](https://arxiv.org/abs/2407.16789)
- **Code**: https://spatial-affordance.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Moderate Embodied Prior)

## Abstract
We explore spatial affordance grounding in multimodal models. Rather than generating text coordinates, our model generates spatial heatmaps directly over image pixels, indicating feasible action regions with spatial confidence.

## Key Empirical Findings
1. Spatial heatmaps over pixels are easier for vision models to predict than text coordinate strings.
2. Continuous heatmaps capture uncertainty naturally.
3. Downstream controllers sample execution points from heatmap peaks.

## Authors' Stated Conclusions
Spatial heatmaps over visual pixels provide a vastly superior interface for spatial localization than autoregressive coordinate tokens.

## Open Challenges & Future Scope
Multi-task affordance learning.

## Architectural Profile
- **Vision**: ViT-L with Heatmap Decoder
- **Projector**: Deconvolutional Upsampler
- **LLM**: PaLM-2
- **Tokens**: Native
