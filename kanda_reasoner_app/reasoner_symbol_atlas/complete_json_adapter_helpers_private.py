# project-path: kanda_reasoner_app/reasoner_symbol_atlas/complete_json_adapter_helpers_private.py
"""Private conversion helpers for complete JSON adapter."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .complete_json_adapter import ProjectSymbolAtlasCompleteJsonSummary

from .schemas import (
    ProjectModuleRecord,
    ProjectSymbol,
    normalize_project_atlas_text,
)

__all__: list[str] = []


def _mapping_count(value: object) -> int:
    """Support mapping count behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return len(value) if isinstance(value, dict) else 0


def _sequence_count(value: object) -> int:
    """Support sequence count behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    return len(value) if isinstance(value, list) else 0


def _format_summary_line(summary: ProjectSymbolAtlasCompleteJsonSummary) -> str:
    """Support format summary line behavior.
    
    Parameters
    ----------
    summary : ProjectSymbolAtlasCompleteJsonSummary
        The summary value.
    
    Returns
    -------
    str
        The string result.
    """
    
    data = summary.to_dict()
    return (
        "Complete JSON adapter status="
        + str(data["status"])
        + "; files="
        + str(data["source_file_count"])
        + "; symbols="
        + str(data["symbol_count"])
        + "; primary_definitions="
        + str(data["primary_definition_count"])
        + "; duplicate_symbols="
        + str(data["duplicate_symbol_count"])
    )


def _modules_from_complete_json(
    payload: dict[str, Any],
    limit: int,
) -> tuple[ProjectModuleRecord, ...]:
    """Support modules from complete json behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    limit : int
        The limit value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    source_index = payload.get("source_file_index")
    if not isinstance(source_index, dict) or limit <= 0:
        return ()
    responsibility_index = payload.get("web_ai_file_responsibility_index")
    if not isinstance(responsibility_index, dict):
        responsibility_index = {}

    modules: list[ProjectModuleRecord] = []
    for key in sorted(source_index.keys())[:limit]:
        item = source_index.get(key)
        if not isinstance(item, dict):
            continue
        file_path = normalize_project_atlas_text(item.get("file") or key)
        responsibility = responsibility_index.get(file_path, {})
        if not isinstance(responsibility, dict):
            responsibility = {}
        evidence = ["source_file_index"]
        owner_box = normalize_project_atlas_text(responsibility.get("owner_box"))
        primary_responsibility = normalize_project_atlas_text(
            responsibility.get("primary_responsibility")
        )
        if owner_box:
            evidence.append("owner_box: " + owner_box)
        if primary_responsibility:
            evidence.append("responsibility: " + primary_responsibility)
        modules.append(
            ProjectModuleRecord(
                module=normalize_project_atlas_text(
                    item.get("module_name") or _module_name_from_path(file_path)
                ),
                path=file_path,
                line_count=_safe_int(item.get("line_count")),
                is_package_init=Path(file_path).name == "__init__.py",
                is_test_file=_is_test_path(file_path),
                owner_role="unknown",
                symbols=(),
                imports=(),
                evidence=tuple(evidence),
            )
        )
    return tuple(modules)


def _symbols_from_complete_json(
    payload: dict[str, Any],
    limit: int,
) -> tuple[ProjectSymbol, ...]:
    """Support symbols from complete json behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    limit : int
        The limit value.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    symbol_index = payload.get("symbol_index")
    if not isinstance(symbol_index, dict) or limit <= 0:
        return ()
    web_symbol_index = payload.get("web_ai_symbol_index")
    if not isinstance(web_symbol_index, dict):
        web_symbol_index = {}

    symbols: list[ProjectSymbol] = []
    for key in sorted(symbol_index.keys())[:limit]:
        item = symbol_index.get(key)
        web_item = web_symbol_index.get(key)
        if not isinstance(item, dict):
            item = {}
        if not isinstance(web_item, dict):
            web_item = {}
        file_path = normalize_project_atlas_text(
            web_item.get("file") or item.get("file") or ""
        )
        kind = _coerce_symbol_kind(web_item.get("kind") or item.get("kind"))
        module = normalize_project_atlas_text(
            web_item.get("module_name") or _module_name_from_path(file_path)
        )
        line = _safe_int(web_item.get("line_start") or item.get("line")) or None
        evidence = ["symbol_index"]
        if key in web_symbol_index:
            evidence.append("web_ai_symbol_index")
        symbols.append(
            ProjectSymbol(
                name=normalize_project_atlas_text(
                    web_item.get("qualified_name") or web_item.get("symbol") or key
                ),
                kind=kind,
                module=module,
                path=file_path,
                line=line,
                is_public=not str(key).split(".")[-1].startswith("_"),
                owner_role="unknown",
                exported_by_all=False,
                evidence=tuple(evidence),
            )
        )
    return tuple(symbols)


def _coerce_symbol_kind(kind: object) -> str:
    """Support coerce symbol kind behavior.
    
    Parameters
    ----------
    kind : object
        The kind value.
    
    Returns
    -------
    str
        The string result.
    """
    
    normalized = normalize_project_atlas_text(kind).lower()
    if normalized in {"function", "method"}:
        return "function"
    if normalized in {"class", "dataclass", "constant", "import", "module"}:
        return normalized
    return "unknown"


def _module_name_from_path(path_text: str) -> str:
    """Support module name from path behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not path_text:
        return ""
    path = Path(path_text)
    parts = list(path.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _is_test_path(path_text: str) -> bool:
    """Support is test path behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    normalized = path_text.replace("\\", "/").lower()
    name = Path(normalized).name
    return normalized.startswith("tests/") or name.startswith("test_") or name.endswith("_test.py")


def _safe_int(value: object) -> int:
    """Support safe int behavior.
    
    Parameters
    ----------
    value : object
        The input value.
    
    Returns
    -------
    int
        The integer result.
    """
    
    try:
        if value is None:
            return 0
        return int(value)
    except (TypeError, ValueError):
        return 0
