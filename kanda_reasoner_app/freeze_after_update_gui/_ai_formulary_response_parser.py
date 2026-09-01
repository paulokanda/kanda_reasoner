# project-path: kanda_reasoner_app/freeze_after_update_gui/_ai_formulary_response_parser.py
"""Fail-closed parser for AI-returned local Freeze formulary JSON."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping

__all__ = [
    "ParsedAIFormulary",
    "canonical_formulary_json_schema",
    "canonical_formulary_payload",
    "parse_ai_formulary_response",
]

_FIELDS = (
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
)
_LIST_FIELDS = {
    "validated_files",
    "generated_files",
    "protected_paths",
    "do_not_regress_rules",
    "validation_evidence_summary",
}


@dataclass(frozen=True, slots=True)
class ParsedAIFormulary:
    """Strictly parsed AI formulary represented as widget-ready text."""

    inputs: dict[str, str]
    ignored_fields: list[str]


def _reject_constant(value: str) -> None:
    raise ValueError("Non-standard JSON constant is not allowed: " + value)


def _pairs_to_unique_dict(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key is not allowed: " + key)
        result[key] = value
    return result


def _decoder() -> json.JSONDecoder:
    return json.JSONDecoder(
        object_pairs_hook=_pairs_to_unique_dict,
        parse_constant=_reject_constant,
    )


def _validate_field_inventory(payload: Mapping[str, Any]) -> None:
    expected = set(_FIELDS)
    actual = set(payload)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        raise ValueError("Freeze formulary missing field(s): " + ", ".join(missing))
    if extra:
        raise ValueError("Freeze formulary unknown field(s): " + ", ".join(extra))


def _list_items(value: Any) -> list[str]:
    if isinstance(value, list):
        if not all(isinstance(item, str) for item in value):
            raise ValueError("Freeze formulary arrays must contain strings only.")
        return [item for item in value if item.strip()]
    if isinstance(value, str):
        return [line for line in value.splitlines() if line.strip()]
    raise ValueError("Freeze formulary multiline fields must be arrays or strings.")


def canonical_formulary_payload(inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Return the single canonical 11-field Freeze transport payload."""
    payload: dict[str, Any] = {}
    for field in _FIELDS:
        value = inputs.get(field, "")
        if field in _LIST_FIELDS:
            payload[field] = _list_items(value)
            continue
        if not isinstance(value, str):
            value = str(value or "")
        payload[field] = value
    return payload


def canonical_formulary_json_schema() -> dict[str, Any]:
    """Return the strict JSON schema used by every Freeze AI producer."""
    properties: dict[str, Any] = {}
    for field in _FIELDS:
        if field in _LIST_FIELDS:
            properties[field] = {
                "type": "array",
                "items": {"type": "string"},
            }
        else:
            properties[field] = {"type": "string"}
    return {
        "type": "object",
        "properties": properties,
        "required": list(_FIELDS),
        "additionalProperties": False,
    }


def _payload_to_text(payload: Mapping[str, Any]) -> dict[str, str]:
    _validate_field_inventory(payload)
    converted: dict[str, str] = {}
    for field in _FIELDS:
        value = payload[field]
        if field in _LIST_FIELDS:
            converted[field] = "\n".join(_list_items(value))
            continue
        if not isinstance(value, str):
            raise ValueError(field + " must be a JSON string.")
        converted[field] = value
    return converted


def _decoded_objects(text: str) -> list[dict[str, Any]]:
    """Decode all top-level JSON objects discoverable in arbitrary response text."""
    decoder = _decoder()
    objects: list[dict[str, Any]] = []
    seen_spans: set[tuple[int, int]] = set()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            payload, end_index = decoder.raw_decode(text, index)
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(payload, dict):
            continue
        span = (index, end_index)
        if span in seen_spans:
            continue
        seen_spans.add(span)
        objects.append(payload)
    return objects


def _candidate_is_valid(payload: Mapping[str, Any]) -> bool:
    try:
        _payload_to_text(payload)
    except (TypeError, ValueError):
        return False
    return True


def _extract_single_freeze_payload(text: str) -> dict[str, Any]:
    normalized = str(text or "").strip()
    if not normalized:
        raise ValueError("Freeze formulary response is empty.")

    # Preserve precise errors for the common raw-JSON path.
    if normalized.startswith("{"):
        try:
            payload, end_index = _decoder().raw_decode(normalized)
        except (json.JSONDecodeError, ValueError):
            payload = None
        else:
            if isinstance(payload, dict) and not normalized[end_index:].strip():
                _payload_to_text(payload)
                return payload

    objects = _decoded_objects(normalized)
    valid = [payload for payload in objects if _candidate_is_valid(payload)]
    if len(valid) == 1:
        return valid[0]
    if len(valid) > 1:
        raise ValueError(
            "Freeze response is ambiguous: more than one valid 11-field JSON object was found."
        )
    if len(objects) == 1:
        # Surface the exact schema/type defect when there is one unambiguous object.
        _payload_to_text(objects[0])
    raise ValueError(
        "Freeze response must contain exactly one valid 11-field JSON object."
    )


def parse_ai_formulary_response(
    text: str,
    current_inputs: dict[str, Any] | None = None,
    *,
    transport: str | None = None,
) -> ParsedAIFormulary:
    """Parse one Freeze response using the unified schema-driven receiver.

    ``transport`` remains accepted only for backward compatibility with existing
    callers. The receiver no longer changes behavior based on response origin.
    Legacy marker/fence envelopes are tolerated as surrounding text when they
    contain exactly one valid Freeze object.
    """

    del current_inputs, transport
    payload = _extract_single_freeze_payload(str(text or ""))
    return ParsedAIFormulary(inputs=_payload_to_text(payload), ignored_fields=[])
