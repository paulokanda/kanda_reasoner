"""JSON recovery and parser helpers for Error Memory AI intake."""

from __future__ import annotations

__all__: list[str] = []


import json
from typing import Any, Mapping

from .intake_normalization import (
    ALLOWED_ERROR_LESSON_FORM_KEYS,
    ERROR_LESSON_JSON_BEGIN,
    ERROR_LESSON_JSON_END,
    _REQUIRED_ACTIVE_AI_KEYS,
    _as_list,
    _as_text,
    _coerce_status_for_ai_form,
)
from .intake_plain_text import _plain_text_to_form


def _normalize_ai_text(raw_text: str) -> str:
    return (
        str(raw_text or "")
        .replace("\ufeff", "")
        .replace("\u200b", "")
        .replace("\u200c", "")
        .replace("\u200d", "")
        .replace("\u00a0", " ")
        .strip()
    )


def _strip_markdown_fences(raw_text: str) -> str:
    stripped = _normalize_ai_text(raw_text)
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    result = "\n".join(lines).strip()
    if result.lower().startswith("json"):
        result = result[4:].strip()
    return result


def _remove_trailing_commas(raw_text: str) -> str:
    text_work = raw_text
    previous = None
    while previous != text_work:
        previous = text_work
        text_work = text_work.replace(",\n}", "\n}").replace(",\r\n}", "\r\n}")
        text_work = text_work.replace(", }", " }").replace(",}", "}")
        text_work = text_work.replace(",\n]", "\n]").replace(",\r\n]", "\r\n]")
        text_work = text_work.replace(", ]", " ]").replace(",]", "]")
    return text_work


def _escape_raw_control_chars_inside_strings(raw_text: str) -> str:
    """Repair real newlines/tabs pasted inside JSON string values."""
    repaired: list[str] = []
    in_string = False
    escaped = False
    for char in raw_text:
        if in_string:
            if escaped:
                repaired.append(char)
                escaped = False
                continue
            if char == "\\":
                repaired.append(char)
                escaped = True
                continue
            if char == '"':
                repaired.append(char)
                in_string = False
                continue
            if char == "\n":
                repaired.append("\\n")
                continue
            if char == "\r":
                continue
            if char == "\t":
                repaired.append("\\t")
                continue
            repaired.append(char)
            continue
        repaired.append(char)
        if char == '"':
            in_string = True
    return "".join(repaired)


def _extract_balanced_json_objects(raw_text: str) -> list[str]:
    candidate = _normalize_ai_text(raw_text)
    objects: list[str] = []
    index = 0
    while index < len(candidate):
        if candidate[index] != "{":
            index += 1
            continue
        in_string = False
        escaped = False
        depth = 0
        cursor = index
        end_index: int | None = None
        while cursor < len(candidate):
            char = candidate[cursor]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                cursor += 1
                continue
            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    end_index = cursor + 1
                    break
            cursor += 1
        if end_index is None:
            index += 1
        else:
            objects.append(candidate[index:end_index].strip())
            index = end_index
    return objects


def _candidate_blocks(raw_text: str) -> list[str]:
    normalized = _normalize_ai_text(raw_text)
    blocks: list[str] = []
    if ERROR_LESSON_JSON_BEGIN in normalized and ERROR_LESSON_JSON_END in normalized:
        blocks.append(normalized.split(ERROR_LESSON_JSON_BEGIN, 1)[1].split(ERROR_LESSON_JSON_END, 1)[0].strip())
    for fence_part in normalized.split("```"):
        block = _strip_markdown_fences(fence_part)
        if "{" in block and "}" in block:
            blocks.append(block)
    blocks.extend(_extract_balanced_json_objects(normalized))
    first = normalized.find("{")
    last = normalized.rfind("}")
    if first >= 0 and last > first:
        blocks.append(normalized[first : last + 1])
    unique: list[str] = []
    seen: set[str] = set()
    for block in blocks:
        cleaned = _strip_markdown_fences(block).strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            unique.append(cleaned)
    return unique


def _json_load_attempts(raw_block: str) -> dict[str, Any] | None:
    variants: list[str] = []
    base = _strip_markdown_fences(raw_block)
    variants.append(base)
    variants.append(_remove_trailing_commas(base))
    variants.append(_remove_trailing_commas(_escape_raw_control_chars_inside_strings(base)))
    for obj in _extract_balanced_json_objects(base):
        variants.append(obj)
        variants.append(_remove_trailing_commas(obj))
        variants.append(_remove_trailing_commas(_escape_raw_control_chars_inside_strings(obj)))
    attempted: set[str] = set()
    for variant in variants:
        candidate = variant.strip()
        if not candidate or candidate in attempted:
            continue
        attempted.add(candidate)
        try:
            loaded = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(loaded, dict):
            return loaded
    return None


def _payload_score(payload: Mapping[str, Any]) -> tuple[int, int, int]:
    present_keys = sum(1 for key in ALLOWED_ERROR_LESSON_FORM_KEYS if key in payload)
    required_present = sum(1 for key in _REQUIRED_ACTIVE_AI_KEYS if str(payload.get(key, "")).strip())
    meaningful_chars = sum(len(str(payload.get(key, "")).strip()) for key in ALLOWED_ERROR_LESSON_FORM_KEYS)
    return (required_present, present_keys, meaningful_chars)


def parse_error_lesson_ai_response(text: str) -> dict[str, Any]:
    """Parse an AI Error Lesson formulary answer into clean form inputs."""
    parsed: list[dict[str, Any]] = []
    for block in _candidate_blocks(text):
        payload = _json_load_attempts(block)
        if payload is not None:
            parsed.append(payload)
    if not parsed:
        return _plain_text_to_form(text)
    payload = max(parsed, key=_payload_score)
    cleaned: dict[str, Any] = {}
    for key in ALLOWED_ERROR_LESSON_FORM_KEYS:
        if key not in payload:
            continue
        value = payload.get(key)
        if key in {"prevention_triggers", "validation_evidence"}:
            cleaned[key] = _as_list(value)
        elif key in {"regression_check", "exception", "fingerprint", "redaction"} and isinstance(value, dict):
            cleaned[key] = dict(value)
        else:
            cleaned[key] = _as_text(value)
    cleaned["status"] = _coerce_status_for_ai_form(cleaned, str(cleaned.get("status") or "active"))
    return cleaned
