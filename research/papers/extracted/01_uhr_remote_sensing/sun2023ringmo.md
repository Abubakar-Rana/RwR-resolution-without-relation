# RingMo: A Remote Sensing Foundation Model with Masked Image Modeling

- **Authors**: Xian Sun, Peijin Wang, Wanxuan Lu, Zicong Zhu, et al.
- **Year**: 2023
- **Venue**: IEEE TGRS 2023
- **arXiv**: 2206.07778
- **URL**: https://arxiv.org/abs/2206.07778
- **BibTeX Key**: `sun2023ringmo`

## Abstract
Foundation models pretrained via self-supervised learning on natural scenes show limited transferability to remote sensing due to the complex visual distributions of Earth surface objects. We introduce RingMo, a foundation model specifically designed for remote sensing using Masked Image Modeling (MIM). RingMo incorporates a patch-incomplete generative objective tailored for overhead imagery with diverse ground sampling distances. Extensive evaluations on 8 downstream benchmarks demonstrate significant improvements in object localization, building extraction, and land-cover mapping.

## Key Extracted Contributions
1. Generative masked pre-training forces the vision encoder to learn dense geometric priors and spatial boundaries.
2. Superior small-object localization compared to contrastive CLIP encoders.
