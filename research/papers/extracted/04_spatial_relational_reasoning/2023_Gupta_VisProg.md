# Machine Extraction: Visual Programming: Compositional Visual Reasoning Without Training

- **BibTeX Key**: `gupta2023visprog`
- **Authors**: Tanmay Gupta, Aniruddha Kembhavi
- **Venue**: CVPR 2023 (2023)
- **arXiv**: [2211.11559](https://arxiv.org/abs/2211.11559)
- **Code**: https://github.com/allenai/visprog
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Programmatic Prior)

## Abstract
We present VisProg, a neuro-symbolic approach to complex and compositional visual tasks without task-specific training. VisProg prompts an LLM to generate 2-step Python-like visual programs that invoke CV models, image filters, and geometric calculations.

## Key Empirical Findings
1. In-context program generation achieves SOTA on compositional visual reasoning (GQA, NLVR2).
2. Step-by-step execution provides complete interpretability.
3. Failures are easily debugged to either program generation or specific vision tool errors.

## Authors' Stated Conclusions
Neuro-symbolic program synthesis sidesteps the reasoning limitations of monolithic vision-language transformers.

## Open Challenges & Future Scope
Dynamic replanning upon tool execution failure.

## Architectural Profile
- **Vision**: ViLD / MDETR / OpenCV
- **Projector**: Tool interfaces
- **LLM**: GPT-3 (text-davinci-003)
- **Tokens**: N/A
