"""Post-migration guard for evidence output routing.

This module verifies that generated evidence routing remains external to the
selected project source tree. It is report-only and side-effect free on import:
importing it must not create folders, move files, delete files, or scan the live
source tree.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from kanda_reasoner_app.storage_policy.path_resolver import (
    is_path_same_or_inside,
    normalize_path,
)

EVIDENCE_OUTPUT_ROUTE_GUARD_ACTION = "report_only"
EVIDENCE_OUTPUT_ROUTE_GUARD_SCHEMA_VERSION = 1
EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_CLEAN = "clean"
EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_BLOCKED = "blocked"
EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_SOURCE_EVIDENCE_RECREATED = (
    "source_evidence_recreated"
)
EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_SOURCE_JSON_RECREATED = "source_json_recreated"
EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_RESOLVER_INSIDE_SOURCE = "resolver_inside_source"
EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_AUDIT_JSON_MISSING = "audit_json_missing"
EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_AUDIT_JSON_COUNT_LOW = "audit_json_count_low"


@dataclass(frozen=True)
class EvidenceOutputRouteGuardFinding:
    """One route-guard finding requiring review before future generation."""

    risk: str
    path: str
    message: str


@dataclass(frozen=True)
class EvidenceOutputRouteGuardReport:
    """Report describing whether evidence output routing is still safe."""

    action: str
    schema_version: int
    source_root: str
    active_evidence_root: str
    active_json_complete_dir: str
    in_source_evidence_root: str
    in_source_evidence_exists: bool
    in_source_json_count: int
    audit_json_complete_exists: bool
    audit_json_count: int
    expected_min_audit_json_count: int | None
    findings: tuple[EvidenceOutputRouteGuardFinding, ...]

    @property
    def total_findings(self) -> int:
        """Return the number of blocking findings."""
        return len(self.findings)

    def status(self) -> str:
        """Return clean when no blocking findings are present."""
        if self.findings:
            return EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_BLOCKED
        return EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_CLEAN


def _count_json_files(folder: Path) -> int:
    """Return the number of JSON files under folder without creating it."""
    if not folder.exists():
        return 0
    if folder.is_file():
        return 1 if folder.suffix.lower() == ".json" else 0
    return sum(1 for path in folder.rglob("*.json") if path.is_file())


def build_evidence_output_route_guard(
    project_root: str | Path,
    expected_min_audit_json_count: int | None = None,
    require_existing_audit_json_complete: bool = False,
) -> EvidenceOutputRouteGuardReport:
    """Build a report that detects evidence output routing regressions."""
    from kanda_reasoner_app.project_analysis_evidence_paths import (
        analysis_json_complete_dir,
        project_analysis_evidence_root,
    )

    root = normalize_path(project_root)
    active_root = project_analysis_evidence_root(root)
    audit_json_dir = analysis_json_complete_dir(root)
    in_source_root = root / "project_analysis_evidence"

    in_source_exists = in_source_root.exists()
    in_source_json_count = _count_json_files(in_source_root)
    audit_exists = audit_json_dir.exists()
    audit_json_count = _count_json_files(audit_json_dir)

    findings: list[EvidenceOutputRouteGuardFinding] = []

    if is_path_same_or_inside(active_root, root):
        findings.append(
            EvidenceOutputRouteGuardFinding(
                risk=EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_RESOLVER_INSIDE_SOURCE,
                path=str(active_root),
                message="Active evidence root resolves inside the selected project source tree.",
            )
        )

    if in_source_exists:
        findings.append(
            EvidenceOutputRouteGuardFinding(
                risk=EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_SOURCE_EVIDENCE_RECREATED,
                path=str(in_source_root),
                message="The old in-source project_analysis_evidence folder exists again.",
            )
        )

    if in_source_json_count:
        findings.append(
            EvidenceOutputRouteGuardFinding(
                risk=EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_SOURCE_JSON_RECREATED,
                path=str(in_source_root),
                message="Generated evidence JSON files are present inside source again.",
            )
        )

    if require_existing_audit_json_complete and not audit_exists:
        findings.append(
            EvidenceOutputRouteGuardFinding(
                risk=EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_AUDIT_JSON_MISSING,
                path=str(audit_json_dir),
                message="External audit json_complete folder is required but missing.",
            )
        )

    if expected_min_audit_json_count is not None:
        if expected_min_audit_json_count < 0:
            raise ValueError("expected_min_audit_json_count must not be negative.")
        if audit_json_count < expected_min_audit_json_count:
            findings.append(
                EvidenceOutputRouteGuardFinding(
                    risk=EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_AUDIT_JSON_COUNT_LOW,
                    path=str(audit_json_dir),
                    message=(
                        "External audit JSON count is below the expected minimum "
                        f"({audit_json_count} < {expected_min_audit_json_count})."
                    ),
                )
            )

    return EvidenceOutputRouteGuardReport(
        action=EVIDENCE_OUTPUT_ROUTE_GUARD_ACTION,
        schema_version=EVIDENCE_OUTPUT_ROUTE_GUARD_SCHEMA_VERSION,
        source_root=str(root),
        active_evidence_root=str(active_root),
        active_json_complete_dir=str(audit_json_dir),
        in_source_evidence_root=str(in_source_root),
        in_source_evidence_exists=in_source_exists,
        in_source_json_count=in_source_json_count,
        audit_json_complete_exists=audit_exists,
        audit_json_count=audit_json_count,
        expected_min_audit_json_count=expected_min_audit_json_count,
        findings=tuple(findings),
    )


def evidence_output_route_guard_to_dict(
    report: EvidenceOutputRouteGuardReport,
) -> dict[str, Any]:
    """Return a stable JSON-serializable representation of report."""
    return {
        "action": report.action,
        "schema_version": report.schema_version,
        "status": report.status(),
        "source_root": report.source_root,
        "active_evidence_root": report.active_evidence_root,
        "active_json_complete_dir": report.active_json_complete_dir,
        "in_source_evidence_root": report.in_source_evidence_root,
        "in_source_evidence_exists": report.in_source_evidence_exists,
        "in_source_json_count": report.in_source_json_count,
        "audit_json_complete_exists": report.audit_json_complete_exists,
        "audit_json_count": report.audit_json_count,
        "expected_min_audit_json_count": report.expected_min_audit_json_count,
        "findings": [finding.__dict__ for finding in report.findings],
    }


def render_evidence_output_route_guard_json(
    report: EvidenceOutputRouteGuardReport,
) -> str:
    """Render report as stable JSON text."""
    return json.dumps(
        evidence_output_route_guard_to_dict(report),
        indent=2,
        sort_keys=True,
    )


def render_evidence_output_route_guard_text(
    report: EvidenceOutputRouteGuardReport,
) -> str:
    """Render report as human-readable text."""
    lines = [
        "Kanda Reasoner evidence output route guard",
        f"Action: {report.action}",
        f"Status: {report.status()}",
        f"Source root: {report.source_root}",
        f"Active evidence root: {report.active_evidence_root}",
        f"Active json_complete: {report.active_json_complete_dir}",
        f"In-source evidence exists: {report.in_source_evidence_exists}",
        f"In-source JSON count: {report.in_source_json_count}",
        f"Audit json_complete exists: {report.audit_json_complete_exists}",
        f"Audit JSON count: {report.audit_json_count}",
        f"Findings: {report.total_findings}",
    ]

    if report.findings:
        lines.append("Items:")
        for finding in report.findings:
            lines.append(f"  - {finding.risk}: {finding.path} :: {finding.message}")

    return "\n".join(lines)


def _write_text(path: str | Path, text: str, overwrite: bool) -> Path:
    """Write text to an existing parent directory."""
    destination = Path(path)
    if not destination.parent.exists():
        raise FileNotFoundError(f"Parent folder does not exist: {destination.parent}")
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing file: {destination}")
    destination.write_text(text, encoding="utf-8")
    return destination


def write_evidence_output_route_guard_text(
    report: EvidenceOutputRouteGuardReport,
    output_path: str | Path,
    overwrite: bool = False,
) -> Path:
    """Write the human-readable route guard report explicitly."""
    return _write_text(
        output_path,
        render_evidence_output_route_guard_text(report),
        overwrite=overwrite,
    )


def write_evidence_output_route_guard_json(
    report: EvidenceOutputRouteGuardReport,
    output_path: str | Path,
    overwrite: bool = False,
) -> Path:
    """Write the JSON route guard report explicitly."""
    return _write_text(
        output_path,
        render_evidence_output_route_guard_json(report),
        overwrite=overwrite,
    )


__all__ = [
    "EVIDENCE_OUTPUT_ROUTE_GUARD_ACTION",
    "EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_AUDIT_JSON_COUNT_LOW",
    "EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_AUDIT_JSON_MISSING",
    "EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_RESOLVER_INSIDE_SOURCE",
    "EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_SOURCE_EVIDENCE_RECREATED",
    "EVIDENCE_OUTPUT_ROUTE_GUARD_RISK_SOURCE_JSON_RECREATED",
    "EVIDENCE_OUTPUT_ROUTE_GUARD_SCHEMA_VERSION",
    "EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_BLOCKED",
    "EVIDENCE_OUTPUT_ROUTE_GUARD_STATUS_CLEAN",
    "EvidenceOutputRouteGuardFinding",
    "EvidenceOutputRouteGuardReport",
    "build_evidence_output_route_guard",
    "evidence_output_route_guard_to_dict",
    "render_evidence_output_route_guard_json",
    "render_evidence_output_route_guard_text",
    "write_evidence_output_route_guard_json",
    "write_evidence_output_route_guard_text",
]
