# Machine Extraction: H2RSVLM: Towards High-Resolution and Hybrid Remote Sensing Vision-Language Models

- **BibTeX Key**: `zhang2024h2rsvlm`
- **Authors**: Zhiqiang Zhang, Xiao Xiang, Wanying Xu, Lichao Mou
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2403.13098](https://arxiv.org/abs/2403.13098)
- **Code**: https://github.com/TUM-LMF/H2RSVLM
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
To balance global context and local detail in remote sensing, H2RSVLM introduces a dual-path architecture that feeds a low-resolution downscaled image and selected high-resolution crops into separate cross-attention layers before the LLM backbone.

## Key Empirical Findings
1. Dual-path hybrid encoding outperforms naive tiling by +6.8% on complex scene QA.
2. Preserves overall scene category while allowing fine object identification.

## Authors' Stated Conclusions
Global and local features must be fused hierarchically rather than concatenated blindly.

## Open Challenges & Future Scope
Adaptive selection of high-resolution crop locations.

## Architectural Profile
- **Vision**: Dual ViT-L/14 (Global + Local)
- **Projector**: Cross-attention Resampler
- **LLM**: Vicuna-7B
- **Tokens**: 1,536 tokens
