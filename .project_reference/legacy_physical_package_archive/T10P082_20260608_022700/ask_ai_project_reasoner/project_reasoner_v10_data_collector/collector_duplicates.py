"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from collections import defaultdict


def find_duplicate_symbols(files_payload: list[dict]) -> list[dict]:
    symbol_map: dict[str, list[str]] = defaultdict(list)

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            symbol_map[fn.get("name", "")].append(path)

        for cls in file_record.get("classes", []):
            symbol_map[cls.get("name", "")].append(path)
            for method in cls.get("methods", []):
                symbol_map[method.get("name", "")].append(path)

    results: list[dict] = []

    for symbol_name, occurrences in sorted(symbol_map.items()):
        unique_occurrences = sorted(set(occurrences))
        if symbol_name and len(unique_occurrences) > 1:
            results.append(
                {
                    "symbol_name": symbol_name,
                    "occurrences": unique_occurrences,
                    "kind": "name_collision",
                }
            )

    return results