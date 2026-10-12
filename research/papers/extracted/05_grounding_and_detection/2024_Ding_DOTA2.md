# Machine Extraction: DOTA-v2.0: A Large-Scale Dataset for Object Detection in Aerial Images with Oriented Bounding Boxes

- **BibTeX Key**: `ding2024dota2`
- **Authors**: Jian Ding, Nan Xue, Yang Long, Gui-Song Xia, Dengxin Dai
- **Venue**: IEEE TPAMI 2024 (2024)
- **arXiv**: [2102.12219](https://arxiv.org/abs/2102.12219)
- **Code**: https://captain-whu.github.io/DOTA/
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We introduce DOTA-v2.0, extending DOTA with tiny targets and extreme scale variations. DOTA-v2.0 contains 1.79 million oriented bounding box instances, introducing new categories such as container cranes and airports, establishing a comprehensive aerial benchmark.

## Key Empirical Findings
1. Tiny targets (<10 pixels) comprise 35% of all instances in aerial scenes.
2. Oriented bounding boxes are essential to avoid massive box overlap in dense harbors and airfields.
3. Standard axis-aligned detectors experience up to 40% false merge rates on clustered targets.

## Authors' Stated Conclusions
Oriented representations are mandatory for crowded aerial objects with large aspect ratios.

## Open Challenges & Future Scope
Open-vocabulary oriented detection in MLLMs.

## Architectural Profile
- **Vision**: Oriented R-CNN / RoI Transformer
- **Projector**: Rotated RoIAlign
- **LLM**: None
- **Tokens**: N/A
