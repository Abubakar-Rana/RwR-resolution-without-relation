# Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V

- **Authors**: Jianwei Yang, Hao Zhang, Feng Li, Xueyan Zou, Chunyuan Li, Jianfeng Gao
- **Year**: 2023
- **Venue**: arXiv preprint
- **arXiv**: 2310.11441
- **URL**: https://arxiv.org/abs/2310.11441
- **BibTeX Key**: `yang2023som`

## Abstract
We present Set-of-Mark (SoM), a simple yet powerful visual prompting method to unleash the extraordinary visual grounding capabilities of Large Multimodal Models (LMMs) like GPT-4V. Instead of asking LMMs to predict numerical coordinate boxes, SoM uses off-the-shelf interactive segmentation models (like SAM) to partition the image into visual regions and overlays distinct alphanumeric marks (e.g. [1], [2], [A], [B]) or colored contours on them. The LMM then references entities using their visual mark IDs. SoM dramatically outperforms coordinate-based prompting across fine-grained visual grounding, spatial relational reasoning, and object attribute identification.

## Key Extracted Contributions
1. Numerical coordinate prediction ($[x_1, y_1, x_2, y_2]$) in VLMs is highly error-prone and brittle.
2. Overlaying visual marks (numbers/letters) directly into pixel space grounds attention firmly on targets.
3. Enables VLMs to reason unambiguously about spatial relationships by referencing visual mark IDs (e.g. 'Is [1] north of [2]?').
