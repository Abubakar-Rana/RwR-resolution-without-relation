# Machine Extraction: Making the V in VQA Matter: Elevating the Role of Image Understanding

- **BibTeX Key**: `goyal2024counterfactualvqa`
- **Authors**: Yash Goyal, Tejas Khot, Douglas Summers-Stay, Dhruv Batra, Devi Parikh
- **Venue**: CVPR 2017 (2017)
- **arXiv**: [1612.00837](https://arxiv.org/abs/1612.00837)
- **Code**: https://visualqa.org
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 4 / 5 (Foundational VQA Benchmark)

## Abstract
We show that standard VQA benchmarks suffer from severe language biases where models answer questions accurately without even looking at the image. We create VQA v2.0, balancing the dataset so that every question is associated with a pair of similar images resulting in different answers.

## Key Empirical Findings
1. Standard models achieve high benchmark scores on VQA v1.0 by memorizing statistical language correlations.
2. Balancing image pairs drops blind language models from 55% to near chance (25%).
3. Foundational paper that forced the field to ensure models actually look at visual evidence.

## Authors' Stated Conclusions
VQA benchmarks must be balanced with counterfactual image pairs to prevent models from gaming benchmarks via language priors.

## Open Challenges & Future Scope
Balanced multimodal evaluation in the LLM era.

## Architectural Profile
- **Vision**: ResNet-152
- **Projector**: Multimodal pooling
- **LLM**: LSTM
- **Tokens**: N/A
