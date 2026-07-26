# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_json_response.py
"""Bounded JSON extraction for local-AI Planner responses."""

from __future__ import annotations

import json
import re
from typing import Any

__all__ = [
    "LocalAIJSONResponseError",
    "parse_local_ai_json_object",
]

_MAX_NESTED_STRING_PASSES = 2
_MAX_PREFIX_DIAGNOSTIC = 160
_FENCE_PATTERN = re.compile(
    r"```(?:json|javascript|js)?\s*(.*?)```",
    flags=re.IGNORECASE | re.DOTALL,
)


class LocalAIJSONResponseError(ValueError):
    """Raised when a local-AI response contains no valid JSON object."""


def parse_local_ai_json_object(
    raw_response: Any,
    *,
    context: str = "Local AI response",
) -> dict[str, Any]:
    """Return the first valid JSON object from one bounded model response.

    Accepted transport wrappers include direct JSON, Markdown JSON fences,
    marker-wrapped JSON, short prose prefixes/suffixes, and reasoning wrappers.
    The returned object is still subject to the caller's strict schema checks.
    """

    if isinstance(raw_response, dict):
        return dict(raw_response)
    text = _normalize_text(raw_response)
    if not text:
        raise LocalAIJSONResponseError(context + " is empty.")

    candidates = [text]
    candidates.extend(match.strip() for match in _FENCE_PATTERN.findall(text))
    seen: set[str] = set()
    for candidate in candidates:
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        parsed = _parse_candidate(candidate)
        if isinstance(parsed, dict):
            return parsed

    for candidate in _balanced_json_object_candidates(text):
        if candidate in seen:
            continue
        seen.add(candidate)
        parsed = _parse_candidate(candidate)
        if isinstance(parsed, dict):
            return parsed

    raise LocalAIJSONResponseError(_diagnostic_message(context, text))


def _normalize_text(raw_response: Any) -> str:
    """Normalize one response to stripped Unicode text."""

    return str(raw_response or "").lstrip("\ufeff").strip()


def _parse_candidate(candidate: str) -> Any:
    """Parse JSON and unwrap a bounded number of JSON-encoded strings."""

    current: Any = candidate
    for _pass in range(_MAX_NESTED_STRING_PASSES + 1):
        if not isinstance(current, str):
            return current
        try:
            parsed = json.loads(current)
        except json.JSONDecodeError:
            return None
        current = parsed
    return current


def _balanced_json_object_candidates(text: str) -> list[str]:
    """Return balanced top-level object substrings while respecting strings."""

    results: list[str] = []
    start: int | None = None
    depth = 0
    in_string = False
    escaped = False

    for index, char in enumerate(text):
        if start is None:
            if char == "{":
                start = index
                depth = 1
                in_string = False
                escaped = False
            continue

        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue
        if char == "{":
            depth += 1
            continue
        if char == "}":
            depth -= 1
            if depth == 0:
                results.append(text[start : index + 1])
                start = None

    return results


def _diagnostic_message(context: str, text: str) -> str:
    """Return a safe compact diagnostic without echoing the full response."""

    prefix = text[:_MAX_PREFIX_DIAGNOSTIC]
    prefix = prefix.replace("\r", "\\r").replace("\n", "\\n")
    return (
        context
        + " does not contain a valid JSON object. response_length="
        + str(len(text))
        + "; prefix="
        + repr(prefix)
    )
