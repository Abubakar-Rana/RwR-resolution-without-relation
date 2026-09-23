#!/usr/bin/env python
"""Decompress the per-item predictions shipped with the repository.

The .jsonl.gz files are what the analysis scripts read once expanded. Run once after cloning:

    python scripts/prepare_results.py
"""
import gzip
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = 0
for gz in sorted((ROOT / "results").rglob("predictions.jsonl.gz")):
    out = gz.with_suffix("")          # strip .gz
    if out.exists() and out.stat().st_mtime >= gz.stat().st_mtime:
        print("up to date:", out.relative_to(ROOT))
        continue
    with gzip.open(gz, "rb") as f, open(out, "wb") as o:
        shutil.copyfileobj(f, o)
    print("expanded:", out.relative_to(ROOT), f"({out.stat().st_size / 1e6:.1f} MB)")
    n += 1
print(f"{n} file(s) expanded.")
