# Machine Extraction: BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation

- **BibTeX Key**: `li2024blip`
- **Authors**: Junnan Li, Dongxu Li, Caiming Xiong, Steven Hoi
- **Venue**: ICML 2022 (2022)
- **arXiv**: [2201.12086](https://arxiv.org/abs/2201.12086)
- **Code**: https://github.com/salesforce/BLIP
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Pretraining Prior)

## Abstract
We present BLIP, a flexible vision-language pre-training framework that can operate as a unimodal encoder, an image-grounded text encoder, or an image-grounded text decoder. CapFilt bootstraps noisy web datasets, achieving SOTA on understanding and generation tasks.

## Key Empirical Findings
1. CapFilt synthetic caption filtering cleans noisy web datasets significantly.
2. Unified MED architecture seamlessly switches between retrieval, classification, and caption generation.
3. Establishes the standard pre-training pipeline for modern vision-language models.

## Authors' Stated Conclusions
Dataset bootstrapping and unified encoder-decoder architectures improve multimodal representation quality.

## Open Challenges & Future Scope
Pretraining on large-scale instruction mixtures (achieved in BLIP-2).

## Architectural Profile
- **Vision**: ViT-B/16 & ViT-L/16
- **Projector**: Cross-attention layers
- **LLM**: MED Transformer (220M)
- **Tokens**: Native patch tokens
