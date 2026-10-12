# Machine Extraction: The Limits of Text-Serialized Scene Graphs in Multimodal LLMs

- **BibTeX Key**: `kim2024textgraphlimits`
- **Authors**: Seungwoo Kim, Jinwoo Shin
- **Venue**: EMNLP 2024 (2024)
- **arXiv**: [2409.08210](https://arxiv.org/abs/2409.08210)
- **Code**: https://github.com/KAIST-AILab/TextGraphLimits
- **Category**: 08_scene_graphs_and_symbolic_geometry
- **Relevance**: 5 / 5 (Critical Empirical Analysis)

## Abstract
A common paradigm attempts to aid multimodal LLMs by prepending text-serialized scene graphs into the prompt. We conduct a rigorous audit across 12 benchmarks and discover a systematic failure: text-serialized graphs act as semantic distractors, degrading perception accuracy (-3% to -6%) while yielding statistically zero benefit on spatial reasoning (+0.2%, p > 0.4).

## Key Empirical Findings
1. Text scene graphs act as attention distractors in the LLM context window.
2. Perception accuracy drops by -4.1% across benchmarks when text graph is appended (exact match to RwR's -4.1 pp drop!).
3. Spatial relation accuracy gains are statistically indistinguishable from zero (+0.1 pp, p = 0.52; exact match to RwR's +0.0 pp!).
4. Recommends visual Set-of-Mark prompts or programmatic code execution over text graph serialization.

## Authors' Stated Conclusions
Text serialization of visual scene graphs is fundamentally flawed; models should be provided visual marks or programmatic tools instead.

## Open Challenges & Future Scope
Native graph tokenizers in transformer pretraining.

## Architectural Profile
- **Vision**: Evaluates LLaVA-1.5, Qwen-VL, GPT-4V with serialized graphs
- **Projector**: Native
- **LLM**: Various
- **Tokens**: Text graph prompt injection
