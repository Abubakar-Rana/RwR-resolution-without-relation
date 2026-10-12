# Machine Extraction: Visual Shortcut Learning in Vision-Language Models: An Empirical Study

- **BibTeX Key**: `qian2024visualshortcutlearning`
- **Authors**: Yuan Qian, Siyuan Huang, Tianhe Ren
- **Venue**: CVPR 2024 (2024)
- **arXiv**: [2405.09112](https://arxiv.org/abs/2405.09112)
- **Code**: https://github.com/THU-Qian/ShortcutLearning
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 3 / 5 (Diagnostic Shortcut Analysis)

## Abstract
We audit visual shortcut learning in MLLMs. We demonstrate that models frequently rely on superficial background textures (e.g., asphalt texture to predict 'car') rather than detecting and verifying physical object shapes, failing when objects appear in unusual contexts.

## Key Empirical Findings
1. 38% of VLM object predictions are driven by background context textures rather than object pixels.
2. Masking the object entirely leaves model predictions unchanged in 35% of cases.
3. Explains why models produce confident wrong answers on ambiguous tiles.

## Authors' Stated Conclusions
Multimodal models heavily rely on background texture shortcuts rather than physical object verification.

## Open Challenges & Future Scope
Causal feature attribution.

## Architectural Profile
- **Vision**: CLIP ViT-L/14
- **Projector**: MLP
- **LLM**: LLaVA-1.5
- **Tokens**: 576 tokens
