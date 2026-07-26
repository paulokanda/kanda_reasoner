"""Validate the error copy-close floating window template patch."""

from __future__ import annotations

import py_compile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "error-copy-close-floating-window-template-v1"

FILES_TO_COMPILE = [
    "kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py",
    "kanda_reasoner_app/templates/floating_windows/__init__.py",
]

REQUIRED_FILES = [
    "kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py",
    "kanda_reasoner_app/templates/floating_windows/ERROR_COPY_CLOSE_WINDOW_BLUEPRINT.md",
    "kanda_reasoner_app/templates/floating_windows/__init__.py",
]


def read_text(relative_path: str) -> str:
    """Read a project file as UTF-8 text."""
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    """Raise if required text is missing."""
    if needle not in text:
        raise AssertionError(label + " missing: " + needle)


def assert_not_contains(text: str, needle: str, label: str) -> None:
    """Raise if forbidden text is present."""
    if needle in text:
        raise AssertionError(label + " contains forbidden text: " + needle)


def assert_ascii(relative_path: str) -> None:
    """Ensure a changed file contains only ASCII text."""
    data = (PROJECT_ROOT / relative_path).read_bytes()
    try:
        data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise AssertionError("non-ASCII character found in " + relative_path) from exc


def validate_files_exist() -> None:
    """Verify all expected files are present."""
    for relative_path in REQUIRED_FILES:
        path = PROJECT_ROOT / relative_path
        if not path.exists():
            raise AssertionError("missing expected file: " + relative_path)


def validate_compiles() -> None:
    """Compile changed Python files."""
    for relative_path in FILES_TO_COMPILE:
        py_compile.compile(str(PROJECT_ROOT / relative_path), doraise=True)


def validate_template_contract() -> None:
    """Verify the template implements copy-on-OK and silent close behavior."""
    source = read_text("kanda_reasoner_app/templates/floating_windows/error_copy_close_window.py")

    assert_contains(source, "class ErrorCopyCloseFloatingWindow", "template class")
    assert_contains(source, "def show_error_copy_close_window", "show helper")
    assert_contains(source, "def copy_error_text_to_clipboard", "copy method")
    assert_contains(source, "def copy_error_text_to_clipboard_and_close", "copy-close method")
    assert_contains(source, "app.clipboard()", "clipboard access")
    assert_contains(source, "clipboard.setText(self._clipboard_text)", "clipboard write")
    assert_contains(source, "ok_button.clicked.connect(self.copy_error_text_to_clipboard_and_close)", "OK wiring")
    assert_contains(source, "ok_button.setAutoDefault(False)", "no auto default")
    assert_contains(source, "ok_button.setDefault(False)", "no default button")
    assert_contains(source, "super().done(result)", "silent close path")
    assert_contains(source, "Title:\\n", "title copy section")
    assert_contains(source, "Message:\\n", "message copy section")
    assert_contains(source, "Traceback:\\n", "traceback copy section")
    assert_contains(source, "Context:\\n", "context copy section")
    assert_not_contains(source, "QMessageBox", "template source")
    assert_not_contains(source, "beep", "template source")


def validate_blueprint_contract() -> None:
    """Verify the blueprint records when and how to use the template."""
    blueprint = read_text("kanda_reasoner_app/templates/floating_windows/ERROR_COPY_CLOSE_WINDOW_BLUEPRINT.md")

    assert_contains(blueprint, "OK button", "blueprint")
    assert_contains(blueprint, "Copy the complete error text", "blueprint")
    assert_contains(blueprint, "Close the window silently", "blueprint")
    assert_contains(blueprint, "show_error_copy_close_window", "blueprint")
    assert_contains(blueprint, "Window-manager close and Escape close may close without copying", "blueprint")
    assert_contains(blueprint, "Do not use `QMessageBox.critical`", "blueprint sound policy")


def validate_init_exports() -> None:
    """Verify package exports expose the new helper."""
    init_text = read_text("kanda_reasoner_app/templates/floating_windows/__init__.py")
    assert_contains(init_text, "ErrorCopyCloseFloatingWindow", "__init__ export")
    assert_contains(init_text, "show_error_copy_close_window", "__init__ export")
    assert_contains(init_text, "show_auto_close_action_window", "existing export preserved")
    assert_contains(init_text, "attach_floating_window", "existing export preserved")


def validate_ascii() -> None:
    """Validate ASCII-only changed files."""
    for relative_path in REQUIRED_FILES + ["validation/test_error_copy_close_floating_window_template_v1.py"]:
        assert_ascii(relative_path)


def main() -> int:
    """Run validation checks."""
    validate_files_exist()
    validate_compiles()
    validate_template_contract()
    validate_blueprint_contract()
    validate_init_exports()
    validate_ascii()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
