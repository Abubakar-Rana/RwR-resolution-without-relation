# Machine Extraction: CLEVR: A Diagnostic Dataset for Compositional Language and Reasoning

- **BibTeX Key**: `goyal2024clevr`
- **Authors**: Justin Johnson, Bharath Hariharan, Laurens van der Maaten, Li Fei-Fei, C. Lawrence Zitnick, Ross Girshick
- **Venue**: CVPR 2017 (2017)
- **arXiv**: [1612.06890](https://arxiv.org/abs/1612.06890)
- **Code**: https://cs.stanford.edu/people/jcjohns/clevr/
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (Foundational Compositional Benchmark)

## Abstract
We introduce CLEVR, a diagnostic dataset for compositional language and elementary visual reasoning. CLEVR isolates reasoning abilities via synthetic 3D scenes and procedural questions that require counting, spatial relations, and attribute comparison.

## Key Empirical Findings
1. Synthetic compositional questions prevent language priors from acting as shortcuts.
2. Spatial relations ('left of', 'behind') require explicit compositional execution graphs.
3. End-to-end neural models struggle without explicit modular reasoning structures.

## Authors' Stated Conclusions
Compositional spatial reasoning requires modular execution steps rather than flat associative pattern matching.

## Open Challenges & Future Scope
Real-world scaling of compositional reasoning.

## Architectural Profile
- **Vision**: ResNet / FiLM / MAC
- **Projector**: FiLM conditioning
- **LLM**: None (Pre-LLM era)
- **Tokens**: N/A
