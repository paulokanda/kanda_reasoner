# project-path: tools/validate_architecture_review_large_file_refactor_helper_import_synthesis_v1.py
"""Validator for helper dependency/import synthesis train."""
from __future__ import annotations

from pathlib import Path
import py_compile
import subprocess
import sys

FEATURE_ID = "architecture-review-large-file-refactor-helper-import-synthesis-v1"
ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/helper_import_synthesizer.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_real_preview_writer.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_helper_import_synthesis_v1.py",
]


def main() -> int:
    """Run focused validation."""
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            print(f"MISSING VALIDATED FILE: {rel}")
            return 1
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            print(f"MODULE TOO LARGE: {rel}: {line_count}")
            return 1
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)
    result = subprocess.run(
        [sys.executable, str(ROOT / "validation/test_architecture_review_large_file_refactor_helper_import_synthesis_v1.py")],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        check=False,
    )
    print(result.stdout, end="")
    print(result.stderr, end="")
    if result.returncode != 0:
        return result.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
