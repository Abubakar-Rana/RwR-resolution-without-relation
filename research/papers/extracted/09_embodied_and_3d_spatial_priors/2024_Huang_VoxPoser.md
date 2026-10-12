# Machine Extraction: VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models

- **BibTeX Key**: `huang2024voxposer`
- **Authors**: Wenlong Huang, Chen Wang, Ruohan Zhang, Yunzhu Li, Jiajun Wu, Li Fei-Fei
- **Venue**: CoRL 2023 (2023)
- **arXiv**: [2307.05973](https://arxiv.org/abs/2307.05973)
- **Code**: https://voxposer.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (High Spatial Synthesis Prior)

## Abstract
We present VoxPoser, enabling zero-shot robot manipulation by composing 3D value maps. An LLM generates Python code that computes spatial cost functions over voxelized physical scene representations, which motion planners solve for collision-free trajectories.

## Key Empirical Findings
1. Programmatically generating spatial cost maps grounds language instructions in continuous geometry.
2. Voxel cost maps compose seamlessly (e.g. goal attraction map + obstacle avoidance map).
3. Solves spatial trajectories without any robot policy training.

## Authors' Stated Conclusions
Programmatic code generation over spatial cost grids is an exceptionally effective bridge between language models and continuous physical geometry.

## Open Challenges & Future Scope
Dynamic voxel grids in changing scenes.

## Architectural Profile
- **Vision**: RGB-D Voxelizer + OWL-ViT / SAM
- **Projector**: Voxel Value Map
- **LLM**: GPT-4 (Code generation)
- **Tokens**: N/A (Python scripts)
