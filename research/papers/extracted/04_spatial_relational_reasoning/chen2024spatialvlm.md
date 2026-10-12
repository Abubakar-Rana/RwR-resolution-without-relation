# SpatialVLM: Endowing Vision-Language Models with Spatial Reasoning Capabilities

- **Authors**: Boyuan Chen, Zhuo Xu, Sean Kirmani, Brian Ichter, Dorsa Sadigh, Leonidas Guibas, Fei Xia
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2401.12168
- **URL**: https://arxiv.org/abs/2401.12168
- **BibTeX Key**: `chen2024spatialvlm`

## Abstract
While Vision-Language Models (VLMs) excel at high-level semantic tasks like captioning and visual question answering, they struggle with spatial reasoning—such as answering which object is closer, estimating physical distances, or determining qualitative spatial configurations. In this paper, we show that this deficiency stems from the absence of spatial-reasoning data in conventional web-scale pre-training mixtures. We propose SpatialVLM, a framework that endows VLMs with quantitative and qualitative spatial reasoning capabilities. We build an automated synthetic data generation pipeline that extracts 3D spatial relationships from billions of web images and train a spatially-grounded VLM. SpatialVLM demonstrates dramatic gains on spatial VQA benchmarks, robotic manipulation, and spatial commonsense.

## Key Extracted Contributions
1. Standard VLMs (PaLI-X, LLaVA, GPT-4V) score near random guessing on physical distance and 3D spatial relation queries.
2. Standard web pre-training data lacks spatial supervision: captions rarely state physical distances or cardinal coordinates.
3. Explicit spatial pre-training with numerical coordinate prompts dramatically improves spatial relationship reasoning.
