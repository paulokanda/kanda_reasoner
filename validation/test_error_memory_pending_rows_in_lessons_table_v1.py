"""Validate Error Memory pending rows in Lessons table v1."""
from __future__ import annotations
import ast
from pathlib import Path

FEATURE_ID = "error-memory-pending-rows-in-lessons-table-v1"
SOURCE = Path("kanda_reasoner_app/error_memory_gui/error_memory_tab.py")

REQUIRED_SNIPPETS = [
    "pending_review",
    "pending_duplicate",
    "pending_edit",
    "ERROR_MEMORY_ROW_KIND_ROLE",
    "ERROR_MEMORY_PENDING_PATH_ROLE",
    "_pending_lesson_rows_for_table",
    "_load_pending_intake_row_into_editor",
    "_draft_lesson_from_pending_raw_text",
    "_safe_pending_lesson_id_from_file",
    "Raw pending evidence waiting for edition",
    "Select this row to load it into AI-assisted intake and Error Editor",
    "Pending rows are virtual until the user saves them",
]

FORBIDDEN_SNIPPETS = [
    "self._dismissed_pending_intake_files.add(marker)\n                    self._dismissed_pending_intake_lesson_ids.add(lesson_id)\n                    self._show_duplicate_pending_intake_warning",
]


def main() -> int:
    if not SOURCE.exists():
        raise AssertionError("missing source file: " + str(SOURCE))
    text = SOURCE.read_text(encoding="utf-8")
    ast.parse(text)
    for snippet in REQUIRED_SNIPPETS:
        if snippet not in text:
            raise AssertionError("missing required pending-row contract snippet: " + snippet)
    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in text:
            raise AssertionError("duplicate pending intake is still hidden by dismissal before warning")
    if "self.lessons_table.setRowCount(total_rows)" not in text:
        raise AssertionError("Lessons table does not include pending rows in row count")
    if "pending_rows = self._pending_lesson_rows_for_table()" not in text:
        raise AssertionError("_reload_table does not collect pending rows")
    if "row_kind.startswith('pending')" not in text:
        raise AssertionError("selection loader does not route pending rows to editor")
    if "save_lesson(self._current_project_root(), draft)" not in text:
        raise AssertionError("existing draft save route not found")
    if "save_lesson(self._current_project_root(), lesson)" in text[text.index("def _load_pending_intake_row_into_editor"):text.index("def _load_pending_ai_assisted_error_lesson_intake")]:
        raise AssertionError("pending row loader must not auto-save lessons")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
