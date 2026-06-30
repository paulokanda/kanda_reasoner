# project-path: kanda_reasoner_app/reasoner_context_collector/collector_insights.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from typing import Any


def get_top_priority_files(payload: dict[str, Any], limit: int = 10) -> list[dict[str, Any]]:
    """Return the top priority files.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    ranking = payload.get("priority_ranking", [])
    if not isinstance(ranking, list):
        return []

    valid_items: list[dict[str, Any]] = []
    for item in ranking:
        if isinstance(item, dict):
            valid_items.append(item)

    sorted_items = sorted(
        valid_items,
        key=lambda item: float(item.get("priority_score", 0.0)),
        reverse=True,
    )
    return sorted_items[:limit]


def get_project_hotspot_summary(payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Return the project hotspot summary.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    
    Returns
    -------
    dict[str, list[dict[str, Any]]]
        The mapped values.
    """
    
    hotspots = payload.get("project_hotspots", {})
    if not isinstance(hotspots, dict):
        return {
            "top_modules": [],
            "top_symbols": [],
        }

    top_modules = hotspots.get("top_modules", [])
    top_symbols = hotspots.get("top_symbols", [])

    if not isinstance(top_modules, list):
        top_modules = []
    if not isinstance(top_symbols, list):
        top_symbols = []

    return {
        "top_modules": [item for item in top_modules if isinstance(item, dict)],
        "top_symbols": [item for item in top_symbols if isinstance(item, dict)],
    }


def get_top_central_symbols(payload: dict[str, Any], limit: int = 10) -> list[dict[str, Any]]:
    """Return the top central symbols.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    limit : int, optional
        The optional limit value.
    
    Returns
    -------
    list[dict[str, Any]]
        The list of values.
    """
    
    centrality_index = payload.get("symbol_centrality_index", {})
    if not isinstance(centrality_index, dict):
        return []

    rows: list[dict[str, Any]] = []
    for symbol, data in centrality_index.items():
        if not isinstance(data, dict):
            continue
        rows.append(
            {
                "symbol": symbol,
                "score": float(data.get("score", 0.0)),
                "inbound_calls": int(data.get("inbound_calls", 0)),
                "outbound_calls": int(data.get("outbound_calls", 0)),
            }
        )

    rows.sort(key=lambda item: item["score"], reverse=True)
    return rows[:limit]


def get_entry_chain_summary(payload: dict[str, Any]) -> dict[str, Any]:
    """Return the entry chain summary.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    
    Returns
    -------
    dict[str, Any]
        The mapped values.
    """
    
    project_summary = payload.get("project_summary", {})
    execution_chains = payload.get("execution_chains", {})

    if not isinstance(project_summary, dict):
        project_summary = {}
    if not isinstance(execution_chains, dict):
        execution_chains = {}

    entry_files = project_summary.get("entry_files", [])
    if not isinstance(entry_files, list):
        entry_files = []

    entry_chains: dict[str, list[dict[str, Any]]] = {}

    for entry_file in entry_files:
        chains = execution_chains.get(entry_file, [])
        if not isinstance(chains, list):
            chains = []

        entry_chains[str(entry_file)] = [
            item for item in chains if isinstance(item, dict)
        ]

    return {
        "entry_files": entry_files,
        "entry_chains": entry_chains,
    }
