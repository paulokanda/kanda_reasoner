# project-path: tools/validate_architecture_review_large_file_refactor_planner_docstring_contracts_v1.py
"""Tool wrapper for the Large File Refactor Planner docstring contract validator."""
from __future__ import annotations

import runpy
from pathlib import Path


def main() -> int:
    """Run the focused validation script from the tools entrypoint."""
    root = Path(__file__).resolve().parents[1]
    script = root / "validation" / "test_architecture_review_large_file_refactor_planner_docstring_contracts_v1.py"
    namespace = runpy.run_path(str(script), run_name="docstring_contracts_v1")
    return int(namespace["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
