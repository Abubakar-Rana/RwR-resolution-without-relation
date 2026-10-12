# Machine Extraction: Preserving Spatial Topology in Aerial Scene Graph Parsing

- **BibTeX Key**: `zheng2025spatialtopologygraph`
- **Authors**: Kai Zheng, Haoliang Wang, Wen Yang
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2502.13890](https://arxiv.org/abs/2502.13890)
- **Code**: https://github.com/WHU-USI/SpatialTopologyGraph
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 5 / 5 (Critical Direct Prior)

## Abstract
Standard scene graph generators connect objects with dense, arbitrary edges that violate physical spatial topology. We introduce Spatial Topology Graph (STG) parsing, which constrains graph edges using Delaunay triangulation and planar geometric adjacency.

## Key Empirical Findings
1. Delaunay triangulation guarantees that edges only connect true spatial neighbors, eliminating 90% of redundant relations.
2. Preserves topological invariance under coordinate scaling and rotation.
3. Improves downstream spatial VQA accuracy by +16.4% over unconstrained dense graphs.

## Authors' Stated Conclusions
Delaunay triangulation provides the mathematically optimal graph topology for spatial relational reasoning.

## Open Challenges & Future Scope
Dynamic 3D Delaunay graphs.

## Architectural Profile
- **Vision**: YOLO-World + Delaunay Triangulation Solver
- **Projector**: Planar Graph Builder
- **LLM**: Python / Qwen2.5-VL
- **Tokens**: N/A
