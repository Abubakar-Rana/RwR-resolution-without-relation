# Machine Extraction: Set-of-Mark Prompting Unleashes Extraordinary Visual Grounding in GPT-4V

- **BibTeX Key**: `yang2023setofmark`
- **Authors**: Jianwei Yang, Hao Zhang, Feng Li, Xueyan Zou, Chunyuan Li, Jianfeng Gao
- **Venue**: arXiv preprint (2023)
- **arXiv**: [2310.11441](https://arxiv.org/abs/2310.11441)
- **Code**: https://github.com/microsoft/SoM
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 5 / 5 (Critical Grounding Prior)

## Abstract
We present Set-of-Mark (SoM) prompting to unleash visual grounding in large multimodal models. By overlaying distinctive marks (e.g., numbers, alphabets, masks, boxes) on image regions, SoM allows the model to reference objects by visual ID tags rather than hallucinated text coordinates.

## Key Empirical Findings
1. SoM increases visual grounding accuracy in GPT-4V by +20% to +35% across diverse benchmarks.
2. Completely eliminates coordinate hallucination in language models.
3. Enables seamless spatial reasoning (e.g. 'Object [1] is northwest of Object [2]').

## Authors' Stated Conclusions
Visual pixel marking is fundamentally superior to text coordinate generation for grounding in multimodal LLMs.

## Open Challenges & Future Scope
Automating mark generation in high-density multi-object scenes.

## Architectural Profile
- **Vision**: GPT-4V / Qwen-VL with pixel prompt overlays
- **Projector**: Native
- **LLM**: GPT-4V / Qwen2.5-VL
- **Tokens**: Native
