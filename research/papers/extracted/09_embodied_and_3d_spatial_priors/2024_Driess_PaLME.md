# Machine Extraction: PaLM-E: An Embodied Multimodal Language Model

- **BibTeX Key**: `driess2024palme`
- **Authors**: Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Awtar Gondhalekar, Carolina Parada, Kanishka Rao, Pierre Sermanet, Mengyuan Yan, Stefan Welker, et al.
- **Venue**: ICML 2023 (2023)
- **arXiv**: [2303.03378](https://arxiv.org/abs/2303.03378)
- **Code**: https://palm-e.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (Foundational Embodied Prior)

## Abstract
We present PaLM-E, an embodied multimodal language model that ingests continuous sensor modalities directly into a language model. PaLM-E performs sequential robotic manipulation planning, visual question answering, and tabletop spatial reasoning.

## Key Empirical Findings
1. Ingesting continuous state vectors directly into the language embedding space preserves physical metric coordinates.
2. Scale matters: 562B model exhibits emergent multi-modal spatial transfer.
3. Preserves linguistic reasoning without catastrophic forgetting.

## Authors' Stated Conclusions
Continuous spatial grounding vectors enable language models to understand physical real-world spatial environments.

## Open Challenges & Future Scope
Ultra-high-resolution visual exploration.

## Architectural Profile
- **Vision**: ViT-22B + Sensor State Encoders
- **Projector**: Linear Projection
- **LLM**: PaLM (540B)
- **Tokens**: Continuous sensor tokens
