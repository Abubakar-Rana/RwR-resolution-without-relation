# Machine Extraction: SAM 2: Segment Anything in Images and Videos

- **BibTeX Key**: `ravi2024sam2`
- **Authors**: Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rabbat, Chloe Rolland, Laura Gustafson, Eric Mintun, Junting Pan, Kalyan Vasudev Alwala, Nicolas Carion, Chao-Yuan Wu, Ross Girshick, Piotr Dollar, Christoph Feichtenhofer
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2408.00714](https://arxiv.org/abs/2408.00714)
- **Code**: https://github.com/facebookresearch/segment-anything-2
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (High Efficiency Segmentation)

## Abstract
We present SAM 2, a foundation model for promptable visual segmentation in images and videos. Built with a memory architecture and hierarchical vision backbone (Hiera), SAM 2 achieves real-time inference speed (44 FPS) while outperforming SAM 1 across image benchmarks.

## Key Empirical Findings
1. SAM 2 image encoder is 6x faster than SAM 1 (Hiera backbone vs ViT-H).
2. Significantly sharper mask boundaries on tiny cluttered objects.
3. Streaming memory enables multi-temporal satellite change detection.

## Authors' Stated Conclusions
Hierarchical backbones (Hiera) dramatically accelerate promptable segmentation without losing accuracy.

## Open Challenges & Future Scope
Multi-modal audio-visual prompting.

## Architectural Profile
- **Vision**: Hiera Hierarchical Vision Transformer
- **Projector**: Memory attention + Mask decoder
- **LLM**: None
- **Tokens**: Memory tokens
