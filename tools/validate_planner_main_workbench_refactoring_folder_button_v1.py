"""Compatibility validation for the corrected Plan Action path button."""
from __future__ import annotations

import argparse
from pathlib import Path

from validate_planner_main_workbench_refactoring_path_clipboard_v1 import (
    _validate_runtime,
    _validate_static,
)

FEATURE_ID = "planner-main-workbench-refactoring-folder-button-v1"


def main() -> int:
    """Validate the installed corrected behavior without release metadata."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    project_root = Path(args.project_root).resolve()
    try:
        _validate_static(project_root)
        _validate_runtime(project_root)
    except Exception as error:
        print("VALIDATION FAILED: " + type(error).__name__ + ": " + str(error))
        return 1
    print("LEGACY_VALIDATOR_FORWARD_COMPATIBILITY: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
