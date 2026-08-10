# project-path: kanda_reasoner_app/error_memory_gui/_portable_owner_contract.py
"""Owner contracts for portable Error Memory backup and merge workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from kanda_reasoner_app.error_memory.backend import (
    ErrorMemoryBackend,
    ErrorMemoryBackendError,
    OWNER_METADATA_FIELDS,
    OwnerMetadataPolicy,
)

__all__ = [
    "PortableSourceOwner",
    "owner_manifest_fields",
    "owner_policy_for_same_owner_lesson",
    "portable_source_owner",
]


@dataclass(frozen=True)
class PortableSourceOwner:
    """Verified canonical owner identity declared by one portable export."""

    owner_scope: str
    owner_id: str
    owner_slug: str
    owner_root_fingerprint: str
    affected_box: str

    def as_dict(self) -> dict[str, str]:
        return {
            "owner_scope": self.owner_scope,
            "owner_id": self.owner_id,
            "owner_slug": self.owner_slug,
            "owner_root_fingerprint": self.owner_root_fingerprint,
            "affected_box": self.affected_box,
        }


def owner_manifest_fields(backend: ErrorMemoryBackend) -> dict[str, str]:
    """Return system-assigned owner fields for a portable export manifest."""
    return backend.canonical_owner_fields()


def portable_source_owner(manifest: Mapping[str, Any]) -> PortableSourceOwner:
    """Load one complete source-owner identity from an export manifest."""
    values = {
        key: str(manifest.get(key) or "").strip()
        for key in OWNER_METADATA_FIELDS
    }
    missing = [key for key, value in values.items() if not value]
    if missing:
        raise ErrorMemoryBackendError(
            "PORTABLE_SOURCE_OWNER_METADATA_MISSING:" + ",".join(missing)
        )
    if values["owner_scope"] not in {"TOOL", "PROJECT"}:
        raise ErrorMemoryBackendError("PORTABLE_SOURCE_OWNER_SCOPE_INVALID")
    return PortableSourceOwner(**values)


def owner_policy_for_same_owner_lesson(
    target: ErrorMemoryBackend,
    source: PortableSourceOwner,
    lesson: Mapping[str, Any],
) -> OwnerMetadataPolicy:
    """Return the safe write policy for a same-owner backup restore."""
    if source.owner_id != target.owner.owner_id:
        raise ErrorMemoryBackendError("PORTABLE_SOURCE_OWNER_IS_FOREIGN")
    supplied = [str(lesson.get(key) or "").strip() for key in OWNER_METADATA_FIELDS]
    if any(supplied):
        return OwnerMetadataPolicy.REQUIRE_MATCH
    return OwnerMetadataPolicy.SYSTEM_ASSIGN
