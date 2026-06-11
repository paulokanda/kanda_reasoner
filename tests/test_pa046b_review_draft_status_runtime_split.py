"""PA046B tests for split Tab 3 review draft status helpers."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import (
    inline_corrector_runtime,
    review_status_visibility,
    review_engine_status_runtime,
)


def test_inline_corrector_stays_below_architecture_line_threshold() -> None:
    path = Path(
        'ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/inline_corrector_runtime.py'
    )
    line_count = len(path.read_text(encoding="utf-8").splitlines())
    assert line_count < 500


def test_status_helper_preserves_public_status_text() -> None:
    row = {
        "file": "app.py",
        "action": "inserted",
        "target_kind": "function",
        "target_name": "build_runner",
        "line": 1,
        "draft_docstring": "Build a runner.",
        "selected_draft_source": "heuristic",
    }
    assert (
        review_status_visibility.draft_status_text_for_row(row)
        == "HEURISTIC DRAFT GENERATED"
    )
    row["selected_draft_source"] = "ai"
    row["ai_draft_docstring"] = "Build a runner with AI."
    assert review_status_visibility.draft_status_text_for_row(row) == "AI DRAFT GENERATED"
    row["selected_draft_source"] = "heuristic_fallback"
    row["ai_used_fallback"] = True
    assert (
        review_status_visibility.draft_status_text_for_row(row)
        == "AI UNAVAILABLE - HEURISTIC FALLBACK"
    )


def test_inline_public_refresh_delegates_to_split_helper() -> None:
    class Label:
        def __init__(self) -> None:
            self.text = ""

        def setText(self, value: str) -> None:
            self.text = value

    class Owner:
        def __init__(self) -> None:
            self._review_draft_status_label = Label()

    owner = Owner()
    row = {
        "file": "app.py",
        "action": "inserted",
        "target_kind": "function",
        "target_name": "read_value",
        "line": 1,
        "draft_docstring": "Read value.",
        "selected_draft_source": "heuristic",
    }
    inline_corrector_runtime.refresh_review_draft_status(owner, row)
    assert owner._review_draft_status_label.text == "HEURISTIC DRAFT GENERATED"


def test_engine_status_helper_preserves_single_source_of_truth() -> None:
    class CheckBox:
        def __init__(self, checked: bool) -> None:
            self.checked = checked

        def isEnabled(self) -> bool:
            return True

        def isChecked(self) -> bool:
            return self.checked

    class Owner:
        def __init__(self, checked: bool) -> None:
            self._ai_enabled_checkbox = CheckBox(checked)

    assert review_engine_status_runtime.correction_mode_from_owner(Owner(False)) == "heuristics"
    assert review_engine_status_runtime.correction_mode_from_owner(Owner(True)) == "ai"


if __name__ == "__main__":
    test_inline_corrector_stays_below_architecture_line_threshold()
    test_status_helper_preserves_public_status_text()
    test_inline_public_refresh_delegates_to_split_helper()
    test_engine_status_helper_preserves_single_source_of_truth()
    print("PA046B review draft status runtime split tests passed.")
