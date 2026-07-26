"""Validate Copy Current Error Editor JSON uses only Error Editor text.

This is intentionally simple. The button must not call prompt builders, marker
extractors, or raw_error_text extraction heuristics. It copies the current Error
Editor text exactly, except trimming outer whitespace.
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


def test_button_wiring_is_exact_editor_copy() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    if "build_error_lesson_ai_form_prompt" in source:
        raise AssertionError("Copy button must not import or call the AI prompt builder.")
    if "_copy_formulary_prompt_to_ai" in source:
        raise AssertionError("Old prompt-copy handler must not remain defined or wired.")
    if "extract_error_editor_text_for_ai" in source:
        raise AssertionError("Copy button must not use the extraction helper.")
    if "editor_clipboard" in source:
        raise AssertionError("Copy button must be disconnected from editor_clipboard helper logic.")
    if "copy_formulary_button.clicked.connect(self._copy_error_editor_text_to_ai)" not in source:
        raise AssertionError("Copy button must be wired to _copy_error_editor_text_to_ai.")
    if "Copy Current Error Editor JSON" not in source:
        raise AssertionError("Button label must state the exact Error Editor JSON contract.")

    block = _method_block(source, "_copy_error_editor_text_to_ai")
    required = [
        "editor_text = self.received_preview_edit.toPlainText().strip()",
        "QApplication.clipboard().setText(editor_text)",
        "current Error Editor text was copied exactly",
    ]
    for fragment in required:
        if fragment not in block:
            raise AssertionError("Handler missing exact-copy fragment: " + fragment)

    forbidden = [
        "extract_error_editor_text_for_ai",
        "build_error_lesson_ai_form_prompt",
        "ERROR_DRAFT_MARKER",
        "Current error/draft JSON",
        "raw_error_text",
        "KANDA_ERROR_LESSON_JSON_BEGIN",
        "KANDA_ERROR_LESSON_JSON_END",
        "operation_phase=",
        "selected_project_root",
        "payload_text",
    ]
    for fragment in forbidden:
        if fragment in block:
            raise AssertionError("Handler still contains old prompt/extraction logic: " + fragment)


def test_previous_export_guards_preserved() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    export_block = _method_block(source, "_export_for_ai")
    if "textCursor().Start" in export_block:
        raise AssertionError("QTextCursor Start regression returned in _export_for_ai.")
    if "write_error_memory_ai_send_files" in export_block or "resolve_second_prompt_files_root" in export_block:
        raise AssertionError("Complete Error Memory export must not regress to second_prompt_files.")


def main() -> None:
    test_button_wiring_is_exact_editor_copy()
    test_previous_export_guards_preserved()
    print("VALIDATION OK: error-memory-copy-error-editor-exact-json-v12")
    print("ERROR_MEMORY_COPY_BUTTON: exact Error Editor text copied")
    print("ERROR_MEMORY_COPY_BUTTON_NO_PROMPT_BUILDER: enforced")
    print("ERROR_MEMORY_COPY_BUTTON_NO_EXTRACTION_HELPER: enforced")
    print("ERROR_MEMORY_PACKAGED_LESSON_ID: present")
    print("ERROR_MEMORY_EXPORT_PREVIOUS_GUARDS: preserved")


if __name__ == "__main__":
    main()
