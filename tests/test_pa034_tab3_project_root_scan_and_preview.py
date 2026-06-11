"""Tests for PA034 Tab 3 project-root scan and preview placement."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.tab3_manual_review_runtime.inline_preview_runtime import (
    build_corrected_snippet_text,
)
from kanda_reasoner_app.tab3_manual_review_runtime.scan_only_workflow import (
    DEFAULT_SCAN_REPORT_NAME,
    ensure_scan_report_path,
    run_scan_selected_mode,
    use_project_root_as_scan_scope,
)

LAYOUT_FILE = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)
SCAN_ONLY_FILE = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "scan_only_workflow.py"
)
INLINE_FILE = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "inline_corrector_runtime.py"
)


class _FakeLineEdit:
    """Minimal line edit for workflow tests."""

    def __init__(self, value: str = "") -> None:
        self.value = value
        self.cleared = False

    def text(self) -> str:
        """Return current text."""
        return self.value

    def setText(self, value: str) -> None:
        """Set current text."""
        self.value = value

    def clear(self) -> None:
        """Clear current text."""
        self.value = ""
        self.cleared = True


class _FakeCombo:
    """Minimal combo box for scan scope tests."""

    def __init__(self, value: str) -> None:
        self.value = value

    def currentText(self) -> str:
        """Return current text."""
        return self.value

    def setCurrentText(self, value: str) -> None:
        """Set current text."""
        self.value = value


class _FakeButton:
    """Minimal button for scan-only control tests."""

    def __init__(self) -> None:
        self.text_value = ""

    def setText(self, value: str) -> None:
        """Set visible button text."""
        self.text_value = value


class _FakeModeCombo(_FakeCombo):
    """Minimal mode combo with methods used by scan-only configuration."""

    def __init__(self) -> None:
        super().__init__("write")
        self.items: list[str] = []

    def clear(self) -> None:
        """Clear mode items."""
        self.items.clear()

    def addItem(self, value: str) -> None:
        """Add a mode item."""
        self.items.append(value)

    def setEnabled(self, _enabled: bool) -> None:
        """Accept enabled state."""

    def hide(self) -> None:
        """Accept hidden state."""


class _FakeCheckBox:
    """Minimal checkbox used by scan-only configuration."""

    def setChecked(self, _checked: bool) -> None:
        """Accept checked state."""

    def hide(self) -> None:
        """Accept hidden state."""


class _FakeOwner:
    """Minimal owner object for Tab 3 scan tests."""

    def __init__(self, root: Path) -> None:
        self._root_path_edit = _FakeLineEdit(str(root))
        self._report_path_edit = _FakeLineEdit("")
        self._target_path_edit = _FakeLineEdit("")
        self._scope_combo = _FakeCombo("Package/folder")
        self._mode_combo = _FakeModeCombo()
        self._confirm_write_checkbox = _FakeCheckBox()
        self._run_button = _FakeButton()
        self._current_report_path: Path | None = None
        self.saved_preferences = 0
        self.messages: list[str] = []

    def _save_prefs(self) -> None:
        """Record preference save."""
        self.saved_preferences += 1

    def _append_text(self, text: str) -> None:
        """Record output text."""
        self.messages.append(text)


def test_project_group_has_browse_button_next_to_project_root() -> None:
    """The Project group should expose a Browse button for project root."""
    text = LAYOUT_FILE.read_text(encoding="utf-8")

    assert 'QGroupBox("Project")' in text
    assert '_browse_root_button = QPushButton("Browse")' in text
    assert 'window._browse_root_button, "clicked", window.browse_root' in text


def test_scan_uses_project_root_without_target_picker() -> None:
    """Scan should use project root when no explicit module or package is set."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        owner = _FakeOwner(root)

        use_project_root_as_scan_scope(owner)

        assert owner._scope_combo.currentText() == "Full project"
        assert owner._target_path_edit.text() == ""


def test_scan_sets_user_selected_report_path_outside_project_root() -> None:
    """Scan should ask for an outside report path before running."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "project"
        root.mkdir()
        owner = _FakeOwner(root)
        expected = root.parent / DEFAULT_SCAN_REPORT_NAME

        ok = ensure_scan_report_path(owner, chooser=lambda _owner, _default: expected)

        assert ok is True
        assert owner._report_path_edit.text() == str(expected)
        assert owner._current_report_path == expected
        assert "report path selected" in "".join(owner.messages)


def test_scan_run_uses_report_chooser_not_target_picker() -> None:
    """Running scan should use report chooser and never preserve target picker state."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "project"
        root.mkdir()
        owner = _FakeOwner(root)
        called: list[str] = []

        def legacy_run_mode(_owner: object, mode: str) -> None:
            called.append(mode)

        selected = root.parent / DEFAULT_SCAN_REPORT_NAME
        run_scan_selected_mode(
            owner,
            legacy_run_mode,
            chooser=lambda _owner, _default: selected,
        )

        assert called == ["scan"]
        assert owner._scope_combo.currentText() == "Full project"
        assert owner._target_path_edit.text() == ""
        assert owner._report_path_edit.text() == str(selected)


def test_corrected_preview_inserts_docstring_inside_next_method() -> None:
    """Preview should insert method docstrings inside the method block."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / "patient_records.py"
        source.write_text(
            "class PatientRecord:\n"
            "    def __init__(self, patient_id, name):\n"
            "        self.patient_id = patient_id\n"
            "        self.name = name\n"
            "        self.notes = []\n"
            "\n"
            "    def add_note(self, note):\n"
            "        self.notes.append(note)\n"
            "\n"
            "    def summary(self):\n"
            "        return {\n"
            "            \"patient_id\": self.patient_id,\n"
            "        }\n",
            encoding="utf-8",
        )
        owner = type("Owner", (), {"_root_path_edit": _FakeLineEdit(str(root))})()
        row = {
            "action": "inserted",
            "file": "patient_records.py",
            "line": 9,
            "target_kind": "method",
            "target_name": "summary",
            "reason": "missing docstring",
            "draft_docstring": "Support summary behavior.",
        }

        corrected = build_corrected_snippet_text(owner, row, "heuristics")

        assert "    def summary(self):\n" in corrected
        assert '        """Support summary behavior."""' in corrected
        assert '        """Support summary behavior."""\n   11 |     def summary' not in corrected


def test_scan_workflow_uses_save_dialog_for_report_creation() -> None:
    """The scan workflow should ask where to save the report."""
    text = SCAN_ONLY_FILE.read_text(encoding="utf-8")

    assert "getSaveFileName" in text
    assert "Save Missing Docstrings Report" in text
    assert "use_project_root_as_scan_scope" in text


def test_preview_has_definition_aware_insertion_logic() -> None:
    """The preview helper should be definition-aware, not only line-based."""
    text = INLINE_FILE.read_text(encoding="utf-8")

    preview_file = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime" / "inline_preview_runtime.py"
    preview_text = preview_file.read_text(encoding="utf-8")

    assert "def _preview_insertion_point" in preview_text
    assert "def _find_definition_index" in preview_text
    assert "def _definition_docstring_indent" in preview_text


if __name__ == "__main__":
    test_project_group_has_browse_button_next_to_project_root()
    test_scan_uses_project_root_without_target_picker()
    test_scan_sets_user_selected_report_path_outside_project_root()
    test_scan_run_uses_report_chooser_not_target_picker()
    test_corrected_preview_inserts_docstring_inside_next_method()
    test_scan_workflow_uses_save_dialog_for_report_creation()
    test_preview_has_definition_aware_insertion_logic()
    print("PA034 Tab 3 project-root scan and preview tests passed.")
