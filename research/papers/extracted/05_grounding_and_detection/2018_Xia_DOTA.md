# Machine Extraction: DOTA: A Large-Scale Dataset for Object Detection in Aerial Images

- **BibTeX Key**: `xia2018dota`
- **Authors**: Gui-Song Xia, Xiang Bai, Jian Ding, Zhen Zhu, Serge Belongie, Jiebo Luo, Mihai Datcu, Marcello Pelillo, Liangpei Zhang
- **Venue**: CVPR 2018 (2018)
- **arXiv**: [1711.10398](https://arxiv.org/abs/1711.10398)
- **Code**: https://captain-whu.github.io/DOTA/
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Aerial Dataset)

## Abstract
We present DOTA, a large-scale dataset for object detection in aerial images. DOTA contains 2,806 aerial images with 188,282 instances annotated by oriented bounding boxes, addressing the challenges of arbitrary orientations, high aspect ratios, and huge scale variations.

## Key Empirical Findings
1. Standard computer vision detectors fail in aerial imagery due to arbitrary target orientation.
2. Scale variations span from 10 pixels to over 1,000 pixels in the same image.
3. Formulates evaluation metrics for rotated mean Average Precision (mAP).

## Authors' Stated Conclusions
Earth observation imagery requires oriented bounding box representations to handle arbitrary rotational symmetry.

## Open Challenges & Future Scope
Scaling to million-instance datasets (realized in DOTA-v2).

## Architectural Profile
- **Vision**: Faster R-CNN / SSD variants
- **Projector**: N/A
- **LLM**: None
- **Tokens**: N/A
