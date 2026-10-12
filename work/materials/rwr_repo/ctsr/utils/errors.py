"""Retry / OOM-backoff / stage-isolation primitives.

Design rule for this codebase: a single bad sample must never abort a run that
may take many GPU-hours. Every fallible stage either returns a value or records
a structured failure and degrades gracefully.
"""
from __future__ import annotations

import gc
import time
import traceback
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterator, List, Optional

from .logging_utils import get_logger

LOG = get_logger("ctsr.errors")

# Substrings that identify an out-of-memory condition across torch versions and
# backends without importing backend-specific exception classes.
_OOM_MARKERS = (
    "out of memory",
    "cublas_status_alloc_failed",
    "cudnn_status_alloc_failed",
    "hip out of memory",
    "not enough memory",
    "failed to allocate",
    "can't allocate memory",
)


def is_oom(exc: BaseException) -> bool:
    """Heuristic, version-agnostic OOM detection."""
    if exc.__class__.__name__ in ("OutOfMemoryError", "OutOfMemory"):
        return True
    msg = str(exc).lower()
    return any(m in msg for m in _OOM_MARKERS)


def free_gpu() -> None:
    """Release cached GPU memory; no-op when torch/CUDA is absent."""
    gc.collect()
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
    except Exception:
        pass


@dataclass
class StageError:
    """A structured, JSON-serialisable record of one failure."""

    stage: str
    kind: str
    message: str
    tb: str = ""
    attempt: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage": self.stage,
            "kind": self.kind,
            "message": self.message[:2000],
            "traceback": self.tb[-4000:],
            "attempt": self.attempt,
        }


@dataclass
class ErrorCollector:
    """Accumulates StageError records for one sample."""

    errors: List[StageError] = field(default_factory=list)

    def add(self, stage: str, exc: BaseException, attempt: int = 0) -> StageError:
        err = StageError(
            stage=stage,
            kind=exc.__class__.__name__,
            message=str(exc),
            tb="".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
            attempt=attempt,
        )
        self.errors.append(err)
        return err

    @property
    def ok(self) -> bool:
        return not self.errors

    def stages(self) -> List[str]:
        return sorted({e.stage for e in self.errors})

    def to_list(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self.errors]


@dataclass
class RetryConfig:
    attempts: int = 3
    base_delay: float = 2.0
    max_delay: float = 30.0
    backoff: float = 2.0
    retry_on_oom: bool = True


def retry_call(
    fn: Callable[..., Any],
    *args: Any,
    retry: Optional[RetryConfig] = None,
    stage_name: str = "call",
    collector: Optional[ErrorCollector] = None,
    on_oom: Optional[Callable[[int], None]] = None,
    on_error: Optional[Callable[[int, BaseException], None]] = None,
    **kwargs: Any,
) -> Any:
    """Call `fn` with retries and exponential backoff.

    On a detected OOM the `on_oom(attempt)` hook runs before the next attempt so
    the caller can shrink its own workload (fewer pixels, fewer images).

    Re-raises the last exception if every attempt fails, so the caller decides
    whether the failure is fatal for the sample or merely degrades it.
    """
    cfg = retry or RetryConfig()
    delay = cfg.base_delay
    last: Optional[BaseException] = None

    for attempt in range(1, max(1, cfg.attempts) + 1):
        try:
            return fn(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit):
            raise
        except BaseException as exc:  # noqa: BLE001 - deliberate broad catch
            last = exc
            if collector is not None:
                collector.add(stage_name, exc, attempt=attempt)
            oom = is_oom(exc)
            LOG.warning(
                "[%s] attempt %d/%d failed (%s%s): %s",
                stage_name, attempt, cfg.attempts, exc.__class__.__name__,
                ", OOM" if oom else "", str(exc)[:300],
            )
            if oom:
                free_gpu()
                if on_oom is not None:
                    try:
                        on_oom(attempt)
                    except Exception:
                        LOG.exception("on_oom hook raised; continuing")
                if not cfg.retry_on_oom:
                    break
            elif on_error is not None:
                try:
                    on_error(attempt, exc)
                except Exception:
                    LOG.exception("on_error hook raised; continuing")

            if attempt >= cfg.attempts:
                break
            time.sleep(min(delay, cfg.max_delay))
            delay *= cfg.backoff

    assert last is not None
    raise last


@contextmanager
def stage(name: str, collector: ErrorCollector, reraise: bool = False) -> Iterator[Dict[str, Any]]:
    """Isolate an optional stage.

    Usage:
        with stage("relations", col) as box:
            box["value"] = build_relations(...)

    On failure the error is recorded and box["failed"] becomes True.
    """
    box: Dict[str, Any] = {"value": None, "failed": False}
    try:
        yield box
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as exc:  # noqa: BLE001
        box["failed"] = True
        collector.add(name, exc)
        LOG.warning("stage '%s' failed: %s: %s", name, exc.__class__.__name__, str(exc)[:300])
        if reraise:
            raise
