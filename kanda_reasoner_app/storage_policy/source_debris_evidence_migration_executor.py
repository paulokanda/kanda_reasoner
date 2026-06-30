# project-path: kanda_reasoner_app/storage_policy/source_debris_evidence_migration_executor.py
"""Executor for reviewed source-debris evidence migration.

This module executes only evidence migration dry-run items produced by
source_debris_evidence_migration_dry_run. Execution requires an exact
confirmation token. Import is side-effect free: it does not create folders,
copy files, move files, delete files, or inspect the live source tree.

The executor is conservative. It copies each source JSON file to the external
architecture audit destination, verifies the destination SHA-256 hash, and only
then removes the source file. It refuses to overwrite existing destinations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import shutil

from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.source_debris_evidence_migration_dry_run import (
    SourceDebrisEvidenceMigrationDryRunItem,
    SourceDebrisEvidenceMigrationDryRunPlan,
    build_source_debris_evidence_migration_dry_run,
)

SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_ACTION = (
    "copy_verify_and_remove_source_evidence"
)
SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_SCHEMA_VERSION = 1
SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN = (
    "MIGRATE_SOURCE_DEBRIS_EVIDENCE_TO_ARCHITECTURE_AUDIT"
)
SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_CONFIRMATION_REQUIRED = (
    "confirmation_required"
)
SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_COMPLETED = "completed"
SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_FAILED = "failed"
SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_SKIPPED_EMPTY = "skipped_empty"
SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_MOVED_VERIFIED = "moved_verified"
SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_SKIPPED_MISSING = "skipped_missing"
SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_DESTINATION_EXISTS = (
    "failed_destination_exists"
)
SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_VERIFICATION = (
    "failed_verification"
)
SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_SOURCE_REMOVAL = (
    "failed_source_removal"
)
SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED = "failed"


@dataclass(frozen=True)
class SourceDebrisEvidenceMigrationExecutionItem:
    """One source-debris evidence migration execution result item."""

    relative_path: str
    source_path: str
    destination_path: str
    status: str
    byte_count: int
    sha256_before: str = ""
    sha256_after: str = ""
    message: str = ""

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "source_path": self.source_path,
            "destination_path": self.destination_path,
            "status": self.status,
            "byte_count": self.byte_count,
            "sha256_before": self.sha256_before,
            "sha256_after": self.sha256_after,
            "message": self.message,
        }


@dataclass(frozen=True)
class SourceDebrisEvidenceMigrationExecutionResult:
    """Result of explicit source-debris evidence migration execution."""

    source_root: str
    project_slug: str
    status: str
    confirmation_token_required: str
    action: str = SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_ACTION
    schema_version: int = SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_SCHEMA_VERSION
    items: tuple[SourceDebrisEvidenceMigrationExecutionItem, ...] = field(
        default_factory=tuple
    )

    @property
    def total_items(self) -> int:
        """Return the total execution item count."""
        return len(self.items)

    @property
    def moved_items(self) -> int:
        """Return the number of moved and verified items."""
        return sum(
            1
            for item in self.items
            if item.status == SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_MOVED_VERIFIED
        )

    @property
    def skipped_items(self) -> int:
        """Return the number of skipped items."""
        return sum(1 for item in self.items if item.status.startswith("skipped"))

    @property
    def failed_items(self) -> int:
        """Return the number of failed items."""
        return sum(1 for item in self.items if item.status.startswith("failed"))

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "action": self.action,
            "status": self.status,
            "source_root": self.source_root,
            "project_slug": self.project_slug,
            "confirmation_token_required": self.confirmation_token_required,
            "total_items": self.total_items,
            "moved_items": self.moved_items,
            "skipped_items": self.skipped_items,
            "failed_items": self.failed_items,
            "items": [item.to_dict() for item in self.items],
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable summary as lines."""
        lines = [
            "Kanda Reasoner source debris evidence migration execution result",
            f"Action: {self.action}",
            f"Status: {self.status}",
            f"Source root: {self.source_root}",
            f"Project slug: {self.project_slug}",
            f"Items: {self.total_items}",
            f"Moved items: {self.moved_items}",
            f"Skipped items: {self.skipped_items}",
            f"Failed items: {self.failed_items}",
        ]
        if self.items:
            lines.append("Execution items:")
            for item in self.items:
                lines.append(
                    f"  - {item.relative_path} [{item.status}] -> "
                    f"{item.destination_path or 'not moved'}"
                )
        return lines

    def summary(self) -> str:
        """Return a human-readable summary."""
        return "\n".join(self.summary_lines())


def calculate_source_debris_evidence_sha256(path: str | Path) -> str:
    """Return the SHA-256 digest for a file."""
    target = normalize_path(path)
    digest = hashlib.sha256()
    with target.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _confirmation_required_result(
    plan: SourceDebrisEvidenceMigrationDryRunPlan,
) -> SourceDebrisEvidenceMigrationExecutionResult:
    """Return a no-move result when confirmation is missing."""
    return SourceDebrisEvidenceMigrationExecutionResult(
        source_root=plan.source_root,
        project_slug=plan.project_slug,
        status=SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_CONFIRMATION_REQUIRED,
        confirmation_token_required=(
            SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
        ),
        items=(),
    )


def _skipped_missing_item(
    item: SourceDebrisEvidenceMigrationDryRunItem,
) -> SourceDebrisEvidenceMigrationExecutionItem:
    """Return a skipped item for a missing source file."""
    return SourceDebrisEvidenceMigrationExecutionItem(
        relative_path=item.relative_path,
        source_path=item.source_path,
        destination_path=item.destination_path,
        status=SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_SKIPPED_MISSING,
        byte_count=0,
        message="source file was not found at execution time",
    )


def _destination_exists_item(
    item: SourceDebrisEvidenceMigrationDryRunItem,
) -> SourceDebrisEvidenceMigrationExecutionItem:
    """Return a failed item when destination already exists."""
    return SourceDebrisEvidenceMigrationExecutionItem(
        relative_path=item.relative_path,
        source_path=item.source_path,
        destination_path=item.destination_path,
        status=SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_DESTINATION_EXISTS,
        byte_count=item.byte_count,
        message="destination already exists; refusing to overwrite",
    )


def _copy_verify_and_remove_item(
    item: SourceDebrisEvidenceMigrationDryRunItem,
) -> SourceDebrisEvidenceMigrationExecutionItem:
    """Copy, verify, and remove one source evidence JSON item."""
    source_path = normalize_path(item.source_path)
    destination_path = normalize_path(item.destination_path)

    if not source_path.exists() or not source_path.is_file():
        return _skipped_missing_item(item)

    if destination_path.exists():
        return _destination_exists_item(item)

    try:
        source_hash = calculate_source_debris_evidence_sha256(source_path)
        byte_count = source_path.stat().st_size
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)
        destination_hash = calculate_source_debris_evidence_sha256(destination_path)
    except OSError as exc:
        return SourceDebrisEvidenceMigrationExecutionItem(
            relative_path=item.relative_path,
            source_path=str(source_path),
            destination_path=str(destination_path),
            status=SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED,
            byte_count=item.byte_count,
            message=f"copy failed: {exc}",
        )

    if source_hash != destination_hash:
        return SourceDebrisEvidenceMigrationExecutionItem(
            relative_path=item.relative_path,
            source_path=str(source_path),
            destination_path=str(destination_path),
            status=SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_VERIFICATION,
            byte_count=byte_count,
            sha256_before=source_hash,
            sha256_after=destination_hash,
            message="destination hash did not match source hash; source preserved",
        )

    try:
        source_path.unlink()
    except OSError as exc:
        return SourceDebrisEvidenceMigrationExecutionItem(
            relative_path=item.relative_path,
            source_path=str(source_path),
            destination_path=str(destination_path),
            status=SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_SOURCE_REMOVAL,
            byte_count=byte_count,
            sha256_before=source_hash,
            sha256_after=destination_hash,
            message=f"copied and verified, but source removal failed: {exc}",
        )

    return SourceDebrisEvidenceMigrationExecutionItem(
        relative_path=item.relative_path,
        source_path=str(source_path),
        destination_path=str(destination_path),
        status=SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_MOVED_VERIFIED,
        byte_count=byte_count,
        sha256_before=source_hash,
        sha256_after=destination_hash,
        message="copied, hash-verified, and source file removed",
    )


def execute_source_debris_evidence_migration_plan(
    plan: SourceDebrisEvidenceMigrationDryRunPlan,
    *,
    confirmation_token: str | None = None,
) -> SourceDebrisEvidenceMigrationExecutionResult:
    """Execute evidence migration from an existing dry-run plan."""
    if confirmation_token != SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN:
        return _confirmation_required_result(plan)

    if not plan.items:
        return SourceDebrisEvidenceMigrationExecutionResult(
            source_root=plan.source_root,
            project_slug=plan.project_slug,
            status=SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_SKIPPED_EMPTY,
            confirmation_token_required=(
                SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
            ),
            items=(),
        )

    items = tuple(_copy_verify_and_remove_item(item) for item in plan.items)
    if any(item.status.startswith("failed") for item in items):
        status = SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_FAILED
    else:
        status = SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_COMPLETED

    return SourceDebrisEvidenceMigrationExecutionResult(
        source_root=plan.source_root,
        project_slug=plan.project_slug,
        status=status,
        confirmation_token_required=(
            SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN
        ),
        items=items,
    )


def execute_source_debris_evidence_migration(
    source_root: str | Path,
    *,
    maintenance_root: str | Path | None = None,
    audit_root: str | Path | None = None,
    confirmation_token: str | None = None,
) -> SourceDebrisEvidenceMigrationExecutionResult:
    """Build a dry-run plan and execute reviewed evidence migration."""
    plan = build_source_debris_evidence_migration_dry_run(
        source_root,
        maintenance_root=maintenance_root,
        audit_root=audit_root,
    )
    return execute_source_debris_evidence_migration_plan(
        plan,
        confirmation_token=confirmation_token,
    )


def render_source_debris_evidence_migration_execution_text(
    result: SourceDebrisEvidenceMigrationExecutionResult,
) -> str:
    """Return a human-readable execution result."""
    return result.summary()


def render_source_debris_evidence_migration_execution_json(
    result: SourceDebrisEvidenceMigrationExecutionResult,
) -> str:
    """Return a stable JSON execution result."""
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"


def _assert_can_write(path: Path, overwrite: bool) -> None:
    """Validate explicit result write target safety."""
    if path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {path}")
    if not path.parent.exists() or not path.parent.is_dir():
        raise ValueError(f"output parent must be an existing directory: {path.parent}")


def write_source_debris_evidence_migration_execution_text(
    result: SourceDebrisEvidenceMigrationExecutionResult,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write an execution text result when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_evidence_migration_execution_text(result),
        encoding="utf-8",
    )
    return path


def write_source_debris_evidence_migration_execution_json(
    result: SourceDebrisEvidenceMigrationExecutionResult,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write an execution JSON result when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_evidence_migration_execution_json(result),
        encoding="utf-8",
    )
    return path


__all__ = [
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_ACTION",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_CONFIRMATION_TOKEN",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_SCHEMA_VERSION",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_COMPLETED",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_CONFIRMATION_REQUIRED",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_FAILED",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_EXECUTOR_STATUS_SKIPPED_EMPTY",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_DESTINATION_EXISTS",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_SOURCE_REMOVAL",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_FAILED_VERIFICATION",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_MOVED_VERIFIED",
    "SOURCE_DEBRIS_EVIDENCE_MIGRATION_ITEM_STATUS_SKIPPED_MISSING",
    "SourceDebrisEvidenceMigrationExecutionItem",
    "SourceDebrisEvidenceMigrationExecutionResult",
    "calculate_source_debris_evidence_sha256",
    "execute_source_debris_evidence_migration",
    "execute_source_debris_evidence_migration_plan",
    "render_source_debris_evidence_migration_execution_json",
    "render_source_debris_evidence_migration_execution_text",
    "write_source_debris_evidence_migration_execution_json",
    "write_source_debris_evidence_migration_execution_text",
]
