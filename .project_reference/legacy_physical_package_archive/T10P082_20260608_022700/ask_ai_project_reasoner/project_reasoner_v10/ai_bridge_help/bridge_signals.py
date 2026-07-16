"""Support V10 project reasoning and evidence handling."""

# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
# MODULE ORIGIN : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_bridge.py
# MANIFEST      : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_bridge_help.json
# HELP FOLDER   : E:\developer_tools\kanda_reasoner_app\project_reasoner_v10\ai_bridge_help
# PURPOSE       : Qt signal bridge for AI answer, token, error, and status events.
# EXPORTS       : AIWorkerBridge
# DEPENDS ON    : none
# REFACTOR DATE : 2026-04-11
# -"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR-"EUR
from __future__ import annotations

from PySide6.QtCore import QObject, Signal

__all__ = ["AIWorkerBridge"]


class AIWorkerBridge(QObject):
    answer_ready = Signal(str)
    token_ready = Signal(str)
    error_ready = Signal(str)
    status_ready = Signal(str)



