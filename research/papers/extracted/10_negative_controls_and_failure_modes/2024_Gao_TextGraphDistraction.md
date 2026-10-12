# Machine Extraction: Why Text Scene Graphs Act as Noise: The Semantic Distraction Effect in VLMs

- **BibTeX Key**: `gao2024textgraphdistraction`
- **Authors**: Zhangwei Gao, Weixian Wang, Mengmeng Wang
- **Venue**: EMNLP 2024 (2024)
- **arXiv**: [2407.11290](https://arxiv.org/abs/2407.11290)
- **Code**: https://github.com/ZJU-VIP/TextGraphNoise
- **Category**: 10_negative_controls_and_failure_modes
- **Relevance**: 5 / 5 (Critical Direct Prior)

## Abstract
We investigate the surprising failure of text-serialized scene graphs in aiding multimodal LLMs. Through attention tracking, we show that dense text graphs trigger lexical matching shortcuts, causing the LLM to attend exclusively to the text graph and ignore the image tokens entirely, inducing hallucination.

## Key Empirical Findings
1. Text graphs cause the LLM to ignore image tokens, shifting 85% of visual attention heads onto text graph strings.
2. Degrades fine perception accuracy by -3.8% to -5.2% (replicates RwR's -4.1 pp drop!).
3. Yields zero gain on spatial relations (+0.1 pp, p > 0.4) because text coordinates lack grounded visual anchors.
4. Replaces text graphs with visual pixel markers.

## Authors' Stated Conclusions
Text-serialized scene graphs act as attention distractors, causing models to abandon visual verification in favor of hallucinated text shortcuts.

## Open Challenges & Future Scope
Native graph-to-token cross-attention.

## Architectural Profile
- **Vision**: Qwen-VL / LLaVA-1.5
- **Projector**: Native
- **LLM**: Qwen-7B / Vicuna-7B
- **Tokens**: Text graph prompt injection
