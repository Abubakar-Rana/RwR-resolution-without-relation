# Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection

- **Authors**: Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, Lei Zhang
- **Year**: 2024
- **Venue**: ECCV 2024
- **arXiv**: 2303.05499
- **URL**: https://arxiv.org/abs/2303.05499
- **BibTeX Key**: `liu2024groundingdino`

## Abstract
We develop Grounding DINO, an open-set object detector that marries the transformer-based detector DINO with grounded pre-training. Grounding DINO performs feature enhancement at multiple phases via cross-modality feature fusion, cross-modality query selection, and cross-modality cross-attention. This deep multimodal fusion allows the model to detect arbitrary objects specified by text inputs with outstanding localization accuracy. Grounding DINO sets new state-of-the-art records on zero-shot detection on COCO, LVIS, and ODinW benchmarks, outperforming prior open-vocabulary detectors by substantial margins.

## Key Extracted Contributions
1. Multi-phase cross-modality feature fusion aligns text and visual tokens far better than post-hoc late fusion.
2. Achieves superior precision on tiny, dense, and non-canonical objects compared to general-purpose VLMs.
3. Emits calibrated bounding boxes $[x_1, y_1, x_2, y_2]$ and class confidences natively without language generation parsing errors.
