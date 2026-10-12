# Machine Extraction: LHRS-Bot: Empowering Remote Sensing with Vision-Language Models

- **BibTeX Key**: `muhtar2024lhrsbot`
- **Authors**: Diliyaer Muhtar, Zhenshi Li, Feng Gu, Xueliang Lu, Pengfeng Xiao
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2402.02544](https://arxiv.org/abs/2402.02544)
- **Code**: https://github.com/NJU-LHRS/LHRS-Bot
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
We present LHRS-Bot, a multi-modal conversational model designed for Earth observation. LHRS-Bot incorporates hierarchical semantic descriptions and fine-grained visual features to address complex geospatial queries.

## Key Empirical Findings
1. Multi-level geospatial prompts improve attribute recognition.
2. Hallucinations rise when small targets are not resolved in the visual input.

## Authors' Stated Conclusions
Instruction tuning requires high-quality multi-turn geospatial conversations.

## Open Challenges & Future Scope
Active zooming and efficient token budgeting.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Vicuna-13B
- **Tokens**: 576 tokens
