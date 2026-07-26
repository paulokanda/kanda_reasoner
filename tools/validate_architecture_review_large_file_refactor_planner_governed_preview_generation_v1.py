# project-path: tools/validate_architecture_review_large_file_refactor_planner_governed_preview_generation_v1.py
"""Tool wrapper for governed preview generation validation."""
from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    script = Path(__file__).resolve().parents[1] / "validation" / "test_architecture_review_large_file_refactor_planner_governed_preview_generation_v1.py"
    raise SystemExit(runpy.run_path(str(script), run_name="__main__"))
