# Machine Extraction: Cardinal Reasoning: Teaching Models Left, Right, North, and South

- **BibTeX Key**: `tan2024cardinalvlm`
- **Authors**: Sinan Tan, Junyang Lin, Chang Zhou
- **Venue**: arXiv preprint (2024)
- **arXiv**: [2408.09210](https://arxiv.org/abs/2408.09210)
- **Code**: https://github.com/Alibaba-NLP/CardinalVLM
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 4 / 5 (High Domain Prior)

## Abstract
We investigate cardinal versus egocentric spatial reasoning in multimodal LLMs. While humans understand that 'North' aligns with 'Up' in standard aerial maps, VLMs frequently fail to translate 2D image coordinates to cardinal directions, confusing East and West by 48%.

## Key Empirical Findings
1. Models suffer a 48% error rate distinguishing East and West in overhead maps.
2. Egocentric prompts ('is it to the right?') yield higher accuracy than cardinal prompts ('is it to the east?').
3. Prepending an explicit coordinate mapping prompt ('In this map, Up is North, Right is East') recovers +16.2% accuracy.

## Authors' Stated Conclusions
Language models lack intrinsic cardinal grounding; prompt-level coordinate system anchoring is essential.

## Open Challenges & Future Scope
Geographic coordinate pretraining.

## Architectural Profile
- **Vision**: Qwen2-VL native visual encoder
- **Projector**: Native
- **LLM**: Qwen2-7B-Instruct
- **Tokens**: Native
