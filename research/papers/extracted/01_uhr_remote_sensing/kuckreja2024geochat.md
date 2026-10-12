# GeoChat: Grounded Large Vision-Language Model for Remote Sensing

- **Authors**: Kartik Kuckreja, Muhammad Sohail Danish, Muzammal Naseer, Abhijit Das, Salman Khan, Fahad Shahbaz Khan
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2311.15826
- **URL**: https://arxiv.org/abs/2311.15826
- **BibTeX Key**: `kuckreja2024geochat`

## Abstract
General-domain Vision-Language Models (VLMs) demonstrate remarkable conversational and reasoning capabilities on natural scenes, but perform poorly on remote sensing imagery due to distinct overhead viewpoints, arbitrary object orientations, and specialized domain semantics. To address this, we present GeoChat, the first grounded large vision-language model tailored for remote sensing. GeoChat can handle various tasks including image-level conversation, complex reasoning, and grounded question answering with bounding boxes. We establish a diverse instruction-following dataset comprising over 500k visual-text pairs derived from multiple Earth Observation datasets. Extensive evaluations demonstrate that GeoChat achieves superior performance on diverse RS benchmarks, significantly outperforming general VLMs.

## Key Extracted Contributions
1. General VLMs (LLaVA-1.5) degrade by over 20% on remote sensing tasks due to viewpoint and scale divergence.
2. Grounded instruction tuning with bounding boxes enables the model to output coordinates $[x_1, y_1, x_2, y_2]$.
3. Pre-training on standard RS datasets creates strong semantic priors for aerial object classes.
