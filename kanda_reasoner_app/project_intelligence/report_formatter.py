# project-path: kanda_reasoner_app/project_intelligence/report_formatter.py
"""Human-readable formatter for Project Intelligence engine reports."""

from __future__ import annotations

from typing import Iterable

from .models import ADVISORY_SOURCE_TRUTH_WARNING, EngineFinding, EngineReport

DEFAULT_VALIDATION_NOTE = "Run the patch-specific validation command before freezing or editing."
STANDARD_SECTION_TITLES = (
    "What this found",
    "Why it matters",
    "What to inspect next",
    "What an AI must not assume",
    "Findings",
    "Warnings",
    "Errors",
    "Suggested validation",
)

__all__ = [
    "DEFAULT_VALIDATION_NOTE",
    "EngineReportFormatter",
    "STANDARD_SECTION_TITLES",
    "format_engine_report",
]


def _clean_text(value: object) -> str:
    """Return compact display text."""
    return " ".join(str(value or "").strip().split())


def _clean_lines(values: Iterable[object] | object | None) -> list[str]:
    """Return non-empty display lines from any iterable or scalar value."""
    if values is None:
        return []
    if isinstance(values, str):
        values = [values]
    try:
        iterator = iter(values)  # type: ignore[arg-type]
    except TypeError:
        iterator = iter([values])
    output: list[str] = []
    for value in iterator:
        text = _clean_text(value)
        if text:
            output.append(text)
    return output


def _bullet_lines(values: Iterable[object] | object | None, empty_text: str) -> list[str]:
    """Return Markdown bullet lines for values, or one empty-state bullet."""
    lines = _clean_lines(values)
    if not lines:
        return ["- " + empty_text]
    return ["- " + item for item in lines]


class EngineReportFormatter:
    """Format advisory Project Intelligence reports for a human reader."""

    def __init__(self, max_findings: int = 25) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        max_findings : int, optional
            The optional max findings value.
        """
        
        self.max_findings = max(1, int(max_findings or 25))

    def format_report(
        self,
        report: EngineReport,
        *,
        title: str = "Project Intelligence Report",
        suggested_validation: Iterable[object] | object | None = None,
    ) -> str:
        """Return a deterministic Markdown report without writing files."""
        if not isinstance(report, EngineReport):
            raise TypeError("report must be an EngineReport")

        report_data = report.to_dict()
        validation_lines = _clean_lines(suggested_validation)
        if not validation_lines:
            validation_lines = [DEFAULT_VALIDATION_NOTE]

        lines: list[str] = [
            "# " + (_clean_text(title) or "Project Intelligence Report"),
            "",
            "Engine: " + str(report_data.get("engine_id", "")),
            "Version: " + str(report_data.get("engine_version", "")),
            "Status: " + str(report_data.get("status", "")),
            "Generated at: " + str(report_data.get("generated_at", "")),
            "Project root label: " + str(report_data.get("project_root_label", "")),
            "",
            "## What this found",
            str(report_data.get("summary") or "No summary was provided."),
            "",
            "## Why it matters",
            ADVISORY_SOURCE_TRUTH_WARNING,
            "",
            "## What to inspect next",
        ]
        lines.extend(_bullet_lines(report_data.get("next_steps"), "Inspect the exact source files before editing."))
        lines.extend(["", "## What an AI must not assume"])
        ai_limits = report_data.get("ai_must_not_assume") or [ADVISORY_SOURCE_TRUTH_WARNING]
        if ADVISORY_SOURCE_TRUTH_WARNING not in ai_limits:
            ai_limits = [ADVISORY_SOURCE_TRUTH_WARNING, *list(ai_limits)]
        lines.extend(_bullet_lines(ai_limits, ADVISORY_SOURCE_TRUTH_WARNING))
        lines.extend(["", "## Findings"])
        lines.extend(self._format_findings(report.findings))
        lines.extend(["", "## Warnings"])
        lines.extend(_bullet_lines(report_data.get("warnings"), "No warnings were produced."))
        lines.extend(["", "## Errors"])
        lines.extend(_bullet_lines(report_data.get("errors"), "No engine errors were produced."))
        lines.extend(["", "## Suggested validation"])
        lines.extend(_bullet_lines(validation_lines, DEFAULT_VALIDATION_NOTE))
        return "\n".join(lines).strip() + "\n"

    def _format_findings(self, findings: list[EngineFinding]) -> list[str]:
        """Return human-readable finding lines with truncation."""
        if not findings:
            return ["- No advisory findings were produced."]
        lines: list[str] = []
        for index, finding in enumerate(findings[: self.max_findings], start=1):
            data = finding.to_dict()
            location = str(data.get("file_path") or "project")
            line_number = int(data.get("line_number") or 0)
            if line_number > 0:
                location = location + ":" + str(line_number)
            lines.append(
                "- "
                + str(index)
                + ". ["
                + str(data.get("severity", "info"))
                + "] "
                + str(data.get("title", "Finding"))
                + " ("
                + location
                + ") - "
                + str(data.get("message", ""))
            )
            evidence = _clean_text(data.get("evidence", ""))
            if evidence:
                lines.append("  - Evidence: " + evidence)
            recommendation = _clean_text(data.get("recommendation", ""))
            if recommendation:
                lines.append("  - Recommendation: " + recommendation)
        remaining = len(findings) - self.max_findings
        if remaining > 0:
            lines.append("- Truncated " + str(remaining) + " additional findings.")
        return lines


def format_engine_report(
    report: EngineReport,
    *,
    title: str = "Project Intelligence Report",
    suggested_validation: Iterable[object] | object | None = None,
    max_findings: int = 25,
) -> str:
    """Convenience wrapper for formatting one EngineReport."""
    formatter = EngineReportFormatter(max_findings=max_findings)
    return formatter.format_report(
        report,
        title=title,
        suggested_validation=suggested_validation,
    )
