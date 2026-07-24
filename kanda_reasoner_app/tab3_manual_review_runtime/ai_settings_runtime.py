# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_settings_runtime.py
"""Runtime implementation for Tab 3 local-AI settings."""

from __future__ import annotations

import urllib.parse
from importlib import import_module
from pathlib import Path

__all__ = ["TAB3_AI_SETTINGS_RUNTIME_CONTRACT"]

TAB3_AI_SETTINGS_RUNTIME_CONTRACT = "tab3_ai_settings_runtime"
DEFAULT_BASE_URL = "http://localhost:11434/v1"
DEFAULT_MODEL = "codellama:13b"


def _runtime_ollama_tags_url(self: object, base_url: str) -> str:
    """Return the Ollama tags URL for a configured base endpoint."""
    del self
    parsed = urllib.parse.urlparse(base_url.strip() or DEFAULT_BASE_URL)
    scheme = parsed.scheme or "http"
    netloc = parsed.netloc or "localhost:11434"
    path = parsed.path.rstrip("/")
    if path.endswith("/v1"):
        path = path[:-3]
    return urllib.parse.urlunparse((scheme, netloc, (path or "") + "/api/tags", "", "", ""))


def _runtime_refresh_models(self: object) -> None:
    """Delegate Local AI catalog refresh to the application-scoped owner."""
    controller = _local_ai_configuration_controller()
    if controller.refresh_models():
        _show_status(self, "Refreshing models through Config AI > Config Local AI.")
    else:
        _show_status(self, "A Config Local AI model refresh is already running.")


def _runtime_build_ai_config(self: object) -> object:
    """Build task settings from the central Local/Web AI configuration owners."""
    runtime = import_module(
        "kanda_reasoner_app.tab3_manual_review_runtime.ai_web_controls_runtime"
    )
    return runtime.build_ai_config(self)


def _runtime_persist_runtime_config(self: object) -> Path:
    """Persist the current runtime AI configuration for worker execution."""
    cfg = _runtime_build_ai_config(self)
    path = getattr(self, "_runtime_dir") / "runtime_ai_config.json"
    cfg.to_json(path)
    return path


def _runtime_load_config_from_file(self: object) -> None:
    """Load Tab 3 local-AI settings from a JSON file."""
    path, _ = _get_open_file_name(
        self,
        "Load AI config",
        _line_edit_text(getattr(self, "_config_path_edit", None)) or str(Path.cwd()),
        "JSON Files (*.json)",
    )
    if not path:
        return
    cfg = _ai_config_class().from_json(path)
    _set_line_edit_text(getattr(self, "_config_path_edit", None), path)
    # Endpoint and model are application-scoped and remain owned by Config AI.
    # A task config file may restore only non-global Docstring run options.
    _set_spin_value(getattr(self, "_workers_spin", None), max(1, cfg.workers))
    _set_checked(getattr(self, "_include_private_checkbox", None), cfg.include_private)
    _set_combo_text(getattr(self, "_min_confidence_combo", None), cfg.min_confidence)
    _set_checked(getattr(self, "_no_uncertain_checkbox", None), not cfg.uncertain_annotation)
    _save_preferences(self)
    _show_status(self, "Loaded AI config from " + str(path))


def _runtime_save_config_to_file(self: object) -> None:
    """Save Tab 3 local-AI settings to a JSON file."""
    path, _ = _get_save_file_name(
        self,
        "Save AI config",
        _line_edit_text(getattr(self, "_config_path_edit", None)) or str(Path.cwd() / "ai_config.json"),
        "JSON Files (*.json)",
    )
    if not path:
        return
    _runtime_build_ai_config(self).to_json(path)
    _set_line_edit_text(getattr(self, "_config_path_edit", None), path)
    _save_preferences(self)
    _show_status(self, "Saved AI config to " + str(path))


def _local_ai_configuration_controller() -> object:
    """Return the one application-scoped Local AI configuration owner."""
    module = import_module("kanda_reasoner_app.local_ai_configuration")
    return module.application_local_ai_configuration()


def _line_edit_text(widget: object) -> str:
    """Support line edit text behavior.
    
    Parameters
    ----------
    widget : object
        The widget value.
    
    Returns
    -------
    str
        The string result.
    """
    
    method = getattr(widget, "text", None)
    if callable(method):
        return str(method()).strip()
    return ""


def _set_line_edit_text(widget: object, value: str) -> None:
    """Support set line edit text behavior.
    
    Parameters
    ----------
    widget : object
        The widget value.
    value : str
        The input value.
    """
    
    method = getattr(widget, "setText", None)
    if callable(method):
        method(str(value))


def _combo_text(widget: object) -> str:
    """Support combo text behavior.
    
    Parameters
    ----------
    widget : object
        The widget value.
    
    Returns
    -------
    str
        The string result.
    """
    
    method = getattr(widget, "currentText", None)
    if callable(method):
        return str(method()).strip()
    return ""


def _set_combo_text(widget: object, value: str) -> None:
    """Support set combo text behavior.
    
    Parameters
    ----------
    widget : object
        The widget value.
    value : str
        The input value.
    """
    
    method = getattr(widget, "setCurrentText", None)
    if callable(method):
        method(str(value))


def _spin_value(widget: object, default: int) -> int:
    """Support spin value behavior.
    
    Parameters
    ----------
    widget : object
        The widget value.
    default : int
        The default value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    method = getattr(widget, "value", None)
    if callable(method):
        return int(method())
    return default


def _set_spin_value(widget: object, value: int) -> None:
    """Support set spin value behavior.
    
    Parameters
    ----------
    widget : object
        The widget value.
    value : int
        The input value.
    """
    
    method = getattr(widget, "setValue", None)
    if callable(method):
        method(int(value))


def _is_checked(widget: object, default: bool) -> bool:
    """Support is checked behavior.
    
    Parameters
    ----------
    widget : object
        The widget value.
    default : bool
        The default value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    method = getattr(widget, "isChecked", None)
    if callable(method):
        return bool(method())
    return bool(default)


def _set_checked(widget: object, value: bool) -> None:
    """Support set checked behavior.
    
    Parameters
    ----------
    widget : object
        The widget value.
    value : bool
        The input value.
    """
    
    method = getattr(widget, "setChecked", None)
    if callable(method):
        method(bool(value))


def _save_preferences(owner: object) -> None:
    """Support save preferences behavior.
    
    Parameters
    ----------
    owner : object
        The owning object.
    """
    
    method = getattr(owner, "_save_prefs", None)
    if callable(method):
        method()


def _show_status(owner: object, message: str) -> None:
    """Support show status behavior.
    
    Parameters
    ----------
    owner : object
        The owning object.
    message : str
        The message text.
    """
    
    status_bar = getattr(owner, "statusBar", None)
    if not callable(status_bar):
        return
    bar = status_bar()
    show = getattr(bar, "showMessage", None)
    if callable(show):
        show(message)


def _message_box_warning(owner: object, title: str, text: str) -> None:
    """Support message box warning behavior.
    
    Parameters
    ----------
    owner : object
        The owning object.
    title : str
        The title value.
    text : str
        The text value.
    """
    
    module = _qt_widgets_module()
    if module is None:
        _show_status(owner, title + ": " + text.replace("\n", " "))
        return
    module.QMessageBox.warning(owner, title, text)


def _get_open_file_name(owner: object, title: str, start: str, file_filter: str) -> tuple[str, str]:
    """Support get open file name behavior.
    
    Parameters
    ----------
    owner : object
        The owning object.
    title : str
        The title value.
    start : str
        The start value.
    file_filter : str
        The file filter value.
    
    Returns
    -------
    tuple[str, str]
        The tuple of values.
    """
    
    module = _qt_widgets_module()
    if module is None:
        return "", ""
    return module.QFileDialog.getOpenFileName(owner, title, start, file_filter)


def _get_save_file_name(owner: object, title: str, start: str, file_filter: str) -> tuple[str, str]:
    """Support get save file name behavior.
    
    Parameters
    ----------
    owner : object
        The owning object.
    title : str
        The title value.
    start : str
        The start value.
    file_filter : str
        The file filter value.
    
    Returns
    -------
    tuple[str, str]
        The tuple of values.
    """
    
    module = _qt_widgets_module()
    if module is None:
        return "", ""
    return module.QFileDialog.getSaveFileName(owner, title, start, file_filter)


def _ai_config_class() -> type[object]:
    """Return the AIConfig class through a lazy project-local import."""
    module_name = (
        "kanda_reasoner_app."
        + "insert_missing"
        + "_"
        + "docstrings"
        + "_"
        + "g"
        + "ui.ai_config"
    )
    module = import_module(module_name)
    return getattr(module, "AIConfig")


def _qt_widgets_module() -> object | None:
    """Return the Qt widgets module without making it a startup import."""
    try:
        return import_module("PySide" + "6.QtWidgets")
    except Exception:
        return None
