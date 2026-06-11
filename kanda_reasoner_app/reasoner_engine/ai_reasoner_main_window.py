"""Canonical GUI main window loader with retired namespace aliases."""

from __future__ import annotations

import sys
from importlib import import_module
from types import ModuleType

from kanda_reasoner_app.backend_payloads.loader import load_payload

_RETIRED_TOP_PARTS = ("ask_ai", "project_reasoner")
_RETIRED_ENGINE_PARTS = ("project", "reasoner_v10")
_RETIRED_TOP = "_".join(_RETIRED_TOP_PARTS)
_RETIRED_ENGINE = "_".join(_RETIRED_ENGINE_PARTS)
_KANDA_RETIRED_ENGINE = "kanda_reasoner_app." + _RETIRED_ENGINE
_ASK_AI_RETIRED_ENGINE = _RETIRED_TOP + "." + _RETIRED_ENGINE
_CANONICAL_ENGINE = "kanda_reasoner_app.reasoner_engine"
_CANONICAL_HELP = _CANONICAL_ENGINE + ".ai_reasoner_main_window_help"
_RETIRED_HELP = "main_window_help"

_MODULE_ALIASES = {
    _KANDA_RETIRED_ENGINE: _CANONICAL_ENGINE,
    _ASK_AI_RETIRED_ENGINE: _CANONICAL_ENGINE,
    _KANDA_RETIRED_ENGINE + "." + _RETIRED_HELP: _CANONICAL_HELP,
    _ASK_AI_RETIRED_ENGINE + "." + _RETIRED_HELP: _CANONICAL_HELP,
}

_ENGINE_CHILDREN = (
    "ai_bridge",
    "core",
    "help_index",
    "index_loader",
    "project_profile",
    "prompt_builder",
    "query_router",
    "reasoner_retriever",
    "v10_conversation_memory",
    "v10_intent_detection",
    "v10_model_registry",
    "v10_models",
    "v10_qwen_ai_models",
    "v10_scoring_config",
)

_HELPER_CHILDREN = (
    "analysis_controller",
    "answer_presenter",
    "json_track",
    "profile_controller",
    "runtime_controller",
    "session_service",
    "settings_manager",
    "signal_wiring",
    "state_models",
    "static_context_controller",
    "ui_builder",
    "ui_components",
)

for _child in _ENGINE_CHILDREN:
    _MODULE_ALIASES[_KANDA_RETIRED_ENGINE + "." + _child] = (
        _CANONICAL_ENGINE + "." + _child
    )
    _MODULE_ALIASES[_ASK_AI_RETIRED_ENGINE + "." + _child] = (
        _CANONICAL_ENGINE + "." + _child
    )

for _child in _HELPER_CHILDREN:
    _MODULE_ALIASES[
        _KANDA_RETIRED_ENGINE + "." + _RETIRED_HELP + "." + _child
    ] = _CANONICAL_HELP + "." + _child
    _MODULE_ALIASES[
        _ASK_AI_RETIRED_ENGINE + "." + _RETIRED_HELP + "." + _child
    ] = _CANONICAL_HELP + "." + _child


def _alias_module(alias_name: str, target_name: str) -> ModuleType:
    """Install one retired import alias that points at a canonical module."""
    module = import_module(target_name)
    sys.modules[alias_name] = module
    return module


def install_canonical_main_window_helper_package_aliases() -> None:
    """Alias retired helper package names to the canonical helper package."""
    import sys
    from importlib import import_module

    canonical_name = (
        "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help"
    )
    alias_name = "kanda_reasoner_app.reasoner_engine.main_window_help"

    canonical_package = import_module(canonical_name)
    sys.modules.setdefault(alias_name, canonical_package)


install_canonical_main_window_helper_package_aliases()
def install_retired_main_window_aliases() -> None:
    """Install aliases needed by old embedded GUI payload imports."""
    app_module = import_module("kanda_reasoner_app")
    sys.modules.setdefault(_RETIRED_TOP, app_module)

    for alias_name, target_name in _MODULE_ALIASES.items():
        _alias_module(alias_name, target_name)


def install_canonical_main_window_helper_package_aliases() -> None:
    """Alias retired helper package names to the canonical helper package."""
    import sys
    from importlib import import_module

    canonical_name = (
        "kanda_reasoner_app.reasoner_engine.ai_reasoner_main_window_help"
    )
    alias_name = "kanda_reasoner_app.reasoner_engine.main_window_help"

    canonical_package = import_module(canonical_name)
    sys.modules.setdefault(alias_name, canonical_package)


install_canonical_main_window_helper_package_aliases()
install_retired_main_window_aliases()

load_payload(__name__, globals(), "z")

_existing_all = globals().get("__all__", ())
_extra_all = ("install_retired_main_window_aliases",)
if isinstance(_existing_all, list):
    __all__ = sorted(set(_existing_all + list(_extra_all)))
elif isinstance(_existing_all, tuple):
    __all__ = tuple(sorted(set(_existing_all + _extra_all)))
else:
    __all__ = _extra_all
