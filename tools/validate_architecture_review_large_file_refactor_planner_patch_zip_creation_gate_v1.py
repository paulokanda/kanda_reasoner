# project-path: tools/validate_architecture_review_large_file_refactor_planner_patch_zip_creation_gate_v1.py
"""Run patch ZIP creation gate validation."""
from __future__ import annotations

import runpy
from pathlib import Path


def main() -> int:
    """Run the feature validator."""
    root = Path(__file__).resolve().parents[1]
    target = root / "validation/test_architecture_review_large_file_refactor_planner_patch_zip_creation_gate_v1.py"
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
