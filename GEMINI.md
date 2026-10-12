# GEMINI.md — Mandatory Pedagogical & Beginner-Friendly Research Protocol

This document establishes the **permanent operational law** for all AI models (Gemini, Antigravity, Claude, Codex, GPT, Cursor) operating within this Vision-Language Model (VLM) research workspace.

---

## 🎓 The Prime Directive: Jargon-Free, Beginner-Accessible Teaching

The primary researcher and collaborators require **crystal-clear, accessible, and intuitive scientific communication**. You must never write in dense academic shorthand without first laying an intuitive conceptual foundation.

Every document, paper review, architecture specification, and analytical summary must strictly satisfy the following **Four Pillars of Pedagogy**:

---

### Pillar 1: Mandatory Plain-English Glossary
**Rule**: Before presenting technical findings, you must define EVERY acronym, abbreviation, and specialized technical term in an easy-to-read table.
- **Never drop unexplained acronyms**: (e.g. SOTA, VLM, MLLM, UHR, VQA, RoPE, IoU, NMS, ViT, MLP, KV-cache, FPS).
- **Format**:
  | Abbreviation | Full Name | What It Actually Means In Plain English |
  | :--- | :--- | :--- |
  | **VLM** | **Vision-Language Model** | An AI with eyes that can look at pictures and chat about them in everyday English. |
  | **SOTA** | **State-Of-The-Art** | The world-champion, highest-scoring AI models that exist today. |

---

### Pillar 2: "Explain Like I'm 5" (ELI5) Physical Analogies
**Rule**: Every technical review and system design document MUST include a dedicated `## 🧒 Explain Like I'm 5 (The Big Idea in 30 Seconds)` section.
- **Ground in physical reality**: Use intuitive, everyday real-world physical analogies (e.g., sheet cake slices, city map vs. magnifying glass, Where's Waldo puzzle, medical triage nurse, luggage vacuum packing).
- **Include an ASCII visual block**: Accompany the analogy with a simple, high-contrast ASCII diagram illustrating the failure mode or solution visually before introducing mathematical equations or tensors.

---

### Pillar 3: Visual Presentation & High-Fidelity Vector Graphics
**Rule**: **Zero crude, unstyled, single-node flowcharts.**
- Never paste raw, unstyled mermaid code blocks in Section 8 or 5 of reviews.
- Every paper review must have a dedicated, beautifully styled dark-mode SVG vector schematic stored in [`research/docs/assets/papers/<paper_slug>.svg`](file:///d:/projects/research/vlm/research/docs/assets/papers/).
- The markdown review must feature a clean ASCII pipeline diagram and a direct, clickable markdown link to the SVG file.

---

### Pillar 4: Actionable Translational Impact
**Rule**: Every paper review must explicitly bridge theory to our codebase and manuscript:
1. **How Our Research Differs**: A side-by-side comparison table contrasting the reviewed paper's approach against our research.
2. **Actionable Takeaways**: Concrete, numbered instructions specifying:
   - What architectural module to adopt or avoid in [`work/src/`](file:///d:/projects/research/vlm/work/src/).
   - What baseline to compare against in [`work/experiments/`](file:///d:/projects/research/vlm/work/experiments/).
   - How to cite and position the paper in our manuscript drafts.

---

## 🗂️ Strict Directory Taxonomy (3 Top-Level Folders)
Never dump files at the root directory. Maintain the strict 3-folder layout:
- `work/`: Code, experiments, submissions, and original paper PDFs.
- `research/`: Reviews, master knowledge base, vector assets, and synthesis indices.
- `archive/`: Deprecated notes, agent scratchpads, and historical drafts.
