# project-path: kanda_reasoner_app/freeze_after_update_gui/_ai_formulary_response_parser.py
"""Tolerant parser for AI-returned local freeze formulary JSON."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_transport_repair import (
    payload_has_suspicious_windows_control_damage,
    transport_repair_variants,
)

__all__ = ["ParsedAIFormulary", "parse_ai_formulary_response"]

_START_MARKER = "KANDA_FREEZE_FORM_JSON_BEGIN"
_END_MARKER = "KANDA_FREEZE_FORM_JSON_END"
_ALLOWED_KEYS = {
    "feature_title",
    "primary_box",
    "box_type",
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
    "known_warnings",
    "planned_next_step",
    "notes",
}


@dataclass(frozen=True)
class ParsedAIFormulary:
    """Parsed AI formulary payload plus ignored unknown fields."""

    inputs: dict
    ignored_fields: list[str]


def _normalize_ai_text(raw_text: str) -> str:
    """Support normalize ai text behavior.
    
    Parameters
    ----------
    raw_text : str
        The raw text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return (
        (raw_text or "")
        .replace("\ufeff", "")
        .replace("\u200b", "")
        .replace("\u200c", "")
        .replace("\u200d", "")
        .replace("\xa0", " ")
        .strip()
    )


def _strip_markdown_fences(raw_text: str) -> str:
    """Support strip markdown fences behavior.
    
    Parameters
    ----------
    raw_text : str
        The raw text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    stripped = _normalize_ai_text(raw_text)
    if not stripped.startswith("```"):
        return stripped
    lines = stripped.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _remove_trailing_commas(raw_text: str) -> str:
    """Support remove trailing commas behavior.
    
    Parameters
    ----------
    raw_text : str
        The raw text value.
    
    Returns
    -------
    str
        The string result.
    """
    
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


def _normalize_common_ai_markdown_damage(value: str) -> str:
    """Support normalize common ai markdown damage behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return value.replace("**init**.py", "__init__.py")


def _extract_balanced_json_objects(raw_text: str) -> list[str]:
    """Return every balanced JSON object from arbitrary pasted AI text."""
    candidate = _normalize_ai_text(raw_text)
    objects: list[str] = []
    length = len(candidate)
    index = 0
    while index < length:
        if candidate[index] != "{":
            index += 1
            continue
        in_string = False
        escaped = False
        depth = 0
        end_index: int | None = None
        cursor = index
        while cursor < length:
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
        if end_index is not None:
            objects.append(candidate[index:end_index].strip())
            index = end_index
        else:
            index += 1
    return objects


def _collect_candidate_blocks(raw_text: str) -> list[str]:
    """Collect marker payloads, fenced JSON, full objects, and form-object fallbacks."""
    normalized = _normalize_ai_text(raw_text)
    blocks: list[str] = []
    if _START_MARKER in normalized and _END_MARKER in normalized:
        marker_payload = normalized.split(_START_MARKER, 1)[1].split(_END_MARKER, 1)[0].strip()
        blocks.append(marker_payload)
    for fence_part in normalized.split("```"):
        block = _strip_markdown_fences(fence_part)
        if block.lower().startswith("json"):
            block = block[4:].strip()
        if "{" in block and "}" in block:
            blocks.append(block)
    blocks.extend(_extract_balanced_json_objects(normalized))
    for key in ['"feature_title"', "'feature_title'"]:
        key_index = normalized.rfind(key)
        if key_index >= 0:
            left = normalized.rfind("{", 0, key_index)
            right = normalized.find("}", key_index)
            if left >= 0 and right > left:
                blocks.append(normalized[left : right + 1])
    first_brace = normalized.find("{")
    last_brace = normalized.rfind("}")
    if first_brace >= 0 and last_brace > first_brace:
        blocks.append(normalized[first_brace : last_brace + 1])
    unique: list[str] = []
    seen: set[str] = set()
    for block in blocks:
        cleaned_block = _strip_markdown_fences(block).strip()
        if not cleaned_block or cleaned_block in seen:
            continue
        seen.add(cleaned_block)
        unique.append(cleaned_block)
    return unique


def _json_load_attempts(raw_block: str) -> dict | None:
    """Try strict and transport-repaired JSON parsing for one candidate block."""
    variants: list[str] = []
    base = _strip_markdown_fences(raw_block)

    def add_variants(candidate_text: str) -> None:
        repaired_controls = _escape_raw_control_chars_inside_strings(candidate_text)
        variants.extend((candidate_text, repaired_controls))
        variants.extend(transport_repair_variants(candidate_text))
        variants.extend(transport_repair_variants(repaired_controls))

    add_variants(base)
    for obj in _extract_balanced_json_objects(base):
        add_variants(obj)
    attempted: set[str] = set()
    for variant in variants:
        candidate = _remove_trailing_commas(variant).strip()
        if not candidate or candidate in attempted:
            continue
        attempted.add(candidate)
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if (
            isinstance(payload, dict)
            and not payload_has_suspicious_windows_control_damage(payload)
        ):
            return payload
    return None


def _payload_score(payload: dict) -> tuple[int, int, int]:
    """Support payload score behavior.
    
    Parameters
    ----------
    payload : dict
        The payload value.
    
    Returns
    -------
    tuple[int, int, int]
        The tuple of values.
    """
    
    present_keys = sum((1 for key in _ALLOWED_KEYS if key in payload))
    meaningful_chars = 0
    placeholder_penalty = 0
    for key in _ALLOWED_KEYS:
        value = payload.get(key)
        if value is None:
            continue
        text_value = str(value)
        meaningful_chars += len(text_value.strip())
        if "..." in text_value or "one project-relative path" in text_value:
            placeholder_penalty += 1
    return (present_keys, meaningful_chars, -placeholder_penalty)


def parse_ai_formulary_response(text: str, current_inputs: dict[str, Any]) -> ParsedAIFormulary:
    """Parse AI formulary answers with a forgiving multi-candidate extractor."""
    parsed_payloads: list[dict] = []
    for block in _collect_candidate_blocks(text):
        payload = _json_load_attempts(block)
        if payload is not None:
            parsed_payloads.append(payload)
    if not parsed_payloads:
        raise ValueError(
            "Could not find a usable freeze-form JSON object in the AI answer. "
            "The receiver searched marker payloads, fenced JSON, balanced JSON objects, "
            "broad fallback slices, and transport repairs. For Windows paths, paste the "
            "marker block with its JSON inside a fenced code block or use \\u005C for "
            "backslashes."
        )
    payload = max(parsed_payloads, key=_payload_score)
    if not isinstance(payload, dict):
        raise ValueError("AI response JSON must be an object.")
    cleaned = dict(current_inputs)
    ignored = sorted((str(key) for key in payload.keys() if key not in _ALLOWED_KEYS))
    for key in _ALLOWED_KEYS:
        if key not in payload:
            continue
        value = payload[key]
        if isinstance(value, list):
            cleaned[key] = "\n".join(
                (_normalize_common_ai_markdown_damage(str(item).strip()) for item in value if str(item).strip())
            )
        elif isinstance(value, dict):
            cleaned[key] = json.dumps(value, ensure_ascii=False, indent=2)
        elif value is None:
            cleaned[key] = ""
        else:
            cleaned[key] = _normalize_common_ai_markdown_damage(str(value))
    return ParsedAIFormulary(inputs=cleaned, ignored_fields=ignored)
