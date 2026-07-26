"""Validate Error Memory table-view lesson selection import repair behavior."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

FEATURE_ID = "error-memory-table-view-lesson-selection-import-repair-v1"
ROOT = Path(__file__).resolve().parents[1]
TABLE_VIEW = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "_table_view.py"
TABLE_DRAFT_MIXIN = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "_table_draft_mixin.py"
ERROR_MEMORY_TAB = ROOT / "kanda_reasoner_app" / "error_memory_gui" / "error_memory_tab.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _function_names(path: Path) -> set[str]:
    tree = ast.parse(_read(path), filename=str(path))
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}


def main() -> int:
    for path in (TABLE_VIEW, TABLE_DRAFT_MIXIN, ERROR_MEMORY_TAB):
        _assert(path.exists(), f"missing expected Error Memory GUI file: {path}")

    table_view_text = _read(TABLE_VIEW)
    mixin_text = _read(TABLE_DRAFT_MIXIN)
    tab_text = _read(ERROR_MEMORY_TAB)

    _assert(
        "lesson_from_current_windows_or_selection" in _function_names(TABLE_VIEW),
        "_table_view must define lesson_from_current_windows_or_selection",
    )
    _assert(
        '"lesson_from_current_windows_or_selection"' in table_view_text
        or "'lesson_from_current_windows_or_selection'" in table_view_text,
        "_table_view __all__ must expose lesson_from_current_windows_or_selection",
    )
    _assert(
        "lesson_from_current_windows_or_selection," in mixin_text,
        "_table_draft_mixin must still be able to import lesson_from_current_windows_or_selection from _table_view",
    )
    _assert(
        "for text in (tab.received_preview_edit.toPlainText(), tab.raw_error_edit.toPlainText())" in table_view_text,
        "helper must preserve Error Editor / AI-assisted intake window priority",
    )
    _assert(
        "tab._lesson_from_formatted_text(stripped)" in table_view_text,
        "helper must parse visible formatted lesson text using tab compatibility method",
    )
    _assert(
        "return tab._lesson_from_preview_or_selection()" in table_view_text,
        "helper must fall back to preview/table selection",
    )
    _assert(
        "from kanda_reasoner_app.error_memory_gui._table_draft_mixin import ErrorMemoryTableDraftMixin" in tab_text,
        "ErrorMemoryTab must continue loading the frozen table/draft mixin",
    )
    _assert(
        "PySide6" not in table_view_text.split("def lesson_from_current_windows_or_selection", 1)[1].split("def load_selected_lesson_into_preview", 1)[0],
        "new helper must stay headless-safe and not add Qt imports",
    )

    # Compile and import only _table_view; _table_draft_mixin imports PySide6 in real app runtime,
    # so this validator checks the broken import surface statically and keeps CI headless-friendly.
    sys.path.insert(0, str(ROOT))
    import kanda_reasoner_app.error_memory_gui._table_view as table_view  # noqa: WPS433

    _assert(
        hasattr(table_view, "lesson_from_current_windows_or_selection"),
        "runtime _table_view module does not expose repair helper",
    )

    print(f"VALIDATION OK: {FEATURE_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
