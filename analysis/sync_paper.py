#!/usr/bin/env python
"""Copy the generated LaTeX fragments into paper/analysis/ so the manuscript picks them up."""
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
DST = HERE.parent / "paper" / "analysis"
for name in ("numbers.tex", "table_pertask.tex"):
    src = HERE / name
    if src.exists():
        shutil.copy2(src, DST / name)
        print("synced", name)
print("(numbers_rev.tex and table_partitions.tex are written directly by r07_paper_assets.py)")
