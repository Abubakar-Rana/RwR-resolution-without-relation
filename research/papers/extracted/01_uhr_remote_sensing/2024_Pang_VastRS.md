# Machine Extraction: VastRS: Visual Instruction Tuning for Gigapixel Remote Sensing

- **BibTeX Key**: `pang2024vastrs`
- **Authors**: Jian Pang, Zichen Guo, Fangrun Wang, Wen Yang
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2409.15844](https://arxiv.org/abs/2409.15844)
- **Code**: https://github.com/WHU-USI/VastRS
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
Training multimodal LLMs directly on gigapixel remote sensing images induces prohibitive GPU memory consumption. VastRS introduces a pyramid token sampling scheme that reduces visual tokens by 70% while maintaining dense semantic supervision.

## Key Empirical Findings
1. Pyramid feature sampling reduces visual tokens by 70% while preserving fine object recognition.
2. Directly training on high-res instruction data improves fine-grained attribute classification.

## Authors' Stated Conclusions
Multi-scale token pruning during pre-training stabilizes gigapixel VLM fine-tuning.

## Open Challenges & Future Scope
Inference-time dynamic routing and open-vocabulary detection.

## Architectural Profile
- **Vision**: InternViT-6B with Pyramid Sampling
- **Projector**: Pixel Shuffle MLP
- **LLM**: Qwen2-7B-Instruct
- **Tokens**: 1,024 tokens
