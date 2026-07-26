# project-path: tools/validate_architecture_review_large_file_refactor_planner_multifile_recovery_evidence_v1.py
"""Run Multi-File Recovery Evidence v1 validation."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    """Run the validation module as a script."""
    project_root_text = str(PROJECT_ROOT)
    if project_root_text not in sys.path:
        sys.path.insert(0, project_root_text)
    target = PROJECT_ROOT / "validation" / "test_architecture_review_large_file_refactor_planner_multifile_recovery_evidence_v1.py"
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
