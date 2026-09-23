"""Logging helpers: one console+file logger per run."""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

_CONFIGURED: set = set()

_FMT = "%(asctime)s | %(levelname)-7s | %(name)-24s | %(message)s"


def get_logger(name: str = "ctsr", logfile=None, level: str = "INFO") -> logging.Logger:
    """Return a logger writing to stderr and, optionally, to `logfile`.

    Safe to call repeatedly with the same name; handlers are attached once.
    """
    logger = logging.getLogger(name)
    key = "{}:{}".format(name, logfile)
    if key in _CONFIGURED:
        return logger

    logger.setLevel(getattr(logging, str(level).upper(), logging.INFO))
    logger.propagate = False
    fmt = logging.Formatter(_FMT)

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        sh = logging.StreamHandler(stream=sys.stderr)
        sh.setFormatter(fmt)
        logger.addHandler(sh)

    if logfile is not None:
        try:
            p = Path(logfile)
            p.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(p, encoding="utf-8")
            fh.setFormatter(fmt)
            logger.addHandler(fh)
        except OSError as exc:  # never let logging setup kill a run
            logger.warning("Could not open logfile %s: %s", logfile, exc)

    _CONFIGURED.add(key)
    return logger


def set_global_level(level: str) -> None:
    logging.getLogger("ctsr").setLevel(getattr(logging, str(level).upper(), logging.INFO))
