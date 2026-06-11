from __future__ import annotations

import importlib
import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_symbol_atlas.report_writer as report_writer
import kanda_reasoner_app.reasoner_symbol_atlas.schemas as schemas
from kanda_reasoner_app.reasoner_symbol_atlas import (
    ProjectModuleRecord,
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    ProjectSymbolQuery,
    ProjectSymbolQueryResult,
    default_reasoner_symbol_atlas_report_dir,
    write_reasoner_symbol_atlas_report,
)


def test_schema_public_contract() -> None:
    assert "ProjectSymbolAtlasReport" in schemas.__all__
    assert "write_reasoner_symbol_atlas_report" in report_writer.__all__
    assert (
        schemas.normalize_project_atlas_report_type("symbol_query_result")
        == "symbol_query_result"
    )
    assert schemas.normalize_project_atlas_symbol_kind("function") == "function"
    assert schemas.normalize_project_atlas_owner_role("facade") == "facade"
    assert not hasattr(schemas, "VALID_REPORT_TYPES")
    assert not hasattr(schemas, "VALID_CONFIDENCE")


def test_report_serializes_modules_symbols_and_query_results() -> None:
    symbol = ProjectSymbol(
        name="build_engineering_safety_panel_command",
        kind="function",
        module="reasoner_tools_gui_engineering_safety_panel",
        path="reasoner_tools_gui_engineering_safety_panel.py",
        line=120,
        is_public=True,
        owner_role="canonical_owner",
        evidence=("Defined by FunctionDef",),
    )
    module = ProjectModuleRecord(
        module="reasoner_tools_gui_engineering_safety_panel",
        path="reasoner_tools_gui_engineering_safety_panel.py",
        line_count=480,
        owner_role="canonical_owner",
        symbols=(symbol,),
        imports=("kanda_reasoner_app.safety_suite_cli.commands",),
    )
    query = ProjectSymbolQuery(
        project_root="E:\\developer_tools",
        name="build_engineering_safety_panel_command",
    )
    query_result = ProjectSymbolQueryResult(
        query=query,
        matches=(symbol,),
        summary="One canonical owner found.",
        status="complete",
    )
    report = ProjectSymbolAtlasReport(
        project_root="E:\\developer_tools",
        report_type="reasoner_symbol_atlas",
        summary="Schema smoke report.",
        modules=(module,),
        symbols=(symbol,),
        query_results=(query_result,),
        input_sources=("reasoner_tools_gui_engineering_safety_panel.py",),
    )

    payload = report.to_dict()

    assert payload["report_type"] == "reasoner_symbol_atlas"
    assert payload["module_count"] == 1
    assert payload["symbol_count"] == 1
    assert payload["query_result_count"] == 1
    assert payload["modules"][0]["owner_role"] == "canonical_owner"
    assert payload["symbols"][0]["kind"] == "function"
    assert payload["query_results"][0]["match_count"] == 1


def test_report_writer_creates_json_and_markdown() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir) / "reports"
        symbol = ProjectSymbol(
            name="TOOLS",
            kind="constant",
            module="kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs",
            path='ask_' 'ai_project_reasoner' '/reasoner_tools_gui_shell/tool_specs.py',
            owner_role="canonical_owner",
        )
        report = ProjectSymbolAtlasReport(
            project_root=temp_dir,
            report_type="owner_map",
            summary="Owner map foundation.",
            symbols=(symbol,),
        )
        result = write_reasoner_symbol_atlas_report(report, output_dir=output_dir)
        assert result.json_path.exists()
        assert result.markdown_path.exists()
        loaded = json.loads(result.json_path.read_text(encoding="utf-8"))
        markdown = result.markdown_path.read_text(encoding="utf-8")
        assert loaded["report_type"] == "owner_map"
        assert loaded["symbol_count"] == 1
        assert "# Project Symbol Atlas Report" in markdown
        assert "TOOLS" in markdown
        assert default_reasoner_symbol_atlas_report_dir(temp_dir).name == (
            "reasoner_symbol_atlas_reports"
        )


def test_public_contract_exports_are_directly_importable() -> None:
    package = importlib.import_module("kanda_reasoner_app.reasoner_symbol_atlas")

    for name in package.__all__:
        assert hasattr(package, name), name

    for name in schemas.__all__:
        assert hasattr(schemas, name), name

    for name in report_writer.__all__:
        assert hasattr(report_writer, name), name


if __name__ == "__main__":
    test_schema_public_contract()
    test_report_serializes_modules_symbols_and_query_results()
    test_report_writer_creates_json_and_markdown()
    test_public_contract_exports_are_directly_importable()
    print("PA001 Project Symbol Atlas schema tests passed.")
