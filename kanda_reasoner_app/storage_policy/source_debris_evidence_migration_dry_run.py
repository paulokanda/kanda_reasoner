"""Dry-run planner for evidence findings from source debris review.

This module refines source-debris evidence review items into exact external
architecture audit destinations. It is side-effect free on import and report
only when called: it does not create folders, copy files, move files, delete
files, or modify audit evidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.architecture_audit_resolver import (
    ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run import (
    SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW,
    SourceDebrisQuarantineDryRunItem,
    SourceDebrisQuarantineDryRunPlan,
    build_source_debris_quarantine_dry_run,
)

SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_ACTION = "dry_run_only"
SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_SCHEMA_VERSION = 1
SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_EMPTY = "empty"
SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_PLANNED = "planned"


@dataclass(frozen=True)
class SourceDebrisEvidenceMigrationDryRunItem:
    """One planned valid-evidence migration review item."""

    relative_path: str
    source_path: str
    destination_path: str
    source_exists: bool
    destination_exists: bool
    byte_count: int
    message: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "source_path": self.source_path,
            "destination_path": self.destination_path,
            "source_exists": self.source_exists,
            "destination_exists": self.destination_exists,
            "byte_count": self.byte_count,
            "message": self.message,
        }


@dataclass(frozen=True)
class SourceDebrisEvidenceMigrationDryRunPlan:
    """Dry-run plan for evidence findings from source debris review."""

    source_root: str
    project_slug: str
    action: str = SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_ACTION
    schema_version: int = SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_SCHEMA_VERSION
    items: tuple[SourceDebrisEvidenceMigrationDryRunItem, ...] = field(
        default_factory=tuple
    )

    @property
    def total_items(self) -> int:
        """Return the number of evidence migration review items."""
        return len(self.items)

    @property
    def existing_source_items(self) -> int:
        """Return the number of planned items whose source exists."""
        return sum(1 for item in self.items if item.source_exists)

    @property
    def existing_destination_items(self) -> int:
        """Return the number of planned items whose destination exists."""
        return sum(1 for item in self.items if item.destination_exists)

    def status(self) -> str:
        """Return the dry-run plan status."""
        if self.total_items == 0:
            return SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_EMPTY
        return SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_PLANNED

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "action": self.action,
            "status": self.status(),
            "source_root": self.source_root,
            "project_slug": self.project_slug,
            "total_items": self.total_items,
            "existing_source_items": self.existing_source_items,
            "existing_destination_items": self.existing_destination_items,
            "items": [item.to_dict() for item in self.items],
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable summary as lines."""
        lines = [
            "Kanda Reasoner source debris evidence migration dry-run report",
            f"Action: {self.action}",
            f"Status: {self.status()}",
            f"Source root: {self.source_root}",
            f"Project slug: {self.project_slug}",
            f"Items: {self.total_items}",
            f"Existing source items: {self.existing_source_items}",
            f"Existing destination items: {self.existing_destination_items}",
        ]

        if self.items:
            lines.append("Planned evidence migration destinations:")
            for item in self.items:
                source_status = "exists" if item.source_exists else "missing"
                destination_status = "exists" if item.destination_exists else "free"
                lines.append(
                    f"  - {item.relative_path} [{source_status}; "
                    f"destination {destination_status}] -> {item.destination_path}"
                )

        return lines

    def summary(self) -> str:
        """Return a human-readable summary."""
        return "\n".join(self.summary_lines())


def _destination_for_evidence_item(item: SourceDebrisQuarantineDryRunItem) -> Path:
    """Return the exact planned architecture audit destination for an item."""
    destination_root = normalize_path(item.planned_destination_path)
    source_filename = normalize_path(item.source_path).name

    if destination_root.name == ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER:
        return destination_root / source_filename

    return destination_root / ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER / source_filename


def _evidence_item_from_quarantine_item(
    item: SourceDebrisQuarantineDryRunItem,
) -> SourceDebrisEvidenceMigrationDryRunItem:
    """Convert a source-debris evidence review item into migration dry-run item."""
    source_path = normalize_path(item.source_path)
    destination_path = _destination_for_evidence_item(item)
    source_exists = source_path.exists()
    byte_count = source_path.stat().st_size if source_exists and source_path.is_file() else 0
    destination_exists = destination_path.exists()

    if not source_exists:
        message = "source file was not found at dry-run time"
    elif destination_exists:
        message = "destination already exists; executor must not overwrite blindly"
    else:
        message = "valid evidence candidate for external architecture audit migration"

    return SourceDebrisEvidenceMigrationDryRunItem(
        relative_path=item.relative_path,
        source_path=str(source_path),
        destination_path=str(destination_path),
        source_exists=source_exists,
        destination_exists=destination_exists,
        byte_count=byte_count,
        message=message,
    )


def build_source_debris_evidence_migration_dry_run_from_quarantine_plan(
    plan: SourceDebrisQuarantineDryRunPlan,
) -> SourceDebrisEvidenceMigrationDryRunPlan:
    """Build an evidence migration dry-run from a source debris review plan."""
    items = tuple(
        _evidence_item_from_quarantine_item(item)
        for item in plan.items
        if (
            item.planned_operation
            == SOURCE_DEBRIS_OPERATION_EVIDENCE_MIGRATION_REVIEW
            and not item.is_directory
            and normalize_path(item.source_path).suffix.lower() == ".json"
        )
    )
    return SourceDebrisEvidenceMigrationDryRunPlan(
        source_root=plan.source_root,
        project_slug=plan.project_slug,
        items=items,
    )


def build_source_debris_evidence_migration_dry_run(
    source_root: str | Path,
    *,
    maintenance_root: str | Path | None = None,
    audit_root: str | Path | None = None,
) -> SourceDebrisEvidenceMigrationDryRunPlan:
    """Build a report-only evidence migration dry-run for source debris items."""
    quarantine_plan = build_source_debris_quarantine_dry_run(
        source_root,
        maintenance_root=maintenance_root,
        audit_root=audit_root,
    )
    return build_source_debris_evidence_migration_dry_run_from_quarantine_plan(
        quarantine_plan
    )


def render_source_debris_evidence_migration_dry_run_text(
    plan: SourceDebrisEvidenceMigrationDryRunPlan,
) -> str:
    """Return a human-readable dry-run report."""
    return plan.summary()


def render_source_debris_evidence_migration_dry_run_json(
    plan: SourceDebrisEvidenceMigrationDryRunPlan,
) -> str:
    """Return a stable JSON dry-run report."""
    return json.dumps(plan.to_dict(), indent=2, sort_keys=True) + "\n"


def _assert_can_write(path: Path, overwrite: bool) -> None:
    """Validate write target safety for explicit report writes."""
    if path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {path}")
    parent = path.parent
    if not parent.exists() or not parent.is_dir():
        raise ValueError(f"output parent must be an existing directory: {parent}")


def write_source_debris_evidence_migration_dry_run_text(
    plan: SourceDebrisEvidenceMigrationDryRunPlan,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a human-readable dry-run report when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_evidence_migration_dry_run_text(plan),
        encoding="utf-8",
    )
    return path


def write_source_debris_evidence_migration_dry_run_json(
    plan: SourceDebrisEvidenceMigrationDryRunPlan,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a JSON dry-run report when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_evidence_migration_dry_run_json(plan),
        encoding="utf-8",
    )
    return path


__all__ = [
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_ACTION",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_DRY_RUN_SCHEMA_VERSION",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_EMPTY",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_STATUS_PLANNED",
    "SourceDebrisEvidenceMigrationDryRunItem",
    "SourceDebrisEvidenceMigrationDryRunPlan",
    "build_source_debris_evidence_migration_dry_run",
    "build_source_debris_evidence_migration_dry_run_from_quarantine_plan",
    "render_source_debris_evidence_migration_dry_run_json",
    "render_source_debris_evidence_migration_dry_run_text",
    "write_source_debris_evidence_migration_dry_run_json",
    "write_source_debris_evidence_migration_dry_run_text",
]
