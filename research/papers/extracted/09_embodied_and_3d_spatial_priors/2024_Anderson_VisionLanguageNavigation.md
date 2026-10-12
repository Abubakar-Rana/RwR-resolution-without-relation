# Machine Extraction: Vision-and-Language Navigation: Interpreting visually-grounded navigation instructions

- **BibTeX Key**: `anderson2024vln`
- **Authors**: Peter Anderson, Qi Wu, Damien Teney, Jake Bruce, Mark Johnson, Niko Sünderhauf, Ian Reid, Stephen Gould, Anton van den Hengel
- **Venue**: CVPR 2018 (2018)
- **arXiv**: [1711.07280](https://arxiv.org/abs/1711.07280)
- **Code**: https://github.com/peteanderson80/Matterport3DSimulator
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Foundational VLN Benchmark)

## Abstract
We introduce the Vision-and-Language Navigation (VLN) problem. Agents are placed in photo-realistic 3D environments and must carry out natural language instructions by interpreting visual panoramas and navigating topological graphs to goals.

## Key Empirical Findings
1. Pioneers the VLN benchmark paradigm using Matterport3D panoramas.
2. Directional prepositions ('turn left', 'go forward') must be mapped to visual heading changes.
3. Early sequence-to-sequence models achieve low navigation success (approx 25%).

## Authors' Stated Conclusions
Mapping linguistic navigation directions to physical spatial heading is challenging for neural models.

## Open Challenges & Future Scope
Transformer-based navigation agents (achieved in VLN-BERT).

## Architectural Profile
- **Vision**: ResNet-152 image features
- **Projector**: Attention LSTM
- **LLM**: None (Pre-LLM era)
- **Tokens**: N/A
