# Machine Extraction: SatChat: Satellite Imagery Reasoning with Grounded Tokens

- **BibTeX Key**: `ma2024satchat`
- **Authors**: Qiang Ma, Dong Wang, Zichen Guo, Wen Yang
- **Venue**: IEEE GRSL 2024 (2024)
- **arXiv**: [2405.14320](https://arxiv.org/abs/2405.14320)
- **Code**: https://github.com/WHU-USI/SatChat
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
We explore region-grounded conversation in satellite imagery. SatChat prepends visual region tokens to language embeddings to allow conversational grounding of high-resolution structures.

## Key Empirical Findings
1. Region token conditioning improves targeted captioning.
2. Latency grows linearly with the number of queried regions.

## Authors' Stated Conclusions
Dedicated region tokens bridge the gap between global image context and local objects.

## Open Challenges & Future Scope
Dynamic token gating.

## Architectural Profile
- **Vision**: ViT-L/14 with RoIAlign
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: 800 tokens
