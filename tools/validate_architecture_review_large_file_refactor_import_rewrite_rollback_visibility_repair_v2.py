# project-path: tools/validate_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_repair_v2.py
"""Validate import rewrite rollback visibility repair v2."""
from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-import-rewrite-rollback-visibility-repair-v2"
ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_rollback_executor.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_import_rewrite_rollback_formatting.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py",
    "validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_repair_v2.py",
    "tools/validate_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py",
    "tools/validate_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_repair_v2.py",
]


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def main() -> int:
    for rel in FILES:
        path = ROOT / rel
        if not path.exists():
            print(f"MISSING: {rel}", file=sys.stderr)
            return 1
        if rel.endswith(".py"):
            py_compile.compile(str(path), doraise=True)
            if _line_count(path) > 500:
                print(f"MODULE TOO LARGE: {rel}", file=sys.stderr)
                return 1

    tests = [
        ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_v1.py",
        ROOT / "validation/test_architecture_review_large_file_refactor_import_rewrite_rollback_visibility_repair_v2.py",
    ]
    for test_path in tests:
        completed = subprocess.run([sys.executable, str(test_path)], cwd=str(ROOT), text=True)
        if completed.returncode != 0:
            return completed.returncode

    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
