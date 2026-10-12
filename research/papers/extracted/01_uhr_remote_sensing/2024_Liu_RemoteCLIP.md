# Machine Extraction: RemoteCLIP: A Vision Language Foundation Model for Remote Sensing

- **BibTeX Key**: `liu2024remoteclip`
- **Authors**: Fan Liu, Delong Chen, Zhangyang Wang, Fayao Liu
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2306.11029](https://arxiv.org/abs/2306.11029)
- **Code**: https://github.com/ChenDelong1999/RemoteCLIP
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
Vision-language foundation models like CLIP exhibit poor zero-shot performance in Earth observation due to domain divergence in scale, perspective, and semantics. RemoteCLIP solves this via pre-training on 800K remote sensing image-caption pairs curated through automated scaling and expert filtering.

## Key Empirical Findings
1. RemoteCLIP outperforms standard CLIP by +18.4% zero-shot classification on aerial benchmarks.
2. Delivers robust semantic text-to-tile alignment for overhead search.

## Authors' Stated Conclusions
Overhead visual features require domain-aligned contrastive representations.

## Open Challenges & Future Scope
Multimodal LLM integration and dynamic tile selection scoring.

## Architectural Profile
- **Vision**: RemoteCLIP ViT-L/14
- **Projector**: Cosine similarity head
- **LLM**: None (Encoder only)
- **Tokens**: N/A
