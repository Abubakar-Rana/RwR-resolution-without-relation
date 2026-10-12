# DetGPT: Detect What You Need via Reasoning

- **Authors**: Renjie Pi, Jiahui Gao, Shuhuai Ren, Ke Shen, Lingpeng Kong, Tong Zhang
- **Year**: 2023
- **Venue**: ACL 2024
- **arXiv**: 2305.14167
- **URL**: https://arxiv.org/abs/2305.14167
- **BibTeX Key**: `li2023detgpt`

## Abstract
Existing open-vocabulary object detectors require users to provide explicit target category names, failing when user queries require abstract reasoning (e.g. 'detect objects that can be used to extinguish a fire'). We present DetGPT, a reasoning-based object detection framework. DetGPT uses a Large Language Model to interpret abstract user instructions, infer implicit target objects and visual attributes, and direct an open-vocabulary detector to localize the inferred entities. DetGPT demonstrates strong zero-shot reasoning-guided detection without requiring task-specific fine-tuning.

## Key Extracted Contributions
1. Decoupling reasoning (LLM) from localization (detector) is strictly superior to forcing an LLM to predict numerical coordinates.
2. LLMs excel at expanding abstract queries into concrete visual search lists (e.g. 'damaged infrastructure' -> 'broken roofs, debris, collapsed walls').
3. Eliminates coordinate hallucination while maintaining semantic flexibility.
