# Machine Extraction: Improved Baselines with Visual Instruction Tuning

- **BibTeX Key**: `liu2023llava15`
- **Authors**: Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, Yong Jae Lee
- **Venue**: CVPR 2024 (2023)
- **arXiv**: [2310.03744](https://arxiv.org/abs/2310.03744)
- **Code**: https://github.com/haotian-liu/LLaVA
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational VLM Architecture)

## Abstract
We present LLaVA-1.5, incorporating simple modifications to the original LLaVA: replacing the linear projector with a two-layer MLP, scaling resolution to 336x336, and incorporating academic VQA datasets into instruction tuning.

## Key Empirical Findings
1. Two-layer MLP projector improves multimodal representation over linear layer (+4.2%).
2. 336px resolution improves OCR and small detail perception.
3. Canonical open-weights baseline evaluated across thousands of papers.

## Authors' Stated Conclusions
A two-layer MLP projector and modest resolution scaling significantly improve open-source VLM capability.

## Open Challenges & Future Scope
Dynamic resolution and multi-crop tiling (realized in LLaVA-NeXT).

## Architectural Profile
- **Vision**: CLIP ViT-L/14-336
- **Projector**: Two-layer MLP (GELU)
- **LLM**: Vicuna-7B-v1.5 / Vicuna-13B-v1.5
- **Tokens**: 576 tokens
