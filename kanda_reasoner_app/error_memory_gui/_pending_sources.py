# project-path: kanda_reasoner_app/error_memory_gui/_pending_sources.py
"""Pending source path and deletion helpers for the Error Memory GUI tab."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from kanda_reasoner_app.error_memory.paths import resolve_project_error_memory_root
from kanda_reasoner_app.error_memory_gui._text_payloads import lesson_id_from_text_lenient

__all__ = [
    "candidate_pending_ai_assisted_intake_dirs",
    "delete_matching_pending_intake_files",
    "pending_file_matches_draft_identity",
    "pending_intake_dirs_for_root_hint",
    "pending_intake_files_for_candidate_dirs",
    "safe_pending_lesson_id_from_file",
]


def _resolved_path(value: str | Path | None) -> Path | None:
    """Return a best-effort resolved Path or None for invalid input."""
    if value is None:
        return None
    try:
        return Path(value).expanduser().resolve(strict=False)
    except Exception:
        return None


def pending_intake_dirs_for_root_hint(root_hint: str | Path, *, pending_dir_name: str) -> list[Path]:
    """Return possible pending-intake folders for one root hint."""
    root = _resolved_path(root_hint)
    if root is None:
        return []
    candidates: list[Path] = []
    if root.name == pending_dir_name:
        candidates.append(root)
    if root.name == "project_error_memory":
        candidates.append(root / pending_dir_name)
    if root.name.endswith("_show_project_to_AI"):
        candidates.append(root / "project_error_memory" / pending_dir_name)
    candidates.append(resolve_project_error_memory_root(root) / pending_dir_name)
    candidates.append(root / "project_error_memory" / pending_dir_name)
    return candidates


def candidate_pending_ai_assisted_intake_dirs(root_hints: Iterable[str | Path | None], *, pending_dir_name: str) -> list[Path]:
    """Return pending-intake folders in priority order without duplicates."""
    normalized_hints: list[Path] = []
    seen_hints: set[str] = set()
    for value in root_hints:
        path = _resolved_path(value)
        if path is None:
            continue
        key = str(path).casefold()
        if key in seen_hints:
            continue
        seen_hints.add(key)
        normalized_hints.append(path)

    dirs: list[Path] = []
    seen_dirs: set[str] = set()
    for hint in normalized_hints:
        for candidate in pending_intake_dirs_for_root_hint(hint, pending_dir_name=pending_dir_name):
            key = str(candidate.resolve(strict=False)).casefold()
            if key in seen_dirs:
                continue
            seen_dirs.add(key)
            dirs.append(candidate)
    return dirs


def safe_pending_lesson_id_from_file(pending_file: Path) -> str:
    """Return a stable draft lesson_id for a raw pending intake file."""
    stem = Path(pending_file).stem.strip().lower() or "pending-error"
    stem = stem.replace("raw_error_evidence_", "").replace("kanda_error_lesson_json_", "")
    safe = "".join(ch if ch.isalnum() else "-" for ch in stem)
    safe = "-".join(part for part in safe.split("-") if part)
    if not safe:
        safe = "pending-error"
    return "lesson-pending-" + safe[:96]


def pending_intake_files_for_candidate_dirs(candidate_dirs: Iterable[Path], *, allowed_suffixes: set[str]) -> list[Path]:
    """Return all pending intake files visible to the loader."""
    files: list[Path] = []
    seen: set[str] = set()
    normalized_suffixes = {str(item).lower() for item in allowed_suffixes}
    for pending_dir in candidate_dirs:
        if not pending_dir.exists():
            continue
        try:
            items = sorted(
                item
                for item in pending_dir.iterdir()
                if item.is_file() and item.suffix.lower() in normalized_suffixes
            )
        except Exception:
            continue
        for item in items:
            key = str(item.resolve(strict=False)).casefold()
            if key in seen:
                continue
            seen.add(key)
            files.append(item)
    return files


def pending_file_matches_draft_identity(
    path: Path,
    lesson_ids: set[str],
    visible_texts: Sequence[str],
    explicit_paths: Sequence[str],
) -> bool:
    """Return whether one pending source belongs to the draft being deleted."""
    marker = str(path.resolve(strict=False))
    if any(marker.casefold() == str(item).casefold() for item in explicit_paths):
        return True
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace").strip()
    except Exception:
        text = ""
    if text and any(text == visible for visible in visible_texts):
        return True
    lesson_id = lesson_id_from_text_lenient(text)
    if lesson_id and lesson_id in lesson_ids:
        return True
    safe_name = path.stem.casefold()
    return any(lesson_id.casefold() in safe_name for lesson_id in lesson_ids if lesson_id)


def delete_matching_pending_intake_files(
    lesson_ids: set[str],
    visible_texts: Sequence[str],
    explicit_paths: Sequence[str],
    visible_pending_files: Iterable[Path],
) -> tuple[int, list[str], set[str]]:
    """Delete every staged pending intake file for the current draft."""
    deleted_count = 0
    failures: list[str] = []
    dismissed_markers: set[str] = set()
    candidate_paths: list[Path] = []
    seen: set[str] = set()

    def add_candidate(path_value: str | Path) -> None:
        path = _resolved_path(path_value)
        if path is None:
            return
        key = str(path).casefold()
        if key in seen:
            return
        seen.add(key)
        candidate_paths.append(path)

    for marker in explicit_paths:
        add_candidate(marker)
    for item in visible_pending_files:
        add_candidate(item)

    for candidate in candidate_paths:
        if not pending_file_matches_draft_identity(candidate, lesson_ids, visible_texts, explicit_paths):
            continue
        marker = str(candidate.resolve(strict=False))
        try:
            if candidate.exists() and candidate.is_file():
                candidate.unlink()
                deleted_count += 1
            dismissed_markers.add(marker)
        except Exception as exc:
            dismissed_markers.add(marker)
            failures.append(str(candidate) + " -> " + str(exc))
    return (deleted_count, failures, dismissed_markers)
