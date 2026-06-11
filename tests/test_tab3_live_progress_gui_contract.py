"""Source contract tests for Tab 3 live progress GUI wiring."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_worker_and_run_controls_wire_progress_signal() -> None:
    """The worker should send file progress to the run-controls facade."""
    worker_source = _read(
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_gui_help/worker_thread.py"
    )
    run_controls_source = _read(
        'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
        "insert_missing_docstrings_gui_help/run_controls.py"
    )
    assert "progress_ready = Signal(dict)" in worker_source
    assert "progress_callback" in worker_source
    assert "handle_worker_progress" in run_controls_source


def test_helper_manifest_exports_new_run_control_contracts() -> None:
    """Helper manifest exports should stay aligned with run_controls.__all__."""
    manifest = json.loads(
        _read(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_gui_help.json"
        )
    )
    exports = manifest["helpers"]["run_controls.py"]["exports"]
    assert "handle_worker_progress" in exports
    assert "stop_running_selected_mode" in exports


def test_review_support_accepts_suggested_docstring_field() -> None:
    """The manual review surface should treat suggested_docstring as report text."""
    source = _read('ask_' 'ai_project_reasoner' '/tab3_manual_review_runtime/review_support.py')
    assert '"suggested_docstring"' in source


if __name__ == "__main__":
    test_worker_and_run_controls_wire_progress_signal()
    test_helper_manifest_exports_new_run_control_contracts()
    test_review_support_accepts_suggested_docstring_field()
    print("Tab 3 live progress GUI contract tests passed.")
