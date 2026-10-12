# Machine Extraction: Spurious Correlations in Vision-Language Pre-training: A Spatial Case Study

- **BibTeX Key**: `patel2024spuriouscorrelationsvlm`
- **Authors**: Mitesh Patel, Arpit Sharma, David Doermann
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2403.11290](https://arxiv.org/abs/2403.11290)
- **Code**: https://github.com/UB-Vision/SpuriousSpatial
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 3 / 5 (Diagnostic Failure Analysis)

## Abstract
We investigate spurious spatial correlations in vision-language models. Models frequently rely on pre-trained semantic priors (e.g., sky is above, ground is below) to guess spatial answers, leading to systematic failure on nadir aerial imagery where all objects exist on an orthographic 2D plane.

## Key Empirical Findings
1. Pretrained models possess strong vertical bias ('above'/'below') learned from gravity in web images.
2. Fails in nadir satellite imagery where 'above' is interpreted as 'North' but model treats it as vertical elevation.
3. Semantic categories carry spurious directional priors (e.g. 'planes are above clouds').

## Authors' Stated Conclusions
Terrestrial gravity biases in pre-trained models confound nadir 2D aerial spatial reasoning.

## Open Challenges & Future Scope
Gravity-invariant aerial pretraining.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
