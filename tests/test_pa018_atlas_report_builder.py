"""Tests for PA018 Project Symbol Atlas report builder."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.atlas_report_builder import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_BUILT,
    PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_WRITTEN,
    ProjectSymbolAtlasReportBuilderOptions,
    build_reasoner_symbol_atlas_reports,
    write_reasoner_symbol_atlas_reports,
)


def _write_demo_project(project_root: Path) -> None:
    package_dir = project_root / "demo_package"
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "__init__.py").write_text("", encoding="utf-8", newline="\n")
    (package_dir / "service.py").write_text(
        "def existing_target():\n"
        "    return 'ok'\n",
        encoding="utf-8",
        newline="\n",
    )


def test_pa018_builds_selected_reports_without_writing() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _write_demo_project(project_root)
        options = ProjectSymbolAtlasReportBuilderOptions(
            project_root=str(project_root),
            symbol_name="existing_target",
            query_text="existing_target",
            exact=True,
            include_workbench=False,
        )
        result = build_reasoner_symbol_atlas_reports(options)
        assert result.status == PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_BUILT
        assert len(result.reports) == 3
        assert not result.written_reports
        summaries = [report.to_dict()["summary"] for report in result.reports]
        assert any("Existing code finder" in item for item in summaries)
        assert any("Evidence freshness" in item for item in summaries)
        assert any("Live plus JSON" in item for item in summaries)


def test_pa018_writes_reports_to_requested_output_dir() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _write_demo_project(project_root)
        output_dir = project_root / "atlas_reports"
        options = ProjectSymbolAtlasReportBuilderOptions(
            project_root=str(project_root),
            output_dir=str(output_dir),
            symbol_name="existing_target",
            query_text="existing_target",
            exact=True,
            include_freshness_report=False,
            include_merge_report=False,
        )
        result = write_reasoner_symbol_atlas_reports(options)
        assert result.status == PROJECT_SYMBOL_ATLAS_REPORT_BUILDER_STATUS_WRITTEN
        assert len(result.reports) == 1
        assert len(result.written_reports) == 1
        written = result.written_reports[0]
        assert written.json_path.exists()
        assert written.markdown_path.exists()
        assert str(output_dir) in str(written.json_path)


def main() -> int:
    test_pa018_builds_selected_reports_without_writing()
    test_pa018_writes_reports_to_requested_output_dir()
    print("PA018 Atlas report builder tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
