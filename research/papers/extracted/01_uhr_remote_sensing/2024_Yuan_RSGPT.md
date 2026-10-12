# Machine Extraction: RSGPT: Remote Sensing Vision-Language Pretraining with Multi-Scale Instruction Tuning

- **BibTeX Key**: `yuan2024rsgpt`
- **Authors**: Zhiqiang Yuan, Wanying Xu, Xiao Xiang, Lichao Mou
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2407.12033](https://arxiv.org/abs/2407.12033)
- **Code**: https://github.com/TUM-LMF/RSGPT
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
Remote sensing imagery exhibits drastic scale variations due to differing sensor altitudes and resolutions. RSGPT introduces multi-scale instruction tuning, bridging satellite and aerial resolutions within an aligned vision-language space.

## Key Empirical Findings
1. Multi-scale instruction tuning improves cross-sensor generalization by +9.1%.
2. Performance on fine targets degrades if scale embeddings are omitted.

## Authors' Stated Conclusions
Ground sample distance (GSD) must be explicitly parameterized in vision-language models.

## Open Challenges & Future Scope
Continuous scale representation and dynamic token allocation.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: Scale-Aware MLP
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
