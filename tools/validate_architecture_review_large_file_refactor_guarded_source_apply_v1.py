# project-path: tools/validate_architecture_review_large_file_refactor_guarded_source_apply_v1.py
"""Run guarded source apply validation for Large File Refactor Workbench."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATION_SCRIPT = (
    PROJECT_ROOT
    / "validation"
    / "test_architecture_review_large_file_refactor_guarded_source_apply_v1.py"
)

if __name__ == "__main__":
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    namespace = runpy.run_path(str(VALIDATION_SCRIPT))
    namespace["main"]()
