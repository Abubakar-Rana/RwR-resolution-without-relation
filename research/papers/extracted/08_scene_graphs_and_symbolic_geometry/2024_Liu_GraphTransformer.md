# Machine Extraction: Graph Transformer Networks for Spatial Relation Disambiguation

- **BibTeX Key**: `liu2024graphtransformer`
- **Authors**: Shuai Liu, Kexin Cheng, Xiang Bai
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2408.15670](https://arxiv.org/abs/2408.15670)
- **Code**: https://github.com/HUST-VL/GraphTransformer
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Dense visual scenes present overlapping spatial relations that confound standard transformers. We propose Graph Transformer Networks for spatial disambiguation, injecting graph shortest-path distances and 2D relative angle biases directly into transformer attention heads.

## Key Empirical Findings
1. Graph shortest-path distance bias guides attention along physical spatial adjacency.
2. Disambiguates dense object clusters where multiple objects share similar attributes.
3. Improves spatial relation accuracy by +14.8% on GQA and Spatial-Bench.

## Authors' Stated Conclusions
Graph structure bias injected into transformer attention heads effectively resolves spatial relation ambiguity.

## Open Challenges & Future Scope
Application to multimodal vision-language pretraining.

## Architectural Profile
- **Vision**: Graph Transformer with 2D Relative Angle Bias
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: 576 tokens
