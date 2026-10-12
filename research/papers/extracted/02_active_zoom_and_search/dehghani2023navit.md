# Patch n' Pack: NaViT, a Vision Transformer for Any Aspect Ratio and Resolution

- **Authors**: Mostafa Dehghani, Basil Mustafa, Josip Djolonga, Jonathan Heek, Matthias Minderer, Mathilde Caron, Andreas Steiner, Joan Puigcerver, Robert Geirhos, Ibrahim Alabdulmohsin, Neil Houlsby
- **Year**: 2023
- **Venue**: NeurIPS 2023
- **arXiv**: 2307.06304
- **URL**: https://arxiv.org/abs/2307.06304
- **BibTeX Key**: `dehghani2023navit`

## Abstract
The ubiquitous computer vision convention of resizing images to fixed square resolutions introduces severe geometric distortions, discards aspect-ratio information, and limits operational flexibility. We introduce NaViT (Native Resolution ViT), which breaks this convention using 'Patch n' Pack'. NaViT treats images as variable-length sequences of patches and packs multiple patches from different images and crops into single training sequences using masked self-attention. NaViT can ingest arbitrary aspect ratios and resolutions natively during both training and inference. Across extensive image classification, retrieval, and VLM benchmarks, NaViT achieves significantly higher throughput, flexibility, and accuracy.

## Key Extracted Contributions
1. Resizing to square inputs distorts natural visual aspect ratios and hurts recognition of long/thin structures (bridges, rivers, roads).
2. Sequence packing completely eliminates padding token waste during batch processing.
3. Enables continuous resolution scaling at inference time without architectural changes.
