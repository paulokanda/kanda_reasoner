# project-path: kanda_reasoner_app/reasoner_engine/
# project_web_ai_complete_json_sections.py
"""Read approved top-level sections from one verified complete-JSON file."""

from __future__ import annotations

import hashlib
import json
import mmap
from pathlib import Path
from typing import Iterable, Mapping

__all__ = [
    "APPROVED_COMPLETE_JSON_SECTIONS",
    "SmartCompleteJsonReadError",
    "complete_json_section_fingerprint",
    "extract_complete_json_sections",
]

MAX_SECTION_BYTES = 48 * 1024 * 1024
MAX_TOTAL_SECTION_BYTES = 128 * 1024 * 1024
APPROVED_COMPLETE_JSON_SECTIONS = (
    "web_ai_symbol_index",
    "primary_definition_index",
    "entry_points_detail",
    "web_ai_file_responsibility_index",
    "web_ai_test_protection_index",
    "stable_evidence_id_index",
)


class SmartCompleteJsonReadError(RuntimeError):
    """Raised when approved generated evidence cannot be read safely."""


def _scan_string_end(data: mmap.mmap, start: int) -> int:
    if start >= len(data) or data[start] != 34:
        raise SmartCompleteJsonReadError("SMART_CONTEXT_JSON_STRING_EXPECTED")
    escaped = False
    index = start + 1
    while index < len(data):
        value = data[index]
        if escaped:
            escaped = False
        elif value == 92:
            escaped = True
        elif value == 34:
            return index + 1
        index += 1
    raise SmartCompleteJsonReadError("SMART_CONTEXT_JSON_STRING_UNTERMINATED")


def _skip_space(data: mmap.mmap, index: int) -> int:
    while index < len(data) and data[index] in b" \t\r\n":
        index += 1
    return index


def _scan_value_end(data: mmap.mmap, start: int) -> int:
    start = _skip_space(data, start)
    if start >= len(data):
        raise SmartCompleteJsonReadError("SMART_CONTEXT_JSON_VALUE_MISSING")
    first = data[start]
    if first == 34:
        return _scan_string_end(data, start)
    if first not in (91, 123):
        index = start
        while index < len(data) and data[index] not in b",}]\r\n\t ":
            index += 1
        return index

    stack = [first]
    in_string = False
    escaped = False
    index = start + 1
    while index < len(data):
        value = data[index]
        if in_string:
            if escaped:
                escaped = False
            elif value == 92:
                escaped = True
            elif value == 34:
                in_string = False
        elif value == 34:
            in_string = True
        elif value in (91, 123):
            stack.append(value)
        elif value in (93, 125):
            expected = 91 if value == 93 else 123
            if not stack or stack[-1] != expected:
                raise SmartCompleteJsonReadError(
                    "SMART_CONTEXT_JSON_BRACKET_MISMATCH"
                )
            stack.pop()
            if not stack:
                return index + 1
        index += 1
    raise SmartCompleteJsonReadError("SMART_CONTEXT_JSON_VALUE_UNTERMINATED")


def _section_candidates(data: mmap.mmap, name: str) -> Iterable[tuple[int, int]]:
    needle = (json.dumps(name, ensure_ascii=True) + ":").encode("ascii")
    offset = 0
    while True:
        found = data.find(needle, offset)
        if found < 0:
            return
        start = found + len(needle)
        try:
            end = _scan_value_end(data, start)
        except SmartCompleteJsonReadError:
            offset = found + 1
            continue
        yield _skip_space(data, start), end
        offset = found + len(needle)


def extract_complete_json_sections(path: str | Path) -> dict[str, object]:
    """Extract the largest valid occurrence of every approved section."""
    source = Path(path)
    if not source.is_file():
        raise SmartCompleteJsonReadError("SMART_CONTEXT_COMPLETE_JSON_MISSING")
    if source.stat().st_size == 0:
        raise SmartCompleteJsonReadError("SMART_CONTEXT_COMPLETE_JSON_EMPTY")

    selected: dict[str, object] = {}
    total = 0
    with source.open("rb") as handle:
        with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as data:
            for name in APPROVED_COMPLETE_JSON_SECTIONS:
                best: tuple[int, int] | None = None
                for start, end in _section_candidates(data, name):
                    size = end - start
                    if size <= 0 or size > MAX_SECTION_BYTES:
                        continue
                    if best is None or size > best[1] - best[0]:
                        best = (start, end)
                if best is None:
                    needle = (json.dumps(name, ensure_ascii=True) + ":").encode(
                        "ascii"
                    )
                    if data.find(needle) >= 0:
                        raise SmartCompleteJsonReadError(
                            "SMART_CONTEXT_SECTION_MALFORMED:" + name
                        )
                    continue
                raw = bytes(data[best[0] : best[1]])
                try:
                    value = json.loads(raw.decode("utf-8", errors="strict"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise SmartCompleteJsonReadError(
                        "SMART_CONTEXT_SECTION_MALFORMED:" + name
                    ) from exc
                if not isinstance(value, (dict, list)):
                    continue
                total += len(raw)
                if total > MAX_TOTAL_SECTION_BYTES:
                    raise SmartCompleteJsonReadError(
                        "SMART_CONTEXT_SECTION_READ_BUDGET_EXCEEDED"
                    )
                selected[name] = value
    return selected


def complete_json_section_fingerprint(
    path: str | Path,
    sections: Mapping[str, object],
) -> str:
    """Bind routed evidence to file stat and extracted section content."""
    source = Path(path)
    stat = source.stat()
    digest = hashlib.sha256()
    digest.update(str(stat.st_size).encode("ascii"))
    digest.update(str(stat.st_mtime_ns).encode("ascii"))
    for name in APPROVED_COMPLETE_JSON_SECTIONS:
        if name not in sections:
            continue
        digest.update(name.encode("ascii"))
        digest.update(
            json.dumps(
                sections[name],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
    return digest.hexdigest()
