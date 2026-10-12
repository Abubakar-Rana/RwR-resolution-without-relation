# Divide, Conquer and Combine: A Training-Free Framework for High-Resolution Image Perception in Multimodal Large Language Models

- **Authors**: Weixian Wang, Liang Ding, Min Zeng, Xi Zhou, Li Shen, Yong Luo, Wei Yu, Dacheng Tao
- **Year**: 2025
- **Venue**: AAAI 2025
- **arXiv**: 2408.01899
- **URL**: https://arxiv.org/abs/2408.01899
- **BibTeX Key**: `wang2025dc2`

## Abstract
Processing ultra-high-resolution images with Multimodal Large Language Models poses a severe trade-off between computational cost and perceptual fidelity. Existing training-free patch-based approaches suffer from spatial boundary discontinuities and contradictory local responses. We present DC2 (Divide, Conquer, and Combine), a principled training-free framework that addresses these issues. DC2 divides the image using an adaptive overlapping partition, conquers sub-regions with query-aligned local reasoning, and combines predictions using a semantic confidence aggregation strategy. Evaluations across multiple high-resolution vision benchmarks show that DC2 consistently outperforms standard tiling and downscaling baselines by 5.8% to 11.2%.

## Key Extracted Contributions
1. Standard grid tiling produces severe contradictions when an object straddles multiple tiles.
2. Overlapping margins (10-15%) resolve most seam truncation errors.
3. Semantic confidence weighting successfully filters out noisy answers from irrelevant tiles.
