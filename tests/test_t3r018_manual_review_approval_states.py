"""Regression tests for Tab 3 manual review approval states."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HELP = ROOT / 'ask_' 'ai_project_reasoner' / "insert_missing_docstrings_gui" / "insert_missing_docstrings_gui_help"
EDITOR = HELP / "manual_docstring_review_editor.py"
SUPPORT = HELP / "manual_docstring_review_support.py"
EXPORT = HELP / "manual_docstring_review_export.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_editor_has_approval_state_buttons_and_handler() -> None:
    text = _read(EDITOR)
    assert 'QPushButton("Approve")' in text
    assert 'QPushButton("Reject")' in text
    assert 'QPushButton("Needs edit")' in text
    assert 'set_approval_state(value)' in text
    assert "def set_approval_state(self, approval_state: str) -> None:" in text


def test_editor_state_indicator_shows_approval_state() -> None:
    text = _read(EDITOR)
    assert 'location.get("approval_state", "")' in text
    assert '" | Approval: " + approval + " | Filter: "' in text
    assert "Approval state saved: " in text


def test_support_persists_and_restores_approval_state() -> None:
    text = _read(SUPPORT)
    assert 'location["approval_state"] = str(saved.get("approval_state", ""))' in text
    assert '"approval_state": str(location.get("approval_state", ""))' in text


def test_export_includes_approval_state() -> None:
    assert '"approval_state": str(location.get("approval_state", ""))' in _read(EXPORT)


def test_modules_remain_under_size_threshold() -> None:
    assert len(_read(EDITOR).splitlines()) < 500
    assert len(_read(SUPPORT).splitlines()) < 500
    assert len(_read(EXPORT).splitlines()) < 500


if __name__ == "__main__":
    test_editor_has_approval_state_buttons_and_handler()
    test_editor_state_indicator_shows_approval_state()
    test_support_persists_and_restores_approval_state()
    test_export_includes_approval_state()
    test_modules_remain_under_size_threshold()
    print("T3R018 manual review approval state tests passed.")
