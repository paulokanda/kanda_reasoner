"""Validate preimplementation actions in the large-file refactor planner."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

__all__ = [
    "main",
]

FEATURE_ID = "large-file-refactor-planner-preimplementation-actions-v1"
PLANNER_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner"
)
EXPECTED_BUTTONS = (
    "Analyze File",
    "Generate Split Plan",
    "Generate Docstring Plan",
    "Ask Local LLM for Ambiguous Symbols",
    "Show Planning Summary",
    "Copy Planning Summary",
)
FORBIDDEN_UI = (
    "Generate Preview",
    "Validate Preview",
    "Create Patch ZIP",
    "Prepare Apply Gate",
    "Open Preview Folder",
    "Show E2E Workflow",
    "Copy E2E Gate Summary",
)
FORBIDDEN_HANDLERS = (
    "_generate_preview_skeleton",
    "_validate_preview_skeleton",
    "_create_patch_zip_gate",
    "_prepare_payload_apply_gate",
    "attach_large_file_refactor_workflow_polish",
)


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION ERROR: {message}")


def read_text(path: Path) -> str:
    if not path.is_file():
        fail(f"required file missing: {path}")
    return path.read_text(encoding="utf-8")


def parse_python(path: Path) -> str:
    text = read_text(path)
    try:
        ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        fail(f"Python parse failed for {path}: {exc}")
    return text


def validate_gui_shell(text: str) -> None:
    for label in EXPECTED_BUTTONS:
        if f'QPushButton("{label}")' not in text:
            fail(f"expected Planner button missing: {label}")
    for label in FORBIDDEN_UI:
        if label in text:
            fail(f"legacy/downstream Planner UI still present: {label}")
    for token in FORBIDDEN_HANDLERS:
        if token in text:
            fail(f"legacy/downstream Planner handler still present: {token}")
    required = (
        'QGroupBox("5. Planning actions and review")',
        "Workbench handoff:",
        "build_planning_summary",
        "build_planner_inner_tabs",
        "apply_settings_panel_presentation",
        "build_planner_action_enablement",
    )
    for token in required:
        if token not in text:
            fail(f"required Planner pre-implementation contract missing: {token}")


def validate_summary_helper(text: str) -> None:
    required = (
        "PRE-IMPLEMENTATION SUMMARY",
        "Planner boundary:",
        "This tab is pre-implementation only.",
        "ready for Workbench intake checks",
    )
    for token in required:
        if token not in text:
            fail(f"planning summary contract missing: {token}")
    forbidden = (
        "_large_file_refactor_workbench_",
        "write_text(",
        "write_bytes(",
        "open(",
        "Path(",
    )
    for token in forbidden:
        if token in text:
            fail(f"planning summary helper violates box-local read-only contract: {token}")


def validate_module_sizes(paths: list[Path]) -> None:
    for path in paths:
        count = len(read_text(path).splitlines())
        if count > 500:
            fail(f"module exceeds 500 physical lines: {path} -> {count}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    planner_root = project_root / PLANNER_REL
    gui_path = planner_root / "gui_shell.py"
    summary_path = planner_root / "planner_preimplementation_summary.py"
    inner_tabs_path = planner_root / "planner_inner_tabs_layout.py"
    settings_path = planner_root / "planner_settings_panel_presentation.py"

    gui_text = parse_python(gui_path)
    summary_text = parse_python(summary_path)
    parse_python(inner_tabs_path)
    parse_python(settings_path)

    validate_gui_shell(gui_text)
    validate_summary_helper(summary_text)
    validate_module_sizes(
        [gui_path, summary_path, inner_tabs_path, settings_path]
    )

    print("PLAN_ACTIONS_ROLE: PRE_IMPLEMENTATION_ONLY")
    print("LEGACY_PLANNER_PREVIEW_BUTTONS: REMOVED")
    print("WORKBENCH_OWNED_ACTIONS: REMOVED_FROM_PLANNER_GUI")
    print("PLANNING_ACTIONS: PRESERVED")
    print("PLANNING_SUMMARY: READ_ONLY_BOX_LOCAL")
    print("CHILD_TAB_LAYOUT: PRESERVED")
    print("SETTINGS_PRESENTATION: PRESERVED")
    print("BOX_SHIELD: PASS")
    print("NO_LEAK_LOGIC: PASS")
    print("MODULE_SIZE_GATE: PASS")
    print(f"VALIDATION OK: {FEATURE_ID}")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
