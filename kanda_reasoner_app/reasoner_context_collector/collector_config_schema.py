# project-path: kanda_reasoner_app/reasoner_context_collector/collector_config_schema.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


CONFIG_KEY_HINTS = {
    "config",
    "settings",
    "schema",
    "cache",
    "path",
    "folder",
    "directory",
    "json",
    "csv",
    "hdf",
    "hdf5",
    "parquet",
    "key",
    "field",
    "column",
    "group",
    "dataset",
    "export",
    "import",
}


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
    
    return str(value or "").strip()


def _normalize_token(token: str) -> str:
    """Support normalize token behavior.
    
    Parameters
    ----------
    token : str
        The token value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return (
        _safe_text(token)
        .lower()
        .replace("\\", "_")
        .replace("/", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace(" ", "_")
    )


def _is_schema_like(token: str) -> bool:
    """Support is schema like behavior.
    
    Parameters
    ----------
    token : str
        The token value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    normalized = _normalize_token(token)
    if not normalized:
        return False
    if normalized in CONFIG_KEY_HINTS:
        return True
    return any(hint in normalized for hint in CONFIG_KEY_HINTS)


def _safe_bucket(file_record: dict[str, Any]) -> str:
    """Support safe bucket behavior.
    
    Parameters
    ----------
    file_record : dict[str, Any]
        The file record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return _safe_text(file_record.get("subsystem_bucket", "")).lower() or "general"


def _collect_assignment_targets(file_record: dict[str, Any]) -> set[str]:
    """Support collect assignment targets behavior.
    
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

    def add_assignment(assignment: dict[str, Any]) -> None:
        target = _safe_text(assignment.get("target", ""))
        if target:
            out.add(target)

    for fn in file_record.get("functions", []):
        if not isinstance(fn, dict):
            continue
        for assignment in fn.get("assignments", []):
            if isinstance(assignment, dict):
                add_assignment(assignment)

    for cls in file_record.get("classes", []):
        if not isinstance(cls, dict):
            continue
        for method in cls.get("methods", []):
            if not isinstance(method, dict):
                continue
            for assignment in method.get("assignments", []):
                if isinstance(assignment, dict):
                    add_assignment(assignment)

    return out


def _collect_call_names(file_record: dict[str, Any]) -> set[str]:
    """Support collect call names behavior.
    
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

    def add_call(call: dict[str, Any]) -> None:
        call_name = _safe_text(call.get("call_name", ""))
        if call_name:
            out.add(call_name)

    for fn in file_record.get("functions", []):
        if not isinstance(fn, dict):
            continue
        for call in fn.get("calls", []):
            if isinstance(call, dict):
                add_call(call)

    for cls in file_record.get("classes", []):
        if not isinstance(cls, dict):
            continue
        for method in cls.get("methods", []):
            if not isinstance(method, dict):
                continue
            for call in method.get("calls", []):
                if isinstance(call, dict):
                    add_call(call)

    return out


def _collect_semantic_terms(file_record: dict[str, Any]) -> set[str]:
    """Support collect semantic terms behavior.
    
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

    for key in (
        "primary_role",
        "summary",
        "docstring",
    ):
        value = _safe_text(file_record.get(key, ""))
        if value:
            out.add(value)

    for value in file_record.get("secondary_roles", []):
        text = _safe_text(value)
        if text:
            out.add(text)

    for value in file_record.get("semantic_hints", []):
        text = _safe_text(value)
        if text:
            out.add(text)

    summary_payload = file_record.get("module_responsibility_summary", {})
    if isinstance(summary_payload, dict):
        for key in (
            "primary_responsibilities",
            "secondary_responsibilities",
            "keywords",
            "responsibility_terms",
        ):
            for value in summary_payload.get(key, []):
                text = _safe_text(value)
                if text:
                    out.add(text)

    return out


def build_config_schema_registry(
    files_payload: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a config schema registry.
    
    Parameters
    ----------
    files_payload : list[dict[str, Any]]
        The files payload value.
    
    Returns
    -------
    dict[str, dict[str, Any]]
        The mapped values.
    """
    
    registry: dict[str, dict[str, Any]] = {}

    for file_record in files_payload:
        file_path = _safe_text(file_record.get("path", ""))
        if not file_path:
            continue

        assignment_targets = _collect_assignment_targets(file_record)
        call_names = _collect_call_names(file_record)
        semantic_terms = _collect_semantic_terms(file_record)

        raw_candidates = assignment_targets | call_names | semantic_terms

        schema_terms = sorted(
            {
                token
                for token in raw_candidates
                if _is_schema_like(token)
            }
        )

        namespace_roots = sorted(
            {
                _normalize_token(term).split("_")[0]
                for term in schema_terms
                if _normalize_token(term)
            }
        )

        registry[file_path] = {
            "file": file_path,
            "bucket": _safe_bucket(file_record),
            "schema_term_count": len(schema_terms),
            "schema_terms": schema_terms[:100],
            "namespace_roots": namespace_roots[:50],
            "is_schema_risk_candidate": bool(len(schema_terms) >= 5),
        }

    return dict(sorted(registry.items()))


def build_config_schema_summary(
    config_schema_registry: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a config schema summary.
    
    Parameters
    ----------
    config_schema_registry : dict[str, dict[str, Any]]
        The config schema registry value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    rows: list[dict[str, Any]] = []
    all_terms: set[str] = set()
    all_namespaces: set[str] = set()

    for file_path, payload in config_schema_registry.items():
        schema_terms = list(payload.get("schema_terms", []))
        namespace_roots = list(payload.get("namespace_roots", []))

        for term in schema_terms:
            all_terms.add(_safe_text(term))
        for ns in namespace_roots:
            all_namespaces.add(_safe_text(ns))

        rows.append(
            {
                "file": file_path,
                "bucket": _safe_text(payload.get("bucket", "general")) or "general",
                "schema_term_count": int(payload.get("schema_term_count", 0)),
                "namespace_root_count": len(namespace_roots),
                "is_schema_risk_candidate": bool(
                    payload.get("is_schema_risk_candidate", False)
                ),
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("schema_term_count", 0)),
            item.get("file", ""),
        )
    )

    schema_risk_hotspot_count = sum(
        1 for row in rows if bool(row.get("is_schema_risk_candidate", False))
    )

    return {
        "file_count": len(rows),
        "config_key_count": len(all_terms),
        "schema_namespace_count": len(all_namespaces),
        "schema_risk_hotspot_count": schema_risk_hotspot_count,
        "files": rows,
    }


def build_schema_risk_hotspots(
    config_schema_registry: dict[str, dict[str, Any]],
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Build a schema risk hotspots.
    
    Parameters
    ----------
    config_schema_registry : dict[str, dict[str, Any]]
        The config schema registry value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    rows: list[dict[str, Any]] = []

    for file_path, payload in config_schema_registry.items():
        if not bool(payload.get("is_schema_risk_candidate", False)):
            continue

        rows.append(
            {
                "file": file_path,
                "bucket": _safe_text(payload.get("bucket", "general")) or "general",
                "schema_term_count": int(payload.get("schema_term_count", 0)),
                "namespace_root_count": len(payload.get("namespace_roots", [])),
                "schema_terms": list(payload.get("schema_terms", []))[:20],
                "namespace_roots": list(payload.get("namespace_roots", []))[:20],
            }
        )

    rows.sort(
        key=lambda item: (
            -int(item.get("schema_term_count", 0)),
            item.get("file", ""),
        )
    )

    return rows[:limit]
