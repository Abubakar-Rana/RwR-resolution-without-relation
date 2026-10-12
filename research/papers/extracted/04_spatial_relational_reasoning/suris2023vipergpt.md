# ViperGPT: Visual Inference via Python Execution for Reasoning

- **Authors**: Dídac Surís, Sachit Menon, Carl Vondrick
- **Year**: 2023
- **Venue**: ICCV 2023
- **arXiv**: 2303.08128
- **URL**: https://arxiv.org/abs/2303.08128
- **BibTeX Key**: `suris2023vipergpt`

## Abstract
Answering complex visual queries requires composing diverse perceptual and spatial operations, including object localization, attribute recognition, spatial relation reasoning, and logical arithmetic. We present ViperGPT, a framework that executes visual reasoning by synthesizing Python programs. Given an input query, an LLM generates a Python script that calls specialized vision modules (e.g. GLIP, Grounding DINO, depth estimators, geometric functions) and uses standard control flow to compose their results into a final answer. ViperGPT achieves state-of-the-art zero-shot performance across complex compositional VQA benchmarks.

## Key Extracted Contributions
1. Programmatic decomposition natively solves multi-hop spatial and counting queries (e.g. 'find all cars inside the red circle').
2. Calling specialized detectors (Grounding DINO) is drastically more reliable than general-purpose VLM bounding box generation.
3. Python arithmetic and geometric functions eliminate counting and spatial relation hallucinations.
