# project-path: kanda_reasoner_app/storage_policy/evidence_relocation_dry_run.py
"""Dry-run planner for relocating in-source project evidence.

This module inspects the old in-source evidence folder and builds a report-only
relocation plan to the external architecture audit folder. It is side-effect
free on import and report-only when called: it must not create folders, move
files, delete files, or modify audit outputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from kanda_reasoner_app.storage_policy.architecture_audit_resolver import (
    ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER,
    ARCHITECTURE_AUDIT_SUBFOLDER_NAMES,
    get_architecture_audit_current_root,
    get_architecture_audit_root,
    get_architecture_audit_subfolder,
    get_project_slug,
)
from kanda_reasoner_app.storage_policy.maintenance_subfolder_policy import (
    get_maintenance_subfolder,
)
from kanda_reasoner_app.storage_policy.path_resolver import (
    get_app_root,
    normalize_path,
)

IN_SOURCE_EVIDENCE_FOLDER_NAME = "project_analysis_evidence"
EVIDENCE_RELOCATION_DRY_RUN_ACTION = "dry_run_only"
EVIDENCE_RELOCATION_CATEGORY_JSON = "json_evidence"
EVIDENCE_RELOCATION_CATEGORY_REVIEW = "review_or_quarantine"
EVIDENCE_RELOCATION_STATUS_ABSENT = "absent"
EVIDENCE_RELOCATION_STATUS_READY = "ready"
EVIDENCE_RELOCATION_STATUS_REVIEW_REQUIRED = "review_required"


@dataclass(frozen=True)
class EvidenceRelocationItem:
    """One planned evidence relocation or review item."""

    relative_path: str
    source_path: str
    planned_destination_path: str
    category: str
    byte_count: int


@dataclass(frozen=True)
class EvidenceRelocationPlan:
    """Report-only plan for relocating old in-source project evidence."""

    project_root: str
    project_slug: str
    source_evidence_root: str
    architecture_audit_root: str
    action: str = EVIDENCE_RELOCATION_DRY_RUN_ACTION
    source_exists: bool = False
    json_items: tuple[EvidenceRelocationItem, ...] = field(default_factory=tuple)
    review_items: tuple[EvidenceRelocationItem, ...] = field(default_factory=tuple)

    @property
    def total_json_items(self) -> int:
        """Return the number of JSON evidence items."""
        return len(self.json_items)

    @property
    def total_review_items(self) -> int:
        """Return the number of non-JSON review items."""
        return len(self.review_items)

    @property
    def total_items(self) -> int:
        """Return the total number of planned items."""
        return self.total_json_items + self.total_review_items

    def has_valid_evidence(self) -> bool:
        """Return True when JSON evidence files were found."""
        return self.total_json_items > 0

    def requires_review(self) -> bool:
        """Return True when non-JSON or mixed content needs review."""
        return self.total_review_items > 0

    def status(self) -> str:
        """Return the dry-run status."""
        if not self.source_exists:
            return EVIDENCE_RELOCATION_STATUS_ABSENT
        if self.requires_review():
            return EVIDENCE_RELOCATION_STATUS_REVIEW_REQUIRED
        return EVIDENCE_RELOCATION_STATUS_READY

    def summary_lines(self) -> list[str]:
        """Return a human-readable dry-run summary."""
        lines = [
            "Kanda Reasoner evidence relocation dry-run report",
            f"Action: {self.action}",
            f"Status: {self.status()}",
            f"Project root: {self.project_root}",
            f"Project slug: {self.project_slug}",
            f"Source evidence root: {self.source_evidence_root}",
            f"Architecture audit root: {self.architecture_audit_root}",
            f"JSON evidence items: {self.total_json_items}",
            f"Review items: {self.total_review_items}",
        ]

        if self.json_items:
            lines.append("Planned JSON evidence destinations:")
            for item in self.json_items:
                lines.append(
                    f"  - {item.relative_path} -> {item.planned_destination_path}"
                )

        if self.review_items:
            lines.append("Review or quarantine candidates:")
            for item in self.review_items:
                lines.append(
                    f"  - {item.relative_path} -> {item.planned_destination_path}"
                )

        return lines

    def summary(self) -> str:
        """Return a human-readable dry-run summary."""
        return "\n".join(self.summary_lines())


def get_in_source_evidence_root(project_root: str | Path | None = None) -> Path:
    """Return the old in-source evidence folder without creating it."""
    root = get_app_root() if project_root is None else normalize_path(project_root)
    return root / IN_SOURCE_EVIDENCE_FOLDER_NAME


def _relative_text(path: Path) -> str:
    """Return normalized POSIX-style relative path text."""
    return path.as_posix()


def _planned_json_destination(project_root: Path, relative_path: Path) -> Path:
    """Return the external architecture audit destination for a JSON file."""
    parts = relative_path.parts
    if parts and parts[0] in ARCHITECTURE_AUDIT_SUBFOLDER_NAMES:
        return get_architecture_audit_current_root(project_root) / relative_path

    return (
        get_architecture_audit_subfolder(
            project_root,
            ARCHITECTURE_AUDIT_ARTIFACT_SUBFOLDER,
        )
        / relative_path.name
    )


def _planned_review_destination(project_root: Path, relative_path: Path) -> Path:
    """Return the maintenance quarantine destination for review-only files."""
    slug = get_project_slug(project_root)
    return (
        get_maintenance_subfolder("quarantine_manual")
        / slug
        / IN_SOURCE_EVIDENCE_FOLDER_NAME
        / relative_path
    )


def _build_item(
    source_file: Path,
    source_evidence_root: Path,
    planned_destination: Path,
    category: str,
) -> EvidenceRelocationItem:
    """Build one relocation item from a file path."""
    relative_path = source_file.relative_to(source_evidence_root)
    return EvidenceRelocationItem(
        relative_path=_relative_text(relative_path),
        source_path=str(source_file),
        planned_destination_path=str(planned_destination),
        category=category,
        byte_count=source_file.stat().st_size,
    )


def plan_evidence_relocation_dry_run(
    project_root: str | Path | None = None,
) -> EvidenceRelocationPlan:
    """Build a report-only relocation plan for old in-source evidence."""
    root = get_app_root() if project_root is None else normalize_path(project_root)
    source_root = get_in_source_evidence_root(root)
    audit_root = get_architecture_audit_root(root)
    slug = get_project_slug(root)

    if not source_root.exists():
        return EvidenceRelocationPlan(
            project_root=str(root),
            project_slug=slug,
            source_evidence_root=str(source_root),
            architecture_audit_root=str(audit_root),
            source_exists=False,
        )

    if not source_root.is_dir():
        raise ValueError(
            "In-source evidence path exists but is not a directory: "
            f"{str(source_root)!r}."
        )

    json_items: list[EvidenceRelocationItem] = []
    review_items: list[EvidenceRelocationItem] = []

    for source_file in sorted(source_root.rglob("*")):
        if not source_file.is_file():
            continue

        relative_path = source_file.relative_to(source_root)
        if source_file.suffix.lower() == ".json":
            destination = _planned_json_destination(root, relative_path)
            json_items.append(
                _build_item(
                    source_file,
                    source_root,
                    destination,
                    EVIDENCE_RELOCATION_CATEGORY_JSON,
                )
            )
        else:
            destination = _planned_review_destination(root, relative_path)
            review_items.append(
                _build_item(
                    source_file,
                    source_root,
                    destination,
                    EVIDENCE_RELOCATION_CATEGORY_REVIEW,
                )
            )

    return EvidenceRelocationPlan(
        project_root=str(root),
        project_slug=slug,
        source_evidence_root=str(source_root),
        architecture_audit_root=str(audit_root),
        source_exists=True,
        json_items=tuple(json_items),
        review_items=tuple(review_items),
    )


def summarize_evidence_relocation_dry_run(
    plan: EvidenceRelocationPlan,
) -> str:
    """Return the dry-run plan summary."""
    return plan.summary()


__all__ = [
    "EVIDENCE_RELOCATION_CATEGORY_JSON",
    "EVIDENCE_RELOCATION_CATEGORY_REVIEW",
    "EVIDENCE_RELOCATION_DRY_RUN_ACTION",
    "EVIDENCE_RELOCATION_STATUS_ABSENT",
    "EVIDENCE_RELOCATION_STATUS_READY",
    "EVIDENCE_RELOCATION_STATUS_REVIEW_REQUIRED",
    "EvidenceRelocationItem",
    "EvidenceRelocationPlan",
    "IN_SOURCE_EVIDENCE_FOLDER_NAME",
    "get_in_source_evidence_root",
    "plan_evidence_relocation_dry_run",
    "summarize_evidence_relocation_dry_run",
]
