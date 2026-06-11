"""JSONCTX014A/014B focused regression for lazy tab load error isolation."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "lazy_tabs.py"


def test_lazy_tab_load_tool_reports_error_without_closing_gui() -> None:
    """Ensure lazy tab import failures are displayed without closing the GUI."""
    source = SOURCE_PATH.read_text(encoding="utf-8")
    error_panel_marker = "ToolLoadErrorPanel("
    status_marker = 'self.status_label.setText("FAILED TO LOAD")'
    old_reraise_marker = "            self._loaded = True\n            raise\n"
    typed_failure_marker = "            self._loaded = True\n            return False\n"

    assert error_panel_marker in source
    assert status_marker in source
    assert old_reraise_marker not in source
    assert typed_failure_marker in source


def main() -> int:
    test_lazy_tab_load_tool_reports_error_without_closing_gui()
    print("JSONCTX014A lazy tab load error isolation tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
