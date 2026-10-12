# Machine Extraction: ViperGPT: Visual Inference via Python Execution for Reasoning

- **BibTeX Key**: `suris2023vipergpt`
- **Authors**: Dídac Surís, Sachit Menon, Carl Vondrick
- **Venue**: ICCV 2023 (2023)
- **arXiv**: [2303.08128](https://arxiv.org/abs/2303.08128)
- **Code**: https://github.com/columbia-ai-robotics/viper
- **Category**: 04_spatial_relational_reasoning
- **Relevance**: 5 / 5 (Critical Programmatic Prior)

## Abstract
We present ViperGPT, a framework that leverages code-generation models to compose vision-and-language models into subroutines for complex reasoning. Given an image and query, ViperGPT produces Python code that queries specialized perception modules and computes exact mathematical logic.

## Key Empirical Findings
1. Programmatic execution eliminates VLM arithmetic and spatial orientation errors.
2. Compositional code handles multi-hop relational questions (e.g. 'Is object A left of object B and closer than object C?').
3. Outperforms monolithic end-to-end VLMs on spatial benchmarks without model training.

## Authors' Stated Conclusions
Decomposing visual reasoning into programmatic subroutines solves spatial relation bottlenecks that defeat monolithic models.

## Open Challenges & Future Scope
Handling gigapixel image tiling within programmatic execution loops.

## Architectural Profile
- **Vision**: GLIP / Grounding DINO + CLIP APIs
- **Projector**: API function calls
- **LLM**: Codex / GPT-4
- **Tokens**: N/A (Code execution)
