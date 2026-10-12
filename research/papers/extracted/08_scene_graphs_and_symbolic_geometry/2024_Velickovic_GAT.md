# Machine Extraction: Graph Attention Networks

- **BibTeX Key**: `velickovic2024gat`
- **Authors**: Petar Velickovic, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Lio, Yoshua Bengio
- **Venue**: ICLR 2018 (2018)
- **arXiv**: [1710.10903](https://arxiv.org/abs/1710.10903)
- **Code**: https://github.com/PetarV-/GAT
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (Foundational Graph Attention)

## Abstract
We present Graph Attention Networks (GAT), introducing masked self-attention to graph-structured data. By calculating dynamic attention weights over neighboring nodes, GAT enables anisotropic message passing without computationally expensive matrix operations.

## Key Empirical Findings
1. Self-attention over graph neighbors allows anisotropic feature aggregation.
2. Preserves spatial orientation between connected nodes by weighting directional neighbors differently.
3. Foundational graph attention mechanism.

## Authors' Stated Conclusions
Attention mechanisms dynamically modulate message passing strength across distinct relational graph edges.

## Open Challenges & Future Scope
Edge-featured graph attention.

## Architectural Profile
- **Vision**: None
- **Projector**: N/A
- **LLM**: GAT Layers with Multi-Head Attention
- **Tokens**: Node embeddings
