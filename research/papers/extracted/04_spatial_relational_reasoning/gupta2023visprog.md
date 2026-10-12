# Visual Programming: Compositional Visual Reasoning Without Training

- **Authors**: Tanmay Gupta, Aniruddha Kembhavi
- **Year**: 2023
- **Venue**: CVPR 2023
- **arXiv**: 2211.11559
- **URL**: https://arxiv.org/abs/2211.11559
- **BibTeX Key**: `gupta2023visprog`

## Abstract
We present VisProg (Visual Programming), a neuro-symbolic approach to compositional visual problem-solving without training. VisProg uses an in-context LLM to map natural language queries into 2D modular visual programs. Each program step invokes one of a suite of specialized computer vision models or mathematical modules, passing intermediate visual and structured outputs to subsequent steps. VisProg achieves strong performance across complex compositional VQA, visual math, and directional spatial queries while providing complete interpretability.

## Key Extracted Contributions
1. Multi-step compositional queries fail when executed as a single monolithic VLM call.
2. Decomposing complex queries into discrete steps (Locate -> Crop -> Inspect -> Compare) dramatically reduces error propagation.
3. Produces fully explainable visual audit trails.
