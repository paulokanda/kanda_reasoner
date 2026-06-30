# project-path: kanda_reasoner_app/project_json_scope_filter.py
"""Apply Project Exclusion Rules to project-analysis JSON payloads."""

from __future__ import annotations

import copy
import os
import types
from pathlib import Path
from typing import Any, MutableMapping

from kanda_reasoner_app.project_exclusion_policy import (
    load_reasoner_project_exclusion_rules,
    should_exclude_reasoner_project_path,
)

PROJECT_ANALYSIS_MARKER_KEYS = {
    "collector_info", "project_summary", "source_file_index",
    "web_ai_symbol_index", "web_ai_file_responsibility_index",
    "web_ai_test_protection_index",
}
PATH_FIELD_NAMES = {
    "file", "path", "source_file", "source_path", "target_file",
    "target_path", "module_path", "owner_path", "relative_path",
}

__all__ = [
    "filter_project_analysis_json_payload",
    "install_json_splitter_project_exclusion_filter",
    "is_project_analysis_json_payload",
]


def is_project_analysis_json_payload(payload: Any) -> bool:
    """Return whether project analysis json payload.
    
    Parameters
    ----------
    payload : Any
        The payload value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return isinstance(payload, dict) and bool(PROJECT_ANALYSIS_MARKER_KEYS.intersection(payload.keys()))


def _project_root_from_payload(payload: Any, source_json_path: str | Path | None) -> Path:
    """Support project root from payload behavior.
    
    Parameters
    ----------
    payload : Any
        The payload value.
    source_json_path : str | Path | None
        The source json path value.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    if isinstance(payload, dict):
        for key in ("collector_info", "project_summary"):
            item = payload.get(key)
            if isinstance(item, dict) and item.get("project_root"):
                return Path(str(item["project_root"])).expanduser().resolve()
    for env_name in (
        "kanda_reasoner_project_root",
        "KANDA_REASONER_PROJECT_ROOT",
        "KANDA_RUNTIME_PROJECT_ROOT",
        "PROJECT_REASONER_PROJECT_ROOT",
        "PROJECT_REASONER_SCAN_ROOT",
        "KANDA_REASONER_SCAN_ROOT",
    ):
        value = os.environ.get(env_name, "").strip()
        if value:
            return Path(value).expanduser().resolve()
    if source_json_path is not None:
        path = Path(source_json_path).expanduser().resolve()
        for parent in path.parents:
            if parent.name == "project_analysis_evidence":
                return parent.parent
    return Path.cwd().resolve()


def _looks_like_relative_project_path(value: str) -> bool:
    """Support looks like relative project path behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    text = value.strip().replace("\\", "/")
    if not text or "\n" in text or len(text) > 260:
        return False
    if text.startswith(("http://", "https://")):
        return False
    return "/" in text or text.endswith((".py", ".md", ".txt", ".json", ".toml", ".cfg", ".ini"))


def _is_excluded_path_text(value: str, project_root: Path, rules: dict[str, list[str]]) -> bool:
    """Support is excluded path text behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    project_root : Path
        The project root path.
    rules : dict[str, list[str]]
        The rules value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not _looks_like_relative_project_path(value):
        return False
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    return should_exclude_reasoner_project_path(candidate, project_root, rules)


def _dict_has_excluded_path_field(value: dict[str, Any], project_root: Path, rules: dict[str, list[str]]) -> bool:
    """Support dict has excluded path field behavior.
    
    Parameters
    ----------
    value : dict[str, Any]
        The input value.
    project_root : Path
        The project root path.
    rules : dict[str, list[str]]
        The rules value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for field in PATH_FIELD_NAMES:
        item = value.get(field)
        if isinstance(item, str) and _is_excluded_path_text(item, project_root, rules):
            return True
    return False


def _filter_value(value: Any, project_root: Path, rules: dict[str, list[str]], summary: dict[str, int]) -> Any:
    """Support filter value behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    project_root : Path
        The project root path.
    rules : dict[str, list[str]]
        The rules value.
    summary : dict[str, int]
        The summary value.
    
    Returns
    -------
    Any
        The any result.
    """
    
    if isinstance(value, dict):
        if _dict_has_excluded_path_field(value, project_root, rules):
            summary["removed_count"] += 1
            return None
        result: dict[Any, Any] = {}
        for key, item in value.items():
            if isinstance(key, str) and _is_excluded_path_text(key, project_root, rules):
                summary["removed_count"] += 1
                continue
            filtered = _filter_value(item, project_root, rules, summary)
            if filtered is not None:
                result[key] = filtered
        return result
    if isinstance(value, list):
        result_list: list[Any] = []
        for item in value:
            filtered = _filter_value(item, project_root, rules, summary)
            if filtered is not None:
                result_list.append(filtered)
        return result_list
    if isinstance(value, str) and _is_excluded_path_text(value, project_root, rules):
        summary["removed_count"] += 1
        return None
    return value


def filter_project_analysis_json_payload(
    payload: Any,
    *,
    project_root: str | Path | None = None,
    source_json_path: str | Path | None = None,
) -> tuple[Any, dict[str, Any]]:
    """Support filter project analysis json payload behavior.
    
    Parameters
    ----------
    payload : Any
        The payload value.
    project_root : str | Path | None, optional
        The project root path.
    source_json_path : str | Path | None, optional
        The optional source json path value.
    
    Returns
    -------
    tuple[Any, dict[str, Any]]
        The tuple of values.
    """
    
    summary: dict[str, Any] = {"applied": False, "removed_count": 0, "project_root": ""}
    if not is_project_analysis_json_payload(payload):
        return payload, summary
    root = Path(project_root).expanduser().resolve() if project_root else _project_root_from_payload(payload, source_json_path)
    rules = load_reasoner_project_exclusion_rules(root)
    summary["applied"] = True
    summary["project_root"] = str(root)
    filtered = _filter_value(copy.deepcopy(payload), root, rules, summary)
    if filtered is None:
        filtered = {}
    return filtered, summary


def install_json_splitter_project_exclusion_filter(target_globals: MutableMapping[str, Any]) -> None:
    """Install a module-local json.load filter for JsonSplitterWorker."""
    json_module = target_globals.get("json")
    if json_module is None or getattr(json_module, "_pa024_scope_filter", False):
        return
    proxy = types.SimpleNamespace(**vars(json_module))
    original_load = json_module.load

    def load_with_project_scope_filter(fp: Any, *args: Any, **kwargs: Any) -> Any:
        payload = original_load(fp, *args, **kwargs)
        source_path = getattr(fp, "name", None)
        filtered, _summary = filter_project_analysis_json_payload(payload, source_json_path=source_path)
        return filtered

    proxy.load = load_with_project_scope_filter
    proxy._pa024_scope_filter = True
    target_globals["json"] = proxy
