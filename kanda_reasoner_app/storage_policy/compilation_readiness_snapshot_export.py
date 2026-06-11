"""Final compilation-readiness snapshot exporter for storage cleanup.

This module builds and exports a report-only snapshot of the source cleanup
state before compilation or build packaging. Importing and building a snapshot
are side-effect free. Only the explicit export function creates an output
folder and writes JSON/TXT review files.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.architecture_audit_resolver import (
    get_project_slug,
)
from kanda_reasoner_app.storage_policy.compilation_readiness_validator import (
    CompilationReadinessReport,
    validate_compilation_readiness,
)
from kanda_reasoner_app.storage_policy.maintenance_subfolder_policy import (
    get_maintenance_subfolder,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.source_debris_packaging_exclusion_dry_run import (
    SourceDebrisPackagingExclusionDryRunPlan,
    build_source_debris_packaging_exclusion_dry_run,
)
from kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run import (
    SourceDebrisQuarantineDryRunPlan,
    build_source_debris_quarantine_dry_run,
)

COMPILATION_READINESS_SNAPSHOT_EXPORT_ACTION = "export_readiness_snapshot_only"
COMPILATION_READINESS_SNAPSHOT_EXPORT_SCHEMA_VERSION = 1
COMPILATION_READINESS_SNAPSHOT_EXPORT_FOLDER_NAME = "compilation_readiness_snapshot"
COMPILATION_READINESS_SNAPSHOT_EXPORT_BASENAME = "compilation_readiness_snapshot"
COMPILATION_READINESS_SNAPSHOT_EXPORT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"


@dataclass(frozen=True)
class CompilationReadinessSnapshotExportPaths:
    """Canonical output paths for one readiness snapshot export."""

    source_root: str
    project_slug: str
    output_root: str
    text_path: str
    json_path: str
    run_id: str

    def to_dict(self) -> dict[str, str]:
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
class CompilationReadinessSnapshot:
    """Combined final source cleanup and compilation-readiness snapshot."""

    source_root: str
    project_slug: str
    run_id: str
    readiness: CompilationReadinessReport
    source_debris: SourceDebrisQuarantineDryRunPlan
    packaging_exclusion: SourceDebrisPackagingExclusionDryRunPlan
    action: str = COMPILATION_READINESS_SNAPSHOT_EXPORT_ACTION
    schema_version: int = COMPILATION_READINESS_SNAPSHOT_EXPORT_SCHEMA_VERSION

    @property
    def readiness_status(self) -> str:
        """Return the stable compilation-readiness status."""
        return self.readiness.status()

    @property
    def blocking_source_failures(self) -> int:
        """Return the number of blocking source failures."""
        return self.readiness.blocking_source_failures

    @property
    def blocking_secret_findings(self) -> int:
        """Return the number of blocking high-confidence secret findings."""
        return self.readiness.blocking_secret_findings

    @property
    def advisory_warnings(self) -> int:
        """Return the number of non-blocking warnings."""
        return self.readiness.advisory_warnings

    @property
    def total_findings(self) -> int:
        """Return all findings considered by readiness validation."""
        return self.readiness.total_findings

    @property
    def source_debris_items(self) -> int:
        """Return source debris review item count."""
        return self.source_debris.total_items

    @property
    def quarantine_review_items(self) -> int:
        """Return remaining quarantine-review item count."""
        return self.source_debris.quarantine_review_items

    @property
    def evidence_migration_review_items(self) -> int:
        """Return remaining evidence-migration item count."""
        return self.source_debris.evidence_migration_review_items

    @property
    def packaging_exclusion_review_items(self) -> int:
        """Return remaining packaging-exclusion item count."""
        return self.source_debris.packaging_exclusion_review_items

    @property
    def packaging_exclusion_status(self) -> str:
        """Return packaging exclusion coverage status."""
        return self.packaging_exclusion.status()

    @property
    def is_compilation_unblocked(self) -> bool:
        """Return True when no blocking source or secret findings remain."""
        return (
            self.blocking_source_failures == 0
            and self.blocking_secret_findings == 0
        )

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "action": self.action,
            "source_root": self.source_root,
            "project_slug": self.project_slug,
            "run_id": self.run_id,
            "is_compilation_unblocked": self.is_compilation_unblocked,
            "readiness": {
                "status": self.readiness_status,
                "blocking_source_failures": self.blocking_source_failures,
                "blocking_high_confidence_secret_findings": (
                    self.blocking_secret_findings
                ),
                "advisory_warnings": self.advisory_warnings,
                "total_findings": self.total_findings,
            },
            "source_debris": {
                "status": self.source_debris.status(),
                "total_items": self.source_debris_items,
                "quarantine_review_items": self.quarantine_review_items,
                "evidence_migration_review_items": (
                    self.evidence_migration_review_items
                ),
                "packaging_exclusion_review_items": (
                    self.packaging_exclusion_review_items
                ),
            },
            "packaging_exclusion": {
                "status": self.packaging_exclusion_status,
                "total_items": self.packaging_exclusion.total_items,
                "covered_items": self.packaging_exclusion.covered_items,
                "uncovered_items": self.packaging_exclusion.uncovered_items,
            },
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable summary as lines."""
        lines = [
            "Kanda Reasoner final compilation-readiness snapshot",
            f"Action: {self.action}",
            f"Source root: {self.source_root}",
            f"Project slug: {self.project_slug}",
            f"Run id: {self.run_id}",
            f"Compilation unblocked: {self.is_compilation_unblocked}",
            f"Readiness status: {self.readiness_status}",
            f"Blocking source failures: {self.blocking_source_failures}",
            "Blocking high-confidence secret findings: "
            f"{self.blocking_secret_findings}",
            f"Advisory warnings: {self.advisory_warnings}",
            f"Total findings: {self.total_findings}",
            f"Source debris review items: {self.source_debris_items}",
            f"Quarantine review items: {self.quarantine_review_items}",
            "Evidence migration review items: "
            f"{self.evidence_migration_review_items}",
            "Packaging exclusion review items: "
            f"{self.packaging_exclusion_review_items}",
            f"Packaging exclusion status: {self.packaging_exclusion_status}",
            f"Packaging covered items: {self.packaging_exclusion.covered_items}",
            f"Packaging uncovered items: {self.packaging_exclusion.uncovered_items}",
        ]
        return lines

    def summary(self) -> str:
        """Return a human-readable summary."""
        return "\n".join(self.summary_lines())


@dataclass(frozen=True)
class CompilationReadinessSnapshotExportResult:
    """Result returned after writing a readiness snapshot export."""

    paths: CompilationReadinessSnapshotExportPaths
    snapshot: CompilationReadinessSnapshot

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.snapshot.schema_version,
            "action": self.snapshot.action,
            "paths": self.paths.to_dict(),
            "snapshot": self.snapshot.to_dict(),
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable summary as lines."""
        lines = self.snapshot.summary_lines()
        lines.extend(
            [
                f"Output root: {self.paths.output_root}",
                f"Text report: {self.paths.text_path}",
                f"JSON report: {self.paths.json_path}",
            ]
        )
        return lines

    def summary(self) -> str:
        """Return a human-readable summary."""
        return "\n".join(self.summary_lines())


def build_compilation_readiness_snapshot_run_id(
    now: datetime | None = None,
) -> str:
    """Return a stable run id for a readiness snapshot export."""
    value = now or datetime.now()
    return value.strftime(COMPILATION_READINESS_SNAPSHOT_EXPORT_TIMESTAMP_FORMAT)


def build_compilation_readiness_snapshot_export_paths(
    source_root: str | Path,
    *,
    maintenance_root: str | Path | None = None,
    run_id: str | None = None,
) -> CompilationReadinessSnapshotExportPaths:
    """Return canonical snapshot export paths without creating folders."""
    root = normalize_path(source_root)
    project_slug = get_project_slug(root)
    actual_run_id = run_id or build_compilation_readiness_snapshot_run_id()
    audit_root = get_maintenance_subfolder("audit_logs", maintenance_root)
    output_root = (
        audit_root
        / COMPILATION_READINESS_SNAPSHOT_EXPORT_FOLDER_NAME
        / project_slug
        / actual_run_id
    )
    text_path = output_root / f"{COMPILATION_READINESS_SNAPSHOT_EXPORT_BASENAME}.txt"
    json_path = output_root / f"{COMPILATION_READINESS_SNAPSHOT_EXPORT_BASENAME}.json"
    return CompilationReadinessSnapshotExportPaths(
        source_root=str(root),
        project_slug=project_slug,
        output_root=str(output_root),
        text_path=str(text_path),
        json_path=str(json_path),
        run_id=actual_run_id,
    )


def build_compilation_readiness_snapshot(
    source_root: str | Path,
    *,
    run_id: str | None = None,
) -> CompilationReadinessSnapshot:
    """Build a final readiness snapshot without writing files."""
    root = normalize_path(source_root)
    actual_run_id = run_id or build_compilation_readiness_snapshot_run_id()
    return CompilationReadinessSnapshot(
        source_root=str(root),
        project_slug=get_project_slug(root),
        run_id=actual_run_id,
        readiness=validate_compilation_readiness(root),
        source_debris=build_source_debris_quarantine_dry_run(root),
        packaging_exclusion=build_source_debris_packaging_exclusion_dry_run(root),
    )


def _ensure_write_target(path: str | Path, overwrite: bool) -> Path:
    """Return a normalized write path after validating write safety."""
    target = normalize_path(path)
    if not target.parent.exists():
        raise ValueError(f"parent folder does not exist: {target.parent}")
    if target.exists() and not overwrite:
        raise FileExistsError(f"output file already exists: {target}")
    return target


def render_compilation_readiness_snapshot_text(
    snapshot: CompilationReadinessSnapshot,
) -> str:
    """Return a human-readable snapshot."""
    return snapshot.summary()


def render_compilation_readiness_snapshot_json(
    snapshot: CompilationReadinessSnapshot,
) -> str:
    """Return a JSON snapshot."""
    return json.dumps(snapshot.to_dict(), indent=2, sort_keys=True)


def write_compilation_readiness_snapshot_text(
    snapshot: CompilationReadinessSnapshot,
    path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a human-readable snapshot to path."""
    target = _ensure_write_target(path, overwrite)
    target.write_text(
        render_compilation_readiness_snapshot_text(snapshot),
        encoding="utf-8",
    )
    return target


def write_compilation_readiness_snapshot_json(
    snapshot: CompilationReadinessSnapshot,
    path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a JSON snapshot to path."""
    target = _ensure_write_target(path, overwrite)
    target.write_text(
        render_compilation_readiness_snapshot_json(snapshot),
        encoding="utf-8",
    )
    return target


def export_compilation_readiness_snapshot(
    source_root: str | Path,
    *,
    maintenance_root: str | Path | None = None,
    run_id: str | None = None,
    overwrite: bool = False,
) -> CompilationReadinessSnapshotExportResult:
    """Build and write a final readiness snapshot export."""
    paths = build_compilation_readiness_snapshot_export_paths(
        source_root,
        maintenance_root=maintenance_root,
        run_id=run_id,
    )
    output_root = normalize_path(paths.output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    snapshot = build_compilation_readiness_snapshot(
        source_root,
        run_id=paths.run_id,
    )
    write_compilation_readiness_snapshot_text(
        snapshot,
        paths.text_path,
        overwrite=overwrite,
    )
    write_compilation_readiness_snapshot_json(
        snapshot,
        paths.json_path,
        overwrite=overwrite,
    )
    return CompilationReadinessSnapshotExportResult(
        paths=paths,
        snapshot=snapshot,
    )


def render_compilation_readiness_snapshot_export_text(
    result: CompilationReadinessSnapshotExportResult,
) -> str:
    """Return a human-readable export result."""
    return result.summary()


def render_compilation_readiness_snapshot_export_json(
    result: CompilationReadinessSnapshotExportResult,
) -> str:
    """Return a JSON export result."""
    return json.dumps(result.to_dict(), indent=2, sort_keys=True)


__all__ = [
    "COMPILATION_READINESS_SNAPSHOT_EXPORT_ACTION",
    "COMPILATION_READINESS_SNAPSHOT_EXPORT_BASENAME",
    "COMPILATION_READINESS_SNAPSHOT_EXPORT_FOLDER_NAME",
    "COMPILATION_READINESS_SNAPSHOT_EXPORT_SCHEMA_VERSION",
    "COMPILATION_READINESS_SNAPSHOT_EXPORT_TIMESTAMP_FORMAT",
    "CompilationReadinessSnapshot",
    "CompilationReadinessSnapshotExportPaths",
    "CompilationReadinessSnapshotExportResult",
    "build_compilation_readiness_snapshot",
    "build_compilation_readiness_snapshot_export_paths",
    "build_compilation_readiness_snapshot_run_id",
    "export_compilation_readiness_snapshot",
    "render_compilation_readiness_snapshot_export_json",
    "render_compilation_readiness_snapshot_export_text",
    "render_compilation_readiness_snapshot_json",
    "render_compilation_readiness_snapshot_text",
    "write_compilation_readiness_snapshot_json",
    "write_compilation_readiness_snapshot_text",
]
