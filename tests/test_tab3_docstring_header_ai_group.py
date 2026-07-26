"""Source contract for the Docstring Assistant header AI model group."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAZY_TABS = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"


def _source() -> str:
    """Return the lazy tab host source."""
    return LAZY_TABS.read_text(encoding="utf-8")


def test_docstring_assistant_uses_header_ai_template_group() -> None:
    """Docstring Assistant should install the compact template AI model group."""
    source = _source()
    start = source.index("if spec.source_hint in {")
    end = source.index("outer.addLayout(self.header_row)")
    block = source[start:end]

    assert "_DOCSTRINGS_GUI_SOURCE" in block
    assert "self.tab_header_template.install_ai_group_blueprint" in block
    assert "refresh_handler = self._refresh_docstring_header_ai_models" in block
    assert "review_handler = None" in block


def test_docstring_header_group_binds_after_safe_mode_radio() -> None:
    """The AI group should sit after the Tab 1 audit radio and before Help."""
    source = _source()
    load_start = source.index("def load_tool")
    load_block = source[load_start:]

    safe_mode_index = load_block.index("self._move_tab3_safe_mode_radio_to_header_row(widget)")
    bind_index = load_block.index("self._bind_tab3_header_ai_model_controls(widget)")
    show_project_index = load_block.index("self._move_show_project_project_root_controls_to_header_row(widget)")

    assert safe_mode_index < bind_index < show_project_index


def test_docstring_header_model_selector_sync_helpers_exist() -> None:
    """Header selector must synchronize with the embedded Tab 3 model combo."""
    source = _source()

    assert "def _refresh_docstring_header_ai_models" in source
    assert "def _copy_tab3_model_combo_to_header" in source
    assert "def _apply_header_ai_model_to_tab3" in source
    assert "getattr(widget, \"_model_combo\", None)" in source


if __name__ == "__main__":
    test_docstring_assistant_uses_header_ai_template_group()
    test_docstring_header_group_binds_after_safe_mode_radio()
    test_docstring_header_model_selector_sync_helpers_exist()
    print("Tab 3 Docstring Assistant header AI group tests passed.")
