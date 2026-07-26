"""Focused coverage for Docstring Assistant scan/diff/write mode restoration."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.tab3_manual_review_runtime import scan_only_workflow


class _Combo:
    """Small combo-box test double."""

    def __init__(self, current: str = "diff") -> None:
        self.items: list[str] = ["scan", "diff", "write"]
        self.current = current
        self.enabled = False
        self.hidden = True
        self.shown = False

    def clear(self) -> None:
        self.items.clear()

    def addItem(self, value: str) -> None:
        self.items.append(value)

    def setCurrentText(self, value: str) -> None:
        self.current = value

    def setEnabled(self, value: bool) -> None:
        self.enabled = bool(value)

    def show(self) -> None:
        self.hidden = False
        self.shown = True


class _CheckBox:
    """Small checkbox test double."""

    def __init__(self) -> None:
        self.enabled = False
        self.hidden = True
        self.shown = False

    def setEnabled(self, value: bool) -> None:
        self.enabled = bool(value)

    def show(self) -> None:
        self.hidden = False
        self.shown = True


class _Button:
    """Small button test double."""

    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _Owner:
    """Small owner object with the controls used by the mode helper."""

    def __init__(self) -> None:
        self._mode_combo = _Combo()
        self._confirm_write_checkbox = _CheckBox()
        self._module_checkbox = _CheckBox()
        self._class_checkbox = _CheckBox()
        self._function_checkbox = _CheckBox()
        self._file_address_checkbox = _CheckBox()
        self._run_button = _Button()


def test_scan_diff_write_controls_restore_all_modes() -> None:
    """The live Tab 3 helper should expose all backend modes."""
    owner = _Owner()

    scan_only_workflow.configure_scan_diff_write_controls(owner)

    assert owner._mode_combo.items == ["scan", "diff", "write"]
    assert owner._mode_combo.current == "diff"
    assert owner._mode_combo.enabled is True
    assert owner._mode_combo.hidden is False
    assert owner._confirm_write_checkbox.hidden is False
    assert owner._run_button.text == "Preview Docstring Diff"


def test_run_button_text_tracks_selected_mode() -> None:
    """The primary action should make the selected mode explicit."""
    owner = _Owner()

    scan_only_workflow.refresh_selected_mode_controls(owner, "scan")
    assert owner._run_button.text == "Scan Files for Missing Docstrings"

    scan_only_workflow.refresh_selected_mode_controls(owner, "write")
    assert owner._run_button.text == "Write Missing Docstrings"
    assert owner._confirm_write_checkbox.enabled is True


if __name__ == "__main__":
    test_scan_diff_write_controls_restore_all_modes()
    test_run_button_text_tracks_selected_mode()
    print("Docstring Assistant scan/diff/write mode tests passed.")
