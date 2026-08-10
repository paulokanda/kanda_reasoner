# project-path: kanda_reasoner_app/freeze_after_update_gui/_ai_formulary_transport_repair.py
"""Conservative transport repairs for pasted Freeze-form JSON."""
from __future__ import annotations

import re
from typing import Any

__all__ = [
    "payload_has_suspicious_windows_control_damage",
    "transport_repair_variants",
]

_VALID_SIMPLE_JSON_ESCAPES = frozenset('"\\/bfnrt')
_HEX_DIGITS = frozenset("0123456789abcdefABCDEF")
_WINDOWS_DRIVE_IN_TEXT = re.compile(r"(?:^|[^A-Za-z0-9])[A-Za-z]:")
_WINDOWS_DRIVE_PREFIX = re.compile(r"(?:^|[^A-Za-z0-9])[A-Za-z]:$")
_VALIDATION_LINE_AFTER_ESCAPE = re.compile(r"[A-Z][A-Z0-9 _./()\-]{2,}:")


def _repair_invalid_json_escapes_inside_strings(raw_text: str) -> str:
    """Double invalid single backslashes without changing valid JSON escapes."""
    repaired: list[str] = []
    in_string = False
    index = 0
    while index < len(raw_text):
        char = raw_text[index]
        if not in_string:
            repaired.append(char)
            if char == '"':
                in_string = True
            index += 1
            continue
        if char == '"':
            repaired.append(char)
            in_string = False
            index += 1
            continue
        if char != "\\":
            repaired.append(char)
            index += 1
            continue
        if index + 1 >= len(raw_text):
            repaired.append("\\\\")
            index += 1
            continue
        next_char = raw_text[index + 1]
        if next_char in _VALID_SIMPLE_JSON_ESCAPES:
            repaired.extend((char, next_char))
            index += 2
            continue
        if (
            next_char == "u"
            and index + 5 < len(raw_text)
            and all(item in _HEX_DIGITS for item in raw_text[index + 2 : index + 6])
        ):
            repaired.append(raw_text[index : index + 6])
            index += 6
            continue
        repaired.append("\\\\")
        index += 1
    return "".join(repaired)


def _looks_like_multiline_separator(raw_text: str, slash_index: int) -> bool:
    """Return whether one ``\\n`` after a path starts a new validation line."""
    if raw_text[slash_index : slash_index + 2] != "\\n":
        return False
    following = raw_text[slash_index + 2 : slash_index + 110]
    return bool(_VALIDATION_LINE_AFTER_ESCAPE.match(following))


def _repair_windows_drive_backslashes_inside_strings(raw_text: str) -> str:
    """Repair Markdown-collapsed backslashes after a Windows drive prefix."""
    repaired: list[str] = []
    in_string = False
    path_mode = False
    string_tail = ""
    index = 0
    while index < len(raw_text):
        char = raw_text[index]
        if not in_string:
            repaired.append(char)
            if char == '"':
                in_string = True
                path_mode = False
                string_tail = ""
            index += 1
            continue
        if char == '"':
            repaired.append(char)
            in_string = False
            path_mode = False
            string_tail = ""
            index += 1
            continue
        if char != "\\":
            repaired.append(char)
            string_tail = (string_tail + char)[-120:]
            index += 1
            continue
        if not path_mode and _WINDOWS_DRIVE_PREFIX.search(string_tail):
            path_mode = True
        if not path_mode:
            if index + 1 < len(raw_text):
                repaired.append(raw_text[index : index + 2])
                string_tail = (string_tail + raw_text[index + 1])[-120:]
                index += 2
            else:
                repaired.append("\\\\")
                index += 1
            continue
        if raw_text[index : index + 2] == "\\\\":
            repaired.append("\\\\")
            string_tail = (string_tail + "\\")[-120:]
            index += 2
            continue
        unicode_escape = raw_text[index : index + 6]
        if len(unicode_escape) == 6 and unicode_escape.lower() == "\\u005c":
            repaired.append(unicode_escape)
            string_tail = (string_tail + "\\")[-120:]
            index += 6
            continue
        if _looks_like_multiline_separator(raw_text, index):
            repaired.append("\\n")
            path_mode = False
            string_tail = ""
            index += 2
            continue
        repaired.append("\\\\")
        string_tail = (string_tail + "\\")[-120:]
        index += 1
    return "".join(repaired)


def transport_repair_variants(raw_text: str) -> list[str]:
    """Return deterministic repair variants for one candidate JSON block."""
    invalid_escapes = _repair_invalid_json_escapes_inside_strings(raw_text)
    windows_paths = _repair_windows_drive_backslashes_inside_strings(raw_text)
    return [
        invalid_escapes,
        windows_paths,
        _repair_invalid_json_escapes_inside_strings(windows_paths),
    ]


def _payload_strings(value: Any) -> list[str]:
    """Collect nested string values for transport-corruption checks."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for nested in value.values():
            strings.extend(_payload_strings(nested))
        return strings
    if isinstance(value, list):
        strings = []
        for nested in value:
            strings.extend(_payload_strings(nested))
        return strings
    return []


def _string_has_suspicious_windows_control_damage(value: str) -> bool:
    """Detect controls that appear inside one decoded Windows path span."""
    for drive_match in _WINDOWS_DRIVE_IN_TEXT.finditer(value):
        tail = value[drive_match.end() :]
        for index, char in enumerate(tail):
            if char not in "\b\f\n\r\t":
                continue
            following = tail[index + 1 : index + 110]
            first_line = following.splitlines()[0] if following else ""
            if char == "\n" and first_line and all(
                item.isupper() or item.isdigit() or item in " _./()-:"
                for item in first_line
            ):
                continue
            return True
    return False


def payload_has_suspicious_windows_control_damage(payload: dict) -> bool:
    """Reject JSON that decoded a pasted Windows path into control characters."""
    return any(
        _string_has_suspicious_windows_control_damage(value)
        for value in _payload_strings(payload)
    )
