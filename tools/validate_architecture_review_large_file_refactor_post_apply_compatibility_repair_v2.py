# project-path: tools/validate_architecture_review_large_file_refactor_post_apply_compatibility_repair_v2.py
"""Run focused validation for Workbench post-apply compatibility repair v2."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-post-apply-compatibility-repair-v2"


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    test_path = project_root / "validation" / "test_architecture_review_large_file_refactor_post_apply_compatibility_repair_v2.py"
    result = subprocess.run([sys.executable, str(test_path)], cwd=str(project_root), check=False)
    if result.returncode != 0:
        return result.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
