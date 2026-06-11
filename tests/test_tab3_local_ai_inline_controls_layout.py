"""Source contract tests for Tab 3 Local AI inline controls layout."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAYOUT_RUNTIME = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "tab3_manual_review_runtime"
    / "layout_runtime.py"
)


def _local_ai_block() -> str:
    """Return the Local AI group source block."""
    source = LAYOUT_RUNTIME.read_text(encoding="utf-8")
    start = source.index("def _build_ai_group")
    end = source.index("def _build_report_group")
    return source[start:end]


def test_local_ai_runtime_controls_share_enable_row() -> None:
    """Enable, Base URL, Model, and Refresh should be on one row."""
    block = _local_ai_block()

    assert 'QGroupBox("Local AI")' in block
    assert "ai_runtime_row = QHBoxLayout()" in block
    assert "ai_runtime_row.addWidget(window._ai_enabled_checkbox)" in block
    assert 'ai_runtime_row.addWidget(QLabel("Base URL"))' in block
    assert "ai_runtime_row.addWidget(window._base_url_edit, 1)" in block
    assert 'ai_runtime_row.addWidget(QLabel("Model"))' in block
    assert "ai_runtime_row.addWidget(window._model_combo, 1)" in block
    assert 'ai_runtime_row.addWidget(QLabel("Refresh"))' in block
    assert "ai_runtime_row.addWidget(window._refresh_models_button)" in block
    assert 'layout.addRow("Enable local AI", ai_runtime_row)' in block


def test_local_ai_controls_are_not_vertical_form_rows() -> None:
    """The runtime controls should not be separate vertical form rows."""
    block = _local_ai_block()

    assert 'layout.addRow("Enable", window._ai_enabled_checkbox)' not in block
    assert 'layout.addRow("Base URL", window._base_url_edit)' not in block
    assert 'layout.addRow("Model", window._model_combo)' not in block
    assert 'layout.addRow("Refresh", window._refresh_models_button)' not in block


if __name__ == "__main__":
    test_local_ai_runtime_controls_share_enable_row()
    test_local_ai_controls_are_not_vertical_form_rows()
    print("Tab 3 Local AI inline controls layout tests passed.")
