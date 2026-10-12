# RemoteCLIP: A Vision Language Foundation Model for Remote Sensing

- **Authors**: Fan Liu, Delong Chen, Zhangqing Guan, Xiaocong Zhou, Jialun Zhu, Qiaolin Ye, Lihuo Fu, Jun Zhou
- **Year**: 2024
- **Venue**: IEEE TGRS 2024
- **arXiv**: 2306.11029
- **URL**: https://arxiv.org/abs/2306.11029
- **BibTeX Key**: `liu2024remoteclip`

## Abstract
Vision-language foundation models like CLIP exhibit remarkable zero-shot transfer on natural images, but their features degrade severely when transferred to remote sensing imagery due to extreme scale variations and nadir viewing angles. We propose RemoteCLIP, the first vision-language foundation model tailored for Earth Observation. We curate a large-scale multimodal remote sensing dataset via automated caption expansion and cross-dataset alignment. RemoteCLIP demonstrates state-of-the-art performance across zero-shot classification, cross-modal retrieval, and object localization, establishing a powerful visual representation for downstream remote sensing vision-language applications.

## Key Extracted Contributions
1. Standard OpenAI CLIP features have weak sensitivity to aerial infrastructure and fine-grained land use.
2. RemoteCLIP significantly improves zero-shot retrieval and image-text alignment on aerial benchmarks.
3. RemoteCLIP embeddings provide superior similarity scoring when searching for task-relevant aerial regions.
