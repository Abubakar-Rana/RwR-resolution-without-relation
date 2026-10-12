# Machine Extraction: Semi-Supervised Classification with Graph Convolutional Networks

- **BibTeX Key**: `kipf2024gcn`
- **Authors**: Thomas N. Kipf, Max Welling
- **Venue**: ICLR 2017 (2017)
- **arXiv**: [1609.02907](https://arxiv.org/abs/1609.02907)
- **Code**: https://github.com/tkipf/gcn
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (Foundational Graph Neural Network)

## Abstract
We present a scalable approach for semi-supervised learning on graph-structured data based on an efficient localized first-order approximation of spectral graph convolutions. Our GCN model scales linearly in graph edges and learns localized structural representations.

## Key Empirical Findings
1. Localized graph convolution scales linearly in the number of edges $\mathcal{O}(|E|)$.
2. First-order spectral approximation aggregates 1-hop neighbor features efficiently.
3. Foundational architecture of modern Graph Neural Networks.

## Authors' Stated Conclusions
Spectral graph convolutions can be approximated via simple localized spatial message passing.

## Open Challenges & Future Scope
Attention-based dynamic edge weighting (realized in GAT).

## Architectural Profile
- **Vision**: None
- **Projector**: N/A
- **LLM**: GCN Layers
- **Tokens**: Graph node embeddings
