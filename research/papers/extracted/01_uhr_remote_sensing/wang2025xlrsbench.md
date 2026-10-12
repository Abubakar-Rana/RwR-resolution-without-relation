# XLRS-Bench: Could Your Multimodal LLMs Understand Extremely Large Ultra-High-Resolution Remote Sensing Imagery?

- **Authors**: Fangrun Wang, Haoliang Wang, Zichen Guo, Dong Wang, Yuting Wang, Mengxi Chen, Qiang Ma, Lin Lan, Wen Yang, Jiaming Zhang, Zhiyong Liu, Ming-Ming Sun
- **Year**: 2025
- **Venue**: CVPR 2025
- **arXiv**: 2503.23771
- **URL**: https://arxiv.org/abs/2503.23771
- **BibTeX Key**: `wang2025xlrsbench`

## Abstract
Multimodal Large Language Models (MLLMs) have made remarkable strides in natural image comprehension, yet their capability on extremely large ultra-high-resolution (UHR) remote sensing imagery remains largely unmapped. Standard remote sensing images frequently exceed 8000x8000 pixels, where targets of interest occupy only dozens of pixels against massive geospatial backgrounds. In this paper, we introduce XLRS-Bench, the first comprehensive benchmark tailored for UHR remote sensing MLLM evaluation. XLRS-Bench contains 45,942 annotations spanning 16 vision-language tasks covering fine-grained perception, complex relational reasoning, cross-region counting, and multi-temporal change. Extensive evaluations of over 20 proprietary and open-source MLLMs reveal substantial performance degradation caused by excessive downscaling and fragmentation during tiling, establishing critical benchmarks and failure modes for future geospatial multimodal intelligence.

## Key Extracted Contributions
1. SOTA models like GPT-4V and Qwen2.5-VL drop significantly below human performance on UHR imagery compared to natural benchmarks.
2. Naive image resizing obliterates sub-100-pixel objects entirely.
3. Independent tiling preserves local details but severs cross-tile context, causing relational reasoning accuracy to collapse.
4. Establishes the 16-task taxonomy including object spatial relationship, regional counting, route planning, and object attribute detection.
