"""Run validation for Large File Refactor final integration hardening v1."""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

FEATURE_ID = "architecture-review-large-file-refactor-final-integration-hardening-v1"


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    env["KANDA_PROJECT_ROOT"] = str(project_root)
    test_file = project_root / "validation" / "test_architecture_review_large_file_refactor_final_integration_hardening_v1.py"
    result = subprocess.run([sys.executable, str(test_file)], cwd=str(project_root), env=env)
    if result.returncode != 0:
        return result.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
