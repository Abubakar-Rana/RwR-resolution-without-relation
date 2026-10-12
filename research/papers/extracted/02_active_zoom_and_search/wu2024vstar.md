# V*: Guided Visual Search as a Core Mechanism in Multimodal LLMs

- **Authors**: Penghao Wu, Saining Xie
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2312.14135
- **URL**: https://arxiv.org/abs/2312.14135
- **BibTeX Key**: `wu2024vstar`

## Abstract
Current Multimodal Large Language Models (MLLMs) struggle with visual queries that require fine-grained search over high-resolution images, as standard vision architectures process images passively at fixed downsampled grids. We propose V*, an MLLM architecture with 'Guided Visual Search'. V* introduces an LLM-guided search algorithm that actively directs gaze across high-resolution image regions, maintaining an explicit visual working memory of localized observations. We construct VStar-Bench to evaluate targeted visual search. Experiments show that V* dramatically outperforms standard MLLMs on high-resolution object search, demonstrating that active search is a fundamental cognitive primitive for multimodal reasoning.

## Key Extracted Contributions
1. Passive single-pass visual processing fails fundamentally when evidence occupies <1% of the image area.
2. Visual working memory allows models to accumulate localized observations across multiple search steps.
3. LLM semantic guidance directs search far more effectively than blind visual saliency.
