# Machine Extraction: Voyager: An Open-Ended Embodied Agent with Large Language Models

- **BibTeX Key**: `wang2024voyager`
- **Authors**: Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar
- **Venue**: TMLR 2024 (2024)
- **arXiv**: [2305.16291](https://arxiv.org/abs/2305.16291)
- **Code**: https://voyager.minedojo.org
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 4 / 5 (High Autonomous Prior)

## Abstract
We introduce Voyager, an open-ended embodied agent driven by GPT-4. Voyager consists of an automatic curriculum, a skill library of executable code, and an iterative prompting mechanism with environmental feedback, continuously acquiring complex spatial and procedural abilities.

## Key Empirical Findings
1. Compounding reusable code skills in a skill library enables open-ended problem solving.
2. Iterative execution feedback corrects syntax and runtime errors automatically.
3. Discovers 3.3x more items and traverses 2.3x longer spatial distances than baseline agents.

## Authors' Stated Conclusions
A library of executable, verified code skills enables lifelong acquisition of complex spatial and procedural tasks.

## Open Challenges & Future Scope
Real-world robotics deployment.

## Architectural Profile
- **Vision**: MineDojo visual environment
- **Projector**: Skill Library (Vector DB)
- **LLM**: GPT-4 (Code generation)
- **Tokens**: N/A
