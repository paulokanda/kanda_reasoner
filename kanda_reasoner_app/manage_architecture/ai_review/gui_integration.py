# project-path: kanda_reasoner_app/manage_architecture/ai_review/gui_integration.py
"""GUI integration for Audit Project heuristic, Local AI, and Web AI review."""

from __future__ import annotations

import uuid
from importlib import import_module
from typing import Any

from kanda_reasoner_app.local_ai_configuration import (
    LocalAIConfigurationController,
    application_local_ai_configuration,
)
from kanda_reasoner_app.web_ai_configuration import (
    WebAIConfigurationController,
    application_web_ai_configuration,
)

from .adapter import Tab1AIReviewAdapter
from .contracts import (
    AuditReviewIdentity,
    audit_snapshot_hash,
    build_audit_review_identity,
    current_project_identity,
)
from .models import HEURISTIC_MODE, LOCAL_AI_MODE, WEB_AI_MODE
from .qt_worker import Tab1AIReviewWorker
from .running_indicator import install_tab1_activity_indicator

__all__ = [
    "install_tab1_ai_review_controls",
    "populate_ai_review_model_combo",
]


def _qt_symbol(module_name: str, symbol_name: str) -> Any:
    return getattr(import_module(module_name), symbol_name)


def _qthread_class() -> Any:
    return _qt_symbol("PySide6.QtCore", "QThread")


def _widgets() -> Any:
    return import_module("PySide6.QtWidgets")


def _controller(window: Any) -> WebAIConfigurationController:
    controller = getattr(window, "_audit_web_ai_configuration", None)
    if not isinstance(controller, WebAIConfigurationController):
        controller = application_web_ai_configuration()
        window._audit_web_ai_configuration = controller
    return controller


def _local_controller(window: Any) -> LocalAIConfigurationController:
    controller = getattr(window, "_audit_local_ai_configuration", None)
    if not isinstance(controller, LocalAIConfigurationController):
        controller = application_local_ai_configuration()
        window._audit_local_ai_configuration = controller
    return controller


def _qt_object_is_alive(value: Any) -> bool:
    if value is None:
        return False
    try:
        is_valid = getattr(import_module("shiboken6"), "isValid")
        return bool(is_valid(value))
    except (ImportError, AttributeError):
        try:
            value.objectName()
        except RuntimeError:
            return False
        except Exception:
            return True
        return True


def _radio_is_checked(window: Any, attribute: str) -> bool:
    radio = getattr(window, attribute, None)
    if not _qt_object_is_alive(radio):
        return False
    try:
        return bool(radio.isChecked())
    except RuntimeError:
        return False


def _selected_mode(window: Any) -> str:
    if _radio_is_checked(window, "_ai_review_web_radio"):
        return WEB_AI_MODE
    if _radio_is_checked(window, "_ai_review_local_radio"):
        return LOCAL_AI_MODE
    return HEURISTIC_MODE


def _disconnect_configuration_sync(window: Any, generation: int | None = None) -> None:
    if generation is not None and generation != int(
        getattr(window, "_ai_review_controls_generation", -1)
    ):
        return
    bindings = tuple(
        getattr(window, "_ai_review_configuration_sync_bindings", ()) or ()
    )
    window._ai_review_configuration_sync_bindings = ()
    for signal, callback in bindings:
        try:
            signal.disconnect(callback)
        except (RuntimeError, TypeError):
            pass


def _connect_configuration_sync(window: Any, mode_host: Any) -> None:
    _disconnect_configuration_sync(window)
    generation = int(getattr(window, "_ai_review_controls_generation", 0)) + 1
    window._ai_review_controls_generation = generation

    def sync_callback(_value: object = None) -> None:
        if generation != int(getattr(window, "_ai_review_controls_generation", -1)):
            return
        _sync_review_controls(window)

    signals = (
        _controller(window).configuration_changed,
        _controller(window).catalog_changed,
        _local_controller(window).configuration_changed,
        _local_controller(window).catalog_changed,
    )
    bindings = tuple((signal, sync_callback) for signal in signals)
    for signal, callback in bindings:
        signal.connect(callback)
    window._ai_review_configuration_sync_bindings = bindings
    mode_host.destroyed.connect(
        lambda *_args: _disconnect_configuration_sync(window, generation)
    )


def _mode_label(mode: str) -> str:
    return {
        HEURISTIC_MODE: "Heuristic",
        LOCAL_AI_MODE: "Local AI",
        WEB_AI_MODE: "Web AI",
    }.get(mode, "Heuristic")


def _sync_review_controls(window: Any) -> None:
    button = getattr(window, "_ai_review_button", None)
    if not _qt_object_is_alive(button):
        return
    running = getattr(window, "_ai_review_thread", None) is not None
    mode = _selected_mode(window)
    try:
        button.setText("Review with " + _mode_label(mode))
        button.setEnabled(not running)
        if mode == WEB_AI_MODE:
            button.setToolTip(
                "Read-only advisory synthesis using Config Web AI. Current: "
                + _controller(window).summary()
            )
        elif mode == LOCAL_AI_MODE:
            button.setToolTip(
                "Read-only advisory synthesis using Config AI > Config Local AI. Current: "
                + _local_controller(window).summary()
            )
        else:
            button.setToolTip(
                "Build a deterministic advisory summary without sending a model request."
            )
    except RuntimeError:
        return


def install_tab1_ai_review_controls(window: Any, buttons_layout: Any) -> None:
    """Install only workflow mode choices and one advisory review action."""
    qt = _widgets()
    mode_label = qt.QLabel("Review Engine:")
    mode_host = qt.QWidget(window)
    mode_layout = qt.QHBoxLayout(mode_host)
    mode_layout.setContentsMargins(0, 0, 0, 0)
    mode_layout.setSpacing(5)
    group = qt.QButtonGroup(window)
    heuristic = qt.QRadioButton("Heuristic", mode_host)
    local = qt.QRadioButton("Local AI", mode_host)
    web = qt.QRadioButton("Web AI", mode_host)
    heuristic.setObjectName("audit_review_mode_heuristic")
    local.setObjectName("audit_review_mode_local_ai")
    web.setObjectName("audit_review_mode_web_ai")
    for radio in (heuristic, local, web):
        group.addButton(radio)
        mode_layout.addWidget(radio)
        radio.toggled.connect(lambda _checked=False, owner=window: _sync_review_controls(owner))
    heuristic.setChecked(True)

    review_button = qt.QPushButton("Review with Heuristic")
    review_button.setObjectName("audit_project_review_current_results_button")
    review_button.clicked.connect(lambda: _run_review(window))

    window._audit_web_ai_configuration = application_web_ai_configuration()
    window._audit_local_ai_configuration = application_local_ai_configuration()
    window._ai_review_mode_group = group
    window._ai_review_heuristic_radio = heuristic
    window._ai_review_local_radio = local
    window._ai_review_web_radio = web
    window._ai_review_mode_host = mode_host
    window._ai_review_model_label = mode_label
    window._ai_review_model_combo = mode_host
    window._ai_review_refresh_models_button = None
    window._ai_review_button = review_button
    window._ai_review_generation = 0
    window._ai_review_identity = None
    window._ai_review_source_snapshot = ""
    window._ai_review_terminal_result_seen = False

    buttons_layout.addWidget(mode_label)
    buttons_layout.addWidget(mode_host)
    buttons_layout.addWidget(review_button)
    install_tab1_activity_indicator(window, buttons_layout)

    _connect_configuration_sync(window, mode_host)
    _sync_review_controls(window)


def populate_ai_review_model_combo(
    window: Any,
    adapter: Tab1AIReviewAdapter | None = None,
) -> list[str]:
    """Compatibility helper: return Local AI models without creating a selector."""
    del window
    try:
        return (adapter or Tab1AIReviewAdapter()).list_models()
    except Exception:
        return []


def _set_controls_enabled(window: Any, enabled: bool) -> None:
    for name in (
        "_ai_review_heuristic_radio",
        "_ai_review_local_radio",
        "_ai_review_web_radio",
        "_ai_review_button",
    ):
        widget = getattr(window, name, None)
        if not _qt_object_is_alive(widget):
            continue
        try:
            widget.setEnabled(enabled)
        except RuntimeError:
            continue


def _request_web_approval(window: Any, audit_text: str) -> str:
    qt = _widgets()
    controller = _controller(window)
    snapshot = controller.snapshot()
    model = controller.selected_model()
    if model is None or not controller.ready_for_chat():
        qt.QMessageBox.warning(
            window,
            "Web AI not configured",
            "Open Config Web AI, refresh models, and select a usable model first.",
        )
        controller.request_open_configuration()
        return ""
    if not snapshot.structured_output_supported:
        qt.QMessageBox.warning(
            window,
            "Web AI model unsupported",
            "Audit Project Web AI requires a model that advertises strict response_format support.",
        )
        controller.request_open_configuration()
        return ""
    try:
        project = current_project_identity(window)
    except Exception as exc:
        qt.QMessageBox.warning(window, "Project identity unavailable", str(exc))
        return ""
    details = (
        "Approve one read-only Audit Project Web AI review?\n\n"
        f"Project: {project.active_project_slug}\n"
        f"Project root: {project.active_project_root}\n"
        f"Project Support: {project.active_project_support_root}\n"
        f"Gateway: {snapshot.gateway_id}\n"
        f"Model: {snapshot.model_id}\n"
        f"Payload bytes: {len(audit_text.encode('utf-8'))}\n"
        f"Audit SHA-256: {audit_snapshot_hash(audit_text)}\n"
        f"Privacy: {snapshot.privacy_summary}\n\n"
        "The result is advisory and read-only. It cannot change audit pass/fail, write source, or Freeze."
    )
    decision = qt.QMessageBox.question(
        window,
        "Approve Audit Project Web AI Review",
        details,
        qt.QMessageBox.StandardButton.Yes | qt.QMessageBox.StandardButton.No,
        qt.QMessageBox.StandardButton.No,
    )
    return uuid.uuid4().hex if decision == qt.QMessageBox.StandardButton.Yes else ""


def _identity_is_current(window: Any, identity: AuditReviewIdentity) -> bool:
    if bool(getattr(window, "_operation_cancel_requested", False)):
        return False
    if identity.generation != int(getattr(window, "_ai_review_generation", -1)):
        return False
    if _selected_mode(window) != identity.provider_mode:
        return False
    current_text = window._output.toPlainText().strip()
    if audit_snapshot_hash(current_text) != identity.audit_snapshot_hash:
        return False
    try:
        project = current_project_identity(window)
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
    if identity.provider_mode == LOCAL_AI_MODE:
        snapshot = _local_controller(window).snapshot()
        return (
            snapshot.revision == identity.configuration_revision
            and snapshot.model_id == identity.model_id
        )
    if identity.provider_mode == WEB_AI_MODE:
        snapshot = _controller(window).snapshot()
        return (
            bool(identity.privacy_approval_id)
            and snapshot.revision == identity.configuration_revision
            and snapshot.gateway_id == identity.gateway_id
            and snapshot.model_id == identity.model_id
        )
    return True


def _run_review(window: Any) -> None:
    qt = _widgets()
    if window._worker_thread is not None or window._ai_review_thread is not None:
        qt.QMessageBox.warning(window, "Work running", "Wait for current work to finish first.")
        return
    audit_text = window._output.toPlainText().strip()
    if not audit_text:
        qt.QMessageBox.information(
            window,
            "Run Project Audit first",
            "Run deterministic Project Audit before requesting an advisory review.",
        )
        return
    mode = _selected_mode(window)
    approval_id = ""
    if mode == LOCAL_AI_MODE:
        local_controller = _local_controller(window)
        if not local_controller.ready_for_chat():
            qt.QMessageBox.warning(
                window,
                "Local AI not configured",
                "Open Config AI > Config Local AI and select a model first.",
            )
            local_controller.request_open_configuration()
            return
    elif mode == WEB_AI_MODE:
        approval_id = _request_web_approval(window, audit_text)
        if not approval_id:
            return
    window._ai_review_generation = int(window._ai_review_generation) + 1
    try:
        identity, project = build_audit_review_identity(
            window,
            generation=window._ai_review_generation,
            audit_text=audit_text,
            provider_mode=mode,
            approval_id=approval_id,
        )
    except Exception as exc:
        qt.QMessageBox.warning(window, "Project identity unavailable", str(exc))
        return

    controller = _controller(window)
    model_name = ""
    gateway_id = ""
    api_key = ""
    display = _mode_label(mode)
    if mode == LOCAL_AI_MODE:
        model_name = _local_controller(window).selected_model_id()
        display += " | " + model_name
    elif mode == WEB_AI_MODE:
        model_name = controller.selected_model_id()
        gateway_id = controller.gateway_id()
        api_key = controller.api_key()
        display += " | " + model_name

    window._ai_review_identity = identity
    window._ai_review_source_snapshot = audit_text
    window._ai_review_terminal_result_seen = False
    window._operation_cancel_requested = False
    _set_controls_enabled(window, False)
    if hasattr(window, "_set_operation_buttons_running"):
        window._set_operation_buttons_running(True)
    else:
        window._run_button.setEnabled(False)
    indicator = getattr(window, "_tab1_activity_indicator", None)
    if indicator is not None:
        indicator.start_ai_review(display)
    window.statusBar().showMessage("Running read-only " + display + " audit review...")

    thread = _qthread_class()(window)
    worker = Tab1AIReviewWorker(
        audit_text,
        str(project.active_project_root),
        model_name,
        provider_mode=mode,
        gateway_id=gateway_id,
        api_key=api_key,
        request_id=identity.request_id,
    )
    worker.moveToThread(thread)
    window._ai_review_thread = thread
    window._ai_review_worker = worker
    thread.started.connect(worker.run)
    worker.result_ready.connect(lambda result: _handle_result(window, result))
    worker.result_ready.connect(thread.quit)
    thread.finished.connect(lambda: _cleanup(window))
    thread.start()


def _restore_terminal_controls(window: Any) -> None:
    if hasattr(window, "_set_operation_buttons_running"):
        window._set_operation_buttons_running(False)
    else:
        window._run_button.setEnabled(True)
    _set_controls_enabled(window, True)
    _sync_review_controls(window)


def _handle_result(window: Any, result: object) -> None:
    window._ai_review_terminal_result_seen = True
    identity = getattr(window, "_ai_review_identity", None)
    _restore_terminal_controls(window)
    if not isinstance(identity, AuditReviewIdentity) or not _identity_is_current(window, identity):
        _widgets().QMessageBox.warning(
            window,
            "Audit review discarded",
            "The Project, audit text, review mode, or central AI configuration changed. "
            "The stale advisory result was discarded.",
        )
        window.statusBar().showMessage("Stale audit review discarded")
        return
    if str(getattr(result, "request_id", "")) != identity.request_id:
        window.statusBar().showMessage("Mismatched audit review discarded")
        return
    success = bool(getattr(result, "success", False))
    indicator = getattr(window, "_tab1_activity_indicator", None)
    if success:
        window._append_text("\n" + str(getattr(result, "text", "") or "") + "\n")
        if indicator is not None:
            indicator.finish_success("advisory review finished")
        window.statusBar().showMessage("Read-only audit review finished")
        return
    error = str(getattr(result, "error_message", "") or "Unknown review error.")
    window._append_text(
        "\nADVISORY AUDIT REVIEW UNAVAILABLE\n"
        + error
        + "\nDeterministic Project Audit remains available and authoritative.\n"
    )
    if indicator is not None:
        indicator.finish_error("advisory review unavailable")
    window.statusBar().showMessage("Audit review unavailable")
    _widgets().QMessageBox.warning(window, "Audit review unavailable", error)


def _cleanup(window: Any) -> None:
    if not bool(getattr(window, "_ai_review_terminal_result_seen", False)):
        _restore_terminal_controls(window)
    worker = getattr(window, "_ai_review_worker", None)
    thread = getattr(window, "_ai_review_thread", None)
    if worker is not None:
        worker.deleteLater()
    if thread is not None:
        thread.deleteLater()
    window._ai_review_worker = None
    window._ai_review_thread = None
    window._ai_review_identity = None
    window._ai_review_source_snapshot = ""
    _sync_review_controls(window)
