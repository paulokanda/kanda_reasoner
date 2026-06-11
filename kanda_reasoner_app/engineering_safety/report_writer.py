"""Writers for Engineering Safety JSON and Markdown reports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import EngineeringSafetyReport

__all__ = [
    "default_engineering_safety_report_dir",
    "engineering_safety_report_stem",
    "format_engineering_safety_markdown",
    "write_engineering_safety_report",
]


def default_engineering_safety_report_dir(project_root: str | Path) -> Path:
    """Return the default Engineering Safety report output folder."""
    return Path(project_root) / "workbench" / "engineering_safety_reports"


def engineering_safety_report_stem(report: EngineeringSafetyReport) -> str:
    """Return a filesystem-safe report stem."""
    timestamp = report.created_at.replace(":", "").replace("+", "_")
    timestamp = timestamp.replace("-", "").replace("T", "_")
    return timestamp + "_" + report.report_type + "_" + report.report_id[-12:]


def _format_list(values: list[str]) -> str:
    if not values:
        return "- none"
    return "\n".join("- " + value for value in values)


def format_engineering_safety_markdown(report: EngineeringSafetyReport) -> str:
    """Format an Engineering Safety report as Markdown."""
    lines = [
        "# Engineering Safety Report",
        "",
        "Report ID: " + report.report_id,
        "Report type: " + report.report_type,
        "Created at: " + report.created_at,
        "Project root: " + report.project_root,
        "Risk level: " + report.risk_level,
        "Confidence: " + report.confidence,
        "Owning box: " + (report.owning_box or "unknown"),
        "",
        "## Input sources",
        _format_list(report.input_sources),
        "",
        "## Affected files",
        _format_list(report.affected_files),
        "",
        "## Root cause or risk hypothesis",
        report.root_cause_or_risk_hypothesis or "Not provided.",
        "",
        "## Suggested first action",
        report.suggested_first_action or "Not provided.",
        "",
        "## Tests to run",
        _format_list(report.tests_to_run),
        "",
        "## Rollback plan",
        report.rollback_plan or "Not provided.",
        "",
        "## Evidence",
        _format_list(report.evidence),
        "",
        "## Review state",
        "Human decision: " + report.human_decision,
        "Validation status: " + report.validation_status,
        "",
    ]
    return "\n".join(lines)


def write_engineering_safety_report(
    report: EngineeringSafetyReport,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Write an Engineering Safety report as JSON and Markdown."""
    target_dir = Path(output_dir) if output_dir is not None else default_engineering_safety_report_dir(
        report.project_root
    )
    target_dir.mkdir(parents=True, exist_ok=True)
    stem = engineering_safety_report_stem(report)
    json_path = target_dir / (stem + ".json")
    markdown_path = target_dir / (stem + ".md")
    json_path.write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True),
        encoding="utf-8",
    )
    markdown_path.write_text(format_engineering_safety_markdown(report), encoding="utf-8")
    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "report_id": report.report_id,
    }
