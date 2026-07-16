"""Quality checks for generated complete JSON active-scope paths.

This module checks complete Project Analysis Evidence JSON after Tab 4 creates
it. It does not edit JSON files and does not import analyzed project modules.
It separates dangerous active-path leaks from truthful source/documentation text
that merely mentions inactive reference folders.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .complete_json_adapter import (
    collect_reasoner_symbol_atlas_complete_json_files,
    load_reasoner_symbol_atlas_complete_json,
)
from .output_policy import is_active_atlas_path
from .schemas import (
    ProjectSymbol,
    ProjectSymbolAtlasReport,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)

PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_CLEAN = "clean"
PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_TEXT_ONLY = "text_only"
PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_ACTIVE_LEAK = "active_scope_leak"
PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_MISSING_JSON = "missing_json"
PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_INVALID_JSON = "invalid_json"

ACTIVE_PATH_FIELD_NAMES = frozenset(
    {
        "file",
        "path",
        "source_file",
        "source_path",
        "target_file",
        "target_path",
        "module_path",
        "owner_path",
        "owner_file",
        "relative_path",
        "active_target_path",
        "primary_edit_target",
        "main_path",
        "helper_path",
        "related_file",
        "test_to_run",
    }
)

ACTIVE_PATH_SECTIONS = frozenset(
    {
        "active_code_index",
        "boundary_index",
        "canonical_conflict_index",
        "change_impact_index",
        "duplicate_symbols",
        "edit_ready_symbol_index",
        "import_graph",
        "primary_definition_index",
        "responsibility_overlap_index",
        "source_file_index",
        "symbol_index",
        "ui_action_index",
        "web_ai_file_responsibility_index",
        "web_ai_symbol_index",
        "web_ai_test_protection_index",
        "widget_registry",
        "widget_ui_action_bridge",
    }
)

TRUTH_TEXT_FIELD_NAMES = frozenset(
    {
        "code",
        "content",
        "docstring",
        "documentation",
        "expr",
        "full_source",
        "markdown",
        "note",
        "notes",
        "primary_responsibility",
        "reason",
        "snippet",
        "source",
        "source_excerpt",
        "summary",
        "text",
        "value_excerpt",
    }
)

# Keep this as a static normalized tuple. The architecture validator treats
# top-level method calls inside constant comprehensions as possible import
# side effects, even when they are only string normalization. Values checked by
# this module are normalized to forward slashes before comparison, so one slash
# form per marker is enough.
INACTIVE_TEXT_MARKERS = (
    "_project_reference/",
    ".project_reference/",
    "tests_archive/",
    "remaining_misplaced_tests/",
)

__all__ = [
    "ACTIVE_PATH_FIELD_NAMES",
    "ACTIVE_PATH_SECTIONS",
    "PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_ACTIVE_LEAK",
    "PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_CLEAN",
    "PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_INVALID_JSON",
    "PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_MISSING_JSON",
    "PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_TEXT_ONLY",
    "ProjectSymbolAtlasJsonActiveScopeOccurrence",
    "ProjectSymbolAtlasJsonActiveScopeQualityOptions",
    "ProjectSymbolAtlasJsonActiveScopeQualitySummary",
    "TRUTH_TEXT_FIELD_NAMES",
    "build_reasoner_symbol_atlas_json_active_scope_report",
    "check_reasoner_symbol_atlas_json_active_scope_quality",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasJsonActiveScopeQualityOptions:
    """Options for complete JSON active-scope quality checks."""

    project_root: str
    json_path: str = ""
    max_items: int = 50

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible options dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "max_items": int(self.max_items),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasJsonActiveScopeOccurrence:
    """One inactive reference-path occurrence inside complete JSON evidence."""

    json_location: str
    occurrence_type: str
    marker: str
    value_excerpt: str = ""

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-compatible occurrence dictionary."""

        return {
            "json_location": normalize_project_atlas_text(self.json_location),
            "occurrence_type": normalize_project_atlas_text(self.occurrence_type),
            "marker": normalize_project_atlas_text(self.marker),
            "value_excerpt": normalize_project_atlas_text(self.value_excerpt),
        }


@dataclass(frozen=True)
class ProjectSymbolAtlasJsonActiveScopeQualitySummary:
    """Summary of complete JSON active-scope quality."""

    project_root: str
    json_path: str = ""
    status: str = PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_MISSING_JSON
    active_path_occurrence_count: int = 0
    text_occurrence_count: int = 0
    key_occurrence_count: int = 0
    checked_value_count: int = 0
    active_occurrences: tuple[ProjectSymbolAtlasJsonActiveScopeOccurrence, ...] = field(default_factory=tuple)
    text_occurrences: tuple[ProjectSymbolAtlasJsonActiveScopeOccurrence, ...] = field(default_factory=tuple)
    notes: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible summary dictionary."""

        return {
            "project_root": str(Path(self.project_root)),
            "json_path": str(Path(self.json_path)) if self.json_path else "",
            "status": normalize_project_atlas_text(self.status),
            "active_path_occurrence_count": int(self.active_path_occurrence_count),
            "text_occurrence_count": int(self.text_occurrence_count),
            "key_occurrence_count": int(self.key_occurrence_count),
            "checked_value_count": int(self.checked_value_count),
            "active_occurrences": [item.to_dict() for item in self.active_occurrences],
            "text_occurrences": [item.to_dict() for item in self.text_occurrences],
            "notes": list(self.notes),
        }


def check_reasoner_symbol_atlas_json_active_scope_quality(
    options: ProjectSymbolAtlasJsonActiveScopeQualityOptions,
) -> ProjectSymbolAtlasJsonActiveScopeQualitySummary:
    """Check whether complete JSON has inactive paths in active fields."""

    project_root = Path(options.project_root).expanduser().resolve(strict=False)
    json_path = _select_json_path(project_root, options.json_path)
    if json_path is None:
        return ProjectSymbolAtlasJsonActiveScopeQualitySummary(
            project_root=str(project_root),
            status=PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_MISSING_JSON,
            notes=("No complete JSON evidence file was found.",),
        )

    try:
        payload = load_reasoner_symbol_atlas_complete_json(json_path)
    except ValueError as exc:
        return ProjectSymbolAtlasJsonActiveScopeQualitySummary(
            project_root=str(project_root),
            json_path=str(json_path),
            status=PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_INVALID_JSON,
            notes=(str(exc),),
        )

    scanner = _QualityScanner(max_items=max(1, int(options.max_items)))
    scanner.scan(payload)
    active_count = scanner.active_path_occurrence_count
    text_count = scanner.text_occurrence_count
    if active_count:
        status = PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_ACTIVE_LEAK
        notes = (
            "Inactive reference paths were found in active JSON decision fields.",
            "Regenerate Tab 4 JSON after fixing the source of those active fields.",
        )
    elif text_count:
        status = PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_TEXT_ONLY
        notes = (
            "Inactive reference strings remain only in source or documentation text.",
            "Active JSON decision fields are clean.",
        )
    else:
        status = PROJECT_SYMBOL_ATLAS_JSON_QUALITY_STATUS_CLEAN
        notes = ("No inactive reference path strings were found in complete JSON.",)

    return ProjectSymbolAtlasJsonActiveScopeQualitySummary(
        project_root=str(project_root),
        json_path=str(json_path),
        status=status,
        active_path_occurrence_count=active_count,
        text_occurrence_count=text_count,
        key_occurrence_count=scanner.key_occurrence_count,
        checked_value_count=scanner.checked_value_count,
        active_occurrences=tuple(scanner.active_occurrences),
        text_occurrences=tuple(scanner.text_occurrences),
        notes=notes,
    )


def build_reasoner_symbol_atlas_json_active_scope_report(
    options: ProjectSymbolAtlasJsonActiveScopeQualityOptions,
) -> ProjectSymbolAtlasReport:
    """Build a Project Symbol Atlas report for complete JSON active-scope quality."""

    summary = check_reasoner_symbol_atlas_json_active_scope_quality(options)
    data = summary.to_dict()
    symbols: list[ProjectSymbol] = []
    for occurrence in summary.active_occurrences:
        symbols.append(
            ProjectSymbol(
                name="json_active_scope_leak",
                kind="unknown",
                path=occurrence.json_location,
                is_public=False,
                evidence=(occurrence.occurrence_type, occurrence.marker),
            )
        )
    for occurrence in summary.text_occurrences[: min(10, len(summary.text_occurrences))]:
        symbols.append(
            ProjectSymbol(
                name="json_text_reference_only",
                kind="unknown",
                path=occurrence.json_location,
                is_public=False,
                evidence=(occurrence.occurrence_type, occurrence.marker),
            )
        )

    return ProjectSymbolAtlasReport(
        project_root=options.project_root,
        report_type="reasoner_symbol_atlas",
        summary=(
            "JSON active-scope quality status="
            + str(data["status"])
            + "; active_path_occurrences="
            + str(data["active_path_occurrence_count"])
            + "; text_occurrences="
            + str(data["text_occurrence_count"])
            + "; key_occurrences="
            + str(data["key_occurrence_count"])
            + "; json_path="
            + str(data["json_path"])
        ),
        symbols=tuple(symbols),
        input_sources=("complete_json", data["json_path"], "json_active_scope_quality"),
    )


class _QualityScanner:
    """Internal recursive scanner for complete JSON payloads."""

    def __init__(self, max_items: int) -> None:
        self.max_items = max_items
        self.active_occurrences: list[ProjectSymbolAtlasJsonActiveScopeOccurrence] = []
        self.text_occurrences: list[ProjectSymbolAtlasJsonActiveScopeOccurrence] = []
        self.active_path_occurrence_count = 0
        self.text_occurrence_count = 0
        self.key_occurrence_count = 0
        self.checked_value_count = 0

    def scan(self, value: Any, path: tuple[str, ...] = ()) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                key_text = str(key)
                child_path = (*path, key_text)
                marker = _inactive_marker_in_text(key_text)
                if marker:
                    occurrence = ProjectSymbolAtlasJsonActiveScopeOccurrence(
                        json_location=_format_json_path(child_path),
                        occurrence_type="active_path_key" if _is_path_like_text(key_text) else "text_key",
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
            marker = _inactive_marker_in_text(value)
            if not marker:
                return
            occurrence_type = _classify_string_occurrence(path, value)
            occurrence = ProjectSymbolAtlasJsonActiveScopeOccurrence(
                json_location=_format_json_path(path),
                occurrence_type=occurrence_type,
                marker=marker,
                value_excerpt=_excerpt(value),
            )
            if occurrence_type.startswith("active_"):
                self._add_active(occurrence)
            else:
                self._add_text(occurrence)

    def _add_active(self, occurrence: ProjectSymbolAtlasJsonActiveScopeOccurrence) -> None:
        self.active_path_occurrence_count += 1
        if len(self.active_occurrences) < self.max_items:
            self.active_occurrences.append(occurrence)

    def _add_text(self, occurrence: ProjectSymbolAtlasJsonActiveScopeOccurrence) -> None:
        if occurrence.occurrence_type == "text_key":
            self.key_occurrence_count += 1
        self.text_occurrence_count += 1
        if len(self.text_occurrences) < self.max_items:
            self.text_occurrences.append(occurrence)


def _select_json_path(project_root: Path, json_path: str) -> Path | None:
    if json_path.strip():
        return Path(json_path).expanduser().resolve(strict=False)
    candidates = collect_reasoner_symbol_atlas_complete_json_files(project_root)
    return candidates[0] if candidates else None


def _classify_string_occurrence(path: tuple[str, ...], value: str) -> str:
    field_name = _field_name(path)
    if field_name in TRUTH_TEXT_FIELD_NAMES:
        return "source_or_documentation_text"
    if field_name in ACTIVE_PATH_FIELD_NAMES and _is_path_like_text(value):
        return "active_path_field"
    if _top_level_section(path) in ACTIVE_PATH_SECTIONS and _is_path_like_text(value):
        return "active_index_path_value"
    return "source_or_documentation_text"


def _inactive_marker_in_text(value: str) -> str:
    normalized = str(value).replace("\\", "/").lower()
    for marker in INACTIVE_TEXT_MARKERS:
        if marker in normalized:
            return marker
    return ""


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


def _is_path_like_text(value: str) -> bool:
    text = str(value).strip().replace("\\", "/")
    if not text or len(text) > 500:
        return False
    if "\n" in text:
        return False
    if text.startswith(("http://", "https://")):
        return False
    if text.startswith("python ") and ("tests/" in text or "tests_archive/" in text):
        return True
    if any(marker in text.lower() for marker in INACTIVE_TEXT_MARKERS):
        return "/" in text or text.endswith((".py", ".md", ".json", ".txt"))
    return False


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
