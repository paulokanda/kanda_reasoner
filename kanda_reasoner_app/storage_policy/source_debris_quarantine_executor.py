"""Executor for reviewed source debris quarantine moves.

This module performs only one kind of operation: moving items that were already
classified by the dry-run planner as maintenance-quarantine review items. It
never moves evidence-migration review items and never moves packaging-exclusion
review items. Actual movement requires an explicit confirmation token.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import shutil

from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run import (
    SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW,
    SourceDebrisQuarantineDryRunItem,
    SourceDebrisQuarantineDryRunPlan,
    build_source_debris_quarantine_dry_run,
)

SOURCE_DEBRIS_QUARANTINE_EXECUTOR_ACTION = "move_quarantine_review_items"
SOURCE_DEBRIS_QUARANTINE_EXECUTOR_SCHEMA_VERSION = 1
SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN = (
    "MOVE_SOURCE_DEBRIS_TO_QUARANTINE"
)
SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_CONFIRMATION_REQUIRED = (
    "confirmation_required"
)
SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_COMPLETED = "completed"
SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_FAILED = "failed"
SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_SKIPPED_EMPTY = "skipped_empty"
SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_MOVED = "moved"
SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_NON_QUARANTINE = (
    "skipped_non_quarantine"
)
SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_MISSING = "skipped_missing"
SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED_DESTINATION_EXISTS = (
    "failed_destination_exists"
)
SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED = "failed"


@dataclass(frozen=True)
class SourceDebrisQuarantineExecutionItem:
    """One source debris quarantine execution result item."""

    relative_path: str
    source_path: str
    destination_path: str
    planned_operation: str
    status: str
    message: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "source_path": self.source_path,
            "destination_path": self.destination_path,
            "planned_operation": self.planned_operation,
            "status": self.status,
            "message": self.message,
        }


@dataclass(frozen=True)
class SourceDebrisQuarantineExecutionResult:
    """Result of an explicit source debris quarantine execution."""

    source_root: str
    project_slug: str
    status: str
    confirmation_token_required: str
    action: str = SOURCE_DEBRIS_QUARANTINE_EXECUTOR_ACTION
    schema_version: int = SOURCE_DEBRIS_QUARANTINE_EXECUTOR_SCHEMA_VERSION
    items: tuple[SourceDebrisQuarantineExecutionItem, ...] = field(
        default_factory=tuple
    )

    @property
    def total_items(self) -> int:
        """Return the total execution item count."""
        return len(self.items)

    @property
    def moved_items(self) -> int:
        """Return the number of moved items."""
        return sum(
            1
            for item in self.items
            if item.status == SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_MOVED
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
            "Kanda Reasoner source debris quarantine execution result",
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



def _confirmation_required_result(
    plan: SourceDebrisQuarantineDryRunPlan,
) -> SourceDebrisQuarantineExecutionResult:
    """Return a no-move result when confirmation is missing."""
    return SourceDebrisQuarantineExecutionResult(
        source_root=plan.source_root,
        project_slug=plan.project_slug,
        status=SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_CONFIRMATION_REQUIRED,
        confirmation_token_required=(
            SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN
        ),
        items=(),
    )



def _non_quarantine_item(
    item: SourceDebrisQuarantineDryRunItem,
) -> SourceDebrisQuarantineExecutionItem:
    """Return a skipped item for a non-quarantine review operation."""
    return SourceDebrisQuarantineExecutionItem(
        relative_path=item.relative_path,
        source_path=item.source_path,
        destination_path="",
        planned_operation=item.planned_operation,
        status=SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_NON_QUARANTINE,
        message="item is review-only and is not a quarantine move candidate",
    )



def _missing_source_item(
    item: SourceDebrisQuarantineDryRunItem,
) -> SourceDebrisQuarantineExecutionItem:
    """Return a skipped item for a missing source path."""
    return SourceDebrisQuarantineExecutionItem(
        relative_path=item.relative_path,
        source_path=item.source_path,
        destination_path=item.planned_destination_path,
        planned_operation=item.planned_operation,
        status=SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_MISSING,
        message="source path was not found at execution time",
    )



def _destination_exists_item(
    item: SourceDebrisQuarantineDryRunItem,
) -> SourceDebrisQuarantineExecutionItem:
    """Return a failed item when destination already exists."""
    return SourceDebrisQuarantineExecutionItem(
        relative_path=item.relative_path,
        source_path=item.source_path,
        destination_path=item.planned_destination_path,
        planned_operation=item.planned_operation,
        status=SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED_DESTINATION_EXISTS,
        message="destination already exists; refusing to overwrite",
    )



def _move_quarantine_item(
    item: SourceDebrisQuarantineDryRunItem,
) -> SourceDebrisQuarantineExecutionItem:
    """Move one quarantine item to its planned destination."""
    source_path = normalize_path(item.source_path)
    destination_path = normalize_path(item.planned_destination_path)

    if not source_path.exists():
        return _missing_source_item(item)

    if destination_path.exists():
        return _destination_exists_item(item)

    try:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source_path), str(destination_path))
    except OSError as exc:
        return SourceDebrisQuarantineExecutionItem(
            relative_path=item.relative_path,
            source_path=str(source_path),
            destination_path=str(destination_path),
            planned_operation=item.planned_operation,
            status=SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED,
            message=f"move failed: {exc}",
        )

    return SourceDebrisQuarantineExecutionItem(
        relative_path=item.relative_path,
        source_path=str(source_path),
        destination_path=str(destination_path),
        planned_operation=item.planned_operation,
        status=SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_MOVED,
        message="moved to maintenance quarantine",
    )



def execute_source_debris_quarantine_plan(
    plan: SourceDebrisQuarantineDryRunPlan,
    *,
    confirmation_token: str | None = None,
) -> SourceDebrisQuarantineExecutionResult:
    """Execute quarantine moves from an existing dry-run plan.

    Only items with planned_operation == quarantine_review are moved. Evidence
    migration review and packaging exclusion review items are always skipped.
    """
    if confirmation_token != SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN:
        return _confirmation_required_result(plan)

    result_items: list[SourceDebrisQuarantineExecutionItem] = []
    for item in plan.items:
        if item.planned_operation != SOURCE_DEBRIS_OPERATION_QUARANTINE_REVIEW:
            result_items.append(_non_quarantine_item(item))
            continue
        result_items.append(_move_quarantine_item(item))

    items = tuple(result_items)
    if not items:
        status = SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_SKIPPED_EMPTY
    elif any(item.status.startswith("failed") for item in items):
        status = SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_FAILED
    else:
        status = SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_COMPLETED

    return SourceDebrisQuarantineExecutionResult(
        source_root=plan.source_root,
        project_slug=plan.project_slug,
        status=status,
        confirmation_token_required=(
            SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN
        ),
        items=items,
    )



def execute_source_debris_quarantine(
    source_root: str | Path,
    *,
    maintenance_root: str | Path | None = None,
    audit_root: str | Path | None = None,
    confirmation_token: str | None = None,
) -> SourceDebrisQuarantineExecutionResult:
    """Build a dry-run plan and execute reviewed quarantine moves."""
    plan = build_source_debris_quarantine_dry_run(
        source_root,
        maintenance_root=maintenance_root,
        audit_root=audit_root,
    )
    return execute_source_debris_quarantine_plan(
        plan,
        confirmation_token=confirmation_token,
    )



def render_source_debris_quarantine_execution_text(
    result: SourceDebrisQuarantineExecutionResult,
) -> str:
    """Return a human-readable execution result."""
    return result.summary()



def render_source_debris_quarantine_execution_json(
    result: SourceDebrisQuarantineExecutionResult,
) -> str:
    """Return a stable JSON execution result."""
    return json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n"



def _assert_can_write(path: Path, overwrite: bool) -> None:
    """Validate explicit result write target safety."""
    if path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {path}")
    if not path.parent.exists() or not path.parent.is_dir():
        raise ValueError(f"output parent must be an existing directory: {path.parent}")



def write_source_debris_quarantine_execution_text(
    result: SourceDebrisQuarantineExecutionResult,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write an execution text result when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_quarantine_execution_text(result),
        encoding="utf-8",
    )
    return path



def write_source_debris_quarantine_execution_json(
    result: SourceDebrisQuarantineExecutionResult,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write an execution JSON result when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_quarantine_execution_json(result),
        encoding="utf-8",
    )
    return path


__all__ = [
    "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_ACTION",
    "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_CONFIRMATION_TOKEN",
    "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_SCHEMA_VERSION",
    "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_COMPLETED",
    "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_CONFIRMATION_REQUIRED",
    "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_FAILED",
    "SOURCE_DEBRIS_QUARANTINE_EXECUTOR_STATUS_SKIPPED_EMPTY",
    "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED",
    "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_FAILED_DESTINATION_EXISTS",
    "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_MOVED",
    "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_MISSING",
    "SOURCE_DEBRIS_QUARANTINE_ITEM_STATUS_SKIPPED_NON_QUARANTINE",
    "SourceDebrisQuarantineExecutionItem",
    "SourceDebrisQuarantineExecutionResult",
    "execute_source_debris_quarantine",
    "execute_source_debris_quarantine_plan",
    "render_source_debris_quarantine_execution_json",
    "render_source_debris_quarantine_execution_text",
    "write_source_debris_quarantine_execution_json",
    "write_source_debris_quarantine_execution_text",
]
