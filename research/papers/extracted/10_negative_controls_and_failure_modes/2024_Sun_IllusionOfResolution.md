# Machine Extraction: The Illusion of Resolution: Why More Pixels Do Not Automatically Yield Spatial Reasoning

- **BibTeX Key**: `sun2024illusionofresolution`
- **Authors**: Yabo Sun, Zhang Li, Xiang Bai
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2407.18210](https://arxiv.org/abs/2407.18210)
- **Code**: https://github.com/HUST-VL/ResolutionIllusion
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
We challenge the assumption that resolution scaling monotonically improves vision-language model capabilities. Across 8 models, we show that while object recognition accuracy scales with resolution, spatial relational reasoning plateaus at low resolutions (448px) and systematically degrades at higher resolutions due to context fragmentation.

## Key Empirical Findings
1. Object recognition scales monotonically with resolution ($R^2 = 0.94$).
2. Spatial relational reasoning plateaus at 448px and degrades by -5.2% at 1344px ($R^2 = -0.81$).
3. Establishes the exact empirical divergence between perception scaling and relational scaling.
4. Co-authors term this divergent phenomenon the 'Resolution Illusion'.

## Authors' Stated Conclusions
Resolution scaling is fundamentally asymmetric: it monotonically aids perception but impairs spatial relational reasoning.

## Open Challenges & Future Scope
Dual-scale resolution architectures.

## Architectural Profile
- **Vision**: Evaluates 8 MLLMs across 224, 448, 672, 896, 1344 resolutions
- **Projector**: Native
- **LLM**: Various
- **Tokens**: Variable
