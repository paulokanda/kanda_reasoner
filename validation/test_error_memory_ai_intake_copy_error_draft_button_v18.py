"""Validate AI-assisted intake Copy error/draft button v18."""

from __future__ import annotations

from pathlib import Path
import py_compile
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _scope(text: str, start: str, end: str) -> str:
    _assert(start in text, "missing scope start: " + start)
    piece = text.split(start, 1)[1]
    _assert(end in piece, "missing scope end: " + end)
    return piece.split(end, 1)[0]


def main() -> int:
    gui_path = PROJECT_ROOT / "kanda_reasoner_app/error_memory_gui/error_memory_tab.py"
    normalizer_path = PROJECT_ROOT / "kanda_reasoner_app/error_memory/heuristic_normalizer.py"
    merge_path = PROJECT_ROOT / "scripts/merge_freeze_validation_evidence.py"
    py_compile.compile(str(gui_path), doraise=True)
    py_compile.compile(str(normalizer_path), doraise=True)
    py_compile.compile(str(merge_path), doraise=True)

    gui_text = gui_path.read_text(encoding="utf-8")

    required = [
        'self.copy_ai_assisted_intake_error_draft_button = QPushButton("Copy error/draft")',
        'intake_buttons_1.addWidget(self.copy_ai_assisted_intake_error_draft_button)',
        'self.copy_ai_assisted_intake_error_draft_button.setToolTip("Copy exactly the current AI-assisted error lesson intake text.',
        'self.copy_ai_assisted_intake_error_draft_button.clicked.connect(self._copy_ai_assisted_intake_error_draft_to_clipboard)',
        'def _copy_ai_assisted_intake_error_draft_to_clipboard(self) -> None:',
        'intake_text = self.raw_error_edit.toPlainText().strip()',
        'QApplication.clipboard().setText(intake_text)',
        'The current AI-assisted error lesson intake text was copied exactly.',
    ]
    for fragment in required:
        _assert(fragment in gui_text, "missing intake copy fragment: " + fragment)

    handler_scope = _scope(gui_text, "def _copy_ai_assisted_intake_error_draft_to_clipboard", "def _copy_error_draft_to_clipboard")
    forbidden = [
        "self.received_preview_edit.toPlainText()",
        "json.loads",
        "parse_error_lesson_ai_response",
        "build_lesson_from_ai_form",
        "build_error_lesson_ai_form_prompt",
        "self._lesson_from_formatted_text",
        "save_lesson(",
        "self._formatted_lesson_block",
        "self._lesson_json_text_for_windows",
    ]
    for fragment in forbidden:
        _assert(fragment not in handler_scope, "intake copy button crossed box boundary: " + fragment)

    editor_handler_scope = _scope(gui_text, "def _copy_error_draft_to_clipboard", "def _clean_intake_window")
    _assert("error_draft_text = self.received_preview_edit.toPlainText().strip()" in editor_handler_scope, "existing Error Editor copy button must remain editor-only")
    _assert("self.raw_error_edit.toPlainText()" not in editor_handler_scope, "existing Error Editor copy button must not switch to intake source")

    previous_guards = [
        'self.copy_error_draft_button = QPushButton("Copy error/draft")',
        'self.heuristic_correction_button = QPushButton("Need AI to Correct")',
        'self._load_pending_ai_assisted_error_lesson_intake(mirror_loaded_json_to_error_editor=True)',
        'self._consume_loaded_pending_intake_file_if_matches(lesson)',
    ]
    for fragment in previous_guards:
        _assert(fragment in gui_text, "previous guard missing: " + fragment)

    print("VALIDATION OK: error-memory-ai-intake-copy-error-draft-button-v18")
    print("ERROR_MEMORY_AI_INTAKE_COPY_BUTTON: Copy error/draft added to intake group")
    print("ERROR_MEMORY_AI_INTAKE_COPY_BUTTON: intake window text copied exactly")
    print("ERROR_MEMORY_AI_INTAKE_COPY_BUTTON_NO_EDITOR_SOURCE: enforced")
    print("ERROR_MEMORY_AI_INTAKE_COPY_BUTTON_NO_PARSER_OR_PROMPT: enforced")
    print("ERROR_MEMORY_PREVIOUS_GUARDS: editor copy, heuristic, pending sync preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
