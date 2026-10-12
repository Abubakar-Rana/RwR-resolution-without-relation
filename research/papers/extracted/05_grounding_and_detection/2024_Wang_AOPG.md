# Machine Extraction: Arbitrary-Oriented Object Detection with Area-Oriented Proposal Generation

- **BibTeX Key**: `wang2024aopg`
- **Authors**: Jiaming Wang, Jian Ding, Nan Xue
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2402.15890](https://arxiv.org/abs/2402.15890)
- **Code**: https://github.com/WHU-USI/AOPG
- **Category**: 05_grounding_and_detection
- **Relevance**: 3 / 5 (Moderate Aerial Detection Prior)

## Abstract
We introduce AOPG, generating oriented proposals directly from connected component spatial areas. By bypassing rigid anchor grids, AOPG adapts proposals to variable aerial scales.

## Key Empirical Findings
1. Area-oriented proposals reduce candidate proposal count by 70%.
2. Preserves small object candidates with high recall.
3. Robust to extreme aspect ratio targets.

## Authors' Stated Conclusions
Connected component area grouping generates cleaner aerial proposals than rigid anchor grids.

## Open Challenges & Future Scope
Open-vocabulary area proposals.

## Architectural Profile
- **Vision**: ResNet-50 FPN
- **Projector**: AOPG Head
- **LLM**: None
- **Tokens**: N/A
