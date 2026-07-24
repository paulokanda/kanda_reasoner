# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_suggestion.py
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

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_row_bridge_runtime import (
    generate_ai_review_draft_for_row,
)


__all__ = ["generate_manual_review_docstring"]


def generate_manual_review_docstring(
    window: object,
    location: dict,
    module_text: str,
) -> str:
    """Return one provider-selected draft through the canonical row bridge."""
    return generate_ai_review_draft_for_row(window, location, module_text)


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
