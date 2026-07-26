"""Validate Error Memory GUI AI draft/ZIP workflow labels and contracts v6."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUI_PATH = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
INTAKE_PATH = ROOT / "kanda_reasoner_app" / "error_memory" / "intake.py"


def assert_contains(text: str, needle: str, message: str) -> None:
    if needle not in text:
        raise AssertionError(message + " Missing: " + needle)


def assert_not_contains(text: str, needle: str, message: str) -> None:
    if needle in text:
        raise AssertionError(message + " Unexpected: " + needle)


def main() -> None:
    gui_text = GUI_PATH.read_text(encoding="utf-8")
    intake_text = INTAKE_PATH.read_text(encoding="utf-8")

    ast.parse(gui_text)
    ast.parse(intake_text)

    assert_contains(gui_text, 'QPushButton("Copy error/draft to AI")', "Copy button label was not updated.")
    assert_contains(gui_text, 'QPushButton("Paste error formatted from AI")', "Paste button label was not updated.")
    assert_not_contains(gui_text, 'QPushButton("Copy Formulary Prompt to AI")', "Old copy button label remains.")
    assert_not_contains(gui_text, 'QPushButton("Receive Formulary from AI")', "Old receive button label remains.")

    assert_contains(gui_text, 'def _formatted_lesson_block', "Lesson selection must produce a formatted intake block.")
    assert_contains(gui_text, 'self.raw_error_edit.setPlainText(self._formatted_lesson_block(lesson))', "Clicking a lesson must populate AI-assisted intake.")
    assert_contains(gui_text, 'Current Error Editor JSON/draft', "Copy error/draft to AI must include Error Editor draft context.")
    assert_contains(gui_text, 'operation_phase=self._operation_phase_from_editor_or_unknown()', "Copy prompt must preserve operation_phase metadata from JSON when available.")

    receive_start = gui_text.index('def _receive_formulary_from_ai')
    receive_end = gui_text.index('def _text_has_formatted_lesson_payload', receive_start)
    receive_block = gui_text[receive_start:receive_end]
    assert_contains(receive_block, 'lesson = self._lesson_from_formatted_text(formatted_text)', "Paste formatted from AI must parse formatted text.")
    assert_contains(receive_block, 'self.raw_error_edit.setPlainText(formatted_text)', "Paste formatted from AI must populate AI-assisted intake.")
    assert_contains(receive_block, 'self.received_preview_edit.setPlainText(json.dumps(lesson', "Paste formatted from AI must populate Error Editor.")
    assert_not_contains(receive_block, 'save_ai_form_as_lesson', "Paste formatted from AI must not save directly.")
    assert_not_contains(receive_block, 'Saved AI lesson', "Paste formatted from AI must not report direct save.")

    import_start = gui_text.index('def _import_error_lesson_zip')
    import_end = gui_text.index('def _save_preview_lesson', import_start)
    import_block = gui_text[import_start:import_end]
    assert_contains(import_block, 'daily_work = drive_root / (root.name + "_delete_after_daily_work")', "Import should look from drive root or daily-work context.")
    assert_contains(import_block, 'Select AI-created formatted Error Lesson ZIP/JSON', "Import dialog title must reflect AI-created formatted lesson ZIP.")
    assert_contains(import_block, 'It was not saved yet', "Import must not imply direct memorization.")

    assert_contains(intake_text, 'Return the Copy error/draft to AI prompt', "Intake prompt docstring not updated.")
    assert_contains(intake_text, 'Paste error formatted from AI', "AI prompt must reference the new paste button.")
    assert_contains(intake_text, 'AI-created Error Lesson ZIP', "AI prompt must reference the formatted ZIP path.")
    assert_contains(intake_text, 'operation_phase is metadata', "AI prompt must preserve operation_phase as metadata.")
    assert_contains(intake_text, 'Current error/draft JSON for completion or correction', "AI prompt must identify draft JSON correctly.")

    print("VALIDATION OK: error-memory-gui-ai-draft-zip-workflow-v6")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
