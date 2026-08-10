"""Validate separated terminal phases for the complete release routine."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from _answer_validate_freeze_memorize_contract import validate_all

FEATURE_ID = "answer-validate-freeze-memorize-separated-terminal-phases-v1"
PROMPT_REL = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "patch_validate_freeze_error_memory_routine_blueprint.md"
)
HELPER_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "answer_validate_freeze_memorize_button_private_impl.py"
)
UI_REL = Path(
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/"
    "window_methods_private_impl.py"
)


def require(condition: bool, marker: str) -> None:
    """Raise when a validation condition is false and print on success."""
    if not condition:
        raise AssertionError(marker + ": FAIL")
    print(marker + ": PASS")


def load_helper(root: Path):
    """Load the button helper from the selected source root."""
    path = root / HELPER_REL
    spec = importlib.util.spec_from_file_location("separated_answer_routine", path)
    require(spec is not None and spec.loader is not None, "BUTTON_HELPER_IMPORT")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    """Run focused validation for the phase-separated release contract."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve(strict=True)

    validate_all(root)
    prompt = (root / PROMPT_REL).read_text(encoding="utf-8")
    ui = (root / UI_REL).read_text(encoding="utf-8")

    require(
        "one self-contained feature or update ZIP" in prompt
        and "exactly one primary feature/update ZIP" in prompt,
        "ONE_PRIMARY_UPDATE_ZIP",
    )
    require(
        "Do not require a separate installer" in prompt
        and "validation-report download" in prompt,
        "NO_SEPARATE_INSTALLER_VALIDATOR_REPORT_DOWNLOADS",
    )

    phases = (
        "### Terminal 1 - INSTALL",
        "### Terminal 2 - VALIDATE",
        "### Terminal 3 - FREEZE",
        "### Terminal 4 - ERROR MEMORY",
    )
    positions = [prompt.index(marker) for marker in phases]
    require(positions == sorted(positions), "TERMINAL_PHASE_ORDER")
    require(
        "One terminal block never executes two lifecycle phases" in prompt
        and "Never present an all-in-one command" in prompt,
        "TERMINAL_PHASE_ISOLATION",
    )
    require(
        "INSTALL PHASE COMPLETE: <feature_id>" in prompt
        and "VALIDATION OK: <feature_id>" in prompt
        and "STATUS: IN_SYNC" in prompt,
        "INSTALL_AND_VALIDATE_MARKERS",
    )
    require(
        "FREEZE DISPOSITION: PREPARED_FOR_HUMAN_CONFIRMATION" in prompt
        and "not run Preview or Confirm and Write" in prompt,
        "FREEZE_SEPARATE_HUMAN_GATE",
    )
    require(
        "ERROR MEMORY DISPOSITION: NOT_REQUIRED" in prompt
        and "The terminal must never execute `Memorize Error`" in prompt,
        "ERROR_MEMORY_SEPARATE_HUMAN_GATE",
    )
    require(
        "*_VALIDATION_REPORT.txt" in prompt
        and "Do not expose disposable reports as downloads" in prompt,
        "NO_ORPHAN_REPORT_DOWNLOAD",
    )

    helper = load_helper(root)
    wrapped = helper.build_answer_validate_freeze_memorize_wrapper(
        root,
        tool_root=root,
    )
    require("version: 3.2" in wrapped, "BUTTON_CURRENT_PROMPT_VERSION")
    require("Terminal phase rule:" in wrapped, "BUTTON_TERMINAL_PHASE_RULE")
    require(
        "separate INSTALL, VALIDATE, FREEZE, and ERROR MEMORY terminal blocks"
        in wrapped,
        "BUTTON_SEPARATED_PHASES",
    )
    require("Freeze rule:" in wrapped, "BUTTON_FREEZE_GATE")
    require("Error Memory rule:" in wrapped, "BUTTON_ERROR_MEMORY_GATE")
    require(
        str((root / PROMPT_REL).resolve()) in wrapped,
        "BUTTON_CANONICAL_PROMPT_LINK",
    )
    require(
        "update ZIP followed by separate Install, Validate, Freeze, and Error " in ui
        and "Memory terminal phases." in ui,
        "BUTTON_TOOLTIP_PHASE_SEQUENCE",
    )

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
