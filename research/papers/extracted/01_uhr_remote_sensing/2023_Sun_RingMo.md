# Machine Extraction: RingMo: A Remote Sensing Foundation Model with Masked Image Modeling

- **BibTeX Key**: `sun2023ringmo`
- **Authors**: Xian Sun, Peijin Wang, Wanxuan Lu, Zicong Zhu, Xiaonan Lu, Fanglong Yao, Kun Fu
- **Venue**: IEEE TGRS 2023 (2023)
- **arXiv**: [2206.07778](https://arxiv.org/abs/2206.07778)
- **Code**: https://github.com/AIR-CAS/RingMo
- **Category**: 01_uhr_remote_sensing
- **Relevance**: 3 / 5 (Moderate Prior)

## Abstract
Generative self-supervised learning has revolutionized visual pre-training. We introduce RingMo, a foundation model framework tailored for remote sensing imagery via masked image modeling on multi-sensor, multi-resolution datasets.

## Key Empirical Findings
1. MIM pre-training preserves high-frequency edge information crucial for tiny aerial targets.
2. Significant gains on oriented object detection in cluttered ports and airfields.

## Authors' Stated Conclusions
Masked auto-encoding encourages spatial pattern completion across partial visual context.

## Open Challenges & Future Scope
Multimodal alignment with text instructions.

## Architectural Profile
- **Vision**: ViT-B/16 & ViT-L/16
- **Projector**: N/A
- **LLM**: None
- **Tokens**: N/A
