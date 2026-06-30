# project-path: kanda_reasoner_app/reasoner_engine/__init__.py
"""Canonical reasoner engine package.

This package is the active engine namespace. Its initializer only exposes
canonical modules and selected public symbols through lazy imports.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

_CANONICAL_MODULE_EXPORTS = {
    "ai_bridge": "kanda_reasoner_app.reasoner_engine.ai_bridge",
    "ai_reasoner_main_window": (
        "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
    ),
    "core": "kanda_reasoner_app.reasoner_engine.core",
    "help_index": "kanda_reasoner_app.reasoner_engine.help_index",
    "index_loader": "kanda_reasoner_app.reasoner_engine.index_loader",
    "project_profile": "kanda_reasoner_app.reasoner_engine.project_profile",
    "prompt_builder": "kanda_reasoner_app.reasoner_engine.prompt_builder",
    "query_router": "kanda_reasoner_app.reasoner_engine.query_router",
    "reasoner_retriever": (
        "kanda_reasoner_app.reasoner_engine.reasoner_retriever"
    ),
    "v10_conversation_memory": (
        "kanda_reasoner_app.reasoner_engine.v10_conversation_memory"
    ),
    "v10_intent_detection": (
        "kanda_reasoner_app.reasoner_engine.v10_intent_detection"
    ),
    "v10_model_registry": (
        "kanda_reasoner_app.reasoner_engine.v10_model_registry"
    ),
    "v10_models": "kanda_reasoner_app.reasoner_engine.v10_models",
    "v10_qwen_ai_models": (
        "kanda_reasoner_app.reasoner_engine.v10_qwen_ai_models"
    ),
    "v10_scoring_config": (
        "kanda_reasoner_app.reasoner_engine.v10_scoring_config"
    ),
}

_SYMBOL_EXPORTS = {
    "JsonProjectReasonerV10": (
        "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window"
    ),
    "main": "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window",
}

__all__ = tuple(
    sorted(
        list(_CANONICAL_MODULE_EXPORTS.keys())
        + list(_SYMBOL_EXPORTS.keys())
    )
)


def __getattr__(name: str) -> Any:
    """Resolve canonical engine modules and selected public symbols lazily."""
    if name in _CANONICAL_MODULE_EXPORTS:
        return import_module(_CANONICAL_MODULE_EXPORTS[name])

    if name in _SYMBOL_EXPORTS:
        module = import_module(_SYMBOL_EXPORTS[name])
        return getattr(module, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
