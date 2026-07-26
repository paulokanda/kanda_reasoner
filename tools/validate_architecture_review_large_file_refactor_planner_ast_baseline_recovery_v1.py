# project-path: tools/validate_architecture_review_large_file_refactor_planner_ast_baseline_recovery_v1.py
"""Tool wrapper for AST baseline recovery validation."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> int:
    """Run the recovery validation from a stable tool entrypoint."""
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    script = project_root / "validation" / "test_architecture_review_large_file_refactor_planner_ast_baseline_recovery_v1.py"
    runpy.run_path(str(script), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
