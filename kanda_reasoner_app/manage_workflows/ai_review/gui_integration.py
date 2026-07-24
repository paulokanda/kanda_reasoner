# project-path: kanda_reasoner_app/manage_workflows/ai_review/gui_integration.py
"""GUI integration for Tab 2 advisory AI review."""

from __future__ import annotations

from importlib import import_module
from typing import Any

from PySide6.QtCore import QObject, QThread, Slot
from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QPushButton

from kanda_reasoner_app.local_ai_configuration import (
    application_local_ai_configuration,
)
from kanda_reasoner_app.local_ai_runtime_state import (
    runtime_local_ai_configuration_snapshot,
)

from ._gui_row_adapter import _QWidgetLikeRow


__all__ = [
    "AUTO_MODEL_LABEL",
    "create_tab2_ai_review_window_class",
    "populate_tab2_ai_review_model_combo",
]

AUTO_MODEL_LABEL = "Global Local AI model"


def _ai_review_module(name: str) -> Any:
    """Load one Tab 2 AI review helper module lazily."""
    return import_module(__package__ + "." + name)


def _new_model_adapter() -> Any:
    """Create the shared local-model adapter lazily."""
    return _ai_review_module("adapter").Tab2AIReviewAdapter()


def _worker_class() -> type[Any]:
    """Return the worker class lazily to keep this GUI adapter decoupled."""
    return _ai_review_module("qt_worker").Tab2AIReviewWorker


def _install_activity_indicator(window: Any, row_layout: Any) -> Any:
    """Install the activity indicator through a lazy helper boundary."""
    return _ai_review_module("running_indicator").install_tab2_activity_indicator(
        window, row_layout
    )


def _local_ai_controller() -> Any:
    """Return the application-scoped Local AI configuration owner."""
    return application_local_ai_configuration()


def populate_tab2_ai_review_model_combo(
    window: Any,
    adapter: Any | None = None,
) -> list[str]:
    """Return the global Local AI catalog without creating a local selector."""
    del adapter
    controller = _local_ai_controller()
    snapshot = controller.snapshot()
    status_bar = getattr(window, "statusBar", None)
    if callable(status_bar):
        status_bar().showMessage("Local AI configuration: " + controller.summary())
    return list(snapshot.available_models)


def _set_ai_review_controls_enabled(window: Any, enabled: bool) -> None:
    """Enable or disable the two advisory review actions safely."""
    for attr_name in (
        "_tab2_ai_review_check_button",
        "_tab2_ai_review_correction_button",
    ):
        widget = getattr(window, attr_name, None)
        if widget is not None and hasattr(widget, "setEnabled"):
            widget.setEnabled(enabled)


def _install_tab2_ai_review_controls(window: Any) -> None:
    """Install read-only AI review controls into the Tab 2 GUI."""
    central = window.centralWidget()
    layout = central.layout() if central is not None else None
    if layout is None:
        return

    row_widget = getattr(window, "_tab2_ai_review_row_widget", None)
    if row_widget is not None:
        return

    row_layout = QHBoxLayout()
    row_layout.setContentsMargins(0, 0, 0, 0)

    review_check_button = QPushButton("AI Review First Check")
    review_check_button.setToolTip(
        "Read-only AI review of the latest deterministic Tab 2 Check output."
    )
    review_check_button.clicked.connect(lambda: _run_tab2_ai_review(window, "check"))

    review_correction_button = QPushButton("AI Review Correction Plan")
    review_correction_button.setToolTip(
        "Read-only AI correction planning. This does not run Correct or write files."
    )
    review_correction_button.clicked.connect(
        lambda: _run_tab2_ai_review(window, "correction_plan")
    )

    window._tab2_ai_review_model_label = None
    window._tab2_ai_review_model_combo = None
    window._tab2_ai_review_refresh_models_button = None
    window._tab2_ai_review_check_button = review_check_button
    window._tab2_ai_review_correction_button = review_correction_button
    window._tab2_ai_review_thread = None
    window._tab2_ai_review_worker = None
    window._tab2_ai_review_result_receiver = None
    window._tab2_ai_review_controls_moved_to_host = False
    row_layout.addWidget(review_check_button)
    row_layout.addWidget(review_correction_button)
    row_layout.addStretch()
    _install_activity_indicator(window, row_layout)

    row_container = _QWidgetLikeRow(row_layout)
    window._tab2_ai_review_row_widget = row_container
    insert_index = min(2, layout.count()) if hasattr(layout, "count") else 0
    if hasattr(layout, "insertWidget"):
        layout.insertWidget(insert_index, row_container)
    else:
        layout.addWidget(row_container)

    def move_ai_review_controls_to_layout(
        destination_layout: Any,
        insert_index: int | None = None,
    ) -> None:
        """Move Tab 2 AI review controls into the host header template."""
        if getattr(window, "_tab2_ai_review_controls_moved_to_host", False):
            return
        widgets = [
            review_check_button,
            review_correction_button,
        ]
        target_index = (
            destination_layout.count()
            if insert_index is None
            else insert_index
        )
        offset = 0
        for widget in widgets:
            parent = widget.parentWidget()
            parent_layout = parent.layout() if parent is not None else None
            if parent_layout is not None:
                parent_layout.removeWidget(widget)
            widget.setParent(None)
            destination_layout.insertWidget(target_index + offset, widget, 0)
            offset += 1
        row_container.hide()
        window._tab2_ai_review_controls_moved_to_host = True

    window.move_ai_review_controls_to_layout = move_ai_review_controls_to_layout


class _Tab2AIReviewResultReceiver(QObject):
    """GUI-thread receiver for results emitted by the AI worker thread."""

    def __init__(self, window: Any) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        window : Any
            The window value.
        """
        
        super().__init__(window)
        self._window = window

    @Slot(object)
    def handle_result(self, result: object) -> None:
        """Handle a worker result on the GUI thread."""
        window = self._window
        if window is None:
            return
        _handle_tab2_ai_review_result(window, result)


def _run_tab2_ai_review(window: Any, review_kind: str) -> None:
    """Run a read-only AI review over the current Tab 2 output panel."""
    if window._worker_thread is not None or window._tab2_ai_review_thread is not None:
        QMessageBox.warning(
            window,
            "Work running",
            "Wait for the current work to finish first.",
        )
        return

    output_text = window._output.toPlainText().strip()
    if not output_text:
        QMessageBox.information(
            window,
            "Run Tab 2 Check first",
            "Run Tab 2 Check before asking for an AI review.",
        )
        return

    project_root = window._root_combo.currentText().strip()
    mode_label = window._mode_combo.currentText().strip()
    controller = _local_ai_controller()
    snapshot = controller.snapshot()
    model_name = snapshot.model_id
    if not snapshot.ready_for_chat:
        controller.request_open_configuration()
        QMessageBox.information(
            window,
            "Configure Local AI",
            "Open Config AI > Config Local AI and select a model first.",
        )
        return
    window._tab2_ai_review_configuration_revision = snapshot.revision
    display_model = model_name
    if review_kind == "correction_plan":
        request_label = "advisory AI correction plan requested"
        activity_label = "correction plan: " + display_model
    else:
        request_label = "advisory AI review requested"
        activity_label = "check review: " + display_model

    window._append_text("\n> " + request_label + " for latest Tab 2 output\n")
    window._append_text("> selected advisory model: " + display_model + "\n")
    _set_ai_review_controls_enabled(window, False)
    window._operation_cancel_requested = False
    if hasattr(window, "_set_operation_buttons_running"):
        window._set_operation_buttons_running(True)
    else:
        window._run_button.setEnabled(False)
    indicator = getattr(window, "_tab2_activity_indicator", None)
    if indicator is not None:
        indicator.start_ai_review(activity_label)
    window.statusBar().showMessage("Running Tab 2 advisory AI review...")

    thread = QThread(window)
    worker_type = _worker_class()
    worker = worker_type(
        review_kind=review_kind,
        check_output_text=output_text,
        project_root=project_root,
        model_name=model_name,
        mode_label=mode_label,
    )
    receiver = _Tab2AIReviewResultReceiver(window)

    window._tab2_ai_review_thread = thread
    window._tab2_ai_review_worker = worker
    window._tab2_ai_review_result_receiver = receiver

    worker.moveToThread(thread)
    thread.started.connect(worker.run)
    worker.result_ready.connect(receiver.handle_result)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(lambda: _cleanup_tab2_ai_review_worker(window))

    thread.start()


def _handle_tab2_ai_review_result(window: Any, result: object) -> None:
    """Append an advisory AI review result to the Tab 2 output panel."""
    success = bool(getattr(result, "success", False))
    text = str(getattr(result, "text", "") or "")
    error_message = str(getattr(result, "error_message", "") or "")
    model_name = str(getattr(result, "model_name", "") or "")
    indicator = getattr(window, "_tab2_activity_indicator", None)

    if getattr(window, "_operation_cancel_requested", False):
        window._append_text("\n[canceled] advisory Tab 2 AI review late result ignored\n")
        window.statusBar().showMessage("Tab 2 AI review canceled")
        return

    runtime_snapshot = runtime_local_ai_configuration_snapshot()
    expected_revision = str(
        getattr(window, "_tab2_ai_review_configuration_revision", "") or ""
    )
    if (
        runtime_snapshot is not None
        and expected_revision
        and runtime_snapshot.revision != expected_revision
    ):
        window._append_text(
            "\n[stale] Local AI configuration changed; late review ignored.\n"
        )
        window.statusBar().showMessage("Tab 2 AI review became stale")
        return

    if success:
        window._append_text("\n" + text + "\n")
        if indicator is not None:
            indicator.finish_success("AI review finished")
        if model_name:
            window.statusBar().showMessage("Tab 2 AI review finished with " + model_name)
        else:
            window.statusBar().showMessage("Tab 2 AI review finished")
        return

    window._append_text(
        "\nADVISORY TAB 2 AI REVIEW UNAVAILABLE\n"
        + (error_message or "Unknown AI review error.")
        + "\n"
        + "Deterministic Tab 2 Check/Correct remain available and authoritative.\n"
    )
    if indicator is not None:
        indicator.finish_error("AI review unavailable")
    window.statusBar().showMessage("Tab 2 AI review unavailable")
    QMessageBox.warning(
        window,
        "AI review unavailable",
        error_message or "Unknown AI review error.",
    )


def _cleanup_tab2_ai_review_worker(window: Any) -> None:
    """Release advisory AI review Qt objects after completion."""
    receiver = getattr(window, "_tab2_ai_review_result_receiver", None)
    if receiver is not None:
        receiver.deleteLater()
        window._tab2_ai_review_result_receiver = None

    thread = getattr(window, "_tab2_ai_review_thread", None)
    if thread is not None:
        thread.deleteLater()
        window._tab2_ai_review_thread = None

    window._tab2_ai_review_worker = None
    window._tab2_ai_review_configuration_revision = ""
    if hasattr(window, "_set_operation_buttons_running"):
        window._set_operation_buttons_running(False)
    else:
        window._run_button.setEnabled(True)
    _set_ai_review_controls_enabled(window, True)


def _deterministic_label(mode: str) -> str:
    """Return the user-facing deterministic work label."""
    normalized = str(mode or "").strip().lower()
    if normalized == "write":
        return "Correct"
    if normalized in {"validate", "scan", "diff"}:
        return "Check"
    return normalized or "work"


def create_tab2_ai_review_window_class(base_class: type[Any]) -> type[Any]:
    """Return an enhanced Tab 2 window class with advisory AI controls."""

    class Tab2AIReviewWorkflowManagerWindow(base_class):  # type: ignore[misc]
        """Workflow manager window with read-only Tab 2 AI review controls."""

        def _build_ui(self) -> None:  # type: ignore[override]
            """Support build ui behavior.
            """
            
            super()._build_ui()
            _install_tab2_ai_review_controls(self)

        def run_mode(self, mode: str) -> None:  # type: ignore[override]
            """Run the mode.
            
            Parameters
            ----------
            mode : str
                The selected mode.
            """
            
            super().run_mode(mode)
            if self._worker_thread is None:
                return
            indicator = getattr(self, "_tab2_activity_indicator", None)
            if indicator is not None:
                indicator.start_deterministic(_deterministic_label(mode))

        def _handle_worker_success(self, mode: str) -> None:  # type: ignore[override]
            """Support handle worker success behavior.
            
            Parameters
            ----------
            mode : str
                The selected mode.
            """
            
            if getattr(self, "_operation_cancel_requested", False):
                super()._handle_worker_success(mode)
                return
            indicator = getattr(self, "_tab2_activity_indicator", None)
            if indicator is not None:
                indicator.finish_success(_deterministic_label(mode) + " finished")
            super()._handle_worker_success(mode)

        def _handle_worker_error(self, mode: str, details: str) -> None:  # type: ignore[override]
            """Support handle worker error behavior.
            
            Parameters
            ----------
            mode : str
                The selected mode.
            details : str
                The details value.
            """
            
            if getattr(self, "_operation_cancel_requested", False):
                super()._handle_worker_error(mode, details)
                return
            indicator = getattr(self, "_tab2_activity_indicator", None)
            if indicator is not None:
                indicator.finish_error(_deterministic_label(mode) + " needs review")
            super()._handle_worker_error(mode, details)

    Tab2AIReviewWorkflowManagerWindow.__name__ = base_class.__name__
    Tab2AIReviewWorkflowManagerWindow.__qualname__ = base_class.__qualname__
    Tab2AIReviewWorkflowManagerWindow.__module__ = base_class.__module__
    return Tab2AIReviewWorkflowManagerWindow
