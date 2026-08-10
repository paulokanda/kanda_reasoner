# project-path: kanda_reasoner_app/external_ai_handoff.py
"""Manual clipboard-and-browser handoff for external Python-coding assistants."""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QGuiApplication

from kanda_reasoner_app.python_coding_ai_catalog import (
    ExternalPythonCodingAssistant,
)

__all__ = ["ExternalAIHandoffResult", "copy_and_open_external_assistant"]

_MAX_CLIPBOARD_CHARACTERS = 4_000_000


@dataclass(frozen=True, slots=True)
class ExternalAIHandoffResult:
    """Report the bounded manual handoff performed for one user action."""

    assistant_id: str
    copied_characters: int
    browser_open_requested: bool
    official_url: str


def copy_and_open_external_assistant(
    assistant: ExternalPythonCodingAssistant,
    prompt_text: str,
) -> ExternalAIHandoffResult:
    """Copy a bounded prompt and request the official site in the default browser.

    The function never logs in, pastes, submits, reads browser state, or receives
    a response. The user remains responsible for reviewing and pasting the text.
    """
    clean_prompt = str(prompt_text or "").strip()
    if not clean_prompt:
        raise ValueError("External AI handoff prompt is empty.")
    if len(clean_prompt) > _MAX_CLIPBOARD_CHARACTERS:
        raise ValueError("External AI handoff prompt exceeds the clipboard limit.")
    clipboard = QGuiApplication.clipboard()
    if clipboard is None:
        raise RuntimeError("The application clipboard is unavailable.")
    clipboard.setText(clean_prompt)
    official_url = assistant.validated_url()
    opened = bool(QDesktopServices.openUrl(QUrl(official_url)))
    return ExternalAIHandoffResult(
        assistant_id=assistant.assistant_id,
        copied_characters=len(clean_prompt),
        browser_open_requested=opened,
        official_url=official_url,
    )
