# project-path: kanda_reasoner_app/web_ai_response_normalization.py
"""Normalize OpenAI-compatible response content and safe diagnostics."""

from __future__ import annotations

from typing import Mapping, Sequence

__all__ = [
    "extract_choice_content",
    "extract_non_stream_choice",
    "response_content_type",
    "safe_stream_diagnostics",
]


def _text_from_value(value: object) -> str:
    """Return readable text from common provider content shapes."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        for key in ("text", "output_text", "content", "value"):
            if key not in value:
                continue
            text = _text_from_value(value.get(key))
            if text:
                return text
        return ""
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        parts = [_text_from_value(item) for item in value]
        return "".join(part for part in parts if part)
    return ""


def extract_choice_content(choice: Mapping[str, object]) -> str:
    """Extract text from streaming or non-streaming choice shapes."""
    delta = choice.get("delta")
    if isinstance(delta, Mapping):
        for key in ("content", "text"):
            text = _text_from_value(delta.get(key))
            if text:
                return text

    message = choice.get("message")
    if isinstance(message, Mapping):
        for key in ("content", "text"):
            text = _text_from_value(message.get(key))
            if text:
                return text

    for key in ("text", "content"):
        text = _text_from_value(choice.get(key))
        if text:
            return text
    return ""


def extract_non_stream_choice(
    payload: Mapping[str, object],
) -> tuple[Mapping[str, object], str]:
    """Return the first usable choice and normalized content."""
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        return {}, ""
    first = choices[0]
    if not isinstance(first, Mapping):
        return {}, ""
    return first, extract_choice_content(first)


def response_content_type(response: object) -> str:
    """Return a safe response content-type label when available."""
    headers = getattr(response, "headers", None)
    getter = getattr(headers, "get", None)
    if not callable(getter):
        return "unknown"
    try:
        value = getter("Content-Type", "")
    except TypeError:
        value = getter("Content-Type")
    return str(value or "unknown").strip()[:160]


def safe_stream_diagnostics(
    *,
    content_type: str,
    sse_events: int,
    choice_events: int,
    text_chunks: int,
    finish_reason: str,
    fallback_status: str,
) -> str:
    """Return bounded diagnostics without request content or credentials."""
    reason = str(finish_reason or "unknown").strip()[:80]
    return (
        "content_type=" + str(content_type or "unknown")[:160]
        + "; sse_events=" + str(max(0, int(sse_events)))
        + "; choice_events=" + str(max(0, int(choice_events)))
        + "; text_chunks=" + str(max(0, int(text_chunks)))
        + "; finish_reason=" + reason
        + "; non_stream_fallback=" + str(fallback_status or "not_attempted")[:160]
    )
