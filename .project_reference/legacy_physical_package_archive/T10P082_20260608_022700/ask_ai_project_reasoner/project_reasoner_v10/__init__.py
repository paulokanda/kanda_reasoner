"""
Curated public API for kanda_reasoner_app.project_reasoner_v10.

This package is primarily consumed through explicit submodule imports, but this
module exposes a stable root-level surface for the most important entry points,
models, routing helpers, and profile helpers.

The exports are loaded lazily at runtime to avoid unnecessary GUI or runtime
side effects when consumers only need a subset of the package.

Static analyzers and IDEs are supported through TYPE_CHECKING imports so the
curated public API resolves cleanly in editors.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .ai_bridge import AIWorkerBridge, LocalAIReasoner
    from .ai_reasoner_main_window import JsonProjectReasonerV10, main
    from .help_index import HELP_INDEX
    from .query_router import QueryRouteDecision, route_query_intent
    from .reasoner_retriever import ProjectRetriever
    from .index_loader import JsonProjectIndex
    from .v10_models import (
        ConversationTurn,
        EvidenceItem,
        RetrievalBundle,
        SymbolEvidenceItem,
    )
    from .project_profile import (
        GENERIC_PROJECT_PROFILE,
        ProjectProfile,
        get_project_profile,
        infer_project_profile,
        infer_project_profile_name_from_metadata,
        iter_project_profiles,
    )

__all__ = [
    "JsonProjectReasonerV10",
    "main",
    "JsonProjectIndex",
    "ProjectRetriever",
    "LocalAIReasoner",
    "AIWorkerBridge",
    "QueryRouteDecision",
    "route_query_intent",
    "HELP_INDEX",
    "EvidenceItem",
    "SymbolEvidenceItem",
    "RetrievalBundle",
    "ConversationTurn",
    "ProjectProfile",
    "GENERIC_PROJECT_PROFILE",
    "get_project_profile",
    "iter_project_profiles",
    "infer_project_profile",
    "infer_project_profile_name_from_metadata",
]

_EXPORT_MAP: dict[str, tuple[str, str]] = {
    "JsonProjectReasonerV10": (".ai_reasoner_main_window", "JsonProjectReasonerV10"),
    "main": (".ai_reasoner_main_window", "main"),
    "JsonProjectIndex": (".index_loader", "JsonProjectIndex"),
    "ProjectRetriever": (".reasoner_retriever", "ProjectRetriever"),
    "LocalAIReasoner": (".ai_bridge", "LocalAIReasoner"),
    "AIWorkerBridge": (".ai_bridge", "AIWorkerBridge"),
    "QueryRouteDecision": (".query_router", "QueryRouteDecision"),
    "route_query_intent": (".query_router", "route_query_intent"),
    "HELP_INDEX": (".help_index", "HELP_INDEX"),
    "EvidenceItem": (".v10_models", "EvidenceItem"),
    "SymbolEvidenceItem": (".v10_models", "SymbolEvidenceItem"),
    "RetrievalBundle": (".v10_models", "RetrievalBundle"),
    "ConversationTurn": (".v10_models", "ConversationTurn"),
    "ProjectProfile": (".project_profile", "ProjectProfile"),
    "GENERIC_PROJECT_PROFILE": (".project_profile", "GENERIC_PROJECT_PROFILE"),
    "get_project_profile": (".project_profile", "get_project_profile"),
    "iter_project_profiles": (".project_profile", "iter_project_profiles"),
    "infer_project_profile": (".project_profile", "infer_project_profile"),
    "infer_project_profile_name_from_metadata": (
        ".project_profile",
        "infer_project_profile_name_from_metadata",
    ),
}


def __getattr__(name: str) -> Any:
    if name not in _EXPORT_MAP:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module_name, symbol_name = _EXPORT_MAP[name]
    module = import_module(module_name, __name__)
    value = getattr(module, symbol_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))





