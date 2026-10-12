# Machine Extraction: ImageBind: One Embedding Space To Bind Them All

- **BibTeX Key**: `girdhar2024imagebind`
- **Authors**: Rohit Girdhar, Alaaeldin El-Nouby, Zhuang Liu, Mannat Singh, Kalyan Vasudev Alwala, Armand Joulin, Ishan Misra
- **Venue**: CVPR 2023 (2023)
- **arXiv**: [2305.05665](https://arxiv.org/abs/2305.05665)
- **Code**: https://github.com/facebookresearch/ImageBind
- **Category**: 07_general_vlm_architectures
- **Relevance**: 3 / 5 (Moderate Multi-Modal Prior)

## Abstract
We present ImageBind, binding six modalities into a single joint embedding space without requiring paired data across all modality combinations. By aligning all modalities to images, ImageBind enables emergent cross-modal capabilities.

## Key Empirical Findings
1. Images serve as a universal anchor binding diverse sensory modalities.
2. Incorporating depth maps improves 3D spatial alignment in visual embeddings.
3. Enables zero-shot cross-modal retrieval across sensors.

## Authors' Stated Conclusions
Visual representations naturally serve as the bridge for multi-sensor geospatial alignment.

## Open Challenges & Future Scope
Multi-spectral remote sensing integration.

## Architectural Profile
- **Vision**: ViT-H/14 with Modality Heads
- **Projector**: Cosine similarity heads
- **LLM**: None
- **Tokens**: Global pooled embeddings
