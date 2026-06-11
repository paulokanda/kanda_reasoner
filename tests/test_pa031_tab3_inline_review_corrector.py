"""Regression checks for the Tab 3 inline review corrector layout."""

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


def test_layout_uses_new_review_tab_title_and_controls() -> None:
    """Verify the review UI keeps the requested controls after PA041."""
    text = _read_text(LAYOUT_RUNTIME)
    inline_text = _read_text(INLINE_RUNTIME)
    engine_text = _read_text(ENGINE_RUNTIME)

    assert "Review and Correct Missing Docstrings" in text
    assert "Before Correction" in text
    assert "After Correction" in text

    for label in (
        "Previous",
        "Next",
        "Reset",
        "Save Review Decision",
        "Approve Row",
        "Reject Row",
        "Undo Row Change",
        "Approve Visible Rows",
    ):
        assert label in text

    assert "_review_engine_status_label" in text
    assert "HEURISTIC CORRECTION" in text or "HEURISTIC CORRECTION" in engine_text
    assert "CORRECTION WITH AI" in engine_text

    assert "QRadioButton" not in text
    assert "Correction with" not in text


if __name__ == "__main__":
    test_layout_uses_new_review_tab_title_and_controls()
    print("PA031 Tab 3 inline review corrector tests passed.")
