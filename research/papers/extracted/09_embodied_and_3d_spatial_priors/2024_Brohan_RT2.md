# Machine Extraction: RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control

- **BibTeX Key**: `brohan2024rt2`
- **Authors**: Anthony Brohan, Noah Brown, Justice Carbajal, Yevgen Chebotar, Joseph Dabis, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Jasmine Hsu, Julian Ibarz, Brian Ichter, et al.
- **Venue**: CoRL 2023 (2023)
- **arXiv**: [2307.15818](https://arxiv.org/abs/2307.15818)
- **Code**: https://robotics-transformer2.github.io
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Moderate Embodied Prior)

## Abstract
We present RT-2, translating vision-language models into vision-language-action models. By outputting robotic actions as text tokens, RT-2 transfers semantic reasoning from web-scale pre-training to physical physical manipulation tasks.

## Key Empirical Findings
1. Discrete action tokens allow standard autoregressive VLMs to output physical motion coordinates.
2. Emergent semantic generalization to unseen objects and relational instructions.
3. Discretization limits motion precision to the quantization bin resolution.

## Authors' Stated Conclusions
Language models can generate physical spatial action trajectories via tokenized coordinate spaces.

## Open Challenges & Future Scope
Continuous action heads.

## Architectural Profile
- **Vision**: PaLI-X / PaLM-E visual encoders
- **Projector**: Linear
- **LLM**: PaLM-2
- **Tokens**: Action tokens (0-255 bins)
