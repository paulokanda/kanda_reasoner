# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_style_diagnostics_runtime.py
"""Diagnostic trace helpers for Tab 3 AI docstring style flow."""

from __future__ import annotations

import re

__all__ = [
    "AI_STYLE_DIAGNOSTICS_CONTRACT",
    "append_ai_style_trace",
    "short_trace_text",
    "source_names_from_snippet",
    "style_trace_enabled_from_owner",
]

AI_STYLE_DIAGNOSTICS_CONTRACT = "tab3_ai_style_diagnostics_v1"
_MAX_TRACE_BODY_CHARS = 220


def style_trace_enabled_from_owner(owner: object) -> bool:
    """Return whether temporary AI style diagnostics should be emitted."""
    value = getattr(owner, "_ai_style_trace_enabled", True)
    return bool(value)


def append_ai_style_trace(owner: object, label: str, **values: object) -> None:
    """Append one normalized AI style trace line to the output panel."""
    if not style_trace_enabled_from_owner(owner):
        return
    append_text = getattr(owner, "_append_text", None)
    if not callable(append_text):
        return
    parts = []
    for key in sorted(values):
        parts.append(str(key) + "=" + _format_trace_value(values[key]))
    suffix = ""
    if parts:
        suffix = " " + " ".join(parts)
    append_text("[review-style-trace] " + str(label) + suffix + "\n")


def short_trace_text(value: object, limit: int = _MAX_TRACE_BODY_CHARS) -> str:
    """Return a single-line diagnostic preview for a potentially long value."""
    text = str(value or "").replace("\r", "\\r").replace("\n", "\\n")
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)] + "..."


def source_names_from_snippet(source_snippet: str) -> list[str]:
    """Return visible function and class names from a source snippet."""
    names: list[str] = []
    patterns = (
        r"^\s*(?:async\s+def|def)\s+([A-Za-z_]\w*)\s*\(",
        r"^\s*class\s+([A-Za-z_]\w*)\b",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, str(source_snippet or ""), flags=re.MULTILINE):
            name = match.group(1)
            if name and not name.startswith("_") and name not in names:
                names.append(name)
    return names[:6]


def _format_trace_value(value: object) -> str:
    """Return a stable key-value representation for one trace value."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, (list, tuple)):
        return "[" + ",".join(short_trace_text(item, 60) for item in value) + "]"
    if value is None:
        return "<none>"
    return '"' + short_trace_text(value) + '"'
