# project-path: kanda_reasoner_app/error_memory_gui/_ai_correction_action.py
"""Qt-facing action bridge for Error Memory correction modes."""

from __future__ import annotations

import traceback
import uuid
import weakref
from typing import Any

from PySide6.QtCore import QObject, QThread, Slot
from PySide6.QtWidgets import QMessageBox, QWidget

from kanda_reasoner_app.error_memory_gui import _ai_mode_runtime
from kanda_reasoner_app.error_memory_gui._ai_correction_contracts import (
    ErrorMemoryCorrectionIdentity,
    build_correction_identity,
    current_project_identity,
    input_snapshot_hash,
    payload_size_bytes,
)
from kanda_reasoner_app.error_memory_gui._ai_correction_worker import (
    ErrorMemoryAICorrectionWorker,
)
from kanda_reasoner_app.error_memory_gui._correction_guard import (
    apply_heuristic_correction_to_error_editor,
)
from kanda_reasoner_app.error_memory_gui._window_sync import (
    apply_corrected_lesson_to_work_windows,
)

__all__ = [
    "run_error_memory_ai_correction_from_header",
    "run_error_memory_ai_correction_from_tab",
]

_ACTIVE_JOBS: dict[int, dict[str, Any]] = {}


def _selected_model_text(lazy_tab: Any) -> str:
    """Return the selected legacy local model when a header combo exists."""
    header = getattr(lazy_tab, "tab_header_template", None)
    combo = getattr(header, "ai_model_combo", None)
    if combo is None:
        return ""
    return str(combo.currentText() or "").strip()


def _current_intake_text(tab: Any) -> tuple[str, str]:
    """Return intake text and editor text for correction."""
    raw_edit = getattr(tab, "raw_error_edit", None)
    editor = getattr(tab, "received_preview_edit", None)
    raw_text = raw_edit.toPlainText().strip() if raw_edit is not None else ""
    editor_text = editor.toPlainText().strip() if editor is not None else ""
    return raw_text, editor_text


def _show_copyable_error(
    parent: QWidget,
    *,
    title: str,
    message: str,
    detail_text: str = "",
) -> None:
    """Show a copy-and-close floating error message window."""
    from kanda_reasoner_app.templates.floating_windows import (
        show_error_copy_close_window,
    )

    show_error_copy_close_window(
        parent,
        title=title,
        message=message,
        detail_text=detail_text,
        button_text="Copy and Close",
    )


def _show_standard_warning(parent: QWidget, title: str, message: str) -> None:
    """Show a normal warning when there is no debug payload to copy."""
    QMessageBox.warning(parent, title, message)


def _show_success(tab: Any, title: str, message: str) -> None:
    """Use the tab's normal success notification."""
    show_action_done = getattr(tab, "_show_action_done", None)
    if callable(show_action_done):
        show_action_done(title, message, "")
        return
    QMessageBox.information(tab, title, message)


def _lazy_tab_for_embedded_tab(tab: Any) -> Any:
    """Return the lazy tab host for an embedded Error Memory tab when available."""
    parent_getter = getattr(tab, "parent", None)
    parent = parent_getter() if callable(parent_getter) else None
    while parent is not None:
        if hasattr(parent, "tab_header_template"):
            return parent
        next_parent_getter = getattr(parent, "parent", None)
        parent = next_parent_getter() if callable(next_parent_getter) else None
    return None


def _set_running_state(tab: Any, running: bool) -> None:
    """Project the background correction lifecycle onto the mode controls."""
    _ai_mode_runtime.set_running_state(tab, running)


def _restore_terminal_button_state(tab: Any, job: dict[str, Any]) -> None:
    """Restore the standby button as soon as one terminal worker signal arrives."""
    if bool(job.get("terminal_ui_ready", False)):
        return
    job["terminal_ui_ready"] = True
    _set_running_state(tab, False)
    thread = job.get("thread")
    if isinstance(thread, QThread) and thread.isRunning():
        thread.quit()


def _job_for(tab: Any) -> dict[str, Any] | None:
    """Return the active correction job for one Error Memory tab."""
    job = _ACTIVE_JOBS.get(id(tab))
    return job if isinstance(job, dict) else None


def _same_source_text(tab: Any, job: dict[str, Any]) -> bool:
    """Return whether the work windows still match the submitted snapshot."""
    intake_text, editor_text = _current_intake_text(tab)
    return (
        intake_text == str(job.get("intake_text", ""))
        and editor_text == str(job.get("editor_text", ""))
    )


def _identity_is_current(tab: Any, job: dict[str, Any]) -> bool:
    """Reject results after Project, mode, input, or central config changes."""
    identity = job.get("identity")
    if not isinstance(identity, ErrorMemoryCorrectionIdentity):
        return _same_source_text(tab, job)
    intake_text, editor_text = _current_intake_text(tab)
    if input_snapshot_hash(intake_text, editor_text) != identity.input_snapshot_hash:
        return False
    try:
        project = current_project_identity(tab)
    except Exception:
        return False
    if (
        project.active_project_id != identity.active_project_id
        or project.active_project_root_fingerprint
        != identity.active_project_root_fingerprint
        or str(project.active_project_support_root)
        != identity.active_project_support_root
    ):
        return False
    if _ai_mode_runtime.selected_mode(tab) != identity.assistant_mode:
        return False
    if identity.assistant_mode == _ai_mode_runtime.WEB_AI_MODE:
        snapshot = _ai_mode_runtime.central_configuration(tab).snapshot()
        return (
            snapshot.revision == identity.configuration_revision
            and snapshot.gateway_id == identity.gateway_id
            and snapshot.model_id == identity.model_id
        )
    if identity.assistant_mode == _ai_mode_runtime.LOCAL_AI_MODE:
        snapshot = _ai_mode_runtime.local_configuration(tab).snapshot()
        return (
            snapshot.revision == identity.configuration_revision
            and snapshot.model_id == identity.model_id
        )
    return True


def _request_web_approval(
    parent: QWidget,
    tab: Any,
    *,
    intake_text: str,
    editor_text: str,
) -> str:
    """Request explicit approval for one exact Project/model/input snapshot."""
    controller = _ai_mode_runtime.central_configuration(tab)
    snapshot = controller.snapshot()
    model = controller.selected_model()
    if model is None or not controller.ready_for_chat():
        _show_standard_warning(
            parent,
            "Web AI not configured",
            "Open Config Web AI, refresh models, and select a usable model first.",
        )
        controller.request_open_configuration()
        return ""
    if not snapshot.structured_output_supported:
        _show_standard_warning(
            parent,
            "Web AI model unsupported",
            "Error Memory Web AI requires a model that advertises strict "
            "response_format support.",
        )
        controller.request_open_configuration()
        return ""
    try:
        project = current_project_identity(tab)
    except Exception as exc:
        _show_standard_warning(parent, "Project identity unavailable", str(exc))
        return ""
    fingerprint = input_snapshot_hash(intake_text, editor_text)
    details = (
        "Approve one Error Memory Web AI correction request?\n\n"
        f"Project: {project.active_project_slug}\n"
        f"Project root: {project.active_project_root}\n"
        f"Project Support: {project.active_project_support_root}\n"
        f"Gateway: {snapshot.gateway_id}\n"
        f"Model: {snapshot.model_id}\n"
        f"Payload bytes: {payload_size_bytes(intake_text, editor_text)}\n"
        f"Input SHA-256: {fingerprint}\n"
        f"Privacy: {snapshot.privacy_summary}\n\n"
        "The result is preview-only. It will not save, activate, supersede, "
        "delete, or memorize any lesson."
    )
    decision = QMessageBox.question(
        parent,
        "Approve Error Memory Web AI Request",
        details,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return uuid.uuid4().hex if decision == QMessageBox.StandardButton.Yes else ""


class _AICorrectionReceiver(QObject):
    """Receive worker results on the GUI thread and enforce preview-only apply."""

    def __init__(self, *, tab: Any, parent: QWidget, generation: int) -> None:
        super().__init__()
        self._tab_ref = weakref.ref(tab)
        self._parent_ref = weakref.ref(parent)
        self._job_key = id(tab)
        self._generation = int(generation)
        self._terminal_result_seen = False

    def _tab_and_job(self) -> tuple[Any | None, dict[str, Any] | None]:
        tab = self._tab_ref()
        if tab is None:
            return None, None
        job = _ACTIVE_JOBS.get(self._job_key)
        if not job or int(job.get("generation", -1)) != self._generation:
            return tab, None
        return tab, job

    @Slot(object)
    def on_result(self, result: object) -> None:
        """Apply one accepted result only when its request identity is current."""
        self._terminal_result_seen = True
        tab, job = self._tab_and_job()
        if tab is None or job is None:
            return
        parent = self._parent_ref() or tab
        _restore_terminal_button_state(tab, job)
        try:
            if not _identity_is_current(tab, job):
                _show_standard_warning(
                    parent,
                    "Error Memory AI correction discarded",
                    "The Project, source text, correction mode, or "
                    "central AI configuration changed while the request was "
                    "running. The stale AI result was discarded. No lesson was saved "
                    "or deleted.",
                )
                return
            lesson_block = getattr(result, "lesson_block", None)
            if not bool(getattr(result, "ok", False)) or lesson_block is None:
                _show_copyable_error(
                    parent,
                    title="Error Memory AI correction failed",
                    message=str(getattr(result, "message", "AI correction failed.")),
                    detail_text=str(getattr(result, "raw_response", "")),
                )
                return
            apply_corrected_lesson_to_work_windows(tab, lesson_block)
            message = str(getattr(result, "message", "AI correction completed."))
            message += (
                "\n\nThe corrected lesson was loaded as a preview only. "
                "Correct with AI did not save, delete, activate, supersede, or memorize any lesson. "
                "Review the result and use an explicit "
                "save/status action when appropriate."
            )
            _show_success(tab, "Error Memory AI correction", message)
        except Exception as exc:
            _show_copyable_error(
                parent,
                title="Error Memory AI correction apply failed",
                message="The background result could not be loaded into the preview: "
                + str(exc),
                detail_text=traceback.format_exc(),
            )

    @Slot(str, str)
    def on_failure(self, message: str, detail_text: str) -> None:
        """Show an unexpected worker exception without leaking it from a Qt slot."""
        self._terminal_result_seen = True
        tab, job = self._tab_and_job()
        if tab is None or job is None:
            return
        parent = self._parent_ref() or tab
        _restore_terminal_button_state(tab, job)
        _show_copyable_error(
            parent,
            title="Error Memory AI correction failed",
            message=str(message or "Unexpected AI correction failure."),
            detail_text=str(detail_text or ""),
        )

    @Slot()
    def on_thread_finished(self) -> None:
        """Release one finished job and restore the GUI action state."""
        tab = self._tab_ref()
        job = _ACTIVE_JOBS.get(self._job_key)
        if job and int(job.get("generation", -1)) == self._generation:
            _ACTIVE_JOBS.pop(self._job_key, None)
            if tab is not None:
                _set_running_state(tab, False)
                if not self._terminal_result_seen:
                    parent = self._parent_ref() or tab
                    _show_copyable_error(
                        parent,
                        title="Error Memory AI correction failed",
                        message="The background correction worker finished without a result.",
                    )
        self.deleteLater()


def _start_error_memory_ai_correction(
    *,
    parent: QWidget,
    tab: Any,
    model_text: str,
    local_model_getter: Any = None,
) -> None:
    """Start one preview-only Error Memory correction in a Qt worker thread."""
    mode = _ai_mode_runtime.selected_mode(tab)
    if mode == _ai_mode_runtime.HEURISTIC_MODE:
        apply_heuristic_correction_to_error_editor(tab)
        _ai_mode_runtime.sync_mode_controls(tab)
        return

    intake_text, editor_text = _current_intake_text(tab)
    if not (intake_text or editor_text):
        _show_standard_warning(
            parent,
            "Error Memory AI correction",
            "Paste or load an Error Memory draft before running AI correction.",
        )
        return
    if _job_for(tab) is not None:
        _show_standard_warning(
            parent,
            "Error Memory AI correction",
            "An AI correction is already running for this Error Memory tab. "
            "A local AI correction is already running when Local AI mode is selected.",
        )
        return

    approval_id = ""
    if mode == _ai_mode_runtime.LOCAL_AI_MODE:
        local_controller = _ai_mode_runtime.local_configuration(tab)
        if not local_controller.ready_for_chat():
            _show_standard_warning(
                parent,
                "Local AI not configured",
                "Open Config AI > Config Local AI and select a model first.",
            )
            local_controller.request_open_configuration()
            return
        model_text = local_controller.selected_model_id()
    elif mode == _ai_mode_runtime.WEB_AI_MODE:
        approval_id = _request_web_approval(
            parent,
            tab,
            intake_text=intake_text,
            editor_text=editor_text,
        )
        if not approval_id:
            return

    generation = int(getattr(tab, "_error_memory_ai_correction_generation", 0) or 0) + 1
    tab._error_memory_ai_correction_generation = generation
    try:
        identity, project = build_correction_identity(
            tab,
            generation=generation,
            intake_text=intake_text,
            editor_text=editor_text,
            approval_id=approval_id,
            local_model_id=model_text,
        )
    except Exception as exc:
        _show_standard_warning(parent, "Project identity unavailable", str(exc))
        return

    gateway_id = ""
    web_model_id = ""
    api_key = ""
    if mode == _ai_mode_runtime.WEB_AI_MODE:
        controller = _ai_mode_runtime.central_configuration(tab)
        gateway_id = controller.gateway_id()
        web_model_id = controller.selected_model_id()
        api_key = controller.api_key()

    thread = QThread()
    worker = ErrorMemoryAICorrectionWorker(
        intake_text=intake_text,
        editor_text=editor_text,
        project_root=project.active_project_root,
        provider_mode=mode,
        model_selection=model_text,
        gateway_id=gateway_id,
        web_model_id=web_model_id,
        api_key=api_key,
        request_id=identity.request_id,
    )
    receiver = _AICorrectionReceiver(tab=tab, parent=parent, generation=generation)
    worker.moveToThread(thread)

    _ACTIVE_JOBS[id(tab)] = {
        "generation": generation,
        "thread": thread,
        "worker": worker,
        "receiver": receiver,
        "intake_text": intake_text,
        "editor_text": editor_text,
        "identity": identity,
    }

    thread.started.connect(worker.run)
    worker.result_ready.connect(receiver.on_result)
    worker.failed.connect(receiver.on_failure)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(receiver.on_thread_finished)
    thread.finished.connect(thread.deleteLater)

    _set_running_state(tab, True)
    try:
        thread.start()
    except Exception as exc:
        _ACTIVE_JOBS.pop(id(tab), None)
        _set_running_state(tab, False)
        receiver.deleteLater()
        worker.deleteLater()
        thread.deleteLater()
        _show_copyable_error(
            parent,
            title="Error Memory AI correction failed to start",
            message=str(exc),
            detail_text=traceback.format_exc(),
        )


def run_error_memory_ai_correction_from_header(lazy_tab: QWidget) -> None:
    """Run the selected correction mode for the embedded Error Memory tab."""
    ensure_loaded = getattr(lazy_tab, "ensure_loaded", None)
    if callable(ensure_loaded) and not bool(ensure_loaded()):
        return
    tab: Any = getattr(lazy_tab, "_embedded_widget", None)
    if tab is None:
        _show_standard_warning(
            lazy_tab,
            "Error Memory AI correction",
            "Error Memory is not loaded.",
        )
        return
    _start_error_memory_ai_correction(
        parent=lazy_tab,
        tab=tab,
        model_text=_selected_model_text(lazy_tab),
        local_model_getter=lambda: _selected_model_text(lazy_tab),
    )


def run_error_memory_ai_correction_from_tab(tab: QWidget) -> None:
    """Run the selected correction mode from the Error Memory action button."""
    lazy_tab = _lazy_tab_for_embedded_tab(tab)
    parent = lazy_tab if lazy_tab is not None else tab
    model_text = _selected_model_text(lazy_tab) if lazy_tab is not None else ""
    getter = (lambda: _selected_model_text(lazy_tab)) if lazy_tab is not None else None
    _start_error_memory_ai_correction(
        parent=parent,
        tab=tab,
        model_text=model_text,
        local_model_getter=getter,
    )
