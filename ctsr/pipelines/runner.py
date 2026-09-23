"""Experiment runner: the loop that survives a long GPU job.

Guarantees:
  * Resume. Results are appended to JSONL and already-completed uids are skipped,
    so a job killed at hour 9 of 12 resumes from sample N, not from zero.
  * Isolation. A failing sample is recorded with its traceback and the loop
    continues. A run never dies on one bad image.
  * Provenance. Every run writes a manifest with the resolved config, the
    pipeline's own description, the environment fingerprint, the dataset field
    map, and whether the backend was a stub. Results with no manifest are not
    trustworthy and the aggregator says so.
  * Determinism of ordering. Samples are processed in sorted-uid order so two
    runs of the same config touch the same samples in the same sequence.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

from ..data.schema import Prediction, Sample
from ..utils.compute import env_info
from ..utils.io_utils import (JsonlWriter, atomic_write_json, completed_uids,
                              config_hash, ensure_dir, load_jsonl)
from ..utils.logging_utils import get_logger

LOG = get_logger("ctsr.runner")


def run_experiment(
    pipeline: Any,
    samples: Sequence[Sample],
    out_dir: str,
    run_name: Optional[str] = None,
    resume: bool = True,
    limit: Optional[int] = None,
    retry_errors: bool = True,
    cfg: Optional[Dict[str, Any]] = None,
    dataset_info: Optional[Dict[str, Any]] = None,
    progress_every: int = 10,
    on_prediction: Optional[Callable[[Prediction], None]] = None,
    save_every_manifest: int = 50,
) -> Dict[str, Any]:
    """Run one arm over `samples`, writing `<out_dir>/<run_name>/predictions.jsonl`.

    Returns a summary dict. The authoritative record is on disk.
    """
    run_name = run_name or pipeline.name
    run_dir = ensure_dir(Path(out_dir) / run_name)
    pred_path = run_dir / "predictions.jsonl"
    manifest_path = run_dir / "manifest.json"
    errors_path = run_dir / "failures.jsonl"

    ordered = sorted(samples, key=lambda s: s.uid)
    if limit is not None:
        ordered = ordered[:int(limit)]

    done = set()
    if resume and pred_path.exists():
        done = completed_uids(pred_path, require_ok=retry_errors)
        LOG.info("Resuming %s: %d of %d samples already complete.",
                 run_name, len(done), len(ordered))
    elif pred_path.exists() and not resume:
        # Never delete previous results silently; move them aside.
        stamp = time.strftime("%Y%m%d_%H%M%S")
        backup = pred_path.with_name("predictions.{}.bak.jsonl".format(stamp))
        pred_path.replace(backup)
        LOG.warning("resume=False: previous results moved to %s", backup.name)

    todo = [s for s in ordered if s.uid not in done]
    is_stub = bool(getattr(pipeline.backend, "is_stub", False))
    if is_stub:
        LOG.warning(
            "Backend is a STUB. Output is placeholder text and MUST NOT be "
            "reported as a result. Set model.backend='qwen' for real numbers."
        )

    manifest: Dict[str, Any] = {
        "run_name": run_name,
        "pipeline": pipeline.name,
        "uses_relations": bool(getattr(pipeline, "uses_relations", False)),
        "backend_is_stub": is_stub,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "n_samples_total": len(ordered),
        "n_samples_pending": len(todo),
        "n_samples_resumed": len(done),
        "config": cfg or {},
        "config_hash": config_hash(cfg or {}),
        "pipeline_description": _safe_describe(pipeline),
        "dataset": dataset_info or {},
        "environment": env_info(),
        "status": "running",
    }
    atomic_write_json(manifest_path, manifest)

    if not todo:
        LOG.info("%s: nothing to do (all %d samples complete).", run_name, len(ordered))
        manifest["status"] = "complete"
        manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        atomic_write_json(manifest_path, manifest)
        return _summarise(run_dir, manifest)

    t0 = time.perf_counter()
    n_ok = n_err = 0
    writer = JsonlWriter(pred_path, mode="a")
    err_writer = JsonlWriter(errors_path, mode="a")

    try:
        for i, sample in enumerate(todo, 1):
            try:
                pred = pipeline.run_sample(sample)
            except (KeyboardInterrupt, SystemExit):
                LOG.warning("Interrupted at sample %d/%d; %d results are on disk.",
                            i, len(todo), n_ok + n_err)
                raise
            except BaseException as exc:  # noqa: BLE001
                # run_sample should not raise, but if it does the loop survives.
                import traceback
                n_err += 1
                LOG.exception("Pipeline raised outside run_sample for %s", sample.uid)
                pred = Prediction(
                    uid=sample.uid, pipeline=pipeline.name, status="error",
                    category=sample.category, task=sample.task, l2=sample.l2,
                    family=sample.family, rel_group=sample.rel_group(),
                    errors=[{"stage": "runner", "kind": exc.__class__.__name__,
                             "message": str(exc)[:2000],
                             "traceback": traceback.format_exc()[-4000:]}],
                )

            record = pred.to_dict()
            record["backend_is_stub"] = is_stub
            writer.write(record)

            if pred.status == "ok":
                n_ok += 1
            else:
                n_err += 1
                err_writer.write({"uid": pred.uid, "task": pred.task,
                                  "errors": pred.errors})

            if on_prediction is not None:
                try:
                    on_prediction(pred)
                except Exception:
                    LOG.exception("on_prediction hook raised; continuing")

            if progress_every and i % progress_every == 0:
                elapsed = time.perf_counter() - t0
                rate = elapsed / i
                LOG.info(
                    "%s: %d/%d (%.1f%%) | ok=%d err=%d | %.1fs/sample | ETA %.1f min",
                    run_name, i, len(todo), 100.0 * i / len(todo), n_ok, n_err,
                    rate, rate * (len(todo) - i) / 60.0,
                )
            if save_every_manifest and i % save_every_manifest == 0:
                manifest["n_completed_this_run"] = i
                manifest["elapsed_seconds"] = round(time.perf_counter() - t0, 1)
                atomic_write_json(manifest_path, manifest)
    finally:
        writer.close()
        err_writer.close()
        manifest["n_completed_this_run"] = n_ok + n_err
        manifest["n_ok"] = n_ok
        manifest["n_error"] = n_err
        manifest["elapsed_seconds"] = round(time.perf_counter() - t0, 1)
        manifest["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        manifest["status"] = "complete" if n_err == 0 else "complete_with_errors"
        atomic_write_json(manifest_path, manifest)

    LOG.info("%s finished: ok=%d error=%d in %.1f min -> %s",
             run_name, n_ok, n_err, manifest["elapsed_seconds"] / 60.0, pred_path)
    return _summarise(run_dir, manifest)


def _safe_describe(obj: Any) -> Dict[str, Any]:
    try:
        return obj.describe() if hasattr(obj, "describe") else {}
    except Exception as exc:
        return {"describe_failed": str(exc)}


def _summarise(run_dir: Path, manifest: Dict[str, Any]) -> Dict[str, Any]:
    """Quick on-disk summary; the real analysis lives in ctsr.eval.aggregate."""
    records = load_jsonl(run_dir / "predictions.jsonl")
    n = len(records)
    scored = [r for r in records if r.get("correct") is not None]
    n_correct = sum(1 for r in scored if r.get("correct"))
    calls = [((r.get("compute") or {}).get("n_vlm_calls") or 0) for r in records]
    secs = [((r.get("compute") or {}).get("wall_seconds") or 0.0) for r in records]
    return {
        "run_name": manifest.get("run_name"),
        "run_dir": str(run_dir),
        "n_records": n,
        "n_scored": len(scored),
        "accuracy": (n_correct / len(scored)) if scored else None,
        "n_parse_failed": sum(1 for r in records if r.get("parse_failed")),
        "n_error": sum(1 for r in records if r.get("status") != "ok"),
        "mean_vlm_calls": (sum(calls) / n) if n else None,
        "mean_seconds": (sum(secs) / n) if n else None,
        "backend_is_stub": manifest.get("backend_is_stub"),
    }


def build_pipeline(name: str, cfg: Dict[str, Any], backend: Any,
                   scorer: Any = None, proposer: Any = None) -> Any:
    """Instantiate an arm by name.

    Names match the plan's experimental design:
      b1_direct, b2_tiling, b3_selected, proposed_ctsr
    """
    from .baselines import DirectPipeline, TilingPipeline
    from .hierarchical import ProposedPipeline, SelectedTilesPipeline

    key = str(name).strip().lower()
    aliases = {
        "b1": "b1_direct", "direct": "b1_direct", "baseline1": "b1_direct",
        "b2": "b2_tiling", "tiling": "b2_tiling", "baseline2": "b2_tiling",
        "b3": "b3_selected", "selected": "b3_selected", "baseline3": "b3_selected",
        "proposed": "proposed_ctsr", "ctsr": "proposed_ctsr", "full": "proposed_ctsr",
    }
    key = aliases.get(key, key)

    if key == "b1_direct":
        return DirectPipeline(cfg, backend)
    if key == "b2_tiling":
        return TilingPipeline(cfg, backend)
    if key == "b3_selected":
        return SelectedTilesPipeline(cfg, backend, scorer=scorer, proposer=proposer)
    if key == "proposed_ctsr":
        return ProposedPipeline(cfg, backend, scorer=scorer, proposer=proposer)
    raise ValueError(
        "Unknown pipeline {!r}. Choose from: b1_direct, b2_tiling, b3_selected, "
        "proposed_ctsr".format(name)
    )


ALL_ARMS: List[str] = ["b1_direct", "b2_tiling", "b3_selected", "proposed_ctsr"]
