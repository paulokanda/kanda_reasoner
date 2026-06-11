
"""State models for guided folder-by-folder docstring runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


FOLDER_STATE_NOT_STARTED = "not_started"
FOLDER_STATE_GENERATED_PENDING_REVIEW = "generated_pending_review"
FOLDER_STATE_PARTIALLY_APPROVED = "partially_approved"
FOLDER_STATE_APPLIED_CLEAN = "applied_clean"
FOLDER_STATE_APPLIED_WITH_SKIPS = "applied_with_skips"
FOLDER_STATE_BLOCKED_BY_SYNTAX_ERROR = "blocked_by_syntax_error"
FOLDER_STATE_BLOCKED_BY_VALIDATION_ERROR = "blocked_by_validation_error"
FOLDER_STATE_SKIPPED_BY_USER = "skipped_by_user"

RESOLVED_FOLDER_STATES = {
    FOLDER_STATE_APPLIED_CLEAN,
    FOLDER_STATE_APPLIED_WITH_SKIPS,
    FOLDER_STATE_SKIPPED_BY_USER,
}

BLOCKED_FOLDER_STATES = {
    FOLDER_STATE_BLOCKED_BY_SYNTAX_ERROR,
    FOLDER_STATE_BLOCKED_BY_VALIDATION_ERROR,
}


@dataclass(frozen=True)
class FolderQueueItem:
    """Describe one folder in a guided docstring run queue."""

    relative_path: str
    python_files: tuple[str, ...]
    state: str = FOLDER_STATE_NOT_STARTED
    error: str = ""

    def is_resolved(self) -> bool:
        """Return True when this folder can be left without more action."""
        return self.state in RESOLVED_FOLDER_STATES

    def is_blocked(self) -> bool:
        """Return True when this folder needs user action before continuing."""
        return self.state in BLOCKED_FOLDER_STATES


@dataclass(frozen=True)
class GuidedFolderSession:
    """Persist folder-by-folder progress without touching insertion logic."""

    project_root: str
    folder_queue: tuple[FolderQueueItem, ...]
    current_index: int = 0
    settings: dict[str, Any] = field(default_factory=dict)
    last_report_path: str = ""

    def current_folder(self) -> FolderQueueItem | None:
        """Return the active folder or None when the queue is empty."""
        if not self.folder_queue:
            return None
        if self.current_index < 0 or self.current_index >= len(self.folder_queue):
            return None
        return self.folder_queue[self.current_index]

    def next_unresolved_index(self) -> int | None:
        """Return the first unresolved folder index at or after current_index."""
        for index in range(max(self.current_index, 0), len(self.folder_queue)):
            if not self.folder_queue[index].is_resolved():
                return index
        for index, item in enumerate(self.folder_queue):
            if not item.is_resolved():
                return index
        return None

    def can_continue_to_next_folder(self) -> bool:
        """Return True when the current folder is resolved."""
        current = self.current_folder()
        if current is None:
            return True
        return current.is_resolved()
