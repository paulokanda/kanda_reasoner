"""Focused tests for the GA001 release notes generator."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.governance_automation import release_notes_generator
from kanda_reasoner_app.governance_automation.release_notes_generator import (
    GA_RELEASE_NOTE_STATUS_VALUES,
    GovernanceReleaseNoteInput,
    build_release_notes_report,
    default_release_notes_dir,
    render_release_notes_markdown,
)


def test_release_notes_report_uses_structured_evidence() -> None:
    item = GovernanceReleaseNoteInput(
        title="Add Risk Change Radar",
        bundle_name="ES002_risk_change_radar.zip",
        summary="Adds read-only risk analysis.",
        changed_files=('ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py',),
        validation_lines=("Architecture: No validation issues",),
        status="validated",
    )

    report = build_release_notes_report("Engineering Safety updates", [item], "validated")
    data = report.to_dict()

    assert data["title"] == "Engineering Safety updates"
    assert data["status"] == "validated"
    assert data["items"][0]["bundle_name"] == "ES002_risk_change_radar.zip"
    assert data["items"][0]["status"] == "validated"

    markdown = render_release_notes_markdown(report)
    assert "# Engineering Safety updates" in markdown
    assert "ES002_risk_change_radar.zip" in markdown
    assert "Architecture: No validation issues" in markdown


def test_release_notes_defaults_are_safe() -> None:
    item = GovernanceReleaseNoteInput(title="")
    report = build_release_notes_report("", [item], "unknown")

    assert report.title == "Not specified."
    assert report.status == "draft"
    assert report.items[0].status == "draft"
    assert "draft" in GA_RELEASE_NOTE_STATUS_VALUES


def test_release_notes_public_contract_is_directly_imported() -> None:
    assert hasattr(release_notes_generator, "__all__")
    exported = set(release_notes_generator.__all__)
    assert "build_release_notes_report" in exported
    assert "render_release_notes_markdown" in exported
    output_dir = default_release_notes_dir("E:/developer_tools")
    assert output_dir.as_posix().endswith("workbench/release_notes")


if __name__ == "__main__":
    test_release_notes_report_uses_structured_evidence()
    test_release_notes_defaults_are_safe()
    test_release_notes_public_contract_is_directly_imported()
    print("GA001 Release Notes Generator tests passed.")
