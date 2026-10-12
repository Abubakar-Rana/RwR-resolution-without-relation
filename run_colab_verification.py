"""Standalone Colab and GPU Verification Script for Test3 Grand Synthesis.

Runs the complete 4-stage verification suite:
1. Environment and GPU Hardware Probe
2. 63-Test Pytest Suite Execution
3. Live Inference / Trace Matching on Representative XLRS-Bench Items
4. End-to-End Grand Synthesis Benchmark Audit (2,983 Items)
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import time

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "work" / "src" if (ROOT_DIR / "work" / "src").exists() else ROOT_DIR / "src"
MATERIALS_DIR = ROOT_DIR / "work" / "materials" if (ROOT_DIR / "work" / "materials").exists() else ROOT_DIR / "materials"

sys.path.insert(0, str(SRC_DIR))


def log_header(title: str) -> None:
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def stage1_gpu_probe() -> None:
    log_header("STAGE 1: GPU & HARDWARE ENVIRONMENT PROBE")
    try:
        import torch
        print(f"PyTorch Version: {torch.__version__}")
        print(f"CUDA Available:  {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            dev_name = torch.cuda.get_device_name(0)
            vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            print(f"GPU Device:      {dev_name}")
            print(f"Total VRAM:      {vram_gb:.2f} GB")
        else:
            print("Running in CPU mode.")
    except ImportError:
        print("ERROR: torch is not installed.")
        sys.exit(1)


def stage2_run_unit_tests() -> bool:
    log_header("STAGE 2: RUNNING 63-TEST UNIT VERIFICATION SUITE")
    tests_dir = ROOT_DIR / "tests"
    if not tests_dir.exists():
        print(f"Warning: {tests_dir} not found. Skipping pytest stage.")
        return False

    cmd = [sys.executable, "-m", "pytest", str(tests_dir), "-v"]
    print(f"Executing: {' '.join(cmd)}\n")
    res = subprocess.run(cmd, cwd=str(ROOT_DIR))
    if res.returncode == 0:
        print("\n==> [PASS] All unit tests executed cleanly with 100% pass rate!")
        return True
    else:
        print(f"\n==> [FAIL] Unit tests exited with code {res.returncode}")
        return False


def stage3_run_colab_inference_runner() -> bool:
    log_header("STAGE 3: LIVE INFERENCE / TRACE TOKEN VERIFICATION")
    runner_script = SRC_DIR / "models" / "colab_inference_runner.py"
    if not runner_script.exists():
        print(f"ERROR: {runner_script} not found.")
        return False

    cmd = [sys.executable, str(runner_script)]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR))
    if res.returncode == 0:
        print("\n==> [PASS] Inference and trace verification completed successfully!")
        return True
    else:
        print(f"\n==> [FAIL] Inference runner failed with code {res.returncode}")
        return False


def stage4_run_benchmark_eval() -> bool:
    log_header("STAGE 4: GRAND SYNTHESIS BENCHMARK AUDIT (2,983 ITEMS)")
    bench_script = SRC_DIR / "models" / "benchmark_test3_eval.py"
    if not bench_script.exists():
        print(f"ERROR: {bench_script} not found.")
        return False

    cmd = [sys.executable, str(bench_script)]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR))
    if res.returncode == 0:
        print("\n==> [PASS] Full benchmark audit completed successfully!")
        return True
    else:
        print(f"\n==> [FAIL] Benchmark evaluation failed with code {res.returncode}")
        return False


def main() -> None:
    start_time = time.time()
    log_header("STARTING TEST3 COMPLETE VERIFICATION PIPELINE")
    stage1_gpu_probe()
    p2 = stage2_run_unit_tests()
    p3 = stage3_run_colab_inference_runner()
    p4 = stage4_run_benchmark_eval()

    elapsed = time.time() - start_time
    log_header("FINAL VERIFICATION SUMMARY")
    print(f"Unit Tests (63 items):         {'PASSED [OK]' if p2 else 'FAILED'}")
    print(f"Token Trace Match (3 items):   {'PASSED [OK]' if p3 else 'FAILED'}")
    print(f"Full Benchmark (2,983 items):  {'PASSED [OK]' if p4 else 'FAILED'}")
    print(f"Total Verification Wall-Time:  {elapsed:.2f} seconds\n")

    if p2 and p3 and p4:
        print("ALL VERIFICATION CHECKS PASSED WITH 100% COMPLIANCE!")
    else:
        print("WARNING: Some verification steps failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
