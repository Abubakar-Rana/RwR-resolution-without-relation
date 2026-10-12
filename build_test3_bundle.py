"""Package test3_colab_complete_bundle.zip for Google Colab deployment."""
from __future__ import annotations

import os
from pathlib import Path
import shutil
import zipfile

ROOT_DIR = Path(__file__).resolve().parent
OUT_ZIP_LOCAL = ROOT_DIR / "work" / "materials" / "test3_colab_complete_bundle.zip"
OUT_ZIP_MAIN_ROOT = Path("d:/projects/research/vlm/test3_colab_complete_bundle.zip")
OUT_ZIP_MAIN_MAT = Path("d:/projects/research/vlm/work/materials/test3_colab_complete_bundle.zip")

print("Packaging test3_colab_complete_bundle.zip...")

if OUT_ZIP_LOCAL.exists():
    OUT_ZIP_LOCAL.unlink()

with zipfile.ZipFile(OUT_ZIP_LOCAL, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    # 1. work/src
    for p in (ROOT_DIR / "work" / "src").rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".pyc"):
            arcname = p.relative_to(ROOT_DIR).as_posix()
            zf.write(p, arcname)

    # 2. tests
    for p in (ROOT_DIR / "tests").rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".pyc"):
            arcname = p.relative_to(ROOT_DIR).as_posix()
            zf.write(p, arcname)

    # 3. run_colab_verification.py
    run_script = ROOT_DIR / "run_colab_verification.py"
    if run_script.exists():
        zf.write(run_script, "run_colab_verification.py")

    # 4. Standalone notebooks and instructions in root
    nb_file = ROOT_DIR / "work" / "materials" / "Test3_Colab_Grand_Synthesis_Verification.ipynb"
    if nb_file.exists():
        zf.write(nb_file, "Test3_Colab_Grand_Synthesis_Verification.ipynb")

    instr_file = ROOT_DIR / "work" / "materials" / "INSTRUCTIONS_TEST3_COLAB.md"
    if instr_file.exists():
        zf.write(instr_file, "INSTRUCTIONS_TEST3_COLAB.md")

    # 5. work/materials core subdirectories (ctsr, analysis, results, logs)
    materials_dir = ROOT_DIR / "work" / "materials"
    for sub in ["rwr_repo/analysis", "rwr_repo/ctsr", "rwr_repo/results", "rwr_repo/notebooks/colab"]:
        target_dir = materials_dir / sub
        if target_dir.exists():
            for p in target_dir.rglob("*"):
                if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".pyc"):
                    arcname = p.relative_to(ROOT_DIR).as_posix()
                    zf.write(p, arcname)

    # 6. Specific trace logs in materials
    for log_name in ["colab_inference_trace_log.json", "colab_inference_trace_log.md"]:
        log_path = materials_dir / log_name
        if log_path.exists():
            zf.write(log_path, f"work/materials/{log_name}")

size_mb = OUT_ZIP_LOCAL.stat().st_size / (1024.0 * 1024.0)
print(f"Successfully packaged {OUT_ZIP_LOCAL} ({size_mb:.2f} MB)")

# Copy to main repo locations
for dest in [OUT_ZIP_MAIN_ROOT, OUT_ZIP_MAIN_MAT]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUT_ZIP_LOCAL, dest)
    print(f"Copied to {dest} ({dest.stat().st_size / (1024.0 * 1024.0):.2f} MB)")
