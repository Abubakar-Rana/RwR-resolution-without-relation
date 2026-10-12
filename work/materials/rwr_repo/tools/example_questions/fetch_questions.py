#!/usr/bin/env python
"""Fetch real XLRS-Bench-lite questions without downloading the images.

Source: the VLMEvalKit mirror `initiacms/XLRS-Bench-lite_VLM` (one JSON object per line, text
fields before the base64 image). We read small byte ranges at many offsets, parse the first
record that starts inside each range, and keep up to PER_TASK items per fine-grained task
(the mirror's `l2-category` field). Results are merged into questions.json across runs.

    python fetch_questions.py
"""
import json
import re
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = "initiacms/XLRS-Bench-lite_VLM"
API = f"https://huggingface.co/api/datasets/{REPO}/tree/main"
URL = f"https://huggingface.co/datasets/{REPO}/resolve/main/{{}}"
OUT = Path(__file__).resolve().parent / "questions.json"
PER_TASK = 2
PROBES = 60
CHUNK = 512 * 1024
WANT = 13


def get(url, lo, hi):
    req = urllib.request.Request(url, headers={"Range": f"bytes={lo}-{hi}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def records_in(buf, at_zero):
    starts = ([0] if at_zero else []) + [m.start() + 1 for m in re.finditer(rb'\n\{"index":', buf)]
    for s in starts:
        text = buf[s:s + 30000].decode("utf-8", "replace")
        cut = text.find(',"image"')
        if cut > 0:
            try:
                yield json.loads(text[:cut] + "}")
            except json.JSONDecodeError:
                pass


def main():
    found = defaultdict(list)
    if OUT.exists():
        for k, v in json.loads(OUT.read_text(encoding="utf-8")).items():
            found[k] = v
    files = [f for f in json.loads(urllib.request.urlopen(API, timeout=60).read())
             if f["path"].endswith(".jsonl")]
    for f in sorted(files, key=lambda x: x["path"]):
        for k in range(PROBES):
            off = int(f["size"] * k / PROBES)
            try:
                buf = get(URL.format(f["path"]), off, min(f["size"] - 1, off + CHUNK))
            except Exception as exc:
                print("  read failed", exc)
                continue
            for rec in records_in(buf, off == 0):
                task = rec.get("l2-category") or rec.get("category") or "?"
                if len(found[task]) < PER_TASK and all(r["index"] != rec["index"] for r in found[task]):
                    rec["task"] = task
                    found[task].append(rec)
        print(f["path"], len(found), "tasks:", {k: len(v) for k, v in sorted(found.items())}, flush=True)
        OUT.write_text(json.dumps(dict(sorted(found.items())), indent=1, ensure_ascii=False),
                       encoding="utf-8")
        if len(found) >= WANT and all(len(v) >= PER_TASK for v in found.values()):
            break
    print("done:", sum(len(v) for v in found.values()), "questions in", len(found), "tasks")


if __name__ == "__main__":
    main()
