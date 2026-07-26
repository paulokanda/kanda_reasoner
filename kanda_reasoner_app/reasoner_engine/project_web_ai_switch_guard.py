# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_switch_guard.py
"""Guard Project Web AI Project switching during source-write transactions."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import QSignalBlocker
from PySide6.QtWidgets import QMessageBox

from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
    ProjectSwitchDecision,
    ProjectWebAISessionStateError,
)

__all__ = ["request_guarded_project_switch"]


def request_guarded_project_switch(
    owner: Any,
    root_text: str,
) -> ProjectSwitchDecision | None:
    """Request one Project switch or restore the current root fail closed."""
    try:
        return owner._project_session.request_switch(
            root_text,
            worker_running=owner._chat_thread is not None,
        )
    except ProjectWebAISessionStateError as exc:
        identity = owner._project_session.identity
        current_root = identity.project_root if identity is not None else ""
        blocker = QSignalBlocker(owner.project_root_edit)
        owner.project_root_edit.setText(current_root)
        del blocker
        owner.status_value.setText(str(exc))
        QMessageBox.warning(
            owner,
            "Project switch blocked",
            "An open or unresolved Project source transaction must settle "
            "before changing Projects.\n\n" + str(exc),
        )
        owner._update_send_state()
        return None
