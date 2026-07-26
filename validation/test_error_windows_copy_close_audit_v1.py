"""Validate critical error dialogs use the copy-and-close error template."""

from __future__ import annotations

import py_compile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "error-windows-copy-close-audit-v1"

TEMPLATE_FILES = [
    "kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py",
    "kanda_reasoner_app/templates/floating_windows/ERROR_COPY_CLOSE_WINDOW_BLUEPRINT.md",
    "kanda_reasoner_app/templates/floating_windows/__init__.py",
]

AUDITED_FILES = [
    "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/run_controls.py",
    "kanda_reasoner_app/json_splitter/__init__.py",
    "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py",
    "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/analysis_controller.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/runtime_runner_part_3_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab_help/prefs_io.py",
    "kanda_reasoner_app/reasoner_tools_gui_shell/main_window_help/window_tool_patches.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/window_process_private_impl.py",
    "kanda_reasoner_app/reasoner_tools_shell/runner_help/zip_json_files_private_impl.py",
]

EXPECTED_MINIMUM_REPLACEMENTS = 43


def read_text(relative_path: str) -> str:
    """Return a project file as UTF-8 text."""
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def assert_exists(relative_path: str) -> None:
    """Assert a project file exists."""
    path = PROJECT_ROOT / relative_path
    if not path.is_file():
        raise AssertionError("Missing file: " + relative_path)


def assert_contains(text: str, needle: str, label: str) -> None:
    """Assert text contains a required fragment."""
    if needle not in text:
        raise AssertionError(label + " is missing: " + needle)


def assert_not_contains(text: str, needle: str, label: str) -> None:
    """Assert text does not contain a forbidden fragment."""
    if needle in text:
        raise AssertionError(label + " still contains forbidden fragment: " + needle)


def assert_ascii(relative_path: str) -> None:
    """Assert a modified Python file contains printable ASCII text only."""
    text = read_text(relative_path)
    for line_number, line in enumerate(text.splitlines(), start=1):
        for char in line:
            if ord(char) > 127:
                raise AssertionError(
                    "Non-ASCII character in "
                    + relative_path
                    + " line "
                    + str(line_number)
                )


def main() -> int:
    """Run static validation checks for the patch."""
    for relative_path in TEMPLATE_FILES + AUDITED_FILES:
        assert_exists(relative_path)

    for relative_path in AUDITED_FILES + [TEMPLATE_FILES[0]]:
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)
        assert_ascii(relative_path)

    template_text = read_text("kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py")
    assert_contains(template_text, "copy_error_text_to_clipboard", "error template copy method")
    assert_contains(template_text, "copy_error_text_to_clipboard_and_close", "error template OK path")
    assert_contains(template_text, "clipboard.setText", "clipboard write")
    assert_contains(template_text, "close_silently", "silent close")
    assert_not_contains(template_text, "QMessageBox", "error template native message box policy")
    assert_not_contains(template_text, "beep", "error template sound policy")

    init_text = read_text("kanda_reasoner_app/templates/floating_windows/__init__.py")
    assert_contains(init_text, "show_error_copy_close_window", "template package export")
    assert_contains(init_text, "ErrorCopyCloseFloatingWindow", "template class export")

    total_replacements = 0
    for relative_path in AUDITED_FILES:
        text = read_text(relative_path)
        assert_not_contains(text, "QMessageBox.critical", relative_path)
        assert_contains(
            text,
            "show_error_copy_close_window",
            "copy-close import/use in " + relative_path,
        )
        total_replacements += text.count("show_error_copy_close_window(")

    if total_replacements < EXPECTED_MINIMUM_REPLACEMENTS:
        raise AssertionError(
            "Too few error-window replacements: "
            + str(total_replacements)
            + " < "
            + str(EXPECTED_MINIMUM_REPLACEMENTS)
        )

    blueprint_text = read_text("kanda_reasoner_app/templates/floating_windows/ERROR_COPY_CLOSE_WINDOW_BLUEPRINT.md")
    assert_contains(blueprint_text, "OK", "blueprint OK button contract")
    assert_contains(blueprint_text, "clipboard", "blueprint clipboard contract")
    assert_contains(blueprint_text, "QMessageBox.critical", "blueprint migration policy")

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
