# Machine Extraction: Scene Graph Generation by Iterative Message Passing

- **BibTeX Key**: `xu2024scenegraphgeneration`
- **Authors**: Danfei Xu, Yuke Zhu, Christopher B. Choy, Li Fei-Fei
- **Venue**: CVPR 2017 (2017)
- **arXiv**: [1701.02426](https://arxiv.org/abs/1701.02426)
- **Code**: https://github.com/danfeiX/scene-graph-generation
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (Foundational SGG Literature)

## Abstract
We present an end-to-end model that generates scene graphs from images using iterative message passing. By allowing contextual information to propagate iteratively between object nodes and relationship edges, our model captures joint contextual dependencies across the visual scene.

## Key Empirical Findings
1. Iterative message passing between objects and relations boosts relation classification by +12.4%.
2. Joint context resolves visual ambiguity (e.g., knowing an object is 'water' helps classify relation 'swimming in').
3. Graph neural message passing is effective for visual topology.

## Authors' Stated Conclusions
Bidirectional message passing between object nodes and relation edges is essential for resolving relational ambiguity.

## Open Challenges & Future Scope
Unbiased relationship generation.

## Architectural Profile
- **Vision**: VGG-16 / Faster R-CNN
- **Projector**: Gated Recurrent Unit (GRU) Message Passing
- **LLM**: None
- **Tokens**: N/A
