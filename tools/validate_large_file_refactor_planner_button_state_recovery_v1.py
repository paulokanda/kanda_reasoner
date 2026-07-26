# project-path: tools/validate_large_file_refactor_planner_button_state_recovery_v1.py
"""CLI wrapper for Planner button-state recovery validation."""
from __future__ import annotations

import argparse
from pathlib import Path
import runpy


def main() -> int:
    """Run the focused validator against one project root."""
    parser = argparse.ArgumentParser()
    parser.add_argument("project_root")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    validator = root / (
        "validation/test_large_file_refactor_planner_button_state_recovery_v1.py"
    )
    namespace = runpy.run_path(str(validator))
    namespace["validate"](str(root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
