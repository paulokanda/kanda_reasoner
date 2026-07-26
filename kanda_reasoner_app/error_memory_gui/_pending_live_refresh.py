# project-path: kanda_reasoner_app/error_memory_gui/_pending_live_refresh.py
"""Live refresh bridge for staged Error Memory pending intake files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = [
    "initialize_pending_intake_live_refresh",
    "refresh_pending_intake_live",
]


PendingSignature = tuple[str, int, int]


def _pending_signature(path: Path) -> PendingSignature | None:
    """Return a stable file signature for one pending intake candidate."""
    try:
        resolved = Path(path).expanduser().resolve(strict=False)
        stat = resolved.stat()
    except OSError:
        return None
    return (str(resolved), int(stat.st_mtime_ns), int(stat.st_size))


def _pending_snapshot(tab: Any) -> tuple[PendingSignature, ...]:
    """Return the ordered snapshot of pending intake files visible to the tab."""
    signatures: list[PendingSignature] = []
    try:
        files = tab._pending_intake_files_for_all_candidate_dirs()
    except Exception:
        files = []
    for path in files:
        signature = _pending_signature(Path(path))
        if signature is not None:
            signatures.append(signature)
    return tuple(sorted(signatures, key=lambda item: item[0].casefold()))


def _snapshot_by_path(snapshot: tuple[PendingSignature, ...]) -> dict[str, PendingSignature]:
    """Index one pending snapshot by normalized resolved path."""
    return {item[0].casefold(): item for item in snapshot}


def _changed_paths(
    previous: tuple[PendingSignature, ...],
    current: tuple[PendingSignature, ...],
) -> list[str]:
    """Return paths that are new or whose mtime/size signature changed."""
    previous_by_path = _snapshot_by_path(previous)
    changed: list[str] = []
    for item in current:
        key = item[0].casefold()
        if previous_by_path.get(key) != item:
            changed.append(item[0])
    return changed


def _clear_stale_dismissal_for_changed_file(tab: Any, path_text: str) -> None:
    """Allow a genuinely changed pending payload to be reviewed again."""
    marker = str(Path(path_text).expanduser().resolve(strict=False))
    dismissed_files = getattr(tab, "_dismissed_pending_intake_files", None)
    if isinstance(dismissed_files, set):
        dismissed_files.discard(marker)

    lesson_id = ""
    try:
        text = Path(marker).read_text(encoding="utf-8-sig", errors="replace")
        lesson_id = str(tab._lesson_id_from_text_lenient(text) or "").strip()
    except Exception:
        lesson_id = ""

    dismissed_ids = getattr(tab, "_dismissed_pending_intake_lesson_ids", None)
    if lesson_id and isinstance(dismissed_ids, set):
        dismissed_ids.discard(lesson_id)


def _work_windows_are_busy(tab: Any) -> bool:
    """Return whether live refresh must avoid replacing visible review text."""
    if str(getattr(tab, "_loaded_pending_intake_file", "") or "").strip():
        return True
    for attr_name in ("raw_error_edit", "received_preview_edit"):
        editor = getattr(tab, attr_name, None)
        reader = getattr(editor, "toPlainText", None)
        if callable(reader) and str(reader() or "").strip():
            return True
    return False


def initialize_pending_intake_live_refresh(tab: Any) -> None:
    """Store the initial pending-intake snapshot for live change detection."""
    tab._pending_live_refresh_snapshot = _pending_snapshot(tab)
    tab._pending_live_refresh_deferred = False


def refresh_pending_intake_live(tab: Any) -> bool:
    """Refresh the GUI when a pending intake file is created or changed.

    This bridge only detects filesystem changes. Parsing, active-ready checks,
    duplicate classification, editor population, and final Memorize Error
    persistence remain owned by the existing Error Memory loader workflow.
    """
    current = _pending_snapshot(tab)
    previous = getattr(tab, "_pending_live_refresh_snapshot", None)

    if previous is None:
        tab._pending_live_refresh_snapshot = current
        return False

    changed = current != previous
    if changed:
        changed_paths = _changed_paths(previous, current)
        tab._pending_live_refresh_snapshot = current
        tab._pending_live_refresh_deferred = True

        for path_text in changed_paths:
            _clear_stale_dismissal_for_changed_file(tab, path_text)

        try:
            tab._reload_table()
        except Exception:
            pass

    if not bool(getattr(tab, "_pending_live_refresh_deferred", False)):
        return False
    if _work_windows_are_busy(tab):
        return False

    try:
        loaded = bool(tab.load_pending_ai_assisted_error_lesson_intake_now())
    except Exception:
        return False
    if loaded:
        tab._pending_live_refresh_deferred = False
    return loaded
