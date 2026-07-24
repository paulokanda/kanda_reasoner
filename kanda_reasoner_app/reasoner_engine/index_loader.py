# project-path: kanda_reasoner_app/reasoner_engine/index_loader.py
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
        """Support init behavior.
        """
        
        initialize_index_state(self)

    def _resolve_runtime_source_file(self, source_file: str) -> str:
        """Support resolve runtime source file behavior.
        
        Parameters
        ----------
        source_file : str
            The source file value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return resolve_runtime_source_file(self, source_file)

    def load_json(self, file_path: str) -> None:
        """Load the json.
        
        Parameters
        ----------
        file_path : str
            The file path.
        """
        
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
        """Support load behavior.
        
        Parameters
        ----------
        file_path : str
            The file path.
        """
        
        self.load_json(file_path)

    def initialize_live_project(self, project_root: str) -> None:
        """Initialize an in-memory index for bounded live-source retrieval.

        This mode is used only when the selected Project has no complete
        Project Q&A JSON. It does not create, overwrite, or persist evidence
        files.
        """
        root_text = str(project_root or "").strip()
        if not root_text:
            raise ValueError("A project root is required for live-source mode.")

        initialize_index_state(self)
        self.index_data = {
            "artifact_type": "local_ai_live_project_source",
            "project_summary": {
                "project_root": root_text,
                "entry_files": [],
            },
        }
        self.top_level_sections = dict(self.index_data)
        self.section_names = sorted(self.top_level_sections.keys())
        self.project_summary = self._safe_dict(
            self.index_data.get("project_summary")
        )
        self.project_root = root_text
        self.semantic_roles = {}

    def _load_full_sections(self) -> None:
        """Support load full sections behavior.
        """
        
        load_full_sections(self)

    def _rebuild_indexes(self) -> None:
        """Support rebuild indexes behavior.
        """
        
        rebuild_indexes(self)

    def _build_snippet_lookup_index(self) -> None:
        """Support build snippet lookup index behavior.
        """
        
        build_snippet_lookup_index(self)

    def _build_core_file_and_symbol_indexes(self) -> None:
        """Support build core file and symbol indexes behavior.
        """
        
        build_core_file_and_symbol_indexes(self)

    def _build_import_and_call_graph_indexes(self) -> None:
        """Support build import and call graph indexes behavior.
        """
        
        build_import_and_call_graph_indexes(self)

    def _build_widget_indexes(self) -> None:
        """Support build widget indexes behavior.
        """
        
        build_widget_indexes(self)

    def _build_ui_action_indexes(self) -> None:
        """Support build ui action indexes behavior.
        """
        
        build_ui_action_indexes(self)

    def _build_boundary_indexes(self) -> None:
        """Support build boundary indexes behavior.
        """
        
        build_boundary_indexes(self)

    def _build_runtime_indexes(self) -> None:
        """Support build runtime indexes behavior.
        """
        
        build_runtime_indexes(self)

    def _build_hotspot_indexes(self) -> None:
        """Support build hotspot indexes behavior.
        """
        
        build_hotspot_indexes(self)

    def resolve_module_to_path(self, module_name: str) -> str | None:
        """Resolve the module to path.
        
        Parameters
        ----------
        module_name : str
            The module name value.
        
        Returns
        -------
        str | None
            The string result.
        """
        
        record = self.files_by_module.get(module_name)
        if record:
            return self._safe_text(record.get("path"))
        return None

    def get_section(self, section_name: str, default: Any = None) -> Any:
        """Return the section.
        
        Parameters
        ----------
        section_name : str
            The section name value.
        default : Any, optional
            The default value.
        
        Returns
        -------
        Any
            The any result.
        """
        
        if not self.index_data:
            return default
        return self.index_data.get(section_name, default)

    def has_section(self, section_name: str) -> bool:
        """Return whether section.
        
        Parameters
        ----------
        section_name : str
            The section name value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        return bool(self.section_presence_map.get(section_name, False))

    def get_runtime_trace_events(self) -> list[dict[str, Any]]:
        """Return the runtime trace events.
        
        Returns
        -------
        list[dict[str, Any]]
            The list of values.
        """
        
        return self._safe_list(self.runtime_trace_raw.get("events"))

    def get_runtime_trace_errors(self) -> list[dict[str, Any]]:
        """Return the runtime trace errors.
        
        Returns
        -------
        list[dict[str, Any]]
            The list of values.
        """
        
        return self._safe_list(self.runtime_trace_raw.get("errors"))

    def get_runtime_trace_warnings(self) -> list[dict[str, Any]]:
        """Return the runtime trace warnings.
        
        Returns
        -------
        list[dict[str, Any]]
            The list of values.
        """
        
        return self._safe_list(self.runtime_trace_raw.get("warnings"))

    def get_file_record(self, path: str) -> dict[str, Any] | None:
        """Return the file record.
        
        Parameters
        ----------
        path : str
            The file or folder path.
        
        Returns
        -------
        dict[str, Any] | None
            The mapped values.
        """
        
        return self.files_by_path.get(path)

    def get_symbol_record(self, symbol_name: str) -> dict[str, Any] | None:
        """Return the symbol record.
        
        Parameters
        ----------
        symbol_name : str
            The symbol name value.
        
        Returns
        -------
        dict[str, Any] | None
            The mapped values.
        """
        
        return self.symbol_details.get(symbol_name)

    def get_all_known_paths(self) -> list[str]:
        """Return the all known paths.
        
        Returns
        -------
        list[str]
            The list of values.
        """
        
        keys = set(self.files_by_path.keys())
        keys.update(self.widgets_by_file.keys())
        keys.update(self.ui_actions_by_file.keys())
        keys.update(self.boundaries_by_file.keys())
        keys.update(self.runtime_events_by_file.keys())
        keys.update(self.hotspots_by_file.keys())
        return sorted(key for key in keys if key)

    @staticmethod
    def _safe_text(value: Any) -> str:
        """Support safe text behavior.
        
        Parameters
        ----------
        value : Any
            The input value.
        
        Returns
        -------
        str
            The string result.
        """
        
        return str(value).strip() if value is not None else ""

    @staticmethod
    def _safe_dict(value: Any) -> dict[str, Any]:
        """Support safe dict behavior.
        
        Parameters
        ----------
        value : Any
            The input value.
        
        Returns
        -------
        dict[str, Any]
            The mapped values.
        """
        
        return value if isinstance(value, dict) else {}

    @staticmethod
    def _safe_list(value: Any) -> list[Any]:
        """Support safe list behavior.
        
        Parameters
        ----------
        value : Any
            The input value.
        
        Returns
        -------
        list[Any]
            The list of values.
        """
        
        return value if isinstance(value, list) else []

    @staticmethod
    def _safe_int(value: Any, default: int = 0) -> int:
        """Support safe int behavior.
        
        Parameters
        ----------
        value : Any
            The input value.
        default : int, optional
            The default value.
        
        Returns
        -------
        int
            The integer result.
        """
        
        try:
            return int(value)
        except Exception:
            return default


