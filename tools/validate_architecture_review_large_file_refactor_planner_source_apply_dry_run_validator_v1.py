# project-path: tools/validate_architecture_review_large_file_refactor_planner_source_apply_dry_run_validator_v1.py
"""Run Source Apply Dry-Run Validator v1 validation."""
from __future__ import annotations

import runpy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATION_SCRIPT = PROJECT_ROOT / "validation" / "test_architecture_review_large_file_refactor_planner_source_apply_dry_run_validator_v1.py"


def main() -> int:
    """Run the feature validation script."""
    runpy.run_path(str(VALIDATION_SCRIPT), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
