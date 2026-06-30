# project-path: kanda_reasoner_app/source_hygiene/schemas.py
"""Shared data structures for source hygiene reports."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_REPORT_TYPE = "source_hygiene"

VALID_REPORT_TYPES = frozenset(
    {
        "source_hygiene",
        "bom_scan",
        "bom_fix",
        "shadow_conflict_audit",
        "shadow_conflict_plan",
        "facade_fix_plan",
    }
)

VALID_SEVERITIES = frozenset({"info", "warning", "error"})
VALID_CONFIDENCE = frozenset({"low", "medium", "high"})

__all__ = [
    "DEFAULT_REPORT_TYPE",
    "SourceHygieneFinding",
    "SourceHygieneReport",
    "SourceHygieneWriteResult",
    "VALID_CONFIDENCE",
    "VALID_REPORT_TYPES",
    "VALID_SEVERITIES",
    "make_report_id",
    "normalize_confidence",
    "normalize_report_type",
    "normalize_severity",
    "utc_timestamp",
]


def utc_timestamp() -> str:
    """Return a stable UTC timestamp suitable for report metadata."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def make_report_id(report_type: str, timestamp: str | None = None) -> str:
    """Create a deterministic report identifier prefix."""
    safe_type = normalize_report_type(report_type)
    value = timestamp or utc_timestamp()
    cleaned = value.replace(":", "").replace("-", "").replace("+", "Z")
    cleaned = cleaned.replace(".", "").replace(" ", "_")
    return safe_type + "_" + cleaned


def normalize_report_type(value: str | None) -> str:
    """Normalize and validate a source hygiene report type."""
    candidate = (value or DEFAULT_REPORT_TYPE).strip().lower()
    if candidate not in VALID_REPORT_TYPES:
        raise ValueError("Unsupported source hygiene report type: " + candidate)
    return candidate


def normalize_severity(value: str | None) -> str:
    """Normalize and validate a finding severity."""
    candidate = (value or "info").strip().lower()
    if candidate not in VALID_SEVERITIES:
        raise ValueError("Unsupported source hygiene severity: " + candidate)
    return candidate


def normalize_confidence(value: str | None) -> str:
    """Normalize and validate a finding confidence level."""
    candidate = (value or "medium").strip().lower()
    if candidate not in VALID_CONFIDENCE:
        raise ValueError("Unsupported source hygiene confidence: " + candidate)
    return candidate


@dataclass(frozen=True)
class SourceHygieneFinding:
    """One source hygiene finding in a report."""

    code: str
    path: str
    message: str
    severity: str = "info"
    confidence: str = "medium"
    line: int | None = None
    evidence: dict[str, Any] = field(default_factory=dict)
    suggested_action: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible finding dictionary."""
        return {
            "code": self.code,
            "path": self.path,
            "line": self.line,
            "severity": normalize_severity(self.severity),
            "confidence": normalize_confidence(self.confidence),
            "message": self.message,
            "evidence": dict(self.evidence),
            "suggested_action": self.suggested_action,
        }


@dataclass(frozen=True)
class SourceHygieneReport:
    """Structured source hygiene report."""

    project_root: str
    report_type: str = DEFAULT_REPORT_TYPE
    report_id: str = ""
    created_at: str = ""
    summary: str = ""
    findings: tuple[SourceHygieneFinding, ...] = ()
    input_sources: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible report dictionary."""
        created = self.created_at or utc_timestamp()
        report_type = normalize_report_type(self.report_type)
        report_id = self.report_id or make_report_id(report_type, created)
        return {
            "report_id": report_id,
            "report_type": report_type,
            "created_at": created,
            "project_root": str(Path(self.project_root)),
            "input_sources": list(self.input_sources),
            "summary": self.summary,
            "finding_count": len(self.findings),
            "findings": [finding.to_dict() for finding in self.findings],
        }


@dataclass(frozen=True)
class SourceHygieneWriteResult:
    """Paths written for a source hygiene report."""

    json_path: Path
    markdown_path: Path

    def to_dict(self) -> dict[str, str]:
        """Return written report paths as strings."""
        return {
            "json_path": str(self.json_path),
            "markdown_path": str(self.markdown_path),
        }
