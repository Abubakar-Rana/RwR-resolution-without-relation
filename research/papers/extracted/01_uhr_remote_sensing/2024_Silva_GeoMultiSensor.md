# Machine Extraction: Multi-Sensor Geospatial Alignment for Earth Observation Vision-Language Models

- **BibTeX Key**: `silva2024geomultisensor`
- **Authors**: Gabriel Silva, Tiago Pereira, Rodrigo Rocha
- **Venue**: Remote Sensing 2024 (2024)
- **arXiv**: [2408.05190](https://arxiv.org/abs/2408.05190)
- **Code**: https://github.com/INPE-Lab/GeoMultiSensor
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 2 / 5 (Tangential / Domain Specific)

## Abstract
We explore multi-sensor alignment between SAR and optical imagery using multimodal contrastive learning. The resulting model enables text-based land use queries across cloud-covered regions.

## Key Empirical Findings
1. SAR features disambiguate flooded vegetation under dense canopy.
2. Text-to-SAR alignment is lower quality than text-to-optical.

## Authors' Stated Conclusions
Multi-sensor alignment requires distinct projection heads per sensor type.

## Open Challenges & Future Scope
Extending to hyperspectral imagery.

## Architectural Profile
- **Vision**: ResNet-50 + Dual ViT
- **Projector**: Cosine head
- **LLM**: None
- **Tokens**: N/A
