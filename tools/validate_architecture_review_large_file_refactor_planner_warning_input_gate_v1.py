# project-path: tools/validate_architecture_review_large_file_refactor_planner_warning_input_gate_v1.py
"""Run warning-input gate validation for the Large File Refactor Planner."""
from __future__ import annotations

import runpy
from pathlib import Path

__all__: list[str] = []

FEATURE_ID = "architecture-review-large-file-refactor-planner-warning-input-gate-v1"


def main() -> int:
    """Execute the focused validation module."""
    project_root = Path(__file__).resolve().parents[1]
    validation = project_root / "validation" / "test_architecture_review_large_file_refactor_planner_warning_input_gate_v1.py"
    runpy.run_path(str(validation), run_name="__main__")
    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
