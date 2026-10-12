# Machine Extraction: AerialGraph: Semantic Topological Graph Construction in Earth Observation

- **BibTeX Key**: `wang2024aerialgraph`
- **Authors**: Dong Wang, Zichen Guo, Fangrun Wang, Wen Yang
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2406.12190](https://arxiv.org/abs/2406.12190)
- **Code**: https://github.com/WHU-USI/AerialGraph
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We present AerialGraph, an automated framework constructing topological graphs from Earth observation imagery. By incorporating planar graph constraints, AerialGraph reconstructs road networks and building layouts with guaranteed topological connectivity.

## Key Empirical Findings
1. Enforcing planar graph constraints eliminates 85% of broken road connections.
2. Topological graphs enable deterministic route planning and distance calculations.
3. Outperforms unstructured neural segmentation on network topology.

## Authors' Stated Conclusions
Topological graph constraints are essential for reconstructing physically connected infrastructure in remote sensing.

## Open Challenges & Future Scope
Multimodal conversational querying over topological graphs.

## Architectural Profile
- **Vision**: D-LinkNet + Planar Graph Post-Processor
- **Projector**: Symbolic Graph
- **LLM**: None
- **Tokens**: N/A
