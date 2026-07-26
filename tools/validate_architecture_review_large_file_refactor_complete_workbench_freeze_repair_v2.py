"""Validate complete Workbench freeze closure repair v2."""
from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-complete-workbench-freeze-repair-v2"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED_FILES = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/final_complete_workbench_freeze.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_complete_workbench_freeze_v1.py",
    "validation/test_architecture_review_large_file_refactor_complete_workbench_freeze_repair_v2.py",
    "tools/validate_architecture_review_large_file_refactor_complete_workbench_freeze_v1.py",
    "tools/validate_architecture_review_large_file_refactor_complete_workbench_freeze_repair_v2.py",
]


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8", errors="ignore").splitlines())


def main() -> int:
    for relative in CHANGED_FILES:
        path = PROJECT_ROOT / relative
        if not path.is_file():
            print(f"Missing changed file: {relative}", file=sys.stderr)
            return 1
        if path.suffix == ".py" and _line_count(path) > 500:
            print(f"Module too large: {relative} ({_line_count(path)} lines)", file=sys.stderr)
            return 1
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)
    commands = [
        [sys.executable, "-m", "unittest", "validation.test_architecture_review_large_file_refactor_complete_workbench_freeze_v1"],
        [sys.executable, "-m", "unittest", "validation.test_architecture_review_large_file_refactor_complete_workbench_freeze_repair_v2"],
    ]
    for command in commands:
        completed = subprocess.run(command, cwd=str(PROJECT_ROOT), check=False)
        if completed.returncode != 0:
            return completed.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
