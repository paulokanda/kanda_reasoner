# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/_preview_delivery_models.py
"""Private backing classes for preview and delivery planner models."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ._model_payload_support import (
    _import_migration_payload,
    _plain_payload,
    _preview_bundle_payload,
)

__all__: list[str] = []

@dataclass(frozen=True)
class _PreviewFileDraft:
    """No-write preview draft record for a future LibCST writer train."""

    schema_version: str
    feature_id: str
    relative_path: str
    source_role: str
    planned_symbols: list[str]
    content_hash: str
    estimated_lines: int
    write_enabled: bool = False
    risk_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preview file draft dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class _PreviewBundle:
    """No-write preview bundle contract for selected module refactor output."""

    schema_version: str
    feature_id: str
    target_file: str
    source_content_hash: str
    preview_root: str
    write_mode: str
    libcst_available: bool
    public_api_before: list[str]
    public_api_after_expected: list[str]
    files: list[PreviewFileDraft]
    validation_blockers: list[str]
    risk_flags: list[str]
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preview bundle dictionary."""
        return _preview_bundle_payload(self)


@dataclass(frozen=True)
class _PreviewValidationResult:
    """Validation result for no-write preview bundle contracts."""

    schema_version: str
    feature_id: str
    status: str
    checked_rules: list[str]
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preview validation result dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class _PreviewWriteResult:
    """Governed filesystem write evidence for selected-project Preview support output."""

    schema_version: str
    feature_id: str
    status: str
    preview_root: str
    written_files: list[str]
    skipped_files: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preview write result dictionary."""
        return _plain_payload(self)


@dataclass(frozen=True)
class _ImportMigrationRecord:
    """Preview-only record for a possible project import migration."""

    schema_version: str
    feature_id: str
    importer_file: str
    original_import: str
    suggested_import: str
    action: str
    reason: str
    status: str = "preview_only"
    blockers: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready import migration record."""
        return _plain_payload(self)


@dataclass(frozen=True)
class _ImportMigrationPreview:
    """Read-only preview of import migration candidates."""

    schema_version: str
    feature_id: str
    target_file: str
    source_content_hash: str
    rewrite_enabled: bool
    records: list[ImportMigrationRecord]
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    status: str = "preview_only"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready import migration preview."""
        return _import_migration_payload(self)


@dataclass(frozen=True)
class _PreviewArtifactValidationResult:
    """Filesystem validation result for governed preview artifacts."""

    schema_version: str
    feature_id: str
    status: str
    preview_root: str
    checked_files: list[str]
    source_hash_verified: bool
    manifest_present: bool
    proof_present: bool
    import_migration_preview_status: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready preview artifact validation result."""
        return _plain_payload(self)


@dataclass(frozen=True)
class _ProjectPatchPayloadResult:
    """Governed project patch payload ZIP creation evidence."""

    schema_version: str
    feature_id: str
    status: str
    payload_zip_path: str
    payload_manifest_path: str
    preview_root: str
    included_files: list[str]
    source_hash_verified: bool
    patch_payload_created: bool
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready project patch payload result."""
        return _plain_payload(self)


