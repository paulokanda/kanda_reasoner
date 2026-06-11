"""Tests for PA035C inline corrector runtime hotfix."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.tab3_manual_review_runtime import inline_corrector_runtime


class _Radio:
    """Minimal radio-button stand-in."""

    def __init__(self, checked: bool) -> None:
        self._checked = checked

    def isChecked(self) -> bool:
        """Return whether the radio button is checked."""
        return self._checked


class _TextEdit:
    """Minimal plain-text widget stand-in."""

    def __init__(self) -> None:
        self.text = ""

    def setPlainText(self, value: str) -> None:
        """Store plain text."""
        self.text = value


class _LineEdit:
    """Minimal line-edit stand-in."""

    def __init__(self, value: str) -> None:
        self._value = value

    def text(self) -> str:
        """Return line-edit text."""
        return self._value


class _Owner:
    """Owner object with the attributes used by refresh."""

    def __init__(self, root: Path, ai_checked: bool) -> None:
        self._root_path_edit = _LineEdit(str(root))
        self._review_original_snippet = _TextEdit()
        self._review_corrected_snippet = _TextEdit()
        self._review_ai_radio = _Radio(ai_checked)


def test_refresh_inline_corrector_uses_default_heuristics_mode() -> None:
    """Verify refresh no longer crashes when heuristics is selected."""
    owner = _Owner(Path("."), ai_checked=False)
    inline_corrector_runtime.refresh_inline_corrector_for_selection(owner, None)

    assert "No review item" in owner._review_original_snippet.text
    assert "No review item" in owner._review_corrected_snippet.text


def test_refresh_inline_corrector_uses_ai_mode_when_selected(tmp_path: Path) -> None:
    """Verify refresh accepts AI mode and renders corrected preview."""
    source = tmp_path / "sample.py"
    source.write_text("def sample():\n    return 1\n", encoding="utf-8")
    owner = _Owner(tmp_path, ai_checked=True)
    row = {
        "action": "inserted",
        "file": "sample.py",
        "line": 1,
        "target_kind": "function",
        "target_name": "sample",
        "suggested_docstring": "Support sample behavior.",
    }

    inline_corrector_runtime.refresh_inline_corrector_for_selection(owner, row)

    assert "def sample" in owner._review_original_snippet.text
    assert "Support sample behavior." in owner._review_corrected_snippet.text


if __name__ == "__main__":
    test_refresh_inline_corrector_uses_default_heuristics_mode()
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        test_refresh_inline_corrector_uses_ai_mode_when_selected(Path(temp_dir))
    print("PA035C inline corrector runtime hotfix tests passed.")
