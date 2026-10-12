# Machine Extraction: PointLLM: Empowering Large Language Models to Understand Point Clouds

- **BibTeX Key**: `mani2024pointllm`
- **Authors**: Runsen Xu, Xinwei Chen, Yufei Xu, Jiabo Huang, Siying Dong, Tongyi Lu
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2308.16911](https://arxiv.org/abs/2308.16911)
- **Code**: https://github.com/OpenRobotLab/PointLLM
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Moderate 3D LLM Prior)

## Abstract
We introduce PointLLM, enabling LLMs to understand 3D point clouds. By aligning Point-BERT features with Vicuna-7B, PointLLM processes 3D object geometries and answers questions about 3D shapes, parts, and spatial configurations.

## Key Empirical Findings
1. Point cloud tokenization injects raw 3D coordinate geometry directly into LLM attention.
2. Excels at identifying 3D part orientations.
3. Requires dense 3D point supervision.

## Authors' Stated Conclusions
Direct coordinate point cloud tokenization endows language models with rich geometric awareness.

## Open Challenges & Future Scope
City-scale LiDAR scene comprehension.

## Architectural Profile
- **Vision**: Point-BERT (Point cloud encoder)
- **Projector**: Linear Projection
- **LLM**: Vicuna-7B
- **Tokens**: 512 point tokens
