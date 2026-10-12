# Mini-Gemini: Mining the Potential of Multi-Modality Vision Language Models

- **Authors**: Yanwei Li, Yuechen Zhang, Chengyao Wang, Zhisheng Zhong, Yixin Chen, Ruihang Chu, Jiaya Jia
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2403.18814
- **URL**: https://arxiv.org/abs/2403.18814
- **BibTeX Key**: `li2024minigemini`

## Abstract
While Large Multimodal Models (LMMs) have achieved significant success, scaling up visual resolution while maintaining efficient inference remains difficult. We present Mini-Gemini, a simple yet effective framework that boosts multi-modality capability across high-resolution perception and reasoning. Mini-Gemini employs a dual-stream vision pipeline: a high-resolution visual branch extracts detailed local candidate features, while a low-resolution branch provides global semantic queries. A cross-attention patch mining module merges high-resolution details into low-resolution tokens, keeping the sequence length compact while preserving fine-grained details.

## Key Extracted Contributions
1. Using low-resolution tokens as queries to attend over high-resolution detail tokens compresses sequence length without losing details.
2. Preserving global overview tokens prevents the model from losing scene layout.
3. Generates high-fidelity bounding boxes and dense descriptions at reduced token counts.
