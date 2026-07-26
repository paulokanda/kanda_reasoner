# project-path: kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_qt_controller.py
"""Qt lifecycle controller for non-blocking warning resolver routes."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PySide6.QtCore import QObject, QThread, Signal, Slot

from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
    WarningFinding,
)
from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_qt_worker import (
    WarningHeuristicResolverWorker,
)

__all__ = ["WarningHeuristicResolverController"]

_ROUTE_HEURISTIC = "heuristic"
_ROUTE_MODEL = "model"
_ROUTE_MODEL_APPLY_VERIFY = "model_apply_verify"
_CANCELLABLE_ROUTES = {_ROUTE_HEURISTIC, _ROUTE_MODEL}


class WarningHeuristicResolverController(QObject):
    """Own one warning resolver worker generation while keeping the GUI responsive."""

    progress = Signal(int, int, int, int, str, str)
    result_ready = Signal(object)
    failed = Signal(str)
    model_progress = Signal(int, int, int, int, str, str)
    model_result_ready = Signal(object)
    model_failed = Signal(str)
    model_apply_progress = Signal(int, int, int, int, str, str)
    model_apply_result_ready = Signal(object)
    model_apply_failed = Signal(str)
    state_changed = Signal(bool, bool, bool)
    cancelled = Signal()
    settled = Signal()

    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)
        self._thread: QThread | None = None
        self._worker: WarningHeuristicResolverWorker | None = None
        self._running = False
        self._cancel_requested = False
        self._active_route = _ROUTE_HEURISTIC
        self._pending_apply_plan: object | None = None

    @property
    def running(self) -> bool:
        """Return whether one resolver generation is active."""
        return self._running

    @property
    def cancel_requested(self) -> bool:
        """Return whether the active generation has a pending cancel request."""
        return self._cancel_requested

    @property
    def cancellable(self) -> bool:
        """Return whether the active route can be cancelled safely."""
        return self._running and self._active_route in _CANCELLABLE_ROUTES

    def start(
        self,
        project_root: str | Path,
        findings: Iterable[WarningFinding],
        *,
        route: str = _ROUTE_HEURISTIC,
        model_selection: str = "",
        apply_plan: object | None = None,
    ) -> bool:
        """Start one resolver route and reject overlapping ownership."""
        if self._running:
            return False
        normalized_route = str(route or _ROUTE_HEURISTIC).strip().lower()
        allowed_routes = {
            _ROUTE_HEURISTIC,
            _ROUTE_MODEL,
            _ROUTE_MODEL_APPLY_VERIFY,
        }
        if normalized_route not in allowed_routes:
            raise ValueError("Unknown warning resolver route: " + normalized_route)
        thread = QThread(self)
        worker = WarningHeuristicResolverWorker(
            project_root=project_root,
            findings=tuple(findings),
            route=normalized_route,
            model_selection=model_selection,
            apply_plan=apply_plan,
        )
        worker.moveToThread(thread)
        self._thread = thread
        self._worker = worker
        self._active_route = normalized_route
        self._cancel_requested = False
        self._running = True
        thread.started.connect(worker.run)
        worker.progress.connect(self._on_progress)
        worker.result_ready.connect(self._on_result)
        worker.failed.connect(self._on_failure)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(self._on_thread_finished)
        self.state_changed.emit(True, False, self.cancellable)
        thread.start()
        return True

    def cancel(self) -> bool:
        """Request cooperative cancellation and revoke late result authority."""
        if not self.cancellable or self._cancel_requested:
            return False
        self._cancel_requested = True
        self._pending_apply_plan = None
        worker = self._worker
        if worker is not None:
            worker.request_cancel()
        thread = self._thread
        if thread is not None:
            thread.requestInterruption()
        self.state_changed.emit(True, True, True)
        return True

    @Slot(int, int, int, int, str, str)
    def _on_progress(
        self,
        total: int,
        to_go: int,
        done: int,
        web_ai: int,
        source_path: str,
        action: str,
    ) -> None:
        if self._cancel_requested:
            return
        if self._active_route == _ROUTE_MODEL_APPLY_VERIFY:
            target = self.model_apply_progress
        elif self._active_route == _ROUTE_MODEL:
            target = self.model_progress
        else:
            target = self.progress
        target.emit(total, to_go, done, web_ai, source_path, action)

    @Slot(object)
    def _on_result(self, plan: object) -> None:
        if self._cancel_requested:
            return
        if self._active_route == _ROUTE_MODEL_APPLY_VERIFY:
            target = self.model_apply_result_ready
        elif self._active_route == _ROUTE_MODEL:
            target = self.model_result_ready
        else:
            target = self.result_ready
        target.emit(plan)

    @Slot(str)
    def _on_failure(self, diagnostic: str) -> None:
        if self._cancel_requested:
            return
        if self._active_route == _ROUTE_MODEL_APPLY_VERIFY:
            target = self.model_apply_failed
        elif self._active_route == _ROUTE_MODEL:
            target = self.model_failed
        else:
            target = self.failed
        target.emit(str(diagnostic))

    def queue_model_apply_verify(self, plan: object) -> bool:
        """Queue confirmed apply verification on the shared resolver lifecycle."""
        if self._pending_apply_plan is not None or self._cancel_requested:
            return False
        self._pending_apply_plan = plan
        if not self._running:
            self._start_pending_apply_verify()
        return True

    def _start_pending_apply_verify(self) -> None:
        plan = self._pending_apply_plan
        if plan is None or self._running:
            return
        self._pending_apply_plan = None
        self.start(
            getattr(plan, "project_root", ""),
            (),
            route=_ROUTE_MODEL_APPLY_VERIFY,
            apply_plan=plan,
        )

    @Slot()
    def _on_thread_finished(self) -> None:
        thread = self._thread
        was_cancelled = self._cancel_requested
        self._thread = None
        self._worker = None
        self._running = False
        self._cancel_requested = False
        self._active_route = _ROUTE_HEURISTIC
        if thread is not None:
            thread.deleteLater()
        self.state_changed.emit(False, False, False)
        if was_cancelled:
            self.cancelled.emit()
        self.settled.emit()
        if not was_cancelled:
            self._start_pending_apply_verify()
