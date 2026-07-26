# project-path: tools/validate_architecture_review_large_file_refactor_workbench_intake_v1.py
"""Run Workbench intake validation for Large File Refactor Planner."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "architecture-review-large-file-refactor-workbench-intake-v1"


def main() -> int:
    """Execute the focused validation module."""
    project_root = Path(__file__).resolve().parents[1]
    project_root_text = str(project_root)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)
    validation = project_root / "validation" / "test_architecture_review_large_file_refactor_workbench_intake_v1.py"
    try:
        runpy.run_path(str(validation), run_name="__main__")
    except SystemExit as exc:
        if exc.code not in (0, None):
            raise
    print("ZIP CONTRACT: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
