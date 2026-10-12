# Machine Extraction: Segment Anything

- **BibTeX Key**: `kirillov2023sam`
- **Authors**: Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi Mao, Chloe Rolland, Laura Gustafson, Tete Xiao, Spencer Whitehead, Alexander C. Berg, Wan-Yen Lo, Piotr Dollar, Ross Girshick
- **Venue**: ICCV 2023 (2023)
- **arXiv**: [2304.02643](https://arxiv.org/abs/2304.02643)
- **Code**: https://github.com/facebookresearch/segment-anything
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (Foundational Segmentation Prior)

## Abstract
We present the Segment Anything project: a new task, model, and dataset for image segmentation. Using an efficient data engine, we collected SA-1B, containing over 1 billion masks. SAM is promptable and adapts zero-shot to diverse segmentation tasks with high precision.

## Key Empirical Findings
1. Promptable mask decoder produces pixel-accurate boundaries in ~50ms given a bounding box prompt.
2. Heavy ViT image encoder (ViT-H) takes ~400ms per image.
3. Enables precise polygon extraction for complex aerial structures (runways, ports, agricultural parcels).

## Authors' Stated Conclusions
Foundation models for promptable segmentation enable zero-shot boundary delineation across diverse visual domains.

## Open Challenges & Future Scope
Video segmentation and continuous multi-modal prompts.

## Architectural Profile
- **Vision**: ViT-H / ViT-L Image Encoder
- **Projector**: Two-way transformer prompt decoder
- **LLM**: None
- **Tokens**: Mask tokens
