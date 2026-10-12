# Machine Extraction: Context Severance: Quantifying Edge Seam Artifacts in Grid-Based Image Slicing

- **BibTeX Key**: `chen2024uniformtilingfailure`
- **Authors**: Liang Chen, Haozhe Zhao, Baobao Chang
- **Venue**: ECCV 2024 (2024)
- **arXiv**: [2408.04512](https://arxiv.org/abs/2408.04512)
- **Code**: https://github.com/pkunlp-icler/ContextSeverance
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Failure Analysis)

## Abstract
Grid-based image tiling is standard practice for high-resolution vision models, but its topological impact is rarely audited. We show that uniform grid slicing severs 22.4% of objects across tile boundaries, creating catastrophic fragmentation that destroys spatial continuity and object counting accuracy.

## Key Empirical Findings
1. Uniform grid slicing cuts through 22.4% of objects in dense scenes (exact match to RwR's 22% seam audit!).
2. Severed objects produce double-counting or false negative detections in downstream models.
3. Destroys spatial orientation vectors that cross tile seams.
4. Recommends object-centric padding (15% margin) or continuous overlapping strides.

## Authors' Stated Conclusions
Rigid grid slicing inherently fragments 20%+ of visual entities; margin padding and object-centric cropping are mandatory.

## Open Challenges & Future Scope
Non-Euclidean dynamic tiling.

## Architectural Profile
- **Vision**: Evaluates standard grid slicing across ViT models
- **Projector**: N/A
- **LLM**: None
- **Tokens**: Grid slices
