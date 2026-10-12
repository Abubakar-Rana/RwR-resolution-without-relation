# Machine Extraction: High-Resolution RSVQA Benchmark for Earth Observation: A Multi-Task Evaluation

- **BibTeX Key**: `alsubaie2024rsvqahr`
- **Authors**: Nasser Alsubaie, Yakoub Bazi, Farid Melgani
- **Venue**: IEEE JSTARS 2024 (2024)
- **arXiv**: [2402.16430](https://arxiv.org/abs/2402.16430)
- **Code**: https://github.com/RemoteSensingLab/RSVQA-HR-Benchmark
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
We evaluate high-resolution remote sensing visual question answering using a curated dataset of 2048x2048 images. We benchmark standard convolutional and transformer VQA models across object counting and spatial presence.

## Key Empirical Findings
1. Counting accuracy drops precipitously as target density increases.
2. Models rely on statistical scene priors rather than true spatial grounding.

## Authors' Stated Conclusions
High-resolution VQA requires dedicated spatial grounding mechanisms.

## Open Challenges & Future Scope
Testing on multi-modal large language models.

## Architectural Profile
- **Vision**: ResNet-101 / Swin-B
- **Projector**: Bilinear pooling
- **LLM**: None (LSTM / MCAN classifier)
- **Tokens**: N/A
