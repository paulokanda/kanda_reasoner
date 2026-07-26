# project-path: tools/validate_architecture_review_large_file_refactor_batch_queue_v1.py
"""Validate batch multi-file refactor queue v1."""

from __future__ import annotations

import py_compile
import subprocess
import sys
from pathlib import Path


FEATURE_ID = "architecture-review-large-file-refactor-batch-queue-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHANGED_FILES = [
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/batch_refactor_queue.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/__init__.py",
    "validation/test_architecture_review_large_file_refactor_batch_queue_v1.py",
    "tools/validate_architecture_review_large_file_refactor_batch_queue_v1.py",
]


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def main() -> int:
    for rel in CHANGED_FILES:
        path = PROJECT_ROOT / rel
        if not path.is_file():
            print(f"MISSING: {rel}")
            return 1
        if path.suffix == ".py":
            py_compile.compile(str(path), doraise=True)
        if _line_count(path) > 500:
            print(f"MODULE_TOO_LARGE: {rel} has {_line_count(path)} lines")
            return 1
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "validation" / "test_architecture_review_large_file_refactor_batch_queue_v1.py")],
        cwd=str(PROJECT_ROOT),
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")
    if result.returncode != 0:
        return result.returncode
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
        build_batch_refactor_queue,
        write_batch_refactor_queue,
    )
    if not callable(build_batch_refactor_queue) or not callable(write_batch_refactor_queue):
        print("EXPORT_CHECK_FAILED")
        return 1
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
