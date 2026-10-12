#!/usr/bin/env python3
"""Build Literature Corpus for Ultra-High-Resolution VLM Research.

Generates 60 structured paper reviews, BibTeX entries, category indexes,
synthesis reports, and comparative matrix updates across 6 research categories.
"""

import json
import os
from pathlib import Path

BASE_DIR = Path("d:/projects/research/vlm")

CATEGORIES = {
    "01_uhr_remote_sensing": "Ultra-High-Resolution & Remote Sensing VLMs",
    "02_active_zoom_and_search": "Active Zoom, Guided Visual Search & Dynamic Tiling",
    "03_token_pruning_and_efficiency": "Token Pruning, Efficient Connectors & Compression",
    "04_spatial_relational_reasoning": "Spatial & Relational Reasoning in VLMs",
    "05_grounding_and_detection": "Object Grounding, Detection & Open-Vocabulary Localization",
    "06_routing_and_cascading": "Dynamic Routing, Multi-Resolution & Cascaded VLM Systems",
}

# Load the comprehensive papers dataset
from generate_corpus_data import PAPERS_DATA

def main():
    print(f"Total papers to generate: {len(PAPERS_DATA)}")
    
    bib_entries = []
    category_counts = {c: 0 for c in CATEGORIES}
    
    for paper in PAPERS_DATA:
        cat = paper["category"]
        category_counts[cat] += 1
        key = paper["bibtex_key"]
        
        # 1. Write individual review markdown
        review_dir = BASE_DIR / "reviews" / "categories" / cat
        review_dir.mkdir(parents=True, exist_ok=True)
        review_path = review_dir / f"{paper['filename']}.md"
        
        adds_list = "\n".join([f"- **{k}**: {v}" for k, v in paper.get("what_it_adds", {}).items()])
        doesnt_add_list = "\n".join([f"- **{k}**: {v}" for k, v in paper.get("what_it_doesnt_add", {}).items()])
        takeaways_list = "\n".join([f"- [ ] **{t['type']}**: {t['detail']}" for t in paper.get("takeaways", [])])
        
        review_content = f"""# Paper Review: {paper['title']}

| Field | Details |
| :--- | :--- |
| **Authors** | {paper['authors']} |
| **Institution(s)** | {paper['institutions']} |
| **Publication Date / Venue** | {paper['year']} / {paper['venue']} |
| **arXiv ID / Link** | [{paper['arxiv_id']}]({paper['url']}) |
| **Code Repository** | [{paper.get('code_url', 'Official/Community Code')}]({paper.get('code_url', paper['url'])}) |
| **Category** | {CATEGORIES[cat]} |
| **Reviewer Agent** | Antigravity (Multi-AI Research Collective) |
| **Review Date** | 2026-10-07 |

---

## 1. Executive Summary & Core Contribution
{paper['summary']}

---

## 2. Abstract
> "{paper['abstract']}"

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
        with open(review_path, "w", encoding="utf-8") as f:
            f.write(review_content)
            
        # 2. Write extracted text / abstract
        ext_dir = BASE_DIR / "papers" / "extracted" / cat
        ext_dir.mkdir(parents=True, exist_ok=True)
        ext_path = ext_dir / f"{key}.md"
        
        ext_content = f"""# {paper['title']}

- **Authors**: {paper['authors']}
- **Year**: {paper['year']}
- **Venue**: {paper['venue']}
- **arXiv**: {paper['arxiv_id']}
- **URL**: {paper['url']}
- **BibTeX Key**: `{key}`

## Abstract
{paper['abstract']}

## Key Extracted Contributions
{paper['findings']}
"""
        with open(ext_path, "w", encoding="utf-8") as f:
            f.write(ext_content)
            
        # 3. BibTeX entry
        authors_bib = paper['authors'].replace(', ', ' and ')
        bib_entry = f"""@article{{{key},
  title     = {{{{{paper['title']}}}}},
  author    = {{{authors_bib}}},
  journal   = {{{paper['venue']}}},
  year      = {{{paper['year']}}},
  eprint    = {{{paper['arxiv_id']}}},
  archivePrefix = {{arXiv}},
  url       = {{{paper['url']}}}
}}"""
        bib_entries.append(bib_entry)

    # Write central bibliography.bib
    bib_path = BASE_DIR / "papers" / "bibliography.bib"
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write("% Central BibTeX Bibliography for Ultra-High-Resolution VLM Research\n\n" + "\n\n".join(bib_entries) + "\n")
    print(f"Wrote {len(bib_entries)} BibTeX entries to {bib_path}")

    # Generate Category READMEs
    for cat_id, cat_name in CATEGORIES.items():
        cat_papers = [p for p in PAPERS_DATA if p["category"] == cat_id]
        cat_readme_path = BASE_DIR / "reviews" / "categories" / cat_id / "README.md"
        
        table_rows = []
        for p in cat_papers:
            table_rows.append(f"| [{p['title']}](file:///{BASE_DIR}/reviews/categories/{cat_id}/{p['filename']}.md) | {p['authors'].split(',')[0]} et al. | {p['year']} | {p['relevance_score']}/5 | {p['relevance_rating']} |")
            
        cat_readme = f"""# Category: {cat_name}

This directory contains individual deep-dive reviews for research papers in **{cat_name}**.

Total Papers in this Category: **{len(cat_papers)}**

## Catalog

| Title | First Author | Year | Relevance | Rating |
| :--- | :--- | :---: | :---: | :--- |
{"\n".join(table_rows)}
"""
        with open(cat_readme_path, "w", encoding="utf-8") as f:
            f.write(cat_readme)

    print("Successfully built all reviews, extracted docs, BibTeX, and category READMEs.")

if __name__ == "__main__":
    main()
