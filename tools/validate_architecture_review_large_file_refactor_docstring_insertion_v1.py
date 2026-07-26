# project-path: tools/validate_architecture_review_large_file_refactor_docstring_insertion_v1.py
"""Run validation for Large File Refactor docstring insertion train."""
from __future__ import annotations

import subprocess
import sys


def main() -> int:
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "validation.test_architecture_review_large_file_refactor_docstring_insertion_v1"],
        check=False,
        text=True,
    )
    if result.returncode != 0:
        return result.returncode
    print("VALIDATION OK: architecture-review-large-file-refactor-docstring-insertion-v1")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
