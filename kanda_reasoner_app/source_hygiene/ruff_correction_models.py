# project-path: kanda_reasoner_app/source_hygiene/ruff_correction_models.py
"""Data contracts for reviewed Ruff correction previews and apply receipts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

__all__ = [
    "RUFF_CORRECTION_FEATURE_ID",
    "RUFF_CORRECTION_SCHEMA_VERSION",
    "RuffCorrectionApplyReceipt",
    "RuffCorrectionFileRecord",
    "RuffCorrectionPreviewRecord",
]

RUFF_CORRECTION_FEATURE_ID = "engineering-safety-ruff-correction-workflow-v3a"
RUFF_CORRECTION_SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class RuffCorrectionFileRecord:
    """One source file represented in a reviewed Ruff correction preview."""

    relative_path: str
    source_sha256: str
    preview_sha256: str
    source_size_bytes: int
    preview_size_bytes: int
    safe_lint_finding_count: int = 0
    format_required: bool = False
    diff_sha256: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary."""
        return {
            "relative_path": self.relative_path,
            "source_sha256": self.source_sha256,
            "preview_sha256": self.preview_sha256,
            "source_size_bytes": self.source_size_bytes,
            "preview_size_bytes": self.preview_size_bytes,
            "safe_lint_finding_count": self.safe_lint_finding_count,
            "format_required": self.format_required,
            "diff_sha256": self.diff_sha256,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "RuffCorrectionFileRecord":
        """Build one file record from validated JSON-like data."""
        return cls(
            relative_path=str(value.get("relative_path") or ""),
            source_sha256=str(value.get("source_sha256") or ""),
            preview_sha256=str(value.get("preview_sha256") or ""),
            source_size_bytes=int(value.get("source_size_bytes") or 0),
            preview_size_bytes=int(value.get("preview_size_bytes") or 0),
            safe_lint_finding_count=int(value.get("safe_lint_finding_count") or 0),
            format_required=bool(value.get("format_required")),
            diff_sha256=str(value.get("diff_sha256") or ""),
        )


@dataclass(frozen=True)
class RuffCorrectionPreviewRecord:
    """Durable project-owned evidence for one Ruff correction preview."""

    preview_id: str
    status: str
    project_root: str
    created_at_utc: str
    ruff_version: str
    ruff_command_source: str
    policy_identity_token: str
    policy_config_sha256: str
    scope_paths: tuple[str, ...]
    candidate_file_count: int
    changed_file_count: int
    source_snapshot_sha256: str
    preview_payload_sha256: str
    manifest_identity_sha256: str
    confirm_token: str
    preview_root: str
    manifest_path: str
    diff_path: str
    payload_root: str
    files: tuple[RuffCorrectionFileRecord, ...] = ()
    warnings: tuple[str, ...] = ()
    schema_version: str = RUFF_CORRECTION_SCHEMA_VERSION
    feature_id: str = RUFF_CORRECTION_FEATURE_ID

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary."""
        return {
            "schema_version": self.schema_version,
            "feature_id": self.feature_id,
            "preview_id": self.preview_id,
            "status": self.status,
            "project_root": self.project_root,
            "created_at_utc": self.created_at_utc,
            "ruff_version": self.ruff_version,
            "ruff_command_source": self.ruff_command_source,
            "policy_identity_token": self.policy_identity_token,
            "policy_config_sha256": self.policy_config_sha256,
            "scope_paths": list(self.scope_paths),
            "candidate_file_count": self.candidate_file_count,
            "changed_file_count": self.changed_file_count,
            "source_snapshot_sha256": self.source_snapshot_sha256,
            "preview_payload_sha256": self.preview_payload_sha256,
            "manifest_identity_sha256": self.manifest_identity_sha256,
            "confirm_token": self.confirm_token,
            "preview_root": self.preview_root,
            "manifest_path": self.manifest_path,
            "diff_path": self.diff_path,
            "payload_root": self.payload_root,
            "files": [item.to_dict() for item in self.files],
            "warnings": list(self.warnings),
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "RuffCorrectionPreviewRecord":
        """Build one preview record from validated JSON-like data."""
        files_value = value.get("files")
        files: list[RuffCorrectionFileRecord] = []
        if isinstance(files_value, list):
            for item in files_value:
                if isinstance(item, Mapping):
                    files.append(RuffCorrectionFileRecord.from_dict(item))
        warnings_value = value.get("warnings")
        warnings = (
            tuple(str(item) for item in warnings_value)
            if isinstance(warnings_value, list)
            else ()
        )
        scope_value = value.get("scope_paths")
        scope_paths = (
            tuple(str(item) for item in scope_value)
            if isinstance(scope_value, list)
            else ()
        )
        return cls(
            preview_id=str(value.get("preview_id") or ""),
            status=str(value.get("status") or ""),
            project_root=str(value.get("project_root") or ""),
            created_at_utc=str(value.get("created_at_utc") or ""),
            ruff_version=str(value.get("ruff_version") or ""),
            ruff_command_source=str(value.get("ruff_command_source") or ""),
            policy_identity_token=str(value.get("policy_identity_token") or ""),
            policy_config_sha256=str(value.get("policy_config_sha256") or ""),
            scope_paths=scope_paths,
            candidate_file_count=int(value.get("candidate_file_count") or 0),
            changed_file_count=int(value.get("changed_file_count") or 0),
            source_snapshot_sha256=str(value.get("source_snapshot_sha256") or ""),
            preview_payload_sha256=str(value.get("preview_payload_sha256") or ""),
            manifest_identity_sha256=str(value.get("manifest_identity_sha256") or ""),
            confirm_token=str(value.get("confirm_token") or ""),
            preview_root=str(value.get("preview_root") or ""),
            manifest_path=str(value.get("manifest_path") or ""),
            diff_path=str(value.get("diff_path") or ""),
            payload_root=str(value.get("payload_root") or ""),
            files=tuple(files),
            warnings=warnings,
            schema_version=str(
                value.get("schema_version") or RUFF_CORRECTION_SCHEMA_VERSION
            ),
            feature_id=str(value.get("feature_id") or RUFF_CORRECTION_FEATURE_ID),
        )


@dataclass(frozen=True)
class RuffCorrectionApplyReceipt:
    """Durable receipt for one explicit Ruff correction apply transaction."""

    receipt_id: str
    preview_id: str
    status: str
    project_root: str
    created_at_utc: str
    backup_root: str
    receipt_path: str
    changed_files: tuple[str, ...]
    validation_markers: tuple[str, ...]
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = RUFF_CORRECTION_SCHEMA_VERSION
    feature_id: str = RUFF_CORRECTION_FEATURE_ID

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible dictionary."""
        return {
            "schema_version": self.schema_version,
            "feature_id": self.feature_id,
            "receipt_id": self.receipt_id,
            "preview_id": self.preview_id,
            "status": self.status,
            "project_root": self.project_root,
            "created_at_utc": self.created_at_utc,
            "backup_root": self.backup_root,
            "receipt_path": self.receipt_path,
            "changed_files": list(self.changed_files),
            "validation_markers": list(self.validation_markers),
            "error": self.error,
            "metadata": dict(self.metadata),
        }
