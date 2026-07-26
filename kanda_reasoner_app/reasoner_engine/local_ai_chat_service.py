# project-path: kanda_reasoner_app/reasoner_engine/local_ai_chat_service.py
"""Shared Local AI chat service over the application-scoped configuration."""

from __future__ import annotations

import importlib
from typing import Any

__all__ = [
    "AUTO_LOCAL_AI_MODEL_LABEL",
    "LocalAIChatError",
    "chat_with_local_model",
    "get_local_ai_model_candidates",
    "list_local_ai_models",
    "local_ai_configuration_snapshot",
    "resolve_local_ai_model",
]

AUTO_LOCAL_AI_MODEL_LABEL = "Auto (global Config Local AI model)"
MODEL_REGISTRY_MODULE = "kanda_reasoner_app.reasoner_engine.v10_model_registry"
MODEL_REGISTRY_CLASS = "LocalModelRegistry"
LOCAL_AI_MODULE = "kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models"
LOCAL_AI_CLASS = "V9QwenAIModels"


class LocalAIChatError(RuntimeError):
    """Raised when the global Local AI model cannot be selected or called."""


def _load_class(module_name: str, class_name: str) -> type[Any]:
    module = importlib.import_module(module_name)
    loaded = getattr(module, class_name)
    if not isinstance(loaded, type):
        raise TypeError(module_name + "." + class_name + " is not a class")
    return loaded


def local_ai_configuration_snapshot() -> Any | None:
    """Return current Tool-owned Local AI configuration when Qt is active."""
    from kanda_reasoner_app.local_ai_runtime_state import (
        runtime_local_ai_configuration_snapshot,
    )

    return runtime_local_ai_configuration_snapshot()


def _model_key(value: str) -> str:
    text = str(value or "").lower()
    replacements = {
        "qwen": "qn",
        "coder": "",
        "code": "",
        "ollama": "",
        "model": "",
        ":": "",
        "-": "",
        "_": "",
        ".": "",
        " ": "",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.strip()


def list_local_ai_models(registry: Any | None = None) -> list[str]:
    """Return normalized models from the global endpoint."""
    if registry is None:
        registry_class = _load_class(MODEL_REGISTRY_MODULE, MODEL_REGISTRY_CLASS)
        snapshot = local_ai_configuration_snapshot()
        kwargs = {}
        if snapshot is not None:
            kwargs = {
                "base_url": snapshot.base_url,
                "preferred_model": snapshot.model_id,
            }
        registry = registry_class(**kwargs)
    models = registry.list_models()
    return [str(model).strip() for model in models if str(model).strip()]


def _match_selected_model(selected: str, models: list[str]) -> str:
    if selected in models:
        return selected
    selected_key = _model_key(selected)
    for model in models:
        if _model_key(model) == selected_key:
            return model
    return ""


def get_local_ai_model_candidates(selection: str, registry: Any | None = None) -> list[str]:
    """Return global-first concrete model names for a local AI task."""
    snapshot = local_ai_configuration_snapshot()
    configured = "" if snapshot is None else str(snapshot.model_id or "").strip()
    selected = configured or str(selection or "").strip()
    models = list_local_ai_models(registry)
    if selected and selected != AUTO_LOCAL_AI_MODEL_LABEL:
        matched = _match_selected_model(selected, models)
        if matched:
            return [matched]
        if configured:
            return [configured]
        if models:
            return models
        return [selected]
    return models


def resolve_local_ai_model(selection: str = "", registry: Any | None = None) -> str:
    """Resolve any legacy selection through Config Local AI first."""
    candidates = get_local_ai_model_candidates(selection, registry)
    return candidates[0] if candidates else ""


def chat_with_local_model(
    messages: list[dict[str, str]],
    *,
    model_selection: str = "",
    temperature: float = 0.05,
    max_tokens: int = 3500,
) -> tuple[str, str]:
    """Run one request using the global endpoint and model."""
    snapshot = local_ai_configuration_snapshot()
    model_name = resolve_local_ai_model(model_selection)
    if not model_name:
        raise LocalAIChatError(
            "No global Local AI model is configured. Open Config AI > Config Local AI."
        )
    ai_class = _load_class(LOCAL_AI_MODULE, LOCAL_AI_CLASS)
    kwargs = {} if snapshot is None else {"base_url": snapshot.base_url}
    ai = ai_class(**kwargs)
    response = ai.chat(
        messages,
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        use_cache=False,
    )
    return str(response or ""), model_name
