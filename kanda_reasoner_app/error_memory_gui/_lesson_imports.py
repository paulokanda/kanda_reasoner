# project-path: kanda_reasoner_app/error_memory_gui/_lesson_imports.py
"""Pure import-file helpers for Error Memory lesson payloads."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Callable

from kanda_reasoner_app.error_memory_gui._text_payloads import archive_entry_text

__all__ = [
    "formatted_import_text_for_window",
    "formatted_text_from_manifested_lesson_zip",
]

_ALLOWED_LESSON_IMPORT_SUFFIXES = {".json", ".txt", ".md"}
_MAX_IMPORT_MEMBER_BYTES = 2_000_000


def _normalized_member_name(name: str) -> str:
    """Return a ZIP member name with portable separators."""
    return str(name or "").replace("\\", "/")


def _is_safe_text_member(member_name: str, *, suffixes: set[str] = _ALLOWED_LESSON_IMPORT_SUFFIXES) -> bool:
    """Return whether a ZIP member is safe to scan as candidate lesson text."""
    normalized = _normalized_member_name(member_name)
    if not normalized or normalized.startswith("/") or "../" in normalized:
        return False
    return Path(normalized).suffix.lower() in suffixes


def formatted_text_from_manifested_lesson_zip(
    source: str | Path,
    *,
    is_formatted_lesson_payload: Callable[[str], bool],
) -> str:
    """Return the manifest-declared Error Lesson receive block when present.

    The direct Error Lesson ZIP contract is intentionally not a code-patch ZIP.
    It declares artifact_type=formatted_error_memory_lesson_zip and a receive_block
    path in bundle_manifest.json. Prefer that explicit path before falling back to
    scanning so bundle metadata cannot be mistaken for the lesson payload.
    """
    try:
        with zipfile.ZipFile(Path(source)) as archive:
            names = {_normalized_member_name(info.filename) for info in archive.infolist() if not info.is_dir()}
            if "bundle_manifest.json" not in names:
                return ""
            manifest_text = archive_entry_text(archive, "bundle_manifest.json")
            if not manifest_text:
                return ""
            manifest = json.loads(manifest_text)
            if not isinstance(manifest, dict):
                return ""
            if str(manifest.get("artifact_type", "")).strip() != "formatted_error_memory_lesson_zip":
                return ""
            receive_block = _normalized_member_name(str(manifest.get("receive_block", "")).strip())
            if not receive_block or receive_block not in names:
                return ""
            text = archive_entry_text(archive, receive_block)
            if is_formatted_lesson_payload(text):
                return text
    except Exception:
        return ""
    return ""


def formatted_import_text_for_window(
    selected: str | Path,
    *,
    is_formatted_lesson_payload: Callable[[str], bool],
) -> str:
    """Return formatted Error Memory lesson text from a selected ZIP/JSON/TXT/MD file."""
    source = Path(selected).expanduser().resolve(strict=False)
    try:
        if source.suffix.lower() == ".zip":
            manifested_text = formatted_text_from_manifested_lesson_zip(
                source,
                is_formatted_lesson_payload=is_formatted_lesson_payload,
            )
            if manifested_text:
                return manifested_text
            with zipfile.ZipFile(source) as archive:
                for info in archive.infolist():
                    if info.is_dir() or info.file_size > _MAX_IMPORT_MEMBER_BYTES:
                        continue
                    member_name = _normalized_member_name(info.filename)
                    if not _is_safe_text_member(member_name):
                        continue
                    text = archive.read(info).decode("utf-8-sig", errors="replace").strip()
                    if is_formatted_lesson_payload(text):
                        return text
            return ""
        if source.suffix.lower() in _ALLOWED_LESSON_IMPORT_SUFFIXES:
            text = source.read_text(encoding="utf-8-sig", errors="replace").strip()
            if is_formatted_lesson_payload(text):
                return text
    except Exception:
        return ""
    return ""
