# project-path: kanda_reasoner_app/storage_policy/source_debris_report_export.py
"""Detailed source debris report/export helpers for Kanda Reasoner.

This module converts the report-only source-cleanliness scan into a stable
human-readable and JSON-exportable debris plan. It never moves, deletes,
quarantines, migrates, or creates folders on import. Files are written only by
explicit write functions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from kanda_reasoner_app.storage_policy.path_resolver import normalize_path
from kanda_reasoner_app.storage_policy.source_cleanliness_validator import (
    SOURCE_CLEANLINESS_CATEGORY_FAILURE,
    SOURCE_CLEANLINESS_CATEGORY_WARNING,
    SourceCleanlinessFinding,
    scan_source_cleanliness,
)

SOURCE_DEBRIS_REPORT_ACTION = "report_only"
SOURCE_DEBRIS_REPORT_SCHEMA_VERSION = 1
SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT = "architecture_audit_migration"
SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE = "maintenance_quarantine"
SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION = "packaging_exclusion_review"


@dataclass(frozen=True)
class SourceDebrisReportItem:
    """One source debris item prepared for report/export."""

    relative_path: str
    category: str
    pattern: str
    is_directory: bool
    recommended_destination: str
    recommended_action: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "relative_path": self.relative_path,
            "category": self.category,
            "pattern": self.pattern,
            "is_directory": self.is_directory,
            "recommended_destination": self.recommended_destination,
            "recommended_action": self.recommended_action,
        }


@dataclass(frozen=True)
class SourceDebrisExportPlan:
    """Report-only source debris export plan."""

    source_root: str
    action: str = SOURCE_DEBRIS_REPORT_ACTION
    schema_version: int = SOURCE_DEBRIS_REPORT_SCHEMA_VERSION
    items: tuple[SourceDebrisReportItem, ...] = field(default_factory=tuple)

    @property
    def total_items(self) -> int:
        """Return the total number of debris report items."""
        return len(self.items)

    @property
    def total_failures(self) -> int:
        """Return the number of failure-category items."""
        return sum(
            1
            for item in self.items
            if item.category == SOURCE_CLEANLINESS_CATEGORY_FAILURE
        )

    @property
    def total_warnings(self) -> int:
        """Return the number of warning-category items."""
        return sum(
            1
            for item in self.items
            if item.category == SOURCE_CLEANLINESS_CATEGORY_WARNING
        )

    @property
    def architecture_audit_items(self) -> int:
        """Return the number of items recommended for evidence migration."""
        return sum(
            1
            for item in self.items
            if item.recommended_destination
            == SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT
        )

    @property
    def quarantine_items(self) -> int:
        """Return the number of items recommended for quarantine review."""
        return sum(
            1
            for item in self.items
            if item.recommended_destination
            == SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE
        )

    @property
    def packaging_review_items(self) -> int:
        """Return the number of items recommended for packaging review."""
        return sum(
            1
            for item in self.items
            if item.recommended_destination
            == SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION
        )

    def is_empty(self) -> bool:
        """Return True when no debris report items exist."""
        return self.total_items == 0

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable dictionary."""
        return {
            "schema_version": self.schema_version,
            "action": self.action,
            "source_root": self.source_root,
            "total_items": self.total_items,
            "total_failures": self.total_failures,
            "total_warnings": self.total_warnings,
            "architecture_audit_items": self.architecture_audit_items,
            "quarantine_items": self.quarantine_items,
            "packaging_review_items": self.packaging_review_items,
            "items": [item.to_dict() for item in self.items],
        }

    def summary_lines(self) -> list[str]:
        """Return a human-readable source debris report as lines."""
        lines = [
            "Kanda Reasoner source debris report/export",
            f"Action: {self.action}",
            f"Source root: {self.source_root}",
            f"Items: {self.total_items}",
            f"Failures: {self.total_failures}",
            f"Warnings: {self.total_warnings}",
            f"Architecture audit migration items: {self.architecture_audit_items}",
            f"Maintenance quarantine items: {self.quarantine_items}",
            f"Packaging review items: {self.packaging_review_items}",
        ]

        if self.items:
            lines.append("Items:")
            for item in self.items:
                lines.append(
                    f"  - {item.relative_path} [{item.category}:{item.pattern}] "
                    f"-> {item.recommended_destination}: "
                    f"{item.recommended_action}"
                )

        return lines

    def summary(self) -> str:
        """Return a human-readable source debris report."""
        return "\n".join(self.summary_lines())


def _looks_like_project_evidence(relative_path: str) -> bool:
    """Return True when a path should be treated as project evidence."""
    normalized = relative_path.replace("\\", "/").lower().rstrip("/")
    if "project_analysis_evidence" in normalized:
        return True
    if normalized.endswith("_architecture_audit"):
        return True
    if normalized.endswith("_architecture_audit/current"):
        return True
    if normalized.endswith(".json") and "__" in Path(normalized).name:
        return True
    return False


def _recommended_destination_for_finding(
    finding: SourceCleanlinessFinding,
) -> str:
    """Return the recommended destination class for a cleanliness finding."""
    if _looks_like_project_evidence(finding.relative_path):
        return SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT
    if finding.category == SOURCE_CLEANLINESS_CATEGORY_WARNING:
        return SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION
    return SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE


def _recommended_action_for_destination(destination: str) -> str:
    """Return a human-readable recommended action for a destination."""
    if destination == SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT:
        return "migrate valid evidence to external architecture audit after dry-run"
    if destination == SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION:
        return "keep during development but exclude from packaged builds"
    return "quarantine or remove only after human review"


def _item_from_cleanliness_finding(
    finding: SourceCleanlinessFinding,
) -> SourceDebrisReportItem:
    """Convert a source-cleanliness finding to a debris export item."""
    destination = _recommended_destination_for_finding(finding)
    return SourceDebrisReportItem(
        relative_path=finding.relative_path,
        category=finding.category,
        pattern=finding.pattern,
        is_directory=finding.is_directory,
        recommended_destination=destination,
        recommended_action=_recommended_action_for_destination(destination),
    )


def build_source_debris_report_export(
    source_root: str | Path,
) -> SourceDebrisExportPlan:
    """Build a report-only source debris export plan for source_root."""
    root = normalize_path(source_root)
    cleanliness = scan_source_cleanliness(root)
    findings = tuple(cleanliness.failures) + tuple(cleanliness.warnings)
    items = tuple(_item_from_cleanliness_finding(finding) for finding in findings)
    return SourceDebrisExportPlan(source_root=str(root), items=items)


def render_source_debris_report_text(plan: SourceDebrisExportPlan) -> str:
    """Return a human-readable source debris report."""
    return plan.summary()


def render_source_debris_report_json(plan: SourceDebrisExportPlan) -> str:
    """Return a stable JSON source debris report."""
    return json.dumps(plan.to_dict(), indent=2, sort_keys=True) + "\n"


def _assert_can_write(path: Path, overwrite: bool) -> None:
    """Validate write target safety for explicit report writes."""
    if path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {path}")
    parent = path.parent
    if not parent.exists() or not parent.is_dir():
        raise ValueError(f"output parent must be an existing directory: {parent}")


def write_source_debris_report_text(
    plan: SourceDebrisExportPlan,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a human-readable report to output_path when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(render_source_debris_report_text(plan), encoding="utf-8")
    return path


def write_source_debris_report_json(
    plan: SourceDebrisExportPlan,
    output_path: str | Path,
    *,
    overwrite: bool = False,
) -> Path:
    """Write a JSON report to output_path when explicitly called."""
    path = normalize_path(output_path)
    _assert_can_write(path, overwrite)
    path.write_text(render_source_debris_report_json(plan), encoding="utf-8")
    return path


__all__ = [
    "SOURCE_DEBRIS_DESTINATION_ARCHITECTURE_AUDIT",
    "SOURCE_DEBRIS_DESTINATION_MAINTENANCE_QUARANTINE",
    "SOURCE_DEBRIS_DESTINATION_PACKAGING_EXCLUSION",
    "SOURCE_DEBRIS_REPORT_ACTION",
    "SOURCE_DEBRIS_REPORT_SCHEMA_VERSION",
    "SourceDebrisExportPlan",
    "SourceDebrisReportItem",
    "build_source_debris_report_export",
    "render_source_debris_report_json",
    "render_source_debris_report_text",
    "write_source_debris_report_json",
    "write_source_debris_report_text",
]
