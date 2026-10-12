# Machine Extraction: Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer

- **BibTeX Key**: `shazeer2024outrageouslylargenn`
- **Authors**: Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, Jeff Dean
- **Venue**: ICLR 2017 (2017)
- **arXiv**: [1701.06538](https://arxiv.org/abs/1701.06538)
- **Code**: https://github.com/tensorflow/tensor2tensor
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (Foundational MoE Literature)

## Abstract
We introduce the Sparsely-Gated Mixture-of-Experts layer, realizing 1000x improvements in model capacity with minor computational overhead. A trainable gating network decides a sparse combination of experts to process each input.

## Key Empirical Findings
1. Conditional computation enables massive capacity scaling without proportional compute scaling.
2. Noisy top-k gating ensures balanced expert utilization during training.
3. Foundational paper of modern MoE architectures.

## Authors' Stated Conclusions
Gated conditional routing breaks the coupling between total model capacity and per-sample compute cost.

## Open Challenges & Future Scope
Application to attention layers and multimodal inputs.

## Architectural Profile
- **Vision**: None
- **Projector**: N/A
- **LLM**: LSTM with MoE layers
- **Tokens**: N/A
