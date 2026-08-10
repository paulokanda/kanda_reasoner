# project-path: kanda_reasoner_app/storage_policy/evidence_relocator.py
"""Explicit evidence relocation executor for old project_analysis_evidence.

This module executes a previously dry-run evidence relocation plan only when an
exact confirmation token is provided. It is intentionally conservative: import is
side-effect free, review items are not relocated, source files are not deleted in
copy-only mode, and move mode deletes source files only after destination hash
verification succeeds.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import shutil

from kanda_reasoner_app.storage_policy.evidence_relocation_dry_run import (
    EVIDENCE_RELOCATION_CATEGORY_JSON,
    EVIDENCE_RELOCATION_STATUS_ABSENT,
    EVIDENCE_RELOCATION_STATUS_REVIEW_REQUIRED,
    EvidenceRelocationItem,
    EvidenceRelocationPlan,
    plan_evidence_relocation_dry_run,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path

EVIDENCE_RELOCATOR_ACTION = "explicit_confirmed_relocation"
EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN = "RELOCATE_PROJECT_ANALYSIS_EVIDENCE"
EVIDENCE_RELOCATOR_MODE_COPY_ONLY = "copy_only"
EVIDENCE_RELOCATOR_MODE_MOVE_VERIFIED = "move_verified"
EVIDENCE_RELOCATOR_STATUS_COMPLETED = "completed"
EVIDENCE_RELOCATOR_STATUS_CONFIRMATION_REQUIRED = "confirmation_required"
EVIDENCE_RELOCATOR_STATUS_FAILED = "failed"
EVIDENCE_RELOCATOR_STATUS_REVIEW_REQUIRED = "review_required"
EVIDENCE_RELOCATOR_STATUS_SKIPPED_ABSENT = "skipped_absent"
EVIDENCE_RELOCATOR_ITEM_STATUS_COPIED = "copied"
EVIDENCE_RELOCATOR_ITEM_STATUS_MOVED = "moved_verified"
EVIDENCE_RELOCATOR_ITEM_STATUS_SKIPPED = "skipped"
EVIDENCE_RELOCATOR_ITEM_STATUS_FAILED = "failed"


@dataclass(frozen=True)
class EvidenceRelocationExecutionItem:
    """One executed or skipped evidence relocation item."""

    relative_path: str
    source_path: str
    destination_path: str
    category: str
    operation: str
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
            "category": self.category,
            "operation": self.operation,
            "status": self.status,
            "byte_count": self.byte_count,
            "sha256_before": self.sha256_before,
            "sha256_after": self.sha256_after,
            "message": self.message,
        }


@dataclass(frozen=True)
class EvidenceRelocationExecutionResult:
    """Result of an explicitly confirmed evidence relocation execution."""

    project_root: str
    source_evidence_root: str
    architecture_audit_root: str
    action: str = EVIDENCE_RELOCATOR_ACTION
    mode: str = EVIDENCE_RELOCATOR_MODE_COPY_ONLY
    status_value: str = EVIDENCE_RELOCATOR_STATUS_COMPLETED
    items: tuple[EvidenceRelocationExecutionItem, ...] = field(default_factory=tuple)
    skipped_review_items: tuple[EvidenceRelocationExecutionItem, ...] = field(
        default_factory=tuple
    )
    message: str = ""

    @property
    def total_items(self) -> int:
        """Return the total number of processed JSON evidence items."""
        return len(self.items)

    @property
    def copied_items(self) -> int:
        """Return the number of copied items."""
        return sum(
            1
            for item in self.items
            if item.status == EVIDENCE_RELOCATOR_ITEM_STATUS_COPIED
        )

    @property
    def moved_items(self) -> int:
        """Return the number of moved-and-verified items."""
        return sum(
            1
            for item in self.items
            if item.status == EVIDENCE_RELOCATOR_ITEM_STATUS_MOVED
        )

    @property
    def failed_items(self) -> int:
        """Return the number of failed items."""
        return sum(
            1
            for item in self.items
            if item.status == EVIDENCE_RELOCATOR_ITEM_STATUS_FAILED
        )

    @property
    def skipped_items(self) -> int:
        """Return the number of skipped review items."""
        return len(self.skipped_review_items)

    def status(self) -> str:
        """Return the execution status."""
        if self.failed_items:
            return EVIDENCE_RELOCATOR_STATUS_FAILED
        return self.status_value

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "action": self.action,
            "mode": self.mode,
            "status": self.status(),
            "project_root": self.project_root,
            "source_evidence_root": self.source_evidence_root,
            "architecture_audit_root": self.architecture_audit_root,
            "total_items": self.total_items,
            "copied_items": self.copied_items,
            "moved_items": self.moved_items,
            "failed_items": self.failed_items,
            "skipped_items": self.skipped_items,
            "message": self.message,
            "items": [item.to_dict() for item in self.items],
            "skipped_review_items": [item.to_dict() for item in self.skipped_review_items],
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable execution summary."""
        lines = [
            "Kanda Reasoner evidence relocator report",
            f"Action: {self.action}",
            f"Mode: {self.mode}",
            f"Status: {self.status()}",
            f"Project root: {self.project_root}",
            f"Source evidence root: {self.source_evidence_root}",
            f"Architecture audit root: {self.architecture_audit_root}",
            f"Processed items: {self.total_items}",
            f"Copied items: {self.copied_items}",
            f"Moved items: {self.moved_items}",
            f"Failed items: {self.failed_items}",
            f"Skipped review items: {self.skipped_items}",
        ]
        if self.message:
            lines.append(f"Message: {self.message}")
        if self.items:
            lines.append("Items:")
            for item in self.items:
                lines.append(
                    f"  - {item.relative_path} [{item.status}] -> "
                    f"{item.destination_path}"
                )
        if self.skipped_review_items:
            lines.append("Skipped review items:")
            for item in self.skipped_review_items:
                lines.append(
                    f"  - {item.relative_path} [{item.status}] -> "
                    f"{item.destination_path}"
                )
        return lines

    def summary(self) -> str:
        """Return a human-readable execution summary."""
        return "\n".join(self.summary_lines())


def calculate_file_sha256(path: str | Path) -> str:
    """Return the SHA-256 digest for a file."""
    target = normalize_path(path)
    digest = hashlib.sha256()
    with target.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _assert_confirmed(confirmation_token: str) -> None:
    """Raise when the exact relocation confirmation token is missing."""
    if confirmation_token != EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN:
        raise ValueError(
            "Evidence relocation requires exact confirmation token: "
            f"{EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN!r}."
        )


def _assert_mode(mode: str) -> None:
    """Raise when an unsupported relocation mode is requested."""
    if mode not in {
        EVIDENCE_RELOCATOR_MODE_COPY_ONLY,
        EVIDENCE_RELOCATOR_MODE_MOVE_VERIFIED,
    }:
        raise ValueError(f"Unsupported evidence relocation mode: {mode!r}.")


def _copy_and_verify_item(
    item: EvidenceRelocationItem,
    mode: str,
) -> EvidenceRelocationExecutionItem:
    """Copy one JSON evidence item and optionally remove the verified source."""
    source = normalize_path(item.source_path)
    destination = normalize_path(item.planned_destination_path)
    if item.category != EVIDENCE_RELOCATION_CATEGORY_JSON:
        return EvidenceRelocationExecutionItem(
            relative_path=item.relative_path,
            source_path=str(source),
            destination_path=str(destination),
            category=item.category,
            operation=mode,
            status=EVIDENCE_RELOCATOR_ITEM_STATUS_SKIPPED,
            byte_count=item.byte_count,
            message="non-json review item skipped by evidence relocator",
        )

    source_hash = calculate_file_sha256(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    destination_hash = calculate_file_sha256(destination)
    if source_hash != destination_hash:
        return EvidenceRelocationExecutionItem(
            relative_path=item.relative_path,
            source_path=str(source),
            destination_path=str(destination),
            category=item.category,
            operation=mode,
            status=EVIDENCE_RELOCATOR_ITEM_STATUS_FAILED,
            byte_count=item.byte_count,
            sha256_before=source_hash,
            sha256_after=destination_hash,
            message="destination hash did not match source hash",
        )

    status = EVIDENCE_RELOCATOR_ITEM_STATUS_COPIED
    message = "copied and hash-verified"
    if mode == EVIDENCE_RELOCATOR_MODE_MOVE_VERIFIED:
        source.unlink()
        status = EVIDENCE_RELOCATOR_ITEM_STATUS_MOVED
        message = "copied, hash-verified, and source file removed"

    return EvidenceRelocationExecutionItem(
        relative_path=item.relative_path,
        source_path=str(source),
        destination_path=str(destination),
        category=item.category,
        operation=mode,
        status=status,
        byte_count=item.byte_count,
        sha256_before=source_hash,
        sha256_after=destination_hash,
        message=message,
    )


def _skipped_review_item(
    item: EvidenceRelocationItem,
    mode: str,
) -> EvidenceRelocationExecutionItem:
    """Return an execution item for a skipped review candidate."""
    return EvidenceRelocationExecutionItem(
        relative_path=item.relative_path,
        source_path=item.source_path,
        destination_path=item.planned_destination_path,
        category=item.category,
        operation=mode,
        status=EVIDENCE_RELOCATOR_ITEM_STATUS_SKIPPED,
        byte_count=item.byte_count,
        message="review item requires manual quarantine decision",
    )


def _prune_empty_dirs(root: Path) -> None:
    """Remove empty directories under root, leaving missing paths untouched."""
    if not root.exists() or not root.is_dir():
        return
    for path in sorted(root.rglob("*"), key=lambda value: len(value.parts), reverse=True):
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass
    try:
        root.rmdir()
    except OSError:
        pass


def execute_evidence_relocation_plan(
    plan: EvidenceRelocationPlan,
    confirmation_token: str,
    mode: str = EVIDENCE_RELOCATOR_MODE_COPY_ONLY,
    prune_empty_source_dirs: bool = False,
) -> EvidenceRelocationExecutionResult:
    """Execute a dry-run relocation plan after explicit confirmation."""
    _assert_confirmed(confirmation_token)
    _assert_mode(mode)

    if plan.status() == EVIDENCE_RELOCATION_STATUS_ABSENT:
        return EvidenceRelocationExecutionResult(
            project_root=plan.project_root,
            source_evidence_root=plan.source_evidence_root,
            architecture_audit_root=plan.architecture_audit_root,
            mode=mode,
            status_value=EVIDENCE_RELOCATOR_STATUS_SKIPPED_ABSENT,
            message="in-source evidence folder is absent",
        )

    skipped_review_items = tuple(
        _skipped_review_item(item, mode) for item in plan.review_items
    )
    if plan.status() == EVIDENCE_RELOCATION_STATUS_REVIEW_REQUIRED:
        return EvidenceRelocationExecutionResult(
            project_root=plan.project_root,
            source_evidence_root=plan.source_evidence_root,
            architecture_audit_root=plan.architecture_audit_root,
            mode=mode,
            status_value=EVIDENCE_RELOCATOR_STATUS_REVIEW_REQUIRED,
            skipped_review_items=skipped_review_items,
            message="review items exist; no evidence files were relocated",
        )

    executed_items = tuple(_copy_and_verify_item(item, mode) for item in plan.json_items)
    result = EvidenceRelocationExecutionResult(
        project_root=plan.project_root,
        source_evidence_root=plan.source_evidence_root,
        architecture_audit_root=plan.architecture_audit_root,
        mode=mode,
        status_value=EVIDENCE_RELOCATOR_STATUS_COMPLETED,
        items=executed_items,
        skipped_review_items=skipped_review_items,
        message="evidence relocation execution completed",
    )

    if (
        result.status() == EVIDENCE_RELOCATOR_STATUS_COMPLETED
        and mode == EVIDENCE_RELOCATOR_MODE_MOVE_VERIFIED
        and prune_empty_source_dirs
    ):
        _prune_empty_dirs(normalize_path(plan.source_evidence_root))

    return result


def execute_evidence_relocation(
    project_root: str | Path | None,
    confirmation_token: str,
    mode: str = EVIDENCE_RELOCATOR_MODE_COPY_ONLY,
    prune_empty_source_dirs: bool = False,
) -> EvidenceRelocationExecutionResult:
    """Plan and execute evidence relocation after explicit confirmation."""
    plan = plan_evidence_relocation_dry_run(project_root)
    return execute_evidence_relocation_plan(
        plan,
        confirmation_token=confirmation_token,
        mode=mode,
        prune_empty_source_dirs=prune_empty_source_dirs,
    )


def render_evidence_relocation_result_text(
    result: EvidenceRelocationExecutionResult,
) -> str:
    """Return a human-readable execution result."""
    return result.summary()


def render_evidence_relocation_result_json(
    result: EvidenceRelocationExecutionResult,
) -> str:
    """Return a stable JSON execution result."""
    return json.dumps(result.to_dict(), indent=2, sort_keys=True)


def write_evidence_relocation_result_text(
    result: EvidenceRelocationExecutionResult,
    output_path: str | Path,
    overwrite: bool = False,
) -> Path:
    """Write a text execution result to an existing parent directory."""
    target = normalize_path(output_path)
    if not target.parent.exists():
        raise FileNotFoundError(f"Output parent does not exist: {str(target.parent)!r}.")
    if target.exists() and not overwrite:
        raise FileExistsError(f"Output file already exists: {str(target)!r}.")
    target.write_text(render_evidence_relocation_result_text(result), encoding="utf-8")
    return target


def write_evidence_relocation_result_json(
    result: EvidenceRelocationExecutionResult,
    output_path: str | Path,
    overwrite: bool = False,
) -> Path:
    """Write a JSON execution result to an existing parent directory."""
    target = normalize_path(output_path)
    if not target.parent.exists():
        raise FileNotFoundError(f"Output parent does not exist: {str(target.parent)!r}.")
    if target.exists() and not overwrite:
        raise FileExistsError(f"Output file already exists: {str(target)!r}.")
    target.write_text(render_evidence_relocation_result_json(result), encoding="utf-8")
    return target


__all__ = [
    "EVIDENCE_RELOCATOR_ACTION",
    "EVIDENCE_RELOCATOR_CONFIRMATION_TOKEN",
    "EVIDENCE_RELOCATOR_ITEM_STATUS_COPIED",
    "EVIDENCE_RELOCATOR_ITEM_STATUS_FAILED",
    "EVIDENCE_RELOCATOR_ITEM_STATUS_MOVED",
    "EVIDENCE_RELOCATOR_ITEM_STATUS_SKIPPED",
    "EVIDENCE_RELOCATOR_MODE_COPY_ONLY",
    "EVIDENCE_RELOCATOR_MODE_MOVE_VERIFIED",
    "EVIDENCE_RELOCATOR_STATUS_COMPLETED",
    "EVIDENCE_RELOCATOR_STATUS_CONFIRMATION_REQUIRED",
    "EVIDENCE_RELOCATOR_STATUS_FAILED",
    "EVIDENCE_RELOCATOR_STATUS_REVIEW_REQUIRED",
    "EVIDENCE_RELOCATOR_STATUS_SKIPPED_ABSENT",
    "EvidenceRelocationExecutionItem",
    "EvidenceRelocationExecutionResult",
    "calculate_file_sha256",
    "execute_evidence_relocation",
    "execute_evidence_relocation_plan",
    "render_evidence_relocation_result_json",
    "render_evidence_relocation_result_text",
    "write_evidence_relocation_result_json",
    "write_evidence_relocation_result_text",
]
