"""Tests for project-prefixed complete JSON selection in Tab 8 atlas code."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT_FOR_IMPORTS))

from kanda_reasoner_app.reasoner_symbol_atlas.complete_json_adapter import (
    PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_READY,
    collect_reasoner_symbol_atlas_complete_json_files,
    expected_reasoner_symbol_atlas_complete_json_name,
    summarize_reasoner_symbol_atlas_complete_json,
)


def _write_complete_json(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source_file_index": {},
        "symbol_index": {},
        "primary_definition_index": {},
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_prefers_current_project_prefixed_complete_json_over_newer_fallback() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "developer_tools"
        json_complete_dir = project_root / "project_analysis_evidence" / "json_complete"
        expected_path = json_complete_dir / "developer_tools__complete.json"
        other_path = json_complete_dir / "other_project__complete.json"
        runtime_trace_path = json_complete_dir / "developer_tools__complete_runtime_trace.json"
        split_path = project_root / "project_analysis_evidence" / "json_splitted" / "developer_tools_part_001.json"

        _write_complete_json(expected_path)
        _write_complete_json(other_path)
        _write_complete_json(runtime_trace_path)
        _write_complete_json(split_path)

        os.utime(expected_path, (100.0, 100.0))
        os.utime(other_path, (200.0, 200.0))

        candidates = collect_reasoner_symbol_atlas_complete_json_files(project_root)

        assert candidates
        assert candidates[0] == expected_path
        assert other_path in candidates
        assert runtime_trace_path not in candidates
        assert split_path not in candidates
        assert expected_reasoner_symbol_atlas_complete_json_name(project_root) == "developer_tools__complete.json"


def test_summary_uses_current_project_prefixed_complete_json() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "developer_tools"
        json_complete_dir = project_root / "project_analysis_evidence" / "json_complete"
        expected_path = json_complete_dir / "developer_tools__complete.json"
        other_path = json_complete_dir / "other_project__complete.json"

        _write_complete_json(expected_path)
        _write_complete_json(other_path)
        os.utime(expected_path, (100.0, 100.0))
        os.utime(other_path, (200.0, 200.0))

        summary = summarize_reasoner_symbol_atlas_complete_json(project_root)

        assert summary.status == PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_READY
        assert Path(summary.json_path) == expected_path
        assert "Selected complete JSON matches the current project prefix." in summary.notes


def test_falls_back_to_other_complete_json_when_project_prefixed_file_is_missing() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "developer_tools"
        json_complete_dir = project_root / "project_analysis_evidence" / "json_complete"
        fallback_path = json_complete_dir / "other_project__complete.json"

        _write_complete_json(fallback_path)

        summary = summarize_reasoner_symbol_atlas_complete_json(project_root)

        assert summary.status == PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_READY
        assert Path(summary.json_path) == fallback_path
        assert "Selected complete JSON is a fallback match, not the current project prefix." in summary.notes


def main() -> int:
    test_prefers_current_project_prefixed_complete_json_over_newer_fallback()
    test_summary_uses_current_project_prefixed_complete_json()
    test_falls_back_to_other_complete_json_when_project_prefixed_file_is_missing()
    print("PA025 project-prefixed complete JSON selection tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
