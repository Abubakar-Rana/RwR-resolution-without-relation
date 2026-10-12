# Machine Extraction: WayPoint Graph Navigation for Embodied Vision-Language Agents

- **BibTeX Key**: `krantz2024navgraph`
- **Authors**: Jacob Krantz, Stefan Lee
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2406.12890](https://arxiv.org/abs/2406.12890)
- **Code**: https://github.com/krantz-j/NavGraph
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Moderate Navigation Prior)

## Abstract
We explore waypoint graph navigation for vision-language agents. By structuring continuous physical space into a sparse topological graph of navigable waypoints, agents navigate efficiently using graph heuristics.

## Key Empirical Findings
1. Sparse waypoint graphs cut search space by 85% compared to continuous coordinate search.
2. Metric edge weights enforce Euclidean realism.
3. Robust to local perception noise.

## Authors' Stated Conclusions
Discretizing spatial environments into sparse waypoint graphs optimizes navigation planning.

## Open Challenges & Future Scope
Dynamic waypoint generation.

## Architectural Profile
- **Vision**: ViT-B/16
- **Projector**: Graph Attention
- **LLM**: Llama-3-8B
- **Tokens**: Waypoint tokens
