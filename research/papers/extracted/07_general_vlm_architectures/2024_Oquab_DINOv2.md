# Machine Extraction: DINOv2: Learning Robust Visual Features without Supervision

- **BibTeX Key**: `oquab2024dinov2`
- **Authors**: Maxime Oquab, Timothee Darcet, Theo Moutakanni, Huy Vo, Marc Szafraniec, Vasil Khalidov, Pierre Fernandez, Daniel Haziza, Francisco Massa, Alaaeldin El-Nouby, Russell Howes, Po-Yao Huang, Hu Xu, Vasu Sharma, Shang-Wen Li, Jaewon Tompson, et al.
- **Venue**: TMLR 2024 (2024)
- **arXiv**: [2304.07193](https://arxiv.org/abs/2304.07193)
- **Code**: https://github.com/facebookresearch/dinov2
- **Category**: 07_general_vlm_architectures
- **Relevance**: 5 / 5 (Critical Vision Foundation Model)

## Abstract
We present DINOv2, training high-capacity Vision Transformers on curated unlabelled data. DINOv2 visual features demonstrate remarkable out-of-the-box spatial and geometric properties, excelling at dense prediction (depth estimation, semantic segmentation) zero-shot.

## Key Empirical Findings
1. DINOv2 patch features preserve spatial geometry and dense correspondence vastly better than CLIP.
2. Patch embeddings naturally cluster by semantic part without supervision.
3. Does not suffer from CLIP's spatial semantic collapse in deep layers.

## Authors' Stated Conclusions
Self-supervised discriminative pretraining (DINOv2) retains rich spatial geometry that contrastive language supervision (CLIP) discards.

## Open Challenges & Future Scope
Unified DINOv2 + language alignment.

## Architectural Profile
- **Vision**: DINOv2 ViT-L/14 & ViT-g/14 with Register Tokens
- **Projector**: Linear / Attention
- **LLM**: None
- **Tokens**: Native
