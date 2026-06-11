"""Report writer helpers for source hygiene outputs."""

from __future__ import annotations

import json
from pathlib import Path

from .schemas import SourceHygieneReport, SourceHygieneWriteResult

__all__ = [
    "default_source_hygiene_report_dir",
    "write_source_hygiene_report",
]


def default_source_hygiene_report_dir(project_root: str | Path) -> Path:
    """Return the default output folder for source hygiene reports."""
    return Path(project_root) / "workbench" / "source_hygiene_reports"


def write_source_hygiene_report(
    report: SourceHygieneReport,
    output_dir: str | Path | None = None,
) -> SourceHygieneWriteResult:
    """Write a source hygiene report as JSON and Markdown."""
    data = report.to_dict()
    target_dir = Path(output_dir) if output_dir else default_source_hygiene_report_dir(
        report.project_root
    )
    target_dir.mkdir(parents=True, exist_ok=True)

    stem = str(data["report_id"])
    json_path = target_dir / (stem + ".json")
    markdown_path = target_dir / (stem + ".md")

    json_path.write_text(
        json.dumps(data, indent=2, sort_keys=True),
        encoding="utf-8",
        newline="\n",
    )
    markdown_path.write_text(_format_markdown_report(data), encoding="utf-8", newline="\n")

    return SourceHygieneWriteResult(json_path=json_path, markdown_path=markdown_path)


def _format_markdown_report(data: dict[str, object]) -> str:
    """Format a source hygiene report as Markdown text."""
    lines: list[str] = []
    lines.append("# Source Hygiene Report")
    lines.append("")
    lines.append("- report_id: " + str(data.get("report_id", "")))
    lines.append("- report_type: " + str(data.get("report_type", "")))
    lines.append("- created_at: " + str(data.get("created_at", "")))
    lines.append("- project_root: " + str(data.get("project_root", "")))
    lines.append("- finding_count: " + str(data.get("finding_count", 0)))
    lines.append("")
    summary = str(data.get("summary", "")).strip()
    if summary:
        lines.append("## Summary")
        lines.append("")
        lines.append(summary)
        lines.append("")

    lines.append("## Findings")
    lines.append("")
    findings = data.get("findings", [])
    if not isinstance(findings, list) or not findings:
        lines.append("No findings.")
        lines.append("")
        return "\n".join(lines)

    for index, finding in enumerate(findings, start=1):
        if not isinstance(finding, dict):
            continue
        lines.append("### " + str(index) + ". " + str(finding.get("code", "finding")))
        lines.append("")
        lines.append("- path: " + str(finding.get("path", "")))
        lines.append("- line: " + str(finding.get("line", "")))
        lines.append("- severity: " + str(finding.get("severity", "")))
        lines.append("- confidence: " + str(finding.get("confidence", "")))
        lines.append("")
        lines.append(str(finding.get("message", "")))
        action = str(finding.get("suggested_action", "")).strip()
        if action:
            lines.append("")
            lines.append("Suggested action: " + action)
        lines.append("")
    return "\n".join(lines)
