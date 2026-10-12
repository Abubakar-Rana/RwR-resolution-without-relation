# Machine Extraction: InstructBLIP: Towards General-purpose Vision-Language Models with Instruction Tuning

- **BibTeX Key**: `dai2023instructblip`
- **Authors**: Wenliang Dai, Junnan Li, Dongxu Li, Anthony Meng Huat Tiong, Junqi Zhao, Weisheng Wang, Boyang Li, Pascale Fung, Steven Hoi
- **Venue**: NeurIPS 2023 (2023)
- **arXiv**: [2305.06500](https://arxiv.org/abs/2305.06500)
- **Code**: https://github.com/salesforce/LAVIS
- **Category**: 03_token_pruning_and_efficiency
- **Relevance**: 4 / 5 (Foundational Q-Former Prior)

## Abstract
We present InstructBLIP, introducing instruction-aware visual feature extraction. By feeding the user instruction into the Q-Former alongside learnable queries, InstructBLIP extracts 32 task-specific visual tokens that adapt dynamically to the query objective.

## Key Empirical Findings
1. Instruction-guided queries extract task-relevant features better than instruction-agnostic resamplers.
2. Generates a compact fixed budget of 32 visual tokens.
3. Compression to 32 tokens discards fine spatial coordinates and background anchors.

## Authors' Stated Conclusions
Instruction conditioning makes token abstractors flexible, but extreme compression impairs spatial localization.

## Open Challenges & Future Scope
Scaling query token count for complex scenes.

## Architectural Profile
- **Vision**: EVA-CLIP ViT-g/14
- **Projector**: Instruction-guided Q-Former (32 tokens)
- **LLM**: Flan-T5-XXL / Vicuna-7B
- **Tokens**: Fixed 32 tokens
