# Machine Extraction: Divide, Conquer and Combine: A Training-Free Framework for High-Resolution Image Perception in Multimodal Large Language Models

- **BibTeX Key**: `wang2025dc2`
- **Authors**: Weixian Wang, Zhangwei Gao, Mengmeng Wang, Shenghao Zhang
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2408.01890](https://arxiv.org/abs/2408.01890)
- **Code**: https://github.com/ZJU-VIP/DC2
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Algorithmic Relevance)

## Abstract
We introduce DC2 (Divide, Conquer, Combine), a training-free framework scaling off-the-shelf MLLMs to ultra-high resolution. DC2 partitions the image, conquer patches via query-guided filtering, and combines intermediate predictions into the final output.

## Key Empirical Findings
1. Training-free patching improves detail detection on standard MLLMs.
2. Combining local patch descriptions often fails on spatial relational questions.
3. When objects cross patch seams, the combine step hallucinates duplicates.

## Authors' Stated Conclusions
Late-fusion combination of patch text outputs cannot reconstruct spatial geometry.

## Open Challenges & Future Scope
Early visual token fusion rather than late text combination.

## Architectural Profile
- **Vision**: CLIP / Qwen-VL native encoder
- **Projector**: Native
- **LLM**: GPT-4V / Qwen2-VL
- **Tokens**: Native
