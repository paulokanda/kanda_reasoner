"""Support V10 project reasoning and evidence handling."""

# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
# MODULE ORIGIN : kanda_reasoner_app\reasoner_engine\ai_bridge.py
# MANIFEST      : kanda_reasoner_app\reasoner_engine\ai_bridge_help.json
# HELP FOLDER   : kanda_reasoner_app\reasoner_engine\ai_bridge_help
# PURPOSE       : Qt signal bridge for AI answer, token, error, and status events.
# EXPORTS       : AIWorkerBridge
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-11
# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = ["AIWorkerBridge"]


def _load_qt_core_symbol(symbol_name: str) -> Any:
    """Load one QtCore symbol only when the bridge is instantiated."""
    qt_core = import_module("PySide6.QtCore")
    return getattr(qt_core, symbol_name)


def _build_qt_ai_worker_bridge() -> Any:
    """Build the concrete Qt signal bridge behind a lazy boundary."""
    qobject = _load_qt_core_symbol("QObject")
    signal = _load_qt_core_symbol("Signal")

    class QtAIWorkerBridge(qobject):
        """Qt-backed signal bridge for local AI worker events."""

        answer_ready = signal(str)
        token_ready = signal(str)
        error_ready = signal(str)
        status_ready = signal(str)

    return QtAIWorkerBridge


class AIWorkerBridge:
    """Lazy factory for the Qt-backed AI worker bridge."""

    def __new__(cls) -> Any:
        bridge_class = _build_qt_ai_worker_bridge()
        return bridge_class()



