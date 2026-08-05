# project-path: kanda_reasoner_app/error_memory_gui/_portable_transfer.py
"""Portable folder export/import actions for project-scoped Error Memory lessons.

The transfer contract is a complete portable backup plus merge-only restore.
Export copies every valid saved lesson across all statuses without applying the
compact AI-export cap. A successful export is all-or-nothing: it never reports a
partial backup. Import never deletes or replaces current lessons; it validates
the portable folder and adds only lessons that do not match the canonical Error
Memory duplicate-family rules.
"""
from __future__ import annotations

__all__ = [
    "ERROR_MEMORY_EXPORT_MANIFEST",
    "export_error_lessons_folder",
    "export_errors_from_tab",
    "import_error_lessons_folder",
    "import_errors_into_tab",
]

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

from kanda_reasoner_app.error_memory.backend import project_error_memory_backend
from kanda_reasoner_app.error_memory.cross_owner_reference import (
    create_cross_owner_reference_from_identity,
)
from kanda_reasoner_app.error_memory.paths import resolve_error_memory_lessons_dir
from kanda_reasoner_app.error_memory.schema import validate_lesson_shape
from kanda_reasoner_app.error_memory.store import (
    bootstrap_error_memory_store,
    list_lessons,
    rebuild_index,
    save_lesson,
)
from kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard import (
    lesson_matches_candidate_error,
)
from kanda_reasoner_app.error_memory_gui._portable_owner_contract import (
    owner_manifest_fields,
    owner_policy_for_same_owner_lesson,
    portable_source_owner,
)

ERROR_MEMORY_EXPORT_MANIFEST = "KANDA_ERROR_MEMORY_EXPORT.json"
ERROR_MEMORY_EXPORT_ARTIFACT_TYPE = "kanda_error_memory_portable_export"
ERROR_MEMORY_EXPORT_SCHEMA_VERSION = "1.0"
ERROR_MEMORY_EXPORTER_VERSION = "1.1"
ERROR_MEMORY_EXPORT_LESSONS_DIR = "lessons"
_MAX_LESSON_BYTES = 2_000_000
_MAX_LESSON_COUNT = 5_000

def _utc_now_iso() -> str:
    """Return a stable second-resolution UTC timestamp."""
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _sha256_bytes(data: bytes) -> str:
    """Return the SHA-256 digest for bytes."""
    return hashlib.sha256(data).hexdigest()


def _safe_slug(value: str) -> str:
    """Return a portable folder-name slug."""
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value or "").strip())
    return slug.strip("._-") or "project"


def _unique_export_folder(destination_parent: Path, project_slug: str) -> Path:
    """Return a new timestamped export folder below the selected destination."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    base_name = "kanda_error_memory_export_" + _safe_slug(project_slug) + "_" + stamp
    candidate = destination_parent / base_name
    suffix = 2
    while candidate.exists():
        candidate = destination_parent / (base_name + "_" + str(suffix).zfill(2))
        suffix += 1
    return candidate


def _read_lesson_object(path: Path) -> tuple[bytes, dict[str, Any]]:
    """Read one bounded canonical lesson JSON object."""
    size = path.stat().st_size
    if size > _MAX_LESSON_BYTES:
        raise ValueError("lesson file exceeds 2 MB: " + path.name)
    raw = path.read_bytes()
    payload = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError("lesson file is not a JSON object: " + path.name)
    ok, failures = validate_lesson_shape(payload)
    if not ok:
        raise ValueError("invalid lesson: " + "; ".join(failures))
    lesson_id = str(payload.get("lesson_id") or "").strip()
    if not lesson_id:
        raise ValueError("lesson_id is empty: " + path.name)
    return raw, payload


def _atomic_write_text(path: Path, text: str) -> None:
    """Write one UTF-8 text file atomically."""
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def export_error_lessons_folder(
    selected_project_root: str | Path,
    destination_parent: str | Path,
) -> dict[str, Any]:
    """Copy all valid saved lessons into a portable export folder.

    Existing source lessons are read only. The export includes active, draft,
    deprecated, and superseded lessons, applies no compact-export cap, and
    records per-file SHA-256 values. Any invalid lesson aborts the export so a
    successful result is always a complete backup of the canonical lesson set.
    """
    root = Path(selected_project_root).expanduser().resolve(strict=True)
    destination = Path(destination_parent).expanduser().resolve(strict=True)
    if not destination.is_dir():
        raise NotADirectoryError("Export destination is not a folder: " + str(destination))

    backend = project_error_memory_backend(root)
    bootstrap_error_memory_store(backend)
    rebuild_index(backend)
    source_lessons = resolve_error_memory_lessons_dir(backend)
    export_root = _unique_export_folder(destination, root.name)
    export_lessons = export_root / ERROR_MEMORY_EXPORT_LESSONS_DIR
    export_lessons.mkdir(parents=True, exist_ok=False)

    exported: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    source_files = sorted(path for path in source_lessons.glob("lesson-*.json") if path.is_file())
    if len(source_files) > _MAX_LESSON_COUNT:
        raise ValueError("Error Memory contains more than 5000 lesson files.")

    try:
        for source in source_files:
            raw, lesson = _read_lesson_object(source)
            destination_file = export_lessons / source.name
            destination_file.write_bytes(raw)
            exported.append(
                {
                    "lesson_id": str(lesson.get("lesson_id") or ""),
                    "status": str(lesson.get("status") or ""),
                    "file": source.name,
                    "sha256": _sha256_bytes(raw),
                    "size_bytes": len(raw),
                }
            )

        manifest = {
            "artifact_type": ERROR_MEMORY_EXPORT_ARTIFACT_TYPE,
            **owner_manifest_fields(backend),
            "schema_version": ERROR_MEMORY_EXPORT_SCHEMA_VERSION,
            "exporter_version": ERROR_MEMORY_EXPORTER_VERSION,
            "source_project_slug": backend.owner.owner_slug,
            "exported_at_utc": _utc_now_iso(),
            "lesson_count": len(exported),
            "lessons_directory": ERROR_MEMORY_EXPORT_LESSONS_DIR,
            "lessons": exported,
            "skipped": skipped,
            "backup_contract": {
                "scope": "all_valid_saved_lessons",
                "status_filter": "none",
                "compact_limit_applied": False,
                "preserve_source_bytes": True,
                "partial_success_allowed": False,
            },
            "merge_contract": {
                "import_mode": "merge_unique_only",
                "delete_current_lessons": False,
                "replace_current_lessons": False,
                "duplicate_owner": "canonical_error_memory_duplicate_family_rules",
            },
        }
        _atomic_write_text(
            export_root / ERROR_MEMORY_EXPORT_MANIFEST,
            json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False),
        )
    except Exception:
        for path in sorted(export_root.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                path.rmdir()
        if export_root.exists():
            export_root.rmdir()
        raise

    return {
        "ok": True,
        "export_folder": str(export_root),
        "manifest": str(export_root / ERROR_MEMORY_EXPORT_MANIFEST),
        "source_lesson_count": len(source_files),
        "exported_count": len(exported),
        "skipped_count": len(skipped),
        "skipped": skipped,
        "backup_complete": len(exported) == len(source_files),
        "compact_limit_applied": False,
    }


def _resolve_export_root(selected_folder: str | Path) -> tuple[Path, dict[str, Any]]:
    """Resolve a selected export root or its lessons child and load its manifest."""
    selected = Path(selected_folder).expanduser().resolve(strict=True)
    if not selected.is_dir():
        raise NotADirectoryError("Selected import path is not a folder: " + str(selected))
    candidates = [selected]
    if selected.name == ERROR_MEMORY_EXPORT_LESSONS_DIR:
        candidates.append(selected.parent)
    for candidate in candidates:
        manifest_path = candidate / ERROR_MEMORY_EXPORT_MANIFEST
        if not manifest_path.is_file():
            continue
        payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        if not isinstance(payload, dict):
            raise ValueError("Error Memory export manifest is not a JSON object.")
        if payload.get("artifact_type") != ERROR_MEMORY_EXPORT_ARTIFACT_TYPE:
            raise ValueError("Selected folder is not a KANDA Error Memory portable export.")
        if str(payload.get("schema_version") or "") != ERROR_MEMORY_EXPORT_SCHEMA_VERSION:
            raise ValueError("Unsupported Error Memory export schema version.")
        return candidate, payload
    raise FileNotFoundError(
        "The selected folder does not contain " + ERROR_MEMORY_EXPORT_MANIFEST + "."
    )


def _fingerprint_hash(lesson: dict[str, Any]) -> str:
    """Return a lesson fingerprint hash when available."""
    fingerprint = lesson.get("fingerprint")
    if not isinstance(fingerprint, dict):
        return ""
    return str(fingerprint.get("fingerprint_hash") or "").strip()


def _duplicate_reason(
    candidate: dict[str, Any],
    stored_lessons: list[dict[str, Any]],
) -> tuple[str, str]:
    """Return canonical duplicate reason and stored lesson id, if any."""
    candidate_id = str(candidate.get("lesson_id") or "").strip()
    candidate_hash = _fingerprint_hash(candidate)
    for stored in stored_lessons:
        stored_id = str(stored.get("lesson_id") or "").strip()
        if candidate_id and stored_id == candidate_id:
            return "same lesson_id", stored_id
        stored_hash = _fingerprint_hash(stored)
        if candidate_hash and stored_hash and candidate_hash == stored_hash:
            return "same fingerprint.fingerprint_hash", stored_id
        if lesson_matches_candidate_error(candidate, stored):
            return "canonical duplicate-family match", stored_id
    return "", ""


def import_error_lessons_folder(
    selected_project_root: str | Path,
    selected_export_folder: str | Path,
) -> dict[str, Any]:
    """Restore same-owner lessons or create foreign-owner references.

    A portable export from the same canonical owner may restore unique lesson
    files. A foreign-owner export never becomes local canonical history; each
    accepted item becomes a read-only cross-owner reference instead.
    """
    root = Path(selected_project_root).expanduser().resolve(strict=True)
    target_backend = project_error_memory_backend(root)
    export_root, manifest = _resolve_export_root(selected_export_folder)
    source_owner = portable_source_owner(manifest)
    lessons_dir_name = str(manifest.get("lessons_directory") or "")
    if lessons_dir_name != ERROR_MEMORY_EXPORT_LESSONS_DIR:
        raise ValueError("Error Memory export lessons_directory is invalid.")
    export_lessons = (export_root / lessons_dir_name).resolve(strict=True)
    if export_lessons.parent != export_root.resolve(strict=True):
        raise ValueError("Error Memory export lessons path escaped its export root.")

    entries = manifest.get("lessons")
    if not isinstance(entries, list):
        raise ValueError("Error Memory export manifest lessons must be a list.")
    if len(entries) > _MAX_LESSON_COUNT:
        raise ValueError("Error Memory export contains more than 5000 lessons.")
    if int(manifest.get("lesson_count") or 0) != len(entries):
        raise ValueError("Error Memory export lesson_count does not match its manifest.")

    bootstrap_error_memory_store(target_backend)
    rebuild_index(target_backend)
    target_lessons_dir = resolve_error_memory_lessons_dir(target_backend)
    existing_files = {
        path.resolve(strict=True): path.read_bytes()
        for path in target_lessons_dir.glob("lesson-*.json")
        if path.is_file()
    }
    stored_lessons = list_lessons(target_backend, include_inactive=True)
    same_owner = source_owner.owner_id == target_backend.owner.owner_id
    accepted: list[dict[str, Any]] = []
    reference_candidates: list[dict[str, Any]] = []
    duplicates: list[dict[str, str]] = []
    invalid: list[dict[str, str]] = []

    for entry in entries:
        if not isinstance(entry, dict):
            invalid.append({"file": "", "reason": "manifest lesson entry is not an object"})
            continue
        filename = str(entry.get("file") or "").strip()
        if (
            Path(filename).name != filename
            or not filename.startswith("lesson-")
            or not filename.endswith(".json")
        ):
            invalid.append({"file": filename, "reason": "unsafe lesson filename"})
            continue
        source = export_lessons / filename
        try:
            raw, lesson = _read_lesson_object(source)
            expected_sha = str(entry.get("sha256") or "").strip().lower()
            if not expected_sha or _sha256_bytes(raw) != expected_sha:
                raise ValueError("SHA-256 mismatch")
            declared_id = str(entry.get("lesson_id") or "").strip()
            lesson_id = str(lesson.get("lesson_id") or "").strip()
            if declared_id != lesson_id:
                raise ValueError("manifest lesson_id does not match lesson JSON")
        except Exception as exc:
            invalid.append({"file": filename, "reason": str(exc)})
            continue

        if same_owner:
            reason, stored_id = _duplicate_reason(lesson, stored_lessons + accepted)
            if reason:
                duplicates.append(
                    {
                        "lesson_id": str(lesson.get("lesson_id") or ""),
                        "matched_lesson_id": stored_id,
                        "reason": reason,
                    }
                )
                continue
            accepted.append(lesson)
        else:
            reference_candidates.append(lesson)

    created_paths: list[Path] = []
    created_reference_paths: list[Path] = []
    try:
        if same_owner:
            for lesson in accepted:
                policy = owner_policy_for_same_owner_lesson(
                    target_backend, source_owner, lesson
                )
                saved = save_lesson(
                    target_backend,
                    lesson,
                    owner_metadata_policy=policy,
                ).resolve(strict=True)
                if saved in existing_files:
                    raise RuntimeError(
                        "Import attempted to replace a current lesson: " + saved.name
                    )
                created_paths.append(saved)
        else:
            for lesson in reference_candidates:
                created_reference_paths.append(
                    create_cross_owner_reference_from_identity(
                        target_backend,
                        source_owner_scope=source_owner.owner_scope,
                        source_owner_id=source_owner.owner_id,
                        lesson_id=str(lesson.get("lesson_id") or ""),
                    )
                )
        rebuild_index(target_backend)
        for path, original_bytes in existing_files.items():
            if not path.is_file() or path.read_bytes() != original_bytes:
                raise RuntimeError("Import modified a current lesson: " + path.name)
    except Exception:
        for candidate_path in target_lessons_dir.glob("lesson-*.json"):
            resolved = candidate_path.resolve(strict=False)
            if resolved not in existing_files and candidate_path.is_file():
                candidate_path.unlink()
        for path in created_reference_paths:
            if path.is_file():
                path.unlink()
        for path, original_bytes in existing_files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(original_bytes)
        rebuild_index(target_backend)
        raise

    return {
        "ok": True,
        "source_export_folder": str(export_root),
        "imported_count": len(accepted) if same_owner else 0,
        "referenced_count": len(created_reference_paths),
        "duplicate_count": len(duplicates),
        "invalid_count": len(invalid),
        "imported_lesson_ids": [
            str(item.get("lesson_id") or "") for item in accepted
        ],
        "referenced_lesson_ids": [
            str(item.get("lesson_id") or "")
            for item in reference_candidates
        ],
        "duplicates": duplicates,
        "invalid": invalid,
        "merge_only": True,
        "same_owner_restore": same_owner,
        "foreign_owner_reference_only": not same_owner,
        "current_lessons_deleted": 0,
        "current_lessons_replaced": 0,
    }


def _dialog_start_folder(project_root: Path) -> Path:
    """Return a stable existing folder for transfer dialogs."""
    drive_root = Path(project_root.anchor or str(project_root)).resolve(strict=False)
    return drive_root if drive_root.exists() else project_root


def _choose_directory(tab: Any, *, title: str, start_folder: Path) -> str:
    """Return one selected directory, with a narrow validator seam."""
    provider = getattr(tab, "_error_memory_transfer_directory_picker", None)
    if callable(provider):
        return str(provider(title, str(start_folder)) or "")
    from PySide6.QtWidgets import QFileDialog

    return QFileDialog.getExistingDirectory(tab, title, str(start_folder))


def export_errors_from_tab(tab: Any) -> None:
    """Choose a folder and export every valid current-project lesson."""
    from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

    root = tab._current_project_root()
    selected = _choose_directory(
        tab,
        title="Select folder for Error Memory export",
        start_folder=_dialog_start_folder(root),
    )
    if not selected:
        return
    try:
        result = export_error_lessons_folder(root, selected)
    except Exception as exc:
        show_error_copy_close_window(tab, title="Export Errors failed", message=str(exc))
        return
    detail = (
        "Complete backup lessons: " + str(result["exported_count"])
        + "\nAll statuses included: YES"
        + "\nCompact export cap applied: NO"
        + "\nPartial backup allowed: NO"
        + "\n\nExport folder:\n" + str(result["export_folder"])
    )
    tab._show_action_done(
        "Export Errors",
        "Complete Error Memory backup created.",
        detail,
    )


def import_errors_into_tab(tab: Any) -> None:
    """Choose a portable export folder and merge only unique lessons."""
    from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window

    root = tab._current_project_root()
    selected = _choose_directory(
        tab,
        title="Select exported Error Memory folder",
        start_folder=_dialog_start_folder(root),
    )
    if not selected:
        return
    try:
        result = import_error_lessons_folder(root, selected)
    except Exception as exc:
        show_error_copy_close_window(tab, title="Import Errors failed", message=str(exc))
        return
    tab._reload_table()
    detail_lines = [
        "Canonical lessons imported: " + str(result["imported_count"])
        + " | Foreign-owner references: " + str(result["referenced_count"]),
        "Duplicate lessons skipped: " + str(result["duplicate_count"]),
        "Invalid lessons skipped: " + str(result["invalid_count"]),
        "Current lessons deleted: 0",
        "Current lessons replaced: 0",
        "",
        "Source export folder:",
        str(result["source_export_folder"]),
    ]
    tab._show_action_done(
        "Import Errors",
        "Exported Error Memory lessons were merged into the current project.",
        "\n".join(detail_lines),
    )
