# Machine Extraction: DD-PPO: Learning Near-Perfect PointGoal Navigators from 2.5 Billion Steps

- **BibTeX Key**: `wijmans2024ddppo`
- **Authors**: Erik Wijmans, Abhishek Kadian, Ari Morcos, Stefan Lee, Irfan Essa, Devi Parikh, Manolis Savva, Dhruv Batra
- **Venue**: ICLR 2020 (2020)
- **arXiv**: [1911.00357](https://arxiv.org/abs/1911.00357)
- **Code**: https://github.com/facebookresearch/habitat-lab
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Foundational RL Navigation)

## Abstract
We present DD-PPO, scaling distributed reinforcement learning to 2.5 billion steps. We demonstrate that massive-scale RL enables end-to-end neural agents to navigate near-perfectly, learning emergent spatial localization and pathfinding behaviors.

## Key Empirical Findings
1. Massive-scale experience (2.5B steps) produces emergent spatial map construction inside LSTM hidden states.
2. Reaches 99.9% navigation success on GPS+Compass PointNav.
3. Pure end-to-end models require billions of steps to learn basic geometric navigation.

## Authors' Stated Conclusions
End-to-end neural models can learn spatial navigation, but require billions of interactions to acquire basic geometric competence.

## Open Challenges & Future Scope
Zero-shot transfer to real robots.

## Architectural Profile
- **Vision**: ResNet-50 + GPS/Compass Encoders
- **Projector**: Linear
- **LLM**: 2-Layer LSTM Policy Network
- **Tokens**: N/A
