# project-path: kanda_reasoner_app/reasoner_context_collector/collector_roles.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any

from .collector_utils import compact_whitespace


ROLE_HINTS = {
    "startup": ["__main__", "qapplication", "main(", "show(", "showmaximized"],
    "main_window": ["qmainwindow", "setcentralwidget", "main_window", "build_and_show"],
    "tabs": ["addtab", "notebook", "tabfactory", "currentchanged"],
    "timeline": ["timelinewidget", "timelinemanager", "window_moved", "time_clicked", "on_timeline_moved"],
    "topomap": ["topomap", "amplitude_map", "mcrvlt_snapshot_map", "colorbar"],
    "filters": ["filter", "dropdown", "combobox", "toolbar"],
    "splash": ["splash", "kandasplash"],
    "state_reset": ["reset", "snapshot", "cleanup", "destroyed.connect"],
    "memory_monitoring": ["memory", "memoryleakdetector"],
}


def summarize_file_semantics(record: dict[str, Any]) -> dict[str, Any]:
    """Support summarize file semantics behavior.
    
    Parameters
    ----------
    record : dict[str, Any]
        The record value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    blob_parts: list[str] = []

    blob_parts.extend(record.get("imports", []))
    blob_parts.extend(record.get("comments", []))
    blob_parts.extend(record.get("strings", []))
    blob_parts.append(record.get("docstring", ""))

    for fn in record.get("functions", []):
        blob_parts.append(fn.get("name", ""))
        blob_parts.append(fn.get("docstring", ""))
        for call in fn.get("calls", []):
            blob_parts.append(call.get("call_name", ""))

    for cls in record.get("classes", []):
        blob_parts.append(cls.get("name", ""))
        blob_parts.append(cls.get("docstring", ""))
        for method in cls.get("methods", []):
            blob_parts.append(method.get("name", ""))
            blob_parts.append(method.get("docstring", ""))
            for call in method.get("calls", []):
                blob_parts.append(call.get("call_name", ""))

    blob = compact_whitespace(" ".join(blob_parts)).lower()

    roles: list[str] = []
    evidence_terms: list[str] = []
    score_map: dict[str, int] = {}

    for role, hints in ROLE_HINTS.items():
        score = 0
        for hint in hints:
            if hint.lower() in blob:
                score += 1
                evidence_terms.append(hint)
        if score > 0:
            roles.append(role)
            score_map[role] = score

    primary_role = ""
    secondary_roles: list[str] = []
    confidence = 0.0

    if score_map:
        ordered = sorted(score_map.items(), key=lambda item: item[1], reverse=True)
        primary_role = ordered[0][0]
        secondary_roles = [item[0] for item in ordered[1:4]]
        confidence = min(0.99, 0.5 + (ordered[0][1] * 0.1))

    return {
        "roles": roles,
        "primary_role": primary_role,
        "secondary_roles": secondary_roles,
        "confidence": round(confidence, 2),
        "evidence_terms": sorted(set(evidence_terms)),
    }


def summarize_symbol_semantics(symbol_record: dict[str, Any], kind: str) -> str:
    """Support summarize symbol semantics behavior.
    
    Parameters
    ----------
    symbol_record : dict[str, Any]
        The symbol record value.
    kind : str
        The kind value.
    
    Returns
    -------
    str
        The string result.
    """
    
    name = symbol_record.get("qualname") or symbol_record.get("name", "")
    calls = [call.get("call_name", "") for call in symbol_record.get("calls", [])]

    text = " ".join(calls).lower()

    if "connect" in text:
        return f"{kind} {name} wires or reacts to signals."
    if "show" in text or "addtab" in text or "setcentralwidget" in text:
        return f"{kind} {name} builds or displays UI components."
    if "reset" in text or "cleanup" in text:
        return f"{kind} {name} resets or cleans application state."
    if "timeline" in text:
        return f"{kind} {name} manages timeline-related behavior."
    if "topomap" in text or "amplitude_map" in text:
        return f"{kind} {name} manages topomap or amplitude-map behavior."
    if "update_plot" in text or "draw" in text:
        return f"{kind} {name} updates rendered visual state."
    return f"{kind} {name} contributes to project behavior."
