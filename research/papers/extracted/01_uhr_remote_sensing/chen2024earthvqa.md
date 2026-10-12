# EarthVQA: Towards Relational Reasoning for Remote Sensing Visual Question Answering

- **Authors**: Pengfei Chen, Diliyaer Muhtar, Xueliang Lu, et al.
- **Year**: 2024
- **Venue**: IEEE TGRS 2024
- **arXiv**: 2403.04118
- **URL**: https://arxiv.org/abs/2403.04118
- **BibTeX Key**: `chen2024earthvqa`

## Abstract
Visual Question Answering in Earth Observation often requires understanding complex spatial configurations between geographic entities, such as direction, proximity, and containment. Existing RS-VQA datasets predominantly focus on simple object detection and attribute recognition. To bridge this gap, we present EarthVQA, the first benchmark emphasizing complex relational reasoning in remote sensing. EarthVQA comprises over 60,000 question-answer pairs requiring topological, directional, and multi-hop reasoning. We also propose a relational reasoning baseline that constructs spatial scene graphs from segmentation masks and utilizes graph-guided cross-attention. Experiments demonstrate that standard VLMs struggle severely on relational questions without explicit spatial modeling.

## Key Extracted Contributions
1. Standard VLMs score near random chance on directional and topological questions without explicit spatial graph guidance.
2. Scene graphs derived from segmentation masks improve relational reasoning accuracy by 12.3% on standard aerial crops.
3. Cardinal directions (North, South-East) are poorly internalized by standard ViT positional encodings.
