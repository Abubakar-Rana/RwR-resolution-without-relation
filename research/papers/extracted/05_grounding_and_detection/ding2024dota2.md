# DOTA-v2.0: A Large-Scale Dataset for Object Detection in Aerial Images with Oriented Bounding Boxes

- **Authors**: Jian Ding, Nan Xue, Yang Long, Gui-Song Xia, Dengke Shen
- **Year**: 2024
- **Venue**: IEEE TPAMI 2024
- **arXiv**: 2102.12219
- **URL**: https://arxiv.org/abs/2102.12219
- **BibTeX Key**: `ding2024dota2`

## Abstract
Object detection in Earth Observation imagery faces unique challenges absent in natural photography: objects appear from bird's-eye nadir perspectives with arbitrary orientations, extreme aspect ratios (e.g. harbors, bridges, airstrips), and huge scale variations. We present DOTA-v2.0, a comprehensive benchmark for oriented object detection in aerial images. DOTA-v2.0 collects 11,268 ultra-high-resolution aerial images with 1.79 million oriented bounding box (OBB) instances across 18 categories. We evaluate leading oriented detection frameworks and establish standard metrics for aerial object detection.

## Key Extracted Contributions
1. Axis-aligned bounding boxes (AABB) fail on oriented aerial targets (ships at angles, bridges, runways), causing severe IoU overlap errors.
2. Oriented Bounding Boxes (OBB: $(x, y, w, h, \theta)$) provide precise object separation in dense aerial clusters (e.g. parked aircraft, vehicle lots).
3. Remote sensing detectors pre-trained on DOTA achieve over 85% mAP on small aerial infrastructure.
