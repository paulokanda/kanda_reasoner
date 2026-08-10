# project-path: kanda_reasoner_app/error_memory/owner_migration.py
"""Fail-closed migration from legacy physical Project IDs to registry IDs."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.project_support_boundary import (
    legacy_physical_project_identity,
)

__all__ = [
    "ErrorMemoryOwnerMigrationError",
    "ErrorMemoryOwnerMigrationResult",
    "migrate_legacy_project_owner_if_safe",
    "restore_error_memory_owner_migration",
]

OWNER_FIELDS = (
    "owner_scope",
    "owner_id",
    "owner_slug",
    "owner_root_fingerprint",
    "affected_box",
)
MIGRATION_HISTORY_DIR = "owner_migration_history"


class ErrorMemoryOwnerMigrationError(RuntimeError):
    """Raised when owner migration cannot be proven safe."""


@dataclass(frozen=True)
class ErrorMemoryOwnerMigrationResult:
    """Describe one applied or unnecessary legacy-owner migration."""

    applied: bool
    status: str
    receipt_path: Path | None
    legacy_owner_id: str
    stable_owner_id: str
    migrated_lesson_count: int
    ownerless_lesson_count: int


def _read_json_object(path: Path, marker: str) -> dict[str, Any]:
    """Return one decoded JSON object or raise a bounded migration error."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ErrorMemoryOwnerMigrationError(marker + ":" + str(path)) from exc
    if not isinstance(payload, dict):
        raise ErrorMemoryOwnerMigrationError(marker + "_NOT_OBJECT:" + str(path))
    return payload


def _sha256(path: Path) -> str:
    """Return the SHA-256 digest of one physical file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    """Write deterministic JSON through an adjacent atomic replacement."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".kanda_owner_migration_" + uuid.uuid4().hex)
    temporary.write_text(
        json.dumps(dict(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)


def _owner_fields(payload: Mapping[str, Any]) -> dict[str, str]:
    """Return normalized owner metadata from one persistent object."""
    return {
        key: str(payload.get(key) or "").strip()
        for key in OWNER_FIELDS
    }


def _legacy_owner_match(
    supplied: Mapping[str, str],
    expected: Mapping[str, str],
    legacy_owner_id: str,
) -> bool:
    """Return whether owner metadata is exactly the retired same-Project ID."""
    return all(
        supplied.get(key) == (legacy_owner_id if key == "owner_id" else expected[key])
        for key in OWNER_FIELDS
    )


def _current_owner_match(
    supplied: Mapping[str, str],
    expected: Mapping[str, str],
) -> bool:
    """Return whether owner metadata already matches the stable registry ID."""
    return all(supplied.get(key) == expected[key] for key in OWNER_FIELDS)


def _classify_lessons(
    lessons_dir: Path,
    expected_owner: Mapping[str, str],
    legacy_owner_id: str,
) -> tuple[list[tuple[Path, dict[str, Any]]], int]:
    """Return exact legacy lessons and the accepted ownerless lesson count."""
    legacy_lessons: list[tuple[Path, dict[str, Any]]] = []
    ownerless_count = 0
    for path in sorted(lessons_dir.glob("lesson-*.json")):
        payload = _read_json_object(path, "OWNER_MIGRATION_LESSON_INVALID_JSON")
        supplied = _owner_fields(payload)
        if not any(supplied.values()):
            ownerless_count += 1
            continue
        if _current_owner_match(supplied, expected_owner):
            continue
        if _legacy_owner_match(supplied, expected_owner, legacy_owner_id):
            legacy_lessons.append((path, payload))
            continue
        raise ErrorMemoryOwnerMigrationError(
            "OWNER_MIGRATION_FOREIGN_OR_MIXED_LESSON:" + str(path)
        )
    return legacy_lessons, ownerless_count


def _updated_index(
    index_path: Path,
    expected_owner: Mapping[str, str],
    legacy_owner_id: str,
) -> dict[str, Any] | None:
    """Return an owner-reconciled index without hiding foreign records."""
    if not index_path.exists():
        return None
    payload = _read_json_object(index_path, "OWNER_MIGRATION_INDEX_INVALID_JSON")
    supplied = _owner_fields(payload)
    if not (
        _current_owner_match(supplied, expected_owner)
        or _legacy_owner_match(supplied, expected_owner, legacy_owner_id)
    ):
        raise ErrorMemoryOwnerMigrationError(
            "OWNER_MIGRATION_INDEX_OWNER_MISMATCH:" + str(index_path)
        )
    records = payload.get("lessons", [])
    if not isinstance(records, list):
        raise ErrorMemoryOwnerMigrationError(
            "OWNER_MIGRATION_INDEX_LESSONS_NOT_LIST:" + str(index_path)
        )
    for record in records:
        if not isinstance(record, dict):
            raise ErrorMemoryOwnerMigrationError(
                "OWNER_MIGRATION_INDEX_RECORD_NOT_OBJECT:" + str(index_path)
            )
        owner_id = str(record.get("owner_id") or "").strip()
        owner_scope = str(record.get("owner_scope") or "").strip()
        if not owner_id and not owner_scope:
            continue
        if owner_scope != expected_owner["owner_scope"]:
            raise ErrorMemoryOwnerMigrationError(
                "OWNER_MIGRATION_INDEX_FOREIGN_SCOPE:" + str(index_path)
            )
        if owner_id == legacy_owner_id:
            record["owner_id"] = expected_owner["owner_id"]
        elif owner_id != expected_owner["owner_id"]:
            raise ErrorMemoryOwnerMigrationError(
                "OWNER_MIGRATION_INDEX_FOREIGN_OWNER:" + str(index_path)
            )
    for key in OWNER_FIELDS:
        payload[key] = expected_owner[key]
    return payload


def _backup_files(
    store_root: Path,
    backup_root: Path,
    paths: list[Path],
) -> list[dict[str, str]]:
    """Copy exact migration inputs and return their provenance records."""
    records: list[dict[str, str]] = []
    for path in paths:
        relative = path.relative_to(store_root)
        backup = backup_root / relative
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
        records.append(
            {
                "relative_path": relative.as_posix(),
                "original_sha256": _sha256(path),
                "backup_path": str(backup),
                "backup_sha256": _sha256(backup),
            }
        )
    return records


def migrate_legacy_project_owner_if_safe(
    *,
    store_root: str | Path,
    source_root: str | Path,
    expected_manifest: Mapping[str, Any],
) -> ErrorMemoryOwnerMigrationResult:
    """Migrate only a proven same-Project legacy owner ID with exact backup."""
    root = Path(store_root).expanduser().resolve(strict=False)
    source = Path(source_root).expanduser().resolve(strict=False)
    expected = dict(expected_manifest)
    expected_owner = _owner_fields(expected)
    if expected_owner["owner_scope"] != "PROJECT":
        raise ErrorMemoryOwnerMigrationError("OWNER_MIGRATION_PROJECT_SCOPE_REQUIRED")
    manifest_path = root / "owner_manifest.json"
    existing = _read_json_object(
        manifest_path,
        "OWNER_MIGRATION_MANIFEST_INVALID_JSON",
    )
    if existing == expected:
        return ErrorMemoryOwnerMigrationResult(
            applied=False,
            status="OWNER_MANIFEST_ALREADY_CURRENT",
            receipt_path=None,
            legacy_owner_id="",
            stable_owner_id=expected_owner["owner_id"],
            migrated_lesson_count=0,
            ownerless_lesson_count=0,
        )
    legacy_owner_id, legacy_fingerprint = legacy_physical_project_identity(source)
    mismatches = {
        key for key, value in expected.items()
        if existing.get(key) != value
    }
    if mismatches != {"owner_id"}:
        raise ErrorMemoryOwnerMigrationError(
            "OWNER_MIGRATION_MANIFEST_MISMATCH_FIELDS:" + ",".join(sorted(mismatches))
        )
    if str(existing.get("owner_id") or "") != legacy_owner_id:
        raise ErrorMemoryOwnerMigrationError("OWNER_MIGRATION_LEGACY_ID_NOT_MATCHED")
    if expected_owner["owner_root_fingerprint"] != legacy_fingerprint:
        raise ErrorMemoryOwnerMigrationError("OWNER_MIGRATION_ROOT_FINGERPRINT_CHANGED")
    legacy_lessons, ownerless_count = _classify_lessons(
        root / "lessons",
        expected_owner,
        legacy_owner_id,
    )
    index_path = root / "lessons_index.json"
    updated_index = _updated_index(index_path, expected_owner, legacy_owner_id)
    changed_paths = [manifest_path, *[item[0] for item in legacy_lessons]]
    if index_path.exists():
        changed_paths.append(index_path)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_root = (
        root
        / MIGRATION_HISTORY_DIR
        / (timestamp + "_" + legacy_owner_id[:12] + "_to_" + expected_owner["owner_id"][:12])
    )
    backup_root.mkdir(parents=True, exist_ok=False)
    backup_records = _backup_files(root, backup_root / "backup", changed_paths)
    try:
        for path, payload in legacy_lessons:
            migrated = dict(payload)
            for key in OWNER_FIELDS:
                migrated[key] = expected_owner[key]
            _atomic_write_json(path, migrated)
        if updated_index is not None:
            _atomic_write_json(index_path, updated_index)
        _atomic_write_json(manifest_path, expected)
        changed_records = []
        for record in backup_records:
            current = root / Path(record["relative_path"])
            changed_records.append(
                {
                    **record,
                    "migrated_sha256": _sha256(current),
                }
            )
        receipt = {
            "schema_version": "1.0",
            "artifact_type": "error_memory_owner_migration_receipt",
            "status": "APPLIED",
            "store_root": str(root),
            "source_root": str(source),
            "legacy_owner_id": legacy_owner_id,
            "stable_owner_id": expected_owner["owner_id"],
            "root_fingerprint": expected_owner["owner_root_fingerprint"],
            "migrated_lesson_count": len(legacy_lessons),
            "ownerless_lesson_count": ownerless_count,
            "changed_files": changed_records,
            "applied_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        }
        receipt_path = backup_root / "migration_receipt.json"
        _atomic_write_json(receipt_path, receipt)
    except Exception:
        for record in reversed(backup_records):
            destination = root / Path(record["relative_path"])
            shutil.copy2(record["backup_path"], destination)
        raise
    return ErrorMemoryOwnerMigrationResult(
        applied=True,
        status="LEGACY_OWNER_MIGRATED_TO_REGISTRY_ID",
        receipt_path=receipt_path,
        legacy_owner_id=legacy_owner_id,
        stable_owner_id=expected_owner["owner_id"],
        migrated_lesson_count=len(legacy_lessons),
        ownerless_lesson_count=ownerless_count,
    )


def restore_error_memory_owner_migration(
    receipt_path: str | Path,
) -> dict[str, Any]:
    """Restore exact pre-migration bytes when migrated bytes are unchanged."""
    path = Path(receipt_path).expanduser().resolve(strict=True)
    receipt = _read_json_object(path, "OWNER_MIGRATION_RECEIPT_INVALID_JSON")
    store_root = Path(str(receipt.get("store_root") or "")).resolve(strict=True)
    records = receipt.get("changed_files", [])
    if not isinstance(records, list) or not records:
        raise ErrorMemoryOwnerMigrationError("OWNER_MIGRATION_RECEIPT_FILES_MISSING")
    for record in records:
        if not isinstance(record, dict):
            raise ErrorMemoryOwnerMigrationError("OWNER_MIGRATION_RECEIPT_RECORD_INVALID")
        destination = store_root / Path(str(record.get("relative_path") or ""))
        if _sha256(destination) != str(record.get("migrated_sha256") or ""):
            raise ErrorMemoryOwnerMigrationError(
                "OWNER_MIGRATION_ROLLBACK_CURRENT_HASH_MISMATCH:" + str(destination)
            )
        backup = Path(str(record.get("backup_path") or "")).resolve(strict=True)
        if _sha256(backup) != str(record.get("backup_sha256") or ""):
            raise ErrorMemoryOwnerMigrationError(
                "OWNER_MIGRATION_ROLLBACK_BACKUP_HASH_MISMATCH:" + str(backup)
            )
    for record in records:
        destination = store_root / Path(str(record["relative_path"]))
        shutil.copy2(str(record["backup_path"]), destination)
        if _sha256(destination) != str(record["original_sha256"]):
            raise ErrorMemoryOwnerMigrationError(
                "OWNER_MIGRATION_ROLLBACK_RESTORE_HASH_MISMATCH:" + str(destination)
            )
    rollback_receipt = {
        "schema_version": "1.0",
        "artifact_type": "error_memory_owner_migration_rollback_receipt",
        "migration_receipt": str(path),
        "restored_file_count": len(records),
        "restored_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    rollback_path = path.with_name("rollback_receipt.json")
    _atomic_write_json(rollback_path, rollback_receipt)
    return rollback_receipt
