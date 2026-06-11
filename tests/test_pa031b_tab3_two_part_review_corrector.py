"""Regression checks for the strict two-part Tab 3 review corrector."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)
INLINE_RUNTIME = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "inline_corrector_runtime.py"
)
ENGINE_RUNTIME = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "review_engine_status_runtime.py"
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_review_corrector_preserves_requested_controls() -> None:
    """Verify the two-part corrector no longer expects radio buttons."""
    layout_text = _read_text(LAYOUT_RUNTIME)
    inline_text = _read_text(INLINE_RUNTIME)
    engine_text = _read_text(ENGINE_RUNTIME)

    assert "Before Correction" in layout_text
    assert "After Correction" in layout_text
    assert "_review_original_snippet" in layout_text
    assert "_review_corrected_snippet" in layout_text

    for label in (
        "Save Review Decision",
        "Approve Row",
        "Reject Row",
        "Undo Row Change",
        "Approve Visible Rows",
    ):
        assert label in layout_text

    assert "_review_engine_status_label" in layout_text
    assert "HEURISTIC CORRECTION" in layout_text or "HEURISTIC CORRECTION" in engine_text
    assert "CORRECTION WITH AI" in engine_text

    assert "QRadioButton" not in layout_text
    assert "Correction with" not in layout_text


def test_single_engine_source_uses_local_ai_checkbox() -> None:
    """Verify the old review radio-button mode is no longer the source."""
    inline_text = _read_text(INLINE_RUNTIME)
    engine_text = _read_text(ENGINE_RUNTIME)

    assert "def _selected_correction_mode" in inline_text
    assert "review_engine_status_runtime.correction_mode_from_owner" in inline_text
    assert "return \"ai\"" in engine_text
    assert "return \"heuristics\"" in engine_text


if __name__ == "__main__":
    test_review_corrector_preserves_requested_controls()
    test_single_engine_source_uses_local_ai_checkbox()
    print("PA031B Tab 3 two-part review corrector tests passed.")
