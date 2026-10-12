# Machine Extraction: Neuro-Symbolic Spatial Reasoning over Aerial Imagery

- **BibTeX Key**: `mao2024neurosymbolicspatial`
- **Authors**: Jiayuan Mao, Xueliang Lu, Joshua B. Tenenbaum
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2407.05432](https://arxiv.org/abs/2407.05432)
- **Code**: https://github.com/jiayuanm/aerial-neurosymbolic
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 5 / 5 (Critical Programmatic Prior)

## Abstract
We present a neuro-symbolic framework for aerial spatial reasoning. Neural open-vocabulary detectors extract grounded object bounding boxes, and a symbolic spatial DSL (Domain-Specific Language) executes geometric spatial queries (cardinal directions, distance bounds, polygon containment) with mathematical certainty.

## Key Empirical Findings
1. Symbolic DSL eliminates hallucination and guarantees mathematical spatial correctness.
2. Reaches 94.2% accuracy on complex aerial spatial queries where end-to-end VLMs score <40%.
3. Entire pipeline executes in <250ms when paired with fast open-vocabulary detectors.

## Authors' Stated Conclusions
Neuro-symbolic separation (neural detection + symbolic spatial execution) is the optimal paradigm for aerial spatial reasoning.

## Open Challenges & Future Scope
Handling ambiguous queries and imperfect detections.

## Architectural Profile
- **Vision**: YOLO-World + Grounding DINO
- **Projector**: Symbolic DSL
- **LLM**: Codex / Python Execution
- **Tokens**: N/A
