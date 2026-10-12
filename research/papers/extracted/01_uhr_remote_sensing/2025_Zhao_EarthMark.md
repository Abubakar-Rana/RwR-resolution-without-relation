# Machine Extraction: EarthMark: Grounded Remote Sensing Multi-Task Vision-Language Model

- **BibTeX Key**: `zhao2025earthmark`
- **Authors**: Liang Zhao, Pengfei Chen, Haoyu Dong, Bo Du
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2501.07823](https://arxiv.org/abs/2501.07823)
- **Code**: https://github.com/WHU-Geo/EarthMark
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
Grounding objects in remote sensing via text coordinates is error-prone. EarthMark overlays visual mark identifiers directly onto detected buildings, ships, and roads, enabling the language model to reference specific physical objects unambiguously in dialogue.

## Key Empirical Findings
1. Visual mark prompts increase spatial relational reasoning accuracy by +12.4% over text bounding box coordinates.
2. Eliminates coordinate hallucination in complex aerial scenes.

## Authors' Stated Conclusions
Marking objects directly on pixel canvases sidesteps the language model's coordinate parsing deficit.

## Open Challenges & Future Scope
Automating real-time open-vocabulary mark generation on gigapixel images.

## Architectural Profile
- **Vision**: Qwen-VL visual encoder with visual prompt overlays
- **Projector**: MLP
- **LLM**: Qwen-VL-Chat
- **Tokens**: 1,024 tokens
