# DynamicViT: Efficient Vision Transformers with Dynamic Token Sparsification

- **Authors**: Yongming Rao, Wenliang Zhao, Benlin Liu, Jiwen Lu, Jie Zhou, Cho-Jui Hsieh
- **Year**: 2021
- **Venue**: NeurIPS 2021
- **arXiv**: 2106.02034
- **URL**: https://arxiv.org/abs/2106.02034
- **BibTeX Key**: `rao2021dynamicvit`

## Abstract
Vision Transformers (ViTs) achieve remarkable visual recognition performance but suffer from substantial computational costs due to dense quadratic attention over all spatial patch tokens. We present DynamicViT, a dynamic token sparsification framework for Vision Transformers. DynamicViT introduces lightweight prediction modules at multiple stages of the network that assess token importance and dynamically drop uninformative tokens based on current feature representations. Extensive evaluations on ImageNet show that DynamicViT reduces FLOPs by 31% to 37% while retaining over 99.5% accuracy across ViT and DeiT architectures.

## Key Extracted Contributions
1. Lightweight MLP prediction heads (<0.5% parameters) can accurately rank token importance during inference.
2. Gumbel-Softmax training enables end-to-end differentiable optimization of binary token dropping decisions.
3. Informative tokens concentrate on salient foreground objects, while background patches can be dropped early.
