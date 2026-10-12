# Machine Extraction: Cross-Scale Grounding: Open-Vocabulary Aerial Object Localization

- **BibTeX Key**: `chen2024crossscalegrounding`
- **Authors**: Pengfei Chen, Liang Zhao, Bo Du
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2408.13450](https://arxiv.org/abs/2408.13450)
- **Code**: https://github.com/WHU-Geo/CrossScaleGrounding
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We introduce Cross-Scale Grounding for remote sensing referring expression comprehension. By matching language tokens against multi-scale visual feature pyramids, our model resolves scale ambiguities (e.g. distinguishing a small building from a large storage tank).

## Key Empirical Findings
1. Multi-scale feature alignment improves referring expression accuracy on aerial scenes by +13.8%.
2. Disambiguates scale-sensitive targets through context comparison.
3. Preserves relative coordinate offsets across scales.

## Authors' Stated Conclusions
Grounding aerial objects requires cross-scale feature comparison to establish physical scale context.

## Open Challenges & Future Scope
Integration into conversational MLLMs.

## Architectural Profile
- **Vision**: Swin-B with Cross-Scale Alignment
- **Projector**: Cross-Attention Head
- **LLM**: RoBERTa (Text encoder)
- **Tokens**: N/A
