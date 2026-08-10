# project-path: kanda_reasoner_app/engineering_diagnostics_patch_preview/models.py
"""Immutable contracts for governed, non-installable patch previews."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

__all__ = [
    "PATCH_PREVIEW_CORRECTION_KINDS",
    "PATCH_PREVIEW_FEATURE_ID",
    "PATCH_PREVIEW_SCHEMA_VERSION",
    "GovernedPatchPreviewFile",
    "GovernedPatchPreviewPlan",
    "GovernedPatchPreviewRecord",
]

PATCH_PREVIEW_FEATURE_ID = "engineering-diagnostics-governed-patch-preview-wave2u-v1"
PATCH_PREVIEW_SCHEMA_VERSION = "1.0"
PATCH_PREVIEW_CORRECTION_KINDS = frozenset(
    {"UTF8_BOM_REMOVAL", "RUFF_SAFE_UNUSED_IMPORT", "RUFF_SAFE_IMPORT_FORMAT"}
)


def _text(value: object, field: str) -> str:
    result = str(value or "").strip()
    if not result:
        raise ValueError(field + " is required.")
    return result


def _items(values: object) -> tuple[str, ...]:
    if values is None:
        return ()
    result: list[str] = []
    for value in tuple(values):
        text = str(value or "").strip()
        if text and text not in result:
            result.append(text)
    return tuple(result)


@dataclass(frozen=True, slots=True)
class GovernedPatchPreviewPlan:
    """One fail-closed plan derived from a reviewed remediation intent."""

    intent_id: str
    issue_fingerprint: str
    run_id: str
    producer_id: str
    code: str
    relative_path: str
    correction_kind: str
    original_sha256: str
    focused_validation: tuple[str, ...]
    required_project_validation: tuple[str, ...]
    rollback_expectation: str
    approval_token: str
    installable: bool = False
    source_mutation_allowed: bool = False

    def __post_init__(self) -> None:
        for field in (
            "intent_id",
            "issue_fingerprint",
            "run_id",
            "producer_id",
            "code",
            "relative_path",
            "original_sha256",
            "rollback_expectation",
            "approval_token",
        ):
            object.__setattr__(self, field, _text(getattr(self, field), field))
        kind = _text(self.correction_kind, "correction_kind").upper()
        if kind not in PATCH_PREVIEW_CORRECTION_KINDS:
            raise ValueError("Unsupported correction_kind: " + kind)
        object.__setattr__(self, "correction_kind", kind)
        object.__setattr__(self, "focused_validation", _items(self.focused_validation))
        object.__setattr__(
            self,
            "required_project_validation",
            _items(self.required_project_validation),
        )
        if not self.focused_validation or not self.required_project_validation:
            raise ValueError("Patch Preview requires focused and Project validation.")
        if self.installable or self.source_mutation_allowed:
            raise ValueError("Patch Preview plans are non-installable and non-mutating.")

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible plan."""
        return {
            "intent_id": self.intent_id,
            "issue_fingerprint": self.issue_fingerprint,
            "run_id": self.run_id,
            "producer_id": self.producer_id,
            "code": self.code,
            "relative_path": self.relative_path,
            "correction_kind": self.correction_kind,
            "original_sha256": self.original_sha256,
            "focused_validation": list(self.focused_validation),
            "required_project_validation": list(self.required_project_validation),
            "rollback_expectation": self.rollback_expectation,
            "approval_token": self.approval_token,
            "installable": self.installable,
            "source_mutation_allowed": self.source_mutation_allowed,
        }


@dataclass(frozen=True, slots=True)
class GovernedPatchPreviewFile:
    """Exact original and proposed identity for the one eligible source file."""

    relative_path: str
    original_sha256: str
    proposed_sha256: str
    original_size_bytes: int
    proposed_size_bytes: int
    diff_sha256: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible file record."""
        return {
            "relative_path": self.relative_path,
            "original_sha256": self.original_sha256,
            "proposed_sha256": self.proposed_sha256,
            "original_size_bytes": self.original_size_bytes,
            "proposed_size_bytes": self.proposed_size_bytes,
            "diff_sha256": self.diff_sha256,
        }


@dataclass(frozen=True, slots=True)
class GovernedPatchPreviewRecord:
    """Durable support-state evidence for one non-installable preview."""

    preview_id: str
    status: str
    project_root: str
    created_at_utc: str
    plan: GovernedPatchPreviewPlan
    file: GovernedPatchPreviewFile
    preview_root: str
    manifest_path: str
    diff_path: str
    proposal_zip_path: str
    rollback_zip_path: str
    validation_markers: tuple[str, ...]
    warnings: tuple[str, ...]
    schema_version: str = PATCH_PREVIEW_SCHEMA_VERSION
    feature_id: str = PATCH_PREVIEW_FEATURE_ID

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible preview record."""
        return {
            "schema_version": self.schema_version,
            "feature_id": self.feature_id,
            "preview_id": self.preview_id,
            "status": self.status,
            "project_root": self.project_root,
            "created_at_utc": self.created_at_utc,
            "plan": self.plan.to_dict(),
            "file": self.file.to_dict(),
            "preview_root": self.preview_root,
            "manifest_path": self.manifest_path,
            "diff_path": self.diff_path,
            "proposal_zip_path": self.proposal_zip_path,
            "rollback_zip_path": self.rollback_zip_path,
            "validation_markers": list(self.validation_markers),
            "warnings": list(self.warnings),
        }
