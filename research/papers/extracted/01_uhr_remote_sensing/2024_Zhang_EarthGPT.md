# Machine Extraction: EarthGPT: A Universal Multi-Modal Large Language Model for Multi-Sensor Remote Sensing

- **BibTeX Key**: `zhang2024earthgpt`
- **Authors**: Zhenghang Zhang, Shuai Ni, Fanglong Yao, Xian Sun, Kun Fu
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2401.16822](https://arxiv.org/abs/2401.16822)
- **Code**: https://github.com/AIR-CAS/EarthGPT
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
Remote sensing encompasses multi-sensor modalities beyond standard optical RGB. EarthGPT unifies optical, SAR, and infrared modalities into a single MLLM with visual grounding and dense region captioning.

## Key Empirical Findings
1. Unified instruction tuning allows cross-sensor reasoning.
2. Visual grounding improves localization but struggles with global multi-hop relations across massive scenes.

## Authors' Stated Conclusions
Multi-sensor alignment requires robust cross-modal token projectors.

## Open Challenges & Future Scope
Handling ultra-high-resolution tiling and dynamic routing.

## Architectural Profile
- **Vision**: EVA-02-CLIP-E/14
- **Projector**: Q-Former variant
- **LLM**: Llama-2-7B-Chat
- **Tokens**: 256 tokens
