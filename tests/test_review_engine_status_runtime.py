"""Public contract tests for Tab 3 correction engine status helpers."""

from __future__ import annotations

import kanda_reasoner_app.tab3_manual_review_runtime.review_engine_status_runtime as review_engine_status_runtime


class _Label:
    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _CheckBox:
    def __init__(self, checked: bool, enabled: bool = True) -> None:
        self._checked = checked
        self._enabled = enabled

    def isChecked(self) -> bool:
        return self._checked

    def isEnabled(self) -> bool:
        return self._enabled


class _Owner:
    def __init__(self, checked: bool, enabled: bool = True) -> None:
        self._ai_enabled_checkbox = _CheckBox(checked=checked, enabled=enabled)
        self._review_engine_status_label = _Label()


def test_engine_status_uses_local_ai_checkbox_as_source_of_truth() -> None:
    owner = _Owner(checked=False)
    assert review_engine_status_runtime.local_ai_enabled_from_owner(owner) is False
    assert review_engine_status_runtime.correction_mode_from_owner(owner) == "heuristics"
    review_engine_status_runtime.apply_correction_engine_status(owner)
    assert owner._review_engine_status_label.text == "HEURISTIC CORRECTION"

    owner = _Owner(checked=True)
    assert review_engine_status_runtime.local_ai_enabled_from_owner(owner) is True
    assert review_engine_status_runtime.correction_mode_from_owner(owner) == "ai"
    review_engine_status_runtime.apply_correction_engine_status(owner)
    assert owner._review_engine_status_label.text == "CORRECTION WITH AI"

    owner = _Owner(checked=True, enabled=False)
    assert review_engine_status_runtime.local_ai_enabled_from_owner(owner) is False
    assert review_engine_status_runtime.correction_mode_from_owner(owner) == "heuristics"


if __name__ == "__main__":
    test_engine_status_uses_local_ai_checkbox_as_source_of_truth()
    print("review_engine_status_runtime public contract tests passed.")
