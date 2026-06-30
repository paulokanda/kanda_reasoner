# project-path: kanda_reasoner_app/manage_workflows/ai_review/qt_worker.py
"""Qt worker for Tab 2 advisory AI review."""

from __future__ import annotations

from importlib import import_module
import logging

from .controller import build_tab2_ai_review_request, run_tab2_ai_review
from .models import Tab2AIReviewResult

__all__ = ["Tab2AIReviewWorker"]

_LOGGER = logging.getLogger(__name__)


def _qt_core_attr(name: str):
    """Return one PySide6.QtCore attribute at GUI import time."""
    return getattr(import_module("PySide6.QtCore"), name)


QObject = _qt_core_attr("QObject")
Signal = _qt_core_attr("Signal")


class Tab2AIReviewWorker(QObject):
    """Run advisory AI review outside the Tab 2 GUI thread."""

    result_ready = Signal(object)
    finished = Signal()

    def __init__(
        self,
        *,
        review_kind: str,
        check_output_text: str,
        project_root: str,
        model_name: str = "",
        mode_label: str = "",
    ) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        review_kind : str
            The review kind value.
        check_output_text : str
            The check output text value.
        project_root : str
            The project root path.
        model_name : str, optional
            The optional model name value.
        mode_label : str, optional
            The optional mode label value.
        """
        
        super().__init__()
        self._review_kind = str(review_kind or "check")
        self._check_output_text = str(check_output_text or "")
        self._project_root = str(project_root or "")
        self._model_name = str(model_name or "")
        self._mode_label = str(mode_label or "")

    def run(self) -> None:
        """Run the advisory review and emit the result object."""
        try:
            request = build_tab2_ai_review_request(
                review_kind=self._review_kind,
                check_output_text=self._check_output_text,
                project_root=self._project_root,
                model_name=self._model_name,
                mode_label=self._mode_label,
            )
            result = run_tab2_ai_review(request)
        except Exception as exc:
            _LOGGER.exception("Tab 2 AI review worker failed")
            result = Tab2AIReviewResult(
                success=False,
                text="",
                model_name=self._model_name,
                error_message="Tab 2 AI review worker failed: " + str(exc),
            )
        self.result_ready.emit(result)
        self.finished.emit()
