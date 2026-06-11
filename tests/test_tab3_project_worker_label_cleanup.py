"""Source contract tests for Tab 3 Project group worker status layout."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)


def _source() -> str:
    """Return the Tab 3 layout runtime source."""
    return LAYOUT_RUNTIME.read_text(encoding="utf-8")


def test_project_group_has_no_worker_script_label_or_path_field() -> None:
    """The Project group should only show Project root controls."""
    source = _source()
    project_start = source.index("def _build_project_group")
    options_start = source.index("def _build_options_group")
    project_block = source[project_start:options_start]

    assert 'QGroupBox("Project")' in project_block
    assert 'layout.addRow("Project root", window._root_path_edit)' in project_block
    assert "window._worker_path_edit" not in project_block
    assert "Worker script" not in project_block


if __name__ == "__main__":
    test_project_group_has_no_worker_script_label_or_path_field()
    print("Tab 3 Project worker label cleanup tests passed.")
