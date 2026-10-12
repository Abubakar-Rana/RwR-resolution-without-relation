# Machine Extraction: Hierarchical Scene Graph Generation for High-Resolution Imagery

- **BibTeX Key**: `guo2024hierarchicalscenegraph`
- **Authors**: Zichen Guo, Fangrun Wang, Haoliang Wang, Wen Yang
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2405.11200](https://arxiv.org/abs/2405.11200)
- **Code**: https://github.com/WHU-USI/HierarchicalSG
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 5 / 5 (Critical Direct Prior)

## Abstract
Flattening all entities in high-resolution imagery into a single scene graph produces combinatorial edge explosion and noise. We present Hierarchical Scene Graph Generation (HSGG), decomposing aerial graphs into macro-level regional graphs and micro-level object graphs.

## Key Empirical Findings
1. Two-level hierarchy cuts total graph edge count by 80%, eliminating combinatorial edge explosion.
2. Macro-level graphs preserve global cardinal layout and broad topology.
3. Micro-level graphs capture fine object distances and orientations within local clusters.
4. Directly resolves the scale gap in gigapixel scene representations.

## Authors' Stated Conclusions
Hierarchical scene graph decomposition prevents combinatorial noise and separates global topology from local detail.

## Open Challenges & Future Scope
Dynamic depth hierarchies matching image resolution.

## Architectural Profile
- **Vision**: Hierarchical Faster R-CNN + GNN
- **Projector**: Hierarchical Graph Message Passing
- **LLM**: None (Graph generation focus)
- **Tokens**: N/A
