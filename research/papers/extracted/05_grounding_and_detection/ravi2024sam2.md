# SAM 2: Segment Anything in Images and Videos

- **Authors**: Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman Rabbat, Chloe Rolland, Laura Gustafson, Eric Mintun, Junting Pan, Kalyan Vasudev Alwala, Nicolas Carion, Chao-Yuan Wu, Ross Girshick, Piotr Dollár, Christoph Feichtenhofer
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2408.00714
- **URL**: https://arxiv.org/abs/2408.00714
- **BibTeX Key**: `ravi2024sam2`

## Abstract
We present Segment Anything Model 2 (SAM 2), a foundation model for promptable visual segmentation in images and videos. SAM 2 introduces a unified streaming architecture with a memory module that tracks visual representations across frames and spatial regions. Crucially, SAM 2 features an upgraded Hiera hierarchical vision backbone that runs 6x faster than SAM 1 while improving boundary accuracy. Evaluated across extensive image and video benchmarks, SAM 2 delivers state-of-the-art segmentation quality with real-time throughput.

## Key Extracted Contributions
1. Upgraded Hiera hierarchical backbone achieves 6x faster inference than original SAM ViT-H.
2. Superior boundary fidelity on small and complex structures (canals, bridges, building footprints).
3. Real-time inference makes it viable to segment dozens of candidate objects across UHR tiles in <100ms.
