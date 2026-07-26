# project-path: kanda_reasoner_app/reasoner_context_collector/parsers/static_context/_packaging_metadata_result_helpers.py
"""Result assembly helpers for packaging metadata parsing."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__: list[str] = []


def _normalize_rel_path(path: Path, root: Path) -> str:
    """Support normalize rel path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    return str(path.relative_to(root)).replace("\\", "/")


def _truncate_text(value: str, max_chars: int = 200) -> str:
    """Support truncate text behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    max_chars : int, optional
        The optional max chars value.
    
    Returns
    -------
    str
        The string result.
    """
    
    value = value.strip()
    if len(value) <= max_chars:
        return value
    return value[: max_chars - 3].rstrip() + "..."


def _dedupe_keep_order(items: list[str]) -> list[str]:
    """Support dedupe keep order behavior.
    
    Parameters
    ----------
    items : list[str]
        The item values.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        normalized = str(item).strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(normalized)
    return out


def _new_result() -> dict[str, Any]:
    """Support new result behavior.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    return {
        "project_name": "",
        "declared_version": "",
        "build_backend": "",
        "package_manager_signals": [],
        "declared_dependencies": [],
        "declared_optional_dependencies": {},
        "declared_entrypoints": [],
        "declared_tooling": {},
        "packaging_files_found": [],
        "packaging_evidence": [],
        "packaging_parse_warnings": [],
        "packaging_confidence": "unknown",
    }


def _append_evidence(result: dict[str, Any], source_file: str, field_name: str, value: str) -> None:
    """Support append evidence behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    source_file : str
        The source file value.
    field_name : str
        The field name value.
    value : str
        The input value.
    """
    
    result["packaging_evidence"].append(
        {
            "source_file": source_file,
            "field": field_name,
            "value_excerpt": _truncate_text(value),
        }
    )


def _append_parse_warning(result: dict[str, Any], source_file: str, message: str) -> None:
    """Support append parse warning behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    source_file : str
        The source file value.
    message : str
        The message text.
    """
    
    warning = f"{source_file}: {message}" if source_file else message
    result["packaging_parse_warnings"].append(warning)


def _add_package_manager_signal(result: dict[str, Any], signal: str) -> None:
    """Support add package manager signal behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    signal : str
        The signal value.
    """
    
    if signal not in result["package_manager_signals"]:
        result["package_manager_signals"].append(signal)


def _set_if_empty(result: dict[str, Any], key: str, value: str, source_file: str) -> None:
    """Support set if empty behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    key : str
        The key value.
    value : str
        The input value.
    source_file : str
        The source file value.
    """
    
    cleaned = value.strip()
    if cleaned and not result.get(key):
        result[key] = cleaned
        _append_evidence(result, source_file, key, cleaned)


def _merge_dependencies(result: dict[str, Any], dependencies: list[str], max_dependencies: int, source_file: str) -> None:
    """Support merge dependencies behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    dependencies : list[str]
        The dependencies value.
    max_dependencies : int
        The max dependencies value.
    source_file : str
        The source file value.
    """
    
    current = list(result["declared_dependencies"])
    result["declared_dependencies"] = _dedupe_keep_order(current + dependencies)[:max_dependencies]
    for dep in dependencies[:20]:
        _append_evidence(result, source_file, "declared_dependencies", dep)


def _merge_optional_dependencies(
    result: dict[str, Any],
    optional_dependencies: dict[str, list[str]],
    max_dependencies: int,
    source_file: str,
) -> None:
    """Support merge optional dependencies behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    optional_dependencies : dict[str, list[str]]
        The optional dependencies value.
    max_dependencies : int
        The max dependencies value.
    source_file : str
        The source file value.
    """
    
    current = dict(result["declared_optional_dependencies"])
    for extra_name, deps in optional_dependencies.items():
        merged = _dedupe_keep_order(current.get(extra_name, []) + deps)[:max_dependencies]
        current[extra_name] = merged
        for dep in deps[:20]:
            _append_evidence(result, source_file, f"declared_optional_dependencies.{extra_name}", dep)
    result["declared_optional_dependencies"] = current


def _merge_entrypoints(result: dict[str, Any], entries: list[dict[str, str]], source_file: str) -> None:
    """Support merge entrypoints behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    entries : list[dict[str, str]]
        The entries value.
    source_file : str
        The source file value.
    """
    
    current = list(result["declared_entrypoints"])
    seen = {(item.get("group", ""), item.get("name", ""), item.get("target", "")) for item in current if isinstance(item, dict)}
    for entry in entries:
        key = (entry.get("group", ""), entry.get("name", ""), entry.get("target", ""))
        if key in seen:
            continue
        seen.add(key)
        current.append(entry)
        _append_evidence(result, source_file, "declared_entrypoints", f"{entry.get('group', '')}:{entry.get('name', '')}={entry.get('target', '')}")
    result["declared_entrypoints"] = current


def _merge_tooling(result: dict[str, Any], tooling: dict[str, Any], source_file: str) -> None:
    """Support merge tooling behavior.
    
    Parameters
    ----------
    result : dict[str, Any]
        The result value.
    tooling : dict[str, Any]
        The tooling value.
    source_file : str
        The source file value.
    """
    
    current = dict(result["declared_tooling"])
    for key, value in tooling.items():
        if key not in current:
            current[key] = value
            _append_evidence(result, source_file, f"declared_tooling.{key}", str(value))
    result["declared_tooling"] = current
