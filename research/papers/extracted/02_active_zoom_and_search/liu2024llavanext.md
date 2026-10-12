# LLaVA-NeXT: Improved Reasoning, OCR, and World Knowledge

- **Authors**: Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, Yong Jae Lee
- **Year**: 2024
- **Venue**: Blogpost / Technical Report
- **arXiv**: 2401.17644
- **URL**: https://arxiv.org/abs/2401.17644
- **BibTeX Key**: `liu2024llavanext`

## Abstract
We present LLaVA-NeXT, an evolved family of open-source multimodal models offering enhanced visual reasoning, fine-grained OCR, and broader world knowledge. LLaVA-NeXT introduces an AnyRes dynamic resolution framework that divides arbitrary-resolution images into grids of native-resolution crops alongside a downscaled global thumbnail. Slices are concatenated with delimiter tokens indicating spatial coordinates. LLaVA-NeXT demonstrates superior benchmark gains across MMMU, MathVista, and OCRBench while maintaining high training and inference efficiency.

## Key Extracted Contributions
1. AnyRes dynamic grid tiling (crops + thumbnail) establishes the current state of the art in open-source multimodal architectures.
2. Delimiter tokens (newline and crop separator tokens) provide coarse 2D layout cues to the LLM.
3. Beyond 4-9 crops, context length scaling and attention dilution become severe bottlenecks.
