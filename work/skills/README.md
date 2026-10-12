# Research Skills & Tooling Scripts (`skills/`)

This directory houses executable utilities, scripts, and tool bridges used by agents to automate literature search, paper downloading, PDF-to-Markdown extraction, and BibTeX management.

---

## Tooling Modules

- `search_and_fetch/`: Python scripts to query arXiv, OpenAlex, Semantic Scholar, and fetch metadata/papers.
  - `arxiv_fetcher.py`: CLI and importable module to query arXiv and format BibTeX records.

---

## Instructions for AI Agents

1. Whenever you need to search or parse papers repeatedly, use or enhance the Python utilities in this directory.
2. Maintain standalone execution (`python skills/search_and_fetch/arxiv_fetcher.py --query "vision language model" ...`).
3. External API dependencies must use standard libraries (`urllib`, `json`, `xml.etree.ElementTree`) or ubiquitous libraries (`requests`).
