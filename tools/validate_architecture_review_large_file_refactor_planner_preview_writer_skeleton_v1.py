# project-path: tools/validate_architecture_review_large_file_refactor_planner_preview_writer_skeleton_v1.py
"""Wrapper for Architecture Review Large File Refactor Planner Preview Writer Skeleton v1 validation."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATION_SCRIPT = (
    PROJECT_ROOT
    / "validation"
    / "test_architecture_review_large_file_refactor_planner_preview_writer_skeleton_v1.py"
)


def main() -> int:
    """Run the validation script without importing a test module."""
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    namespace = runpy.run_path(str(VALIDATION_SCRIPT))
    return int(namespace["main"]())

if __name__ == "__main__":
    raise SystemExit(main())
