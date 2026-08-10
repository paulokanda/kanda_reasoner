# project-path: kanda_reasoner_app/error_memory/cross_owner_reference.py
"""Read-only cross-owner Error Memory lesson references."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .backend import ErrorMemoryBackend, ErrorMemoryBackendError

__all__ = [
    "CrossOwnerLessonReference",
    "create_cross_owner_reference",
    "create_cross_owner_reference_from_identity",
    "list_cross_owner_references",
    "load_cross_owner_reference",
    "resolve_cross_owner_reference",
]

_REFERENCE_TYPE = "cross_owner_lesson_reference"


@dataclass(frozen=True)
class CrossOwnerLessonReference:
    """Immutable pointer to a lesson owned by another canonical backend."""

    source_owner_scope: str
    source_owner_id: str
    lesson_id: str
    relationship: str = "applicable_prevention_guidance"

    def to_dict(self) -> dict[str, str]:
        return {
            "schema_version": "1.0",
            "artifact_type": _REFERENCE_TYPE,
            "source_owner_scope": self.source_owner_scope,
            "source_owner_id": self.source_owner_id,
            "lesson_id": self.lesson_id,
            "relationship": self.relationship,
        }


def _safe_reference_name(reference: CrossOwnerLessonReference) -> str:
    basis = (
        reference.source_owner_scope
        + "-"
        + reference.source_owner_id[:16]
        + "-"
        + reference.lesson_id
    )
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", basis).strip("._-")
    return safe + ".json"


def _write_reference(
    destination: ErrorMemoryBackend,
    reference: CrossOwnerLessonReference,
) -> Path:
    """Write one validated reference without lesson content."""
    if reference.source_owner_id == destination.owner.owner_id:
        raise ErrorMemoryBackendError(
            "CROSS_OWNER_REFERENCE_REQUIRES_FOREIGN_OWNER"
        )
    destination.ensure_dirs()
    path = destination.references_dir / _safe_reference_name(reference)
    payload = reference.to_dict()
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8-sig"))
        if existing != payload:
            raise ErrorMemoryBackendError(
                "CROSS_OWNER_REFERENCE_IDENTITY_COLLISION"
            )
        return path
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def create_cross_owner_reference_from_identity(
    destination: ErrorMemoryBackend,
    *,
    source_owner_scope: str,
    source_owner_id: str,
    lesson_id: str,
    relationship: str = "applicable_prevention_guidance",
) -> Path:
    """Create a reference from verified export identity metadata."""
    scope = str(source_owner_scope or "").strip()
    owner_id = str(source_owner_id or "").strip()
    lesson = str(lesson_id or "").strip()
    if scope not in {"TOOL", "PROJECT"}:
        raise ErrorMemoryBackendError(
            "CROSS_OWNER_REFERENCE_SOURCE_SCOPE_INVALID"
        )
    if not owner_id or not lesson:
        raise ErrorMemoryBackendError(
            "CROSS_OWNER_REFERENCE_SOURCE_IDENTITY_MISSING"
        )
    reference = CrossOwnerLessonReference(
        source_owner_scope=scope,
        source_owner_id=owner_id,
        lesson_id=lesson,
        relationship=str(
            relationship or "applicable_prevention_guidance"
        ),
    )
    return _write_reference(destination, reference)


def create_cross_owner_reference(
    destination: ErrorMemoryBackend,
    source: ErrorMemoryBackend,
    lesson_id: str,
    *,
    relationship: str = "applicable_prevention_guidance",
) -> Path:
    """Create a read-only reference without copying canonical lesson data."""
    from .store import load_lesson

    load_lesson(source, lesson_id)
    return create_cross_owner_reference_from_identity(
        destination,
        source_owner_scope=source.owner.owner_scope.value,
        source_owner_id=source.owner.owner_id,
        lesson_id=str(lesson_id),
        relationship=relationship,
    )


def load_cross_owner_reference(path: str | Path) -> CrossOwnerLessonReference:
    """Load one validated reference object."""
    payload = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict) or payload.get("artifact_type") != _REFERENCE_TYPE:
        raise ErrorMemoryBackendError("CROSS_OWNER_REFERENCE_INVALID")
    required = (
        "source_owner_scope",
        "source_owner_id",
        "lesson_id",
        "relationship",
    )
    missing = [key for key in required if not str(payload.get(key) or "").strip()]
    if missing:
        raise ErrorMemoryBackendError(
            "CROSS_OWNER_REFERENCE_FIELDS_MISSING:" + ",".join(missing)
        )
    return CrossOwnerLessonReference(
        source_owner_scope=str(payload["source_owner_scope"]),
        source_owner_id=str(payload["source_owner_id"]),
        lesson_id=str(payload["lesson_id"]),
        relationship=str(payload["relationship"]),
    )


def list_cross_owner_references(
    backend: ErrorMemoryBackend,
) -> list[CrossOwnerLessonReference]:
    """Return references without counting them as canonical lessons."""
    backend.ensure_dirs()
    result: list[CrossOwnerLessonReference] = []
    for path in sorted(backend.references_dir.glob("*.json")):
        try:
            result.append(load_cross_owner_reference(path))
        except Exception:
            continue
    return result


def resolve_cross_owner_reference(
    reference: CrossOwnerLessonReference,
    source: ErrorMemoryBackend,
) -> dict[str, Any]:
    """Resolve a reference through the exact owner-aware source backend."""
    if reference.source_owner_scope != source.owner.owner_scope.value:
        raise ErrorMemoryBackendError("CROSS_OWNER_REFERENCE_SCOPE_MISMATCH")
    if reference.source_owner_id != source.owner.owner_id:
        raise ErrorMemoryBackendError("CROSS_OWNER_REFERENCE_OWNER_ID_MISMATCH")
    from .store import load_lesson

    return dict(load_lesson(source, reference.lesson_id))
