# Machine Extraction: SkySense: A Multi-Modal Remote Sensing Foundation Model Towards Universal Geospatial Understanding

- **BibTeX Key**: `guo2024skysense`
- **Authors**: Zichen Guo, Wei Zhang, Xinmin Liu, Yuanbo Rao, Jingdong Wang
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2312.10115](https://arxiv.org/abs/2312.10115)
- **Code**: https://github.com/ant-research/SkySense
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We present SkySense, a multi-modal remote sensing foundation model with billions of parameters. SkySense scales across spatial resolutions from 0.5m to 30m, temporal cadences, and synthetic aperture radar (SAR) modalities, achieving SOTA on 16 benchmark tasks.

## Key Empirical Findings
1. Multi-granularity pre-training captures both tiny object features and landscape-level topography.
2. Scales visual representations effectively across varying GSD (ground sample distance).

## Authors' Stated Conclusions
Foundation models pre-trained on diverse aerial scales show superior cross-scale feature stability.

## Open Challenges & Future Scope
Integration into conversational instruction-following LLMs.

## Architectural Profile
- **Vision**: SkySense Swin-V2-Large / ViT-Giant
- **Projector**: Linear projection
- **LLM**: None
- **Tokens**: Variable
