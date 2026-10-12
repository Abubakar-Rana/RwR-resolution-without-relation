# Cascaded Vision-Language Reasoning: Routing Between Global Overviews and High-Resolution Crops

- **Authors**: Kai Li, Wei Li, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2409.11223
- **URL**: https://arxiv.org/abs/2409.11223
- **BibTeX Key**: `li2024cascadedvlm`

## Abstract
We present CascadedVLM, a framework for cascaded vision-language reasoning that dynamically navigates between global overviews and high-resolution crops. Given a complex image query, CascadedVLM first generates a rapid preliminary response using a global downscaled overview. If the language model's predictive entropy is low, the response is committed; if predictive entropy is high, the query is escalated to a high-resolution crop extraction stage. Across high-resolution benchmarks, CascadedVLM matches the accuracy of full-resolution multi-crop models while reducing average inference latency by 64% and preventing degradation on global spatial queries.

## Key Extracted Contributions
1. Over 60% of high-resolution image questions are solved correctly by the global overview alone.
2. Escalating only uncertain questions to crops prevents the degradation of global spatial context on overview-friendly tasks.
3. Cuts average inference latency by 64% by skipping crop extraction on confident items.
