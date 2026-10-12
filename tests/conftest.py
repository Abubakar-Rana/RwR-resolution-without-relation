"""Pytest configuration and environment fixtures for Test 3 tests."""
import sys
from pathlib import Path

# Add work/src to sys.path
SRC_PATH = Path(__file__).resolve().parent.parent / "work" / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
