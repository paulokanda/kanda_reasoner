"""Canonical exporter for source debris quarantine dry-run reports.

This module writes review-only dry-run reports into the Kanda maintenance audit
log area when explicitly called. It never moves, deletes, quarantines, migrates,
or rewrites source files. Importing this module is side-effect free.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.architecture_audit_resolver import (
    get_project_slug,
)
from kanda_reasoner_app.storage_policy.maintenance_subfolder_policy import (
    get_maintenance_subfolder,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run import (
    SourceDebrisQuarantineDryRunPlan,
    build_source_debris_quarantine_dry_run,
    write_source_debris_quarantine_dry_run_json,
    write_source_debris_quarantine_dry_run_text,
)

SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_ACTION = "export_dry_run_report_only"
SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_SCHEMA_VERSION = 1
SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_FOLDER_NAME = (
    "source_debris_quarantine_dry_run"
)
SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_BASENAME = (
    "source_debris_quarantine_dry_run"
)
SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"


@dataclass(frozen=True)
class SourceDebrisQuarantineReportExportPaths:
    """Canonical paths for one dry-run report export."""

    source_root: str
    project_slug: str
    output_root: str
    text_path: str
    json_path: str
    run_id: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "source_root": self.source_root,
            "project_slug": self.project_slug,
            "output_root": self.output_root,
            "text_path": self.text_path,
            "json_path": self.json_path,
            "run_id": self.run_id,
        }


@dataclass(frozen=True)
class SourceDebrisQuarantineReportExportResult:
    """Result of an explicit dry-run report export."""

    source_root: str
    project_slug: str
    output_root: str
    text_path: str
    json_path: str
    run_id: str
    plan_status: str
    total_items: int
    quarantine_review_items: int
    evidence_migration_review_items: int
    packaging_exclusion_review_items: int
    action: str = SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_ACTION
    schema_version: int = SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "action": self.action,
            "source_root": self.source_root,
            "project_slug": self.project_slug,
            "output_root": self.output_root,
            "text_path": self.text_path,
            "json_path": self.json_path,
            "run_id": self.run_id,
            "plan_status": self.plan_status,
            "total_items": self.total_items,
            "quarantine_review_items": self.quarantine_review_items,
            "evidence_migration_review_items": (
                self.evidence_migration_review_items
            ),
            "packaging_exclusion_review_items": (
                self.packaging_exclusion_review_items
            ),
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable export summary as lines."""
        return [
            "Kanda Reasoner source debris quarantine report export",
            f"Action: {self.action}",
            f"Source root: {self.source_root}",
            f"Project slug: {self.project_slug}",
            f"Run id: {self.run_id}",
            f"Output root: {self.output_root}",
            f"Text report: {self.text_path}",
            f"JSON report: {self.json_path}",
            f"Plan status: {self.plan_status}",
            f"Items: {self.total_items}",
            f"Quarantine review items: {self.quarantine_review_items}",
            f"Evidence migration review items: {self.evidence_migration_review_items}",
            f"Packaging exclusion review items: {self.packaging_exclusion_review_items}",
        ]

    def summary(self) -> str:
        """Return a human-readable export summary."""
        return "\n".join(self.summary_lines())


def build_source_debris_quarantine_report_run_id(
    now: datetime | None = None,
) -> str:
    """Return a timestamp run id for a report export."""
    current = now if now is not None else datetime.now()
    return current.strftime(SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_TIMESTAMP_FORMAT)


def build_source_debris_quarantine_report_export_paths(
    source_root: str | Path,
    *,
    maintenance_root: str | Path | None = None,
    run_id: str | None = None,
) -> SourceDebrisQuarantineReportExportPaths:
    """Build canonical export paths without creating folders."""
    root = normalize_path(source_root)
    project_slug = get_project_slug(root)
    resolved_run_id = run_id or build_source_debris_quarantine_report_run_id()
    audit_log_root = get_maintenance_subfolder("audit_logs", maintenance_root)
    output_root = (
        audit_log_root
        / SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_FOLDER_NAME
        / project_slug
        / resolved_run_id
    )
    text_path = output_root / f"{SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_BASENAME}.txt"
    json_path = output_root / f"{SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_BASENAME}.json"
    return SourceDebrisQuarantineReportExportPaths(
        source_root=str(root),
        project_slug=project_slug,
        output_root=str(output_root),
        text_path=str(text_path),
        json_path=str(json_path),
        run_id=resolved_run_id,
    )


def export_source_debris_quarantine_dry_run_report(
    source_root: str | Path,
    *,
    maintenance_root: str | Path | None = None,
    audit_root: str | Path | None = None,
    run_id: str | None = None,
    overwrite: bool = False,
) -> SourceDebrisQuarantineReportExportResult:
    """Export dry-run JSON and text reports to the maintenance audit log area."""
    paths = build_source_debris_quarantine_report_export_paths(
        source_root,
        maintenance_root=maintenance_root,
        run_id=run_id,
    )
    plan = build_source_debris_quarantine_dry_run(
        paths.source_root,
        maintenance_root=maintenance_root,
        audit_root=audit_root,
    )
    output_root = normalize_path(paths.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    write_source_debris_quarantine_dry_run_text(
        plan,
        paths.text_path,
        overwrite=overwrite,
    )
    write_source_debris_quarantine_dry_run_json(
        plan,
        paths.json_path,
        overwrite=overwrite,
    )
    return _result_from_paths_and_plan(paths, plan)


def _result_from_paths_and_plan(
    paths: SourceDebrisQuarantineReportExportPaths,
    plan: SourceDebrisQuarantineDryRunPlan,
) -> SourceDebrisQuarantineReportExportResult:
    """Create an export result from paths and a dry-run plan."""
    return SourceDebrisQuarantineReportExportResult(
        source_root=paths.source_root,
        project_slug=paths.project_slug,
        output_root=paths.output_root,
        text_path=paths.text_path,
        json_path=paths.json_path,
        run_id=paths.run_id,
        plan_status=plan.status(),
        total_items=plan.total_items,
        quarantine_review_items=plan.quarantine_review_items,
        evidence_migration_review_items=plan.evidence_migration_review_items,
        packaging_exclusion_review_items=plan.packaging_exclusion_review_items,
    )


def render_source_debris_quarantine_report_export_text(
    result: SourceDebrisQuarantineReportExportResult,
) -> str:
    """Return a human-readable export result."""
    return result.summary()


def render_source_debris_quarantine_report_export_json(
    result: SourceDebrisQuarantineReportExportResult,
) -> str:
    """Return a stable JSON export result."""
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"


__all__ = [
    "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_ACTION",
    "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_BASENAME",
    "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_FOLDER_NAME",
    "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_SCHEMA_VERSION",
    "SOURCE_DEBRIS_QUARANTINE_REPORT_EXPORT_TIMESTAMP_FORMAT",
    "SourceDebrisQuarantineReportExportPaths",
    "SourceDebrisQuarantineReportExportResult",
    "build_source_debris_quarantine_report_export_paths",
    "build_source_debris_quarantine_report_run_id",
    "export_source_debris_quarantine_dry_run_report",
    "render_source_debris_quarantine_report_export_json",
    "render_source_debris_quarantine_report_export_text",
]
