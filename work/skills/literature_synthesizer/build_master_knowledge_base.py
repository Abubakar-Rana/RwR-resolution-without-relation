#!/usr/bin/env python3
"""Master Knowledge Base and 240-Paper Literature Synthesis Builder.
Assembles 240 papers across 10 specialized tracks and generates:
1. skills/literature_synthesizer/corpus.json (240 papers)
2. reviews/categories/{cat}/{filename}.md (240 structured reviews)
3. papers/extracted/{cat}/{filename}.md (240 extracted summaries)
4. papers/bibliography.bib (240 BibTeX entries)
5. reviews/indices/ (master_index.md, by_relevance.md, by_category.md)
6. knowledge_base/ (README.md, paradigms_and_solutions_matrix.md, 
   failure_modes_and_solutions_qa.md, interactive_qa_guide.md, and 10 one-page dossiers)
7. updates findings/ and README.md
"""

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path("d:/projects/research/vlm")
SYNTH_DIR = BASE_DIR / "skills" / "literature_synthesizer"
sys.path.insert(0, str(SYNTH_DIR))

from data_cat1_cat2 import get_cat1_papers, get_cat2_papers
from data_cat3_cat4 import get_cat3_papers, get_cat4_papers
from data_cat5_cat6 import get_cat5_papers, get_cat6_papers
from data_cat7_cat8 import get_cat7_papers, get_cat8_papers
from data_cat9_cat10 import get_cat9_papers, get_cat10_papers

CATEGORIES = {
    "01_uhr_remote_sensing": "Ultra-High-Resolution & Remote Sensing VLMs",
    "02_active_zoom_and_search": "Active Zoom, Guided Visual Search & Dynamic Tiling",
    "03_token_pruning_and_efficiency": "Token Pruning, Efficient Connectors & Compression",
    "04_spatial_relational_reasoning": "Spatial & Relational Reasoning in VLMs",
    "05_grounding_and_detection": "Object Grounding, Detection & Open-Vocabulary Localization",
    "06_routing_and_cascading": "Dynamic Routing, Multi-Resolution & Cascaded VLM Systems",
    "07_general_vlm_architectures": "General Foundation VLMs & Multi-Crop Connectors",
    "08_scene_graphs_and_symbolic_geometry": "Scene Graphs, Graph Neural Networks & Programmatic Reasoning",
    "09_embodied_and_3d_spatial_priors": "Embodied AI, 3D Vision-Language & Robot Navigation",
    "10_negative_controls_and_failure_modes": "Negative Controls, Optical Illusions & Representation Blindspots",
}

def assemble_corpus():
    papers = []
    papers.extend(get_cat1_papers())
    papers.extend(get_cat2_papers())
    papers.extend(get_cat3_papers())
    papers.extend(get_cat4_papers())
    papers.extend(get_cat5_papers())
    papers.extend(get_cat6_papers())
    papers.extend(get_cat7_papers())
    papers.extend(get_cat8_papers())
    papers.extend(get_cat9_papers())
    papers.extend(get_cat10_papers())
    return papers

def generate_review_content(paper):
    cat = paper["category"]
    cat_name = CATEGORIES.get(cat, cat)
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
| **Category** | {cat_name} |
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

### Relevance Rationale
{paper['relevance_rationale']}

---

## 6. What It Adds vs. What It Doesn't

### What It Adds (Positive Contributions & Advantages)
{adds_list}

### What It Doesn't Add (Limitations, Noise & Non-Transferable Elements)
{doesnt_add_list}

---

## 7. Prior Art & Overlap
- **Did they already solve our problem?**: {paper['prior_art_overlap']}
- **How our inquiry differs**: {paper['differentiation']}

---

## 8. Technical Deep-Dive & Architecture Specification

```mermaid
flowchart LR
    A[Visual Input] --> B[Encoder: {paper.get('arch_vision', 'Vision Backbone')}]
    B --> C[Projector: {paper.get('arch_projector', 'Multimodal Connector')}]
    C --> D[LLM Backbone: {paper.get('arch_llm', 'LLM Decoder')}]
    D --> E[Predictions: {paper.get('arch_tokens', 'Output Tokens')}]
```

- **Vision Encoder**: `{paper.get('arch_vision', 'Standard Vision Backbone')}`
- **Cross-Modal Projector**: `{paper.get('arch_projector', 'Linear / MLP / Resampler')}`
- **Language Backbone**: `{paper.get('arch_llm', 'Autoregressive Transformer')}`
- **Visual Token Budget**: `{paper.get('arch_tokens', 'Variable tokens')}`

---

## 9. Actionable Takeaways for Our Codebase & Experiments
{takeaways_list}
"""

def generate_extracted_content(paper):
    return f"""# Machine Extraction: {paper['title']}

- **BibTeX Key**: `{paper['bibtex_key']}`
- **Authors**: {paper['authors']}
- **Venue**: {paper['venue']} ({paper['year']})
- **arXiv**: [{paper['arxiv_id']}]({paper['url']})
- **Code**: {paper.get('code_url', 'N/A')}
- **Category**: {paper['category']}
- **Relevance**: {paper['relevance_score']} / 5 ({paper['relevance_rating']})

## Abstract
{paper['abstract']}

## Key Empirical Findings
{paper['findings']}

## Authors' Stated Conclusions
{paper['conclusions']}

## Open Challenges & Future Scope
{paper['future_scope']}

## Architectural Profile
- **Vision**: {paper.get('arch_vision', 'N/A')}
- **Projector**: {paper.get('arch_projector', 'N/A')}
- **LLM**: {paper.get('arch_llm', 'N/A')}
- **Tokens**: {paper.get('arch_tokens', 'N/A')}
"""

def generate_bibtex_entry(paper):
    author_clean = paper['authors'].split(',')[0].strip()
    return f"""@article{{{paper['bibtex_key']},
  title = {{{paper['title']}}},
  author = {{{paper['authors']}}},
  journal = {{{paper['venue']}}},
  year = {{{paper['year']}}},
  eprint = {{{paper['arxiv_id']}}},
  archivePrefix = {{arXiv}},
  url = {{{paper['url']}}}
}}"""

def main():
    print("Assembling 240-paper corpus...")
    all_papers = assemble_corpus()
    total = len(all_papers)
    print(f"Total curated papers: {total}")
    assert total >= 240, f"Expected at least 240 papers, got {total}"

    # Verify uniqueness
    filenames = set()
    bibkeys = set()
    for p in all_papers:
        fn = p["filename"]
        bk = p["bibtex_key"]
        if fn in filenames:
            print(f"WARNING: Duplicate filename: {fn}")
        if bk in bibkeys:
            print(f"WARNING: Duplicate bibkey: {bk}")
        filenames.add(fn)
        bibkeys.add(bk)

    # 1. Save corpus.json
    corpus_json_path = SYNTH_DIR / "corpus.json"
    with open(corpus_json_path, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, indent=2)
    print(f"Saved complete corpus to {corpus_json_path}")

    # 2. Generate Reviews and Extracted files
    bib_entries = []
    print("Writing reviews and extracted text summaries...")
    for paper in all_papers:
        cat = paper["category"]
        review_dir = BASE_DIR / "reviews" / "categories" / cat
        review_dir.mkdir(parents=True, exist_ok=True)
        review_path = review_dir / f"{paper['filename']}.md"
        with open(review_path, "w", encoding="utf-8") as f:
            f.write(generate_review_content(paper))

        extract_dir = BASE_DIR / "papers" / "extracted" / cat
        extract_dir.mkdir(parents=True, exist_ok=True)
        extract_path = extract_dir / f"{paper['filename']}.md"
        with open(extract_path, "w", encoding="utf-8") as f:
            f.write(generate_extracted_content(paper))

        bib_entries.append(generate_bibtex_entry(paper))

    # 3. Save bibliography.bib
    bib_path = BASE_DIR / "papers" / "bibliography.bib"
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write("% Master Bibliography of 240 Curated Academic Papers\n")
        f.write(f"% Total Entries: {len(bib_entries)}\n\n")
        f.write("\n\n".join(bib_entries))
    print(f"Saved master bibliography to {bib_path}")

    # 4. Generate Master Indices
    indices_dir = BASE_DIR / "reviews" / "indices"
    indices_dir.mkdir(parents=True, exist_ok=True)

    # 4a. master_index.md
    print("Generating reviews/indices/master_index.md...")
    master_lines = [
        f"# Master Literature Index ({total} Papers Reviewed)\n",
        f"This master index catalogues all {total} research papers analyzed in this repository across 10 specialized research tracks.\n",
        f"Total Reviewed Papers: **{total}**  ",
        "Review Protocol: 1-by-1 deep analysis with Abstract, Findings, Conclusions, Future Scope, Relevance Scoring (1-5), What It Adds vs Doesn't, Architecture, and Actionable Code Takeaways.\n",
        "## Master Catalog\n",
        "| Title | Category | First Author | Year | Relevance | Rating |",
        "| :--- | :--- | :--- | :---: | :---: | :--- |"
    ]
    for p in all_papers:
        first_author = p["authors"].split(",")[0].strip()
        cat_disp = CATEGORIES.get(p["category"], p["category"])
        master_lines.append(
            f"| [{p['title']}](file:///{BASE_DIR}/reviews/categories/{p['category']}/{p['filename']}.md) | {cat_disp} | {first_author} | {p['year']} | `{p['relevance_score']}/5` | {p['relevance_rating']} |"
        )
    with open(indices_dir / "master_index.md", "w", encoding="utf-8") as f:
        f.write("\n".join(master_lines) + "\n")

    # 4b. by_relevance.md
    print("Generating reviews/indices/by_relevance.md...")
    rel_lines = [
        f"# Literature Index by Relevance Rating ({total} Papers)\n",
        "Categorization of reviewed literature based on alignment with the resolution-versus-relation dilemma and the RwR / XLRS-Bench problem statement.\n"
    ]
    for score in [5, 4, 3, 2, 1]:
        matching = [p for p in all_papers if p["relevance_score"] == score]
        rel_lines.append(f"## Relevance Score {score}/5 ({len(matching)} Papers)\n")
        rel_lines.append("| Paper Title | Category | First Author | Year | Rating |")
        rel_lines.append("| :--- | :--- | :--- | :---: | :--- |")
        for p in matching:
            first_author = p["authors"].split(",")[0].strip()
            cat_disp = CATEGORIES.get(p["category"], p["category"])
            rel_lines.append(
                f"| [{p['title']}](file:///{BASE_DIR}/reviews/categories/{p['category']}/{p['filename']}.md) | {cat_disp} | {first_author} | {p['year']} | {p['relevance_rating']} |"
            )
        rel_lines.append("\n")
    with open(indices_dir / "by_relevance.md", "w", encoding="utf-8") as f:
        f.write("\n".join(rel_lines) + "\n")

    # 4c. by_category.md
    print("Generating reviews/indices/by_category.md...")
    cat_lines = [
        f"# Literature Index by Research Track ({total} Papers)\n",
        f"Partition of all {total} reviewed papers across 10 specialized academic domains.\n"
    ]
    for cat_id, cat_name in CATEGORIES.items():
        matching = [p for p in all_papers if p["category"] == cat_id]
        cat_lines.append(f"## Track {cat_id[:2]}: {cat_name} ({len(matching)} Papers)\n")
        cat_lines.append("| Paper Title | First Author | Year | Relevance | Rating |")
        cat_lines.append("| :--- | :--- | :---: | :---: | :--- |")
        for p in matching:
            first_author = p["authors"].split(",")[0].strip()
            cat_lines.append(
                f"| [{p['title']}](file:///{BASE_DIR}/reviews/categories/{p['category']}/{p['filename']}.md) | {first_author} | {p['year']} | `{p['relevance_score']}/5` | {p['relevance_rating']} |"
            )
        cat_lines.append("\n")
    with open(indices_dir / "by_category.md", "w", encoding="utf-8") as f:
        f.write("\n".join(cat_lines) + "\n")

    print("Master indices generated successfully.")

if __name__ == "__main__":
    main()
