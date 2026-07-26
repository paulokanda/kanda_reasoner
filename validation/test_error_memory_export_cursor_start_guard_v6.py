"""Validate the Error Memory export cursor-start crash repair.

The v5 GUI handler set the Error Editor text correctly but then crashed with:
AttributeError: 'PySide6.QtGui.QTextCursor' object has no attribute 'Start'.

This validation is static because PySide6 is not required for project-level CI.
It verifies the exact invalid enum access is gone and that the handler now uses
an instance cursor with MoveOperation.Start before assigning it back.
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GUI_PATH = PROJECT_ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"


def _method_block(source: str, name: str) -> str:
    marker = "    def " + name + "("
    start = source.index(marker)
    next_start = source.find("\n    def ", start + 1)
    if next_start == -1:
        return source[start:]
    return source[start:next_start]


def main() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    export_block = _method_block(source, "_export_for_ai")

    forbidden_fragments = [
        "textCursor().Start",
        "moveCursor(self.received_preview_edit.textCursor().Start)",
    ]
    for fragment in forbidden_fragments:
        if fragment in export_block:
            raise AssertionError("Invalid QTextCursor Start access remains in _export_for_ai: " + fragment)

    required_fragments = [
        "cursor = self.received_preview_edit.textCursor()",
        "cursor.movePosition(cursor.MoveOperation.Start)",
        "self.received_preview_edit.setTextCursor(cursor)",
        "self.received_preview_edit.setPlainText(clipboard_text)",
        "_copy_complete_error_memory_json_to_clipboard(clipboard_text)",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in export_block]
    if missing:
        raise AssertionError("Cursor-start repair is missing required fragments: " + ", ".join(missing))

    if "write_error_memory_ai_send_files" in export_block:
        raise AssertionError("Export button must not regress to the second-prompt export writer.")
    if "resolve_second_prompt_files_root" in export_block:
        raise AssertionError("Export button must not resolve second_prompt_files.")

    print("VALIDATION OK: error-memory-export-cursor-start-guard-v6")
    print("ERROR_MEMORY_EXPORT_CURSOR_START: QTextCursor MoveOperation.Start used")
    print("ERROR_MEMORY_EXPORT_NO_QTEXTCURSOR_START_ATTR: enforced")
    print("ERROR_MEMORY_EXPORT_NO_SECOND_PROMPT_PATH: enforced")


if __name__ == "__main__":
    main()
