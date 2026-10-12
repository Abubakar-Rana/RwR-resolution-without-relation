#!/usr/bin/env python3
"""Corpus Builder & Literature Synthesizer for VLM Research.

Generates 60 structured paper reviews, BibTeX entries, extracted text,
category indices, and comparative matrix updates across 6 core research categories.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path("d:/projects/research/vlm")

CATEGORIES = {
    "01_uhr_remote_sensing": "Ultra-High-Resolution & Remote Sensing VLMs",
    "02_active_zoom_and_search": "Active Zoom, Guided Visual Search & Dynamic Tiling",
    "03_token_pruning_and_efficiency": "Token Pruning, Efficient Connectors & Compression",
    "04_spatial_relational_reasoning": "Spatial & Relational Reasoning in VLMs",
    "05_grounding_and_detection": "Object Grounding, Detection & Open-Vocabulary Localization",
    "06_routing_and_cascading": "Dynamic Routing, Multi-Resolution & Cascaded VLM Systems",
}

def render_review_markdown(paper: Dict[str, Any]) -> str:
    """Render a comprehensive review conforming to reviews/template.md."""
    adds_list = "\n".join([f"- **{k}**: {v}" for k, v in paper.get("what_it_adds", {}).items()])
    doesnt_add_list = "\n".join([f"- **{k}**: {v}" for k, v in paper.get("what_it_doesnt_add", {}).items()])
    takeaways_list = "\n".join([f"- [ ] **{t['type']}**: {t['detail']}" for t in paper.get("takeaways", [])])
    
    return f"""# Paper Review: {paper['title']}

| Field | Details |
| :--- | :--- |
| **Authors** | {paper['authors']} |
| **Institution(s)** | {paper['institutions']} |
| **Publication Date / Venue** | {paper['year']} / {paper['venue']} |
| **arXiv ID / Link** | [{paper['arxiv_id']}]({paper['url']}) |
| **Code Repository** | [{paper.get('code_url', 'Official/Community Code')}]({paper.get('code_url', paper['url'])}) |
| **Category** | {CATEGORIES[paper['category']]} |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
{paper['summary']}

---

## 2. Abstract
> *"{paper['abstract']}"*

---

## 3. Key Findings
{paper['findings']}

---

## 4. Conclusions & Stated Future Scope
### Stated Conclusions
{paper['conclusions']}

### Future Scope & Unsolved Frontiers
{paper['future_scope']}

---

## 5. Relevance to Our Problem Statement (XLRS-Bench / RwR)
> **Relevance Score**: `{paper['relevance_score']} / 5` — *{paper['relevance_rating']}*

### Detailed Rationale
{paper['relevance_rationale']}

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Strengths)
{adds_list}

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
{doesnt_add_list}

---

## 7. Prior Art & Overlap with Our Approach
- **Did they already solve our problem?**: {paper['prior_art_overlap']}
- **How our inquiry differs from their scope**: {paper['differentiation']}

---

## 8. Technical Deep-Dive & Architecture
- **Vision Tower**: {paper.get('arch_vision', 'Standard ViT')}
- **Projector / Connector**: {paper.get('arch_projector', 'MLP / Resampler')}
- **Language Backbone**: {paper.get('arch_llm', 'Open LLM')}
- **Token Budget / Resolution Handling**: {paper.get('arch_tokens', 'Fixed / Adaptive')}

---

## 9. Actionable Takeaways for Our Codebase & Experiments
{takeaways_list}
"""

def render_bibtex(paper: Dict[str, Any]) -> str:
    """Generate BibTeX entry."""
    return f"""@article{{{paper['bibtex_key']},
  title     = {{{{{paper['title']}}}}},
  author    = {{{paper['authors'].replace(', ', ' and ')}}},
  journal   = {{{paper['venue']}}},
  year      = {{{paper['year']}}},
  eprint    = {{{paper['arxiv_id']}}},
  archivePrefix = {{arXiv}},
  url       = {{{paper['url']}}}
}}
"""
