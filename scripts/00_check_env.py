#!/usr/bin/env python
"""Environment preflight.

Run this FIRST on the GPU machine. It checks, without downloading model weights
unless asked, everything that could make a 12-hour run fail at hour 11:

  * python / torch / CUDA and the visible GPUs with their memory
  * transformers version and whether Qwen2_5_VLForConditionalGeneration exists
  * qwen_vl_utils, Pillow (and its large-image cap), datasets, pyyaml
  * optional extras: matplotlib, pandas, scipy, nltk+wordnet, networkx,
    open-vocabulary detection
  * write permission and free space at the image-cache and results paths
  * that the configured dataset can be reached and its columns resolved

Exit code 0 means every REQUIRED check passed. Optional failures are reported as
warnings with the exact command to fix them.

    python scripts/00_check_env.py
    python scripts/00_check_env.py --config configs/main.yaml --check-data
    python scripts/00_check_env.py --load-model      # actually loads the VLM
"""
from __future__ import annotations

import argparse
import importlib
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

OK = "[ OK ]"
WARN = "[WARN]"
FAIL = "[FAIL]"

_required_failures = []
_warnings = []


def report(status: str, name: str, detail: str = "") -> None:
    line = "{} {:<34} {}".format(status, name, detail)
    print(line)
    if status == FAIL:
        _required_failures.append(name)
    elif status == WARN:
        _warnings.append(name)


def check_python() -> None:
    v = sys.version_info
    detail = "{}.{}.{} at {}".format(v.major, v.minor, v.micro, sys.executable)
    if v < (3, 9):
        report(FAIL, "python >= 3.9", detail)
    else:
        report(OK, "python", detail)


def check_torch() -> None:
    try:
        import torch
    except ImportError as exc:
        report(FAIL, "torch", "not installed ({}). See requirements.txt".format(exc))
        return
    report(OK, "torch", torch.__version__)
    if not torch.cuda.is_available():
        report(WARN, "CUDA", "not available - the pipeline will run on CPU and be "
                             "impractically slow for 8500x8500 images")
        return
    report(OK, "CUDA", "{} | {} device(s)".format(
        getattr(torch.version, "cuda", "?"), torch.cuda.device_count()))
    for i in range(torch.cuda.device_count()):
        try:
            p = torch.cuda.get_device_properties(i)
            total = p.total_memory / (1024 ** 3)
            status = OK if total >= 20 else WARN
            note = "" if total >= 20 else " - Qwen2.5-VL-7B in bf16 needs ~17 GB " \
                                         "plus activations; consider configs/low_vram.yaml"
            report(status, "  gpu{}".format(i),
                   "{} | {:.1f} GB{}".format(p.name, total, note))
        except Exception as exc:
            report(WARN, "  gpu{}".format(i), "could not query: {}".format(exc))
    try:
        import torch.backends.cudnn  # noqa: F401
        x = torch.zeros(8, 8, device="cuda")
        _ = (x @ x).sum().item()
        report(OK, "CUDA matmul smoke test", "passed")
    except Exception as exc:
        report(FAIL, "CUDA matmul smoke test", str(exc)[:160])


def check_transformers(load_model: bool, model_id: str) -> None:
    try:
        import transformers
    except ImportError as exc:
        report(FAIL, "transformers", "not installed ({})".format(exc))
        return
    report(OK, "transformers", transformers.__version__)

    try:
        from transformers import Qwen2_5_VLForConditionalGeneration  # noqa: F401
        report(OK, "Qwen2_5_VLForConditionalGeneration", "available")
    except ImportError:
        report(FAIL, "Qwen2_5_VLForConditionalGeneration",
               "missing from transformers {}. Fix: pip install -U transformers "
               "(or git+https://github.com/huggingface/transformers)"
               .format(transformers.__version__))

    try:
        import qwen_vl_utils
        report(OK, "qwen_vl_utils", getattr(qwen_vl_utils, "__version__", "installed"))
    except ImportError:
        report(WARN, "qwen_vl_utils",
               "not installed - a fallback path is used. Fix: pip install qwen-vl-utils==0.0.8")

    if load_model:
        print("\n  Loading {} (this downloads ~16 GB on first run)...".format(model_id))
        try:
            from ctsr.models.qwen_vl import QwenVLBackend
            be = QwenVLBackend(model_id=model_id).load()
            report(OK, "model load", str(be.describe()))
            try:
                from PIL import Image
                img = Image.new("RGB", (448, 448), (120, 130, 110))
                resp = be.generate("Reply with exactly: READY", images=[img],
                                   max_new_tokens=8)
                report(OK, "model generate", "{!r} ({} prompt tok)".format(
                    resp.text[:60], resp.prompt_tokens))
            except Exception as exc:
                report(FAIL, "model generate", str(exc)[:200])
            be.unload()
        except Exception as exc:
            report(FAIL, "model load", str(exc)[:300])


def check_libs() -> None:
    required = [("PIL", "pillow"), ("yaml", "pyyaml"), ("numpy", "numpy")]
    optional = [
        ("datasets", "datasets", "needed for data.source=hf"),
        ("pyarrow", "pyarrow", "needed for data.source=parquet"),
        ("matplotlib", "matplotlib", "needed for figures"),
        ("pandas", "pandas", "convenience in the notebook"),
        ("scipy", "scipy", "exact binomial p-values (a pure-python fallback exists)"),
        ("networkx", "networkx", "optional graph analysis"),
    ]
    for mod, pkg in required:
        try:
            m = importlib.import_module(mod)
            report(OK, pkg, getattr(m, "__version__", "installed"))
        except ImportError:
            report(FAIL, pkg, "missing. Fix: pip install {}".format(pkg))

    for mod, pkg, why in optional:
        try:
            m = importlib.import_module(mod)
            report(OK, pkg, getattr(m, "__version__", "installed"))
        except ImportError:
            report(WARN, pkg, "missing ({}). Fix: pip install {}".format(why, pkg))

    # Pillow large-image handling
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None
        report(OK, "pillow large-image cap", "lifted (MAX_IMAGE_PIXELS=None)")
    except Exception as exc:
        report(WARN, "pillow large-image cap", str(exc)[:120])

    # METEOR needs NLTK + WordNet data, not just the package.
    try:
        import nltk  # noqa: F401
        from nltk.corpus import wordnet
        wordnet.synsets("test")
        report(OK, "nltk + wordnet (METEOR)", "available")
    except Exception as exc:
        report(WARN, "nltk + wordnet (METEOR)",
               "unavailable ({}). Caption METEOR will be reported as null, never as 0. "
               "Fix: pip install nltk && python -c \"import nltk; "
               "nltk.download('wordnet'); nltk.download('omw-1.4')\""
               .format(type(exc).__name__))

    # Optional open-vocabulary detector
    try:
        from transformers import AutoModelForZeroShotObjectDetection  # noqa: F401
        report(OK, "zero-shot detection API", "available (detection.proposer=openvocab)")
    except Exception:
        report(WARN, "zero-shot detection API",
               "unavailable - keep detection.proposer='vlm' (the default)")


def check_paths(cfg) -> None:
    targets = {
        "image cache": (cfg.get("data") or {}).get("cache_dir", "data/image_cache"),
        "results": (cfg.get("run") or {}).get("out_dir", "results"),
    }
    for label, raw in targets.items():
        p = Path(raw)
        try:
            p.mkdir(parents=True, exist_ok=True)
            probe = p / ".write_test"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            free = shutil.disk_usage(str(p)).free / (1024 ** 3)
            status = OK if free > 50 else WARN
            note = "" if free > 50 else (" - the XLRS-Bench lite split alone is ~38 GB "
                                        "compressed and materialises larger")
            report(status, "{} writable".format(label),
                   "{} | {:.1f} GB free{}".format(p.resolve(), free, note))
        except Exception as exc:
            report(FAIL, "{} writable".format(label),
                   "{}: {}".format(p, str(exc)[:160]))


def check_data(cfg) -> None:
    from ctsr.config import build_dataset
    from ctsr.data.xlrs import summarise

    print("\n  Resolving the dataset (loading a few samples)...")
    try:
        ds = build_dataset(cfg)
        samples = ds.load(limit=6)
    except Exception as exc:
        report(FAIL, "dataset load", "{}: {}".format(type(exc).__name__, str(exc)[:300]))
        return
    if not samples:
        report(FAIL, "dataset load", "returned 0 samples")
        return
    report(OK, "dataset load", "{} sample(s); columns: {}".format(
        len(samples), ds.columns))
    report(OK, "field map", str({k: v for k, v in ds.resolved_map.items() if v}))

    s = samples[0]
    report(OK, "first sample", "uid={} task={} family={} options={} images={}".format(
        s.uid, s.task, s.family, len(s.options), s.n_images))

    unknown = [x.category for x in samples if x.l2 == "Unknown"]
    if unknown:
        report(WARN, "task recognition",
               "unrecognised category label(s) {}. Check data/taxonomy.py aliases so "
               "these are not silently excluded from the relational grouping."
               .format(sorted(set(unknown))))
    else:
        report(OK, "task recognition", "all sampled categories map to known sub-tasks")

    missing_gt = [x.uid for x in samples if x.answer_raw is None]
    if missing_gt:
        report(WARN, "ground truth", "{} of {} sampled items have no answer field; "
                                     "these are reported unscorable, not wrong"
               .format(len(missing_gt), len(samples)))
    else:
        report(OK, "ground truth", "present on all sampled items")

    # Confirm an image actually opens at full size.
    try:
        from ctsr.tiling.tiler import TiledImage
        with TiledImage(s.image_path, tile_size=1024, overlap=128) as ti:
            report(OK, "image open + tile plan", str(ti.describe()))
    except Exception as exc:
        report(FAIL, "image open + tile plan",
               "{}: {}".format(type(exc).__name__, str(exc)[:240]))


def main() -> int:
    ap = argparse.ArgumentParser(description="Environment preflight for the CTSR pipeline")
    ap.add_argument("--config", default=None, help="config file to validate against")
    ap.add_argument("--set", dest="overrides", action="append", default=[],
                    metavar="key.path=value")
    ap.add_argument("--check-data", action="store_true",
                    help="load a few real samples (downloads data if source=hf)")
    ap.add_argument("--load-model", action="store_true",
                    help="actually load the VLM and run one generation")
    args = ap.parse_args()

    print("=" * 78)
    print("CTSR environment preflight")
    print("=" * 78)

    from ctsr.config import load_config
    try:
        cfg = load_config(args.config, args.overrides)
        report(OK, "config", args.config or "built-in defaults")
    except Exception as exc:
        report(FAIL, "config", "{}: {}".format(type(exc).__name__, str(exc)[:300]))
        cfg = {}

    print("\n-- core ----------------------------------------------------------")
    check_python()
    check_torch()

    print("\n-- libraries -----------------------------------------------------")
    check_libs()

    print("\n-- model ---------------------------------------------------------")
    model_id = (cfg.get("model") or {}).get("model_id", "Qwen/Qwen2.5-VL-7B-Instruct")
    check_transformers(args.load_model, model_id)

    if cfg:
        print("\n-- paths ---------------------------------------------------------")
        check_paths(cfg)

    if args.check_data and cfg:
        print("\n-- dataset -------------------------------------------------------")
        check_data(cfg)

    print("\n" + "=" * 78)
    if _required_failures:
        print("{} {} REQUIRED check(s) failed: {}".format(
            FAIL, len(_required_failures), ", ".join(_required_failures)))
        print("Fix these before starting a run.")
    else:
        print("{} All required checks passed.".format(OK))
    if _warnings:
        print("{} {} optional warning(s): {}".format(
            WARN, len(_warnings), ", ".join(_warnings)))
    print("=" * 78)
    return 1 if _required_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
