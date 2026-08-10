# project-path: kanda_reasoner_app/error_memory/backend.py
"""Explicit Tool and Project Error Memory backend contracts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.memory_ownership import (
    MemoryOwnerContext,
    MemoryOwnershipError,
    project_owner_context,
    tool_owner_context,
)

from .owner_migration import (
    ErrorMemoryOwnerMigrationError,
    migrate_legacy_project_owner_if_safe,
)

__all__ = [
    "ErrorMemoryBackend",
    "ErrorMemoryBackendError",
    "OwnerMetadataPolicy",
    "coerce_error_memory_backend",
    "project_error_memory_backend",
    "tool_error_memory_backend",
]

PROJECT_ERROR_MEMORY_DIR = "project_error_memory"
TOOL_ERROR_MEMORY_DIR = "tool_error_memory"
OWNER_METADATA_FIELDS = (
    "owner_scope",
    "owner_id",
    "owner_slug",
    "owner_root_fingerprint",
    "affected_box",
)


class ErrorMemoryBackendError(RuntimeError):
    """Raised when an Error Memory backend or owner contract is unsafe."""


class OwnerMetadataPolicy(str, Enum):
    """Control how supplied owner metadata is handled on canonical writes."""

    SYSTEM_ASSIGN = "SYSTEM_ASSIGN"
    REQUIRE_MATCH = "REQUIRE_MATCH"


@dataclass(frozen=True)
class ErrorMemoryBackend:
    """One explicit canonical Error Memory store and its system owner."""

    owner: MemoryOwnerContext
    root: Path

    @property
    def lessons_dir(self) -> Path:
        return self.root / "lessons"

    @property
    def exports_dir(self) -> Path:
        return self.root / "exports"

    @property
    def schemas_dir(self) -> Path:
        return self.root / "schemas"

    @property
    def references_dir(self) -> Path:
        return self.root / "cross_owner_references"

    @property
    def index_path(self) -> Path:
        return self.root / "lessons_index.json"

    @property
    def schema_path(self) -> Path:
        return self.schemas_dir / "lesson.schema.json"

    def canonical_owner_fields(self) -> dict[str, str]:
        """Return backend-assigned canonical owner fields."""
        return self.owner.canonical_fields()

    def assign_owner_metadata(
        self,
        lesson: Mapping[str, Any],
        *,
        policy: OwnerMetadataPolicy = OwnerMetadataPolicy.SYSTEM_ASSIGN,
    ) -> dict[str, Any]:
        """Return a canonical lesson with safe system-owned metadata."""
        payload = dict(lesson)
        supplied = {
            key: str(payload.get(key) or "").strip()
            for key in OWNER_METADATA_FIELDS
            if key in payload
        }
        expected = self.canonical_owner_fields()
        if policy is OwnerMetadataPolicy.REQUIRE_MATCH:
            missing = [key for key in OWNER_METADATA_FIELDS if not supplied.get(key)]
            if missing:
                raise ErrorMemoryBackendError(
                    "CANONICAL_OWNER_METADATA_MISSING:" + ",".join(missing)
                )
            mismatched = [
                key for key in OWNER_METADATA_FIELDS
                if supplied.get(key) != expected[key]
            ]
            if mismatched:
                raise ErrorMemoryBackendError(
                    "FOREIGN_OWNER_CANONICAL_WRITE_REJECTED:"
                    + ",".join(mismatched)
                )
        for key in OWNER_METADATA_FIELDS:
            payload[key] = expected[key]
        payload["project_slug"] = self.owner.owner_slug
        return payload

    def validate_persisted_owner(
        self,
        lesson: Mapping[str, Any],
        *,
        allow_legacy_ownerless: bool,
    ) -> None:
        """Validate one persisted canonical lesson against this backend."""
        supplied = {
            key: str(lesson.get(key) or "").strip()
            for key in OWNER_METADATA_FIELDS
        }
        if not any(supplied.values()):
            if allow_legacy_ownerless:
                return
            raise ErrorMemoryBackendError("CANONICAL_OWNER_METADATA_MISSING")
        expected = self.canonical_owner_fields()
        mismatched = [
            key for key in OWNER_METADATA_FIELDS
            if supplied.get(key) != expected[key]
        ]
        if mismatched:
            raise ErrorMemoryBackendError(
                "FOREIGN_OWNER_CANONICAL_READ_REJECTED:"
                + ",".join(mismatched)
            )

    def ensure_dirs(self) -> dict[str, Path]:
        """Create canonical backend directories."""
        for path in (
            self.root,
            self.lessons_dir,
            self.exports_dir,
            self.schemas_dir,
            self.references_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)
        return {
            "root": self.root,
            "lessons": self.lessons_dir,
            "exports": self.exports_dir,
            "schemas": self.schemas_dir,
            "references": self.references_dir,
        }

    def write_backend_manifest(self) -> Path:
        """Write the deterministic backend identity manifest when absent."""
        self.ensure_dirs()
        path = self.root / "owner_manifest.json"
        payload = {
            "schema_version": "1.0",
            "artifact_type": "error_memory_backend_owner",
            **self.canonical_owner_fields(),
            "store_root": str(self.root),
        }
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if path.exists():
            existing = json.loads(path.read_text(encoding="utf-8-sig"))
            if existing != payload:
                try:
                    migrate_legacy_project_owner_if_safe(
                        store_root=self.root,
                        source_root=self.owner.source_root,
                        expected_manifest=payload,
                    )
                except ErrorMemoryOwnerMigrationError as exc:
                    raise ErrorMemoryBackendError(
                        "ERROR_MEMORY_BACKEND_OWNER_MANIFEST_MISMATCH:"
                        + str(path)
                        + ":MIGRATION_BLOCKED:"
                        + str(exc)
                    ) from exc
                existing = json.loads(path.read_text(encoding="utf-8-sig"))
                if existing != payload:
                    raise ErrorMemoryBackendError(
                        "ERROR_MEMORY_BACKEND_OWNER_MANIFEST_MISMATCH:"
                        + str(path)
                        + ":MIGRATION_DID_NOT_CONVERGE"
                    )
        else:
            path.write_text(text, encoding="utf-8", newline="\n")
        return path


def project_error_memory_backend(
    selected_project_root: str | Path,
    *,
    tool_source_root: str | Path | None = None,
) -> ErrorMemoryBackend:
    """Return the explicit Project Error Memory backend."""
    owner = project_owner_context(
        selected_project_root,
        tool_source_root=tool_source_root,
        affected_box="Project Error Memory",
    )
    return ErrorMemoryBackend(
        owner=owner,
        root=owner.support_root / PROJECT_ERROR_MEMORY_DIR,
    )


def tool_error_memory_backend(
    tool_source_root: str | Path | None = None,
) -> ErrorMemoryBackend:
    """Return the explicit Tool Error Memory backend."""
    owner = tool_owner_context(
        tool_source_root,
        affected_box="Tool Error Memory",
    )
    return ErrorMemoryBackend(
        owner=owner,
        root=owner.support_root / TOOL_ERROR_MEMORY_DIR,
    )


def coerce_error_memory_backend(
    target: ErrorMemoryBackend | str | Path,
) -> ErrorMemoryBackend:
    """Return an explicit backend, preserving legacy Project-root callers."""
    if isinstance(target, ErrorMemoryBackend):
        return target
    try:
        return project_error_memory_backend(target)
    except (MemoryOwnershipError, OSError) as exc:
        raise ErrorMemoryBackendError(str(exc)) from exc
