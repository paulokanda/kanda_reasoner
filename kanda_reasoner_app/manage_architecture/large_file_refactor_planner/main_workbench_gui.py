# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/main_workbench_gui.py
"""Planner Plan & Actions controls for automatic Main Workbench orchestration."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from .main_workbench_pipeline import (
    MAIN_WORKBENCH_FAILED,
    MAIN_WORKBENCH_READY,
    MAIN_WORKBENCH_STALE,
    MAIN_WORKBENCH_WEB_AI_BLOCKED,
    MainWorkbenchController,
    MainWorkbenchControllerState,
)
from .main_workbench_state_store import (
    load_main_workbench_terminal_seal,
    terminal_seal_is_current,
)
from .main_workbench_web_ai_package import (
    MainWorkbenchWebAIPackageResult,
    build_or_reuse_main_workbench_web_ai_package,
    capture_main_workbench_web_ai_package_request,
)
from .main_workbench_stage_worker import (
    MainWorkbenchStageJob,
    launch_main_workbench_stage_job,
)
from .main_workbench_sonar import (
    finish_main_workbench_package_sonar,
    start_main_workbench_package_sonar,
    sync_main_workbench_sonar,
    update_main_workbench_package_sonar,
)
from .planner_version_state import get_selected_planner_version_bundle

__all__ = ["sync_main_workbench_controls"]

_MAIN_WORKBENCH_SUCCESS_STYLE = "color: #008000; font-weight: bold;"
_MAIN_WORKBENCH_BLOCKED_STYLE = "color: #C62828; font-weight: bold;"


class MainWorkbenchPackageController(QObject):
    """Build one complete package off the GUI thread and quarantine stale results."""

    def __init__(self, *, window: object) -> None:
        super().__init__()
        self._window = window
        self._generation = 0
        self._cancel_requested = False
        self._seal = None
        self._job: MainWorkbenchStageJob | None = None

    def running(self) -> bool:
        """Return whether package assembly still owns a worker thread."""
        return bool(self._job is not None and self._job.running())

    def cancel_requested(self) -> bool:
        """Return whether the current package result must be quarantined."""
        return self._cancel_requested

    def start(self, seal: object) -> bool:
        """Capture GUI evidence and launch package I/O outside the GUI thread."""
        if self.running():
            return False
        request = capture_main_workbench_web_ai_package_request(
            window=self._window,
            active_project_root=_root_text(self._window),
            terminal_seal=seal,
        )
        self._generation += 1
        self._cancel_requested = False
        self._seal = seal
        self._job = launch_main_workbench_stage_job(
            generation=self._generation,
            stage="WEB_AI_PACKAGE",
            request=request,
            execute=build_or_reuse_main_workbench_web_ai_package,
            settled_callback=self._settled,
        )
        _on_package_status(self._window, "RUNNING", None)
        return True

    def cancel(self) -> bool:
        """Quarantine the eventual result and request cooperative interruption."""
        if not self.running() or self._cancel_requested:
            return False
        self._cancel_requested = True
        if self._job is not None:
            self._job.request_cancel()
        _on_package_status(self._window, "CANCEL_REQUESTED", None)
        return True

    @Slot(int, str)
    def _settled(self, generation: int, stage: str) -> None:
        job = self._job
        if (
            job is None
            or generation != self._generation
            or job.generation != generation
            or job.stage != stage
        ):
            return
        self._job = None
        if self._cancel_requested:
            _on_package_status(self._window, "CANCELLED", None)
            return
        if job.failure_text:
            _on_package_status(self._window, "FAILED", job.failure_text)
            return
        if not job.result_received:
            _on_package_status(
                self._window,
                "FAILED",
                "Package worker settled without a result.",
            )
            return
        if not terminal_seal_is_current(self._window, self._seal):
            _on_package_status(self._window, "STALE", None)
            return
        _on_package_status(self._window, "READY", job.result)


def build_main_workbench_controls(window: object) -> QGroupBox:
    """Build the two-button normal workflow after Planning Summary controls."""
    box = QGroupBox("6. Main Workbench and Complete Web AI Handoff")
    layout = QVBoxLayout(box)
    description = QLabel(
        "Main Workbench automatically runs the existing read-only assurance stages. "
        "It never applies canonical Project source. Send Complete Project to Web AI "
        "becomes available only after one fresh package-ready terminal seal."
    )
    description.setWordWrap(True)
    layout.addWidget(description)

    row = QHBoxLayout()
    main_button = QPushButton("Main Workbench")
    main_button.setObjectName("largeFilePlannerMainWorkbenchButton")
    main_button.setEnabled(False)
    cancel_button = QPushButton("Cancel Main Workbench")
    cancel_button.setObjectName("largeFilePlannerCancelMainWorkbenchButton")
    cancel_button.setEnabled(False)
    send_button = QPushButton("Send Complete Project to Web AI")
    send_button.setObjectName("largeFilePlannerSendCompleteProjectWebAiButton")
    send_button.setEnabled(False)
    send_button.setStyleSheet("color: #FF8C00; font-weight: bold;")
    row.addWidget(main_button)
    row.addWidget(cancel_button)
    row.addWidget(send_button)
    row.addStretch(1)
    layout.addLayout(row)

    status = QLabel("Main Workbench: IDLE")
    status.setWordWrap(True)
    output = QPlainTextEdit()
    output.setReadOnly(True)
    output.setPlainText(
        "Generate a split plan first. Main Workbench will then run Plan Intake, "
        "Dependency Readiness, Real Preview, Structural Validation, and Advanced "
        "Quality Review in sequence."
    )
    layout.addWidget(status)
    layout.addWidget(output)

    window._large_file_refactor_main_workbench_button = main_button
    window._large_file_refactor_main_workbench_cancel_button = cancel_button
    window._large_file_refactor_main_workbench_send_button = send_button
    window._large_file_refactor_main_workbench_status_label = status
    window._large_file_refactor_main_workbench_output = output
    window._large_file_refactor_main_workbench_controller = None
    window._large_file_refactor_main_workbench_package_controller = None
    window._large_file_refactor_main_workbench_package_result = None

    main_button.clicked.connect(lambda: _start_main_workbench(window))
    cancel_button.clicked.connect(lambda: _cancel_main_workbench(window))
    send_button.clicked.connect(lambda: _send_complete_project(window))
    sync_main_workbench_controls(window)
    return box


def sync_main_workbench_controls(window: object) -> None:
    """Project Planner, controller, and terminal-seal state onto the two buttons."""
    main_button = getattr(window, "_large_file_refactor_main_workbench_button", None)
    cancel_button = getattr(window, "_large_file_refactor_main_workbench_cancel_button", None)
    send_button = getattr(window, "_large_file_refactor_main_workbench_send_button", None)
    if main_button is None or cancel_button is None or send_button is None:
        return
    controller = getattr(window, "_large_file_refactor_main_workbench_controller", None)
    state = controller.state() if controller is not None else None
    pipeline_running = bool(state and state.running)
    package_controller = getattr(
        window,
        "_large_file_refactor_main_workbench_package_controller",
        None,
    )
    package_running = bool(
        package_controller is not None and package_controller.running()
    )
    running = pipeline_running or package_running
    selected = get_selected_planner_version_bundle(window)
    plan_exists = bool(selected is not None and getattr(selected, "plan", None) is not None)
    split_running = bool(
        getattr(window, "_large_file_refactor_split_plan_running", False)
    )
    ai_running = bool(
        getattr(window, "_large_file_refactor_ai_review_running", False)
    )
    transaction_open = _workbench_transaction_open(window)
    main_button.setEnabled(
        bool(plan_exists and not running and not split_running and not ai_running and not transaction_open)
    )
    cancel_requested = bool(state.cancel_requested if pipeline_running and state else False)
    if package_running and package_controller is not None:
        cancel_requested = package_controller.cancel_requested()
    cancel_button.setEnabled(running and not cancel_requested)
    seal = _current_seal(window)
    seal_current = bool(seal and terminal_seal_is_current(window, seal))
    send_ready = bool(
        seal
        and seal.terminal_status in {MAIN_WORKBENCH_READY, MAIN_WORKBENCH_WEB_AI_BLOCKED}
        and seal_current
        and not running
        and not transaction_open
    )
    send_button.setEnabled(send_ready)
    _sync_main_workbench_button_style(
        main_button,
        state=state,
        seal=seal,
        seal_current=seal_current,
    )
    _render_state(window, state, seal_current=send_ready)


def _start_main_workbench(window: object) -> None:
    controller = _controller(window)
    if not controller.start():
        _set_output(window, "Main Workbench is already running.")
        return
    sync_main_workbench_controls(window)


def _cancel_main_workbench(window: object) -> None:
    controller = getattr(window, "_large_file_refactor_main_workbench_controller", None)
    if controller is not None and controller.state().running:
        controller.cancel()
        sync_main_workbench_controls(window)
        return
    package_controller = getattr(
        window,
        "_large_file_refactor_main_workbench_package_controller",
        None,
    )
    if package_controller is not None:
        package_controller.cancel()
    sync_main_workbench_controls(window)


def _send_complete_project(window: object) -> None:
    try:
        seal = _current_seal(window)
        if seal is None or not terminal_seal_is_current(window, seal):
            raise ValueError(
                "Main Workbench evidence is stale. Run Main Workbench again."
            )
        package_controller = _package_controller(window)
        if not package_controller.start(seal):
            raise RuntimeError("Web AI package assembly is already running.")
    except Exception as error:
        _set_output(
            window,
            "SEND COMPLETE PROJECT TO WEB AI BLOCKED\n\n"
            + type(error).__name__
            + ":"
            + str(error),
        )
    sync_main_workbench_controls(window)


def _package_controller(window: object) -> MainWorkbenchPackageController:
    controller = getattr(
        window,
        "_large_file_refactor_main_workbench_package_controller",
        None,
    )
    if controller is None:
        controller = MainWorkbenchPackageController(window=window)
        window._large_file_refactor_main_workbench_package_controller = controller
    return controller


def _on_package_status(window: object, status: str, payload: object | None) -> None:
    if status == "RUNNING":
        start_main_workbench_package_sonar(window)
        _set_output(
            window,
            "WEB AI PACKAGE\n\nCollecting bounded Project context and building "
            "the verified EXCH package outside the GUI thread.",
        )
    elif status == "CANCEL_REQUESTED":
        update_main_workbench_package_sonar(window, status)
        _set_output(window, "Web AI package cancellation requested.")
    elif status == "CANCELLED":
        finish_main_workbench_package_sonar(
            window,
            status,
            "Web AI package result was cancelled and not adopted.",
        )
        _set_output(window, "Web AI package result was cancelled and not adopted.")
    elif status == "STALE":
        finish_main_workbench_package_sonar(
            window,
            status,
            "The active card or source changed while the package was being built.",
        )
        _set_output(
            window,
            "WEB AI PACKAGE STALE\n\nThe active card or source changed while the "
            "package was being built. Run Main Workbench again.",
        )
    elif status == "FAILED":
        finish_main_workbench_package_sonar(
            window,
            status,
            str(payload or "Package construction failed."),
        )
        _set_output(window, "WEB AI PACKAGE FAILED\n\n" + str(payload or ""))
    elif status == "READY" and isinstance(
        payload,
        MainWorkbenchWebAIPackageResult,
    ):
        window._large_file_refactor_main_workbench_package_result = payload
        finish_main_workbench_package_sonar(
            window,
            status,
            "Exchange " + str(payload.exchange_id) + " is verified and ready.",
        )
        prompt_text = Path(payload.prompt_path).read_text(encoding="utf-8-sig")
        clipboard_text = "\n".join(
            [
                "KANDA COMPLETE REFACTOR PACKAGE READY",
                "",
                "ZIP:",
                payload.zip_path,
                "",
                "Upload the ZIP, then use the complete instruction below:",
                "",
                prompt_text,
            ]
        )
        QApplication.clipboard().setText(clipboard_text)
        _set_output(window, _format_package_result(payload))
    sync_main_workbench_controls(window)


def _controller(window: object) -> MainWorkbenchController:
    controller = getattr(window, "_large_file_refactor_main_workbench_controller", None)
    if controller is not None:
        return controller
    controller = MainWorkbenchController(
        window=window,
        root_callback=_root_text,
        status_callback=lambda state: _on_controller_state(window, state),
    )
    window._large_file_refactor_main_workbench_controller = controller
    return controller


def _on_controller_state(
    window: object,
    state: MainWorkbenchControllerState,
) -> None:
    sync_main_workbench_sonar(window, state)
    _set_output(
        window,
        "\n".join(
            [
                "MAIN WORKBENCH",
                "generation: " + str(state.generation),
                "stage: " + state.stage,
                "terminal_status: " + (state.terminal_status or "<running>"),
                "",
                state.message,
                "",
                "blockers:",
                *(["- " + item for item in state.blockers] or ["- none"]),
            ]
        ),
    )
    sync_main_workbench_controls(window)


def _sync_main_workbench_button_style(
    button: QPushButton,
    *,
    state: MainWorkbenchControllerState | None,
    seal: object | None,
    seal_current: bool,
) -> None:
    """Project terminal pipeline acceptance onto the Main Workbench button."""
    if state is not None and state.running:
        button.setStyleSheet("")
        return
    terminal = str(
        (state.terminal_status if state is not None else "")
        or getattr(seal, "terminal_status", "")
        or ""
    )
    if terminal == MAIN_WORKBENCH_READY and seal_current:
        button.setStyleSheet(_MAIN_WORKBENCH_SUCCESS_STYLE)
        return
    if terminal in {
        MAIN_WORKBENCH_WEB_AI_BLOCKED,
        MAIN_WORKBENCH_FAILED,
        MAIN_WORKBENCH_STALE,
    } or (seal is not None and not seal_current):
        button.setStyleSheet(_MAIN_WORKBENCH_BLOCKED_STYLE)
        return
    button.setStyleSheet("")


def _render_state(
    window: object,
    state: MainWorkbenchControllerState | None,
    *,
    seal_current: bool,
) -> None:
    label = getattr(window, "_large_file_refactor_main_workbench_status_label", None)
    if label is None:
        return
    if state is None:
        label.setText("Main Workbench: IDLE")
        return
    terminal = state.terminal_status or "RUNNING"
    freshness = " | package evidence current" if seal_current else ""
    label.setText(
        "Main Workbench: " + terminal + " | stage: " + state.stage + freshness
    )


def _current_seal(window: object):
    controller = getattr(window, "_large_file_refactor_main_workbench_controller", None)
    seal = controller.terminal_seal() if controller is not None else None
    if seal is not None:
        return seal
    try:
        return load_main_workbench_terminal_seal(_root_text(window))
    except Exception:
        return None


def _workbench_transaction_open(window: object) -> bool:
    from .workbench_snapshot_bridge import workbench_source_transaction_open

    return bool(workbench_source_transaction_open(window))


def _format_package_result(result: object) -> str:
    return "\n".join(
        [
            "COMPLETE REFACTOR PACKAGE READY",
            "",
            "exchange_id: " + str(result.exchange_id),
            "reused: " + ("YES" if result.reused else "NO"),
            "package_content_hash: " + str(result.package_content_hash),
            "candidate_set_hash: " + str(result.candidate_identity.candidate_set_hash),
            "zip_sha256: " + str(result.zip_sha256),
            "",
            "ZIP:",
            str(result.zip_path),
            "",
            "The ZIP path and self-contained Web AI instruction were copied to the clipboard.",
        ]
    )


def _set_output(window: object, text: str) -> None:
    output = getattr(window, "_large_file_refactor_main_workbench_output", None)
    if output is not None:
        output.setPlainText(str(text))


def _root_text(window: object) -> str:
    edit = getattr(window, "_root_path_edit", None)
    if edit is None:
        return str(Path.cwd())
    text = edit.text().strip()
    return text or str(Path.cwd())
