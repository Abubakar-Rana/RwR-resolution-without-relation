# Machine Extraction: Graph-Structured Representations for Visual Question Answering

- **BibTeX Key**: `teney2024graphvqa`
- **Authors**: Damien Teney, Lingqiao Liu, Anton van den Hengel
- **Venue**: CVPR 2017 (2017)
- **arXiv**: [1611.05600](https://arxiv.org/abs/1611.05600)
- **Code**: https://github.com/aimets/graph-vqa
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (Foundational Graph VQA)

## Abstract
We present a framework for VQA that builds graph-structured representations of both the image and the question. By performing graph matching between the visual scene graph and question dependency tree, our model solves multi-hop relational queries.

## Key Empirical Findings
1. Dual graph matching (visual graph matched to language parse tree) handles multi-hop relational questions.
2. Preserves structural isomorphism between question grammar and visual layout.
3. Outperformed monolithic CNN-LSTM baselines by +8.2% on relational VQA.

## Authors' Stated Conclusions
Aligning visual scene graphs with linguistic parse trees provides robust compositional reasoning.

## Open Challenges & Future Scope
Modernizing with foundation model transformers.

## Architectural Profile
- **Vision**: R-CNN + Spatial Graph Builder
- **Projector**: Graph Neural Network
- **LLM**: None
- **Tokens**: N/A
