#!/usr/bin/env python3
"""arXiv Paper Search and Ingestion Utility.

Allows searching arXiv, extracting paper metadata, fetching abstracts,
generating BibTeX citation keys, and optionally downloading PDFs.
Requires only Python standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional

ARXIV_API_BASE = "http://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def search_arxiv(
    query: str,
    max_results: int = 5,
    sort_by: str = "relevance",
    sort_order: str = "descending",
) -> List[Dict[str, Any]]:
    """Query the arXiv API and return parsed paper metadata dictionaries."""
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    url = f"{ARXIV_API_BASE}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "VLM-Research-Agent/1.0"})

    with urllib.request.urlopen(req) as resp:
        xml_content = resp.read()

    root = ET.fromstring(xml_content)
    papers = []

    for entry in root.findall("atom:entry", ATOM_NS):
        id_text = entry.findtext("atom:id", default="", namespaces=ATOM_NS)
        arxiv_id = id_text.split("/abs/")[-1]

        title = entry.findtext("atom:title", default="", namespaces=ATOM_NS).strip()
        title = re.sub(r"\s+", " ", title)

        summary = entry.findtext("atom:summary", default="", namespaces=ATOM_NS).strip()
        summary = re.sub(r"\s+", " ", summary)

        published = entry.findtext("atom:published", default="", namespaces=ATOM_NS)[:10]

        authors = [
            author.findtext("atom:name", default="", namespaces=ATOM_NS)
            for author in entry.findall("atom:author", ATOM_NS)
        ]

        pdf_url = ""
        for link in entry.findall("atom:link", ATOM_NS):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href", "")
                break
        if not pdf_url and arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        # Construct clean bibtex key
        first_author_surname = (
            authors[0].split()[-1].lower() if authors else "unknown"
        )
        year = published[:4] if published else "2024"
        clean_title_word = re.sub(r"[^a-zA-Z]", "", title.split()[0].lower()) if title else "paper"
        bibtex_key = f"{first_author_surname}{year}{clean_title_word}"

        papers.append(
            {
                "bibtex_key": bibtex_key,
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "published": published,
                "summary": summary,
                "abs_url": id_text,
                "pdf_url": pdf_url,
            }
        )

    return papers


def generate_bibtex(paper: Dict[str, Any]) -> str:
    """Generate a clean BibTeX record for a paper."""
    authors_str = " and ".join(paper["authors"])
    year = paper["published"][:4] if paper["published"] else "2024"
    return (
        f"@article{{{paper['bibtex_key']},\n"
        f"  title     = {{{{{paper['title']}}}}},\n"
        f"  author    = {{{authors_str}}},\n"
        f"  journal   = {{arXiv preprint arXiv:{paper['arxiv_id']}}},\n"
        f"  year      = {{{year}}},\n"
        f"  eprint    = {{{paper['arxiv_id']}}},\n"
        f"  archivePrefix = {{arXiv}},\n"
        f"  primaryClass  = {{cs.CV}},\n"
        f"  url       = {{{paper['abs_url']}}}\n"
        f"}}"
    )


def download_pdf(pdf_url: str, dest_path: Path) -> bool:
    """Download PDF file from arXiv to dest_path."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(pdf_url, headers={"User-Agent": "VLM-Research-Agent/1.0"})
    try:
        with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"Failed to download PDF from {pdf_url}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="arXiv Ingestion Tool")
    parser.add_argument("--query", type=str, required=True, help="Search terms")
    parser.add_argument("--max-results", type=int, default=3, help="Max results")
    parser.add_argument("--download-pdf", action="store_true", help="Download PDFs to papers/raw/")
    args = parser.parse_args()

    papers = search_arxiv(args.query, max_results=args.max_results)
    print(f"Found {len(papers)} papers:\n")

    for p in papers:
        print(f"[{p['bibtex_key']}] {p['title']}")
        print(f"Authors: {', '.join(p['authors'])}")
        print(f"Date: {p['published']} | arXiv: {p['arxiv_id']}")
        print(f"URL: {p['abs_url']}")
        print("\nBibTeX:\n" + generate_bibtex(p))
        print("-" * 60)

        if args.download_pdf:
            dest = Path("papers/raw") / f"{p['bibtex_key']}.pdf"
            print(f"Downloading to {dest}...")
            if download_pdf(p["pdf_url"], dest):
                print("Download complete.")


if __name__ == "__main__":
    main()
