"""Source contract for hiding Project Q&A lazy-tab status/source labels."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAZY_TABS = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"


def test_project_qa_hides_loaded_and_source_labels() -> None:
    """Project Q&A should not show the lazy LOADED/Source row."""
    source = LAZY_TABS.read_text(encoding="utf-8")
    header_set_start = source.index("_HEADER_TEMPLATE_ONLY_SOURCES = {")
    header_set_end = source.index("}", header_set_start)
    block = source[header_set_start:header_set_end]

    assert '_PROJECT_QA_GUI_SOURCE = f"{_CANONICAL_PACKAGE_NAME}/reasoner_engine/ai_reasoner_main_window.py"' in source
    assert "_PROJECT_QA_GUI_SOURCE" in block


if __name__ == "__main__":
    test_project_qa_hides_loaded_and_source_labels()
    print("Project Q&A header status/source hidden test passed.")
