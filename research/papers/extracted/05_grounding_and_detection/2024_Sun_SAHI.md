# Machine Extraction: SAHI: Slicing Aided Hyper Inference for Small Object Detection

- **BibTeX Key**: `sun2024sahi`
- **Authors**: Fatih Cagatay Akyon, Sinan Onur Altinuc, Alptekin Temizel
- **Venue**: ICIP 2022 (2022)
- **arXiv**: [2202.06934](https://arxiv.org/abs/2202.06934)
- **Code**: https://github.com/obss/sahi
- **Category**: 05_grounding_and_detection
- **Relevance**: 5 / 5 (Critical Engineering Solution)

## Abstract
Small object detection in ultra-high-resolution imagery fails when entire images are downscaled. SAHI introduces slicing-aided hyper inference, partitioning massive images into overlapping slices, executing standard object detectors on slices and the full image, and merging bounding boxes back to global coordinates using Non-Maximum Merging.

## Key Empirical Findings
1. Slicing-aided inference boosts small object detection mAP by +6.8% to +14.5% across diverse detectors.
2. Overlapping slices (e.g. 20% overlap) prevent objects on patch borders from being severed.
3. Non-Maximum Merging (NMM) accurately reconstructs global coordinates for sliced detections.

## Authors' Stated Conclusions
Slicing with overlapping margins and global coordinate merging is the standard engineering solution for small object detection on massive images.

## Open Challenges & Future Scope
Adaptive non-uniform slicing.

## Architectural Profile
- **Vision**: Compatible with any detector (YOLOv8, Grounding DINO, MMDetection)
- **Projector**: N/A
- **LLM**: None
- **Tokens**: N/A
