# project-path: kanda_reasoner_app/manage_architecture/ai_review/qt_worker.py
"""Qt worker for Audit Project advisory review."""

from __future__ import annotations

from importlib import import_module

from .controller import build_tab1_ai_review_request, run_tab1_ai_review
from .models import LOCAL_AI_MODE

__all__ = ["Tab1AIReviewWorker"]


def _qt_core_attr(name: str):
    """Return one PySide6.QtCore attribute at GUI import time."""
    return getattr(import_module("PySide6.QtCore"), name)


QObject = _qt_core_attr("QObject")
Signal = _qt_core_attr("Signal")


class Tab1AIReviewWorker(QObject):
    """Run one advisory review outside the Audit Project GUI thread."""

    result_ready = Signal(object)

    def __init__(
        self,
        audit_text: str,
        project_root: str,
        model_name: str = "",
        *,
        provider_mode: str = LOCAL_AI_MODE,
        gateway_id: str = "",
        api_key: str = "",
        request_id: str = "",
    ) -> None:
        super().__init__()
        self._audit_text = str(audit_text or "")
        self._project_root = str(project_root or "")
        self._model_name = str(model_name or "")
        self._provider_mode = str(provider_mode or LOCAL_AI_MODE)
        self._gateway_id = str(gateway_id or "")
        self._api_key = str(api_key or "")
        self._request_id = str(request_id or "")

    def run(self) -> None:
        """Run the advisory review and emit one terminal result object."""
        request = build_tab1_ai_review_request(
            audit_text=self._audit_text,
            project_root=self._project_root,
            model_name=self._model_name,
            provider_mode=self._provider_mode,
            gateway_id=self._gateway_id,
            api_key=self._api_key,
            request_id=self._request_id,
        )
        self.result_ready.emit(run_tab1_ai_review(request))
