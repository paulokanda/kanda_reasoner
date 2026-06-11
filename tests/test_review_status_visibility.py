"""Public contract tests for Tab 3 draft status helpers."""

from __future__ import annotations

import kanda_reasoner_app.tab3_manual_review_runtime.review_status_visibility as review_status_visibility


class _Label:
    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _Owner:
    def __init__(self) -> None:
        self._review_draft_status_label = _Label()
        self.output: list[str] = []

    def _append_text(self, text: str) -> None:
        self.output.append(text)


def _reviewable_row() -> dict:
    return {
        "file": "app/main.py",
        "action": "inserted",
        "target_kind": "function",
        "target_name": "build_runner",
        "line": 10,
        "draft_docstring": "Build a runner.",
        "selected_draft_source": "heuristic",
    }


def test_draft_status_public_contract() -> None:
    owner = _Owner()
    row = _reviewable_row()
    assert review_status_visibility.draft_status_text_for_row(row) == "HEURISTIC DRAFT GENERATED"
    review_status_visibility.apply_review_draft_status(owner, row)
    assert owner._review_draft_status_label.text == "HEURISTIC DRAFT GENERATED"

    row["selected_draft_source"] = "ai"
    row["ai_draft_docstring"] = "Build a runner using AI context."
    assert review_status_visibility.draft_status_text_for_row(row) == "AI DRAFT GENERATED"

    row["selected_draft_source"] = "heuristic_fallback"
    row["ai_used_fallback"] = True
    row["ai_error"] = "Connection refused"
    assert review_status_visibility.draft_status_text_for_row(row) == "AI UNAVAILABLE - HEURISTIC FALLBACK"
    review_status_visibility.append_draft_generation_output(owner, row, "ai")
    assert any("AI UNAVAILABLE - HEURISTIC FALLBACK" in line for line in owner.output)
    assert any("AI error: Connection refused" in line for line in owner.output)


if __name__ == "__main__":
    test_draft_status_public_contract()
    print("review_status_visibility public contract tests passed.")
