# project-path: tools/validate_large_file_refactor_planner_ast_target_auto_sync_v1.py
"""CLI wrapper for the AST target auto-sync focused validator."""
from __future__ import annotations

import argparse
from pathlib import Path
import runpy


def main() -> int:
    """Run the focused validator against one project root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root")
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    validator = project_root / (
        "validation/test_large_file_refactor_planner_ast_target_auto_sync_v1.py"
    )
    namespace = runpy.run_path(str(validator))
    namespace["validate"](str(project_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
