# FrugalVLM: Cost-Effective Cascaded Inference for Multimodal Foundation Models

- **Authors**: Lingjiao Chen, Matei Zaharia, James Zou
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2404.14567
- **URL**: https://arxiv.org/abs/2404.14567
- **BibTeX Key**: `chen2024frugalvlm`

## Abstract
Deploying high-resolution multimodal foundation models is cost-prohibitive for high-throughput visual applications. We propose FrugalVLM, an adaptive cascaded inference framework for vision-language tasks. FrugalVLM executes a staged inference strategy: queries are first evaluated by a fast, low-resolution multimodal model; if the output confidence or entropy satisfies a learned threshold, the answer is returned immediately. Queries that exhibit high visual ambiguity are escalated to a high-resolution, multi-crop model. On extensive visual QA benchmarks, FrugalVLM cuts computational cost and latency by up to 73% while matching or improving upon the accuracy of always using the most expensive model.

## Key Extracted Contributions
1. Cascading from low-resolution to high-resolution captures the best of both worlds.
2. Over 65% of visual queries are resolved correctly by low-resolution overviews alone.
3. Output token entropy and top-1 vs top-2 logit margin provide reliable signals for cascading escalation.
