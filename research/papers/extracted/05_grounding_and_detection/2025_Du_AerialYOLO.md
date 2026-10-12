# Machine Extraction: Aerial-YOLO: Real-Time Tiny Object Detection in Gigapixel Imagery

- **BibTeX Key**: `du2025aerialyolo`
- **Authors**: Bo Du, Fangrun Wang, Haoliang Wang, Wen Yang
- **Venue**: CVPR 2025 (2025)
- **arXiv**: [2502.16780](https://arxiv.org/abs/2502.16780)
- **Code**: https://github.com/WHU-USI/AerialYOLO
- **Category**: 05_grounding_and_detection
- **Relevance**: 5 / 5 (Critical Domain Solution)

## Abstract
Standard YOLOs downsample images by 32x, destroying features of tiny aerial targets. Aerial-YOLO introduces a dedicated P2 detection head operating at 4x downsampling with high-frequency spatial attention, detecting sub-15-pixel targets in gigapixel imagery at 45 FPS.

## Key Empirical Findings
1. Adding a P2 (4x downsampling) head boosts tiny object recall by +22.4% on aerial imagery.
2. Detects objects as small as 8x8 pixels reliably.
3. Runs in 22ms per 1024x1024 tile on modern GPUs.

## Authors' Stated Conclusions
Retaining shallow 4x feature pyramid layers is mandatory for detecting sub-20-pixel targets in aerial imagery.

## Open Challenges & Future Scope
Open-vocabulary classification on P2 feature heads.

## Architectural Profile
- **Vision**: YOLOv8-Aerial with P2 Head
- **Projector**: Anchor-free head
- **LLM**: None
- **Tokens**: Dense grid
