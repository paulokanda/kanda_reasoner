"""Report-only high-confidence secret finding inspector.

This module turns the report-only secret scan output into a focused manual
review plan for high-confidence findings. It never prints raw secret values,
never moves files, never deletes files, and writes files only through explicit
write functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.secret_scan_gate import (
    SECRET_SCAN_SEVERITY_HIGH,
    SecretScanFinding,
    SecretScanReport,
    scan_path_for_secrets,
)

HIGH_CONFIDENCE_SECRET_INSPECTION_ACTION = "report_only"
HIGH_CONFIDENCE_SECRET_INSPECTION_SCHEMA_VERSION = 1
HIGH_CONFIDENCE_SECRET_STATUS_CLEAN = "clean"
HIGH_CONFIDENCE_SECRET_STATUS_REVIEW_REQUIRED = "review_required"
HIGH_CONFIDENCE_SECRET_RISK_BLOCKING = "blocking_secret_review"
HIGH_CONFIDENCE_SECRET_RISK_ADVISORY = "advisory_secret_review"


@dataclass(frozen=True)
class HighConfidenceSecretInspectionItem:
    """One redacted secret finding prepared for manual inspection."""

    relative_path: str
    line_number: int
    pattern_name: str
    severity: str
    risk_class: str
    redacted_preview: str
    recommended_action: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "line_number": self.line_number,
            "pattern_name": self.pattern_name,
            "severity": self.severity,
            "risk_class": self.risk_class,
            "redacted_preview": self.redacted_preview,
            "recommended_action": self.recommended_action,
        }


@dataclass(frozen=True)
class HighConfidenceSecretInspectionReport:
    """Report-only manual inspection plan for sensitive findings."""

    source_root: str
    action: str = HIGH_CONFIDENCE_SECRET_INSPECTION_ACTION
    schema_version: int = HIGH_CONFIDENCE_SECRET_INSPECTION_SCHEMA_VERSION
    items: tuple[HighConfidenceSecretInspectionItem, ...] = field(
        default_factory=tuple
    )
    scanned_findings: int = 0

    @property
    def total_items(self) -> int:
        """Return the total number of inspection items."""
        return len(self.items)

    @property
    def blocking_items(self) -> int:
        """Return the number of high-confidence blocking inspection items."""
        return sum(
            1
            for item in self.items
            if item.risk_class == HIGH_CONFIDENCE_SECRET_RISK_BLOCKING
        )

    @property
    def advisory_items(self) -> int:
        """Return the number of advisory inspection items."""
        return sum(
            1
            for item in self.items
            if item.risk_class == HIGH_CONFIDENCE_SECRET_RISK_ADVISORY
        )

    def is_clean(self) -> bool:
        """Return True when no manual inspection items exist."""
        return self.total_items == 0

    def status(self) -> str:
        """Return the high-confidence secret inspection status."""
        if self.blocking_items:
            return HIGH_CONFIDENCE_SECRET_STATUS_REVIEW_REQUIRED
        return HIGH_CONFIDENCE_SECRET_STATUS_CLEAN

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "action": self.action,
            "source_root": self.source_root,
            "status": self.status(),
            "scanned_findings": self.scanned_findings,
            "total_items": self.total_items,
            "blocking_items": self.blocking_items,
            "advisory_items": self.advisory_items,
            "items": [item.to_dict() for item in self.items],
        }

    def summary_lines(self) -> list[str]:
        """Return a redacted human-readable summary as lines."""
        lines = [
            "Kanda Reasoner high-confidence secret inspection report",
            f"Action: {self.action}",
            f"Source root: {self.source_root}",
            f"Status: {self.status()}",
            f"Scanned findings: {self.scanned_findings}",
            f"Inspection items: {self.total_items}",
            f"Blocking items: {self.blocking_items}",
            f"Advisory items: {self.advisory_items}",
        ]

        if self.items:
            lines.append("Items:")
            for item in self.items:
                lines.append(
                    f"  - {item.relative_path}:{item.line_number} "
                    f"[{item.risk_class}:{item.pattern_name}] "
                    f"{item.redacted_preview} -> {item.recommended_action}"
                )

        return lines

    def summary(self) -> str:
        """Return a redacted human-readable summary."""
        return "\n".join(self.summary_lines())


def _risk_class_for_finding(finding: SecretScanFinding) -> str:
    """Return the risk class for a secret scan finding."""
    if finding.severity == SECRET_SCAN_SEVERITY_HIGH:
        return HIGH_CONFIDENCE_SECRET_RISK_BLOCKING
    return HIGH_CONFIDENCE_SECRET_RISK_ADVISORY


def _recommended_action_for_finding(finding: SecretScanFinding) -> str:
    """Return a manual-review action without exposing sensitive values."""
    if finding.severity == SECRET_SCAN_SEVERITY_HIGH:
        return (
            "manually verify, rotate credential if real, remove from source, "
            "and move to an environment variable, OS credential store, or "
            "ignored local config"
        )
    return "review manually and keep out of packaged builds if sensitive"


def _item_from_secret_finding(
    finding: SecretScanFinding,
) -> HighConfidenceSecretInspectionItem:
    """Convert a secret scan finding to an inspection item."""
    return HighConfidenceSecretInspectionItem(
        relative_path=finding.relative_path,
        line_number=finding.line_number,
        pattern_name=finding.pattern_name,
        severity=finding.severity,
        risk_class=_risk_class_for_finding(finding),
        redacted_preview=finding.redacted_preview,
        recommended_action=_recommended_action_for_finding(finding),
    )


def build_high_confidence_secret_inspection_from_report(
    report: SecretScanReport,
    include_advisory: bool = False,
) -> HighConfidenceSecretInspectionReport:
    """Build a redacted inspection report from a secret scan report."""
    selected_findings = []
    for finding in report.findings:
        if finding.severity == SECRET_SCAN_SEVERITY_HIGH or include_advisory:
            selected_findings.append(finding)

    items = tuple(_item_from_secret_finding(finding) for finding in selected_findings)
    return HighConfidenceSecretInspectionReport(
        source_root=report.source_root,
        items=items,
        scanned_findings=report.total_findings,
    )


def build_high_confidence_secret_inspection(
    source_root: str | Path,
    include_advisory: bool = False,
) -> HighConfidenceSecretInspectionReport:
    """Scan source_root and build a report-only manual inspection plan."""
    root = normalize_path(source_root)
    scan_report = scan_path_for_secrets(root)
    return build_high_confidence_secret_inspection_from_report(
        scan_report,
        include_advisory=include_advisory,
    )


def render_high_confidence_secret_inspection_text(
    report: HighConfidenceSecretInspectionReport,
) -> str:
    """Return a redacted human-readable inspection report."""
    return report.summary()


def render_high_confidence_secret_inspection_json(
    report: HighConfidenceSecretInspectionReport,
) -> str:
    """Return a stable JSON inspection report."""
    return json.dumps(report.to_dict(), indent=2, sort_keys=True)


def write_high_confidence_secret_inspection_text(
    report: HighConfidenceSecretInspectionReport,
    destination: str | Path,
    overwrite: bool = False,
) -> Path:
    """Write a redacted text report only when explicitly requested."""
    path = Path(destination)
    if not path.parent.exists():
        raise ValueError(f"destination parent does not exist: {path.parent}")
    if path.exists() and not overwrite:
        raise FileExistsError(f"destination already exists: {path}")
    path.write_text(
        render_high_confidence_secret_inspection_text(report) + "\n",
        encoding="utf-8",
    )
    return path


def write_high_confidence_secret_inspection_json(
    report: HighConfidenceSecretInspectionReport,
    destination: str | Path,
    overwrite: bool = False,
) -> Path:
    """Write a redacted JSON report only when explicitly requested."""
    path = Path(destination)
    if not path.parent.exists():
        raise ValueError(f"destination parent does not exist: {path.parent}")
    if path.exists() and not overwrite:
        raise FileExistsError(f"destination already exists: {path}")
    path.write_text(
        render_high_confidence_secret_inspection_json(report) + "\n",
        encoding="utf-8",
    )
    return path


__all__ = [
    "HIGH_CONFIDENCE_SECRET_INSPECTION_ACTION",
    "HIGH_CONFIDENCE_SECRET_INSPECTION_SCHEMA_VERSION",
    "HIGH_CONFIDENCE_SECRET_RISK_ADVISORY",
    "HIGH_CONFIDENCE_SECRET_RISK_BLOCKING",
    "HIGH_CONFIDENCE_SECRET_STATUS_CLEAN",
    "HIGH_CONFIDENCE_SECRET_STATUS_REVIEW_REQUIRED",
    "HighConfidenceSecretInspectionItem",
    "HighConfidenceSecretInspectionReport",
    "build_high_confidence_secret_inspection",
    "build_high_confidence_secret_inspection_from_report",
    "render_high_confidence_secret_inspection_json",
    "render_high_confidence_secret_inspection_text",
    "write_high_confidence_secret_inspection_json",
    "write_high_confidence_secret_inspection_text",
]
