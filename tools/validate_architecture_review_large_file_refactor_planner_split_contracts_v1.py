# project-path: tools/validate_architecture_review_large_file_refactor_planner_split_contracts_v1.py
"""Tool wrapper for split-contract validation."""
from __future__ import annotations

import runpy
from pathlib import Path


def main() -> int:
    """Run the focused validation script from the project root."""
    root = Path(__file__).resolve().parents[1]
    script = root / "validation" / "test_architecture_review_large_file_refactor_planner_split_contracts_v1.py"
    runpy.run_path(str(script), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
