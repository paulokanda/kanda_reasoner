from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.source_hygiene.report_writer as source_hygiene_report_writer
import kanda_reasoner_app.source_hygiene.schemas as source_hygiene_schemas
from kanda_reasoner_app.source_hygiene import (
    SourceHygieneFinding,
    SourceHygieneReport,
    default_source_hygiene_report_dir,
    write_source_hygiene_report,
)


def test_schema_public_contract() -> None:
    assert "SourceHygieneReport" in source_hygiene_schemas.__all__
    assert "write_source_hygiene_report" in source_hygiene_report_writer.__all__
    assert source_hygiene_schemas.normalize_report_type("bom_scan") == "bom_scan"
    assert source_hygiene_schemas.normalize_severity("warning") == "warning"
    assert source_hygiene_schemas.normalize_confidence("high") == "high"


def test_report_serializes_findings() -> None:
    finding = SourceHygieneFinding(
        code="BOM_PRESENT",
        path="example.py",
        line=1,
        severity="warning",
        confidence="high",
        message="UTF-8 BOM detected.",
        suggested_action="Remove BOM after backup.",
    )
    report = SourceHygieneReport(
        project_root="E:\\developer_tools",
        report_type="bom_scan",
        summary="One BOM finding.",
        findings=(finding,),
        input_sources=("example.py",),
    )
    data = report.to_dict()
    assert data["report_type"] == "bom_scan"
    assert data["finding_count"] == 1
    assert data["findings"][0]["code"] == "BOM_PRESENT"
    assert data["findings"][0]["severity"] == "warning"


def test_report_writer_outputs_json_and_markdown() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir) / "reports"
        report = SourceHygieneReport(
            project_root=temp_dir,
            report_type="shadow_conflict_audit",
            summary="No findings.",
            findings=(),
        )
        result = write_source_hygiene_report(report, output_dir=output_dir)
        assert result.json_path.exists()
        assert result.markdown_path.exists()
        loaded = json.loads(result.json_path.read_text(encoding="utf-8"))
        assert loaded["report_type"] == "shadow_conflict_audit"
        assert loaded["finding_count"] == 0
        assert "Source Hygiene Report" in result.markdown_path.read_text(encoding="utf-8")
        assert default_source_hygiene_report_dir(temp_dir).name == "source_hygiene_reports"


if __name__ == "__main__":
    test_schema_public_contract()
    test_report_serializes_findings()
    test_report_writer_outputs_json_and_markdown()
    print("SH001C Source Hygiene Doctor test import repair passed.")
