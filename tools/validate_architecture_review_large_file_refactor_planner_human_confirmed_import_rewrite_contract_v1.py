# project-path: tools/validate_architecture_review_large_file_refactor_planner_human_confirmed_import_rewrite_contract_v1.py
"""Wrapper validator for Human-Confirmed Import Rewrite Contract v1."""
from __future__ import annotations

import runpy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_PATH = PROJECT_ROOT / "validation" / "test_architecture_review_large_file_refactor_planner_human_confirmed_import_rewrite_contract_v1.py"


def main() -> int:
    """Run the focused feature validation script."""
    runpy.run_path(str(TEST_PATH), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
