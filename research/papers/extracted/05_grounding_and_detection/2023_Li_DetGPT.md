# Machine Extraction: DetGPT: Detect What You Need via Reasoning

- **BibTeX Key**: `pi2023detgpt`
- **Authors**: Renjie Pi, Jiahui Gao, Shuhuai Ren, Kehai Chen, Lingpeng Kong, Baobao Chang
- **Venue**: arXiv preprint (2023)
- **arXiv**: [2305.14167](https://arxiv.org/abs/2305.14167)
- **Code**: https://github.com/OptimalScale/DetGPT
- **Category**: 05_grounding_and_detection
- **Relevance**: 4 / 5 (High Reasoning-Detection Prior)

## Abstract
We introduce DetGPT, an open-vocabulary reasoning-based object detector. DetGPT allows users to issue abstract queries; an instruction-tuned LLM parses user intent, deduces concrete object categories, and queries an open-vocabulary detector to localize targets.

## Key Empirical Findings
1. Decoupling reasoning (LLM) from localization (detector) produces robust zero-shot detection of functional concepts.
2. Avoids requiring the VLM to generate coordinates autoregressively.
3. Outperforms unified VLMs on indirect and abstract referring expression detection.

## Authors' Stated Conclusions
Two-stage decoupled reasoning-detection is more flexible and accurate than forcing a monolithic VLM to output coordinates.

## Open Challenges & Future Scope
End-to-end joint training of the reasoning and localization heads.

## Architectural Profile
- **Vision**: Grounding DINO / Open-Vocabulary Detector
- **Projector**: Text query alignment
- **LLM**: LLaMA-7B
- **Tokens**: Text query embeddings
