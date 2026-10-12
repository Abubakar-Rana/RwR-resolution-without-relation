# Paper Review: Inner Monologue: Embodied Reasoning through Planning with Language Models

| Field | Details |
| :--- | :--- |
| **Authors** | Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, Brian Ichter |
| **Institution(s)** | Google Research |
| **Publication Date / Venue** | 2022 / CoRL 2022 |
| **arXiv ID / Link** | [2207.05608](https://arxiv.org/abs/2207.05608) |
| **Code Repository** | [https://innermonologue-robot.github.io](https://innermonologue-robot.github.io) |
| **Category** | Embodied AI, 3D Vision-Language & Robot Navigation |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Introduces continuous feedback loops for LLM planning via 'inner monologues', where environment perception models and success detectors feed observations back to the LLM to trigger replanning.

---

## 2. Abstract
> "We investigate how environment feedback enables LLMs to perform embodied reasoning. By injecting perceptual feedback (success detection, scene description) back into the prompt history as an 'inner monologue', the model corrects mistakes and replans dynamically."

---

## 3. Key Findings
1. Closed-loop perceptual feedback increases task completion rate from 32% to 78%.
2. Language models adapt plans when environmental obstacles are reported.
3. Prevents compounding execution errors.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Perceptual feedback loops are essential for robust long-horizon reasoning and error recovery.

### Future Scope & Unsolved Frontiers
Hierarchical multi-agent dialogue.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Embodied Prior*

### Relevance Rationale
Relevant for multi-stage visual exploration: if a tile crop fails to answer the question, replan and zoom elsewhere.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Closed-Loop Perceptual Feedback**: Environment perception feeds back into the prompt for dynamic replanning.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **High-Resolution Aerial Tiling**: Indoor tabletop and kitchen robots.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Feedback loops for LLM planning.
- **How our inquiry differs**: We apply closed-loop verification to test if candidate crops contain queried objects before finalizing answers.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: ViLD / CLIP Object Detectors]
    B --> C[Projector: Textual environment descriptions]
    C --> D[LLM Backbone: InstructGPT / PaLM]
    D --> E[Predictions: Multi-turn prompt history]
```

- **Vision Encoder**: `ViLD / CLIP Object Detectors`
- **Cross-Modal Projector**: `Textual environment descriptions`
- **Language Backbone**: `InstructGPT / PaLM`
- **Visual Token Budget**: `Multi-turn prompt history`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Verification Loop**: If candidate crop has zero detections, fall back to global overview automatically.
