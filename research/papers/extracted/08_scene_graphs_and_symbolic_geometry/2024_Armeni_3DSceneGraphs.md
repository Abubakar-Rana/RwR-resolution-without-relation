# Machine Extraction: 3D Scene Graph: A Dense Representation of Large-Scale Environments

- **BibTeX Key**: `armeni20243dscenegraphs`
- **Authors**: Iro Armeni, Zhi-Yang He, JunYoung Gwak, Amir R. Zamir, Martin Fischer, Jitendra Malik, Silvio Savarese
- **Venue**: ICCV 2019 (2019)
- **arXiv**: [1910.02527](https://arxiv.org/abs/1910.02527)
- **Code**: https://3dscenegraph.stanford.edu
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (Foundational 3D Graph Prior)

## Abstract
We present 3D Scene Graph, a unified, hierarchical representation for multi-room large-scale environments. It organizes spatial and semantic entities into a multi-layer graph spanning buildings, rooms, objects, and camera poses with 3D metric coordinates.

## Key Empirical Findings
1. Multi-layer hierarchy (building -> room -> object) enables efficient multi-scale spatial querying.
2. Metric 3D coordinates allow exact distance and visibility computations.
3. Foundational paper bridging geometric computer vision with symbolic spatial graphs.

## Authors' Stated Conclusions
Hierarchical multi-layer graph structuring is essential for scaling spatial representations to large environments.

## Open Challenges & Future Scope
Automated dynamic scene graph construction.

## Architectural Profile
- **Vision**: PointNet++ / 3D CNNs
- **Projector**: Hierarchical Graph
- **LLM**: None
- **Tokens**: N/A
