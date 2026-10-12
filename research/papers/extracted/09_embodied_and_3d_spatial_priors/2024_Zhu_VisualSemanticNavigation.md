# Machine Extraction: Target-Driven Visual Navigation in Indoor Scenes using Deep Reinforcement Learning

- **BibTeX Key**: `zhu2024visualsemanticnavigation`
- **Authors**: Yuke Zhu, Roozbeh Mottaghi, Eric Kolve, Joseph J. Lim, Abhinav Gupta, Li Fei-Fei, Ali Farhadi
- **Venue**: ICRA 2017 (2017)
- **arXiv**: [1609.05143](https://arxiv.org/abs/1609.05143)
- **Code**: https://github.com/allenai/target-driven-visual-navigation
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Foundational Visual Navigation)

## Abstract
We address the problem of target-driven visual navigation. We formulate navigation using deep reinforcement learning where the input is both the current observation and a visual target image, learning generic spatial navigation representations.

## Key Empirical Findings
1. Siamese feature comparison between current observation and target image guides spatial movement.
2. Learns implicit spatial maps of room layout.
3. Generalizes to new targets across unseen physical scenes.

## Authors' Stated Conclusions
Joint representation of current observation and visual target enables goal-directed spatial navigation.

## Open Challenges & Future Scope
Natural language goal specifications.

## Architectural Profile
- **Vision**: ResNet-50 Siamese Network
- **Projector**: Fusion Layer
- **LLM**: A3C Policy Network
- **Tokens**: N/A
