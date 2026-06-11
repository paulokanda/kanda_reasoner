"""Tests for PA032 Tab 3 scan-only and review-state workflow language."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.tab3_manual_review_runtime.scan_only_workflow import (
    SCAN_MODE,
    configure_scan_only_controls,
    run_scan_only_mode,
    run_scan_selected_mode,
)

LAYOUT_FILE = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)
INLINE_FILE = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "inline_corrector_runtime.py"
)
RUN_CONTROLS_FILE = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
    / "run_controls.py"
)
MODE_HELP_FILE = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "mode_options_hlp.py"
)


class _FakeCombo:
    """Minimal combo box for scan-only workflow tests."""

    def __init__(self) -> None:
        self.items: list[str] = ["scan", "diff", "write"]
        self.current = "write"
        self.enabled = True
        self.hidden = False

    def clear(self) -> None:
        """Clear items."""
        self.items.clear()

    def addItem(self, text: str) -> None:
        """Add one item."""
        self.items.append(text)

    def setCurrentText(self, text: str) -> None:
        """Set current text."""
        self.current = text

    def setEnabled(self, enabled: bool) -> None:
        """Set enabled state."""
        self.enabled = enabled

    def hide(self) -> None:
        """Record hidden state."""
        self.hidden = True


class _FakeCheckBox:
    """Minimal check box for scan-only workflow tests."""

    def __init__(self) -> None:
        self.checked = True
        self.hidden = False

    def setChecked(self, checked: bool) -> None:
        """Set checked state."""
        self.checked = checked

    def hide(self) -> None:
        """Record hidden state."""
        self.hidden = True


class _FakeButton:
    """Minimal button for scan-only workflow tests."""

    def __init__(self) -> None:
        self.text = "Run Selected Mode"

    def setText(self, text: str) -> None:
        """Set button text."""
        self.text = text


class _FakeWindow:
    """Minimal window object for scan-only workflow tests."""

    def __init__(self) -> None:
        self._mode_combo = _FakeCombo()
        self._confirm_write_checkbox = _FakeCheckBox()
        self._run_button = _FakeButton()


def test_scan_only_controls_remove_legacy_modes() -> None:
    """Scan-only configuration hides legacy mode and write controls."""
    window = _FakeWindow()

    configure_scan_only_controls(window)

    assert window._mode_combo.items == [SCAN_MODE]
    assert window._mode_combo.current == SCAN_MODE
    assert window._mode_combo.enabled is False
    assert window._mode_combo.hidden is True
    assert window._confirm_write_checkbox.checked is False
    assert window._confirm_write_checkbox.hidden is True
    assert window._run_button.text == "Scan Files for Missing Docstrings"


def test_run_wrappers_always_call_legacy_scan_mode() -> None:
    """Legacy run calls are clamped to scan mode."""
    called: list[str] = []
    window = _FakeWindow()

    def legacy_run_mode(owner: object, mode: str) -> None:
        del owner
        called.append(mode)

    run_scan_selected_mode(window, legacy_run_mode)
    run_scan_only_mode(window, "write", legacy_run_mode)

    assert called == [SCAN_MODE, SCAN_MODE]


def test_tab3_options_layout_uses_scan_language_only() -> None:
    """The Tab 3 options surface should not expose diff/write mode controls."""
    text = LAYOUT_FILE.read_text(encoding="utf-8")

    assert 'QGroupBox("Missing Docstring Handler Options")' in text
    assert 'QLabel("Mode: Scan")' in text
    assert 'mode_row.addWidget(window._mode_combo)' not in text
    assert 'include_row.addWidget(window._confirm_write_checkbox)' not in text
    assert 'QPushButton("Scan Files for Missing Docstrings")' in text
    assert "Run Selected Mode" not in text


def test_review_buttons_use_report_state_language() -> None:
    """Review-stage buttons should not look like source-writing actions."""
    text = LAYOUT_FILE.read_text(encoding="utf-8")

    assert 'QPushButton("Save Review Decision")' in text
    assert 'QPushButton("Approve Row")' in text
    assert 'QPushButton("Reject Row")' in text
    assert 'QPushButton("Undo Row Change")' in text
    assert 'QPushButton("Approve Visible Rows")' in text
    assert 'QPushButton("Save change")' not in text
    assert 'QPushButton("Save All")' not in text


def test_review_stage_does_not_call_batch_source_apply() -> None:
    """Approve Visible Rows must not call the source-writing batch apply path."""
    text = INLINE_FILE.read_text(encoding="utf-8")

    assert "def approve_visible_rows" in text
    assert "apply_approved_review_batch" not in text
    assert "manual_docstring_review_batch" not in text
    assert "It is risky to approve all visible rows" in text
    assert "This will not modify source files" in text


def test_run_controls_facade_clamps_legacy_modes_to_scan() -> None:
    """The run-controls facade should expose scan-only wrappers."""
    text = RUN_CONTROLS_FILE.read_text(encoding="utf-8")

    assert "run_scan_selected_mode" in text
    assert "run_scan_only_mode" in text
    assert "_legacy_run_mode" in text
    assert "currentText()" not in text


def test_mode_help_no_longer_documents_diff_write_as_tab3_modes() -> None:
    """Mode help should document only scan mode for the Tab 3 handler."""
    text = MODE_HELP_FILE.read_text(encoding="utf-8")

    assert '"scan"' in text
    assert '"diff"' not in text
    assert '"write"' not in text
    assert "Apply Approved " in text
    assert "Docstrings to Source Files" in text


if __name__ == "__main__":
    test_scan_only_controls_remove_legacy_modes()
    test_run_wrappers_always_call_legacy_scan_mode()
    test_tab3_options_layout_uses_scan_language_only()
    test_review_buttons_use_report_state_language()
    test_review_stage_does_not_call_batch_source_apply()
    test_run_controls_facade_clamps_legacy_modes_to_scan()
    test_mode_help_no_longer_documents_diff_write_as_tab3_modes()
    print("PA032 Tab 3 scan-only review language tests passed.")
