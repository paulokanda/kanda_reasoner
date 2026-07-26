"""Validate the auto-close action floating window template patch."""

from __future__ import annotations

import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_ID = "auto-close-action-floating-window-template-v1"

TEMPLATE_FILE = PROJECT_ROOT / "kanda_reasoner_app" / "templates" / "floating_windows" / "auto_close_action_window.py"
BLUEPRINT_FILE = PROJECT_ROOT / "kanda_reasoner_app" / "templates" / "floating_windows" / "AUTO_CLOSE_ACTION_WINDOW_BLUEPRINT.md"
INIT_FILE = PROJECT_ROOT / "kanda_reasoner_app" / "templates" / "floating_windows" / "__init__.py"

REQUIRED_TEMPLATE_STRINGS = [
    "class AutoCloseActionFloatingWindow",
    "def show_auto_close_action_window",
    "timeout_ms: int = 3000",
    "_run_close_command_once",
    "self._close_command_ran",
    "self._timer.timeout.connect(self.accept)",
    "on_close: CloseCommand | None = None",
    "This is not a confirmation gate",
]

REQUIRED_BLUEPRINT_STRINGS = [
    "Default timeout is 3000 ms.",
    "The linked close command runs exactly once.",
    "Do not use this pattern as a human confirmation gate.",
    "Local freeze written",
    "New Local Freeze Entry",
    "on_close=dialog.close",
    "kanda_reasoner_app/templates/floating_windows/auto_close_action_window.py",
]

REQUIRED_INIT_STRINGS = [
    "AutoCloseActionFloatingWindow",
    "show_auto_close_action_window",
    "HoverFloatingWindowController",
    "attach_floating_window",
]


def read_text(path: Path) -> str:
    """Read a UTF-8 text file."""
    return path.read_text(encoding="utf-8")


def assert_ascii(path: Path) -> None:
    """Ensure a file contains ASCII-only text."""
    text = read_text(path)
    try:
        text.encode("ascii")
    except UnicodeEncodeError as exc:
        raise AssertionError(f"non-ASCII character found in {path}") from exc


def assert_python_compiles(path: Path) -> None:
    """Ensure a Python file parses and compiles."""
    source = read_text(path)
    ast.parse(source, filename=str(path))
    compile(source, str(path), "exec")


def assert_contains(path: Path, required_strings: list[str]) -> None:
    """Ensure all required strings exist in a file."""
    text = read_text(path)
    for needle in required_strings:
        if needle not in text:
            raise AssertionError(f"missing required text in {path}: {needle}")


def main() -> int:
    """Run the validation checks."""
    for path in (TEMPLATE_FILE, BLUEPRINT_FILE, INIT_FILE):
        if not path.exists():
            raise AssertionError(f"missing expected file: {path}")
        assert_ascii(path)

    assert_python_compiles(TEMPLATE_FILE)
    assert_python_compiles(INIT_FILE)
    assert_contains(TEMPLATE_FILE, REQUIRED_TEMPLATE_STRINGS)
    assert_contains(BLUEPRINT_FILE, REQUIRED_BLUEPRINT_STRINGS)
    assert_contains(INIT_FILE, REQUIRED_INIT_STRINGS)

    template_text = read_text(TEMPLATE_FILE)
    if "QMessageBox" in template_text:
        raise AssertionError("template must not depend on QMessageBox confirmation gates")
    if "exec()" in template_text or "exec_(" in template_text:
        raise AssertionError("auto-close action window must be non-modal and must not call exec")

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
