"""Source contract for the Refactor Report header template layout."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAZY_TABS = ROOT / "kanda_reasoner_app" / "reasoner_tools_gui_shell" / "lazy_tabs.py"


def _source() -> str:
    """Return the lazy tab host source."""
    return LAZY_TABS.read_text(encoding="utf-8")


def test_refactor_report_hides_loaded_source_row() -> None:
    """Refactor Report should use the header template without LOADED/Source row."""
    source = _source()
    header_set_start = source.index("_HEADER_TEMPLATE_ONLY_SOURCES = {")
    header_set_end = source.index("}", header_set_start)
    block = source[header_set_start:header_set_end]

    assert "_DAILY_REFACTOR_GUI_SOURCE" in block


def test_refactor_report_installs_header_ai_group() -> None:
    """Refactor Report should receive the template AI model + refresh group."""
    source = _source()
    install_start = source.index("if spec.source_hint in {")
    install_end = source.index("outer.addLayout(self.header_row)")
    block = source[install_start:install_end]

    assert "_DAILY_REFACTOR_GUI_SOURCE" in block
    assert "self.tab_header_template.install_ai_group_blueprint" in block


def test_refactor_report_moves_project_root_and_hides_mode_a_group() -> None:
    """The old Mode A project-files group should be removed from the body."""
    source = _source()

    assert "def _move_refactor_report_project_root_controls_to_header_row" in source
    assert "def _hide_refactor_report_mode_a_group" in source
    assert '"Select Project Folder"' in source
    assert 'browse_button.setText("browse project folder")' in source
    assert '"Mode A: from project files"' in source

    load_start = source.index("def load_tool")
    load_block = source[load_start:]
    assert "self._move_refactor_report_project_root_controls_to_header_row(widget)" in load_block


if __name__ == "__main__":
    test_refactor_report_hides_loaded_source_row()
    test_refactor_report_installs_header_ai_group()
    test_refactor_report_moves_project_root_and_hides_mode_a_group()
    print("Refactor Report header template tests passed.")
