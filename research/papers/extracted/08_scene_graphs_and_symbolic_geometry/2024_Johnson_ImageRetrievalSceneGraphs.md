# Machine Extraction: Image Retrieval Using Scene Graphs

- **BibTeX Key**: `johnson2024imageretrievalscenegraphs`
- **Authors**: Justin Johnson, Ranjay Krishna, Michael Stark, Li-Jia Li, David Shamma, Michael Bernstein, Li Fei-Fei
- **Venue**: CVPR 2015 (2015)
- **arXiv**: [1504.05809](https://arxiv.org/abs/1504.05809)
- **Code**: https://github.com/jcjohns/scene-graphs
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 4 / 5 (Foundational Scene Graph Literature)

## Abstract
We introduce Scene Graphs, a graph-based semantic representation of visual scenes. Scene graphs explicitly capture objects, their attributes, and directed relationships between pairs of objects, enabling grounding and structured image retrieval beyond unstructured text tags.

## Key Empirical Findings
1. Formalized the scene graph tuple $G = (V, E)$ where nodes are objects and edges are spatial/semantic relationships.
2. Structured relationships capture spatial layout far more accurately than bag-of-words text.
3. Foundational paper that initiated the entire visual scene graph literature.

## Authors' Stated Conclusions
Explicit graph structures of objects and relationships bridge perceptual pixels and symbolic semantic reasoning.

## Open Challenges & Future Scope
Automated scene graph generation from raw pixels (realized in iterative message passing).

## Architectural Profile
- **Vision**: R-CNN object proposals
- **Projector**: Conditional Random Field (CRF) matching
- **LLM**: None
- **Tokens**: Graph tuples
