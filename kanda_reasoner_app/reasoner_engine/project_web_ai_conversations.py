# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_conversations.py
"""Own in-memory Project Web AI chats and explicit Markdown export.

The normal chat lifecycle is memory-only.  This module writes only when the
user explicitly chooses Save chat and selects a destination outside the active
project source and Project Support roots.  It owns no provider transport,
project-context loading, credential persistence, or request identity.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QFileDialog, QListWidgetItem, QMessageBox

from kanda_reasoner_app.reasoner_engine.project_web_ai_clipboard_actions import (
    connect_project_web_ai_clipboard_actions,
    render_project_web_ai_message_html,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ProjectWebAIRequestIdentity,
)

__all__ = ["ProjectWebAIChatHistoryMixin"]


@dataclass
class _ChatMessage:
    """Represent one visible message and its model-context eligibility."""

    role: str
    content: str
    state: str = "complete"
    include_in_context: bool = False


@dataclass
class _ChatSession:
    """Represent one memory-only conversation listed in the sidebar."""

    session_id: str
    title: str = "New chat"
    created_at_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    messages: list[_ChatMessage] = field(default_factory=list)
    provenance: str = ""

    def context_history(self) -> list[dict[str, str]]:
        """Return only completed pairs approved for future model context."""
        return [
            {"role": message.role, "content": message.content}
            for message in self.messages
            if message.include_in_context and message.content.strip()
        ]


class _ChatStore:
    """Keep ordered chats in memory without automatic persistence."""

    def __init__(self) -> None:
        self._sessions: list[_ChatSession] = []

    def create(self) -> _ChatSession:
        """Create and prepend one empty chat."""
        session = _ChatSession(session_id=uuid.uuid4().hex)
        self._sessions.insert(0, session)
        return session

    def all_sessions(self) -> tuple[_ChatSession, ...]:
        """Return chats newest first."""
        return tuple(self._sessions)

    def get(self, session_id: str) -> _ChatSession | None:
        """Return one chat by identity."""
        return next(
            (item for item in self._sessions if item.session_id == session_id),
            None,
        )

    def delete(self, session_id: str) -> None:
        """Delete one memory-only chat."""
        self._sessions = [
            item for item in self._sessions if item.session_id != session_id
        ]


class ProjectWebAIChatHistoryMixin:
    """Add professional in-memory chat history to Project Web AI."""

    def _initialize_chat_history(self) -> None:
        """Create the session store and first empty chat."""
        self._chat_store = _ChatStore()
        self._active_chat_id = ""
        self._active_user_message_index = -1
        self._active_assistant_message_index = -1
        session = self._chat_store.create()
        self._activate_chat(session.session_id)

    def _connect_chat_history_signals(self) -> None:
        """Connect sidebar history actions after controls exist."""
        self.clear_button.clicked.connect(self.new_chat)
        self.load_chat_button.clicked.connect(self.load_selected_chat)
        self.delete_chat_button.clicked.connect(self.delete_selected_chat)
        self.save_chat_button.clicked.connect(self.save_selected_chat)
        connect_project_web_ai_clipboard_actions(self)
        self.chat_list.itemDoubleClicked.connect(
            lambda _item: self.load_selected_chat()
        )
        self.chat_list.currentItemChanged.connect(
            lambda _current, _previous: self._update_chat_history_action_state(
                self._chat_thread is not None
            )
        )

    def _active_chat(self) -> _ChatSession:
        """Return the active chat, creating one when needed."""
        session = self._chat_store.get(self._active_chat_id)
        if session is None:
            session = self._chat_store.create()
            self._active_chat_id = session.session_id
        return session

    def _activate_chat(self, session_id: str) -> None:
        """Load one chat into the conversation canvas."""
        session = self._chat_store.get(session_id)
        if session is None:
            return
        self._active_chat_id = session_id
        self._history = session.context_history()
        self.provenance_box.setPlainText(session.provenance)
        self._rebuild_chat_list()
        self._render_active_chat()
        self._update_chat_history_action_state(self._chat_thread is not None)

    def _reset_chat_history_for_project(self) -> None:
        """Prevent chat leakage when the active project root changes."""
        self._chat_store = _ChatStore()
        session = self._chat_store.create()
        self._active_chat_id = session.session_id
        self._active_user_message_index = -1
        self._active_assistant_message_index = -1
        self._history.clear()
        self.question_edit.clear()
        self.provenance_box.clear()
        self._rebuild_chat_list()
        self._render_active_chat()

    def _rebuild_chat_list(self) -> None:
        """Refresh the visible chat list without changing active identity."""
        self.chat_list.blockSignals(True)
        self.chat_list.clear()
        selected_row = -1
        for row, session in enumerate(self._chat_store.all_sessions()):
            item = QListWidgetItem(session.title)
            item.setData(Qt.ItemDataRole.UserRole, session.session_id)
            item.setToolTip(session.title)
            self.chat_list.addItem(item)
            if session.session_id == self._active_chat_id:
                selected_row = row
        if selected_row >= 0:
            self.chat_list.setCurrentRow(selected_row)
        self.chat_list.blockSignals(False)

    def _selected_chat_id(self) -> str:
        """Return the selected sidebar chat identity."""
        item = self.chat_list.currentItem()
        if item is None:
            return ""
        return str(item.data(Qt.ItemDataRole.UserRole) or "")

    def new_chat(self) -> None:
        """Create and activate one new memory-only chat."""
        if self._chat_thread is not None:
            return
        session = self._chat_store.create()
        self.question_edit.clear()
        self.provenance_box.clear()
        self._activate_chat(session.session_id)
        self.status_value.setText(
            "New memory-only chat created. Project context remains loaded."
        )
        self._update_send_state()

    def load_selected_chat(self) -> None:
        """Load the selected memory-only chat into the active canvas."""
        if self._chat_thread is not None:
            return
        session_id = self._selected_chat_id()
        if session_id:
            self._activate_chat(session_id)
            self.status_value.setText("Selected chat loaded from memory.")
            self._update_send_state()

    def delete_selected_chat(self) -> None:
        """Delete one selected memory-only chat after confirmation."""
        if self._chat_thread is not None:
            return
        session_id = self._selected_chat_id()
        session = self._chat_store.get(session_id)
        if session is None:
            return
        approved = QMessageBox.question(
            self,
            "Delete chat",
            "Delete this memory-only chat? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if approved != QMessageBox.StandardButton.Yes:
            return
        self._chat_store.delete(session_id)
        remaining = self._chat_store.all_sessions()
        if not remaining:
            remaining = (self._chat_store.create(),)
        self._activate_chat(remaining[0].session_id)
        self.status_value.setText("Chat deleted from memory.")
        self._update_send_state()

    def save_selected_chat(self) -> None:
        """Export the selected chat to a user-chosen Markdown file."""
        if self._chat_thread is not None:
            return
        session = self._chat_store.get(self._selected_chat_id())
        if session is None:
            return
        suggested = Path.home() / "Documents" / (
            self._safe_filename(session.title) + ".md"
        )
        selected, _filter = QFileDialog.getSaveFileName(
            self,
            "Save chat as Markdown",
            str(suggested),
            "Markdown files (*.md)",
        )
        if not selected:
            return
        target = Path(selected).expanduser()
        if target.suffix.lower() != ".md":
            target = target.with_suffix(".md")
        if self._export_target_is_protected(target):
            QMessageBox.warning(
                self,
                "Choose another folder",
                "Chat export cannot write inside Tool source, active Project source, "
                "Project Support, or transient daily-work. Choose an external folder.",
            )
            return
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(self._markdown_for(session), encoding="utf-8")
        except OSError as exc:
            QMessageBox.warning(self, "Save chat failed", str(exc))
            return
        self.status_value.setText("Chat saved as Markdown: " + str(target))

    def _export_target_is_protected(self, target: Path) -> bool:
        """Reject writes across all canonical Tool/Project boundary roots."""
        candidate = target.resolve(strict=False)
        for root in self._protected_export_roots():
            try:
                candidate.relative_to(root.resolve(strict=False))
            except ValueError:
                continue
            return True
        return False

    @staticmethod
    def _safe_filename(title: str) -> str:
        """Return a portable filename stem."""
        cleaned = re.sub(r"[^A-Za-z0-9._ -]+", "", title).strip(" .")
        cleaned = re.sub(r"\s+", "-", cleaned).lower()
        return (cleaned or "project-web-ai-chat")[:80]

    def _markdown_for(self, session: _ChatSession) -> str:
        """Return a secret-free Markdown export for one chat."""
        project = self._context.project_slug if self._context is not None else "unknown"
        lines = [
            "# " + session.title,
            "",
            "- Project: `" + project + "`",
            "- Created: `" + session.created_at_utc + "`",
            "- Exported: `" + datetime.now(timezone.utc).isoformat() + "`",
            "- Persistence: explicit user export",
            "",
            "---",
            "",
        ]
        for message in session.messages:
            label = "You" if message.role == "user" else "Web AI"
            lines.extend(("## " + label, "", message.content.rstrip(), ""))
        return "\n".join(lines).rstrip() + "\n"

    def _begin_chat_turn(self, question: str) -> None:
        """Move an approved question from composer into the chat log."""
        session = self._active_chat()
        if session.title == "New chat":
            compact = " ".join(question.split())
            session.title = compact[:48] + ("..." if len(compact) > 48 else "")
        session.messages.append(
            _ChatMessage(role="user", content=question, state="sent")
        )
        session.messages.append(
            _ChatMessage(role="assistant", content="", state="streaming")
        )
        self._active_user_message_index = len(session.messages) - 2
        self._active_assistant_message_index = len(session.messages) - 1
        self.question_edit.clear()
        self._rebuild_chat_list()
        self._render_active_chat()

    def _on_chat_started(self, identity: object) -> None:
        """Display streaming state only for the current request card."""
        if self._event_is_current(identity):
            self.status_value.setText("Streaming response...")

    def _on_chat_token(self, identity: object, token: str) -> None:
        """Append one token only for the current request card."""
        if not self._event_is_current(identity):
            return
        session = self._active_chat()
        index = self._active_assistant_message_index
        if not 0 <= index < len(session.messages):
            return
        session.messages[index].content += token
        self._render_active_chat()

    def _on_chat_completed(self, identity: object, result: object) -> None:
        """Commit one response only for the current request card."""
        if not self._event_is_current(identity):
            return
        if not isinstance(result, ChatResult):
            return
        session = self._active_chat()
        user_index = self._active_user_message_index
        assistant_index = self._active_assistant_message_index
        if not 0 <= user_index < len(session.messages):
            return
        if not 0 <= assistant_index < len(session.messages):
            return
        session.messages[assistant_index].content = result.content
        session.messages[assistant_index].state = "complete"
        session.messages[user_index].include_in_context = True
        session.messages[assistant_index].include_in_context = True
        self._history = session.context_history()
        if not isinstance(identity, ProjectWebAIRequestIdentity):
            return
        session.provenance = self._provenance_text(result, identity)
        self.provenance_box.setPlainText(session.provenance)
        self._render_active_chat()
        self.status_value.setText("Response completed. Output is advisory only.")

    def _on_chat_failed(self, identity: object, message: str) -> None:
        """Render a provider failure only for the current request card."""
        if not self._event_is_current(identity):
            return
        session = self._active_chat()
        index = self._active_assistant_message_index
        if 0 <= index < len(session.messages):
            session.messages[index].content = "REQUEST FAILED\n\n" + message
            session.messages[index].state = "failed"
        self._render_active_chat()
        self.status_value.setText(message)

    def _on_chat_cancelled(self, identity: object) -> None:
        """Mark one current request-card response as cancelled."""
        if not self._event_is_current(identity):
            return
        session = self._active_chat()
        index = self._active_assistant_message_index
        if 0 <= index < len(session.messages):
            current = session.messages[index].content.rstrip()
            session.messages[index].content = current + "\n\n[CANCELLED]"
            session.messages[index].state = "cancelled"
        self._render_active_chat()
        self.status_value.setText(
            "Request cancelled. Partial output is not in conversation history."
        )

    @staticmethod
    def _provenance_text(
        result: ChatResult,
        identity: ProjectWebAIRequestIdentity,
    ) -> str:
        """Return complete Tool/Project response provenance without credentials."""
        usage = result.usage
        cost = "unknown" if usage.cost_usd is None else f"${usage.cost_usd:.6f}"
        transport = result.raw_metadata.get("kanda_transport", {})
        transport_mode = (
            str(transport.get("mode") or "unknown")
            if isinstance(transport, dict)
            else "unknown"
        )
        return (
            "Gateway: " + result.gateway_id
            + "\nRequested model: " + result.requested_model
            + "\nReturned model: " + result.returned_model
            + "\nRequest ID: " + result.request_id
            + "\nSession ID: " + identity.session_id
            + "\nProject: " + identity.project_slug
            + "\nProject epoch: " + str(identity.project_epoch)
            + "\nProject ID: " + identity.project_id
            + "\nProject root fingerprint: " + identity.project_root_fingerprint
            + "\nProject snapshot: " + identity.snapshot_id[:12]
            + "\nContext hash: " + identity.context_hash[:12]
            + "\nApproval ID: " + identity.privacy_approval_id
            + "\nResponse ID: " + (result.response_id or "unknown")
            + "\nFinish reason: " + (result.finish_reason or "unknown")
            + "\nTransport mode: " + transport_mode
            + "\nTokens: " + str(usage.total_tokens)
            + "\nCost: " + cost
            + "\nUpstream provider: " + (usage.provider_name or "unknown")
        )

    def _render_active_chat(self) -> None:
        """Render safe, professional message cards in the read-only canvas."""
        session = self._active_chat()
        if not session.messages:
            body = (
                '<div style="margin:120px 70px; text-align:center; color:#9ba3af;">'
                '<div style="font-size:26px; font-weight:600; color:#f5f7fa;">'
                "Ask about your project"
                "</div>"
                '<div style="margin-top:12px; font-size:14px; line-height:1.6;">'
                "Project context stays read-only and is sent only after approval."
                "</div></div>"
            )
        else:
            body = "".join(
                render_project_web_ai_message_html(
                    item.role, item.content, item.state, index
                )
                for index, item in enumerate(session.messages)
            )
        document = (
            '<html><body style="background:#0d0d0d; color:#eef1f5; '
            'font-family:\'Segoe UI\', sans-serif; font-size:14px;">'
            '<div style="margin:22px 44px 42px 44px;">' + body + "</div>"
            "</body></html>"
        )
        self.answer_box.setHtml(document)
        cursor = self.answer_box.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.answer_box.setTextCursor(cursor)
        self.answer_box.ensureCursorVisible()

    def _update_chat_history_action_state(self, running: bool) -> None:
        """Fail closed chat-history actions while a request is active."""
        selected_id = self._selected_chat_id()
        selected = bool(selected_id)
        self.chat_list.setEnabled(not running)
        self.clear_button.setEnabled(not running)
        self.load_chat_button.setEnabled(
            selected and selected_id != self._active_chat_id and not running
        )
        self.delete_chat_button.setEnabled(selected and not running)
        session = self._chat_store.get(selected_id)
        self.save_chat_button.setEnabled(
            bool(session is not None and session.messages) and not running
        )
