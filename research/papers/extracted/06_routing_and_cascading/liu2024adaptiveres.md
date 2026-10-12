# Adaptive Visual Resolution Routing for High-Throughput Multimodal Processing

- **Authors**: Haotian Liu, Chunyuan Li, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2409.05678
- **URL**: https://arxiv.org/abs/2409.05678
- **BibTeX Key**: `liu2024adaptiveres`

## Abstract
Current Multimodal LLMs process all visual inputs at maximum resolution or fixed crop grids, leading to severe computational waste on questions that only require global scene understanding. We introduce Adaptive Visual Resolution Routing (AdaptiveRes), an inference framework that dynamically routes each visual query to the minimal necessary resolution tier. We train a lightweight resolution predictor that inspects question text and low-resolution image embeddings to assign optimal resolution budgets. AdaptiveRes maintains 99.1% of maximum-resolution accuracy across multi-modal benchmarks while cutting average token processing by 58%.

## Key Extracted Contributions
1. Up to 60% of benchmark queries achieve identical accuracy at lower resolution tiers.
2. Question text contains strong indicators of resolution requirements (e.g. 'what color is the text on the sign' vs 'what scene is depicted').
3. Routing to the minimal sufficient resolution avoids noise and distractor tokens.
