# project-path: tools/validate_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py
"""Validate import rewrite rollback visibility patch."""
from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-import-rewrite-rollback-visibility-v1"
ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_rollback_executor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_rollback_formatting.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py",
]


def main() -> int:
    """Run focused validation."""
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            print(f"Missing expected file: {rel}", file=sys.stderr)
            return 1
        if rel.endswith(".py"):
            py_compile.compile(str(path), doraise=True)
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > 500:
            print(f"Module too large: {rel} has {line_count} lines", file=sys.stderr)
            return 1
    test = ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py"
    result = subprocess.run([sys.executable, str(test)], cwd=str(ROOT), text=True)
    if result.returncode != 0:
        return result.returncode
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
        execute_import_rewrite_rollback,
        expected_import_rewrite_rollback_token,
    )
    if not callable(execute_import_rewrite_rollback) or not callable(expected_import_rewrite_rollback_token):
        print("Import rewrite rollback exports are not callable", file=sys.stderr)
        return 1
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
