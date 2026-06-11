"""Tests for PA007E Project Analysis Evidence producer status."""

from __future__ import annotations

import tempfile
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.evidence_producer_status import (
    PROJECT_ANALYSIS_EVIDENCE_STATUS_OK,
    collect_project_analysis_evidence_producer_status,
    format_project_analysis_evidence_producer_status_markdown,
    write_project_analysis_evidence_producer_status_report,
)


def _make_fake_tab5_owner(project_root: Path) -> None:
    owner = (
        project_root
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_tools_gui_shell"
        / "main_window_help"
        / "window_output_paths.py"
    )
    owner.parent.mkdir(parents=True, exist_ok=True)
    owner.write_text(
        "from kanda_reasoner_app.project_analysis_evidence_paths import "
        "analysis_json_parts_dir, parts_manifest_file_path, parts_index_file_path\n\n"
        "def _json_splitted_dir(project_root):\n"
        "    return analysis_json_parts_dir(project_root)\n\n"
        "def _split_manifest_file(project_root):\n"
        "    return parts_manifest_file_path(project_root)\n\n"
        "def _split_index_file(project_root):\n"
        "    return parts_index_file_path(project_root)\n",
        encoding="utf-8",
    )


def test_pa007e_status_paths_are_canonical_and_dynamic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp) / "future_project"
        project_root.mkdir()
        _make_fake_tab5_owner(project_root)

        status = collect_project_analysis_evidence_producer_status(project_root)
        assert status.status == PROJECT_ANALYSIS_EVIDENCE_STATUS_OK
        assert status.canonical_paths_ok is True
        assert status.tab4_outputs_canonical is True
        assert status.tab5_outputs_canonical is True
        assert status.tab5_window_helpers_detected is True
        assert "project_analysis_evidence" in status.primary_complete_json
        assert "project_analysis_evidence" in status.split_manifest_json
        assert "_project_reference" not in status.primary_complete_json
        assert "_project_reference" not in status.split_manifest_json


def test_pa007e_status_report_writes_json_and_markdown() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp) / "future_project"
        project_root.mkdir()
        _make_fake_tab5_owner(project_root)
        output_dir = project_root / "reports"

        json_path, markdown_path = write_project_analysis_evidence_producer_status_report(
            project_root,
            output_dir=output_dir,
        )
        assert json_path.exists()
        assert markdown_path.exists()
        assert "project_analysis_evidence" in json_path.read_text(encoding="utf-8")
        markdown = markdown_path.read_text(encoding="utf-8")
        assert "Project Analysis Evidence Producer Status" in markdown
        assert "Tab 4 outputs canonical: True" in markdown
        assert "Tab 5 outputs canonical: True" in markdown


def test_pa007e_markdown_is_plain_text() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp) / "future_project"
        project_root.mkdir()
        _make_fake_tab5_owner(project_root)
        status = collect_project_analysis_evidence_producer_status(project_root)
        markdown = format_project_analysis_evidence_producer_status_markdown(status)
        assert "# Project Analysis Evidence Producer Status" in markdown
        assert "Tab 5 helper evidence detected: True" in markdown


def main() -> int:
    test_pa007e_status_paths_are_canonical_and_dynamic()
    test_pa007e_status_report_writes_json_and_markdown()
    test_pa007e_markdown_is_plain_text()
    print("PA007E Project Analysis Evidence producer status tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
