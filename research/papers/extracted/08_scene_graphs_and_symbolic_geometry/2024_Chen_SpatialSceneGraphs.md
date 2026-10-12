# Machine Extraction: Spatial Scene Graphs for Autonomous Aerial Navigation

- **BibTeX Key**: `chen2024spatialscenegraphs`
- **Authors**: Pengfei Chen, Liang Zhao, Bo Du
- **Venue**: IEEE TGRS 2024 (2024)
- **arXiv**: [2406.15890](https://arxiv.org/abs/2406.15890)
- **Code**: https://github.com/WHU-Geo/AerialSpatialSG
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We introduce Spatial Scene Graphs for remote sensing. Aerial scene graphs require metric precision rather than qualitative semantic tags. We construct metric graphs where edges encode continuous Euclidean distance, cardinal azimuth angles, and topological connectivity.

## Key Empirical Findings
1. Metric scene graphs encode continuous distance and cardinal angles explicitly on graph edges.
2. Enables graph traversal algorithms (Dijkstra, A*) for aerial route planning.
3. Outperforms unstructured text descriptions by +24.5% on drone navigation benchmarks.

## Authors' Stated Conclusions
Aerial scene graphs must be metric and geometric rather than purely qualitative semantic tags.

## Open Challenges & Future Scope
Direct integration into vision-language foundation models.

## Architectural Profile
- **Vision**: YOLOv8 + Metric Geometric Builder
- **Projector**: Symbolic Graph
- **LLM**: None (Graph solver)
- **Tokens**: N/A
