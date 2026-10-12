# Machine Extraction: ALFRED: A Benchmark for Interpreting Grounded Instructions for Everyday Tasks

- **BibTeX Key**: `padmakumar2024alfred`
- **Authors**: Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, Dieter Fox
- **Venue**: CVPR 2020 (2020)
- **arXiv**: [1912.01734](https://arxiv.org/abs/1912.01734)
- **Code**: https://askforalfred.com
- **Category**: 09_embodied_and_3d_spatial_priors
- **Relevance**: 3 / 5 (Foundational Task Benchmark)

## Abstract
We introduce ALFRED, a benchmark for learning a mapping from natural language instructions and egocentric vision to sequences of actions. ALFRED requires long-horizon planning and spatial interaction with objects in 3D interactive environments.

## Key Empirical Findings
1. Multi-step compositional instructions suffer compounding error rates in monolithic agents.
2. Sub-goal decomposition (breaking instructions into sub-goals) is essential for long-horizon completion.
3. Interaction mask prediction grounds action targets physically.

## Authors' Stated Conclusions
Long-horizon compositional execution requires modular sub-goal planning to prevent error accumulation.

## Open Challenges & Future Scope
Foundation model planners.

## Architectural Profile
- **Vision**: ResNet-50 + Mask R-CNN
- **Projector**: Seq2Seq LSTM / Transformer
- **LLM**: None (Pre-LLM era)
- **Tokens**: N/A
