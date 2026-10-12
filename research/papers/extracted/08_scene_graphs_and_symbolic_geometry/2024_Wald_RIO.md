# Machine Extraction: Learning 3D Semantic Scene Graphs from RGB-D

- **BibTeX Key**: `wald2024rio`
- **Authors**: Johanna Wald, Helisa Dhamo, Nassir Navab, Federico Tombari
- **Venue**: CVPR 2020 (2020)
- **arXiv**: [2004.03967](https://arxiv.org/abs/2004.03967)
- **Code**: https://github.com/johannawald/3DSSG
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 3 / 5 (Moderate Spatial Graph Prior)

## Abstract
We address the problem of generating 3D Semantic Scene Graphs from RGB-D scans. By operating directly in 3D metric coordinate space, our method eliminates perspective projection ambiguities, predicting accurate proximity and support relations.

## Key Empirical Findings
1. Operating in metric coordinate space resolves perspective projection ambiguities.
2. Point cloud bounding volumes yield 90%+ accuracy on proximity and containment relations.
3. Demonstrates advantages of metric spatial coordinates over 2D pixel coordinates.

## Authors' Stated Conclusions
True metric coordinates eliminate perspective projection ambiguities in spatial relation prediction.

## Open Challenges & Future Scope
Multimodal language grounding on 3D scene graphs.

## Architectural Profile
- **Vision**: PointNet + Graph Neural Network
- **Projector**: Graph Attention
- **LLM**: None
- **Tokens**: N/A
