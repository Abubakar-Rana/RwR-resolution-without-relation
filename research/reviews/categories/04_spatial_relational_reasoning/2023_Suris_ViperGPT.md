# Paper Review: ViperGPT: Visual Inference via Python Execution for Reasoning

| Field | Details |
| :--- | :--- |
| **Authors** | Dídac Surís, Sachit Menon, Carl Vondrick |
| **Institution(s)** | Columbia University |
| **Publication Date / Venue** | 2023 / ICCV 2023 |
| **arXiv ID / Link** | [2303.08128](https://arxiv.org/abs/2303.08128) |
| **Code Repository** | [https://github.com/columbia-ai-robotics/viper](https://github.com/columbia-ai-robotics/viper) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
ViperGPT uses a code-generation LLM to synthesize Python programs that invoke specialized vision APIs (detectors, depth estimators, math functions) to answer complex visual reasoning questions.

---

## 2. Abstract
> "We present ViperGPT, a framework that leverages code-generation models to compose vision-and-language models into subroutines for complex reasoning. Given an image and query, ViperGPT produces Python code that queries specialized perception modules and computes exact mathematical logic."

---

## 3. Key Findings
1. Programmatic execution eliminates VLM arithmetic and spatial orientation errors.
2. Compositional code handles multi-hop relational questions (e.g. 'Is object A left of object B and closer than object C?').
3. Outperforms monolithic end-to-end VLMs on spatial benchmarks without model training.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Decomposing visual reasoning into programmatic subroutines solves spatial relation bottlenecks that defeat monolithic models.

### Future Scope & Unsolved Frontiers
Handling gigapixel image tiling within programmatic execution loops.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `5 / 5` — *Critical Programmatic Prior*

### Relevance Rationale
Direct inspiration for solving spatial relational questions on XLRS-Bench without model fine-tuning.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Programmatic Visual Reasoning**: Translates VQA into executable Python code with vision API calls.
- **Exact Spatial Math**: Calculates coordinates, distances, and orientations via deterministic code.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Gigapixel Tiling Management**: Evaluated on standard single-image benchmarks; no tile selection logic.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Programmatic VQA pioneer; solves spatial reasoning via code.
- **How our inquiry differs**: We apply programmatic reasoning to 8K aerial imagery, pairing it with real-time YOLO-World and dynamic tile routing.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: GLIP / Grounding DINO + CLIP APIs]
    B --> C[Projector: API function calls]
    C --> D[LLM Backbone: Codex / GPT-4]
    D --> E[Predictions: N/A (Code execution)]
```

- **Vision Encoder**: `GLIP / Grounding DINO + CLIP APIs`
- **Cross-Modal Projector**: `API function calls`
- **Language Backbone**: `Codex / GPT-4`
- **Visual Token Budget**: `N/A (Code execution)`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Core Solution Module**: Implement programmatic spatial evaluation in src/spatial/programmatic_eval.py.
- [ ] **Geometric Precision**: Calculate 'left_of', 'north_of', and Euclidean distances using Python Shapely.
