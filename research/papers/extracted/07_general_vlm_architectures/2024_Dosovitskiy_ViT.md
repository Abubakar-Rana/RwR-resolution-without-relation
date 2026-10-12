# Machine Extraction: An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale

- **BibTeX Key**: `dosovitskiy2024vit`
- **Authors**: Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, Jakob Uszkoreit, Neil Houlsby
- **Venue**: ICLR 2021 (2021)
- **arXiv**: [2010.11929](https://arxiv.org/abs/2010.11929)
- **Code**: https://github.com/google-research/vision_transformer
- **Category**: 07_general_vlm_architectures
- **Relevance**: 5 / 5 (Foundational Vision Transformer Origin)

## Abstract
While the Transformer architecture has become the de-facto standard for NLP, applications to computer vision remain limited. We show that a pure transformer applied directly to sequences of image patches performs very well on image classification when pretrained at sufficient scale.

## Key Empirical Findings
1. Slicing images into 16x16 patches maps 2D images directly into 1D token sequences.
2. Self-attention scales effectively with compute and dataset size (JFT-300M).
3. Lacks convolutional inductive biases, requiring heavy pre-training to learn 2D locality.

## Authors' Stated Conclusions
Pure attention over image patches replaces hand-crafted convolutional inductive biases when scaled.

## Open Challenges & Future Scope
Dynamic resolution, arbitrary aspect ratios, and vision-language integration.

## Architectural Profile
- **Vision**: ViT-Base / ViT-Large / ViT-Huge
- **Projector**: Linear patch projection
- **LLM**: None
- **Tokens**: $14 \times 14 = 196$ patch tokens
