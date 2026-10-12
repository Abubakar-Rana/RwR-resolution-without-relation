# Machine Extraction: Qwen2-VL: Enhancing Vision-Language Model with Dynamic Resolution NaViT

- **BibTeX Key**: `bai2024qwen2vl`
- **Authors**: Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, Jingren Zhou
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2409.12191](https://arxiv.org/abs/2409.12191)
- **Code**: https://github.com/QwenLM/Qwen2-VL
- **Category**: 02_active_zoom_and_search
- **Relevance**: 5 / 5 (Foundational VLM Architecture)

## Abstract
We present Qwen2-VL, capable of processing images of dynamically varying resolutions and aspect ratios without fixed patch limits. By introducing 2D-RoPE and native resolution tokenization, Qwen2-VL achieves SOTA on visual understanding, document parsing, and high-resolution video reasoning.

## Key Empirical Findings
1. Dynamic resolution enables native comprehension of diverse image shapes without resizing blur.
2. M-RoPE models temporal, horizontal, and vertical dimensions simultaneously.
3. Serves as the primary 7B backbone in our RwR baseline experiments.

## Authors' Stated Conclusions
Dynamic resolution processing with 2D-RoPE represents the premier vision-language architecture.

## Open Challenges & Future Scope
Handling gigapixel remote sensing images without sequence length explosion.

## Architectural Profile
- **Vision**: NaViT ViT-600M (Dynamic Resolution)
- **Projector**: Pixel Shuffle 2x2 downsampler
- **LLM**: Qwen2-7B-Instruct
- **Tokens**: Variable (1 token per 28x28 pixels)
