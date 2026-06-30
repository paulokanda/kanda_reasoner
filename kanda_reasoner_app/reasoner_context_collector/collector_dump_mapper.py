# project-path: kanda_reasoner_app/reasoner_context_collector/collector_dump_mapper.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

__all__ = [
    "build_change_impact",
    "build_event_propagation",
    "build_local_change_impact",
    "build_local_event_propagation",
    "build_local_symbol_index_with_enrichment",
    "build_symbol_index_with_enrichment",
    "extract_global_state",
    "extract_localization",
]

import ast
from typing import Any


def _string_constant_value(node: ast.AST) -> str:
    """Support string constant value behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return ""


def _decorator_name(decorator: Any) -> str:
    """Support decorator name behavior.
    
    Parameters
    ----------
    decorator : Any
        The decorator value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if isinstance(decorator, str):
        return decorator
    if isinstance(decorator, dict):
        return str(decorator.get("name", "")).strip()
    if isinstance(decorator, ast.Name):
        return decorator.id
    if isinstance(decorator, ast.Attribute):
        parts: list[str] = []
        current: ast.AST | None = decorator
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
        return ".".join(reversed(parts))
    if isinstance(decorator, ast.Call):
        return _decorator_name(decorator.func)
    return str(getattr(decorator, "id", "") or getattr(decorator, "name", "")).strip()


def extract_localization(source: str, path: str) -> dict:
    """Extract localization information such as strings, f-strings, hard-coded paths, and URLs."""
    localization_data = {
        "strings": [],
        "fstrings": [],
        "hard_coded_urls": [],
        "hard_coded_paths": [],
    }

    try:
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                localization_data["strings"].append(node.value)

            elif isinstance(node, ast.JoinedStr):
                fstring_parts = []
                for expr in node.values:
                    text = _string_constant_value(expr)
                    if text:
                        fstring_parts.append(text)
                localization_data["fstrings"].append("".join(fstring_parts))

            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in ["open", "urlopen"]:
                    for arg in node.args:
                        text = _string_constant_value(arg)
                        if not text:
                            continue
                        if text.startswith("http"):
                            localization_data["hard_coded_urls"].append(text)
                        elif "/" in text or "\\" in text:
                            localization_data["hard_coded_paths"].append(text)

    except Exception as e:
        print(f"Error extracting localization from {path}: {e}")

    return localization_data


def infer_module_role(module_name: str, source: str, has_main_guard: bool, imports_flat: list[str]) -> dict:
    """Infer module roles (UI, controller, utility, etc.) based on module content and imports."""
    roles = []
    primary_role = "general"

    if has_main_guard:
        roles.append("entry_point")

    if "PyQt" in imports_flat or "QWidget" in imports_flat:
        roles.append("UI")
        primary_role = "UI"
    elif "flask" in imports_flat or "django" in imports_flat:
        roles.append("web")
        primary_role = "web"
    elif "utils" in module_name:
        roles.append("utility")
        primary_role = "utility"
    elif "test" in module_name:
        roles.append("test")
        primary_role = "test"

    return {
        "primary_role": primary_role,
        "all_roles": roles,
        "is_entry_point": has_main_guard,
    }


def extract_global_state(source_tree: dict) -> list[dict]:
    """Extract global state assignments and mutable variables."""
    global_state = []

    try:
        for node in source_tree.get("body", []):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if isinstance(node.value, (ast.List, ast.Dict)):
                            global_state.append(
                                {
                                    "variable": target.id,
                                    "assignment_line": target.lineno,
                                    "type": "mutable",
                                }
                            )
                        elif isinstance(node.value, ast.Name) and not isinstance(node.value, ast.Constant):
                            global_state.append(
                                {
                                    "variable": target.id,
                                    "assignment_line": target.lineno,
                                    "type": "non-constant",
                                }
                            )
    except Exception as e:
        print(f"Error extracting global state: {e}")

    return global_state


def _build_symbol_record(path: str, symbol_data: dict, kind: str) -> dict:
    """Support build symbol record behavior.
    
    Parameters
    ----------
    path : str
        The file or folder path.
    symbol_data : dict
        The symbol data value.
    kind : str
        The kind value.
    
    Returns
    -------
    dict
        The mapped values.
    """
    
    decorators = [
        name
        for name in (_decorator_name(item) for item in symbol_data.get("decorators", []))
        if name
    ]
    return {
        "file": path,
        "line": symbol_data.get("lineno"),
        "kind": kind,
        "decorators": decorators,
        "return_type": symbol_data.get("returns", "unknown"),
    }


def build_local_symbol_index_with_enrichment(file_record: dict) -> dict:
    """Build a symbol index that is local to one file record only."""
    symbol_index: dict[str, dict] = {}
    path = str(file_record.get("path", "")).strip()
    if not path:
        return symbol_index

    for fn in file_record.get("functions", []):
        symbol = fn.get("qualname", fn.get("name", ""))
        if symbol:
            symbol_index[symbol] = _build_symbol_record(path, fn, "function")

    for cls in file_record.get("classes", []):
        cls_name = cls.get("name", "")
        if cls_name:
            symbol_index[cls_name] = {
                "file": path,
                "line": cls.get("lineno"),
                "kind": "class",
                "decorators": [],
                "return_type": "unknown",
            }

        for method in cls.get("methods", []):
            symbol = method.get("qualname", method.get("name", ""))
            if symbol:
                symbol_index[symbol] = _build_symbol_record(path, method, "method")

    return symbol_index


def build_symbol_index_with_enrichment(files_payload: list[dict]) -> dict:
    """Build an enriched symbol index across the full file corpus."""
    symbol_index: dict[str, dict] = {}

    for file_record in files_payload:
        symbol_index.update(build_local_symbol_index_with_enrichment(file_record))

    return symbol_index


def build_local_event_propagation(file_record: dict) -> list[dict]:
    """Track event propagation local to a single file record."""
    event_propagation: list[dict] = []
    path = str(file_record.get("path", "")).strip()
    if not path:
        return event_propagation

    for fn in file_record.get("functions", []):
        for event in fn.get("events", []):
            event_propagation.append(
                {
                    "from_file": path,
                    "from_symbol": fn.get("qualname", fn.get("name", "")),
                    "event": event.get("event_name"),
                    "to_handler": event.get("handler_name"),
                    "line": fn.get("lineno"),
                }
            )

    return event_propagation


def build_event_propagation(files_payload: list[dict]) -> list[dict]:
    """Track how events propagate through the full project corpus."""
    event_propagation: list[dict] = []
    for file_record in files_payload:
        event_propagation.extend(build_local_event_propagation(file_record))
    return event_propagation


def build_local_change_impact(file_record: dict) -> list[dict]:
    """Track local high-risk dependency impacts for one file record."""
    change_impact: list[dict] = []
    path = str(file_record.get("path", "")).strip()
    if not path:
        return change_impact

    for fn in file_record.get("functions", []):
        dependencies = fn.get("dependencies", [])
        for dep in dependencies:
            if dep.get("type") == "high_risk":
                change_impact.append(
                    {
                        "from_file": path,
                        "from_symbol": fn.get("qualname", fn.get("name", "")),
                        "to_file": dep.get("file"),
                        "to_symbol": dep.get("symbol"),
                        "impact_type": "high_risk",
                    }
                )

    return change_impact


def build_change_impact(files_payload: list[dict]) -> list[dict]:
    """Track high-risk dependency impacts across the full corpus."""
    change_impact: list[dict] = []
    for file_record in files_payload:
        change_impact.extend(build_local_change_impact(file_record))
    return change_impact
