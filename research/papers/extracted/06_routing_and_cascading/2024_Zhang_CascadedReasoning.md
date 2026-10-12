# Machine Extraction: Cascaded Visual Reasoning: From Fast Heuristics to Deep Analysis

- **BibTeX Key**: `zhang2024cascadedreasoning`
- **Authors**: Hao Zhang, Renjie Pi, Tong Zhang
- **Venue**: NeurIPS 2024 (2024)
- **arXiv**: [2406.11200](https://arxiv.org/abs/2406.11200)
- **Code**: https://github.com/HKUST-KnowComp/CascadedReasoning
- **Category**: 06_routing_and_cascading
- **Relevance**: 4 / 5 (High Architectural Prior)

## Abstract
Inspired by dual-process cognitive theory, we present Cascaded Visual Reasoning. System 1 executes fast feed-forward perception on downscaled images; System 2 executes slow deliberate multi-step crop inspection and chain-of-thought reasoning when System 1 detects ambiguity.

## Key Empirical Findings
1. Dual-process architecture mirrors human perceptual cognitive allocation.
2. Answers 70% of perceptual queries in System 1 (300ms); reserves System 2 (4,000ms) for complex reasoning.
3. Balances cognitive efficiency with reasoning depth.

## Authors' Stated Conclusions
Dual-system visual reasoning balances fast perceptual heuristics with deep deliberate analysis.

## Open Challenges & Future Scope
Unified end-to-end policy learning.

## Architectural Profile
- **Vision**: System 1: ViT-B (Direct) / System 2: ViT-L with crops
- **Projector**: MLP
- **LLM**: System 1: 3B / System 2: 13B + CoT
- **Tokens**: Variable
