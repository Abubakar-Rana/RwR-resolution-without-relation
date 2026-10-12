---
name: pedagogical-paper-reviewer
description: Mandatory protocol for conducting and formatting beginner-friendly, jargon-free scientific paper reviews with plain-English glossaries, ELI5 physical analogies, and high-fidelity SVG vector diagrams.
---

# Pedagogical Paper Reviewer Skill

This skill defines the standardized protocol for researching, writing, and presenting academic literature reviews for beginner researchers and collaborators.

## Core Rules

1. **Jargon-Free First Principle**:
   - Every paper review must begin with a **💡 Quick Vocabulary & Plain-English Glossary** table.
   - Define every single abbreviation, acronym, and domain term (e.g., SOTA, VLM, MLLM, UHR, VQA, RoPE, IoU, NMS, ViT, MLP, KV-cache).

2. **ELI5 Real-World Physical Analogy**:
   - Every review must contain a **🧒 Explain Like I'm 5 (The Big Idea in 30 Seconds)** section.
   - Ground the concept in physical reality (e.g. Where's Waldo puzzles, cutting cake slices, microscope vs city map, emergency room triage, moving truck vacuum packing).
   - Accompany the analogy with a high-contrast ASCII diagram illustrating the core idea.

3. **No Raw Flowcharts — High-Fidelity SVGs Only**:
   - Never output unstyled, raw text-based flowcharts.
   - Create a dedicated dark-mode vector SVG diagram stored in `research/docs/assets/papers/<paper_slug>.svg`.
   - Include a clean ASCII architecture diagram and a markdown link to the SVG.

4. **Structured Review Sections**:
   - `Title & Links Header`
   - `💡 Quick Vocabulary & Plain-English Glossary`
   - `🧒 Explain Like I'm 5`
   - `1. Paper Metadata`
   - `2. Key Findings & Discoveries`
   - `3. What It Adds vs. What It Doesn't`
   - `4. How Our Research Differs & Builds On This`
   - `5. Visual Architecture Specification`
   - `6. Actionable Takeaways for Our Codebase & Papers`
