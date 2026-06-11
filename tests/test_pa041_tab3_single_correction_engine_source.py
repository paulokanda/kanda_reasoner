"""Focused tests for PA041 Tab 3 single correction engine source."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import inline_corrector_runtime


class _Signal:
    """Small signal fake that stores connected slots."""

    def __init__(self) -> None:
        self.slots = []

    def connect(self, slot):
        self.slots.append(slot)

    def emit(self, *args):
        for slot in list(self.slots):
            slot(*args)


class _CheckBox:
    """Small checkbox fake for Local AI state."""

    def __init__(self, checked: bool = False, enabled: bool = True) -> None:
        self._checked = checked
        self._enabled = enabled
        self.toggled = _Signal()

    def isChecked(self) -> bool:
        return self._checked

    def isEnabled(self) -> bool:
        return self._enabled

    def setChecked(self, value: bool) -> None:
        self._checked = bool(value)
        self.toggled.emit(bool(value))


class _Label:
    """Small label fake."""

    def __init__(self) -> None:
        self.text = ""

    def setText(self, text: str) -> None:
        self.text = text


class _Owner:
    """Small owner fake for correction engine status."""

    def __init__(self) -> None:
        self._ai_enabled_checkbox = _CheckBox(False)
        self._review_engine_status_label = _Label()
        self._review_previous_button = None
        self._review_next_button = None
        self._review_reset_button = None
        self._review_save_change_button = None
        self._review_approve_row_button = None
        self._review_reject_row_button = None
        self._review_undo_button = None
        self._review_save_all_button = None
        self._review_list = None


def test_local_ai_checkbox_controls_correction_engine_label() -> None:
    """The Local AI checkbox must be the only correction engine source."""
    owner = _Owner()

    inline_corrector_runtime.refresh_correction_engine_status(owner)
    assert owner._review_engine_status_label.text == "HEURISTIC CORRECTION"

    owner._ai_enabled_checkbox.setChecked(True)
    inline_corrector_runtime.refresh_correction_engine_status(owner)
    assert owner._review_engine_status_label.text == "CORRECTION WITH AI"

    owner._ai_enabled_checkbox.setChecked(False)
    inline_corrector_runtime.refresh_correction_engine_status(owner)
    assert owner._review_engine_status_label.text == "HEURISTIC CORRECTION"


def test_wire_events_updates_engine_status_when_local_ai_changes() -> None:
    """Toggling Local AI should update the After Correction status label."""
    owner = _Owner()
    inline_corrector_runtime.wire_inline_corrector_events(owner)

    assert owner._review_engine_status_label.text == "HEURISTIC CORRECTION"

    owner._ai_enabled_checkbox.setChecked(True)
    assert owner._review_engine_status_label.text == "CORRECTION WITH AI"

    owner._ai_enabled_checkbox.setChecked(False)
    assert owner._review_engine_status_label.text == "HEURISTIC CORRECTION"


def test_after_correction_layout_has_no_radio_engine_selector() -> None:
    """After Correction should no longer declare AI/Heuristics radio buttons."""
    layout_path = Path(
        'ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/layout_runtime.py'
    )
    text = layout_path.read_text(encoding="utf-8")

    assert "QRadioButton" not in text
    assert "_review_ai_radio" not in text
    assert "_review_heuristic_radio" not in text
    assert "Correction with" not in text
    assert "_review_engine_status_label" in text
    assert "layout.addRow(ai_runtime_row)" in text


if __name__ == "__main__":
    test_local_ai_checkbox_controls_correction_engine_label()
    test_wire_events_updates_engine_status_when_local_ai_changes()
    test_after_correction_layout_has_no_radio_engine_selector()
    print("PA041 Tab 3 single correction engine source tests passed.")
