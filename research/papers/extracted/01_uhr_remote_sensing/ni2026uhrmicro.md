# UHR-Micro: Diagnosing and Mitigating the Resolution Illusion in Earth Observation VLMs

- **Authors**: Shuai Ni, Zhenghang Yuan, Chenxi Ge, et al.
- **Year**: 2026
- **Venue**: arXiv preprint
- **arXiv**: 2605.12237
- **URL**: https://arxiv.org/abs/2605.12237
- **BibTeX Key**: `ni2026uhrmicro`

## Abstract
The increasing resolution of Earth Observation (EO) sensors has spurred efforts to evaluate Vision-Language Models on ultra-high-resolution imagery. However, does increasing input resolution truly enable MLLMs to perceive microscopic details and reason about spatial interactions? In this paper, we identify and diagnose the 'Resolution Illusion' in Earth Observation VLMs: nominal accuracy gains from higher resolutions often stem from benchmark distribution shifts and semantic coarse-level priors rather than genuine grounded perception of small targets. We construct UHR-Micro, a targeted diagnostic probe consisting of paired high-resolution satellite scenes with controlled micro-target perturbations and spatial relation swaps. Evaluating state-of-the-art models reveals that while zooming enhances confidence, it frequently hallucinates object attributes and severes inter-object spatial alignments.

## Key Extracted Contributions
1. Discovers the 'Resolution Illusion': models gain confidence on zoomed crops but frequently confabulate relationships.
2. Documents severe position bias: models default to specific multiple-choice letters when uncertain in large scenes.
3. Micro-targets (<32x32 pixels) suffer from severe feature distortion even in high-resolution ViT patch tokenization.
