# Machine Extraction: Grounded SAM: Marrying Grounding DINO with Segment Anything

- **BibTeX Key**: `zheng2024groundedsam`
- **Authors**: Tianhe Ren, Shilong Liu, Ailing Zeng, Jing Lin, Kexin Zheng, Hao Zhang, Feng Li, Jianwei Yang, Hongyang Li, Qing Jiang, Lei Zhang
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2401.14159](https://arxiv.org/abs/2401.14159)
- **Code**: https://github.com/IDEA-Research/Grounded-Segment-Anything
- **Category**: 05_grounding_and_detection
- **Relevance**: 5 / 5 (Critical Integration Prior)

## Abstract
We present Grounded SAM, marrying Grounding DINO and Segment Anything. By using Grounding DINO's open-set text-to-box detection to prompt SAM's class-agnostic mask generation, Grounded SAM creates a powerful zero-shot pipeline for detecting, segmenting, and grounding any object specified by text.

## Key Empirical Findings
1. Cascading Grounding DINO boxes into SAM produces pixel-accurate open-vocabulary masks zero-shot.
2. Enables seamless generation of visual mark overlays (masks, outlines, tags) on arbitrary images.
3. Standard pipeline for automatic Set-of-Mark annotation.

## Authors' Stated Conclusions
Cascading an open-vocabulary detector with a class-agnostic segmenter creates the ultimate open-world visual grounding tool.

## Open Challenges & Future Scope
Real-time edge optimization (achieved by replacing components with YOLO-World and SAM-2).

## Architectural Profile
- **Vision**: Swin-B (Grounding DINO) + ViT-H (SAM)
- **Projector**: Box-to-prompt bridge
- **LLM**: None (External pipeline)
- **Tokens**: N/A
