# InternVL: Scaling up Vision Foundation Models and Aligning for Generic Visual-Linguistic Tasks

- **Authors**: Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, Bin Li, Ping Luo, Tong Lu, Yu Qiao, Jifeng Dai
- **Year**: 2024
- **Venue**: CVPR 2024
- **arXiv**: 2312.14238
- **URL**: https://arxiv.org/abs/2312.14238
- **BibTeX Key**: `chen2024internvl`

## Abstract
We introduce InternVL, an open-source vision foundation model scaled up to 6 billion parameters and aligned with Large Language Models. To efficiently ingest high-resolution images, InternVL introduces a dynamic high-resolution strategy combined with a Pixel Shuffle spatial compression projector. Specifically, every 2x2 grid of adjacent visual patch tokens is reshuffled along the channel dimension and projected through a single linear layer, reducing token count by 4x while strictly preserving 2D spatial topology. InternVL achieves state-of-the-art results across numerous multimodal benchmarks, outperforming proprietary models on document understanding, OCR, and visual perception.

## Key Extracted Contributions
1. Pixel Shuffle ($2\times 2$ unshuffle) reduces visual token counts by 4x ($75\%$ reduction) while strictly preserving 2D relative spatial topology.
2. Pixel Shuffle dramatically outperforms simple average pooling and strided convolutions on OCR and fine-grained spatial grounding.
3. Enables ingesting 4K+ resolution images within standard 4,096 token context windows.
