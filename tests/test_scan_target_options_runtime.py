"""Focused tests for PA037 Tab 3 scan target option labels."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime import scan_only_workflow
from kanda_reasoner_app.tab3_manual_review_runtime.scan_target_options_runtime import (
    configure_scan_target_checkboxes,
)


class _Combo:
    """Minimal combo fake."""

    def __init__(self) -> None:
        self.enabled = True
        self.hidden = False
        self.items: list[str] = []
        self.current_text = ""

    def clear(self) -> None:
        self.items.clear()

    def addItem(self, value: str) -> None:
        self.items.append(value)

    def setCurrentText(self, value: str) -> None:
        self.current_text = value

    def setEnabled(self, value: bool) -> None:
        self.enabled = bool(value)

    def hide(self) -> None:
        self.hidden = True


class _Button:
    """Minimal button fake."""

    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _CheckBox:
    """Minimal checkbox fake."""

    def __init__(self, checked: bool = True) -> None:
        self.text = ""
        self.checked = checked
        self.enabled = False
        self.hidden = True
        self.shown = False

    def setText(self, value: str) -> None:
        self.text = value

    def setChecked(self, value: bool) -> None:
        self.checked = bool(value)

    def setEnabled(self, value: bool) -> None:
        self.enabled = bool(value)

    def show(self) -> None:
        self.hidden = False
        self.shown = True

    def hide(self) -> None:
        self.hidden = True


class _Owner:
    """Minimal owner fake for scan-only controls."""

    def __init__(self) -> None:
        self._mode_combo = _Combo()
        self._confirm_write_checkbox = _CheckBox(checked=True)
        self._module_checkbox = _CheckBox(checked=True)
        self._class_checkbox = _CheckBox(checked=True)
        self._function_checkbox = _CheckBox(checked=True)
        self._file_address_checkbox = _CheckBox(checked=False)
        self._run_button = _Button()


def test_scan_target_checkboxes_use_requested_labels() -> None:
    """Tab 3 scan target options should use the requested wording."""
    owner = _Owner()

    configure_scan_target_checkboxes(owner)

    assert owner._module_checkbox.text == "Module Header Docstring"
    assert owner._class_checkbox.text == "Classes"
    assert owner._function_checkbox.text == "Function/Method"
    assert owner._file_address_checkbox.text == "# Path Module at top of file"


def test_file_path_module_checkbox_is_visible_and_preserves_user_choice() -> None:
    """The path-module checkbox should remain user-controlled in scan mode."""
    owner = _Owner()
    owner._file_address_checkbox.checked = False

    scan_only_workflow.configure_scan_only_controls(owner)

    assert owner._file_address_checkbox.hidden is False
    assert owner._file_address_checkbox.enabled is True
    assert owner._file_address_checkbox.checked is False
    assert owner._run_button.text == "Scan Files for Missing Docstrings"


def test_scan_only_still_hides_unsafe_write_confirmation() -> None:
    """Scan-only controls should not expose write confirmation as a scan option."""
    owner = _Owner()

    scan_only_workflow.configure_scan_only_controls(owner)

    assert owner._confirm_write_checkbox.checked is False
    assert owner._confirm_write_checkbox.hidden is True
    assert owner._mode_combo.items == ["scan"]
    assert owner._mode_combo.enabled is False


if __name__ == "__main__":
    test_scan_target_checkboxes_use_requested_labels()
    test_file_path_module_checkbox_is_visible_and_preserves_user_choice()
    test_scan_only_still_hides_unsafe_write_confirmation()
    print("PA037 Tab 3 scan target option label tests passed.")
