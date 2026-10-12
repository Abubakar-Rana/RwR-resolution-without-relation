# Machine Extraction: Spatial Consistency Probing in Large Multimodal Models

- **BibTeX Key**: `liu2024spatialconsistency`
- **Authors**: Shuai Liu, Kexin Cheng, Xiang Bai
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2407.16540](https://arxiv.org/abs/2407.16540)
- **Code**: https://github.com/HUST-VL/SpatialConsistency
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 3 / 5 (Moderate Diagnostic Prior)

## Abstract
We evaluate spatial consistency in MLLMs using symmetric and transitive question pairs. Across 10 top models, we find that models contradict their own answers in 42% of spatial queries, revealing that spatial answers are generated from ungrounded token probability distributions rather than consistent mental models.

## Key Empirical Findings
1. 42% internal contradiction rate on inverse spatial questions ('A is left of B' vs 'B is right of A').
2. Models lack a unified spatial coordinate model.
3. Contradictions occur even when visual perception of individual objects is correct.

## Authors' Stated Conclusions
Autoregressive generation does not enforce transitive or symmetric spatial constraints.

## Open Challenges & Future Scope
Constraint-guided decoding for spatial consistency.

## Architectural Profile
- **Vision**: Evaluates 10 MLLMs
- **Projector**: Native
- **LLM**: Various
- **Tokens**: Native
