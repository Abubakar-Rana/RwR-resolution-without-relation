# Machine Extraction: ConceptGraphs: Open-Vocabulary 3D Scene Graphs for Robot Perception

- **BibTeX Key**: `jatavallabhula2024conceptgraphs`
- **Authors**: Qiao Gu, Ali Kuwajerwala, Soroush Vosoughi, Antonio Torralba
- **Venue**: ICRA 2024 (2024)
- **arXiv**: [2309.16650](https://arxiv.org/abs/2309.16650)
- **Code**: https://concept-graphs.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (High Open-Vocabulary Graph Prior)

## Abstract
We introduce ConceptGraphs, building open-vocabulary 3D scene graphs from RGB-D observations. It clusters 2D segmentations across views into 3D bounding boxes, generating rich scene graphs annotated with language embeddings and spatial relations for downstream LLM reasoning.

## Key Empirical Findings
1. Clustering multi-view segmentations builds clean 3D scene graphs with zero manual supervision.
2. Bounding box coordinates enable exact spatial relation calculations (containment, proximity, relative heading).
3. LLMs reason effectively over the resulting structured graph.

## Authors' Stated Conclusions
Open-vocabulary 3D scene graphs bridge multi-view perception and language model spatial reasoning.

## Open Challenges & Future Scope
Scaling to city-scale aerial mapping.

## Architectural Profile
- **Vision**: SAM + CLIP + Grounding DINO
- **Projector**: 3D Scene Graph
- **LLM**: GPT-4 (Graph querying)
- **Tokens**: Graph nodes and edges
