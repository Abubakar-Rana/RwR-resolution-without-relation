# Oriented Object Detection in Remote Sensing: A Comprehensive Survey

- **Authors**: Jiaming Wang, Wen Yang, Haoliang Wang, et al.
- **Year**: 2024
- **Venue**: IEEE GRSM 2024
- **arXiv**: 2402.15890
- **URL**: https://arxiv.org/abs/2402.15890
- **BibTeX Key**: `wang2024orienteddetrs`

## Abstract
Oriented object detection is a vital task in Earth Observation that aims to locate objects with rotated bounding boxes, capturing true object shapes in bird's-eye imagery. We present a comprehensive survey of oriented object detection in remote sensing. We categorize existing methodologies into two-stage, single-stage, and transformer-based oriented detectors. We examine boundary discontinuity problems in angular representations, evaluate loss formulations (Gaussian Wasserstein Distance, Probabilistic IoU), and review benchmark datasets (DOTA, DIOR-R, FAIR1M). Finally, we highlight emerging trends connecting oriented detection to Multimodal Large Language Models.

## Key Extracted Contributions
1. Standard angle regression suffers from angular boundary discontinuity (e.g. 0 vs 180 degrees).
2. Gaussian Wasserstein Distance (GWD) loss provides smooth, continuous gradients for rotated bounding boxes.
3. Dense aerial targets require rotated non-maximum suppression (R-NMS) to prevent valid adjacent objects from being suppressed.
