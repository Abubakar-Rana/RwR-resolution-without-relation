# Paper Review: Do As I Can, Not As I Say: Grounding Language in Robotic Affordances

| Field | Details |
| :--- | :--- |
| **Authors** | Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, et al. |
| **Institution(s)** | Google Research, Everyday Robots |
| **Publication Date / Venue** | 2022 / CoRL 2022 |
| **arXiv ID / Link** | [2204.01691](https://arxiv.org/abs/2204.01691) |
| **Code Repository** | [https://say-can.github.io](https://say-can.github.io) |
| **Category** | Embodied AI, 3D Vision-Language & Robot Navigation |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Pioneered SayCan, multiplying language model semantic probabilities $P_{LLM}(a|task)$ by affordance probabilities $P_{afford}(a|s)$ from value functions to select feasible real-world actions.

---

## 2. Abstract
> "Language models understand what is semantically sensible, but not what is physically possible in a given state. SayCan factors decision-making into semantic probability (from an LLM) and affordance probability (from a learned value function), selecting actions that are both useful and feasible."

---

## 3. Key Findings
1. Factoring decisions into semantic prior $\times$ visual affordance prevents physically impossible actions.
2. Achieves 84% execution success on long-horizon mobile manipulation.
3. Grounding language in physical feasibility is essential for real-world reliability.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Semantic plausibility must be multiplicatively gated by physical affordance and sensory feasibility.

### Future Scope & Unsolved Frontiers
Continuous affordance spaces.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `3 / 5` — *Moderate Embodied Prior*

### Relevance Rationale
Theoretical inspiration for our router: multiply question semantic prior by visual detector confidence.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Affordance Gating**: Multiplies LLM probability by physical visual feasibility score.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Remote Sensing**: Everyday Robots mobile manipulator in office kitchens.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Pioneering affordance grounding in LLMs.
- **How our inquiry differs**: We gate VLM generation by detection feasibility on 8K gigapixel remote sensing imagery.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: Value Function CNN from visual state]
    B --> C[Projector: Product of probabilities $P_{LLM} \times P_{afford}$]
    C --> D[LLM Backbone: PaLM-540B]
    D --> E[Predictions: N/A]
```

- **Vision Encoder**: `Value Function CNN from visual state`
- **Cross-Modal Projector**: `Product of probabilities $P_{LLM} \times P_{afford}$`
- **Language Backbone**: `PaLM-540B`
- **Visual Token Budget**: `N/A`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Gating Formula**: Gate zoom decisions: $P(zoom) = P_{router}(need\_zoom | query) \times P_{detector}(object\_present | crop)$.
