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
    """Load the Tab 3 local-AI settings runtime lazily."""
    package = "kanda_reasoner_app.tab3_manual_review_runtime"
    return import_module(package + ".ai_settings_runtime")


def ollama_tags_url(*args: Any, **kwargs: Any) -> Any:
    """Return the Ollama tags URL for a configured base endpoint."""
    return _runtime()._runtime_ollama_tags_url(*args, **kwargs)


def refresh_models(*args: Any, **kwargs: Any) -> Any:
    """Refresh the Tab 3 model combo from supported local model sources."""
    return _runtime()._runtime_refresh_models(*args, **kwargs)


def build_ai_config(*args: Any, **kwargs: Any) -> Any:
    """Build an AI configuration object from Tab 3 controls."""
    return _runtime()._runtime_build_ai_config(*args, **kwargs)


def persist_runtime_config(*args: Any, **kwargs: Any) -> Any:
    """Persist the current runtime AI configuration for worker execution."""
    return _runtime()._runtime_persist_runtime_config(*args, **kwargs)


def load_config_from_file(*args: Any, **kwargs: Any) -> Any:
    """Load Tab 3 local-AI settings from a JSON file."""
    return _runtime()._runtime_load_config_from_file(*args, **kwargs)


def save_config_to_file(*args: Any, **kwargs: Any) -> Any:
    """Save Tab 3 local-AI settings to a JSON file."""
    return _runtime()._runtime_save_config_to_file(*args, **kwargs)
