# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/ai_docstring_generator_help/generation_guardrails.py
"""Validate structured AI claims and reject low-information docstrings."""

from __future__ import annotations

__all__ = []

from typing import Any

from ..context_builder import SymbolContext


class _AIOutputFailure(RuntimeError):
    """Represent an AI output failure with a canonical reason code."""

    def __init__(self, failure_reason: str, message: str) -> None:
        """Initialize the failure reason and human-readable message."""
        super().__init__(message)
        self.failure_reason = failure_reason


def _iter_payload_items(
    payload: dict[str, Any],
    key: str,
) -> list[dict[str, Any]]:
    """Return object items from a structured AI payload list field."""
    raw_items = payload.get(key, [])
    if not isinstance(raw_items, list):
        return []
    return [item for item in raw_items if isinstance(item, dict)]


def _detect_unsupported_structured_claims(
    ctx: SymbolContext,
    payload: dict[str, Any],
) -> list[str]:
    """Return structured AI claims that are not grounded in context."""
    issues: list[str] = []

    valid_params = {param.name for param in ctx.parameters}
    for item in _iter_payload_items(payload, "parameters"):
        name = str(item.get("name", "")).lstrip("*").strip()
        if name and name not in valid_params:
            issues.append("unsupported parameter: " + name)

    valid_raises = set(ctx.raises_types)
    for item in _iter_payload_items(payload, "raises"):
        name = str(item.get("type", "")).strip()
        if name and name not in valid_raises:
            issues.append("unsupported raise: " + name)

    valid_attrs = {attr.name for attr in ctx.class_attributes}
    for item in _iter_payload_items(payload, "attributes"):
        name = str(item.get("name", "")).strip()
        if name and name not in valid_attrs:
            issues.append("unsupported attribute: " + name)

    return issues


_LOW_INFORMATION_SUMMARY_PREFIXES = (
    "describe ",
    "document ",
    "todo",
)

_LOW_INFORMATION_SUMMARY_VALUES = {
    "docstring",
    "documentation",
    "function",
    "method",
    "class",
    "module",
    "object",
    "value",
}


def _first_docstring_line(body: str) -> str:
    """Return the first non-empty rendered docstring line."""
    for line in body.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _normalized_summary_key(summary: str) -> str:
    """Return a lowercase summary key without terminal punctuation."""
    return summary.strip().lower().rstrip(".!?:; ")


def _detect_low_information_docstring(
    ctx: SymbolContext,
    body: str,
) -> list[str]:
    """Return evidence-bound quality issues in a rendered docstring."""
    issues: list[str] = []
    summary = _first_docstring_line(body)
    summary_key = _normalized_summary_key(summary)

    if not summary:
        issues.append("missing summary")
    elif summary_key in _LOW_INFORMATION_SUMMARY_VALUES:
        issues.append("low-information summary: " + summary)
    elif any(
        summary_key.startswith(prefix)
        for prefix in _LOW_INFORMATION_SUMMARY_PREFIXES
    ):
        issues.append("low-information summary: " + summary)
    elif (
        len(summary_key.split()) < 3
        and ctx.kind in {"module", "class", "function", "method"}
    ):
        issues.append("too-short summary: " + summary)

    if "TODO:" in body:
        issues.append("contains TODO placeholder")

    return issues
