# Machine Extraction: Inductive Representation Learning on Large Graphs

- **BibTeX Key**: `hamilton2024graphsage`
- **Authors**: William L. Hamilton, Rex Ying, Jure Leskovec
- **Venue**: NeurIPS 2017 (2017)
- **arXiv**: [1706.02216](https://arxiv.org/abs/1706.02216)
- **Code**: https://github.com/williamleif/GraphSAGE
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 3 / 5 (Foundational Inductive GNN)

## Abstract
We present GraphSAGE, an inductive framework for representation learning on large graphs. Instead of training individual embeddings for each node, GraphSAGE learns aggregator functions that generalize to previously unseen nodes and subgraphs.

## Key Empirical Findings
1. Inductive neighborhood sampling generalizes to unseen nodes and entire new graphs.
2. Scales to massive graphs with millions of nodes.
3. Essential for dynamic visual graphs where object counts vary between scenes.

## Authors' Stated Conclusions
Inductive neighborhood aggregation enables graph models to generalize across dynamic, variable-sized visual scenes.

## Open Challenges & Future Scope
Multi-relational inductive learning.

## Architectural Profile
- **Vision**: None
- **Projector**: N/A
- **LLM**: GraphSAGE Aggregators (Mean, Pool, LSTM)
- **Tokens**: Node embeddings
