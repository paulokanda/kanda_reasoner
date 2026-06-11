"""PA029 tests for complete JSON active-scope quality reporting."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.atlas_report_builder import (  # noqa: E402
    ProjectSymbolAtlasReportBuilderOptions,
    build_reasoner_symbol_atlas_reports,
)
from kanda_reasoner_app.reasoner_symbol_atlas.json_active_scope_quality import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_ACTIVE_LEAK,
    PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_CLEAN,
    PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_TEXT_ONLY,
    ProjectSymbolAtlasJsonActiveScopeQualityOptions,
    build_reasoner_symbol_atlas_json_active_scope_report,
    check_reasoner_symbol_atlas_json_active_scope_quality,
)


def _write_complete_json(project_root: Path, payload: dict) -> Path:
    path = (
        project_root
        / "project_analysis_evidence"
        / "json_complete"
        / "sample__complete.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _base_payload(project_root: Path) -> dict:
    return {
        "collector_info": {"project_root": str(project_root), "generated_at": "2026-06-05T00:00:00+00:00"},
        "project_summary": {"project_root": str(project_root)},
        "source_file_index": {
            'ask_' 'ai_project_reasoner' '/active.py': {
                "file": 'ask_' 'ai_project_reasoner' '/active.py',
                "full_source": "x = 1\n",
            }
        },
        "symbol_index": {
            "active_symbol": {
                "file": 'ask_' 'ai_project_reasoner' '/active.py',
                "kind": "function",
            }
        },
        "primary_definition_index": {
            "active_symbol": 'ask_' 'ai_project_reasoner' '/active.py',
        },
    }


def test_pa029_clean_complete_json_reports_clean() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        json_path = _write_complete_json(project_root, _base_payload(project_root))

        summary = check_reasoner_symbol_atlas_json_active_scope_quality(
            ProjectSymbolAtlasJsonActiveScopeQualityOptions(
                project_root=str(project_root),
                json_path=str(json_path),
            )
        )

        assert summary.status == PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_CLEAN
        assert summary.active_path_occurrence_count == 0
        assert summary.text_occurrence_count == 0


def test_pa029_source_text_mentions_are_not_active_leaks() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        payload = _base_payload(project_root)
        payload["source_file_index"]['ask_' 'ai_project_reasoner' '/active.py']["full_source"] = (
            "NOTE = '_project_reference/memo.py'\n"
        )
        payload["edit_ready_symbol_index"] = {
            "active_symbol": {
                "source_excerpt": "open('_project_reference/memo.py')",
            }
        }
        payload["documentation_intent"] = {
            "documentation_evidence": [
                {"value_excerpt": "python _project_reference/manual_note.py"},
            ]
        }
        json_path = _write_complete_json(project_root, payload)

        summary = check_reasoner_symbol_atlas_json_active_scope_quality(
            ProjectSymbolAtlasJsonActiveScopeQualityOptions(
                project_root=str(project_root),
                json_path=str(json_path),
            )
        )

        assert summary.status == PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_TEXT_ONLY
        assert summary.active_path_occurrence_count == 0
        assert summary.text_occurrence_count >= 3


def test_pa029_active_path_fields_are_reported_as_leaks() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        payload = _base_payload(project_root)
        payload["source_file_index"]["_project_reference/memo.py"] = {
            "file": "_project_reference/memo.py",
        }
        payload["primary_definition_index"]["memo_symbol"] = "_project_reference/memo.py"
        payload["web_ai_test_protection_index"] = {
            "memo_symbol": {
                "test_to_run": "python tests_archive/test_memo.py",
            }
        }
        json_path = _write_complete_json(project_root, payload)

        summary = check_reasoner_symbol_atlas_json_active_scope_quality(
            ProjectSymbolAtlasJsonActiveScopeQualityOptions(
                project_root=str(project_root),
                json_path=str(json_path),
            )
        )

        assert summary.status == PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_ACTIVE_LEAK
        assert summary.active_path_occurrence_count >= 3
        active_types = {item.occurrence_type for item in summary.active_occurrences}
        assert "active_path_key" in active_types
        assert "active_path_field" in active_types or "active_index_path_value" in active_types


def test_pa029_report_builder_adds_json_quality_report() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        json_path = _write_complete_json(project_root, _base_payload(project_root))

        result = build_reasoner_symbol_atlas_reports(
            ProjectSymbolAtlasReportBuilderOptions(
                project_root=str(project_root),
                json_path=str(json_path),
                include_existing_code_report=False,
                include_freshness_report=False,
                include_merge_report=False,
                include_json_quality_report=True,
            )
        )

        assert result.status == "built"
        assert len(result.reports) == 1
        assert "JSON active-scope quality status=clean" in result.reports[0].summary
        assert "Built complete-JSON active-scope quality report." in result.notes


def test_pa029_quality_report_uses_public_contract() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        json_path = _write_complete_json(project_root, _base_payload(project_root))

        report = build_reasoner_symbol_atlas_json_active_scope_report(
            ProjectSymbolAtlasJsonActiveScopeQualityOptions(
                project_root=str(project_root),
                json_path=str(json_path),
            )
        )

        data = report.to_dict()
        assert data["report_type"] == "reasoner_symbol_atlas"
        assert "active_path_occurrences=0" in data["summary"]
        assert "json_active_scope_quality" in data["input_sources"]


def main() -> int:
    test_pa029_clean_complete_json_reports_clean()
    test_pa029_source_text_mentions_are_not_active_leaks()
    test_pa029_active_path_fields_are_reported_as_leaks()
    test_pa029_report_builder_adds_json_quality_report()
    test_pa029_quality_report_uses_public_contract()
    print("PA029 JSON active-scope quality tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
