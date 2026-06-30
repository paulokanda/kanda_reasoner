# project-path: kanda_reasoner_app/storage_policy/source_debris_packaging_exclusion_dry_run.py
"""Dry-run planner for source debris packaging exclusions.

This module turns development-only source debris warnings into an explicit
packaging exclusion review plan. It is report-only and side-effect free:
importing or planning never creates folders, writes files, deletes files, moves
files, or changes packaging configuration. Explicit callers may write the plan
with the write functions after creating an output folder.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.build_policy_baseline import (
    PACKAGING_EXCLUDE_PATTERNS,
)
from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.source_debris_quarantine_dry_run import (
    SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW,
    SourceDebrisQuarantineDryRunPlan,
    build_source_debris_quarantine_dry_run,
)
from kanda_reasoner_app.storage_policy.architecture_audit_resolver import (
    get_project_slug,
)

SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_ACTION = "dry_run_only"
SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_SCHEMA_VERSION = 1
SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_EMPTY = "empty"
SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_COVERED = "covered_by_policy"
SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_POLICY_GAP = "policy_gap"


@dataclass(frozen=True)
class SourceDebrisPackagingExclusionDryRunItem:
    """One development-only item reviewed for packaging exclusion."""

    relative_path: str
    source_path: str
    pattern: str
    is_directory: bool
    matched_exclude_pattern: str
    is_covered_by_packaging_policy: bool
    message: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "source_path": self.source_path,
            "pattern": self.pattern,
            "is_directory": self.is_directory,
            "matched_exclude_pattern": self.matched_exclude_pattern,
            "is_covered_by_packaging_policy": self.is_covered_by_packaging_policy,
            "message": self.message,
        }


@dataclass(frozen=True)
class SourceDebrisPackagingExclusionDryRunPlan:
    """Dry-run plan for development-only packaging exclusions."""

    source_root: str
    project_slug: str
    action: str = SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_ACTION
    schema_version: int = SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_SCHEMA_VERSION
    items: tuple[SourceDebrisPackagingExclusionDryRunItem, ...] = field(
        default_factory=tuple
    )

    @property
    def total_items(self) -> int:
        """Return the total number of packaging exclusion items."""
        return len(self.items)

    @property
    def covered_items(self) -> int:
        """Return the number of items covered by packaging policy."""
        return sum(1 for item in self.items if item.is_covered_by_packaging_policy)

    @property
    def uncovered_items(self) -> int:
        """Return the number of items not covered by packaging policy."""
        return self.total_items - self.covered_items

    def status(self) -> str:
        """Return a stable dry-run status string."""
        if self.total_items == 0:
            return SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_EMPTY
        if self.uncovered_items > 0:
            return SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_POLICY_GAP
        return SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_COVERED

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "action": self.action,
            "status": self.status(),
            "source_root": self.source_root,
            "project_slug": self.project_slug,
            "total_items": self.total_items,
            "covered_items": self.covered_items,
            "uncovered_items": self.uncovered_items,
            "items": [item.to_dict() for item in self.items],
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable summary as lines."""
        lines = [
            "Kanda Reasoner source debris packaging exclusion dry-run report",
            f"Action: {self.action}",
            f"Status: {self.status()}",
            f"Source root: {self.source_root}",
            f"Project slug: {self.project_slug}",
            f"Items: {self.total_items}",
            f"Covered items: {self.covered_items}",
            f"Uncovered items: {self.uncovered_items}",
        ]

        if self.items:
            lines.append("Planned packaging exclusion review:")
            for item in self.items:
                coverage = "covered" if item.is_covered_by_packaging_policy else "gap"
                matched = item.matched_exclude_pattern or "no matching exclude"
                lines.append(
                    f"  - {item.relative_path} [{coverage}; {matched}] -> "
                    f"{item.message}"
                )

        return lines

    def summary(self) -> str:
        """Return a human-readable summary."""
        return "\n".join(self.summary_lines())


def _normalize_relative_for_matching(relative_path: str) -> str:
    """Return a normalized relative path for matching."""
    return relative_path.replace("\\", "/").strip("/")


def _pattern_covers_path(relative_path: str, pattern: str) -> bool:
    """Return True when a packaging exclude pattern covers a path.

    Directory patterns are treated recursively because packaging tools usually
    exclude a directory and everything below it.
    """
    normalized_path = _normalize_relative_for_matching(relative_path)
    normalized_pattern = pattern.replace("\\", "/").strip("/")

    if not normalized_pattern:
        return False

    if pattern.replace("\\", "/").endswith("/"):
        return (
            normalized_path == normalized_pattern
            or normalized_path.startswith(normalized_pattern + "/")
        )

    return fnmatch(normalized_path, normalized_pattern)


def _first_covering_exclude_pattern(
    relative_path: str,
    packaging_exclude_patterns: tuple[str, ...],
) -> str:
    """Return the first exclude pattern that covers relative_path."""
    for pattern in packaging_exclude_patterns:
        if _pattern_covers_path(relative_path, pattern):
            return pattern
    return ""


def _item_from_packaging_review_item(
    item,
    packaging_exclude_patterns: tuple[str, ...],
) -> SourceDebrisPackagingExclusionDryRunItem:
    """Convert a packaging review item into a packaging exclusion item."""
    matched = _first_covering_exclude_pattern(
        item.relative_path,
        packaging_exclude_patterns,
    )
    is_covered = bool(matched)
    message = (
        "keep in development source tree and exclude from packaged builds"
        if is_covered
        else "add a reviewed packaging exclusion before release packaging"
    )
    return SourceDebrisPackagingExclusionDryRunItem(
        relative_path=item.relative_path,
        source_path=item.source_path,
        pattern=item.pattern,
        is_directory=item.is_directory,
        matched_exclude_pattern=matched,
        is_covered_by_packaging_policy=is_covered,
        message=message,
    )


def build_source_debris_packaging_exclusion_dry_run(
    source_root: str | Path,
    *,
    packaging_exclude_patterns: tuple[str, ...] = PACKAGING_EXCLUDE_PATTERNS,
) -> SourceDebrisPackagingExclusionDryRunPlan:
    """Build a dry-run packaging exclusion plan for source_root."""
    root = normalize_path(source_root)
    review_plan = build_source_debris_quarantine_dry_run(root)
    return build_source_debris_packaging_exclusion_dry_run_from_review_plan(
        review_plan,
        packaging_exclude_patterns=packaging_exclude_patterns,
    )


def build_source_debris_packaging_exclusion_dry_run_from_review_plan(
    review_plan: SourceDebrisQuarantineDryRunPlan,
    *,
    packaging_exclude_patterns: tuple[str, ...] = PACKAGING_EXCLUDE_PATTERNS,
) -> SourceDebrisPackagingExclusionDryRunPlan:
    """Build a dry-run packaging exclusion plan from a review plan."""
    root = normalize_path(review_plan.source_root)
    items = tuple(
        _item_from_packaging_review_item(item, packaging_exclude_patterns)
        for item in review_plan.items
        if item.planned_operation == SOURCE_DEBRIS_OPERATION_PACKAGING_EXCLUSION_REVIEW
    )
    return SourceDebrisPackagingExclusionDryRunPlan(
        source_root=str(root),
        project_slug=get_project_slug(root),
        items=items,
    )


def render_source_debris_packaging_exclusion_dry_run_text(
    plan: SourceDebrisPackagingExclusionDryRunPlan,
) -> str:
    """Return a human-readable dry-run plan."""
    return plan.summary()


def render_source_debris_packaging_exclusion_dry_run_json(
    plan: SourceDebrisPackagingExclusionDryRunPlan,
) -> str:
    """Return a stable JSON dry-run plan."""
    return json.dumps(plan.to_dict(), indent=2, sort_keys=True) + "\n"


def _assert_can_write(path: Path, overwrite: bool) -> None:
    """Validate write target safety for explicit report writes."""
    if path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {path}")
    if not path.parent.exists() or not path.parent.is_dir():
        raise ValueError(f"output parent must be an existing directory: {path.parent}")


def write_source_debris_packaging_exclusion_dry_run_text(
    plan: SourceDebrisPackagingExclusionDryRunPlan,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a dry-run text report when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_packaging_exclusion_dry_run_text(plan),
        encoding="utf-8",
    )
    return path


def write_source_debris_packaging_exclusion_dry_run_json(
    plan: SourceDebrisPackagingExclusionDryRunPlan,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a dry-run JSON report when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(
        render_source_debris_packaging_exclusion_dry_run_json(plan),
        encoding="utf-8",
    )
    return path


__all__ = [
    "SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_ACTION",
    "SOURCE_DEBRIS_PACKAGING_EXCLUSION_DRY_RUN_SCHEMA_VERSION",
    "SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_COVERED",
    "SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_EMPTY",
    "SOURCE_DEBRIS_PACKAGING_EXCLUSION_STATUS_POLICY_GAP",
    "SourceDebrisPackagingExclusionDryRunItem",
    "SourceDebrisPackagingExclusionDryRunPlan",
    "build_source_debris_packaging_exclusion_dry_run",
    "build_source_debris_packaging_exclusion_dry_run_from_review_plan",
    "render_source_debris_packaging_exclusion_dry_run_json",
    "render_source_debris_packaging_exclusion_dry_run_text",
    "write_source_debris_packaging_exclusion_dry_run_json",
    "write_source_debris_packaging_exclusion_dry_run_text",
]
