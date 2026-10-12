# Machine Extraction: Lost in the Middle: How Language Models Use Long Contexts and Positional Bias

- **BibTeX Key**: `zhang2024positionbiasllm`
- **Authors**: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
- **Venue**: TACL 2024 (2024)
- **arXiv**: [2307.03172](https://arxiv.org/abs/2307.03172)
- **Code**: https://github.com/nelson-liu/lost-in-the-middle
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 4 / 5 (Foundational Positional Bias)

## Abstract
We evaluate language model retrieval across long input contexts. We find that performance degrades drastically when relevant information is located in the middle of long contexts, exhibiting a U-shaped accuracy curve.

## Key Empirical Findings
1. Performance exhibits an extreme U-shaped curve across input context position.
2. Information placed in the middle of a 4K-8K token prompt suffers up to 30% lower retrieval accuracy.
3. Direct impact on multi-crop visual sequences: middle tiles are frequently ignored.

## Authors' Stated Conclusions
Transformer attention decoders suffer from severe middle-position degradation in long context windows.

## Open Challenges & Future Scope
Positional bias mitigation.

## Architectural Profile
- **Vision**: None (Text prompt evaluation)
- **Projector**: N/A
- **LLM**: GPT-3.5-Turbo, Claude, MPT-30B
- **Tokens**: Long text sequences (1K to 16K)
