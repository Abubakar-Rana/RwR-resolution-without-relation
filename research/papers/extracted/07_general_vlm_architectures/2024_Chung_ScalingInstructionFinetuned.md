# Machine Extraction: Scaling Instruction-Finetuned Language Models

- **BibTeX Key**: `chung2024scalinginstructionfinetuned`
- **Authors**: Hyung Won Chung, Le Hou, Long Yue, Barret Zoph, Yi Tay, William Fedus, Eric Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, Noah Fiedel, Rachel Farber, et al.
- **Venue**: JMLR 2024 (2024)
- **arXiv**: [2210.11416](https://arxiv.org/abs/2210.11416)
- **Code**: https://github.com/google-research/t5x
- **Category**: 07_general_vlm_architectures
- **Relevance**: 3 / 5 (Foundational Instruction Tuning)

## Abstract
We explore instruction finetuning across task scaling, model scaling, and chain-of-thought finetuning. Instruction tuning dramatically improves zero-shot performance across unseen tasks, providing a universal capability boost.

## Key Empirical Findings
1. Instruction tuning across diverse tasks is essential for general zero-shot task generalization.
2. Chain-of-thought (CoT) tuning unlocks multi-step arithmetic and reasoning capabilities.
3. Foundation for all modern instruction-following language backbones.

## Authors' Stated Conclusions
Instruction tuning is the key catalyst converting raw language models into general-purpose task solvers.

## Open Challenges & Future Scope
Multimodal instruction scaling.

## Architectural Profile
- **Vision**: None
- **Projector**: N/A
- **LLM**: Flan-T5 / Flan-PaLM
- **Tokens**: N/A
