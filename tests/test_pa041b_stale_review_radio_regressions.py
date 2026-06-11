"""Focused PA041B regression alignment checks."""

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


def test_pa041b_legacy_tests_expect_engine_status_not_radio_buttons() -> None:
    """Protect the PA041 single-engine-source contract."""
    layout_text = _read_text(LAYOUT_RUNTIME)
    inline_text = _read_text(INLINE_RUNTIME)
    engine_text = _read_text(ENGINE_RUNTIME)

    assert "_review_engine_status_label" in layout_text
    assert "HEURISTIC CORRECTION" in layout_text or "HEURISTIC CORRECTION" in engine_text
    assert "CORRECTION WITH AI" in engine_text
    assert "QRadioButton" not in layout_text
    assert "Correction with" not in layout_text


if __name__ == "__main__":
    test_pa041b_legacy_tests_expect_engine_status_not_radio_buttons()
    print("PA041B stale review radio regression tests passed.")
