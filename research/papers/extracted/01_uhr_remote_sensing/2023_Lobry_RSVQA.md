# Machine Extraction: RSVQA: Visual Question Answering for Remote Sensing Data

- **BibTeX Key**: `lobry2023rsvqa`
- **Authors**: Sylvain Lobry, Diego Marcos, Jesse Murray, Devis Tuia
- **Venue**: IEEE TGRS 2023 (2023)
- **arXiv**: [1903.02040](https://arxiv.org/abs/1903.02040)
- **Code**: https://github.com/S-Lobry/RSVQA
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 3 / 5 (Moderate Prior / Foundational)

## Abstract
We introduce the task of Visual Question Answering for remote sensing data (RSVQA). We construct two datasets: one based on low-resolution Sentinel-2 data (10m) and one on high-resolution aerial data (15cm), defining baseline benchmarks.

## Key Empirical Findings
1. Proves feasibility of VQA on overhead remote sensing data.
2. Identifies class imbalance and question template overfitting as major hazards.

## Authors' Stated Conclusions
Remote sensing VQA requires both fine visual acuity and geographic context.

## Open Challenges & Future Scope
Extending to open-ended conversational models.

## Architectural Profile
- **Vision**: ResNet-152
- **Projector**: Element-wise product
- **LLM**: None (GRU decoder)
- **Tokens**: N/A
