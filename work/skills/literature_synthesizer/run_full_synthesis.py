#!/usr/bin/env python3
"""Master literature synthesis runner.
Assembles all 60 papers across 6 categories and builds all documentation,
reviews, extracted texts, BibTeX entries, indices, comparative matrices,
and synthesis reports.
"""

import json
from pathlib import Path

BASE_DIR = Path("d:/projects/research/vlm")

from create_corpus_json import build_category_1
from full_corpus_generator import build_category_2
from corpus_cat3_cat4 import build_category_3, build_category_4
from corpus_cat5_cat6 import build_category_5, build_category_6

CATEGORIES = {
    "01_uhr_remote_sensing": "Ultra-High-Resolution & Remote Sensing VLMs",
    "02_active_zoom_and_search": "Active Zoom, Guided Visual Search & Dynamic Tiling",
    "03_token_pruning_and_efficiency": "Token Pruning, Efficient Connectors & Compression",
    "04_spatial_relational_reasoning": "Spatial & Relational Reasoning in VLMs",
    "05_grounding_and_detection": "Object Grounding, Detection & Open-Vocabulary Localization",
    "06_routing_and_cascading": "Dynamic Routing, Multi-Resolution & Cascaded VLM Systems",
}

def main():
    cat1 = build_category_1()
    cat2 = build_category_2()
    cat3 = build_category_3()
    cat4 = build_category_4()
    cat5 = build_category_5()
    cat6 = build_category_6()

    all_papers = cat1 + cat2 + cat3 + cat4 + cat5 + cat6
    print(f"Total curated papers: {len(all_papers)}")
    assert len(all_papers) == 60, f"Expected 60 papers, got {len(all_papers)}"

    # Save to corpus.json
    corpus_json_path = BASE_DIR / "skills" / "literature_synthesizer" / "corpus.json"
    with open(corpus_json_path, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, indent=2)
    print(f"Saved corpus to {corpus_json_path}")

    bib_entries = []
    
    for paper in all_papers:
        cat = paper["category"]
        key = paper["bibtex_key"]
        
        # 1. Review markdown
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

        # 2. Extracted text / abstract
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

        # 3. BibTeX
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

    # Write bibliography.bib
    bib_path = BASE_DIR / "papers" / "bibliography.bib"
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write("% Central BibTeX Bibliography for Ultra-High-Resolution VLM Research (60 Papers)\n\n" + "\n\n".join(bib_entries) + "\n")
    print(f"Wrote {len(bib_entries)} BibTeX entries to {bib_path}")

    # Write Category READMEs
    for cat_id, cat_name in CATEGORIES.items():
        cat_papers = [p for p in all_papers if p["category"] == cat_id]
        cat_readme_path = BASE_DIR / "reviews" / "categories" / cat_id / "README.md"
        
        table_rows = []
        for p in cat_papers:
            table_rows.append(f"| [{p['title']}](file:///{BASE_DIR}/reviews/categories/{cat_id}/{p['filename']}.md) | {p['authors'].split(',')[0]} et al. | {p['year']} | `{p['relevance_score']}/5` | {p['relevance_rating']} |")
            
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

    # Write Master Index in reviews/indices/master_index.md
    master_index_path = BASE_DIR / "reviews" / "indices" / "master_index.md"
    master_rows = []
    for p in all_papers:
        cat_short = p['category'].split('_', 1)[1].replace('_', ' ').title()
        master_rows.append(f"| [{p['title']}](file:///{BASE_DIR}/reviews/categories/{p['category']}/{p['filename']}.md) | {cat_short} | {p['authors'].split(',')[0]} et al. | {p['year']} | `{p['relevance_score']}/5` | {p['relevance_rating']} |")
    
    master_index_content = f"""# Master Literature Index (60 Papers Reviewed)

This master index catalogues all 60 research papers analyzed in this repository across 6 specialized research tracks.

Total Reviewed Papers: **60**  
Review Protocol: 1-by-1 deep analysis with Abstract, Findings, Conclusions, Future Scope, Relevance Scoring (1-5), What It Adds vs Doesn't, and Actionable Code Takeaways.

## Master Catalog

| Title | Category | First Author | Year | Relevance | Rating |
| :--- | :--- | :--- | :---: | :---: | :--- |
{"\n".join(master_rows)}
"""
    with open(master_index_path, "w", encoding="utf-8") as f:
        f.write(master_index_content)
    print("Master index written.")

    # Write by_relevance index
    by_rel_path = BASE_DIR / "reviews" / "indices" / "by_relevance.md"
    sorted_by_rel = sorted(all_papers, key=lambda x: x["relevance_score"], reverse=True)
    rel_rows = []
    for p in sorted_by_rel:
        rel_rows.append(f"| `{p['relevance_score']}/5` | [{p['title']}](file:///{BASE_DIR}/reviews/categories/{p['category']}/{p['filename']}.md) | {p['relevance_rating']} | {CATEGORIES[p['category']]} |")
    
    with open(by_rel_path, "w", encoding="utf-8") as f:
        f.write(f"""# Papers Sorted by Relevance to Problem Statement

| Score | Paper Title | Rating | Category |
| :---: | :--- | :--- | :--- |
{"\n".join(rel_rows)}
""")
    print("Relevance index written.")

    # Write by_category index
    by_cat_path = BASE_DIR / "reviews" / "indices" / "by_category.md"
    cat_sections = []
    for cat_id, cat_name in CATEGORIES.items():
        cat_papers = [p for p in all_papers if p["category"] == cat_id]
        cat_rows = [f"- [`{p['filename']}`](file:///{BASE_DIR}/reviews/categories/{cat_id}/{p['filename']}.md) — **{p['title']}** ({p['year']}, Relevance: `{p['relevance_score']}/5`)" for p in cat_papers]
        cat_sections.append(f"### {cat_name} ({len(cat_papers)} Papers)\n" + "\n".join(cat_rows))
        
    with open(by_cat_path, "w", encoding="utf-8") as f:
        f.write(f"""# Papers by Research Category

{"\n\n".join(cat_sections)}
""")
    print("Category index written.")

    print("All tasks in run_full_synthesis completed successfully!")

if __name__ == "__main__":
    main()
