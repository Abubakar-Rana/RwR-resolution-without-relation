# Machine Extraction: Don't Just Assume: Analyzing Priors and Language Shortcut Biases in VQA

- **BibTeX Key**: `agrawal2024dontjustassume`
- **Authors**: Aishwarya Agrawal, Dhruv Batra, Devi Parikh, Aniruddha Kembhavi
- **Venue**: CVPR 2018 (2018)
- **arXiv**: [1712.00374](https://arxiv.org/abs/1712.00374)
- **Code**: https://github.com/ashagrawal/vqa-cp
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 4 / 5 (Foundational Bias Analysis)

## Abstract
We introduce VQA-CP, where the distribution of answers per question type differs between train and test splits. When language priors cannot be relied upon, standard VQA model accuracy collapses by over 20%, proving models rely on statistical shortcuts.

## Key Empirical Findings
1. Models rely heavily on memorized conditional distributions $P(answer | question\_prefix)$.
2. Changing prior distributions exposes severe generalization collapse.
3. Spatial questions are especially prone to prior exploitation.

## Authors' Stated Conclusions
Evaluation under changing priors is mandatory to verify true multimodal reasoning.

## Open Challenges & Future Scope
Out-of-distribution evaluation for modern MLLMs.

## Architectural Profile
- **Vision**: Faster R-CNN
- **Projector**: Attention
- **LLM**: LSTM
- **Tokens**: N/A
