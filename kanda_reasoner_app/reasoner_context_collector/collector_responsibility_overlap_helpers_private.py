# project-path: kanda_reasoner_app/reasoner_context_collector/collector_responsibility_overlap_helpers_private.py
"""Private helpers for responsibility overlap collection."""

from __future__ import annotations

__all__: list[str] = []

from typing import Any


GENERIC_TOKENS = {
    "ui",
    "widget",
    "button",
    "dialog",
    "window",
    "tab",
    "panel",
    "bar",
    "menu",
    "layout",
    "tool",
    "tools",
    "template",
    "templates",
    "base",
    "common",
    "utils",
    "util",
    "helper",
    "helpers",
    "core",
    "main",
    "app",
    "manager",
    "controller",
    "service",
    "data",
    "file",
    "files",
    "module",
    "modules",
    "test",
    "tests",
    "view",
    "builder",
    "handler",
}

GENERIC_ROLE_TOKENS = {
    "ui",
    "service",
    "controller",
    "domain",
    "general",
    "visualization",
}


def _safe_float(value: Any) -> float:
    """Support safe float behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    
    Returns
    -------
    float
        The floating-point result.
    """
    
    try:
        return float(value)
    except Exception:
        return 0.0

def _safe_bucket(file_path: str, files_payload: list[dict[str, Any]]) -> str:
    """Support safe bucket behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    str
        The string result.
    """
    
    for record in files_payload:
        if str(record.get("path", "")) == file_path:
            bucket = str(record.get("subsystem_bucket", "")).strip()
            if bucket:
                return bucket
            break
    return "general"

def _safe_role(file_path: str, boundary_index: dict[str, dict[str, Any]]) -> str:
    """Support safe role behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    boundary_index : dict[str, dict[str, Any]]
        The boundary index value.
    
    Returns
    -------
    str
        The string result.
    """
    
    payload = boundary_index.get(file_path, {})
    if not isinstance(payload, dict):
        return "unclassified"
    return str(payload.get("boundary_role", "unclassified") or "unclassified")

def _basename_tokens(file_path: str) -> set[str]:
    """Support basename tokens behavior.
    
    Parameters
    ----------
    file_path : str
        The file path.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    normalized = str(file_path or "").replace("\\", "/").lower()
    name = normalized.rsplit("/", 1)[-1]
    stem = name.rsplit(".", 1)[0]
    parts = stem.replace("-", "_").split("_")
    return {part for part in parts if part and part not in GENERIC_TOKENS and len(part) >= 4}

def _semantic_role_set(file_record: dict[str, Any]) -> set[str]:
    """Support semantic role set behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    roles = file_record.get("semantic_roles", [])
    if not isinstance(roles, list):
        return set()
    return {
        str(role).strip().lower()
        for role in roles
        if str(role).strip()
        and str(role).strip().lower() not in GENERIC_TOKENS
        and str(role).strip().lower() not in GENERIC_ROLE_TOKENS
    }

def _normalize_text_tokens(text: str) -> set[str]:
    """Support normalize text tokens behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    cleaned = (
        str(text or "")
        .lower()
        .replace("-", " ")
        .replace("_", " ")
        .replace("/", " ")
        .replace(".", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace(",", " ")
        .replace(":", " ")
        .replace(";", " ")
    )
    out: set[str] = set()
    for token in cleaned.split():
        token = token.strip()
        if token and token not in GENERIC_TOKENS and len(token) >= 4:
            out.add(token)
    return out

def _summary_terms(file_record: dict[str, Any]) -> set[str]:
    """Support summary terms behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    out: set[str] = set()
    summary_payload = file_record.get("module_responsibility_summary", {})

    if isinstance(summary_payload, dict):
        for key in (
            "primary_responsibilities",
            "secondary_responsibilities",
            "keywords",
            "responsibility_terms",
        ):
            values = summary_payload.get(key, [])
            if isinstance(values, list):
                for value in values:
                    out.update(_normalize_text_tokens(str(value)))

    primary_role = str(file_record.get("primary_role", "")).strip().lower()
    if primary_role and primary_role not in GENERIC_TOKENS and primary_role not in GENERIC_ROLE_TOKENS:
        out.add(primary_role)

    secondary_roles = file_record.get("secondary_roles", [])
    if isinstance(secondary_roles, list):
        for value in secondary_roles:
            text = str(value).strip().lower()
            if text and text not in GENERIC_TOKENS and text not in GENERIC_ROLE_TOKENS:
                out.add(text)

    semantic_hints = file_record.get("semantic_hints", [])
    if isinstance(semantic_hints, list):
        for value in semantic_hints:
            out.update(_normalize_text_tokens(str(value)))

    return out
