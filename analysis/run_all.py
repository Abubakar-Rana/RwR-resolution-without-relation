#!/usr/bin/env python
"""Run every Revision-1 analysis in order. Reads ../Codebase/results/main (read-only);
writes only to ./outputs/. No GPU or model needed."""
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
for script in ("r01_partition_robustness.py", "r02_null_power.py", "r03_router.py",
               "r04_router_figure.py", "r05_detector_grounding.py",
               "r06_grounding_figure.py", "r07_paper_assets.py"):
    print(f"\n==== {script} ====")
    runpy.run_path(str(HERE / script), run_name="__main__")
