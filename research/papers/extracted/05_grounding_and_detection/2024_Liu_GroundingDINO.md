# Machine Extraction: Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection

- **BibTeX Key**: `liu2024groundingdino`
- **Authors**: Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, Lei Zhang
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2303.05499](https://arxiv.org/abs/2303.05499)
- **Code**: https://github.com/IDEA-Research/GroundingDINO
- **Category**: 05_grounding_and_detection
- **Relevance**: 5 / 5 (Critical Solution Prior)

## Abstract
We present Grounding DINO, an open-set object detector that marries transformer-based detector DINO with grounded pre-training. Grounding DINO performs feature enhancement via cross-attention at multiple stages, achieving state-of-the-art open-vocabulary detection performance across multiple benchmarks without fine-tuning.

## Key Empirical Findings
1. Deep multi-stage cross-attention aligns visual features with text phrases tightly.
2. Achieves 52.5 AP zero-shot on COCO and excels on referring expression comprehension.
3. High detection accuracy on small and dense objects compared to autoregressive VLMs.
4. Inference latency is ~120ms per 1K image (acceptable for candidate proposal).

## Authors' Stated Conclusions
Dedicated open-set object detectors vastly outperform autoregressive VLMs on dense localization and fine object detection.

## Open Challenges & Future Scope
Adapting to oriented bounding boxes and gigapixel image slicing.

## Architectural Profile
- **Vision**: Swin-T / Swin-B with Multi-Scale Deformable Attention
- **Projector**: Cross-Modality Feature Enhancer
- **LLM**: BERT-Base / RoBERTa (Text backbone)
- **Tokens**: 900 object queries
