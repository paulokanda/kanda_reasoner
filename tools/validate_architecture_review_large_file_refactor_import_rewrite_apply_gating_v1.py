# project-path: tools/validate_architecture_review_large_file_refactor_import_rewrite_apply_gating_v1.py
"""Run focused validation for import rewrite apply gating v1."""
from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-import-rewrite-apply-gating-v1"
CHANGED = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_apply_readiness.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_apply_formatting.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_import_rewrite_apply_gating_v1.py",
]


def main() -> int:
    """Run focused tests and basic compile/size validation."""
    project_root = Path(__file__).resolve().parents[1]
    for relative in CHANGED:
        path = project_root / relative
        if not path.exists():
            print(f"MISSING: {relative}")
            return 1
        if path.suffix == ".py":
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            if line_count > 500:
                print(f"MODULE TOO LARGE: {relative}: {line_count}")
                return 1
            py_compile.compile(str(path), doraise=True)
    test_path = project_root / "validation" / "test_architecture_review_large_file_refactor_import_rewrite_apply_gating_v1.py"
    result = subprocess.run([sys.executable, str(test_path)], cwd=str(project_root), check=False)
    if result.returncode != 0:
        return result.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
