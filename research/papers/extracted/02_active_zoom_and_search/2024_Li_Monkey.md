# Machine Extraction: Monkey: Image Resolution and Text Label Are Important Things for Large Multi-Modal Models

- **BibTeX Key**: `li2024monkey`
- **Authors**: Zhang Li, Biao Yang, Qiang Liu, Zhiyin Ma, Shuo Zhang, Jingxu Yang, Yabo Sun, Yuliang Liu, Xiang Bai
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2311.06607](https://arxiv.org/abs/2311.06607)
- **Code**: https://github.com/Yuliang-Liu/Monkey
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
We present Monkey, a training-efficient approach scaling MLLM input resolution. By dividing images into uniform patches and processing each through a pre-trained visual encoder before cross-patch fusion, Monkey enhances fine text and small object detection.

## Key Empirical Findings
1. Scaling resolution directly boosts fine-grained perception (+15.2% on document and dense QA).
2. Cross-patch resampler prevents token explosion.
3. Dense uniform patching scales quadratically with gigapixel image dimensions.

## Authors' Stated Conclusions
Resolution scaling is the single most effective lever for small target perception.

## Open Challenges & Future Scope
Non-uniform adaptive patching.

## Architectural Profile
- **Vision**: CLIP ViT-BigG
- **Projector**: Multi-level Resampler
- **LLM**: Qwen-7B
- **Tokens**: 1,024 tokens
