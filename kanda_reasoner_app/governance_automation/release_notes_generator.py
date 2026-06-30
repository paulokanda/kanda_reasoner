# project-path: kanda_reasoner_app/governance_automation/release_notes_generator.py
"""Build release-note reports from bundle and validation evidence."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

GA_RELEASE_NOTE_STATUS_VALUES = {"draft", "validated", "blocked"}
GA_RELEASE_NOTE_DEFAULT_STATUS = "draft"


def _utc_timestamp() -> str:
    """Support utc timestamp behavior.
    
    Returns
    -------
    str
        The string result.
    """
    
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _normalize_status(value: str | None) -> str:
    """Support normalize status behavior.
    
    Parameters
    ----------
    value : str | None
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if value in GA_RELEASE_NOTE_STATUS_VALUES:
        return str(value)
    return GA_RELEASE_NOTE_DEFAULT_STATUS


def _clean_line(value: str) -> str:
    """Support clean line behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    text = " ".join(str(value).strip().split())
    return text or "Not specified."


@dataclass(frozen=True)
class GovernanceReleaseNoteInput:
    """Input evidence used to create a release-note report."""

    title: str
    bundle_name: str = ""
    summary: str = ""
    changed_files: tuple[str, ...] = ()
    validation_lines: tuple[str, ...] = ()
    status: str = GA_RELEASE_NOTE_DEFAULT_STATUS

    def normalized_status(self) -> str:
        """Return a supported release-note status."""

        return _normalize_status(self.status)


@dataclass(frozen=True)
class GovernanceReleaseNoteItem:
    """Single release-note item normalized for report output."""

    title: str
    bundle_name: str
    summary: str
    changed_files: tuple[str, ...] = ()
    validation_lines: tuple[str, ...] = ()
    status: str = GA_RELEASE_NOTE_DEFAULT_STATUS

    def to_dict(self) -> dict[str, object]:
        """Return the item as a JSON-serializable dictionary."""

        return {
            "title": self.title,
            "bundle_name": self.bundle_name,
            "summary": self.summary,
            "changed_files": list(self.changed_files),
            "validation_lines": list(self.validation_lines),
            "status": self.status,
        }


@dataclass(frozen=True)
class GovernanceReleaseNotesReport:
    """Structured release-note report."""

    report_id: str
    created_at: str
    title: str
    items: tuple[GovernanceReleaseNoteItem, ...] = field(default_factory=tuple)
    status: str = GA_RELEASE_NOTE_DEFAULT_STATUS

    def to_dict(self) -> dict[str, object]:
        """Return the report as a JSON-serializable dictionary."""

        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "title": self.title,
            "status": self.status,
            "items": [item.to_dict() for item in self.items],
        }


def make_release_note_item(item: GovernanceReleaseNoteInput) -> GovernanceReleaseNoteItem:
    """Normalize one release-note input item."""

    title = _clean_line(item.title)
    bundle_name = _clean_line(item.bundle_name) if item.bundle_name else "Not specified."
    summary = _clean_line(item.summary) if item.summary else "Not specified."
    changed_files = tuple(_clean_line(path) for path in item.changed_files if str(path).strip())
    validation_lines = tuple(
        _clean_line(line) for line in item.validation_lines if str(line).strip()
    )
    return GovernanceReleaseNoteItem(
        title=title,
        bundle_name=bundle_name,
        summary=summary,
        changed_files=changed_files,
        validation_lines=validation_lines,
        status=item.normalized_status(),
    )


def build_release_notes_report(
    title: str,
    inputs: Iterable[GovernanceReleaseNoteInput],
    status: str | None = None,
) -> GovernanceReleaseNotesReport:
    """Build a structured release-notes report from explicit evidence."""

    items = tuple(make_release_note_item(item) for item in inputs)
    report_status = _normalize_status(status)
    return GovernanceReleaseNotesReport(
        report_id="release_notes_" + _utc_timestamp(),
        created_at=_utc_timestamp(),
        title=_clean_line(title),
        items=items,
        status=report_status,
    )


def render_release_notes_markdown(report: GovernanceReleaseNotesReport) -> str:
    """Render release notes as Markdown text."""

    lines = [
        "# " + report.title,
        "",
        "Report ID: " + report.report_id,
        "Created at: " + report.created_at,
        "Status: " + report.status,
        "",
    ]
    if not report.items:
        lines.extend(["No release-note items were provided.", ""])
        return "\n".join(lines)

    for index, item in enumerate(report.items, start=1):
        lines.extend(
            [
                "## " + str(index) + ". " + item.title,
                "",
                "Bundle: " + item.bundle_name,
                "Status: " + item.status,
                "",
                item.summary,
                "",
                "Changed files:",
            ]
        )
        if item.changed_files:
            lines.extend("- " + path for path in item.changed_files)
        else:
            lines.append("- Not specified.")
        lines.extend(["", "Validation evidence:"])
        if item.validation_lines:
            lines.extend("- " + line for line in item.validation_lines)
        else:
            lines.append("- Not specified.")
        lines.append("")
    return "\n".join(lines)


def default_release_notes_dir(project_root: str | Path) -> Path:
    """Return the default release-notes output directory."""

    return Path(project_root) / "workbench" / "release_notes"


__all__ = [
    "GA_RELEASE_NOTE_DEFAULT_STATUS",
    "GA_RELEASE_NOTE_STATUS_VALUES",
    "GovernanceReleaseNoteInput",
    "GovernanceReleaseNoteItem",
    "GovernanceReleaseNotesReport",
    "build_release_notes_report",
    "default_release_notes_dir",
    "make_release_note_item",
    "render_release_notes_markdown",
]
