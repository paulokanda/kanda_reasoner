"""Validate Project-linked staging in the complete release routine."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from _answer_validate_freeze_memorize_contract import HELPER_REL, validate_all

FEATURE_ID = "answer-validate-freeze-memorize-daily-work-staging-v1"


def require(condition: bool, marker: str) -> None:
    """Raise on failure and print the passed marker."""
    if not condition:
        raise AssertionError(marker + ": FAIL")
    print(marker + ": PASS")


def load_helper(root: Path):
    """Load the canonical button helper from the selected Tool root."""
    path = root / HELPER_REL
    spec = importlib.util.spec_from_file_location("daily_work_answer_routine", path)
    require(spec is not None and spec.loader is not None, "DAILY_WORK_HELPER_IMPORT")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    """Validate dynamic daily-work staging without embedding prompt text in UI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve(strict=True)

    validate_all(root)
    helper = load_helper(root)
    wrapped = helper.build_answer_validate_freeze_memorize_wrapper(
        root,
        tool_root=root,
    )
    expected = root.parent / (root.name + "_delete_after_daily_work")
    require(
        "Selected project-linked transient root: " + str(expected.resolve())
        in wrapped,
        "PROJECT_LINKED_DAILY_WORK_ROOT",
    )
    require(
        "<project_drive>/<project_name>_delete_after_daily_work" in wrapped,
        "PROMPT_DYNAMIC_DAILY_WORK_CONTRACT",
    )
    require("Downloads/Desktop fallback" in wrapped, "NO_GENERIC_FALLBACK")
    require("Terminal 1 - INSTALL" in wrapped, "INSTALL_PHASE_PRESENT")
    require("Terminal 2 - VALIDATE" in wrapped, "VALIDATE_PHASE_PRESENT")
    require("Terminal 3 - FREEZE" in wrapped, "FREEZE_PHASE_PRESENT")
    require("Terminal 4 - ERROR MEMORY" in wrapped, "ERROR_MEMORY_PHASE_PRESENT")

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
