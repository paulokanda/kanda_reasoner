"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

from collections import defaultdict


def build_subsystem_summaries(files_payload: list[dict]) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)

    for file_record in files_payload:
        path = file_record["path"]
        head = path.split("/", 1)[0]
        groups[head].append(file_record)

    results: list[dict] = []

    for name, records in sorted(groups.items()):
        files = [record["path"] for record in records]
        main_symbols: list[str] = []

        for record in records[:10]:
            for cls in record.get("classes", [])[:3]:
                main_symbols.append(cls.get("name", ""))
            for fn in record.get("functions", [])[:3]:
                main_symbols.append(fn.get("qualname", fn.get("name", "")))

        results.append(
            {
                "name": name,
                "files": files[:50],
                "main_symbols": main_symbols[:25],
                "responsibility": f"Subsystem rooted in folder '{name}'.",
            }
        )

    return results