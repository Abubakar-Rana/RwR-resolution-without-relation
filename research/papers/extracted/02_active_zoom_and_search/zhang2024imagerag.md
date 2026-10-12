# Enhancing Ultra High Resolution Remote Sensing Imagery Analysis with ImageRAG

- **Authors**: Zhiqiang Zhang, Hao Shen, Tao Zhao, Zhangqing Guan, Bo Chen, Yuting Wang, Xiao Jia, Yong Cai, Yuhui Shang, Jianwei Yin
- **Year**: 2024
- **Venue**: arXiv preprint
- **arXiv**: 2411.07688
- **URL**: https://arxiv.org/abs/2411.07688
- **BibTeX Key**: `zhang2024imagerag`

## Abstract
Ultra-high-resolution remote sensing imagery contains billions of pixels, rendering direct end-to-end VLM ingestion computationally intractable. Drawing inspiration from text Retrieval-Augmented Generation, we introduce ImageRAG, a framework that models UHR image analysis as visual evidence retrieval. ImageRAG indexes high-resolution tiles using visual-semantic embeddings and retrieves the top-k most relevant patches conditioned on user queries. The retrieved visual evidence is then provided alongside a low-resolution scene overview to a generative VLM. Benchmark results on aerial VQA show that ImageRAG cuts visual token consumption by 72% while outperforming global downsampling by 9.3%.

## Key Extracted Contributions
1. Modeling high-resolution tiles as retrievable documents enables massive token reduction.
2. Dual-index retrieval (combining text-image similarity and visual saliency) outperforms either signal alone.
3. Fails when evidence requires multi-hop reasoning between distantly retrieved tiles.
