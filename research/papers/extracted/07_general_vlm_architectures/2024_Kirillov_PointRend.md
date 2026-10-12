# Machine Extraction: PointRend: Image Segmentation as Rendering

- **BibTeX Key**: `kirillov2024pointrend`
- **Authors**: Alexander Kirillov, Yuxin Wu, Kaiming He, Ross Girshick
- **Venue**: CVPR 2020 (2020)
- **arXiv**: [1912.08193](https://arxiv.org/abs/1912.08193)
- **Code**: https://github.com/facebookresearch/detectron2
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Adaptive Sampling)

## Abstract
We present PointRend, viewing image segmentation as a rendering problem. PointRend performs adaptive subdivision, sampling only a non-uniform set of points along uncertain object boundaries, computing crisp high-resolution edge masks at a fraction of the memory.

## Key Empirical Findings
1. Non-uniform point sampling computes high-resolution boundaries without uniform grid explosion.
2. Allocates compute strictly where boundary uncertainty is highest.
3. Inspires adaptive visual token sampling along object borders.

## Authors' Stated Conclusions
Adaptive point subdivision renders fine details efficiently by concentrating compute on uncertain boundary regions.

## Open Challenges & Future Scope
Adaptive point sampling in vision transformers.

## Architectural Profile
- **Vision**: ResNet-50 + FPN + PointRend Head
- **Projector**: Point MLP
- **LLM**: None
- **Tokens**: Adaptive point tokens
