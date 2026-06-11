"""
Text normalization helpers for the Reasoner Engine help index.

The source help payload contains a few repeated mojibake fragments from earlier
copy/paste or encoding conversions. Normalizing them here keeps the raw content
stable while improving UI text quality.
"""

from __future__ import annotations

__all__ = [
    "normalize_help_text",
    "normalize_help_payload",
]

from typing import Any

_COMMON_REPLACEMENTS: dict[str, str] = {
    "\u00c3\u0192\u00c6\u2019\u00c3\u201a\u00c2\u00a2\u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u201a\u00ac\u00c5\u00a1\u00c3\u201a\u00c2\u00ac\u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u201a\u00c2\u009d": "\u00e2\u20ac\u201d",
    "\u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u00a2\u00e2\u201a\u00ac\u00c5\u201c": "\u00e2\u20ac\u201c",
    "\u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u00a2\u00e2\u20ac\u017e\u00c2\u00a2": "\u00e2\u20ac\u2122",
    "\u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u2026\u00e2\u20ac\u0153": "\u00e2\u20ac\u0153",
    "\u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u201a\u00c2\u009d": "\u00e2\u20ac\u009d",
    "\u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u201a\u00c2\u00a2": "\u00e2\u20ac\u00a2",
    "\u00c3\u0192\u00c2\u00a2\u00c3\u00a2\u00e2\u20ac\u0161\u00c2\u00ac\u00c3\u201a\u00c2\u00a6": "\u00e2\u20ac\u00a6",
}


def normalize_help_text(value: str) -> str:
    text = value
    for old, new in _COMMON_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


def normalize_help_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize_help_payload(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_help_payload(item) for item in value]
    if isinstance(value, str):
        return normalize_help_text(value)
    return value
