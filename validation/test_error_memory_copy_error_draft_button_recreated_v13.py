"""Validate the recreated Copy error/draft button copies Error Editor text only.

Box Logic: this test only covers the Error Memory GUI clipboard button wiring
box. It intentionally rejects the old Copy error/draft to AI button path,
prompt builders, parser/extractor helpers, and any smart payload extraction.
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


def test_old_button_path_removed_and_new_button_created() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    forbidden_global = [
        "copy_formulary_button",
        "_copy_formulary_prompt_to_ai",
        "_copy_error_editor_text_to_ai",
        "build_error_lesson_ai_form_prompt",
        "extract_error_editor_text_for_ai",
        "editor_clipboard",
        "Copy error/draft to AI",
        "Copy Current Error Editor JSON",
    ]
    for fragment in forbidden_global:
        if fragment in source:
            raise AssertionError("Old Copy error/draft to AI path remains: " + fragment)

    required_global = [
        'self.copy_error_draft_button = QPushButton("Copy error/draft")',
        'preview_buttons.addWidget(self.copy_error_draft_button)',
        'self.copy_error_draft_button.clicked.connect(self._copy_error_draft_to_clipboard)',
    ]
    for fragment in required_global:
        if fragment not in source:
            raise AssertionError("New Copy error/draft button contract missing: " + fragment)


def test_new_handler_copies_error_editor_exactly() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    block = _method_block(source, "_copy_error_draft_to_clipboard")
    required = [
        "error_draft_text = self.received_preview_edit.toPlainText().strip()",
        "QApplication.clipboard().setText(error_draft_text)",
        "The Error Editor window is the single source of truth",
    ]
    for fragment in required:
        if fragment not in block:
            raise AssertionError("Handler missing direct Error Editor copy fragment: " + fragment)

    forbidden = [
        "build_error_lesson_ai_form_prompt",
        "extract_error_editor_text_for_ai",
        "ERROR_DRAFT_MARKER",
        "Current error/draft JSON",
        "raw_error_text",
        "ERROR_LESSON_JSON_BEGIN",
        "ERROR_LESSON_JSON_END",
        "operation_phase=",
        "selected_project_root",
        "payload_text",
        "json.loads",
        "parse_",
    ]
    for fragment in forbidden:
        if fragment in block:
            raise AssertionError("Handler still contains prompt/parser/extraction logic: " + fragment)


def test_previous_export_guards_preserved() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    export_block = _method_block(source, "_export_for_ai")
    if "textCursor().Start" in export_block:
        raise AssertionError("QTextCursor Start regression returned in _export_for_ai.")
    if "write_error_memory_ai_send_files" in export_block or "resolve_second_prompt_files_root" in export_block:
        raise AssertionError("Complete Error Memory export must not regress to second_prompt_files.")


def main() -> None:
    test_old_button_path_removed_and_new_button_created()
    test_new_handler_copies_error_editor_exactly()
    test_previous_export_guards_preserved()
    print("VALIDATION OK: error-memory-copy-error-draft-button-recreated-v13")
    print("ERROR_MEMORY_COPY_BUTTON: old to-AI button removed")
    print("ERROR_MEMORY_COPY_BUTTON: new Copy error/draft button created")
    print("ERROR_MEMORY_COPY_BUTTON: exact Error Editor text copied")
    print("ERROR_MEMORY_COPY_BUTTON_NO_PROMPT_BUILDER: enforced")
    print("ERROR_MEMORY_COPY_BUTTON_NO_EXTRACTION_HELPER: enforced")
    print("ERROR_MEMORY_EXPORT_PREVIOUS_GUARDS: preserved")


if __name__ == "__main__":
    main()
