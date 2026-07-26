# project-path: kanda_reasoner_app/error_memory_gui/_duplicate_pending_cleanup.py
"""Pending-source cleanup for duplicate Error Memory candidates."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory_gui._memorize_duplicate_guard import (
    lesson_matches_candidate_error,
)

__all__ = [
    "delete_matching_pending_duplicate_candidates",
]


def _normalized_path(value: str | Path | None) -> Path | None:
    """Return a best-effort normalized path."""
    if value is None:
        return None
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return Path(text).expanduser().resolve(strict=False)
    except Exception:
        return None


def _candidate_pending_files(tab: Any) -> list[Path]:
    """Return visible pending intake files from the tab facade."""
    getter = getattr(tab, "_pending_intake_files_for_all_candidate_dirs", None)
    if not callable(getter):
        return []
    try:
        return [Path(item).expanduser().resolve(strict=False) for item in getter()]
    except Exception:
        return []


def _loaded_pending_file(tab: Any) -> Path | None:
    """Return the currently loaded pending file when present."""
    return _normalized_path(getattr(tab, "_loaded_pending_intake_file", ""))


def _text_for_file(path: Path) -> str:
    """Read a pending file as text."""
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace").strip()
    except Exception:
        return ""


def _normalized_text(value: Any) -> str:
    """Return lowercase search text with stable separators."""
    text = str(value or "").lower().replace("\\", "/")
    return " ".join(text.split())


def _candidate_search_terms(candidate: dict[str, Any]) -> list[str]:
    """Return conservative text terms that can identify raw pending files."""
    terms: list[str] = []
    for key in ("lesson_id", "raw_error_text", "symptom", "do_not_repeat_rule"):
        text = _normalized_text(candidate.get(key))
        if len(text) >= 24 and text not in terms:
            terms.append(text)
    fingerprint = candidate.get("fingerprint")
    if isinstance(fingerprint, dict):
        hash_text = _normalized_text(fingerprint.get("fingerprint_hash"))
        if len(hash_text) >= 16 and hash_text not in terms:
            terms.append(hash_text)
        components = fingerprint.get("components")
        if isinstance(components, list):
            for item in components:
                text = _normalized_text(item)
                if len(text) >= 12 and text not in terms:
                    terms.append(text)
    return terms


def _raw_text_matches_candidate(text: str, path: Path, candidate: dict[str, Any]) -> bool:
    """Return whether unparsed pending text appears to belong to candidate."""
    haystack = _normalized_text(text + " " + str(path.name))
    if not haystack:
        return False
    for term in _candidate_search_terms(candidate):
        if term and term in haystack:
            return True
    return False


def _lesson_from_pending_text(tab: Any, text: str) -> dict[str, Any] | None:
    """Parse one pending text payload into a lesson when possible."""
    if not text:
        return None
    parser = getattr(tab, "_lesson_from_formatted_text", None)
    if not callable(parser):
        return None
    try:
        lesson = parser(text)
    except Exception:
        return None
    return dict(lesson) if isinstance(lesson, dict) else None


def _pending_file_matches_candidate(tab: Any, path: Path, candidate: dict[str, Any]) -> bool:
    """Return whether a pending file represents the same candidate error."""
    text = _text_for_file(path)
    lesson = _lesson_from_pending_text(tab, text)
    if isinstance(lesson, dict) and lesson_matches_candidate_error(candidate, lesson):
        return True
    candidate_id = str(candidate.get("lesson_id") or "").strip()
    if candidate_id:
        try:
            lesson_id_from_text = getattr(tab, "_lesson_id_from_text_lenient")
            pending_id = str(lesson_id_from_text(text) or "").strip()
        except Exception:
            pending_id = ""
        if pending_id and pending_id == candidate_id:
            return True
        if candidate_id.casefold() in path.stem.casefold():
            return True
    return _raw_text_matches_candidate(text, path, candidate)


def _dismiss_pending_marker(tab: Any, path: Path, lesson_id: str) -> None:
    """Mark a pending file and lesson id dismissed for the current session."""
    marker = str(path.expanduser().resolve(strict=False))
    try:
        tab._dismissed_pending_intake_files.add(marker)
    except Exception:
        pass
    if lesson_id:
        try:
            tab._dismissed_pending_intake_lesson_ids.add(lesson_id)
        except Exception:
            pass
    if str(getattr(tab, "_loaded_pending_intake_file", "")).strip() == marker:
        try:
            tab._loaded_pending_intake_file = ""
            tab._loaded_pending_intake_lesson_id = ""
        except Exception:
            pass


def delete_matching_pending_duplicate_candidates(
    tab: Any,
    candidate: dict[str, Any],
    *,
    include_loaded_candidate: bool = True,
) -> tuple[int, tuple[str, ...]]:
    """Delete pending files that duplicate the candidate error.

    This cleans the Lessons table virtual pending rows after duplicate cleanup.
    It never deletes saved Lessons; saved Lesson cleanup is owned by
    _memorize_duplicate_guard.resolve_duplicate_lesson_copies.
    """
    if not isinstance(candidate, dict):
        return (0, ())
    files: list[Path] = []
    seen: set[str] = set()
    force_delete_keys: set[str] = set()

    def key_for(path: Path) -> str:
        return str(path.expanduser().resolve(strict=False)).casefold()

    def add(path: Path | None, *, force: bool = False) -> None:
        if path is None:
            return
        key = key_for(path)
        if force:
            force_delete_keys.add(key)
        if key in seen:
            return
        seen.add(key)
        files.append(path)

    if include_loaded_candidate:
        add(_loaded_pending_file(tab), force=True)
    for path in _candidate_pending_files(tab):
        add(path)

    deleted: list[str] = []
    failures: list[str] = []
    candidate_id = str(candidate.get("lesson_id") or "").strip()
    for path in files:
        forced = key_for(path) in force_delete_keys
        if not forced and not _pending_file_matches_candidate(tab, path, candidate):
            continue
        marker = str(path.expanduser().resolve(strict=False))
        try:
            if path.exists() and path.is_file():
                path.unlink()
                deleted.append(marker)
            _dismiss_pending_marker(tab, path, candidate_id)
        except Exception as exc:
            failures.append(marker + " -> " + str(exc))
            _dismiss_pending_marker(tab, path, candidate_id)
    return (len(deleted), tuple(failures))
