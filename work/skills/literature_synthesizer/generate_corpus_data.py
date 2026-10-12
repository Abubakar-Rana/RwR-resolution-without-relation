"""Corpus Data Generator containing 60 curated research papers across 6 categories.
Each entry contains full metadata, abstract, findings, conclusions, future scope,
relevance scoring against XLRS-Bench/RwR, what it adds vs doesn't, and actionable takeaways.
"""

# Category 1: Ultra-High-Resolution & Remote Sensing VLMs (10 papers)
# Category 2: Active Zoom, Guided Visual Search & Dynamic Tiling (10 papers)
# Category 3: Token Pruning, Efficient Connectors & Compression (10 papers)
# Category 4: Spatial & Relational Reasoning in VLMs (10 papers)
# Category 5: Object Grounding, Detection & Open-Vocabulary Localization (10 papers)
# Category 6: Dynamic Routing, Multi-Resolution & Cascaded VLM Systems (10 papers)

import json
from pathlib import Path

DATA_FILE = Path("d:/projects/research/vlm/skills/literature_synthesizer/corpus.json")

def load_or_generate_corpus():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

PAPERS_DATA = load_or_generate_corpus()
