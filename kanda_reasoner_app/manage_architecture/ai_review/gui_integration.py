"""GUI integration for Tab 1 advisory AI review."""

from __future__ import annotations

from importlib import import_module
from typing import Any

from .adapter import Tab1AIReviewAdapter
from .qt_worker import Tab1AIReviewWorker
from .running_indicator import install_tab1_activity_indicator

__all__ = [
    "install_tab1_ai_review_controls",
    "populate_ai_review_model_combo",
]

AUTO_MODEL_LABEL = "Auto (first available Ollama model)"
SETTINGS_ORGANIZATION = "Kanda"
SETTINGS_APPLICATION = "ProjectReasonerV10"
SETTINGS_KEY_SELECTED_MODEL = "tab1_ai_review_selected_model"


def _load_qt_symbol(module_name: str, symbol_name: str) -> Any:
    """Load one Qt symbol only when GUI controls are used."""
    module = import_module(module_name)
    return getattr(module, symbol_name)


def _qsettings_class() -> Any:
    """Return the Qt settings class through a lazy import boundary."""
    return _load_qt_symbol("PySide6.QtCore", "QSettings")


def _qthread_class() -> Any:
    """Return the Qt thread class through a lazy import boundary."""
    return _load_qt_symbol("PySide6.QtCore", "QThread")


def _combo_box_class() -> Any:
    """Return the Qt combo-box class through a lazy import boundary."""
    return _load_qt_symbol("PySide6.QtWidgets", "QComboBox")


def _label_class() -> Any:
    """Return the Qt label class through a lazy import boundary."""
    return _load_qt_symbol("PySide6.QtWidgets", "QLabel")


def _message_box_class() -> Any:
    """Return the Qt message-box class through a lazy import boundary."""
    return _load_qt_symbol("PySide6.QtWidgets", "QMessageBox")


def _push_button_class() -> Any:
    """Return the Qt push-button class through a lazy import boundary."""
    return _load_qt_symbol("PySide6.QtWidgets", "QPushButton")


def _load_saved_ai_review_model_name() -> str:
    """Load the last selected Tab 1 AI review model from user settings."""
    try:
        settings = _qsettings_class()(SETTINGS_ORGANIZATION, SETTINGS_APPLICATION)
        value = settings.value(SETTINGS_KEY_SELECTED_MODEL, "")
    except Exception:
        return ""
    return str(value or "").strip()


def _save_ai_review_model_name(model_name: str) -> None:
    """Persist the last selected Tab 1 AI review model in user settings."""
    normalized = str(model_name or "").strip()
    try:
        settings = _qsettings_class()(SETTINGS_ORGANIZATION, SETTINGS_APPLICATION)
        settings.setValue(SETTINGS_KEY_SELECTED_MODEL, normalized)
        sync = getattr(settings, "sync", None)
        if callable(sync):
            sync()
    except Exception:
        return


def _model_name_from_combo_text(text: str) -> str:
    """Normalize combo text to a stored model name."""
    selected = str(text or "").strip()
    if not selected or selected == AUTO_MODEL_LABEL:
        return ""
    return selected


def _handle_ai_review_model_changed(window: Any, text: str) -> None:
    """Persist a user-initiated Tab 1 AI model selection change."""
    model_name = _model_name_from_combo_text(text)
    window._ai_review_saved_model_name = model_name
    _save_ai_review_model_name(model_name)


def install_tab1_ai_review_controls(window: Any, buttons_layout: Any) -> None:
    """Install read-only AI review controls into the Tab 1 GUI."""
    model_label = _label_class()("AI model:")
    model_combo = _combo_box_class()()
    model_combo.setMinimumWidth(210)
    model_combo.setToolTip(
        "Select the local Ollama model used by Tab 1 AI Review."
    )
    model_combo.addItem(AUTO_MODEL_LABEL)
    saved_model_name = _load_saved_ai_review_model_name()
    window._ai_review_saved_model_name = saved_model_name
    if saved_model_name:
        model_combo.addItem(saved_model_name)
        model_combo.setCurrentIndex(model_combo.findText(saved_model_name))
    model_combo.currentTextChanged.connect(
        lambda text: _handle_ai_review_model_changed(window, text)
    )

    refresh_button = _push_button_class()("Refresh AI Models")
    refresh_button.setToolTip("Refresh Tab 1 Ollama model choices.")
    refresh_button.clicked.connect(lambda: populate_ai_review_model_combo(window))

    review_button = _push_button_class()("AI Review First Check")
    review_button.setToolTip(
        "Read-only AI review of the latest deterministic First Check output."
    )
    review_button.clicked.connect(lambda: _run_ai_review_first_check(window))

    window._ai_review_model_label = model_label
    window._ai_review_model_combo = model_combo
    window._ai_review_refresh_models_button = refresh_button
    window._ai_review_button = review_button

    buttons_layout.addWidget(model_label)
    buttons_layout.addWidget(model_combo)
    buttons_layout.addWidget(refresh_button)
    buttons_layout.addWidget(review_button)
    install_tab1_activity_indicator(window, buttons_layout)


def populate_ai_review_model_combo(
    window: Any,
    adapter: Tab1AIReviewAdapter | None = None,
) -> list[str]:
    """Refresh the Tab 1 AI model selector from the shared registry."""
    combo = getattr(window, "_ai_review_model_combo", None)
    if combo is None:
        return []

    previous = _model_name_from_combo_text(str(combo.currentText() or ""))
    saved_model_name = str(
        getattr(window, "_ai_review_saved_model_name", "")
        or _load_saved_ai_review_model_name()
    ).strip()
    desired_model_name = previous or saved_model_name
    active_adapter = adapter or Tab1AIReviewAdapter()
    try:
        models = active_adapter.list_models()
    except Exception as exc:
        models = []
        status_bar = getattr(window, "statusBar", None)
        if callable(status_bar):
            status_bar().showMessage("AI model refresh failed: " + str(exc))

    combo.blockSignals(True)
    try:
        combo.clear()
        combo.addItem(AUTO_MODEL_LABEL)
        for model_name in models:
            combo.addItem(model_name)
        if desired_model_name:
            index = combo.findText(desired_model_name)
            if index >= 0:
                combo.setCurrentIndex(index)
                window._ai_review_saved_model_name = desired_model_name
    finally:
        combo.blockSignals(False)

    status_bar = getattr(window, "statusBar", None)
    if callable(status_bar):
        status_bar().showMessage(
            "Tab 1 AI model refresh found " + str(len(models)) + " model(s)."
        )
    return models


def _selected_ai_review_model(window: Any) -> str:
    """Return the selected Tab 1 AI model, or empty string for auto."""
    combo = getattr(window, "_ai_review_model_combo", None)
    if combo is None:
        return ""
    return _model_name_from_combo_text(str(combo.currentText() or ""))


def _set_ai_review_controls_enabled(window: Any, enabled: bool) -> None:
    """Enable or disable Tab 1 AI review controls safely."""
    for attr_name in (
        "_ai_review_button",
        "_ai_review_model_combo",
        "_ai_review_refresh_models_button",
    ):
        widget = getattr(window, attr_name, None)
        if widget is not None and hasattr(widget, "setEnabled"):
            widget.setEnabled(enabled)


def _run_ai_review_first_check(window: Any) -> None:
    """Run a read-only AI review over the current First Check output."""
    if window._worker_thread is not None or window._ai_review_thread is not None:
        _message_box_class().warning(
            window,
            "Work running",
            "Wait for the current work to finish first.",
        )
        return

    audit_text = window._output.toPlainText().strip()
    if not audit_text:
        _message_box_class().information(
            window,
            "Run First Check first",
            "Run Tab 1 First Check before asking for an AI review.",
        )
        return

    project_root = window._root_path_edit.text().strip()
    model_name = _selected_ai_review_model(window)
    window._ai_review_saved_model_name = model_name
    _save_ai_review_model_name(model_name)
    display_model = model_name or AUTO_MODEL_LABEL
    window._append_text(
        "\n> advisory AI review requested for latest Tab 1 output\n"
    )
    window._append_text(
        "> selected advisory model: " + display_model + "\n"
    )
    _set_ai_review_controls_enabled(window, False)
    window._run_button.setEnabled(False)
    indicator = getattr(window, "_tab1_activity_indicator", None)
    if indicator is not None:
        indicator.start_ai_review(display_model)
    window.statusBar().showMessage("Running advisory AI review...")

    window._ai_review_thread = _qthread_class()(window)
    window._ai_review_worker = Tab1AIReviewWorker(
        audit_text=audit_text,
        project_root=project_root,
        model_name=model_name,
    )
    window._ai_review_worker.moveToThread(window._ai_review_thread)

    window._ai_review_thread.started.connect(window._ai_review_worker.run)
    window._ai_review_worker.result_ready.connect(
        lambda result: _handle_ai_review_result(window, result)
    )
    window._ai_review_worker.result_ready.connect(window._ai_review_thread.quit)
    window._ai_review_thread.finished.connect(lambda: _cleanup_ai_review_worker(window))

    window._ai_review_thread.start()


def _handle_ai_review_result(window: Any, result: object) -> None:
    """Append an advisory AI review result to the Tab 1 output panel."""
    success = bool(getattr(result, "success", False))
    text = str(getattr(result, "text", "") or "")
    error_message = str(getattr(result, "error_message", "") or "")
    model_name = str(getattr(result, "model_name", "") or "")
    indicator = getattr(window, "_tab1_activity_indicator", None)

    if success:
        window._append_text("\n" + text + "\n")
        if indicator is not None:
            indicator.finish_success("AI review finished")
        if model_name:
            window.statusBar().showMessage("AI review finished with " + model_name)
        else:
            window.statusBar().showMessage("AI review finished")
        return

    window._append_text(
        "\nADVISORY AI REVIEW UNAVAILABLE\n"
        + (error_message or "Unknown AI review error.")
        + "\n"
        + "Deterministic First Check remains available and authoritative.\n"
    )
    if indicator is not None:
        indicator.finish_error("AI review unavailable")
    window.statusBar().showMessage("AI review unavailable")
    _message_box_class().warning(
        window,
        "AI review unavailable",
        error_message or "Unknown AI review error.",
    )


def _cleanup_ai_review_worker(window: Any) -> None:
    """Release the advisory AI review worker after completion."""
    if window._ai_review_worker is not None:
        window._ai_review_worker.deleteLater()
        window._ai_review_worker = None
    if window._ai_review_thread is not None:
        window._ai_review_thread.deleteLater()
        window._ai_review_thread = None
    window._run_button.setEnabled(True)
    _set_ai_review_controls_enabled(window, True)
