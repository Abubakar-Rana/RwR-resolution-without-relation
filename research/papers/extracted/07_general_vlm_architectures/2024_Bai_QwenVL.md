# Machine Extraction: Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, and Text Reading

- **BibTeX Key**: `bai2024qwenvl`
- **Authors**: Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, Jingren Zhou
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2308.12966](https://arxiv.org/abs/2308.12966)
- **Code**: https://github.com/QwenLM/Qwen-VL
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational VLM Architecture)

## Abstract
We introduce Qwen-VL, a comprehensive vision-language model. Qwen-VL integrates high-resolution visual processing (448x448) via a cross-attention visual resampler, supporting grounding, OCR, and multi-turn conversation with specialized bounding box tokens.

## Key Empirical Findings
1. Cross-attention resampler compresses visual tokens from 1,024 to 256.
2. Specialized coordinate tokens format bounding boxes as `(x1, y1), (x2, y2)`.
3. Outperformed open-source peers on visual grounding and document comprehension.

## Authors' Stated Conclusions
Visual resamplers balance token efficiency and visual perception for high-resolution images.

## Open Challenges & Future Scope
Dynamic resolution and native aspect ratios (realized in Qwen2-VL).

## Architectural Profile
- **Vision**: Openclip ViT-bigG
- **Projector**: Cross-Attention Resampler (256 tokens)
- **LLM**: Qwen-7B
- **Tokens**: 256 tokens
