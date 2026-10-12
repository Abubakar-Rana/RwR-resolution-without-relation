# Machine Extraction: GigaRS: Gigapixel Remote Sensing Image Captioning and QA

- **BibTeX Key**: `ding2025gigars`
- **Authors**: Jian Ding, Yihua Wang, Gui-Song Xia
- **Venue**: arXiv preprint (2025)
- **arXiv**: [2502.04119](https://arxiv.org/abs/2502.04119)
- **Code**: https://github.com/CAP-GigaRS/GigaRS
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
Gigapixel remote sensing images pose unique challenges where scene narratives span kilometers while target objects occupy meters. GigaRS establishes a benchmark for gigapixel captioning and VQA with hierarchical multi-tier annotations.

## Key Empirical Findings
1. Monolithic VLMs fail completely on gigapixel images without hierarchical decomposition.
2. Hierarchical decomposition preserves both landscape context and object details.

## Authors' Stated Conclusions
Hierarchical multi-tier representation is mandatory for imagery exceeding 10K resolution.

## Open Challenges & Future Scope
Automated hierarchical planning and token compression.

## Architectural Profile
- **Vision**: Hierarchical Swin-L
- **Projector**: Resampler
- **LLM**: Qwen-7B
- **Tokens**: 4,096 tokens
