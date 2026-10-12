# Machine Extraction: SEAL: Segment-and-Look for High-Resolution Visual Reasoning

- **BibTeX Key**: `bao2024seal`
- **Authors**: Yushi Bao, Zhilin Yang, Guohao Li
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2407.03920](https://arxiv.org/abs/2407.03920)
- **Code**: https://github.com/THU-Bao/SEAL
- **Category**: 02_active_zoom_and_search
- **Relevance**: 4 / 5 (High Algorithmic Relevance)

## Abstract
Uniform grid slicing cuts through objects and severs topological context. SEAL proposes a 'Segment-and-Look' framework: it uses an open-vocabulary segmenter to locate object clusters and extracts object-centric bounding crops rather than rigid rectangular grids.

## Key Empirical Findings
1. Object-centric cropping eliminates seam fragmentation artifacts.
2. Reduces visual tokens by 55% compared to uniform grid slicing.
3. Requires an accurate upstream segmenter; false negatives in segmentation cause missed crops.

## Authors' Stated Conclusions
Object-aware cropping is fundamentally superior to rigid grid slicing.

## Open Challenges & Future Scope
Unified end-to-end proposal generation and routing.

## Architectural Profile
- **Vision**: SAM Segmenter + CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: Vicuna-7B
- **Tokens**: Variable (Object-dependent)
