# Machine Extraction: DeepSeek-VL: Towards Real-World Vision-Language Understanding

- **BibTeX Key**: `deepseek2024deepseekvl`
- **Authors**: Haishi Lu, Zhenda Xie, Zhewei Yao, Chong Ruan, Xiaokang Yang
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2403.05534](https://arxiv.org/abs/2403.05534)
- **Code**: https://github.com/deepseek-ai/DeepSeek-VL
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We present DeepSeek-VL, an open-source vision-language model. DeepSeek-VL processes high-resolution images (1024x1024) via a hybrid vision encoder that combines a low-level CNN encoder with a high-level ViT encoder, achieving high performance on real-world vision tasks.

## Key Empirical Findings
1. Hybrid CNN + ViT architecture captures both fine high-frequency textures and global semantics.
2. Convolutional branch retains sharp edge coordinates for small objects.
3. Balances compute by allocating 576 tokens for 1024x1024 resolution.

## Authors' Stated Conclusions
Hybrid convolutional and transformer encoders provide the best balance of fine-grained spatial acuity and semantic abstraction.

## Open Challenges & Future Scope
Scaling to 4K+ resolutions.

## Architectural Profile
- **Vision**: Hybrid: SAM-B (CNN, 1024x1024) + SigLIP (ViT, 384x384)
- **Projector**: MLP Resampler
- **LLM**: DeepSeek-7B
- **Tokens**: 576 tokens
