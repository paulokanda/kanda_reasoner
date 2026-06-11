"""Verify Tab 3 Project group no longer shows worker path controls."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)


def test_project_group_keeps_project_root_only() -> None:
    """Project group should not add the worker path field to the form layout."""
    source = LAYOUT_RUNTIME.read_text(encoding="utf-8")
    start = source.index("def _build_project_group")
    end = source.index("def _build_options_group")
    project_block = source[start:end]

    assert 'QGroupBox("Project")' in project_block
    assert 'layout.addRow("Project root", window._root_path_edit)' in project_block
    assert "layout.addRow(window._worker_path_edit)" not in project_block
    assert 'layout.addRow("Worker script", window._worker_path_edit)' not in project_block


if __name__ == "__main__":
    test_project_group_keeps_project_root_only()
    print("Tab 3 Project worker path field cleanup tests passed.")
