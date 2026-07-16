"""Build On Every Push validation plans and reports.

This module is intentionally report-only. It does not execute shell commands.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

GA_PUSH_STATUS_PASS = "pass"
GA_PUSH_STATUS_FAIL = "fail"
GA_PUSH_STATUS_UNKNOWN = "unknown"
GA_PUSH_VALID_STATUSES = {
    GA_PUSH_STATUS_PASS,
    GA_PUSH_STATUS_FAIL,
    GA_PUSH_STATUS_UNKNOWN,
}
GA_PUSH_DEFAULT_CHECKS = (
    "focused_tests",
    "architecture_validation",
    "workflow_validation",
    "import_smoke",
)


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _clean_text(value: str | None, default: str = "Not specified.") -> str:
    text = " ".join(str(value or "").strip().split())
    return text or default


def _normalize_status(value: str | None) -> str:
    text = str(value or "").strip().lower()
    if text in GA_PUSH_VALID_STATUSES:
        return text
    return GA_PUSH_STATUS_UNKNOWN


def build_default_push_commands(project_root: str | Path) -> tuple[str, ...]:
    """Return the default local commands for an on-every-push gate."""

    root = str(project_root)
    return (
        "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py "
        "--root " + root + " --validate",
        "python kanda_reasoner_app\\manage_workflows\\manage_workflows.py "
        "--root " + root + " --validate",
        "python -c \"import kanda_reasoner_app; "
        "import reasoner_tools_gui; print('import smoke ok')\"",
    )


def classify_validation_text(text: str) -> str:
    """Classify validation text as pass, fail, or unknown."""

    lower_text = text.lower()
    failure_tokens = (
        "traceback",
        "error   ",
        " fail=1",
        " fail=2",
        " fail=3",
        " fail=4",
        " expected exit code 0, got 1",
        "no module named",
    )
    if any(token in lower_text for token in failure_tokens):
        return GA_PUSH_STATUS_FAIL
    if "no validation issues" in lower_text:
        return GA_PUSH_STATUS_PASS
    if "summary: pass=" in lower_text and " fail=0 " in lower_text:
        return GA_PUSH_STATUS_PASS
    if "tests passed" in lower_text:
        return GA_PUSH_STATUS_PASS
    return GA_PUSH_STATUS_UNKNOWN


@dataclass(frozen=True)
class OnEveryPushCheckResult:
    """One check result supplied to the on-every-push report."""

    name: str
    command: str = ""
    status: str = GA_PUSH_STATUS_UNKNOWN
    output_excerpt: str = ""

    def normalized_status(self) -> str:
        """Return a supported check status."""

        return _normalize_status(self.status)

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-serializable check dictionary."""

        return {
            "name": _clean_text(self.name),
            "command": _clean_text(self.command),
            "status": self.normalized_status(),
            "output_excerpt": _clean_text(self.output_excerpt),
        }


@dataclass(frozen=True)
class OnEveryPushReport:
    """Structured On Every Push validation report."""

    report_id: str
    created_at: str
    project_root: str
    overall_status: str
    commands: tuple[str, ...] = field(default_factory=tuple)
    check_results: tuple[OnEveryPushCheckResult, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        """Return the report as a JSON-serializable dictionary."""

        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "project_root": self.project_root,
            "overall_status": self.overall_status,
            "commands": list(self.commands),
            "check_results": [item.to_dict() for item in self.check_results],
            "notes": list(self.notes),
        }


def infer_overall_push_status(results: Iterable[OnEveryPushCheckResult]) -> str:
    """Infer the overall push-gate status from supplied results."""

    normalized = [item.normalized_status() for item in results]
    if not normalized:
        return GA_PUSH_STATUS_UNKNOWN
    if GA_PUSH_STATUS_FAIL in normalized:
        return GA_PUSH_STATUS_FAIL
    if all(status == GA_PUSH_STATUS_PASS for status in normalized):
        return GA_PUSH_STATUS_PASS
    return GA_PUSH_STATUS_UNKNOWN


def build_on_every_push_report(
    project_root: str | Path,
    results: Iterable[OnEveryPushCheckResult] = (),
    notes: Iterable[str] = (),
) -> OnEveryPushReport:
    """Build a report from explicit on-every-push evidence."""

    check_results = tuple(results)
    clean_notes = tuple(_clean_text(note) for note in notes if str(note).strip())
    return OnEveryPushReport(
        report_id="on_every_push_" + _utc_timestamp(),
        created_at=_utc_timestamp(),
        project_root=str(project_root),
        overall_status=infer_overall_push_status(check_results),
        commands=build_default_push_commands(project_root),
        check_results=check_results,
        notes=clean_notes,
    )


def build_check_result_from_output(name: str, command: str, output: str) -> OnEveryPushCheckResult:
    """Create a check result by classifying an output excerpt."""

    excerpt = "\n".join(str(output).splitlines()[:20])
    return OnEveryPushCheckResult(
        name=name,
        command=command,
        status=classify_validation_text(output),
        output_excerpt=excerpt,
    )


def render_on_every_push_markdown(report: OnEveryPushReport) -> str:
    """Render an On Every Push report as Markdown text."""

    lines = [
        "# On Every Push Validation Report",
        "",
        "Report ID: " + report.report_id,
        "Created at: " + report.created_at,
        "Project root: " + report.project_root,
        "Overall status: " + report.overall_status,
        "",
        "## Commands",
    ]
    lines.extend("- " + command for command in report.commands)
    lines.extend(["", "## Check results"])
    if report.check_results:
        for item in report.check_results:
            lines.extend(
                [
                    "- " + _clean_text(item.name) + ": " + item.normalized_status(),
                    "  Command: " + _clean_text(item.command),
                ]
            )
    else:
        lines.append("- No check results were supplied.")
    if report.notes:
        lines.extend(["", "## Notes"])
        lines.extend("- " + note for note in report.notes)
    lines.append("")
    return "\n".join(lines)


def default_on_every_push_report_dir(project_root: str | Path) -> Path:
    """Return the default on-every-push report directory."""

    return Path(project_root) / "workbench" / "on_every_push_reports"


__all__ = [
    "GA_PUSH_DEFAULT_CHECKS",
    "GA_PUSH_STATUS_FAIL",
    "GA_PUSH_STATUS_PASS",
    "GA_PUSH_STATUS_UNKNOWN",
    "GA_PUSH_VALID_STATUSES",
    "OnEveryPushCheckResult",
    "OnEveryPushReport",
    "build_check_result_from_output",
    "build_default_push_commands",
    "build_on_every_push_report",
    "classify_validation_text",
    "default_on_every_push_report_dir",
    "infer_overall_push_status",
    "render_on_every_push_markdown",
]
