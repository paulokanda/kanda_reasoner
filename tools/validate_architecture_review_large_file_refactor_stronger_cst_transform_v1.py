# project-path: tools/validate_architecture_review_large_file_refactor_stronger_cst_transform_v1.py
"""Run validation for stronger CST transform fidelity."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-stronger-cst-transform-v1"


def main() -> int:
    """Run focused validation and print stable markers."""
    root = Path(__file__).resolve().parents[1]
    test = root / "validation" / "test_architecture_review_large_file_refactor_stronger_cst_transform_v1.py"
    result = subprocess.run([sys.executable, str(test)], cwd=str(root), text=True)
    if result.returncode != 0:
        return result.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
