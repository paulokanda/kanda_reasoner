"""Validate auto-close replacement for post-action done windows."""

from __future__ import annotations

import py_compile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODIFIED_FILES = [
    "kanda_reasoner_app/templates/floating_windows/auto_close_action_window.py",
    "kanda_reasoner_app/templates/floating_windows/AUTO_CLOSE_ACTION_WINDOW_BLUEPRINT.md",
    "kanda_reasoner_app/templates/floating_windows/__init__.py",
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/run_controls.py",
    "kanda_reasoner_app/json_splitter/__init__.py",
    "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py",
    "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/runtime_runner_part_3_private_impl.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/report_io_runtime.py",
    "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
]

PY_FILES = [path for path in MODIFIED_FILES if path.endswith(".py")]

TARGET_SUCCESS_FRAGMENTS = [
    'QMessageBox.information(self, "Work done"',
    'QMessageBox.information(self, "Done"',
    'QMessageBox.information(self, "Finished"',
    'QMessageBox.information(self, "Trace saved"',
    'QMessageBox.information(window, "Loaded", "JSON loaded successfully.")',
    'QMessageBox.information(self, "Local freeze written"',
    'QMessageBox.information(self, "Get Last Freeze"',
    'QMessageBox.information(self, "Get All Frozen"',
    'QMessageBox.information(self, "Error Memory", "Saved lesson:',
    'QMessageBox.information(self, "Error Memory", "Deleted lesson',
    'QMessageBox.information(self, "Error Memory", "Updated lesson status',
    'QMessageBox.information(self, "Error Memory", "Superseded lesson',
    'QMessageBox.information(self, "Error Memory", "Restored deleted lesson',
    'QMessageBox.information(self, "Delete draft", "Draft deleted completely',
    'QMessageBox.information(self, "Error Memory complete JSON copied"',
    'QMessageBox.information(self, "Copied error/draft"',
    'QMessageBox.information(self, "Heuristic Correction"',
    'QMessageBox.information(receive_dialog, "Error Memory"',
]

ALLOWED_INFORMATION_FRAGMENTS = [
    'QMessageBox.information(self, "Delete draft", "No pending draft',
    'QMessageBox.information(self, "Error Memory", "Nothing to undo',
    'QMessageBox.information(self, "Repeat Error Guard", "Load an error',
    'QMessageBox.information(self, "No frozen entries"',
    'QMessageBox.information(self, "Help"',
    'QMessageBox.information(self, "Busy"',
    'QMessageBox.information(self, "Mode Help"',
    'QMessageBox.information(self, "Session History"',
    'QMessageBox.information(self, f"Mode Help',
    'QMessageBox.information(self, "No Evidence"',
    'QMessageBox.information(window, "Analysis running"',
    'QMessageBox.information(\n            window,\n            "Run Tab 2 Check first"',
    'QMessageBox.information(\n                self,\n                "Analysis running"',
]

REQUIRED_TEMPLATE_CALL_FILES = [
    "kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py",
    "kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/run_controls.py",
    "kanda_reasoner_app/json_splitter/__init__.py",
    "kanda_reasoner_app/manage_architecture/manage_architecture_gui.py",
    "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_window.py",
    "kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/runtime_runner_part_3_private_impl.py",
    "kanda_reasoner_app/reasoner_engine/ai_reasoner_main_window_help/runtime_controller.py",
    "kanda_reasoner_app/tab3_manual_review_runtime/report_io_runtime.py",
    "kanda_reasoner_app/error_memory_gui/error_memory_tab.py",
]


def read_text(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def assert_file_exists(relative_path: str) -> None:
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        raise AssertionError("missing file: " + relative_path)


def assert_compiles(relative_path: str) -> None:
    py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def assert_contains(relative_path: str, fragment: str) -> None:
    text = read_text(relative_path)
    if fragment not in text:
        raise AssertionError("missing fragment in " + relative_path + ": " + fragment)


def assert_not_contains_any(relative_path: str, fragments: list[str]) -> None:
    text = read_text(relative_path)
    found = [fragment for fragment in fragments if fragment in text]
    if found:
        raise AssertionError("forbidden success QMessageBox remains in " + relative_path + ": " + repr(found))


def validate_remaining_information_dialogs() -> None:
    unexpected: list[str] = []
    for path in (PROJECT_ROOT / "kanda_reasoner_app").rglob("*.py"):
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        if "QMessageBox.information" not in text:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if "QMessageBox.information" not in line:
                continue
            combined = "\n".join(text.splitlines()[max(0, line_number - 1): line_number + 4])
            if any(fragment in combined for fragment in ALLOWED_INFORMATION_FRAGMENTS):
                continue
            unexpected.append(relative + ":" + str(line_number) + ": " + line.strip())
    if unexpected:
        raise AssertionError("unexpected QMessageBox.information calls remain: " + repr(unexpected))


def main() -> int:
    for relative_path in MODIFIED_FILES:
        assert_file_exists(relative_path)
    for relative_path in PY_FILES:
        assert_compiles(relative_path)

    template_text = read_text("kanda_reasoner_app/templates/floating_windows/auto_close_action_window.py")
    if "close_silently" not in template_text:
        raise AssertionError("auto-close template must expose close_silently")
    forbidden_template_calls = [
        '_qt_widgets_attr("QMessageBox")',
        "QMessageBox.information",
        "QMessageBox.warning",
        "QMessageBox.critical",
        "QApplication.beep",
    ]
    found_forbidden = [item for item in forbidden_template_calls if item in template_text]
    if found_forbidden:
        raise AssertionError("auto-close template uses forbidden alert APIs: " + repr(found_forbidden))

    for relative_path in REQUIRED_TEMPLATE_CALL_FILES:
        assert_contains(relative_path, "show_auto_close_action_window")
        assert_not_contains_any(relative_path, TARGET_SUCCESS_FRAGMENTS)

    freeze_source = read_text("kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py")
    if "title=\"Local freeze written\"" not in freeze_source:
        raise AssertionError("Local freeze written success must use auto-close template")
    if "on_close=dialog.close" not in freeze_source:
        raise AssertionError("Local freeze written auto-close must close the parent entry dialog")

    validate_remaining_information_dialogs()

    print("VALIDATION OK: auto-close-done-windows-audit-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
