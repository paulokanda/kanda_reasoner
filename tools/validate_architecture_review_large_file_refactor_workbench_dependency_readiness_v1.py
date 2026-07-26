# project-path: tools/validate_architecture_review_large_file_refactor_workbench_dependency_readiness_v1.py
"""CLI wrapper for Workbench dependency readiness validation."""
from __future__ import annotations

from pathlib import Path
import runpy
import sys


def main() -> None:
    """Run the focused validation script from the project root."""
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    target = root / "validation/test_architecture_review_large_file_refactor_workbench_dependency_readiness_v1.py"
    runpy.run_path(str(target), run_name="__main__")


if __name__ == "__main__":
    main()
