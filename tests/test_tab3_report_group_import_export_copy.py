"""Contract tests for Tab 3 report save, load, and copy controls."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAYOUT = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime" / "layout_runtime.py"
REPORT_IO = ROOT / 'ask_' 'ai_project_reasoner' / "tab3_manual_review_runtime" / "report_io_runtime.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_report_group_has_real_buttons() -> None:
    """Report group exposes save, load, and copy buttons."""
    source = _read(LAYOUT)
    assert 'QGroupBox("Report")' in source
    assert 'QPushButton("Save report")' in source
    assert 'QPushButton("Load report")' in source
    assert 'QPushButton("Copy report")' in source
    assert "window._save_report_button" in source
    assert "window._load_report_button" in source
    assert "window._copy_report_button" in source


def test_report_group_wires_buttons_to_report_io_runtime() -> None:
    """Report buttons are wired through the Tab 3 report IO runtime boundary."""
    source = _read(LAYOUT)
    assert '_report_io_slot(window, "save_report")' in source
    assert '_report_io_slot(window, "load_report")' in source
    assert '_report_io_slot(window, "copy_report")' in source
    assert "tab3_manual_review_runtime.report_io_runtime" in source


def test_report_io_runtime_has_required_actions() -> None:
    """Report IO runtime implements the three user-facing report actions."""
    source = _read(REPORT_IO)
    assert "def save_report(owner: object) -> None:" in source
    assert "def load_report(owner: object) -> None:" in source
    assert "def copy_report(owner: object) -> None:" in source
    assert "REPORT_IO_PREFS_NAME" in source
    assert "_remember_folder" in source
    assert "_default_external_folder" in source


if __name__ == "__main__":
    test_report_group_has_real_buttons()
    test_report_group_wires_buttons_to_report_io_runtime()
    test_report_io_runtime_has_required_actions()
    print("Tab 3 report import/export/copy contract tests passed.")
