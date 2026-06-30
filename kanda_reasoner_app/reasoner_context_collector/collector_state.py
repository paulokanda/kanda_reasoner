# project-path: kanda_reasoner_app/reasoner_context_collector/collector_state.py
"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from collections import defaultdict


def build_attribute_state_map(files_payload: list[dict]) -> dict:
    """Build a attribute state map.
    
    Parameters
    ----------
    files_payload : list[dict]
        The files payload value.
    
    Returns
    -------
    dict
        The mapped values.
    """
    
    state_map: dict = defaultdict(lambda: {"writers": [], "readers": []})

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            symbol = fn.get("qualname", fn.get("name", ""))

            for item in fn.get("assignments", []):
                state_map[item["target"]]["writers"].append(
                    {
                        "file": path,
                        "symbol": symbol,
                        "line": item.get("lineno"),
                    }
                )

            for item in fn.get("attribute_reads", []):
                state_map[item["attribute"]]["readers"].append(
                    {
                        "file": path,
                        "symbol": symbol,
                        "line": item.get("lineno"),
                    }
                )

        for cls in file_record.get("classes", []):
            for method in cls.get("methods", []):
                symbol = method.get("qualname", method.get("name", ""))

                for item in method.get("assignments", []):
                    state_map[item["target"]]["writers"].append(
                        {
                            "file": path,
                            "symbol": symbol,
                            "line": item.get("lineno"),
                        }
                    )

                for item in method.get("attribute_reads", []):
                    state_map[item["attribute"]]["readers"].append(
                        {
                            "file": path,
                            "symbol": symbol,
                            "line": item.get("lineno"),
                        }
                    )

    return dict(state_map)
