# project-path: kanda_reasoner_app/storage_policy/compilation_readiness_validator.py
"""Compilation-readiness validator for Kanda Reasoner storage policy.

This module combines report-only source-cleanliness and secret-scan reports
into one pre-compilation readiness summary. It is side-effect free on import
and during validation: it never creates folders, moves files, deletes files,
writes logs, or changes build behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.storage_policy.secret_scan_gate import (
    SECRET_SCAN_SEVERITY_HIGH,
    SecretScanReport,
    scan_path_for_secrets,
)
from kanda_reasoner_app.storage_policy.source_cleanliness_validator import (
    SourceCleanlinessReport,
    scan_source_cleanliness,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path

COMPILATION_READINESS_ACTION = "report_only"
COMPILATION_READINESS_STATUS_READY = "ready"
COMPILATION_READINESS_STATUS_BLOCKED = "blocked"
COMPILATION_READINESS_STATUS_WARNINGS_ONLY = "warnings_only"


@dataclass(frozen=True)
class CompilationReadinessReport:
    """Combined report for pre-compilation readiness."""

    source_root: str
    source_cleanliness: SourceCleanlinessReport
    secret_scan: SecretScanReport
    action: str = COMPILATION_READINESS_ACTION

    @property
    def blocking_source_failures(self) -> int:
        """Return source-cleanliness findings that block compilation."""
        return self.source_cleanliness.total_failures

    @property
    def blocking_secret_findings(self) -> int:
        """Return high-confidence secret findings that block compilation."""
        return self.secret_scan.high_confidence_findings

    @property
    def advisory_warnings(self) -> int:
        """Return warnings and non-blocking secret findings."""
        non_blocking_secrets = sum(
            1
            for finding in self.secret_scan.findings
            if finding.severity != SECRET_SCAN_SEVERITY_HIGH
        )
        return self.source_cleanliness.total_warnings + non_blocking_secrets

    @property
    def total_findings(self) -> int:
        """Return all findings considered by this report."""
        return (
            self.source_cleanliness.total_findings
            + self.secret_scan.total_findings
        )

    def is_ready(self) -> bool:
        """Return True when no blocking findings exist."""
        return (
            self.blocking_source_failures == 0
            and self.blocking_secret_findings == 0
        )

    def status(self) -> str:
        """Return a stable readiness status string."""
        if not self.is_ready():
            return COMPILATION_READINESS_STATUS_BLOCKED
        if self.advisory_warnings > 0:
            return COMPILATION_READINESS_STATUS_WARNINGS_ONLY
        return COMPILATION_READINESS_STATUS_READY

    def summary_lines(self) -> list[str]:
        """Return a human-readable readiness summary."""
        return [
            "Kanda Reasoner compilation readiness report",
            f"Action: {self.action}",
            f"Source root: {self.source_root}",
            f"Status: {self.status()}",
            f"Blocking source failures: {self.blocking_source_failures}",
            f"Blocking high-confidence secret findings: {self.blocking_secret_findings}",
            f"Advisory warnings: {self.advisory_warnings}",
            f"Total findings: {self.total_findings}",
            "Resolution: review blocking findings before compilation; "
            "quarantine debris, migrate valid evidence, and move real secrets "
            "to environment variables, OS credential storage, or ignored local config.",
        ]

    def summary(self) -> str:
        """Return a human-readable readiness summary."""
        return "\n".join(self.summary_lines())


def validate_compilation_readiness(source_root: str | Path) -> CompilationReadinessReport:
    """Return a report-only compilation-readiness result for source_root."""
    root = normalize_path(source_root)
    if not root.exists() or not root.is_dir():
        raise ValueError(f"source_root must be an existing directory: {root}")

    source_report = scan_source_cleanliness(root)
    secret_report = scan_path_for_secrets(root)

    return CompilationReadinessReport(
        source_root=str(root),
        source_cleanliness=source_report,
        secret_scan=secret_report,
    )


def summarize_compilation_readiness(report: CompilationReadinessReport) -> str:
    """Return a human-readable compilation-readiness summary."""
    return report.summary()


__all__ = [
    "COMPILATION_READINESS_ACTION",
    "COMPILATION_READINESS_STATUS_BLOCKED",
    "COMPILATION_READINESS_STATUS_READY",
    "COMPILATION_READINESS_STATUS_WARNINGS_ONLY",
    "CompilationReadinessReport",
    "summarize_compilation_readiness",
    "validate_compilation_readiness",
]
