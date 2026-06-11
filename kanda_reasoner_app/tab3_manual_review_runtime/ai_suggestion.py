# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Suggest one manual-review docstring through a local AI endpoint.
# EXPORTS       : generate_manual_review_docstring
# DEPENDS ON    : none
# REFACTOR DATE : 2026-06-01
# ------------------------------------------------------
"""Suggest one manual-review docstring through a local AI endpoint."""

from __future__ import annotations

import json
import urllib.error
import urllib.request


__all__ = ["generate_manual_review_docstring"]


def generate_manual_review_docstring(window: object, location: dict, module_text: str) -> str:
    """Return one docstring suggestion for the selected review location."""
    return _suggest_manual_review_docstring(window, location, module_text)


def _suggest_manual_review_docstring(window: object, location: dict, module_text: str) -> str:
    """Return one docstring suggestion for the selected review location."""
    fallback = _fallback_docstring(location)
    base_url = _window_text(window, ("_base_url_edit", "ai_base_url_edit", "base_url_edit", "base_url_combo"))
    model = _window_text(window, ("_model_combo", "ai_model_combo", "model_combo", "model_edit"))
    if not base_url or not model:
        return fallback
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return only one Python triple-quoted docstring."},
            {"role": "user", "content": _build_prompt(location, module_text)},
        ],
        "temperature": 0.0,
        "max_tokens": 180,
    }
    try:
        text = _post_chat_completion(base_url, payload)
    except (OSError, urllib.error.URLError, TimeoutError, ValueError):
        return fallback
    return _clean_docstring(text) or fallback


def _post_chat_completion(base_url: str, payload: dict) -> str:
    """Post to an OpenAI-compatible local chat-completions endpoint."""
    url = base_url.rstrip("/")
    if not url.endswith("/chat/completions"):
        url += "/chat/completions"
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        raw = response.read().decode("utf-8", errors="replace")
    body = json.loads(raw)
    choices = body.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    return str(message.get("content", "")).strip()


def _build_prompt(location: dict, module_text: str) -> str:
    """Build a compact prompt for one selected source location."""
    line = str(location.get("line", ""))
    return (
        "Write one concise Python docstring for this target. "
        "Do not invent parameters, return values, raises, or behavior.\n"
        + "file: " + str(location.get("file", "")) + "\n"
        + "line: " + line + "\n"
        + "target_kind: " + str(location.get("target_kind", "")) + "\n"
        + "target_name: " + str(location.get("target_name", "")) + "\n"
        + "source snippet:\n" + _nearby_source(module_text, int(location.get("line", 1) or 1))
    )


def _nearby_source(module_text: str, line_number: int) -> str:
    """Return nearby source text around a 1-based line number."""
    lines = module_text.splitlines()
    start = max(0, line_number - 8)
    end = min(len(lines), line_number + 14)
    return "\n".join(lines[start:end])


def _clean_docstring(text: str) -> str:
    """Normalize model output to a triple-quoted docstring."""
    stripped = text.strip()
    if not stripped:
        return ""
    if stripped.startswith("```"):
        stripped = stripped.strip("`").strip()
        if stripped.startswith("python"):
            stripped = stripped[6:].strip()
    triple_double = chr(34) * 3
    triple_single = chr(39) * 3
    if not stripped.startswith((triple_double, triple_single)):
        stripped = triple_double + stripped.strip(chr(34) + chr(39) + "\n ") + triple_double
    return stripped


def _fallback_docstring(location: dict) -> str:
    """Return deterministic fallback text when AI is unavailable."""
    target = str(location.get("target_name", "module") or "module")
    target = " ".join(target.replace("_", " ").replace(":", " ").split())
    if not target:
        target = "module"
    return (chr(34) * 3) + "Support " + target + " behavior." + (chr(34) * 3)


def _window_text(window: object, names: tuple[str, ...]) -> str:
    """Return text/currentText from the first matching owner-window widget."""
    for name in names:
        widget = getattr(window, name, None)
        if widget is None:
            continue
        for method_name in ("currentText", "text"):
            method = getattr(widget, method_name, None)
            if not callable(method):
                continue
            try:
                value = str(method()).strip()
            except Exception:
                value = ""
            if value:
                return value
    return ""
