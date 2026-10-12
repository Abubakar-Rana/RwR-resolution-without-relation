# Monkey: Image Resolution and Text Label Are Important Things for Large Multi-Modal Models

- **Authors**: Zhang Li, Biao Yang, Qiang Liu, Zhiyin Ma, Shuo Zhang, Jingyi Yang, Yabo Sun, Yuliang Liu, Xiang Bai
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2311.06607
- **URL**: https://arxiv.org/abs/2311.06607
- **BibTeX Key**: `li2024monkey`

## Abstract
Enhancing image resolution is pivotal for capturing small targets, dense document text, and complex spatial configurations in Large Multimodal Models (LMMs). We propose Monkey, an efficient high-resolution LMM architecture that scales input resolution to 1344x1344 (over 6x larger than standard 336x336 inputs) without requiring end-to-end vision backbone retraining. Monkey splits high-resolution inputs into uniform patches, encodes each with a frozen CLIP ViT, and fuses local patch tokens with global context using a multi-level resampler. Combined with high-quality detailed text captioning data, Monkey achieves state-of-the-art results on DocVQA, TextVQA, and complex scene benchmarks.

## Key Extracted Contributions
1. Uniform patch splitting without retraining vision towers scales resolution effectively up to ~1.8 megapixels.
2. Multi-level resamplers preserve patch localization while compressing sequence length.
3. Beyond 1344x1344, quadratic token growth in the LLM becomes the primary bottleneck.
