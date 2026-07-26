# project-path: validation/test_no_leak_logic_bridge_v1.py
"""Validate the NO_LEAK_LOGIC_V1 prompt and startup bridge patch."""

from __future__ import annotations

import py_compile
from pathlib import Path


FEATURE_ID = "no-leak-logic-bridge-v1"
PROJECT_ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md",
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py",
    "kanda_prompt_workspace/prompt_tools/startup_kernel/startup_source_map.py",
    "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json",
)


REQUIRED_TOKENS = {
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/box_architecture_canon.md": (
        "NO_LEAK_LOGIC_V1",
        "No-Leak Logic Object",
        "NO-LEAK CHECK",
        "Tool/project leakage",
        "Wrong-root leakage",
        "Generated-artifact leakage",
        "Validation/freeze leakage",
        "Refactor-output leakage",
    ),
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md": (
        "No-Leak Shield Checklist",
        "NO_LEAK_LOGIC_V1",
        "tool/project ownership leakage",
        "wrong-root writes",
        "generated-artifact-as-source leakage",
    ),
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md": (
        "No-Leak tool/project rule",
        "NO_LEAK_LOGIC_V1",
        "Reusable tool engines",
        "Concrete generated or refactored files",
    ),
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/start_of_day_master_stack.md": (
        "BEGINNING_OF_DAY_NO_LEAK_LOGIC_BRIDGE",
        "BEGINNING_OF_DAY_NO_LEAK_LOGIC_V1_START",
        "BEGINNING_OF_DAY_NO_LEAK_LOGIC_V1_END",
        "NO-LEAK CHECK",
    ),
    "kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py": (
        "No-Leak Logic Bridge",
        "NO_LEAK_LOGIC_V1 prevents wrong-root writes",
        "validation/freeze evidence leakage",
    ),
    "kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py": (
        "No-Leak Logic Bridge",
        "NO_LEAK_LOGIC_V1 prevents wrong-root writes",
        "validation/freeze evidence leakage",
    ),
    "kanda_prompt_workspace/prompt_tools/startup_kernel/startup_source_map.py": (
        "No-Leak Logic Bridge",
    ),
    "kanda_prompt_workspace/prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json": (
        "No-Leak Logic Bridge",
    ),
}


def _read(relative_path: str) -> str:
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError("Missing required file: " + relative_path)
    return path.read_text(encoding="utf-8", errors="replace")


def _assert_tokens() -> None:
    for relative_path in REQUIRED_FILES:
        _read(relative_path)
    for relative_path, tokens in REQUIRED_TOKENS.items():
        text = _read(relative_path)
        missing = [token for token in tokens if token not in text]
        if missing:
            raise AssertionError(
                "Missing tokens in " + relative_path + ": " + ", ".join(missing)
            )


def _assert_bridge_order() -> None:
    for relative_path in (
        "kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py",
        "kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py",
    ):
        text = _read(relative_path)
        code_index = text.find("1. Code Module Size Bridge")
        box_index = text.find("2. Box Logic Startup Bridge")
        leak_index = text.find("3. No-Leak Logic Bridge")
        terminal_index = text.find("4. Terminal Cleanup Bridge")
        if -1 in (code_index, box_index, leak_index, terminal_index):
            raise AssertionError("Startup bridge numbering missing in " + relative_path)
        if not (code_index < box_index < leak_index < terminal_index):
            raise AssertionError("Startup bridge order is invalid in " + relative_path)


def _assert_python_compiles() -> None:
    for relative_path in (
        "kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py",
        "kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py",
        "kanda_prompt_workspace/prompt_tools/startup_kernel/startup_source_map.py",
    ):
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def main() -> int:
    _assert_tokens()
    _assert_bridge_order()
    _assert_python_compiles()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: SOURCE_CHECKED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
