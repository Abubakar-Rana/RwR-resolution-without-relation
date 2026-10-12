# GeoLLaVA-8K: Scaling Remote-Sensing Multimodal Large Language Models to 8K Resolution

- **Authors**: Fangrun Wang, Mengxi Chen, Yuting Wang, Dong Wang, Haoliang Wang, Zichen Guo, Zheng Wang, Bo Shan, Lin Lan, Yihua Wang, Heng Wang, Wen Yang, Bo Du, Jiaming Zhang
- **Year**: 2025
- **Venue**: arXiv preprint
- **arXiv**: 2505.21375
- **URL**: https://arxiv.org/abs/2505.21375
- **BibTeX Key**: `wang2025geollava8k`

## Abstract
While multimodal large language models demonstrate impressive visual reasoning, scaling them to ultra-high-resolution remote sensing imagery (exceeding 8192x8192 pixels) is severely constrained by quadratic attention complexity. Prior approaches rely on either aggressive downsampling or heuristic tiling, both suffering severe information loss. In this work, we propose GeoLLaVA-8K, a framework capable of natively processing 8K remote sensing images. We introduce Anchored Token Selection (ATS), which identifies critical foreground visual tokens guided by multi-scale anchors, and Background Token Pruning (BTP) to filter redundant geospatial textures. Furthermore, we construct GeoInstruct-8K, a high-quality instruction-tuning dataset spanning diverse geospatial scenarios. Empirical results demonstrate that GeoLLaVA-8K surpasses existing open-source remote sensing VLMs by 8.4% on high-resolution benchmarks while reducing token redundancy by 65%.

## Key Extracted Contributions
1. Processing 8K imagery directly generates over 16,000 visual tokens without pruning, exceeding GPU memory limits.
2. Background Token Pruning safely discards 65% of tokens in uniform regions (water, desert, homogeneous canopy) with minimal accuracy penalty.
3. Anchored Token Selection focuses attention on small targets like vessels and isolated structures.
