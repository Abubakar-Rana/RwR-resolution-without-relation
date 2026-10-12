# Machine Extraction: EarthVQA: Towards Relational Reasoning for Remote Sensing Visual Question Answering

- **BibTeX Key**: `chen2024earthvqa`
- **Authors**: Pengfei Chen, Liang Zhao, Zhenghua Chen, Bo Du
- **Venue**: ISPRS Journal 2024 (2024)
- **arXiv**: [2403.11902](https://arxiv.org/abs/2403.11902)
- **Code**: https://github.com/ChenPF-Geo/EarthVQA
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 4 / 5 (High Relational Prior)

## Abstract
Conventional remote sensing VQA benchmarks disproportionately focus on simple object presence or category recognition. We introduce EarthVQA, a benchmark and relational framework specifically evaluating multi-hop spatial relationships, cardinal geometry, and topological containment in aerial scenes.

## Key Empirical Findings
1. Standard VLMs drop by over 25% when queries shift from object existence to spatial relations.
2. Relational accuracy depends heavily on uncorrupted global coordinate context.

## Authors' Stated Conclusions
Spatial relation questions demand holistic topological representation rather than isolated object patches.

## Open Challenges & Future Scope
Hierarchical graph reasoning combined with high-resolution visual tokens.

## Architectural Profile
- **Vision**: Swin-B
- **Projector**: Cross-Attention
- **LLM**: LLaMA-7B
- **Tokens**: 1,024 tokens
