# Machine Extraction: Out of the Box: Reasoning with Knowledge Graphs for VQA

- **BibTeX Key**: `narasimhan2024outofthebox`
- **Authors**: Medhini Narasimhan, Svetlana Lazebnik, Alexander G. Schwing
- **Venue**: CVPR 2018 (2018)
- **arXiv**: [1811.00538](https://arxiv.org/abs/1811.00538)
- **Code**: https://github.com/medhini/OutOfTheBox
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 3 / 5 (Moderate Graph Prior)

## Abstract
Answering visual questions frequently requires knowledge beyond the visual pixels. We introduce a framework that integrates external knowledge graphs with visual representations, querying relevant factual subgraphs using graph attention.

## Key Empirical Findings
1. External knowledge graphs ground abstract visual concepts in factual knowledge.
2. Graph attention routes queries to relevant factual subgraphs.
3. Prevents hallucination of factual contradictions.

## Authors' Stated Conclusions
Graph-structured external knowledge enhances visual question answering robustness.

## Open Challenges & Future Scope
Integration into modern foundation LLMs.

## Architectural Profile
- **Vision**: Faster R-CNN
- **Projector**: Graph Attention over ConceptNet
- **LLM**: None
- **Tokens**: N/A
