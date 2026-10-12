# Machine Extraction: SpatialQA: Evaluating 2D and 3D Spatial Knowledge in Large Language Models

- **BibTeX Key**: `wu2024spatialqa`
- **Authors**: Yuan-Hong Wu, Siyuan Huang, Tianhe Ren
- **Venue**: ACL 2024 (2024)
- **arXiv**: [2405.11890](https://arxiv.org/abs/2405.11890)
- **Code**: https://github.com/THU-Wu/SpatialQA
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 3 / 5 (Moderate Spatial Prior)

## Abstract
We evaluate spatial knowledge in LLMs and MLLMs using SpatialQA, testing coordinate conversion, topological connectivity, and mental rotation. We find that language models possess abstract geographic knowledge but fail completely on geometric spatial reasoning.

## Key Empirical Findings
1. LLMs know facts (e.g. 'Paris is north of Madrid') but fail on coordinate-based spatial calculation.
2. Multimodal models perform worse than expected when image visual cues contradict common language priors.
3. Spatial mental rotation is near chance in 7B-13B models.

## Authors' Stated Conclusions
Language models cannot perform spatial arithmetic; geometric relationships must be grounded visually or calculated symbolically.

## Open Challenges & Future Scope
Specialized spatial reasoning pretraining.

## Architectural Profile
- **Vision**: Evaluates GPT-4, LLaMA-3, Claude
- **Projector**: N/A
- **LLM**: Various
- **Tokens**: N/A
