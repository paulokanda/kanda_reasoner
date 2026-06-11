"""Regression tests for Tab 3 live audit progress and final report output."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
from pathlib import Path

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings import run
from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_help.file_processing import (
    collect_changes,
)


def _write_sample_project(root: Path) -> None:
    package = root / "sample_package"
    package.mkdir()
    (package / "module_a.py").write_text(
        "def needs_docstring(value):\n"
        "    return value + 1\n",
        encoding="utf-8",
    )


def test_collect_changes_emits_file_progress_and_suggested_docstring() -> None:
    """Progress callbacks should report total, audited, and remaining files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_sample_project(root)
        progress: list[dict[str, object]] = []

        _changes, _skipped, rows, telemetry = collect_changes(
            root,
            include_module=True,
            include_classes=True,
            include_functions=True,
            include_init=False,
            include_relaxed_paths=False,
            include_tests=False,
            insert_file_address_at_top=False,
            workers=1,
            progress_callback=progress.append,
        )

    assert telemetry["files_selected"] == 1
    assert progress[0] == {
        "total_files_to_audit": 1,
        "files_audited": 0,
        "files_to_go": 1,
    }
    assert progress[-1] == {
        "total_files_to_audit": 1,
        "files_audited": 1,
        "files_to_go": 0,
    }
    inserted_rows = [row for row in rows if row.get("action") == "inserted"]
    assert inserted_rows
    assert any(str(row.get("suggested_docstring", "")).strip() for row in inserted_rows)


def test_scan_replaces_live_progress_with_final_real_output_contract() -> None:
    """Scan mode should still print the final JSON report after progress updates."""
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write_sample_project(root)
        report_path = root / "report.jsonl"
        progress: list[dict[str, object]] = []
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exit_code = run(
                root,
                "scan",
                include_module=True,
                include_classes=True,
                include_functions=True,
                report_path=str(report_path),
                workers=1,
                progress_callback=progress.append,
            )
        output = buffer.getvalue()

    assert exit_code == 0
    assert progress
    summary = json.loads(output)
    assert summary["files_with_missing_docstrings"] >= 1
    assert summary["files"]
    assert report_path.name == "report.jsonl"


if __name__ == "__main__":
    test_collect_changes_emits_file_progress_and_suggested_docstring()
    test_scan_replaces_live_progress_with_final_real_output_contract()
    print("Tab 3 live audit progress contract tests passed.")
