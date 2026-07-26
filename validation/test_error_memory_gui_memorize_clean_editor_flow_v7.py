"""Validate Error Memory GUI memorize/clean/editor workflow v7 source contract."""

from __future__ import annotations

from pathlib import Path


def _read_source() -> str:
    root = Path(__file__).resolve().parents[1]
    path = root / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"
    if not path.exists():
        raise AssertionError(f"Missing source file: {path}")
    return path.read_text(encoding="utf-8")


def _section(source: str, start: str, end: str) -> str:
    start_index = source.index(start)
    end_index = source.index(end, start_index)
    return source[start_index:end_index]


def main() -> None:
    source = _read_source()

    required = [
        "self.clean_intake_button = QPushButton(\"Clean\")",
        "self.clean_editor_button = QPushButton(\"Clean\")",
        "self.clean_intake_button.clicked.connect(self._clean_intake_window)",
        "self.clean_editor_button.clicked.connect(self._clean_error_editor)",
        "def _clean_intake_window(self) -> None:",
        "def _clean_error_editor(self) -> None:",
        "self.raw_error_edit.clear()",
        "self.received_preview_edit.clear()",
        "Copy error/draft to AI uses only the Error Editor window",
        "Only the current Error Editor content was copied to the clipboard",
        "Destination path copied to clipboard.",
        "Check whether the current error/draft already exists in the Error Memory lesson library",
    ]
    for needle in required:
        if needle not in source:
            raise AssertionError(f"Missing required v7 source contract: {needle}")

    intake_section = _section(source, "# LEFT COLUMN", "# RIGHT COLUMN")
    editor_section = _section(source, "# RIGHT COLUMN", "list_box = QGroupBox(\"Lessons\")")

    if "self.copy_formulary_button = QPushButton(\"Copy error/draft to AI\")" in intake_section:
        raise AssertionError("Copy error/draft to AI must not be placed in AI-assisted intake buttons.")
    if "self.copy_formulary_button = QPushButton(\"Copy error/draft to AI\")" not in editor_section:
        raise AssertionError("Copy error/draft to AI must be placed in Error Editor buttons.")

    copy_method = _section(source, "def _copy_formulary_prompt_to_ai", "def _clean_intake_window")
    if "self.raw_error_edit.toPlainText()" in copy_method:
        raise AssertionError("Copy error/draft to AI must not copy raw intake content; it must use Error Editor only.")
    if "editor_draft = self.received_preview_edit.toPlainText().strip()" not in copy_method:
        raise AssertionError("Copy error/draft to AI must copy Error Editor content.")

    memorize_method = _section(source, "def _memorize_error_from_text_window", "def _formatted_import_text_for_window")
    if "path = self._save_active_ready_lesson" not in memorize_method:
        raise AssertionError("Memorize Error must capture the active save result.")
    if "if path is not None:" not in memorize_method or "self.raw_error_edit.clear()" not in memorize_method:
        raise AssertionError("Memorize Error must clear AI-assisted intake after successful active save.")

    load_method = _section(source, "def _load_selected_lesson_into_preview", "def _copy_formulary_prompt_to_ai")
    if load_method.count(".clear()") < 2:
        raise AssertionError("Loading a lesson must clear both windows before inserting selected lesson content.")
    if "self.raw_error_edit.setPlainText(self._formatted_lesson_block(lesson))" not in load_method:
        raise AssertionError("Selected lesson must populate AI-assisted intake.")
    if "self.received_preview_edit.setPlainText(json.dumps(lesson" not in load_method:
        raise AssertionError("Selected lesson must populate Error Editor.")

    check_method = _section(source, "def _check_against_lessons", "def _show_repeat_guard_report")
    first_editor = check_method.find("self.received_preview_edit.toPlainText().strip()")
    first_raw = check_method.find("self.raw_error_edit.toPlainText().strip()")
    if first_editor < 0 or first_raw < 0 or first_editor > first_raw:
        raise AssertionError("Check Against Lessons must prefer Error Editor content, then intake content.")

    if "VALIDATION OK: error-memory-gui-memorize-clean-editor-flow-v7" in source:
        raise AssertionError("Validation marker must not be embedded in production GUI source.")

    print("VALIDATION OK: error-memory-gui-memorize-clean-editor-flow-v7")
    print("STATUS: IN_SYNC")


if __name__ == "__main__":
    main()
