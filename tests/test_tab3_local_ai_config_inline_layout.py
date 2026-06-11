"""Source contract tests for the Tab 3 Local AI config row layout."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)


def _source() -> str:
    return LAYOUT_RUNTIME.read_text(encoding="utf-8")


def _ai_group_block() -> str:
    source = _source()
    start = source.index("def _build_ai_group")
    end = source.index("def _build_report_group")
    return source[start:end]


def test_config_path_and_config_buttons_share_one_row() -> None:
    block = _ai_group_block()
    assert "config_row = QHBoxLayout()" in block
    assert "config_row.addWidget(window._config_path_edit, 1)" in block
    assert "config_row.addWidget(QLabel(\"Config\"))" in block
    assert "config_row.addWidget(window._load_config_button)" in block
    assert "config_row.addWidget(window._save_config_button)" in block
    assert "layout.addRow(\"Config path\", config_row)" in block


def test_config_buttons_are_not_on_separate_form_row() -> None:
    block = _ai_group_block()
    assert "layout.addRow(\"Config\", config_row)" not in block
    assert "layout.addRow(\"Config path\", window._config_path_edit)" not in block


if __name__ == "__main__":
    test_config_path_and_config_buttons_share_one_row()
    test_config_buttons_are_not_on_separate_form_row()
    print("Tab 3 Local AI config inline layout tests passed.")
