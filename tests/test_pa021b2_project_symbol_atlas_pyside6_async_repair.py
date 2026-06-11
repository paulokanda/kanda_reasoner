"""Tests for PA021B2 Project Symbol Atlas PySide6 async repair."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "reasoner_tools_gui_engineering_safety_panel.py"


def _read_panel() -> str:
    return PANEL.read_text(encoding="utf-8", errors="replace")


def test_pa021b2_pyside6_async_runner_is_installed() -> None:
    text = _read_panel()
    assert "# BEGIN PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER" in text
    assert "# END PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER" in text
    assert "ThreadPoolExecutor(max_workers=1)" in text
    assert "from PySide6.QtCore import QTimer" in text
    assert "QTimer.singleShot" in text
    assert "command_executor.submit(" in text
    assert "tkinter" not in text.lower()


def test_pa021b2_ui_slot_does_not_run_atlas_command_directly() -> None:
    text = _read_panel()
    marker_start = text.index("# BEGIN PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER")
    marker_end = text.index("# END PA021B2_ENGINEERING_SAFETY_PYSIDE6_ASYNC_RUNNER")
    block = text[marker_start:marker_end]
    assert "run_engineering_safety_panel_cli_command" in block
    assert "command_executor.submit(" in block
    submit_index = block.index("command_executor.submit(")
    call_index = block.index("run_engineering_safety_panel_cli_command")
    assert submit_index < call_index
    assert "raise RuntimeError" not in block


def main() -> int:
    test_pa021b2_pyside6_async_runner_is_installed()
    test_pa021b2_ui_slot_does_not_run_atlas_command_directly()
    print("PA021B2 Project Symbol Atlas PySide6 async repair tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
