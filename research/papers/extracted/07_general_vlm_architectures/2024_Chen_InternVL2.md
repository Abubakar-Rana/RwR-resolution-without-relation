# Machine Extraction: InternVL 2.0: Master High-Resolution Multimodal Understanding

- **BibTeX Key**: `chen2024internvl2`
- **Authors**: Zhe Chen, Weiyun Wang, Hao Tian, Shenglong Ye, Zhangwei Gao, Erfei Cui, Wenwen Wen, Zhaoyang Zeng, Jiashuo Sun, Chao Shen, et al.
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2408.03326](https://arxiv.org/abs/2408.03326)
- **Code**: https://github.com/OpenGVLab/InternVL
- **Category**: 07_general_vlm_architectures
- **Relevance**: 5 / 5 (Critical Direct Comparison)

## Abstract
We introduce InternVL 2.0, advancing open-source multimodal understanding across resolutions up to 4K. By using dynamic patch subdivision and a 2x2 Pixel Shuffle projector, InternVL 2.0 matches proprietary models like GPT-4V across core benchmarks.

## Key Empirical Findings
1. Dynamic patch subdivision handles arbitrary aspect ratios with up to 12 tiles.
2. Pixel Shuffle 2x2 downsamples tokens by 4x, maintaining compact 256 tokens per tile.
3. Achieves SOTA among open-weights models on document, OCR, and visual perception benchmarks.

## Authors' Stated Conclusions
Dynamic patch tiling combined with Pixel Shuffle compression is the premier open-source high-resolution architecture.

## Open Challenges & Future Scope
Gigapixel scaling beyond 4K.

## Architectural Profile
- **Vision**: InternViT-6B-448
- **Projector**: Pixel Shuffle (4x compression) + MLP
- **LLM**: InternLM2.5-7B / InternLM2.5-20B / Qwen-72B
- **Tokens**: 256 tokens per tile (up to 3,072 tokens)
