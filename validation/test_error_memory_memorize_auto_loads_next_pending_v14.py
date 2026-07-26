"""Validate Memorize Error immediately advances AI-assisted pending intake.

Box Logic: this test only covers the Error Memory GUI pending-intake loader
post-action refresh box. It must not touch clipboard copy behavior, freeze
logic, ZIP staging, or Error Memory storage schema.
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


def _index_of(block: str, fragment: str) -> int:
    index = block.find(fragment)
    if index == -1:
        raise AssertionError("Expected fragment missing: " + fragment)
    return index


def test_memorize_error_calls_post_save_refresh_hook() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    block = _method_block(source, "_memorize_error_from_text_window")
    if "if path is not None:" not in block:
        raise AssertionError("Memorize Error no longer checks successful save before post-save intake handling.")
    if "self._clear_ai_assisted_intake_after_memorize(lesson)" not in block:
        raise AssertionError("Memorize Error does not call the post-save intake refresh hook.")


def test_post_save_hook_consumes_clears_and_loads_next_pending() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    block = _method_block(source, "_clear_ai_assisted_intake_after_memorize")

    required = [
        "Box Logic: this method belongs only to the AI-assisted pending-intake",
        "self._consume_loaded_pending_intake_file_if_matches(lesson)",
        "self.raw_error_edit.clear()",
        "self.received_preview_edit.clear()",
        "self._last_received_lesson = None",
        "self._load_pending_ai_assisted_error_lesson_intake()",
    ]
    for fragment in required:
        if fragment not in block:
            raise AssertionError("Post-save intake refresh fragment missing: " + fragment)

    consume_index = _index_of(block, "self._consume_loaded_pending_intake_file_if_matches(lesson)")
    raw_clear_index = _index_of(block, "self.raw_error_edit.clear()")
    editor_clear_index = _index_of(block, "self.received_preview_edit.clear()")
    reload_index = _index_of(block, "self._load_pending_ai_assisted_error_lesson_intake()")

    if not (consume_index < raw_clear_index < editor_clear_index < reload_index):
        raise AssertionError("Post-save refresh must consume current file, clear windows, then load the next pending lesson.")


def test_post_save_hook_stays_inside_pending_intake_box() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    block = _method_block(source, "_clear_ai_assisted_intake_after_memorize")
    forbidden = [
        "QApplication.clipboard()",
        "build_error_lesson_ai_form_prompt",
        "merge_freeze_validation_evidence",
        "save_lesson(",
        "delete_lesson(",
        "deprecate",
        "supersed",
        "supersede",
        "archive",
    ]
    for fragment in forbidden:
        if fragment in block:
            raise AssertionError("Post-save intake refresh crossed into another box: " + fragment)


def test_copy_button_contract_from_v13_preserved() -> None:
    source = GUI_PATH.read_text(encoding="utf-8")
    if 'self.copy_error_draft_button = QPushButton("Copy error/draft")' not in source:
        raise AssertionError("The recreated Copy error/draft button regressed.")
    copy_block = _method_block(source, "_copy_error_draft_to_clipboard")
    if "error_draft_text = self.received_preview_edit.toPlainText().strip()" not in copy_block:
        raise AssertionError("Copy error/draft no longer copies the exact Error Editor text.")
    if "build_error_lesson_ai_form_prompt" in copy_block or "extract_error_editor_text_for_ai" in copy_block:
        raise AssertionError("Copy error/draft regressed to prompt/extraction logic.")


def main() -> None:
    test_memorize_error_calls_post_save_refresh_hook()
    test_post_save_hook_consumes_clears_and_loads_next_pending()
    test_post_save_hook_stays_inside_pending_intake_box()
    test_copy_button_contract_from_v13_preserved()
    print("VALIDATION OK: error-memory-memorize-auto-loads-next-pending-v14")
    print("ERROR_MEMORY_MEMORIZE: consumes current pending lesson after save")
    print("ERROR_MEMORY_MEMORIZE: clears current intake/editor after save")
    print("ERROR_MEMORY_MEMORIZE: auto-loads next pending lesson without tab switch")
    print("ERROR_MEMORY_BOX_LOGIC: pending-intake loader only")
    print("ERROR_MEMORY_COPY_BUTTON_PREVIOUS_GUARDS: preserved")


if __name__ == "__main__":
    main()
