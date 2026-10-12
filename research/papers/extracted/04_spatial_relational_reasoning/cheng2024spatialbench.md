# Spatial-Bench: Benchmarking Spatial Understanding and Cardinal Reasoning in Vision-Language Models

- **Authors**: Kexin Cheng, Tianyi Zhou, et al.
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2404.09234
- **URL**: https://arxiv.org/abs/2404.09234
- **BibTeX Key**: `cheng2024spatialbench`

## Abstract
We introduce Spatial-Bench, a diagnostic benchmark for evaluating spatial understanding in Vision-Language Models across 12 granular spatial relations, including 8 cardinal directions, Euclidean distance comparisons, topological containment, and relative depth. We evaluate over 15 frontier VLMs and observe that model accuracy degrades sharply as spatial complexity increases, with directional reasoning frequently dropping below 35% accuracy. We provide an in-depth error taxonomy categorizing failures into coordinate mislocalization, reference frame confusion, and semantic prior override.

## Key Extracted Contributions
1. Frontier models (GPT-4V, Gemini Pro, LLaVA) perform near chance on 8-way cardinal direction queries.
2. Reference frame confusion (confusing viewer-centric with object-centric perspective) accounts for over 40% of directional errors.
3. Metric distance comparisons degrade severely when objects are distant.
