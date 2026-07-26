# project-path: kanda_reasoner_app/freeze_after_update_gui/_frozen_list_worker.py
"""Background worker for List Frozen loading and state mutations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, Signal, Slot

from kanda_reasoner_app.freeze_after_update.contract import refresh_ai_compliance_context
from kanda_reasoner_app.freeze_after_update.frozen_entry_management import (
    activate_frozen_entries,
    delete_last_deprecated_entry,
    delete_selected_deprecated_entries,
    inactivate_frozen_entries,
    list_managed_frozen_entries,
    undelete_last_frozen_entry,
)

__all__ = ["FrozenListWorker"]

_ACTION_LOAD = "load"
_ACTION_DELETE_LAST = "delete_last"
_ACTION_DELETE_SELECTED = "delete_selected"
_ACTION_UNDELETE_LAST = "undelete_last"
_ACTION_INACTIVATE = "inactivate"
_ACTION_ACTIVATE = "activate"
_VALID_ACTIONS = {
    _ACTION_LOAD,
    _ACTION_DELETE_LAST,
    _ACTION_DELETE_SELECTED,
    _ACTION_UNDELETE_LAST,
    _ACTION_INACTIVATE,
    _ACTION_ACTIVATE,
}


class FrozenListWorker(QObject):
    """Perform one frozen-memory operation outside the Qt GUI thread."""

    progress = Signal(str)
    completed = Signal(object)
    failed = Signal(str)
    finished = Signal()

    def __init__(
        self,
        *,
        project_root: Path,
        action: str,
        selected_paths: list[Path] | None = None,
    ) -> None:
        super().__init__()
        if action not in _VALID_ACTIONS:
            raise ValueError("Unsupported List Frozen worker action: " + action)
        self._project_root = Path(project_root)
        self._action = action
        self._selected_paths = [Path(path) for path in (selected_paths or [])]

    @Slot()
    def run(self) -> None:
        """Execute one operation, refresh exposure once, and return one snapshot."""
        try:
            result: dict[str, Any] = {"ok": True, "action": self._action}
            exposure: dict[str, Any] | None = None
            if self._action != _ACTION_LOAD:
                self.progress.emit("Applying frozen-memory change...")
                result = self._execute_mutation()
                self.progress.emit("Updating AI freeze context...")
                exposure = refresh_ai_compliance_context(self._project_root)
            self.progress.emit("Loading frozen-entry index...")
            entries = list_managed_frozen_entries(self._project_root)
            self.completed.emit(
                {
                    "action": self._action,
                    "result": result,
                    "exposure": exposure,
                    "entries": entries,
                }
            )
        except Exception as exc:  # boundary: never strand the QThread lifecycle
            self.failed.emit(str(exc))
        finally:
            self.finished.emit()

    def _execute_mutation(self) -> dict[str, Any]:
        """Dispatch the selected governed frozen-memory mutation."""
        if self._action == _ACTION_DELETE_LAST:
            return delete_last_deprecated_entry(self._project_root)
        if self._action == _ACTION_DELETE_SELECTED:
            return delete_selected_deprecated_entries(
                self._project_root,
                self._selected_paths,
            )
        if self._action == _ACTION_UNDELETE_LAST:
            return undelete_last_frozen_entry(self._project_root)
        if self._action == _ACTION_INACTIVATE:
            return inactivate_frozen_entries(
                self._project_root,
                self._selected_paths,
            )
        if self._action == _ACTION_ACTIVATE:
            return activate_frozen_entries(
                self._project_root,
                self._selected_paths,
            )
        raise ValueError("List Frozen action is not a mutation: " + self._action)
