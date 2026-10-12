# Paper Review: EarthMark: Grounded Remote Sensing Multi-Task Vision-Language Model

| Field | Details |
| :--- | :--- |
| **Authors** | Liang Zhao, Pengfei Chen, Haoyu Dong, Bo Du |
| **Institution(s)** | Wuhan University |
| **Publication Date / Venue** | 2025 / CVPR 2025 |
| **arXiv ID / Link** | [2501.07823](https://arxiv.org/abs/2501.07823) |
| **Code Repository** | [https://github.com/WHU-Geo/EarthMark](https://github.com/WHU-Geo/EarthMark) |
| **Category** | Ultra-High-Resolution & Remote Sensing VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
EarthMark adapts Set-of-Mark visual prompting to remote sensing imagery, overlaying visual numeric identifiers on detected aerial structures to allow the VLM to reason over marked objects directly.

---

## 2. Abstract
> "Grounding objects in remote sensing via text coordinates is error-prone. EarthMark overlays visual mark identifiers directly onto detected buildings, ships, and roads, enabling the language model to reference specific physical objects unambiguously in dialogue."

---

## 3. Key Findings
1. Visual mark prompts increase spatial relational reasoning accuracy by +12.4% over text bounding box coordinates.
2. Eliminates coordinate hallucination in complex aerial scenes.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Marking objects directly on pixel canvases sidesteps the language model's coordinate parsing deficit.

### Future Scope & Unsolved Frontiers
Automating real-time open-vocabulary mark generation on gigapixel images.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Domain Prior*

### Relevance Rationale
Provides direct validation for our proposed Set-of-Mark grounding solution in RwR.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Set-of-Mark for Aerial Imagery**: Adapts visual identifier overlays to dense overhead scenes.
- **Empirical Gain**: +12.4% on spatial relational reasoning over text box baseline.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Real-Time Detection**: Relies on pre-extracted offline annotations; does not integrate real-time fast detector.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Applies Set-of-Mark to remote sensing, validating our architectural direction.
- **How our inquiry differs**: We pair real-time YOLO-World open-vocabulary detection with Set-of-Mark within a dynamic router.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Qwen-VL visual encoder with visual prompt overlays]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: Qwen-VL-Chat]
    D --> E[Predictions: 1,024 tokens]
```

- **Vision Encoder**: `Qwen-VL visual encoder with visual prompt overlays`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `Qwen-VL-Chat`
- **Visual Token Budget**: `1,024 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Core Solution**: Implement Set-of-Mark overlay in src/grounding/set_of_mark.py.
- [ ] **Validation**: Confirm that visual marks replace noisy text coordinate strings.
