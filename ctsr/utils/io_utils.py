"""Crash-safe, resumable I/O.

Runs write one JSONL record per sample and are resumed by reading back the uids
already present. Writes are line-buffered and flushed so a killed job keeps
everything up to the last completed sample.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional, Set

from .logging_utils import get_logger

LOG = get_logger("ctsr.io")


def ensure_dir(path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def _json_default(obj: Any) -> Any:
    """Make numpy / Path / set / dataclass-ish objects serialisable."""
    for attr in ("tolist", "item"):
        fn = getattr(obj, attr, None)
        if callable(fn):
            try:
                return fn()
            except Exception:
                pass
    if isinstance(obj, (set, frozenset, tuple)):
        return list(obj)
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "to_dict") and callable(obj.to_dict):
        try:
            return obj.to_dict()
        except Exception:
            pass
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in vars(obj).items() if not k.startswith("_")}
    return str(obj)


def dumps(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=_json_default)


def atomic_write_text(path, text: str, encoding: str = "utf-8") -> Path:
    """Write via a temp file + replace so readers never see a partial file."""
    p = Path(path)
    ensure_dir(p.parent)
    fd, tmp = tempfile.mkstemp(dir=str(p.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, p)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    return p


def atomic_write_json(path, obj: Any, indent: int = 2) -> Path:
    return atomic_write_text(path, json.dumps(obj, ensure_ascii=False, indent=indent,
                                             default=_json_default))


def read_json(path, default: Any = None) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        LOG.warning("Could not read JSON %s: %s", p, exc)
        return default


def read_jsonl(path, skip_bad: bool = True) -> Iterator[Dict[str, Any]]:
    """Stream a JSONL file, tolerating a truncated final line from a killed job."""
    p = Path(path)
    if not p.exists():
        return
    with p.open("r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                if skip_bad:
                    LOG.warning("Skipping malformed line %d in %s: %s", lineno, p, exc)
                    continue
                raise


def load_jsonl(path) -> List[Dict[str, Any]]:
    return list(read_jsonl(path))


def completed_uids(path, key: str = "uid", require_ok: bool = False) -> Set[str]:
    """uids already recorded in a results JSONL, for resuming a run.

    With `require_ok=True`, samples whose status is not "ok" are treated as not
    done so a re-run retries them.
    """
    done: Set[str] = set()
    for rec in read_jsonl(path):
        uid = rec.get(key)
        if uid is None:
            continue
        if require_ok and rec.get("status") != "ok":
            continue
        done.add(str(uid))
    return done


class JsonlWriter:
    """Append-only JSONL writer that flushes after every record."""

    def __init__(self, path, mode: str = "a") -> None:
        self.path = Path(path)
        ensure_dir(self.path.parent)
        self._fh = self.path.open(mode, encoding="utf-8", newline="\n")
        self.n_written = 0

    def write(self, obj: Any) -> None:
        self._fh.write(dumps(obj) + "\n")
        self._fh.flush()
        try:
            os.fsync(self._fh.fileno())
        except (OSError, ValueError):
            # fsync is unavailable on some network filesystems; flush is enough.
            pass
        self.n_written += 1

    def close(self) -> None:
        try:
            self._fh.close()
        except Exception:
            pass

    def __enter__(self) -> "JsonlWriter":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def config_hash(cfg: Any, length: int = 10) -> str:
    """Stable short hash of a config, used to tag runs and detect config drift."""
    blob = json.dumps(cfg, sort_keys=True, ensure_ascii=False, default=_json_default)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:length]


def write_csv(path, rows: Iterable[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> Optional[Path]:
    """Minimal CSV writer so results survive even if pandas is unavailable."""
    import csv

    rows = list(rows)
    if not rows:
        LOG.warning("write_csv: nothing to write for %s", path)
        return None
    if fieldnames is None:
        seen: List[str] = []
        for r in rows:
            for k in r:
                if k not in seen:
                    seen.append(k)
        fieldnames = seen
    p = Path(path)
    ensure_dir(p.parent)
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return p
