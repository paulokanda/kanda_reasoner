"""Validate Error Memory GUI Error Editor and Memorize Error contract v5."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"


def assert_contains(text: str, needle: str, message: str) -> None:
    if needle not in text:
        raise AssertionError(message)


def assert_not_contains(text: str, needle: str, message: str) -> None:
    if needle in text:
        raise AssertionError(message)


def main() -> None:
    text = TAB.read_text(encoding="utf-8")

    assert_contains(text, 'QGroupBox("Error Editor")', "Error Editor group title is missing.")
    assert_not_contains(text, 'QGroupBox("Last received lesson Preview")', "Old preview group title is still present.")
    assert_not_contains(text, "Loaded project context", "Loaded project context label must stay removed.")
    assert_not_contains(text, 'QPushButton("Save Draft from Raw Error")', "Save Draft from Raw Error must stay removed.")
    assert_not_contains(text, "operation_phase_combo", "Manual Operation phase chooser must stay removed.")
    assert_not_contains(text, "import_error_memory_file", "Import Error Lesson ZIP must not directly save through importer.")

    assert_contains(text, "def _save_active_ready_lesson", "Shared active-ready save helper is missing.")
    assert_contains(text, "def _text_is_formatted_error_lesson_payload", "Import must distinguish Error Memory lesson JSON from unrelated JSON.")
    assert_contains(text, "def _candidate_text_for_memorize", "Memorize candidate selection helper is missing.")
    assert_contains(text, "return editor_text, \"Error Editor\"", "Memorize Error must prefer edited Error Editor JSON.")
    assert_contains(text, "return raw_text, \"AI-assisted error lesson intake\"", "Memorize Error must fall back to intake text window.")
    assert_contains(text, "self._save_active_ready_lesson(lesson, \"Memorized active Error Memory lesson\")", "Memorize Error must use active-ready helper.")
    assert_contains(text, "self._save_active_ready_lesson(lesson, \"Updated lesson status to active\")", "Mark Active must use the same active-ready helper.")
    assert_contains(text, "same required fields, prevention triggers, and redaction metadata required by Memorize Error", "Mark Active must use the Memorize Error active-ready rule.")
    assert_not_contains(text, "missing_validation =", "Mark Active must not use a stricter separate validation gate than Memorize Error.")

    assert_contains(text, "self._text_is_formatted_error_lesson_payload(text)", "Import must accept only formatted Error Memory lesson payloads.")
    assert_contains(text, "Loaded formatted Error Memory lesson into the AI-assisted intake and Error Editor", "Import must load formatted lesson into intake/editor.")
    assert_contains(text, "Review or edit it, then click Memorize Error to save it into Lessons", "Import must instruct user to memorize after review.")
    assert_contains(text, "self.raw_error_edit.setPlainText(formatted_text)", "Import must populate AI-assisted intake text window.")
    assert_contains(text, "self.received_preview_edit.setPlainText(json.dumps(lesson", "Import/memorize must populate Error Editor.")

    print("VALIDATION OK: error-memory-gui-error-editor-memorize-active-v5")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
