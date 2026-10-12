# Machine Extraction: Masked Autoencoders Are Scalable Vision Learners

- **BibTeX Key**: `he2024maskedautoencoders`
- **Authors**: Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollar, Ross Girshick
- **Venue**: CVPR 2022 (2022)
- **arXiv**: [2111.06377](https://arxiv.org/abs/2111.06377)
- **Code**: https://github.com/facebookresearch/mae
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Self-Supervised Learning)

## Abstract
We show that masked autoencoders (MAE) are scalable self-supervised learners for computer vision. By masking a high proportion of the input image (75%) and processing only visible patches through an asymmetric encoder, MAE learns rich spatial and semantic representations.

## Key Empirical Findings
1. High masking ratio (75%) eliminates spatial redundancy and forces global semantic reasoning.
2. Asymmetric design makes encoder 4x faster during pretraining.
3. Learned representations retain rich high-frequency spatial details and pixel geometry.

## Authors' Stated Conclusions
Generative masked autoencoding pretraining forces models to learn holistic spatial layout and pixel-level topology.

## Open Challenges & Future Scope
Multimodal masked pretraining.

## Architectural Profile
- **Vision**: ViT-L/16 MAE Encoder
- **Projector**: Lightweight MAE Decoder
- **LLM**: None
- **Tokens**: Visible patches only (25%)
