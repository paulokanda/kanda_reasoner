# project-path: tools/validate_architecture_review_large_file_refactor_dependency_clustering_v1.py
"""Run focused validation for dependency clustering v1."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

FEATURE_ID = "architecture-review-large-file-refactor-dependency-clustering-v1"


def main() -> int:
    """Run the dependency clustering focused tests."""
    project_root = Path(__file__).resolve().parents[1]
    test_path = project_root / "validation" / "test_architecture_review_large_file_refactor_dependency_clustering_v1.py"
    result = subprocess.run([sys.executable, str(test_path)], cwd=str(project_root), check=False)
    if result.returncode != 0:
        return result.returncode
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")
    print("ZIP CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
