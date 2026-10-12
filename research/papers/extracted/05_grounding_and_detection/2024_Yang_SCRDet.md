# Machine Extraction: SCRDet: Towards More Robust Detection for Small, Cluttered and Rotated Objects

- **BibTeX Key**: `yang2024scrdet`
- **Authors**: Xue Yang, Jirui Yang, Junchi Yan, Yue Zhang, Tengfei Zhang, Zhi Guo, Xian Sun, Kun Fu
- **Venue**: ICCV 2019 (2019)
- **arXiv**: [1811.07126](https://arxiv.org/abs/1811.07126)
- **Code**: https://github.com/Thinklab-SJTU/SCRDet
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Aerial Detection)

## Abstract
Detecting small, cluttered, and rotated objects in aerial imagery suffers from feature loss and boundary discontinuities. SCRDet introduces a supervised feature attention network and an IoU-smooth L1 loss that eliminates gradient explosion at angle boundaries.

## Key Empirical Findings
1. Supervised attention suppresses background clutter in aerial scenes.
2. IoU-smooth L1 loss handles angle boundary periodicity ($0^\circ \leftrightarrow 180^\circ$).
3. High recall on densely packed vehicles and small ships.

## Authors' Stated Conclusions
Feature attention and smooth angle losses are essential for detecting small cluttered aerial targets.

## Open Challenges & Future Scope
Transformer-based oriented detection.

## Architectural Profile
- **Vision**: ResNet-101 with Feature Attention
- **Projector**: Rotated RoI Head
- **LLM**: None
- **Tokens**: N/A
