# Papers Library (`papers/`)

This directory is the central ingestion point and reference store for all scientific literature, preprints, and academic publications relevant to this VLM research.

---

## Directory Layout

- [`bibliography.bib`](file:///d:/projects/research/vlm/papers/bibliography.bib): Canonical BibTeX file holding citation metadata for all referenced papers.
- `raw/`: Raw downloaded paper files (PDFs, conference archives). *Note: Large binary PDFs are gitignored by default; download scripts or URLs are kept in metadata.*
- `extracted/`: Machine-readable extractions (markdown, plaintext, LaTeX source, or parsed tables/equations) for fast reading by AI agents.

---

## Guidelines for AI Agents

1. **BibTeX Key Convention**:
   Use standard citation keys: `[FirstAuthorLastName][YYYY][SignificantKeyword]`, e.g., `liu2024llavanext`, `chen2024internvl`, `bai2023qwen`.
2. **Metadata Consistency**:
   Ensure every entry in `bibliography.bib` contains at least:
   - `author`
   - `title`
   - `year`
   - `eprint` (arXiv ID) or `journal`/`booktitle`
   - `url`
   - `abstract`
3. **Extracted Content Format**:
   Save parsed text in `extracted/[bibtex_key].md`.
