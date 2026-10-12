# Machine Extraction: Winoground: Scrutinizing Language and Vision Compositionality

- **BibTeX Key**: `thrush2024winoground`
- **Authors**: Tristan Thrush, Ryan Jiang, Max Bartolo, Amanpreet Singh, Adina Williams, Douwe Kiela, Christopher Candido
- **Venue**: CVPR 2022 (2022)
- **arXiv**: [2204.03162](https://arxiv.org/abs/2204.03162)
- **Code**: https://huggingface.co/datasets/facebook/winoground
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 4 / 5 (Foundational Negative Control)

## Abstract
We present Winoground, a novel task and dataset for evaluating whether vision-language models can resolve visio-linguistic compositionality. Given two images and two captions with identical words in different orders, models perform near chance, demonstrating a severe lack of compositional understanding.

## Key Empirical Findings
1. SOTA models (CLIP, ViLBERT, UNITER) score near 0% group score (random chance is 16.7%).
2. Swapping words reveals models act as bag-of-words keyword matchers rather than parsing relational grammar.
3. Establishes the classic compositional negative control.

## Authors' Stated Conclusions
Contrastive and masked vision-language pretraining does not induce compositional or relational grammar understanding.

## Open Challenges & Future Scope
Compositional pretraining objectives.

## Architectural Profile
- **Vision**: Evaluates 10+ vision-language models
- **Projector**: Native
- **LLM**: Various
- **Tokens**: Native
