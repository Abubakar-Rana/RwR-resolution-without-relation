"""Deterministic seeding across python / numpy / torch."""
from __future__ import annotations

import os
import random


def set_seed(seed: int = 1234, deterministic_torch: bool = True) -> int:
    """Seed every RNG we can reach. Returns the seed so callers can log it."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except Exception:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        if deterministic_torch:
            # Best effort: some VLM kernels have no deterministic implementation,
            # so we request determinism but never hard-fail on it.
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except Exception:
        pass
    return seed
