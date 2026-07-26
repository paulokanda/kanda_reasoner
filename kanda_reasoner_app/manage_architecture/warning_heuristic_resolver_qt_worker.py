# project-path: kanda_reasoner_app/manage_architecture/warning_heuristic_resolver_qt_worker.py
"""Qt worker for non-blocking warning resolver analysis routes."""

from __future__ import annotations

from pathlib import Path
import subprocess
from threading import Event
from typing import Iterable

from PySide6.QtCore import QObject, Signal, Slot

from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
    WarningFinding,
)
from kanda_reasoner_app.manage_architecture.warning_model_live_audit import (
    apply_and_verify_model_plan,
    run_fresh_test_protection_audit,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_resolver import (
    build_model_test_protection_plan,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    build_test_protection_gap_plan,
)

__all__ = ["WarningHeuristicResolverWorker"]

_ROUTE_HEURISTIC = "heuristic"
_ROUTE_MODEL = "model"
_ROUTE_MODEL_APPLY_VERIFY = "model_apply_verify"


class _WarningResolverCancelled(Exception):
    """Internal cooperative cancellation boundary."""


class WarningHeuristicResolverWorker(QObject):
    """Build one deterministic or model-assisted plan outside the GUI thread."""

    progress = Signal(int, int, int, int, str, str)
    result_ready = Signal(object)
    failed = Signal(str)
    finished = Signal()

    def __init__(
        self,
        *,
        project_root: str | Path,
        findings: Iterable[WarningFinding],
        route: str = _ROUTE_HEURISTIC,
        model_selection: str = "",
        apply_plan: object | None = None,
    ) -> None:
        super().__init__()
        self._project_root = Path(project_root).expanduser().resolve()
        self._findings = tuple(findings)
        self._route = str(route or _ROUTE_HEURISTIC).strip().lower()
        self._model_selection = str(model_selection or "").strip()
        self._apply_plan = apply_plan
        self._cancel_event = Event()

    def request_cancel(self) -> None:
        """Request thread-safe cooperative cancellation from the GUI thread."""
        self._cancel_event.set()

    @Slot()
    def run(self) -> None:
        """Build one route plan and emit terminal evidence without touching widgets."""
        total = len(self._findings)
        try:
            self._raise_if_cancelled()
            self.progress.emit(total, total, 0, 0, "", "starting")
            if self._route == _ROUTE_MODEL:
                self._emit_progress(
                    total, total, 0, 0, "Architecture Review", "fresh_audit"
                )
                fresh = run_fresh_test_protection_audit(
                    self._project_root,
                    runner=self._cancellable_runner,
                )
                self._raise_if_cancelled()
                plan = build_model_test_protection_plan(
                    self._project_root,
                    fresh.findings,
                    model_selection=self._model_selection,
                    progress_callback=self._emit_progress,
                )
            elif self._route == _ROUTE_MODEL_APPLY_VERIFY:
                if self._apply_plan is None:
                    raise RuntimeError(
                        "Missing confirmed Local AI plan for apply verification."
                    )
                plan = apply_and_verify_model_plan(
                    self._apply_plan,
                    progress_callback=self._emit_progress,
                )
            elif self._route == _ROUTE_HEURISTIC:
                plan = build_test_protection_gap_plan(
                    self._project_root,
                    self._findings,
                    progress_callback=self._emit_progress,
                )
            else:
                raise ValueError("Unknown warning resolver route: " + self._route)
            self._raise_if_cancelled()
        except _WarningResolverCancelled:
            pass
        except Exception as exc:  # Qt boundary converts failure to signal evidence.
            self.failed.emit(type(exc).__name__ + ": " + str(exc))
        else:
            self.result_ready.emit(plan)
        finally:
            self.finished.emit()

    def _raise_if_cancelled(self) -> None:
        if self._cancel_event.is_set():
            raise _WarningResolverCancelled()

    def _emit_progress(
        self,
        total: int,
        to_go: int,
        done: int,
        web_ai: int,
        source_path: str,
        action: str,
    ) -> None:
        self._raise_if_cancelled()
        self.progress.emit(total, to_go, done, web_ai, source_path, action)
        self._raise_if_cancelled()

    def _cancellable_runner(
        self,
        command: object,
        **kwargs: object,
    ) -> subprocess.CompletedProcess[str]:
        """Run the fresh audit subprocess with cancellation and timeout checks."""
        capture_output = bool(kwargs.pop("capture_output", False))
        check = bool(kwargs.pop("check", False))
        timeout = kwargs.pop("timeout", None)
        if capture_output:
            if "stdout" in kwargs or "stderr" in kwargs:
                raise ValueError("capture_output conflicts with stdout or stderr")
            kwargs["stdout"] = subprocess.PIPE
            kwargs["stderr"] = subprocess.PIPE
        process = subprocess.Popen(command, **kwargs)
        elapsed = 0.0
        interval = 0.1
        while True:
            try:
                stdout, stderr = process.communicate(timeout=interval)
                break
            except subprocess.TimeoutExpired:
                elapsed += interval
                if self._cancel_event.is_set():
                    self._stop_process(process)
                    raise _WarningResolverCancelled()
                if timeout is not None and elapsed >= float(timeout):
                    self._stop_process(process)
                    raise subprocess.TimeoutExpired(command, timeout)
        completed = subprocess.CompletedProcess(
            args=command,
            returncode=process.returncode,
            stdout=stdout,
            stderr=stderr,
        )
        if check:
            completed.check_returncode()
        return completed

    @staticmethod
    def _stop_process(process: subprocess.Popen[object]) -> None:
        """Stop and reap one cancellable child process."""
        if process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2.0)
