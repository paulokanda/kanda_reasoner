"""Clipboard buttons and message-copy links for Project Web AI."""

from __future__ import annotations

import html
import re
from typing import Any

from kanda_reasoner_app.reasoner_engine.chat_clipboard_actions import (
    copy_editor_text,
    copy_text,
    paste_clipboard_into,
)

__all__ = [
    "connect_project_web_ai_clipboard_actions",
    "render_project_web_ai_message_html",
]

_COPY_LINK = re.compile(r"^copy-message-(\d+)$")
_BUTTON_STYLE = (
    "display:inline-block; color:#e8edf3; text-decoration:none; "
    "background-color:#222730; border:1px solid #383f4b; "
    "padding:4px 9px; border-radius:6px; font-size:11px;"
)


def _notify(owner: Any, message: str) -> None:
    owner.status_value.setText(message)


def _refresh_primary_action(owner: Any) -> None:
    """Recompute the canonical Send gate after programmatic editor changes."""
    refresh = getattr(owner, "_update_send_state", None)
    if callable(refresh):
        refresh()


def _paste_question(owner: Any) -> None:
    if paste_clipboard_into(owner.question_edit):
        _refresh_primary_action(owner)
        _notify(owner, "Clipboard pasted into the Web AI question.")


def _copy_draft(owner: Any) -> None:
    if copy_editor_text(owner.question_edit):
        _notify(owner, "Web AI question copied.")


def _copy_message(owner: Any, link: object) -> None:
    text = link.toString() if hasattr(link, "toString") else str(link)
    match = _COPY_LINK.fullmatch(text)
    if match is None:
        return
    index = int(match.group(1))
    messages = owner._active_chat().messages
    if 0 <= index < len(messages) and copy_text(messages[index].content):
        label = "question" if messages[index].role == "user" else "answer"
        _notify(owner, "Web AI " + label + " copied.")


def _refresh_draft_state(owner: Any) -> None:
    owner.copy_question_button.setEnabled(
        bool(owner.question_edit.toPlainText())
    )


def connect_project_web_ai_clipboard_actions(owner: Any) -> None:
    """Connect the visible clipboard controls to memory-only chat state."""
    owner.paste_question_button.clicked.connect(
        lambda _checked=False: _paste_question(owner)
    )
    owner.copy_question_button.clicked.connect(
        lambda _checked=False: _copy_draft(owner)
    )
    owner.answer_box.anchorClicked.connect(lambda link: _copy_message(owner, link))
    owner.question_edit.textChanged.connect(lambda: _refresh_draft_state(owner))
    _refresh_draft_state(owner)


def _copy_action(index: int, visible: bool) -> str:
    if not visible:
        return ""
    return (
        '<div style="margin-top:10px;">'
        '<a href="copy-message-' + str(index) + '" style="' + _BUTTON_STYLE
        + '">Copy</a></div>'
    )


def render_project_web_ai_message_html(
    role: str,
    content: str,
    state: str,
    index: int,
) -> str:
    """Return one escaped chat card with a message-specific Copy button."""
    raw = str(content or "")
    rendered = html.escape(raw or "Thinking...").replace("\n", "<br>")
    action = _copy_action(index, bool(raw))
    if role == "user":
        return (
            '<table width="100%" cellspacing="0" cellpadding="0" '
            'style="margin:12px 0 18px 0;"><tr>'
            '<td width="22%"></td><td bgcolor="#2b3039" '
            'style="padding:13px 16px; color:#f6f7f9;">'
            '<div style="font-size:11px; font-weight:600; color:#aeb6c2; '
            'margin-bottom:6px;">YOU</div>' + rendered + action
            + "</td></tr></table>"
        )
    tone = "#ef6a6a" if state == "failed" else "#95a0ad"
    return (
        '<table width="100%" cellspacing="0" cellpadding="0" '
        'style="margin:8px 0 24px 0;"><tr><td bgcolor="#15181e" '
        'style="padding:15px 18px; color:#eef1f5;">'
        '<div style="font-size:11px; font-weight:600; color:' + tone
        + '; margin-bottom:7px;">PROJECT WEB AI</div>' + rendered + action
        + '</td><td width="10%"></td></tr></table>'
    )
