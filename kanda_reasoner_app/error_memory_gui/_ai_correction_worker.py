# project-path: kanda_reasoner_app/error_memory_gui/_ai_correction_worker.py
"""Qt worker for Error Memory local or Web AI correction requests."""

from __future__ import annotations

import traceback
from typing import Any

from PySide6.QtCore import QObject, Signal, Slot

from kanda_reasoner_app.error_memory_gui._ai_corrector_service import (
    correct_error_memory_lesson_with_local_ai,
)
from kanda_reasoner_app.error_memory_gui._web_ai_corrector_service import (
    correct_error_memory_lesson_with_web_ai,
)

__all__ = ["ErrorMemoryAICorrectionWorker"]


class ErrorMemoryAICorrectionWorker(QObject):
    """Run one Error Memory model correction outside the Qt GUI thread."""

    result_ready = Signal(object)
    failed = Signal(str, str)
    finished = Signal()

    def __init__(
        self,
        *,
        intake_text: str,
        editor_text: str,
        project_root: Any,
        provider_mode: str = "local",
        model_selection: str = "",
        gateway_id: str = "",
        web_model_id: str = "",
        api_key: str = "",
        request_id: str = "",
    ) -> None:
        super().__init__()
        self._intake_text = str(intake_text or "")
        self._editor_text = str(editor_text or "")
        self._project_root = project_root
        self._provider_mode = str(provider_mode or "local").strip().lower()
        self._model_selection = str(model_selection or "")
        self._gateway_id = str(gateway_id or "")
        self._web_model_id = str(web_model_id or "")
        self._api_key = str(api_key or "")
        self._request_id = str(request_id or "")

    @Slot()
    def run(self) -> None:
        """Execute the selected provider and always finish the worker lifecycle."""
        try:
            if self._provider_mode == "web":
                result = correct_error_memory_lesson_with_web_ai(
                    intake_text=self._intake_text,
                    editor_text=self._editor_text,
                    project_root=self._project_root,
                    gateway_id=self._gateway_id,
                    model_id=self._web_model_id,
                    api_key=self._api_key,
                    request_id=self._request_id,
                )
            else:
                result = correct_error_memory_lesson_with_local_ai(
                    intake_text=self._intake_text,
                    editor_text=self._editor_text,
                    project_root=self._project_root,
                    model_selection=self._model_selection,
                )
        except Exception as exc:  # Qt boundary: never leak exceptions from a slot
            self.failed.emit(
                "Unexpected Error Memory AI correction failure: " + str(exc),
                traceback.format_exc(),
            )
        else:
            self.result_ready.emit(result)
        finally:
            self.finished.emit()
