"""
JSON index loader public entry point for Project Reasoner V10.

This module keeps JsonProjectIndex as the stable public contract while moving
repetitive state initialization, section loading, and index-building logic into
helper modules.
"""
from __future__ import annotations

import json
from typing import Any

from .index_loader_help.index_builders import (
    build_boundary_indexes,
    build_core_file_and_symbol_indexes,
    build_hotspot_indexes,
    build_import_and_call_graph_indexes,
    build_runtime_indexes,
    build_snippet_lookup_index,
    build_ui_action_indexes,
    build_widget_indexes,
    rebuild_indexes,
)
from .index_loader_help.path_resolution import resolve_runtime_source_file
from .index_loader_help.section_loading import load_full_sections
from .index_loader_help.state_init import initialize_index_state


__all__ = ["JsonProjectIndex"]


class JsonProjectIndex:
    """
    Loads the canonical Project Reasoner JSON and exposes both:
    1. backward-compatible core indexes used by the current retriever
    2. broader section-level access for full JSON reading

    Design goals:
    - Do not break the current retriever contract
    - Keep the full canonical JSON in memory
    - Normalize important advanced sections for later retrieval
    """

    def __init__(self) -> None:
        initialize_index_state(self)

    def _resolve_runtime_source_file(self, source_file: str) -> str:
        return resolve_runtime_source_file(self, source_file)

    def load_json(self, file_path: str) -> None:
        with open(file_path, "r", encoding="utf-8", errors="replace") as handle:
            self.index_data = json.load(handle)

        if not isinstance(self.index_data, dict):
            raise ValueError("Project index JSON root must be a dictionary.")

        self.top_level_sections = dict(self.index_data)
        self.section_names = sorted(self.top_level_sections.keys())

        self.project_summary = self._safe_dict(self.index_data.get("project_summary"))
        self.project_root = self._safe_text(self.project_summary.get("project_root"))
        self.semantic_roles = self._safe_dict(self.index_data.get("semantic_roles"))

        self._load_full_sections()
        self._rebuild_indexes()

    def load(self, file_path: str) -> None:
        self.load_json(file_path)

    def _load_full_sections(self) -> None:
        load_full_sections(self)

    def _rebuild_indexes(self) -> None:
        rebuild_indexes(self)

    def _build_snippet_lookup_index(self) -> None:
        build_snippet_lookup_index(self)

    def _build_core_file_and_symbol_indexes(self) -> None:
        build_core_file_and_symbol_indexes(self)

    def _build_import_and_call_graph_indexes(self) -> None:
        build_import_and_call_graph_indexes(self)

    def _build_widget_indexes(self) -> None:
        build_widget_indexes(self)

    def _build_ui_action_indexes(self) -> None:
        build_ui_action_indexes(self)

    def _build_boundary_indexes(self) -> None:
        build_boundary_indexes(self)

    def _build_runtime_indexes(self) -> None:
        build_runtime_indexes(self)

    def _build_hotspot_indexes(self) -> None:
        build_hotspot_indexes(self)

    def resolve_module_to_path(self, module_name: str) -> str | None:
        record = self.files_by_module.get(module_name)
        if record:
            return self._safe_text(record.get("path"))
        return None

    def get_section(self, section_name: str, default: Any = None) -> Any:
        if not self.index_data:
            return default
        return self.index_data.get(section_name, default)

    def has_section(self, section_name: str) -> bool:
        return bool(self.section_presence_map.get(section_name, False))

    def get_runtime_trace_events(self) -> list[dict[str, Any]]:
        return self._safe_list(self.runtime_trace_raw.get("events"))

    def get_runtime_trace_errors(self) -> list[dict[str, Any]]:
        return self._safe_list(self.runtime_trace_raw.get("errors"))

    def get_runtime_trace_warnings(self) -> list[dict[str, Any]]:
        return self._safe_list(self.runtime_trace_raw.get("warnings"))

    def get_file_record(self, path: str) -> dict[str, Any] | None:
        return self.files_by_path.get(path)

    def get_symbol_record(self, symbol_name: str) -> dict[str, Any] | None:
        return self.symbol_details.get(symbol_name)

    def get_all_known_paths(self) -> list[str]:
        keys = set(self.files_by_path.keys())
        keys.update(self.widgets_by_file.keys())
        keys.update(self.ui_actions_by_file.keys())
        keys.update(self.boundaries_by_file.keys())
        keys.update(self.runtime_events_by_file.keys())
        keys.update(self.hotspots_by_file.keys())
        return sorted(key for key in keys if key)

    @staticmethod
    def _safe_text(value: Any) -> str:
        return str(value).strip() if value is not None else ""

    @staticmethod
    def _safe_dict(value: Any) -> dict[str, Any]:
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _safe_list(value: Any) -> list[Any]:
        return value if isinstance(value, list) else []

    @staticmethod
    def _safe_int(value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except Exception:
            return default


