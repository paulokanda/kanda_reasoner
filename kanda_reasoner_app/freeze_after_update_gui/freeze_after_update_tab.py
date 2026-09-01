# project-path: kanda_reasoner_app/freeze_after_update_gui/freeze_after_update_tab.py
"""GUI tab for project-local Freeze Feature After Update governance."""

from __future__ import annotations

import queue
import threading
from pathlib import Path
from typing import Any

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QDialog, QTextEdit, QWidget

from kanda_reasoner_app.freeze_after_update_gui._box_actions import FreezeBoxActionsMixin
from kanda_reasoner_app.freeze_after_update_gui._freeze_memory_exports import (
    FreezeMemoryExportMixin,
)
from kanda_reasoner_app.freeze_after_update_gui._frozen_list_dialog import (
    FreezeFrozenListMixin,
)
from kanda_reasoner_app.freeze_after_update_gui._frozen_library_transfer import (
    FreezeFrozenLibraryTransferMixin,
)
from kanda_reasoner_app.freeze_after_update_gui._local_freeze_dialog_runtime import (
    FreezeLocalEntryRuntimeMixin,
)
from kanda_reasoner_app.freeze_after_update_gui._local_freeze_dialog_widgets import (
    FreezeLocalFreezeDialogSupportMixin,
)
from kanda_reasoner_app.freeze_after_update_gui._path_controls import (
    FreezePathControlsMixin,
)
from kanda_reasoner_app.freeze_after_update_gui._ui_builder import FreezeUiBuilderMixin

__all__ = ["FreezeAfterUpdateTab"]


class FreezeAfterUpdateTab(
    FreezeFrozenLibraryTransferMixin,
    FreezeUiBuilderMixin,
    FreezePathControlsMixin,
    FreezeBoxActionsMixin,
    FreezeMemoryExportMixin,
    FreezeFrozenListMixin,
    FreezeLocalFreezeDialogSupportMixin,
    FreezeLocalEntryRuntimeMixin,
    QWidget,
):
    """Human-facing controller for the external project freeze box."""

    def __init__(self) -> None:
        super().__init__()
        self._last_output_folder: Path | None = None
        self._pending_staged_project_root: Path | None = None
        self._pending_staged_action: str | None = None
        self._local_freeze_preview: dict | None = None
        self._local_freeze_dialog: QDialog | None = None
        self._what_to_say_dialog: QDialog | None = None
        self._what_to_say_text_edit: QTextEdit | None = None
        self._frozen_list_dialog: QDialog | None = None
        self._project_root_controls_moved = False
        self._local_freeze_ai_thread: threading.Thread | None = None
        self._local_freeze_ai_result_queue: queue.Queue | None = None
        self._local_freeze_ai_request_id: str | None = None
        self._local_freeze_ai_identity: Any = None
        self._local_freeze_ai_generation = 0
        self._local_freeze_ai_poll_timer: QTimer | None = None
        self._local_freeze_bootstrap_generation = 0
        self._local_freeze_bootstrap_job: Any = None
        self._local_freeze_bootstrap_retired_jobs: list[Any] = []
        self._freeze_web_ai_configuration: Any = None
        self._build_ui()
        self._connect_signals()
