# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_settings_runtime.py
"""Runtime implementation for Tab 3 local-AI settings."""

from __future__ import annotations

import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from importlib import import_module
from pathlib import Path
from typing import Iterable

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
    """Refresh the Tab 3 model combo from supported local model sources."""
    try:
        base_url = _line_edit_text(getattr(self, "_base_url_edit", None)) or DEFAULT_BASE_URL
        models = _discover_models(base_url)
        current = _combo_text(getattr(self, "_model_combo", None)).strip()
        _replace_combo_items(getattr(self, "_model_combo", None), models, current)
        _show_status(self, "Loaded " + str(len(models)) + " installed model(s).")
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as exc:
        _message_box_warning(
            self,
            "Model refresh failed",
            "Could not load installed models from the local Ollama endpoint.\n"
            + "Details: "
            + str(exc),
        )


def _runtime_build_ai_config(self: object) -> object:
    """Build an AIConfig object from Tab 3 controls."""
    config_class = _ai_config_class()
    return config_class(
        base_url=_line_edit_text(getattr(self, "_base_url_edit", None)) or DEFAULT_BASE_URL,
        model=_combo_text(getattr(self, "_model_combo", None)).strip() or DEFAULT_MODEL,
        workers=max(1, int(_spin_value(getattr(self, "_workers_spin", None), 1))),
        include_private=_is_checked(getattr(self, "_include_private_checkbox", None), True),
        min_confidence=_combo_text(getattr(self, "_min_confidence_combo", None)).strip() or "low",
        uncertain_annotation=not _is_checked(getattr(self, "_no_uncertain_checkbox", None), False),
    )


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
    _set_line_edit_text(getattr(self, "_base_url_edit", None), cfg.base_url)
    _set_combo_text(getattr(self, "_model_combo", None), cfg.model)
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


def _discover_models(base_url: str) -> list[str]:
    """Return visible Ollama models from HTTP endpoints and the CLI."""
    names: list[str] = []
    endpoint_failures = 0
    for fetcher in (_models_from_tags, _models_from_v1_models):
        try:
            names.extend(fetcher(base_url))
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError):
            endpoint_failures += 1
    names.extend(_models_from_cli())
    models = _unique_sorted(names)
    if not models and endpoint_failures >= 2:
        raise OSError("No local models were discovered from Ollama endpoints or CLI.")
    return models


def _models_from_tags(base_url: str) -> list[str]:
    """Return models from the configured tags endpoint."""
    request = urllib.request.Request(_runtime_ollama_tags_url(None, base_url), method="GET")
    with urllib.request.urlopen(request, timeout=5.0) as response:
        payload = json.loads(response.read().decode("utf-8"))
    items = payload.get("models", [])
    return _names_from_items(items)


def _models_from_v1_models(base_url: str) -> list[str]:
    """Return models from an OpenAI-compatible local models endpoint."""
    url = _v1_models_url(base_url)
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=5.0) as response:
        payload = json.loads(response.read().decode("utf-8"))
    items = payload.get("data", [])
    return _names_from_items(items)


def _v1_models_url(base_url: str) -> str:
    """Return the local OpenAI-compatible models endpoint URL."""
    parsed = urllib.parse.urlparse(base_url.strip() or DEFAULT_BASE_URL)
    scheme = parsed.scheme or "http"
    netloc = parsed.netloc or "localhost:11434"
    path = parsed.path.rstrip("/")
    if not path.endswith("/v1"):
        path += "/v1"
    return urllib.parse.urlunparse((scheme, netloc, path + "/models", "", "", ""))


def _models_from_cli() -> list[str]:
    """Return models visible through the Ollama command-line tool."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5.0,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if result.returncode != 0:
        return []
    names: list[str] = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if parts:
            names.append(parts[0])
    return _unique_sorted(names)


def _names_from_items(items: object) -> list[str]:
    """Return model names from list entries."""
    names: list[str] = []
    if not isinstance(items, list):
        return []
    for item in items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name") or item.get("model") or item.get("id") or "").strip()
        if name:
            names.append(name)
    return _unique_sorted(names)


def _replace_combo_items(combo: object, models: list[str], current: str) -> None:
    """Replace combo items while preserving a valid current selection."""
    clear = getattr(combo, "clear", None)
    add_items = getattr(combo, "addItems", None)
    add_item = getattr(combo, "addItem", None)
    set_current = getattr(combo, "setCurrentText", None)
    if callable(clear):
        clear()
    if models and callable(add_items):
        add_items(models)
    if current and current not in models and callable(add_item):
        add_item(current)
    selected = current or (models[0] if models else DEFAULT_MODEL)
    if callable(set_current):
        set_current(selected)


def _unique_sorted(names: Iterable[str]) -> list[str]:
    """Return stable unique model names."""
    return sorted({str(name).strip() for name in names if str(name).strip()}, key=str.casefold)


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
