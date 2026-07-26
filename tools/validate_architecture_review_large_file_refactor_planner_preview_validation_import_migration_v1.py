# project-path: tools/validate_architecture_review_large_file_refactor_planner_preview_validation_import_migration_v1.py
"""Tool wrapper for preview artifact validation and import migration preview."""
from __future__ import annotations

import runpy
from pathlib import Path

if __name__ == "__main__":
    script = Path(__file__).resolve().parents[1] / "validation" / "test_architecture_review_large_file_refactor_planner_preview_validation_import_migration_v1.py"
    raise SystemExit(runpy.run_path(str(script), run_name="__main__"))
