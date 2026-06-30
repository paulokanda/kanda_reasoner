# project-path: kanda_reasoner_app/reasoner_context_collector/collector_priority.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations


def build_file_priority_index(
    files_payload: list[dict],
    module_centrality_index: dict,
) -> dict:
    """Build a file priority index.
    
    Parameters
    ----------
    files_payload : list[dict]
        The files payload value.
    module_centrality_index : dict
        The module centrality index value.
    
    Returns
    -------
    dict
        The mapped values.
    """
    
    out: dict = {}

    for record in files_payload:
        path = record["path"]
        module_name = record["module_name"]
        centrality = module_centrality_index.get(module_name, {})

        score = 0
        reasons: list[str] = []

        if record.get("entry_markers"):
            score += 30
            reasons.append("entry_point")

        primary_role = record.get("primary_role", "")
        if primary_role in {"ui", "controller", "orchestrator", "application"}:
            score += 20
            reasons.append("high_level_role")

        if record.get("classes"):
            score += min(len(record["classes"]) * 3, 12)
            reasons.append("contains_classes")

        if "QApplication(" in record.get("source", ""):
            score += 20
            reasons.append("qt_application_bootstrap")

        inbound = int(centrality.get("imported_by_count", 0))
        outbound = int(centrality.get("imports_count", 0))
        calls_in = int(centrality.get("called_by_count", 0))
        calls_out = int(centrality.get("calls_count", 0))

        connectivity_score = min(inbound + outbound + calls_in + calls_out, 40)
        if connectivity_score:
            score += connectivity_score
            reasons.append("connectivity")

        out[path] = {
            "priority_score": score,
            "priority_level": (
                "critical" if score >= 70 else
                "high" if score >= 45 else
                "medium" if score >= 20 else
                "low"
            ),
            "reasons": reasons,
        }

    return out


def build_priority_ranking(file_priority_index: dict, limit: int = 50) -> list[dict]:
    """Build a priority ranking.
    
    Parameters
    ----------
    file_priority_index : dict
        The file priority index value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict]
        The list of values.
    """
    
    ranked = [
        {
            "file": path,
            "priority_score": payload.get("priority_score", 0),
            "priority_level": payload.get("priority_level", "low"),
            "reasons": payload.get("reasons", []),
        }
        for path, payload in file_priority_index.items()
    ]
    ranked.sort(key=lambda item: (-item["priority_score"], item["file"]))
    return ranked[:limit]
