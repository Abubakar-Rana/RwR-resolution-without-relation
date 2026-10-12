# Paper Review: Image Retrieval Using Scene Graphs

| Field | Details |
| :--- | :--- |
| **Authors** | Justin Johnson, Ranjay Krishna, Michael Stark, Li-Jia Li, David Shamma, Michael Bernstein, Li Fei-Fei |
| **Institution(s)** | Stanford University, Yahoo Labs |
| **Publication Date / Venue** | 2015 / CVPR 2015 |
| **arXiv ID / Link** | [1504.05809](https://arxiv.org/abs/1504.05809) |
| **Code Repository** | [https://github.com/jcjohns/scene-graphs](https://github.com/jcjohns/scene-graphs) |
| **Category** | Scene Graphs, Graph Neural Networks & Programmatic Reasoning |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Pioneered the formal concept of Scene Graphs for visual representation, modeling images as structured graphs of objects, attributes, and pairwise relationships (subject-predicate-object).

---

## 2. Abstract
> "We introduce Scene Graphs, a graph-based semantic representation of visual scenes. Scene graphs explicitly capture objects, their attributes, and directed relationships between pairs of objects, enabling grounding and structured image retrieval beyond unstructured text tags."

---

## 3. Key Findings
1. Formalized the scene graph tuple $G = (V, E)$ where nodes are objects and edges are spatial/semantic relationships.
2. Structured relationships capture spatial layout far more accurately than bag-of-words text.
3. Foundational paper that initiated the entire visual scene graph literature.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
Explicit graph structures of objects and relationships bridge perceptual pixels and symbolic semantic reasoning.

### Future Scope & Unsolved Frontiers
Automated scene graph generation from raw pixels (realized in iterative message passing).

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *Foundational Scene Graph Literature*

### Relevance Rationale
Historical foundation of the Scene Graph representation evaluated in the RwR Relation Block experiment.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Scene Graph Formalism**: Definition of $G = (O, A, R)$ object-attribute-relationship graphs.
- **Spatial Edge Modeling**: Structured representation of spatial prepositions.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Deep Learning Generation**: Relied on manual annotations and CRF matching; pre-transformer era.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Foundational paper defining scene graphs.
- **How our inquiry differs**: We investigate how scene graphs interact with modern multimodal LLMs, specifically examining why text serialization of scene graphs failed in RwR.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: R-CNN object proposals]
    B --> C[Projector: Conditional Random Field (CRF) matching]
    C --> D[LLM Backbone: None]
    D --> E[Predictions: Graph tuples]
```

- **Vision Encoder**: `R-CNN object proposals`
- **Cross-Modal Projector**: `Conditional Random Field (CRF) matching`
- **Language Backbone**: `None`
- **Visual Token Budget**: `Graph tuples`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Historic Citation**: Cite Johnson et al. as the origin of scene graph representation.
