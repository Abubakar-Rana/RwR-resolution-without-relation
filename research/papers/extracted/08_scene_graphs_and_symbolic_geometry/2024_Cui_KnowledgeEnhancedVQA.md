# Machine Extraction: Knowledge-Enhanced Visual Question Answering via Graph Routing

- **BibTeX Key**: `cui2024knowledgeenhancedvqa`
- **Authors**: Jiaxi Cui, Bin Lin, Li Yuan
- **Venue**: ACL 2024 (2024)
- **arXiv**: [2405.09840](https://arxiv.org/abs/2405.09840)
- **Code**: https://github.com/PKU-YuanGroup/GraphRouteVQA
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 3 / 5 (Moderate Routing Prior)

## Abstract
Injecting entire knowledge graphs into LLM context introduces noise and distracts reasoning. We introduce Graph-Routed VQA, which dynamically prunes knowledge graphs to retain only 1-hop and 2-hop subgraphs relevant to queried entities.

## Key Empirical Findings
1. Pruning irrelevant graph edges is essential; full graphs act as distracting noise in LLM prompts.
2. 1-hop and 2-hop relevant subgraphs improve answer accuracy by +9.2%.
3. Confirms that unstructured text graph serialization introduces semantic distraction.

## Authors' Stated Conclusions
Graph information must be aggressively filtered; unpruned graphs degrade reasoning via prompt distraction.

## Open Challenges & Future Scope
Adaptive subgraph pruning thresholds.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: Graph Router + MLP
- **LLM**: LLaMA-2-7B-Chat
- **Tokens**: Pruned graph prompt tokens
