# Machine Extraction: Oriented RepPoints for Aerial Object Detection

- **BibTeX Key**: `li2024orientedreppoints`
- **Authors**: Wentong Li, Yijie Chen, Kehai Chen, Jianke Zhu
- **Venue**: CVPR 2022 (2022)
- **arXiv**: [2105.11111](https://arxiv.org/abs/2105.11111)
- **Code**: https://github.com/Li-Wentong/OrientedRepPoints
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Aerial Detection)

## Abstract
We present Oriented RepPoints, a point-based aerial object detector. By learning adaptive point sets that dynamically capture spatial extents and geometric boundaries, Oriented RepPoints avoids rigid bounding box constraints and achieves high precision on aerial benchmarks.

## Key Empirical Findings
1. Point sets capture irregular object geometries (e.g. curved bridges, harbor docks) better than boxes.
2. Eliminates angle regression ambiguity.
3. Outperformed bounding box detectors by +2.5 mAP on DOTA.

## Authors' Stated Conclusions
Point-based representation provides richer geometric boundaries than rectangular bounding boxes.

## Open Challenges & Future Scope
Point-based visual prompting in VLMs.

## Architectural Profile
- **Vision**: ResNet-50 with Deformable Convolutions
- **Projector**: Point-to-Box Conversion Head
- **LLM**: None
- **Tokens**: N/A
