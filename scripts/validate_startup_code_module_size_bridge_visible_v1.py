# project-path: scripts/validate_startup_code_module_size_bridge_visible_v1.py
"""Validate startup-visible code module hard max bridge behavior."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import runpy
import sys

__all__ = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STARTUP_STACK = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_library"
    / "ACTIVE_PROMPTS"
    / "01_session_start_and_navigation"
    / "start_of_day_master_stack.md"
)
STARTUP_STACK_ROOT_MIRROR = (
    PROJECT_ROOT
    / "prompt_library"
    / "ACTIVE_PROMPTS"
    / "01_session_start_and_navigation"
    / "start_of_day_master_stack.md"
)
SOURCE_MAP = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_tools"
    / "STARTUP_ROUTING_KERNEL_SOURCES.json"
)
BOOT_TEXT = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_tools"
    / "startup_kernel"
    / "boot_text.py"
)
START_HERE_LISTS = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_tools"
    / "startup_kernel"
    / "start_here_lists.py"
)

PROMPT_TOOLS_ROOT = (
    PROJECT_ROOT
    / "kanda_prompt_workspace"
    / "prompt_tools"
)

REQUIRED_STARTUP_TEXT = (
    "BEGINNING_OF_DAY_CODE_MODULE_SIZE_BRIDGE",
    "BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_START",
    "CODE_MODULE_HARD_MAX_500_LINES",
    "Absolute hard maximum code/source module size: 500 physical lines or fewer.",
    "Every new or touched code/source module must be at most 500 physical lines",
    "including creation, update, modification, refactor, or",
    "Do not create, keep, enlarge, or deliver a touched code/source module above",
    "route to `large_module_refactor_protocol.md`",
    "BEGINNING_OF_DAY_CODE_MODULE_SIZE_HARD_GATE_V1_END",
)

REQUIRED_GENERATOR_TEXT = (
    "Code Module Size Bridge - loaded/missing",
    "hard gate: ideal <=400 code lines; maximum <=500 physical lines",
    "every new or touched code/source module must be <=500 lines after",
    "create, update, modify, refactor, or split work",
    "route above-limit code work to large_module_refactor_protocol on demand",
)

REQUIRED_BOOT_DELEGATION = (
    "from startup_kernel.start_here_lists import build_active_bridge_report",
    "active_bridge_report = build_active_bridge_report()",
)

TOUCHED_CODE_FILES = (
    Path("kanda_prompt_workspace/prompt_tools/startup_kernel/boot_text.py"),
    Path("kanda_prompt_workspace/prompt_tools/startup_kernel/start_here_lists.py"),
    Path("scripts/validate_startup_code_module_size_bridge_visible_v1.py"),
)


def read_text(path: Path) -> str:
    """Read a UTF-8 text file with a clear missing-file error."""
    if not path.is_file():
        raise AssertionError("missing required file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="replace")


def assert_contains_all(text: str, needles: tuple[str, ...], label: str) -> None:
    """Assert that all expected strings are present in text."""
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise AssertionError(label + " missing expected text: " + repr(missing))


def assert_python_module_under_500(relative_path: Path) -> None:
    """Assert that a touched Python source file stays within the hard limit."""
    path = PROJECT_ROOT / relative_path
    text = read_text(path)
    ast.parse(text, filename=str(path))
    line_count = len(text.splitlines())
    if line_count > 500:
        raise AssertionError(
            str(relative_path) + " exceeds 500 lines: " + str(line_count)
        )


def validate_startup_stack() -> None:
    """Validate the canonical bridge and the non-authoritative redirect."""
    assert_contains_all(
        read_text(STARTUP_STACK),
        REQUIRED_STARTUP_TEXT,
        "startup stack",
    )
    assert_contains_all(
        read_text(STARTUP_STACK_ROOT_MIRROR),
        (
            "Deprecated duplicate source",
            "not canonical",
            "KPR-01-001 start_of_day_master_stack",
        ),
        "root prompt-library redirect",
    )


def validate_source_map() -> None:
    """Validate the startup source map still loads the bridge at startup."""
    source_map = json.loads(read_text(SOURCE_MAP))
    entries = source_map.get("startup_sources", [])
    matches = [
        entry
        for entry in entries
        if entry.get("generated_filename") == "05_start_of_day_master_stack.md"
    ]
    if len(matches) != 1:
        raise AssertionError(
            "expected exactly one start_of_day_master_stack startup source"
        )
    role = str(matches[0].get("role", ""))
    if "beginning-of-day Code Module Size Bridge" not in role:
        raise AssertionError(
            "source map role does not name the beginning-of-day "
            "Code Module Size Bridge"
        )
    if matches[0].get("load_mode") != "always_startup":
        raise AssertionError("start_of_day_master_stack must remain always_startup")


def validate_generator_bridge_reports() -> None:
    """Validate startup load checks obtain the hard gate from one owner."""
    lists_text = read_text(START_HERE_LISTS)
    ast.parse(lists_text, filename=str(START_HERE_LISTS))
    prompt_tools_text = str(PROMPT_TOOLS_ROOT)
    inserted = prompt_tools_text not in sys.path
    if inserted:
        sys.path.insert(0, prompt_tools_text)
    try:
        lists_namespace = runpy.run_path(str(START_HERE_LISTS))
    finally:
        if inserted:
            sys.path.remove(prompt_tools_text)
    bridge_report = lists_namespace["build_active_bridge_report"]()
    assert_contains_all(
        bridge_report,
        REQUIRED_GENERATOR_TEXT,
        str(START_HERE_LISTS),
    )

    boot_text = read_text(BOOT_TEXT)
    ast.parse(boot_text, filename=str(BOOT_TEXT))
    assert_contains_all(
        boot_text,
        REQUIRED_BOOT_DELEGATION,
        str(BOOT_TEXT),
    )


def validate_touched_python_line_counts() -> None:
    """Validate touched Python files comply with the hard maximum."""
    for relative_path in TOUCHED_CODE_FILES:
        assert_python_module_under_500(relative_path)


if __name__ == "__main__":
    validate_startup_stack()
    validate_source_map()
    validate_generator_bridge_reports()
    validate_touched_python_line_counts()
    print("VALIDATION OK: startup-code-module-hard-max-500-bridge-v1")
