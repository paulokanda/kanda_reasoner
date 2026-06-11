"""Focused tests for PA008 complete JSON atlas adapter."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.complete_json_adapter import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_JSON,
    PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_SECTIONS,
    PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_READY,
    ProjectSymbolAtlasCompleteJsonOptions,
    build_reasoner_symbol_atlas_complete_json_report,
    collect_reasoner_symbol_atlas_complete_json_files,
    summarize_reasoner_symbol_atlas_complete_json,
)


def _write_complete_json(project_root: Path, payload: dict[str, object]) -> Path:
    evidence_dir = project_root / "project_analysis_evidence" / "json_complete"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    path = evidence_dir / "sample_project__complete.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8", newline="\n")
    return path


def _sample_payload() -> dict[str, object]:
    return {
        "source_file_index": {
            "pkg/main.py": {
                "file": "pkg/main.py",
                "module_name": "pkg.main",
                "line_count": 12,
            }
        },
        "symbol_index": {
            "run_app": {
                "file": "pkg/main.py",
                "kind": "function",
                "line": 5,
            }
        },
        "primary_definition_index": {
            "run_app": {
                "primary": {
                    "file": "pkg/main.py",
                    "kind": "function",
                    "line_start": 5,
                }
            }
        },
        "duplicate_symbols": [
            {"symbol_name": "run_app", "occurrences": ["pkg/main.py"]}
        ],
        "web_ai_symbol_index": {
            "run_app": {
                "file": "pkg/main.py",
                "kind": "function",
                "line_start": 5,
                "module_name": "pkg.main",
                "qualified_name": "run_app",
            }
        },
        "web_ai_file_responsibility_index": {
            "pkg/main.py": {
                "owner_box": "runtime",
                "primary_responsibility": "Application entry logic",
            }
        },
    }


def test_pa008_missing_json_is_reported_without_writes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        summary = summarize_reasoner_symbol_atlas_complete_json(root)
        assert summary.status == PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_JSON
        assert not (root / "project_analysis_evidence").exists()


def test_pa008_collects_complete_json_from_canonical_subfolder() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        json_path = _write_complete_json(root, _sample_payload())
        candidates = collect_reasoner_symbol_atlas_complete_json_files(root)
        assert candidates == (json_path,)


def test_pa008_summarizes_complete_json_sections() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        json_path = _write_complete_json(root, _sample_payload())
        summary = summarize_reasoner_symbol_atlas_complete_json(root, json_path=json_path)
        assert summary.status == PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_READY
        assert summary.source_file_count == 1
        assert summary.symbol_count == 1
        assert summary.primary_definition_count == 1
        assert summary.duplicate_symbol_count == 1
        assert not summary.missing_sections


def test_pa008_reports_missing_required_sections() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        json_path = _write_complete_json(root, {"source_file_index": {}})
        summary = summarize_reasoner_symbol_atlas_complete_json(root, json_path=json_path)
        assert summary.status == PROJECT_SYMBOL_ATLAS_COMPLETE_JSON_STATUS_MISSING_SECTIONS
        assert "symbol_index" in summary.missing_sections
        assert "primary_definition_index" in summary.missing_sections


def test_pa008_builds_reasoner_symbol_atlas_report() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        json_path = _write_complete_json(root, _sample_payload())
        report = build_reasoner_symbol_atlas_complete_json_report(
            ProjectSymbolAtlasCompleteJsonOptions(
                project_root=str(root),
                json_path=str(json_path),
                max_modules=10,
                max_symbols=10,
            )
        )
        data = report.to_dict()
        assert data["report_type"] == "reasoner_symbol_atlas"
        assert data["module_count"] == 1
        assert data["symbol_count"] == 1
        assert "status=complete_json_ready" in data["summary"]


def main() -> int:
    test_pa008_missing_json_is_reported_without_writes()
    test_pa008_collects_complete_json_from_canonical_subfolder()
    test_pa008_summarizes_complete_json_sections()
    test_pa008_reports_missing_required_sections()
    test_pa008_builds_reasoner_symbol_atlas_report()
    print("PA008 Complete JSON Atlas adapter tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
