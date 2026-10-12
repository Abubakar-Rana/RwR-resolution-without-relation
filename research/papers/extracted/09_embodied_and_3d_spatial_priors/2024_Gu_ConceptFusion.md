# Machine Extraction: ConceptFusion: Open-set Multimodal 3D Mapping

- **BibTeX Key**: `gu2024conceptfusion`
- **Authors**: Krishna Murthy Jatavallabhula, Alireza Saharkhiz, Soroush Vosoughi, Antonio Torralba
- **Venue**: CVPR 2023 (2023)
- **arXiv**: [2302.07241](https://arxiv.org/abs/2302.07241)
- **Code**: https://concept-fusion.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (High Multimodal Mapping Prior)

## Abstract
We present ConceptFusion, building open-set multimodal 3D maps. By projecting pixel-aligned foundation model features (CLIP, DINO) into 3D geometry via SLAM, ConceptFusion supports open-ended text, audio, and visual queries directly on physical 3D maps.

## Key Empirical Findings
1. Fusing 2D foundation features into metric 3D point clouds retains fine semantic concepts.
2. Preserves exact metric spatial distances between entities.
3. Enables zero-shot natural language spatial queries ('find the area between the yellow couch and the desk').

## Authors' Stated Conclusions
Grounding 2D foundation features directly into metric spatial geometry creates powerful open-vocabulary spatial maps.

## Open Challenges & Future Scope
Dynamic scene updates and aerial mapping.

## Architectural Profile
- **Vision**: CLIP + DINO pixel features projected to 3D point cloud
- **Projector**: 3D Point Cloud Spatial Index
- **LLM**: None (Cosine similarity retrieval)
- **Tokens**: Dense 3D point features
