"""Validate Error Memory post-Memorize next-pending syncs Error Editor v17."""

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
        "def _load_pending_ai_assisted_error_lesson_intake(self, *, mirror_loaded_json_to_error_editor: bool = False) -> bool:",
        "def _set_ai_assisted_intake_and_error_editor_to_same_lesson_json(self, lesson: dict[str, Any]) -> None:",
        "lesson_json = self._lesson_json_text_for_windows(lesson)",
        "self.raw_error_edit.setPlainText(lesson_json)",
        "self.received_preview_edit.setPlainText(lesson_json)",
        "self._load_pending_ai_assisted_error_lesson_intake(mirror_loaded_json_to_error_editor=True)",
        "When Memorize Error advances to the next pending lesson",
        "both windows must be updated from the same parsed lesson",
    ]
    for fragment in required:
        _assert(fragment in gui_text, "missing sync fragment: " + fragment)

    load_scope = _scope(gui_text, "def _load_pending_ai_assisted_error_lesson_intake", "def _reload_table")
    _assert("if mirror_loaded_json_to_error_editor:" in load_scope, "loader must branch on post-Memorize mirror flag")
    _assert("self._set_ai_assisted_intake_and_error_editor_to_same_lesson_json(lesson)" in load_scope, "loader must mirror same parsed lesson JSON when requested")
    _assert("self.raw_error_edit.setPlainText(formatted_text)" in load_scope, "normal tab-refresh loader behavior must remain available")

    clear_scope = _scope(gui_text, "def _clear_ai_assisted_intake_after_memorize", "def _memorize_error_from_text_window")
    _assert("self.raw_error_edit.clear()" in clear_scope, "Memorize Error must still clear current intake first")
    _assert("self.received_preview_edit.clear()" in clear_scope, "Memorize Error must still clear current Error Editor first")
    _assert("mirror_loaded_json_to_error_editor=True" in clear_scope, "post-Memorize advance must force editor sync")

    helper_scope = _scope(gui_text, "def _set_ai_assisted_intake_and_error_editor_to_same_lesson_json", "def _operation_phase_from_editor_or_unknown")
    forbidden = [
        "save_lesson(",
        "build_error_lesson_ai_form_prompt",
        "parse_error_lesson_ai_response",
        "build_lesson_from_ai_form",
        "unlink()",
    ]
    for fragment in forbidden:
        _assert(fragment not in helper_scope, "sync helper must not cross box boundary: " + fragment)

    previous_guards = [
        'self.copy_error_draft_button = QPushButton("Copy error/draft")',
        'self.heuristic_correction_button = QPushButton("Need AI to Correct")',
        'self.heuristic_correction_button.setText("Heuristic Correction")',
        'self.heuristic_correction_button.setEnabled(False)',
        'self._consume_loaded_pending_intake_file_if_matches(lesson)',
    ]
    for fragment in previous_guards:
        _assert(fragment in gui_text, "previous guard missing: " + fragment)

    print("VALIDATION OK: error-memory-memorize-next-syncs-editor-v17")
    print("ERROR_MEMORY_MEMORIZE_NEXT_SYNC: AI-assisted intake JSON mirrored to Error Editor")
    print("ERROR_MEMORY_MEMORIZE_NEXT_SYNC: post-Memorize loader uses same parsed lesson")
    print("ERROR_MEMORY_MEMORIZE_NEXT_SYNC: current windows clear before next load preserved")
    print("ERROR_MEMORY_BOX_LOGIC: window synchronization only")
    print("ERROR_MEMORY_PREVIOUS_GUARDS: copy button, heuristic button, pending consume preserved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
