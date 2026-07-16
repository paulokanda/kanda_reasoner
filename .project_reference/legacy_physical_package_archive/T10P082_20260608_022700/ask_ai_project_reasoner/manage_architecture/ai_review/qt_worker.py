"""Qt worker for Tab 1 advisory AI review."""

from __future__ import annotations

from importlib import import_module

from .controller import build_tab1_ai_review_request, run_tab1_ai_review

__all__ = ["Tab1AIReviewWorker"]


def _qt_core_attr(name: str):
    """Return one PySide6.QtCore attribute at GUI import time."""
    return getattr(import_module("PySide6.QtCore"), name)


QObject = _qt_core_attr("QObject")
Signal = _qt_core_attr("Signal")


class Tab1AIReviewWorker(QObject):
    """Run advisory AI review outside the Tab 1 GUI thread."""

    result_ready = Signal(object)

    def __init__(
        self,
        audit_text: str,
        project_root: str,
        model_name: str = "",
    ) -> None:
        super().__init__()
        self._audit_text = str(audit_text or "")
        self._project_root = str(project_root or "")
        self._model_name = str(model_name or "")

    def run(self) -> None:
        """Run the advisory review and emit the result object."""
        request = build_tab1_ai_review_request(
            audit_text=self._audit_text,
            project_root=self._project_root,
            model_name=self._model_name,
        )
        result = run_tab1_ai_review(request)
        self.result_ready.emit(result)
