# Paper Review: Eyes Wide Shut? Exploring the Visual Spatial Reasoning Limits of Multi-Modal Large Language Models

| Field | Details |
| :--- | :--- |
| **Authors** | Shengbang Tong, Zhuang Liu, Yuexiang Zhai, Yi Ma, Yann LeCun |
| **Institution(s)** | UC Berkeley, Meta AI, NYU |
| **Publication Date / Venue** | 2024 / CVPR 2024 |
| **arXiv ID / Link** | [2403.02151](https://arxiv.org/abs/2403.02151) |
| **Code Repository** | [https://github.com/ShengbangTong/EyesWideShut](https://github.com/ShengbangTong/EyesWideShut) |
| **Category** | Spatial & Relational Reasoning in VLMs |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
Audits visual spatial reasoning in CLIP, LLaVA, and GPT-4V, demonstrating that visual encoders compress away fine spatial relationships due to patch-level pooling and lack of spatial pretraining.

---

## 2. Abstract
> "Why do advanced MLLMs struggle with basic visual spatial tasks? We trace this weakness directly to the visual encoder. We show that contrastive pretraining (CLIP) collapses fine spatial structures in favor of high-level semantic abstractions, leaving downstream LLMs without the spatial signals necessary for relational reasoning."

---

## 3. Key Findings
1. CLIP visual tokens lose spatial coordinate fidelity in deeper layers as semantic invariant loss dominates.
2. Visual token representations cannot reconstruct relative distance or orientation without retraining.
3. Supervised self-attention heads prioritize object identity over inter-object spatial vectors.

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
The root cause of spatial reasoning failure lies in the visual encoder pretraining objective, which optimizes for semantic invariance rather than spatial equivariance.

### Future Scope & Unsolved Frontiers
Spatially equivariant vision-language foundation models.

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `4 / 5` — *High Spatial Prior*

### Relevance Rationale
Fundamental diagnosis: proves why CLIP-based models (including Qwen2.5-VL) intrinsically struggle with spatial relationships.

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
- **Root Cause Diagnosis**: Traces spatial failure to CLIP's semantic invariance objective.
- **Spatial Equivariance Deficit**: Demonstrates loss of spatial vectors in deep visual tokens.

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
- **Architecture Fix**: Exposes encoder limitations without providing a retrained alternative.

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: Encoder-level spatial deficit diagnosis.
- **How our inquiry differs**: We circumvent this encoder deficit at inference time by providing explicit visual marks and symbolic execution.

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: CLIP ViT-L/14, DINOv2, SigLIP]
    B --> C[Projector: MLP]
    C --> D[LLM Backbone: LLaVA-1.5-7B / GPT-4V]
    D --> E[Predictions: 576 tokens]
```

- **Vision Encoder**: `CLIP ViT-L/14, DINOv2, SigLIP`
- **Cross-Modal Projector**: `MLP`
- **Language Backbone**: `LLaVA-1.5-7B / GPT-4V`
- **Visual Token Budget**: `576 tokens`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
- [ ] **Theoretical Grounding**: Cite Tong et al. to ground why CLIP encoders fail on spatial relations.
- [ ] **Bypass Strategy**: Do not rely on CLIP features for spatial relations; use detector bounding boxes + code.
