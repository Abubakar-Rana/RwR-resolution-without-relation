# Machine Extraction: Vision Language Models are Blind

- **BibTeX Key**: `rahmanzadehgervi2024vlmsareblind`
- **Authors**: Pooya Rahmanzadehgervi, Logan Caracci, Mohammad Reza Taesiri, Anh Totti Nguyen
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2407.06581](https://arxiv.org/abs/2407.06581)
- **Code**: https://github.com/Pooya-rg/VLMsAreBlind
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
We show that state-of-the-art VLMs are remarkably blind to simple low-level geometric and spatial properties. On simple synthetic tasks such as identifying whether two lines intersect, counting concentric circles, or detecting which point is closer to a line, frontier models frequently fail, behaving like 'blind' statistical text models.

## Key Empirical Findings
1. Frontier VLMs fail on elementary 2D geometry (line intersection, circle containment, relative distance).
2. Models guess based on semantic language biases rather than visual inspection.
3. Increasing image resolution does not resolve these geometric failures.

## Authors' Stated Conclusions
Modern visual tokenizers and cross-attention architectures discard exact metric geometry and topological connectivity.

## Open Challenges & Future Scope
Developing geometric inductive biases for multimodal models.

## Architectural Profile
- **Vision**: Evaluates GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Qwen2-VL
- **Projector**: Proprietary / MLP
- **LLM**: Frontier LLM backbones
- **Tokens**: Native
