# project-path: kanda_reasoner_app/freeze_after_update_gui/_frozen_list_dialog.py
"""Responsive floating frozen-entry manager for Freeze Feature After Update."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from PySide6.QtCore import QThread, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableView,
    QVBoxLayout,
)

from ._frozen_list_model import FrozenEntryTableModel
from ._frozen_list_worker import FrozenListWorker

__all__ = ["FreezeFrozenListMixin", "FrozenListDialog"]


class FrozenListDialog(QDialog):
    """Non-modal responsive manager for active and deprecated frozen entries."""

    def __init__(
        self,
        parent,
        *,
        project_root: Path,
        log_callback: Callable[[str], None],
        status_callback: Callable[[str], None],
    ) -> None:
        super().__init__(parent)
        self.project_root = project_root
        self._log = log_callback
        self._set_parent_status = status_callback
        self._entries: list[dict[str, Any]] = []
        self._worker_thread: QThread | None = None
        self._worker: FrozenListWorker | None = None
        self._busy = False
        self._pending_action_name = ""
        self.setWindowTitle("List Frozen")
        self.resize(1180, 680)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
        self._build_ui()
        self.refresh_table()

    def _build_ui(self) -> None:
        """Build the frozen-entry manager controls."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        intro = QLabel(
            "Frozen entries are listed newest first. Active entries are green. "
            "Deprecated entries are red and may be deleted. Deletion is reversible "
            "through Undelete Last Deletion."
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)
        self.summary_label = QLabel("Loading frozen entries...")
        self.summary_label.setWordWrap(True)
        layout.addWidget(self.summary_label)
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("freeze_list_frozen_progress")
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        self.table_model = FrozenEntryTableModel(self)
        self.table = QTableView()
        self.table.setObjectName("freeze_list_frozen_table")
        self.table.setModel(self.table_model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table, 1)
        button_row = QHBoxLayout()
        button_row.setSpacing(8)
        self.delete_last_button = QPushButton("Delete Last")
        self.delete_last_button.setToolTip("Delete the newest deprecated frozen entry")
        self.delete_selected_button = QPushButton("Delete Selected")
        self.delete_selected_button.setToolTip(
            "Delete selected deprecated entries; active entries are protected"
        )
        self.undelete_button = QPushButton("Undelete Last Deletion")
        self.inactivate_button = QPushButton("Inactivate")
        self.activate_button = QPushButton("Activate")
        self.close_button = QPushButton("Close")
        self._action_buttons = (
            self.delete_last_button,
            self.delete_selected_button,
            self.undelete_button,
            self.inactivate_button,
            self.activate_button,
        )
        for button in self._action_buttons:
            button_row.addWidget(button)
        button_row.addStretch(1)
        button_row.addWidget(self.close_button)
        layout.addLayout(button_row)
        self.delete_last_button.clicked.connect(self._delete_last)
        self.delete_selected_button.clicked.connect(self._delete_selected)
        self.undelete_button.clicked.connect(self._undelete_last)
        self.inactivate_button.clicked.connect(self._inactivate_selected)
        self.activate_button.clicked.connect(self._activate_selected)
        self.close_button.clicked.connect(self.close)

    def refresh_table(self) -> None:
        """Reload frozen-entry state without blocking the Qt GUI thread."""
        self._start_worker("REFRESH FROZEN LIST", "load")

    def _selected_rows(self) -> list[int]:
        """Return selected table rows in visual order."""
        selection_model = self.table.selectionModel()
        if selection_model is None:
            return []
        return sorted({index.row() for index in selection_model.selectedRows()})

    def _selected_paths(self) -> list[Path]:
        """Return unique selected entry paths in table order."""
        paths: list[Path] = []
        for row in self._selected_rows():
            entry = self.table_model.entry_at(row)
            if entry is not None:
                paths.append(Path(entry["path"]))
        return paths

    def _selected_entries(self) -> list[dict[str, Any]]:
        """Return selected entry metadata in table order."""
        result: list[dict[str, Any]] = []
        for row in self._selected_rows():
            entry = self.table_model.entry_at(row)
            if entry is not None:
                result.append(entry)
        return result

    def _require_selection(self) -> list[Path]:
        """Return selected paths or show a concise notice."""
        paths = self._selected_paths()
        if not paths:
            QMessageBox.information(
                self,
                "Selection required",
                "Select one or more frozen entries first.",
            )
        return paths

    def _confirm(self, title: str, message: str) -> bool:
        """Return whether the user explicitly confirms one management action."""
        answer = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return answer == QMessageBox.StandardButton.Yes

    def _start_worker(
        self,
        action_name: str,
        action: str,
        selected_paths: list[Path] | None = None,
    ) -> None:
        """Start one background load or mutation operation."""
        if self._busy:
            self._set_parent_status("List Frozen is already updating. No duplicate action was started.")
            return
        self._pending_action_name = action_name
        self._set_busy(True, action_name.replace("_", " ").title() + "...")
        thread = QThread(self)
        worker = FrozenListWorker(
            project_root=self.project_root,
            action=action,
            selected_paths=selected_paths,
        )
        worker.moveToThread(thread)
        self._worker_thread = thread
        self._worker = worker
        thread.started.connect(worker.run)
        worker.progress.connect(self._on_worker_progress)
        worker.completed.connect(self._on_worker_completed)
        worker.failed.connect(self._on_worker_failed)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(self._on_worker_thread_finished)
        thread.finished.connect(thread.deleteLater)
        thread.start()

    def _set_busy(self, busy: bool, message: str = "") -> None:
        """Project one background-operation state onto the controls."""
        self._busy = busy
        self.progress_bar.setVisible(busy)
        self.table.setEnabled(not busy)
        for button in self._action_buttons:
            button.setEnabled(not busy)
        self.close_button.setEnabled(not busy)
        if message:
            self.summary_label.setText(message)
            self._set_parent_status(message)

    def _on_worker_progress(self, message: str) -> None:
        """Render one worker progress phase on the GUI thread."""
        self.summary_label.setText(message)
        self._set_parent_status(message)

    def _on_worker_completed(self, payload: object) -> None:
        """Apply one immutable worker result snapshot on the GUI thread."""
        data = dict(payload) if isinstance(payload, dict) else {}
        entries = data.get("entries") or []
        self._entries = list(entries)
        self.table_model.replace_entries(self._entries)
        active_count = sum(1 for entry in self._entries if entry.get("active"))
        deprecated_count = len(self._entries) - active_count
        self.summary_label.setText(
            f"Total: {len(self._entries)} | Active: {active_count} | "
            f"Deprecated: {deprecated_count}"
        )
        self._log(
            "LIST FROZEN REFRESH: total=" + str(len(self._entries))
            + " active=" + str(active_count)
            + " deprecated=" + str(deprecated_count)
        )
        result = data.get("result") or {}
        exposure = data.get("exposure")
        if data.get("action") == "load":
            self._set_parent_status("Frozen list loaded without blocking the interface.")
            return
        self._log(self._pending_action_name + " OK: " + str(result))
        if isinstance(exposure, dict) and exposure.get("startup_context_refreshed"):
            self._log("LIST FROZEN STARTUP CONTEXT REFRESHED")
            self._set_parent_status(
                self._pending_action_name + " completed and freeze context refreshed."
            )
            return
        errors = exposure.get("errors") if isinstance(exposure, dict) else []
        self._log(
            "LIST FROZEN CONTEXT REFRESH WARNING: "
            + "; ".join(map(str, errors or []))
        )
        self._set_parent_status(
            self._pending_action_name
            + " completed; freeze-context refresh warning logged."
        )

    def _on_worker_failed(self, message: str) -> None:
        """Show one background-operation failure without stranding the thread."""
        action_name = self._pending_action_name or "List Frozen"
        self._log(action_name + " FAILED: " + message)
        self.summary_label.setText(action_name + " failed: " + message)
        self._set_parent_status(action_name + " failed. See the List Frozen warning.")
        QMessageBox.warning(self, action_name + " failed", message)

    def _on_worker_thread_finished(self) -> None:
        """Release worker ownership and restore controls after thread exit."""
        self._worker = None
        self._worker_thread = None
        self._set_busy(False)

    def _delete_last(self) -> None:
        """Delete the newest deprecated entry."""
        deprecated = next((entry for entry in self._entries if not entry.get("active")), None)
        if deprecated is None:
            QMessageBox.information(
                self,
                "Nothing to delete",
                "No deprecated frozen entry is available.",
            )
            return
        if not self._confirm(
            "Delete last deprecated freeze",
            "Move the newest deprecated entry to reversible deleted storage?\n\n"
            + str(deprecated.get("feature_title") or deprecated.get("freeze_id")),
        ):
            return
        self._start_worker("DELETE LAST FROZEN", "delete_last")

    def _delete_selected(self) -> None:
        """Delete selected deprecated entries only."""
        entries = self._selected_entries()
        if not entries:
            self._require_selection()
            return
        if any(entry.get("active") for entry in entries):
            QMessageBox.warning(
                self,
                "Active entries protected",
                "Active frozen entries cannot be deleted. Inactivate them first.",
            )
            return
        if not self._confirm(
            "Delete selected freezes",
            "Move " + str(len(entries))
            + " selected deprecated entrie(s) to reversible deleted storage?",
        ):
            return
        self._start_worker(
            "DELETE SELECTED FROZEN",
            "delete_selected",
            [Path(entry["path"]) for entry in entries],
        )

    def _undelete_last(self) -> None:
        """Restore the most recently deleted entry."""
        self._start_worker("UNDELETE LAST FROZEN", "undelete_last")

    def _inactivate_selected(self) -> None:
        """Mark selected entries deprecated."""
        paths = self._require_selection()
        if not paths:
            return
        if not self._confirm(
            "Inactivate frozen entries",
            "Mark " + str(len(paths)) + " selected entrie(s) as deprecated?",
        ):
            return
        self._start_worker("INACTIVATE FROZEN", "inactivate", paths)

    def _activate_selected(self) -> None:
        """Mark selected entries active and clear superseded_by."""
        paths = self._require_selection()
        if not paths:
            return
        if not self._confirm(
            "Activate frozen entries",
            "Activate " + str(len(paths)) + " selected entrie(s)?",
        ):
            return
        self._start_worker("ACTIVATE FROZEN", "activate", paths)

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802
        """Prevent deleting the dialog while its owned QThread is still active."""
        if self._busy:
            event.ignore()
            self._set_parent_status(
                "List Frozen is updating in the background. Close is available when it finishes."
            )
            return
        super().closeEvent(event)


class FreezeFrozenListMixin:
    """Open and own the non-modal List Frozen window."""

    def _show_frozen_list_window(self) -> None:
        """Open or raise the current floating frozen-entry manager."""
        existing = getattr(self, "_frozen_list_dialog", None)
        if existing is not None and existing.isVisible():
            existing.raise_()
            existing.activateWindow()
            existing.refresh_table()
            return
        project_root = self._require_project_root()
        if project_root is None:
            return
        dialog = FrozenListDialog(
            self,
            project_root=project_root,
            log_callback=self._append_log,
            status_callback=self.status_label.setText,
        )

        def clear_reference(_result: int = 0) -> None:
            if getattr(self, "_frozen_list_dialog", None) is dialog:
                self._frozen_list_dialog = None

        dialog.finished.connect(clear_reference)
        self._frozen_list_dialog = dialog
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()
