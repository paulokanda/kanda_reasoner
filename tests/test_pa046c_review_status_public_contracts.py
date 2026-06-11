"""PA046C direct public-contract tests for split review status helpers."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime import review_status_visibility
from kanda_reasoner_app.tab3_manual_review_runtime import review_engine_status_runtime


class _Label:
    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _Checkbox:
    def __init__(self, checked: bool = False, enabled: bool = True) -> None:
        self._checked = checked
        self._enabled = enabled

    def isChecked(self) -> bool:
        return self._checked

    def isEnabled(self) -> bool:
        return self._enabled


class _Owner:
    def __init__(self, checked: bool = False) -> None:
        self._ai_enabled_checkbox = _Checkbox(checked=checked)
        self._review_engine_status_label = _Label()
        self._review_draft_status_label = _Label()
        self.output = []

    def _append_text(self, text: str) -> None:
        self.output.append(text)


def test_review_engine_status_runtime_public_contract() -> None:
    owner = _Owner(checked=False)
    assert review_engine_status_runtime.correction_mode_from_owner(owner) == "heuristics"
    review_engine_status_runtime.apply_correction_engine_status(owner)
    assert owner._review_engine_status_label.text == "HEURISTIC CORRECTION"

    owner = _Owner(checked=True)
    assert review_engine_status_runtime.correction_mode_from_owner(owner) == "ai"
    review_engine_status_runtime.apply_correction_engine_status(owner)
    assert owner._review_engine_status_label.text == "CORRECTION WITH AI"


def test_review_status_visibility_public_contract() -> None:
    owner = _Owner()
    row = {
        "file": "app/main.py",
        "action": "inserted",
        "target_kind": "function",
        "target_name": "build_runner",
        "line": 10,
        "kind": "function",
        "name": "build_runner",
        "draft_docstring": "Build a runner.",
        "selected_draft_source": "heuristic",
    }

    assert review_status_visibility.draft_status_text_for_row(row) == "HEURISTIC DRAFT GENERATED"
    review_status_visibility.apply_review_draft_status(owner, row)
    assert owner._review_draft_status_label.text == "HEURISTIC DRAFT GENERATED"

    row["selected_draft_source"] = "heuristic_fallback"
    row["ai_used_fallback"] = True
    row["ai_error"] = "Connection refused"
    review_status_visibility.append_draft_generation_output(owner, row, "ai")
    assert any("AI UNAVAILABLE - HEURISTIC FALLBACK" in line for line in owner.output)
    assert any("AI error: Connection refused" in line for line in owner.output)


if __name__ == "__main__":
    test_review_engine_status_runtime_public_contract()
    test_review_status_visibility_public_contract()
    print("PA046C review status public contract tests passed.")
