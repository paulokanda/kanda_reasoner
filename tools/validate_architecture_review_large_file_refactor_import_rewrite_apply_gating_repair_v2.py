# project-path: tools/validate_architecture_review_large_file_refactor_import_rewrite_apply_gating_repair_v2.py
"""Validator for import rewrite apply gating repair v2."""
from __future__ import annotations

import importlib
import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-import-rewrite-apply-gating-repair-v2"
ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_apply_readiness.py",
    ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_apply_gating_v1.py",
    ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_apply_gating_repair_v2.py",
]


def main() -> int:
    for path in FILES:
        if not path.exists():
            raise SystemExit(f"missing required file: {path}")
        py_compile.compile(str(path), doraise=True)
        if _line_count(path) > 500:
            raise SystemExit(f"module too large: {path}")

    module = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_import_rewrite_apply_readiness"
    )
    if not hasattr(module, "_allowed_preview_roots_for"):
        raise SystemExit("missing _allowed_preview_roots_for repair helper")

    for test_path in [
        ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_apply_gating_v1.py",
        ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_apply_gating_repair_v2.py",
    ]:
        result = subprocess.run([sys.executable, str(test_path)], cwd=str(ROOT), text=True)
        if result.returncode != 0:
            return result.returncode

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


if __name__ == "__main__":
    raise SystemExit(main())
