# project-path: kanda_reasoner_app/storage_policy/source_debris_quarantine_dry_run.py
"""Dry-run planner for source debris quarantine and review.

This module consumes the report-only source debris export and converts it into
an explicit, human-reviewable action plan. It never moves, deletes, copies, or
creates files on import or during planning. The plan is intentionally dry-run
only so Kanda Reasoner can decide which findings should be quarantined, which
valid evidence should be migrated, and which development-only files should be
excluded from packaging before any destructive operation exists.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.architecture_audit_resolver import (
    get_architecture_audit_current_root,
    get_project_slug,
)
from kanda_reasoner_app.storage_policy.maintenance_subfolder_policy import (
    get_maintenance_subfolder,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.source_debris_report_export import (
    SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT,
    SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE,
    SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION,
    SourceDebrisExportPlan,
    SourceDebrisReportItem,
    build_source_debris_report_export,
)

SOURCE_DEBRIS_QUARANTINE_DRY_RUN_ACTION = "dry_run_only"
SOURCE_DEBRIS_QUARANTINE_DRY_RUN_SCHEMA_VERSION = 1
SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW = "quarantine_review"
SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW = "evidence_migration_review"
SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW = "packaging_exclusion_review"
SOURCE_DEBRIS_QUARANTINE_STATUS_EMPTY = "empty"
SOURCE_DEBRIS_QUARANTINE_STATUS_PLANNED = "planned"


@dataclass(frozen=True)
class SourceDebrisQuarantineDryRunItem:
    """One planned source debris review action."""

    relative_path: str
    source_path: str
    category: str
    pattern: str
    is_directory: bool
    recommended_destination: str
    planned_operation: str
    planned_destination_path: str
    requires_human_review: bool
    message: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "source_path": self.source_path,
            "category": self.category,
            "pattern": self.pattern,
            "is_directory": self.is_directory,
            "recommended_destination": self.recommended_destination,
            "planned_operation": self.planned_operation,
            "planned_destination_path": self.planned_destination_path,
            "requires_human_review": self.requires_human_review,
            "message": self.message,
        }


@dataclass(frozen=True)
class SourceDebrisQuarantineDryRunPlan:
    """Dry-run plan for source debris quarantine and review."""

    source_root: str
    project_slug: str
    action: str = SOURCE_DEBRIS_QUARANTINE_DRY_RUN_ACTION
    schema_version: int = SOURCE_DEBRIS_QUARANTINE_DRY_RUN_SCHEMA_VERSION
    items: tuple[SourceDebrisQuarantineDryRunItem, ...] = field(default_factory=tuple)

    @property
    def total_items(self) -> int:
        """Return the total number of dry-run items."""
        return len(self.items)

    @property
    def quarantine_review_items(self) -> int:
        """Return the number of manual quarantine review items."""
        return sum(
            1
            for item in self.items
            if item.planned_operation == SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW
        )

    @property
    def evidence_migration_review_items(self) -> int:
        """Return the number of evidence migration review items."""
        return sum(
            1
            for item in self.items
            if item.planned_operation
            == SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW
        )

    @property
    def packaging_exclusion_review_items(self) -> int:
        """Return the number of packaging exclusion review items."""
        return sum(
            1
            for item in self.items
            if item.planned_operation
            == SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW
        )

    def status(self) -> str:
        """Return the dry-run plan status."""
        if self.total_items == 0:
            return SOURCE_DEBRIS_QUARANTINE_STATUS_EMPTY
        return SOURCE_DEBRIS_QUARANTINE_STATUS_PLANNED

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "action": self.action,
            "status": self.status(),
            "source_root": self.source_root,
            "project_slug": self.project_slug,
            "total_items": self.total_items,
            "quarantine_review_items": self.quarantine_review_items,
            "evidence_migration_review_items": (
                self.evidence_migration_review_items
            ),
            "packaging_exclusion_review_items": (
                self.packaging_exclusion_review_items
            ),
            "items": [item.to_dict() for item in self.items],
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable summary as lines."""
        lines = [
            "Kanda Reasoner source debris quarantine dry-run report",
            f"Action: {self.action}",
            f"Status: {self.status()}",
            f"Source root: {self.source_root}",
            f"Project slug: {self.project_slug}",
            f"Items: {self.total_items}",
            f"Quarantine review items: {self.quarantine_review_items}",
            f"Evidence migration review items: {self.evidence_migration_review_items}",
            f"Packaging exclusion review items: {self.packaging_exclusion_review_items}",
        ]

        if self.items:
            lines.append("Planned review actions:")
            for item in self.items:
                lines.append(
                    f"  - {item.relative_path} [{item.planned_operation}] -> "
                    f"{item.planned_destination_path or 'review only'}"
                )

        return lines

    def summary(self) -> str:
        """Return a human-readable summary."""
        return "\n".join(self.summary_lines())



def _normalize_relative_for_destination(relative_path: str) -> Path:
    """Return a safe relative path object for planned destinations."""
    cleaned = relative_path.replace("\\", "/").strip("/")
    if cleaned.endswith("/"):
        cleaned = cleaned.rstrip("/")
    return Path(*[part for part in cleaned.split("/") if part])



def _source_path_for_item(source_root: Path, item: SourceDebrisReportItem) -> Path:
    """Return the absolute source path for a report item."""
    return source_root / _normalize_relative_for_destination(item.relative_path)



def _quarantine_destination(
    source_root: Path,
    item: SourceDebrisReportItem,
    maintenance_root: str | Path | None,
) -> Path:
    """Return the planned manual quarantine destination."""
    project_slug = get_project_slug(source_root)
    quarantine_root = get_maintenance_subfolder("quarantine_manual", maintenance_root)
    return quarantine_root / project_slug / _normalize_relative_for_destination(
        item.relative_path
    )



def _evidence_review_destination(
    source_root: Path,
    audit_root: str | Path | None,
) -> Path:
    """Return the audit root that should receive reviewed valid evidence."""
    if audit_root is not None:
        return normalize_path(audit_root)
    return get_architecture_audit_current_root(source_root)



def _item_from_report_item(
    source_root: Path,
    item: SourceDebrisReportItem,
    maintenance_root: str | Path | None,
    audit_root: str | Path | None,
) -> SourceDebrisQuarantineDryRunItem:
    """Convert a debris report item into a dry-run review item."""
    source_path = _source_path_for_item(source_root, item)

    if item.recommended_destination == SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE:
        operation = SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW
        destination = _quarantine_destination(source_root, item, maintenance_root)
        message = "review, then quarantine under the Kanda maintenance root"
    elif item.recommended_destination == SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT:
        operation = SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW
        destination = _evidence_review_destination(source_root, audit_root)
        message = "review with the evidence migrator before moving valid evidence"
    elif item.recommended_destination == SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION:
        operation = SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW
        destination = Path("")
        message = "keep during development and exclude from packaged builds"
    else:
        operation = SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW
        destination = _quarantine_destination(source_root, item, maintenance_root)
        message = "unknown destination; review manually before any move"

    return SourceDebrisQuarantineDryRunItem(
        relative_path=item.relative_path,
        source_path=str(source_path),
        category=item.category,
        pattern=item.pattern,
        is_directory=item.is_directory,
        recommended_destination=item.recommended_destination,
        planned_operation=operation,
        planned_destination_path=str(destination),
        requires_human_review=True,
        message=message,
    )



def build_source_debris_quarantine_dry_run(
    source_root: str | Path,
    *,
    maintenance_root: str | Path | None = None,
    audit_root: str | Path | None = None,
) -> SourceDebrisQuarantineDryRunPlan:
    """Build a dry-run plan for source debris quarantine and review."""
    root = normalize_path(source_root)
    report = build_source_debris_report_export(root)
    return build_source_debris_quarantine_dry_run_from_report(
        report,
        maintenance_root=maintenance_root,
        audit_root=audit_root,
    )



def build_source_debris_quarantine_dry_run_from_report(
    report: SourceDebrisExportPlan,
    *,
    maintenance_root: str | Path | None = None,
    audit_root: str | Path | None = None,
) -> SourceDebrisQuarantineDryRunPlan:
    """Build a dry-run plan from an existing source debris report."""
    root = normalize_path(report.source_root)
    items = tuple(
        _item_from_report_item(root, item, maintenance_root, audit_root)
        for item in report.items
    )
    return SourceDebrisQuarantineDryRunPlan(
        source_root=str(root),
        project_slug=get_project_slug(root),
        items=items,
    )



def render_source_debris_quarantine_dry_run_text(
    plan: SourceDebrisQuarantineDryRunPlan,
) -> str:
    """Return a human-readable dry-run plan."""
    return plan.summary()



def render_source_debris_quarantine_dry_run_json(
    plan: SourceDebrisQuarantineDryRunPlan,
) -> str:
    """Return a stable JSON dry-run plan."""
    return json.dumps(plan.to_dict(), indent=2, sort_keys=True) + "\n"



def _assert_can_write(path: Path, overwrite: bool) -> None:
    """Validate write target safety for explicit report writes."""
    if path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {path}")
    if not path.parent.exists() or not path.parent.is_dir():
        raise ValueError(f"output parent must be an existing directory: {path.parent}")



def write_source_debris_quarantine_dry_run_text(
    plan: SourceDebrisQuarantineDryRunPlan,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a dry-run text report when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_quarantine_dry_run_text(plan),
        encoding="utf-8",
    )
    return path



def write_source_debris_quarantine_dry_run_json(
    plan: SourceDebrisQuarantineDryRunPlan,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a dry-run JSON report when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_quarantine_dry_run_json(plan),
        encoding="utf-8",
    )
    return path


__all__ = [
    "SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW",
    "SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW",
    "SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW",
    "SOURCE_DEBRIS_QUARANTINE_DRY_RUN_ACTION",
    "SOURCE_DEBRIS_QUARANTINE_DRY_RUN_SCHEMA_VERSION",
    "SOURCE_DEBRIS_QUARANTINE_STATUS_EMPTY",
    "SOURCE_DEBRIS_QUARANTINE_STATUS_PLANNED",
    "SourceDebrisQuarantineDryRunItem",
    "SourceDebrisQuarantineDryRunPlan",
    "build_source_debris_quarantine_dry_run",
    "build_source_debris_quarantine_dry_run_from_report",
    "render_source_debris_quarantine_dry_run_json",
    "render_source_debris_quarantine_dry_run_text",
    "write_source_debris_quarantine_dry_run_json",
    "write_source_debris_quarantine_dry_run_text",
]
