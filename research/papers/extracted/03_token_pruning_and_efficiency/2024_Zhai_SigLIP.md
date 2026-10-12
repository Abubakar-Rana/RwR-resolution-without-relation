# Machine Extraction: Sigmoid Loss for Language-Image Pre-Training

- **BibTeX Key**: `zhai2024siglip`
- **Authors**: Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, Lucas Beyer
- **Venue**: ICCV 2023 (2024)
- **arXiv**: [2303.15343](https://arxiv.org/abs/2303.15343)
- **Code**: https://github.com/google-research/big_vision
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 5 / 5 (Foundational Vision Encoder)

## Abstract
We propose SigLIP, using a simple pairwise sigmoid loss for language-image pre-training. Unlike standard contrastive learning with softmax normalization over the full batch, sigmoid loss operates on image-text pairs independently, scaling efficiently and improving zero-shot classification and fine-grained localization.

## Key Empirical Findings
1. SigLIP-SO400M outperforms CLIP-ViT-L on dense localization and fine-grained classification.
2. More stable feature embeddings across varying aspect ratios and resolutions.
3. Standard visual encoder in modern SOTA VLMs (PaliGemma, Qwen2.5-VL).

## Authors' Stated Conclusions
Pairwise sigmoid loss produces superior spatial and fine-grained visual representations compared to softmax CLIP.

## Open Challenges & Future Scope
Scaling to gigapixel imagery and video foundation models.

## Architectural Profile
- **Vision**: SigLIP-SO400M / ViT-B-16
- **Projector**: Linear projection
- **LLM**: None
- **Tokens**: Native
