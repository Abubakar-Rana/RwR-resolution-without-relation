# Machine Extraction: Spatial-Bench: Benchmarking Spatial Understanding and Cardinal Reasoning in Vision-Language Models

- **BibTeX Key**: `cheng2024spatialbench`
- **Authors**: Kexin Cheng, Ziyang Chen, Yuliang Liu, Xiang Bai
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2406.14120](https://arxiv.org/abs/2406.14120)
- **Code**: https://github.com/HUST-VL/SpatialBench
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Diagnostic Prior)

## Abstract
Evaluating spatial understanding in MLLMs is hindered by benchmark contamination and confounding semantic shortcuts. Spatial-Bench introduces 12,000 controlled queries isolating 8 spatial capabilities across natural, synthetic, and aerial imagery, rigorously testing cardinal and topological reasoning.

## Key Empirical Findings
1. Frontier models score <35% on cardinal directions (north, south, east, west) across aerial imagery.
2. Models frequently confuse left/right with east/west due to lack of geographic coordinate anchoring.
3. Performance collapses further when images are flipped or rotated.

## Authors' Stated Conclusions
VLMs lack grounded cardinal orientation systems; spatial answers are heavily confounded by linguistic priors.

## Open Challenges & Future Scope
Cardinal-aware visual position encodings.

## Architectural Profile
- **Vision**: Evaluates 15 open-source and proprietary VLMs
- **Projector**: Native
- **LLM**: Various
- **Tokens**: Native
