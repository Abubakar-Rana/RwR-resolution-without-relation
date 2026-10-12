# Machine Extraction: Advancing Plain Vision Transformer Towards Remote Sensing Multimodal Understanding

- **BibTeX Key**: `wang2023advancingrsvl`
- **Authors**: Di Wang, Jing Zhang, Bo Du, Dacheng Tao
- **Venue**: IEEE TGRS 2023 (2023)
- **arXiv**: [2303.14681](https://arxiv.org/abs/2303.14681)
- **Code**: https://github.com/whu-adv/PlainViT-RS
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
Hierarchical vision transformers like Swin introduce spatial inductive biases but discard fine coordinate granularity. We demonstrate that plain ViTs with windowed attention and simple feature pyramids excel in remote sensing detection.

## Key Empirical Findings
1. Plain ViTs retain fine spatial localization better than hierarchical token-pooling transformers.
2. Preserves sub-pixel boundary information for small vehicles.

## Authors' Stated Conclusions
Maintaining constant spatial resolution throughout transformer layers prevents spatial coordinate blur.

## Open Challenges & Future Scope
Integration into autoregressive language models.

## Architectural Profile
- **Vision**: Plain ViT-B/16 & ViT-L/16
- **Projector**: FPN
- **LLM**: None
- **Tokens**: Variable
