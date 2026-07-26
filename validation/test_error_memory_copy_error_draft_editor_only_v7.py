"""Validate Copy Error Editor text to AI copies no prompt wrapper.

The button previously built a full AI formulary prompt from the Error Editor text.
The required contract is stricter: copy exactly the Error Editor text and nothing
else. This validation is static and guards the GUI wiring and handler body.
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

    if "build_error_lesson_ai_form_prompt" in source:
        raise AssertionError("Copy error/draft to AI must not import or call the prompt builder.")
    if "_copy_formulary_prompt_to_ai" in source:
        raise AssertionError("Old prompt-copy handler name remains wired or defined.")
    if "copy_formulary_button.clicked.connect(self._copy_error_editor_text_to_ai)" not in source:
        raise AssertionError("Copy button must be wired to _copy_error_editor_text_to_ai.")
    if "Copy exactly the current Error Editor text" not in source:
        raise AssertionError("Tooltip must state exact Error Editor text copy contract.")
    if "No prompt wrapper" not in source:
        raise AssertionError("User-facing text must state that no prompt wrapper is added.")

    block = _method_block(source, "_copy_error_editor_text_to_ai")
    required_fragments = [
        "editor_text = self.received_preview_edit.toPlainText().strip()",
        "QApplication.clipboard().setText(editor_text)",
        "Only the current Error Editor text was copied to the clipboard. No prompt wrapper was added.",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in block]
    if missing:
        raise AssertionError("Raw Error Editor copy handler is missing required fragments: " + "; ".join(missing))

    forbidden_fragments = [
        "build_error_lesson_ai_form_prompt",
        "selected_project_root",
        "raw_error_text=editor",
        "operation_phase=",
        "ERROR_LESSON_JSON_BEGIN",
        "ERROR_LESSON_JSON_END",
        "Paste it into AI",
        "AI answer must start",
    ]
    for fragment in forbidden_fragments:
        if fragment in block:
            raise AssertionError("Raw Error Editor copy handler still contains prompt/formulary behavior: " + fragment)

    # Preserve previous export repairs while touching the same GUI file.
    export_block = _method_block(source, "_export_for_ai")
    if "textCursor().Start" in export_block:
        raise AssertionError("QTextCursor Start regression returned in _export_for_ai.")
    if "write_error_memory_ai_send_files" in export_block or "resolve_second_prompt_files_root" in export_block:
        raise AssertionError("Complete Error Memory export must not regress to second_prompt_files.")

    print("VALIDATION OK: error-memory-copy-error-draft-editor-only-v7")
    print("ERROR_MEMORY_COPY_DRAFT: editor text only")
    print("ERROR_MEMORY_COPY_DRAFT_NO_PROMPT_WRAPPER: enforced")
    print("ERROR_MEMORY_EXPORT_PREVIOUS_GUARDS: preserved")


if __name__ == "__main__":
    main()
