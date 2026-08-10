# project-path: kanda_reasoner_app/reasoner_symbol_atlas/json_active_scope_quality_helpers_private.py
"""Private scanner helpers for complete JSON active-scope quality."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .complete_json_adapter import resolve_reasoner_symbol_atlas_complete_json_path

__all__: list[str] = []


@dataclass(frozen=True)
class _RawJsonActiveScopeOccurrence:
    json_location: str
    occurrence_type: str
    marker: str
    value_excerpt: str = ""


@dataclass(frozen=True)
class _JsonActiveScopeScanResult:
    active_path_occurrence_count: int = 0
    text_occurrence_count: int = 0
    key_occurrence_count: int = 0
    checked_value_count: int = 0
    active_occurrences: tuple[_RawJsonActiveScopeOccurrence, ...] = field(default_factory=tuple)
    text_occurrences: tuple[_RawJsonActiveScopeOccurrence, ...] = field(default_factory=tuple)


def _select_json_path(project_root: Path, json_path: str) -> Path | None:
    return resolve_reasoner_symbol_atlas_complete_json_path(
        project_root,
        json_path or None,
    )


def _scan_json_active_scope_payload(
    payload: Any,
    max_items: int,
    active_path_field_names: frozenset[str],
    active_path_sections: frozenset[str],
    truth_text_field_names: frozenset[str],
    inactive_text_markers: tuple[str, ...],
) -> _JsonActiveScopeScanResult:
    scanner = _QualityScanner(
        max_items=max_items,
        active_path_field_names=active_path_field_names,
        active_path_sections=active_path_sections,
        truth_text_field_names=truth_text_field_names,
        inactive_text_markers=inactive_text_markers,
    )
    scanner.scan(payload)
    return scanner.result()


class _QualityScanner:
    """Internal recursive scanner for complete JSON payloads."""

    def __init__(
        self,
        max_items: int,
        active_path_field_names: frozenset[str],
        active_path_sections: frozenset[str],
        truth_text_field_names: frozenset[str],
        inactive_text_markers: tuple[str, ...],
    ) -> None:
        self.max_items = max_items
        self.active_path_field_names = active_path_field_names
        self.active_path_sections = active_path_sections
        self.truth_text_field_names = truth_text_field_names
        self.inactive_text_markers = inactive_text_markers
        self.active_occurrences: list[_RawJsonActiveScopeOccurrence] = []
        self.text_occurrences: list[_RawJsonActiveScopeOccurrence] = []
        self.active_path_occurrence_count = 0
        self.text_occurrence_count = 0
        self.key_occurrence_count = 0
        self.checked_value_count = 0

    def scan(self, value: Any, path: tuple[str, ...] = ()) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                key_text = str(key)
                child_path = (*path, key_text)
                marker = self._inactive_marker_in_text(key_text)
                if marker:
                    occurrence = _RawJsonActiveScopeOccurrence(
                        json_location=_format_json_path(child_path),
                        occurrence_type="active_path_key"
                        if self._is_path_like_text(key_text)
                        else "text_key",
                        marker=marker,
                        value_excerpt=_excerpt(key_text),
                    )
                    if occurrence.occurrence_type == "active_path_key":
                        self._add_active(occurrence)
                    else:
                        self._add_text(occurrence)
                self.scan(item, child_path)
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                self.scan(item, (*path, "[" + str(index) + "]"))
            return
        if isinstance(value, str):
            self.checked_value_count += 1
            marker = self._inactive_marker_in_text(value)
            if not marker:
                return
            occurrence_type = self._classify_string_occurrence(path, value)
            occurrence = _RawJsonActiveScopeOccurrence(
                json_location=_format_json_path(path),
                occurrence_type=occurrence_type,
                marker=marker,
                value_excerpt=_excerpt(value),
            )
            if occurrence_type.startswith("active_"):
                self._add_active(occurrence)
            else:
                self._add_text(occurrence)

    def result(self) -> _JsonActiveScopeScanResult:
        return _JsonActiveScopeScanResult(
            active_path_occurrence_count=self.active_path_occurrence_count,
            text_occurrence_count=self.text_occurrence_count,
            key_occurrence_count=self.key_occurrence_count,
            checked_value_count=self.checked_value_count,
            active_occurrences=tuple(self.active_occurrences),
            text_occurrences=tuple(self.text_occurrences),
        )

    def _add_active(self, occurrence: _RawJsonActiveScopeOccurrence) -> None:
        self.active_path_occurrence_count += 1
        if len(self.active_occurrences) < self.max_items:
            self.active_occurrences.append(occurrence)

    def _add_text(self, occurrence: _RawJsonActiveScopeOccurrence) -> None:
        if occurrence.occurrence_type == "text_key":
            self.key_occurrence_count += 1
        self.text_occurrence_count += 1
        if len(self.text_occurrences) < self.max_items:
            self.text_occurrences.append(occurrence)

    def _classify_string_occurrence(self, path: tuple[str, ...], value: str) -> str:
        field_name = _field_name(path)
        if field_name in self.truth_text_field_names:
            return "source_or_documentation_text"
        if field_name in self.active_path_field_names and self._is_path_like_text(value):
            return "active_path_field"
        if _top_level_section(path) in self.active_path_sections and self._is_path_like_text(value):
            return "active_index_path_value"
        return "source_or_documentation_text"

    def _inactive_marker_in_text(self, value: str) -> str:
        normalized = str(value).replace("\\", "/").lower()
        for marker in self.inactive_text_markers:
            if marker in normalized:
                return marker
        return ""

    def _is_path_like_text(self, value: str) -> bool:
        text = str(value).strip().replace("\\", "/")
        if not text or len(text) > 500:
            return False
        if "\n" in text:
            return False
        if text.startswith(("http://", "https://")):
            return False
        if text.startswith("python ") and ("tests/" in text or "tests_archive/" in text):
            return True
        if any(marker in text.lower() for marker in self.inactive_text_markers):
            return "/" in text or text.endswith((".py", ".md", ".json", ".txt"))
        return False


def _field_name(path: tuple[str, ...]) -> str:
    for part in reversed(path):
        if not part.startswith("["):
            return part
    return ""


def _top_level_section(path: tuple[str, ...]) -> str:
    for part in path:
        if not part.startswith("["):
            return part
    return ""


def _format_json_path(path: Iterable[str]) -> str:
    parts: list[str] = []
    for item in path:
        if item.startswith("[") and parts:
            parts[-1] = parts[-1] + item
        else:
            parts.append(item)
    return "/".join(parts)


def _excerpt(value: str) -> str:
    return " ".join(str(value).split())[:220]
