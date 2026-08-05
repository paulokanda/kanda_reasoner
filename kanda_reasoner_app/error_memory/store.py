# project-path: kanda_reasoner_app/error_memory/store.py
"""Owner-aware canonical Error Memory lesson store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .backend import (
    ErrorMemoryBackend,
    ErrorMemoryBackendError,
    OwnerMetadataPolicy,
    coerce_error_memory_backend,
)
from .schema import validate_lesson_shape, write_schema_if_missing

__all__ = [
    "bootstrap_error_memory_store",
    "delete_lesson",
    "list_lessons",
    "load_lesson",
    "rebuild_index",
    "save_lesson",
]


def bootstrap_error_memory_store(
    target: ErrorMemoryBackend | str | Path,
) -> dict[str, Any]:
    """Create one backend, owner manifest, schema, and index when needed."""
    backend = coerce_error_memory_backend(target)
    paths = backend.ensure_dirs()
    owner_manifest = backend.write_backend_manifest()
    schema_path = write_schema_if_missing(backend)
    if not backend.index_path.exists():
        _write_index(backend, [])
    return {
        "paths": {key: str(value) for key, value in paths.items()},
        "schema": str(schema_path),
        "index": str(backend.index_path),
        "owner_manifest": str(owner_manifest),
        "owner": backend.canonical_owner_fields(),
    }


def _safe_lesson_id(lesson_id: str) -> str:
    """Return a filesystem-safe lesson ID."""
    safe_id = "".join(
        ch if ch.isalnum() or ch in {"-", "_"} else "_"
        for ch in str(lesson_id)
    )
    if not safe_id.startswith("lesson-"):
        safe_id = "lesson-" + safe_id
    return safe_id


def _lesson_path(backend: ErrorMemoryBackend, lesson_id: str) -> Path:
    """Return one canonical lesson path inside an explicit backend."""
    return backend.lessons_dir / (_safe_lesson_id(lesson_id) + ".json")


def _read_lesson_path(
    backend: ErrorMemoryBackend,
    path: Path,
    *,
    allow_legacy_ownerless: bool,
) -> dict[str, Any]:
    """Read and owner-validate one lesson file."""
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("Lesson file is not a JSON object: " + str(path))
    backend.validate_persisted_owner(
        payload,
        allow_legacy_ownerless=allow_legacy_ownerless,
    )
    return payload


def load_lesson(
    target: ErrorMemoryBackend | str | Path,
    lesson_id: str,
    *,
    allow_legacy_ownerless: bool = True,
) -> dict[str, Any]:
    """Load one owner-validated canonical lesson JSON object."""
    backend = coerce_error_memory_backend(target)
    return _read_lesson_path(
        backend,
        _lesson_path(backend, lesson_id),
        allow_legacy_ownerless=allow_legacy_ownerless,
    )


def _index_record(lesson: dict[str, Any]) -> dict[str, Any]:
    """Return the lightweight index record for one lesson."""
    fingerprint = lesson.get("fingerprint", {})
    if not isinstance(fingerprint, dict):
        fingerprint = {}
    return {
        "lesson_id": lesson.get("lesson_id", ""),
        "status": lesson.get("status", ""),
        "symptom": lesson.get("symptom", ""),
        "do_not_repeat_rule": lesson.get("do_not_repeat_rule", ""),
        "updated_at_utc": lesson.get("updated_at_utc", ""),
        "fingerprint_hash": fingerprint.get("fingerprint_hash", ""),
        "owner_scope": lesson.get("owner_scope", ""),
        "owner_id": lesson.get("owner_id", ""),
    }


def _write_index(
    backend: ErrorMemoryBackend,
    lessons: list[dict[str, Any]],
) -> dict[str, Any]:
    """Write one deterministic owner-scoped lesson index."""
    index = {
        "schema_version": "1.0",
        "artifact_type": "error_memory_lesson_index",
        **backend.canonical_owner_fields(),
        "lessons": lessons,
    }
    backend.index_path.write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return index


def rebuild_index(
    target: ErrorMemoryBackend | str | Path,
) -> dict[str, Any]:
    """Rebuild the lightweight index from owner-valid lesson files."""
    backend = coerce_error_memory_backend(target)
    bootstrap_error_memory_store(backend)
    records: list[dict[str, Any]] = []
    for path in sorted(backend.lessons_dir.glob("lesson-*.json")):
        try:
            payload = _read_lesson_path(
                backend,
                path,
                allow_legacy_ownerless=True,
            )
            ok, _failures = validate_lesson_shape(payload)
            if ok:
                records.append(_index_record(payload))
        except Exception:
            continue
    return _write_index(backend, records)


def save_lesson(
    target: ErrorMemoryBackend | str | Path,
    lesson: dict[str, Any],
    *,
    owner_metadata_policy: OwnerMetadataPolicy = OwnerMetadataPolicy.SYSTEM_ASSIGN,
) -> Path:
    """Validate and save one canonical owner-scoped lesson JSON file."""
    backend = coerce_error_memory_backend(target)
    bootstrap_error_memory_store(backend)
    canonical = backend.assign_owner_metadata(
        lesson,
        policy=owner_metadata_policy,
    )
    ok, failures = validate_lesson_shape(canonical)
    if not ok:
        raise ValueError("Invalid Error Memory lesson: " + "; ".join(failures))
    path = _lesson_path(backend, str(canonical.get("lesson_id", "")))
    path.write_text(
        json.dumps(canonical, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rebuild_index(backend)
    lesson.clear()
    lesson.update(canonical)
    return path


def delete_lesson(
    target: ErrorMemoryBackend | str | Path,
    lesson_id: str,
) -> dict[str, Any]:
    """Delete one canonical lesson file and rebuild the owner index."""
    backend = coerce_error_memory_backend(target)
    bootstrap_error_memory_store(backend)
    payload = load_lesson(backend, lesson_id)
    path = _lesson_path(backend, lesson_id)
    if path.exists():
        path.unlink()
    rebuild_index(backend)
    return payload


def list_lessons(
    target: ErrorMemoryBackend | str | Path,
    *,
    include_inactive: bool = True,
    allow_legacy_ownerless: bool = True,
) -> list[dict[str, Any]]:
    """Return full canonical lessons from exactly one owner backend."""
    backend = coerce_error_memory_backend(target)
    bootstrap_error_memory_store(backend)
    result: list[dict[str, Any]] = []
    for path in sorted(backend.lessons_dir.glob("lesson-*.json")):
        try:
            payload = _read_lesson_path(
                backend,
                path,
                allow_legacy_ownerless=allow_legacy_ownerless,
            )
        except (OSError, ValueError, ErrorMemoryBackendError, json.JSONDecodeError):
            continue
        if include_inactive or payload.get("status") == "active":
            result.append(payload)
    return result
