# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/ai_settings.py
"""Tab 3 local-AI settings facade."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "ollama_tags_url",
    "refresh_models",
    "build_ai_config",
    "persist_runtime_config",
    "load_config_from_file",
    "save_config_to_file",
]


def _runtime() -> Any:
    """Load the legacy local-settings runtime lazily."""
    package = "kanda_reasoner_app.tab3_manual_review_runtime"
    return import_module(package + ".ai_settings_runtime")


def _web_runtime() -> Any:
    """Load the provider-neutral Docstring Assistant controls lazily."""
    package = "kanda_reasoner_app.tab3_manual_review_runtime"
    return import_module(package + ".ai_web_controls_runtime")


def ollama_tags_url(*args: Any, **kwargs: Any) -> Any:
    """Return the Ollama tags URL for a configured base endpoint."""
    return _runtime()._runtime_ollama_tags_url(*args, **kwargs)


def refresh_models(*args: Any, **kwargs: Any) -> Any:
    """Refresh local or web models through the selected canonical owner."""
    return _web_runtime().refresh_models(*args, **kwargs)


def build_ai_config(*args: Any, **kwargs: Any) -> Any:
    """Build provider-neutral settings without persisting credentials."""
    return _web_runtime().build_ai_config(*args, **kwargs)


def persist_runtime_config(*args: Any, **kwargs: Any) -> Any:
    """Persist non-secret runtime settings for worker execution."""
    owner = args[0]
    cfg = _web_runtime().build_ai_config(owner)
    path = getattr(owner, "_runtime_dir") / "runtime_ai_config.json"
    cfg.to_json(path)
    return path


def load_config_from_file(*args: Any, **kwargs: Any) -> Any:
    """Load only task options; global endpoint/model remain Config AI-owned."""
    return _runtime()._runtime_load_config_from_file(*args, **kwargs)


def save_config_to_file(*args: Any, **kwargs: Any) -> Any:
    """Save Tab 3 local-AI settings to a JSON file."""
    return _runtime()._runtime_save_config_to_file(*args, **kwargs)
