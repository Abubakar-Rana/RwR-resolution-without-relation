# Resolution-Aware Vision Transformers: When to Zoom and When to Glance

- **Authors**: Dong Wang, Haoliang Wang, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2405.09112
- **URL**: https://arxiv.org/abs/2405.09112
- **BibTeX Key**: `wang2024resolutionaware`

## Abstract
Human observers dynamically modulate cognitive resolution depending on task demands: scene classification requires a broad 'glance', whereas counting small vehicles demands a focused 'zoom'. In this work, we investigate Resolution-Aware Vision Transformers for Earth Observation. We demonstrate that forcing all aerial queries through high-resolution zoomed pipelines introduces high-frequency noise and destroys macro-scale spatial awareness. We propose a Dual-Paced Vision framework that routes broad queries to a global glance pathway and fine queries to a local zoom pathway. On remote sensing benchmarks, Dual-Paced processing outperforms static high-resolution processing by 4.8% while reducing FLOPs by 52%.

## Key Extracted Contributions
1. Forcing macro-scale land-use and spatial queries through zoomed crops introduces high-frequency noise that confuses models.
2. Dual-paced architecture (Glance vs Zoom) outperforms static high-resolution models on both macro and micro tasks.
3. Validates that global overview representations possess unique contextual signals absent in zoomed crops.
