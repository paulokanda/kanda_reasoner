"""Regression tests for Tab 3 manual review import boundaries."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
        manual_docstring_review_support as manual_support,
    )
except Exception:
    manual_support = None

try:
    from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help import (
        manual_docstring_review_editor as manual_editor,
    )
except Exception:
    manual_editor = None


ROOT = Path(__file__).resolve().parents[1]
HELP = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
)
SUPPORT = HELP / "manual_docstring_review_support.py"
EDITOR = HELP / "manual_docstring_review_editor.py"
REPORT = HELP / "report_review_panel.py"
MANIFEST = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help.json"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_support_has_no_reverse_import_to_review_panel() -> None:
    text = _read(SUPPORT)

    assert "from .report_review_panel import" not in text
    assert "_manual_review_status_for_row" in text
    assert "manual_review_is_inside_project_root" in text
    assert "manual_review_safe_int" in text


def test_editor_uses_non_colliding_support_names() -> None:
    text = _read(EDITOR)

    assert "manual_review_is_inside_project_root" in text
    assert "manual_review_safe_int" in text
    assert "def is_inside_project_root(" not in text
    assert "def safe_int(" not in text


def test_manifest_breaks_manual_review_cycle() -> None:
    data = json.loads(_read(MANIFEST))
    helper = data["helpers"]["manual_docstring_review_support.py"]

    assert "manual_docstring_review_support.py" in data["helpers"]
    assert "tab1_audit_docstring_source.py" in helper["depends_on"]
    assert "report_review_panel.py" not in helper["depends_on"]


def test_report_panel_lazily_opens_editor() -> None:
    text = _read(REPORT)

    assert "def open_docstring_review_window" in text
    assert "from .manual_docstring_review_editor import DocstringReviewEditorDialog" in text


def test_direct_support_import_when_dependencies_are_available() -> None:
    if manual_support is None:
        return
    assert hasattr(manual_support, "manual_review_safe_int")
    assert manual_support.manual_review_safe_int("3") == 3


def test_direct_editor_import_when_qt_is_available() -> None:
    if manual_editor is None:
        return
    assert hasattr(manual_editor, "DocstringReviewEditorDialog")


if __name__ == "__main__":
    test_support_has_no_reverse_import_to_review_panel()
    test_editor_uses_non_colliding_support_names()
    test_manifest_breaks_manual_review_cycle()
    test_report_panel_lazily_opens_editor()
    test_direct_support_import_when_dependencies_are_available()
    test_direct_editor_import_when_qt_is_available()
    print("T3R004 manual review import boundary tests passed.")
