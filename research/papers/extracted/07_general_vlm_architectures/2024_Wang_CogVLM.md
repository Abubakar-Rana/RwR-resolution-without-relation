# Machine Extraction: CogVLM: Visual Expert for Large Language Models

- **BibTeX Key**: `wang2024cogvlm`
- **Authors**: Weihan Wang, Qingsong Lv, Wenyi Hong, Ji Qi, Yan Wang, Junhui Ji, Zhuoyi Yang, Lei Zhao, Xixuan Song, Jiale Cheng, Bin Xu, Jie Tang
- **Venue**: NIPS 2023 (2024)
- **arXiv**: [2311.03079](https://arxiv.org/abs/2311.03079)
- **Code**: https://github.com/THUDM/CogVLM
- **Category**: 07_general_vlm_architectures
- **Relevance**: 4 / 5 (Foundational Deep Fusion Architecture)

## Abstract
We present CogVLM, a powerful open-source visual language foundation model. Unlike shallow-projector architectures (LLaVA), CogVLM incorporates deep visual expert blocks into every transformer layer, achieving deep cross-modal fusion and SOTA visual grounding.

## Key Empirical Findings
1. Deep expert fusion outperforms shallow MLP projectors by +8.5% on visual grounding benchmarks.
2. Preserves spatial coordinate awareness throughout all transformer layers.
3. Doubles memory requirement for LLM feedforward layers.

## Authors' Stated Conclusions
Deep per-layer visual adaptation preserves spatial signals that shallow projectors fail to propagate.

## Open Challenges & Future Scope
Sparse visual expert routing (achieved in MoE-LLaVA).

## Architectural Profile
- **Vision**: EVA-02-CLIP-E/14
- **Projector**: Visual Expert Layers inside LLM
- **LLM**: Vicuna-7B with Visual Experts
- **Tokens**: 1,225 tokens
