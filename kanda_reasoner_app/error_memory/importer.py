# project-path: kanda_reasoner_app/error_memory/importer.py
"""Import helpers for Error Memory lesson ZIPs and AI formulary files.

This module repairs the GUI workflow gap where an Error Memory ZIP could be
installed into the canonical folder while the Error Memory tab did not have a
button to import that ZIP through the same store/index path used by the tab.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
import zipfile

from .backend import ErrorMemoryBackend, OwnerMetadataPolicy
from .intake import parse_error_lesson_ai_response, save_ai_form_as_lesson
from .schema import validate_lesson_shape
from .store import rebuild_index, save_lesson

__all__ = ["import_error_memory_file", "import_error_memory_zip"]

_TEXT_SUFFIXES = {".txt", ".md"}
_JSON_SUFFIXES = {".json"}
_MAX_MEMBER_BYTES = 2_000_000


def _safe_member_names(archive: zipfile.ZipFile) -> list[str]:
    """Return regular non-directory member names without path traversal."""
    names: list[str] = []
    for info in archive.infolist():
        if info.is_dir():
            continue
        name = info.filename.replace("\\", "/")
        if name.startswith("/") or "../" in name or name == ".." or name.startswith("../"):
            continue
        names.append(info.filename)
    return names


def _decode_member(archive: zipfile.ZipFile, member_name: str) -> str:
    """Read and decode one bounded text member from a ZIP archive."""
    info = archive.getinfo(member_name)
    if info.file_size > _MAX_MEMBER_BYTES:
        raise ValueError("Error Memory ZIP member is too large to import safely: " + member_name)
    data = archive.read(member_name)
    return data.decode("utf-8-sig", errors="replace")


def _looks_like_importable_text_lesson(text: str) -> bool:
    """Return whether a text member is a deliberate AI lesson payload.

    ZIP imports must be conservative.  Human helper files such as README.txt
    must not become draft lessons simply because they are readable text files.
    Plain text freeform intake remains a GUI/paste workflow; ZIP import only
    accepts marker-wrapped Error Memory lessons or JSON lesson/form payloads.
    """
    stripped = str(text or "").strip()
    if not stripped:
        return False
    if "KANDA_ERROR_LESSON_JSON_BEGIN" in stripped and "KANDA_ERROR_LESSON_JSON_END" in stripped:
        return True
    if stripped.startswith("{") and stripped.endswith("}"):
        return True
    return False


def _save_payload_or_form(
    *,
    selected_project_root: ErrorMemoryBackend | str | Path,
    payload: dict[str, Any],
    source_name: str,
) -> tuple[Path, dict[str, Any], str]:
    """Save a canonical lesson payload or convert an AI form payload."""
    ok, _failures = validate_lesson_shape(payload)
    if ok:
        path = save_lesson(
            selected_project_root,
            payload,
            owner_metadata_policy=OwnerMetadataPolicy.REQUIRE_MATCH,
        )
        return path, payload, "canonical_json"
    path, lesson = save_ai_form_as_lesson(
        selected_project_root=selected_project_root,
        form_inputs=payload,
        fallback_raw_error_text="Imported from Error Memory file: " + source_name,
        fallback_operation_phase=str(payload.get("operation_phase") or "unknown"),
    )
    return path, lesson, "ai_form_json"


def _import_json_text(
    *,
    selected_project_root: ErrorMemoryBackend | str | Path,
    text: str,
    source_name: str,
) -> list[dict[str, Any]]:
    """Import one JSON or marker-wrapped formulary text payload."""
    imported: list[dict[str, Any]] = []
    stripped = text.strip()
    payload: dict[str, Any] | None = None
    try:
        loaded = json.loads(stripped)
        if isinstance(loaded, dict):
            payload = loaded
    except json.JSONDecodeError:
        payload = None
    if payload is None:
        form = parse_error_lesson_ai_response(stripped)
        path, lesson = save_ai_form_as_lesson(
            selected_project_root=selected_project_root,
            form_inputs=form,
            fallback_raw_error_text="Imported from Error Memory file: " + source_name,
            fallback_operation_phase=str(form.get("operation_phase") or "unknown"),
        )
        imported.append(
            {
                "lesson_id": lesson.get("lesson_id", ""),
                "status": lesson.get("status", ""),
                "source": source_name,
                "saved_path": str(path),
                "import_kind": "ai_form_text",
            }
        )
        return imported
    path, lesson, import_kind = _save_payload_or_form(
        selected_project_root=selected_project_root,
        payload=payload,
        source_name=source_name,
    )
    imported.append(
        {
            "lesson_id": lesson.get("lesson_id", ""),
            "status": lesson.get("status", ""),
            "source": source_name,
            "saved_path": str(path),
            "import_kind": import_kind,
        }
    )
    return imported


def import_error_memory_zip(selected_project_root: ErrorMemoryBackend | str | Path, zip_path: str | Path) -> dict[str, Any]:
    """Import lessons from an Error Memory ZIP into the selected project's store.

    The ZIP is not extracted to disk.  JSON lesson files and marker-wrapped AI
    formulary text files are read in memory, passed through the canonical store,
    and the index is rebuilt so the GUI table refreshes immediately.
    """
    source = Path(zip_path).expanduser().resolve(strict=False)
    if not source.is_file():
        raise FileNotFoundError("Error Memory ZIP not found: " + str(source))
    if source.suffix.lower() != ".zip":
        raise ValueError("Expected an Error Memory ZIP: " + str(source))
    imported: list[dict[str, Any]] = []
    skipped: list[str] = []
    with zipfile.ZipFile(source) as archive:
        for member_name in _safe_member_names(archive):
            suffix = Path(member_name).suffix.lower()
            if suffix not in (_JSON_SUFFIXES | _TEXT_SUFFIXES):
                continue
            try:
                text = _decode_member(archive, member_name)
                if suffix in _TEXT_SUFFIXES and not _looks_like_importable_text_lesson(text):
                    skipped.append(member_name + ": skipped non-lesson text file")
                    continue
                imported.extend(
                    _import_json_text(
                        selected_project_root=selected_project_root,
                        text=text,
                        source_name=member_name,
                    )
                )
            except Exception as exc:
                skipped.append(member_name + ": " + str(exc))
    rebuild_index(selected_project_root)
    if not imported:
        raise ValueError("No importable Error Memory lesson found in ZIP. Skipped: " + "; ".join(skipped[:5]))
    return {
        "ok": True,
        "source_zip": str(source),
        "imported_count": len(imported),
        "imported_lessons": imported,
        "skipped": skipped,
    }


def import_error_memory_file(selected_project_root: ErrorMemoryBackend | str | Path, source_path: str | Path) -> dict[str, Any]:
    """Import an Error Memory ZIP, JSON lesson, or marker-wrapped text file."""
    source = Path(source_path).expanduser().resolve(strict=False)
    if not source.is_file():
        raise FileNotFoundError("Error Memory import file not found: " + str(source))
    suffix = source.suffix.lower()
    if suffix == ".zip":
        return import_error_memory_zip(selected_project_root, source)
    if suffix not in (_JSON_SUFFIXES | _TEXT_SUFFIXES):
        raise ValueError("Unsupported Error Memory import file type: " + str(source))
    imported = _import_json_text(
        selected_project_root=selected_project_root,
        text=source.read_text(encoding="utf-8-sig", errors="replace"),
        source_name=source.name,
    )
    rebuild_index(selected_project_root)
    return {
        "ok": True,
        "source_file": str(source),
        "imported_count": len(imported),
        "imported_lessons": imported,
        "skipped": [],
    }
