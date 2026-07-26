# project-path: tools/validate_architecture_review_large_file_refactor_docstring_insertion_install_repair_v2.py
"""Run validation for docstring insertion install repair v2."""
from __future__ import annotations

import subprocess
import sys


FEATURE_ID = "architecture-review-large-file-refactor-docstring-insertion-install-repair-v2"


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "validation.test_architecture_review_large_file_refactor_docstring_insertion_install_repair_v2"],
        check=False,
        text=True,
    )
    if result.returncode != 0:
        return result.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
