# Multi-Resolution Visual Prompting: Dynamic Scale Selection for Vision-Language Models

- **Authors**: Zichen Yu, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2408.13456
- **URL**: https://arxiv.org/abs/2408.13456
- **BibTeX Key**: `yu2024multiresprompt`

## Abstract
We investigate scale sensitivity in Vision-Language Models, discovering that different question types exhibit distinct optimal visual resolution scales: broad relational questions suffer from high-frequency noise at excessive resolutions, whereas fine-grained entity queries fail at low resolutions. We propose Multi-Resolution Visual Prompting (MRVP), which dynamically predicts the optimal resolution scale conditioned on the query prompt. Evaluated across diverse VQA benchmarks, MRVP reduces hallucinations by 24% while cutting visual computation by 45%.

## Key Extracted Contributions
1. High-frequency noise from excessive resolution corrupts relational and spatial reasoning.
2. Dynamic scale selection eliminates over-resolution visual hallucinations.
3. Question syntax contains strong signals for optimal visual scale selection.
