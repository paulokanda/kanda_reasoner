"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations


def _find_matching_symbols(files_payload: list[dict], terms: list[str]) -> list[dict]:
    matches: list[dict] = []

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            name = fn.get("qualname", fn.get("name", "")).lower()
            if any(term in name for term in terms):
                matches.append(
                    {
                        "file": path,
                        "symbol": fn.get("qualname", fn.get("name", "")),
                    }
                )

        for cls in file_record.get("classes", []):
            cls_name = cls.get("name", "").lower()
            if any(term in cls_name for term in terms):
                matches.append(
                    {
                        "file": path,
                        "symbol": cls.get("name", ""),
                    }
                )
            for method in cls.get("methods", []):
                name = method.get("qualname", method.get("name", "")).lower()
                if any(term in name for term in terms):
                    matches.append(
                        {
                            "file": path,
                            "symbol": method.get("qualname", method.get("name", "")),
                        }
                    )

    return matches


def derive_startup_chain(files_payload: list[dict], entry_files: list[str]) -> list[dict]:
    steps: list[dict] = []

    for idx, entry in enumerate(entry_files[:8], start=1):
        steps.append(
            {
                "step": idx,
                "file": entry,
                "symbol": "__main__",
                "why": "entrypoint candidate",
            }
        )

    for item in _find_matching_symbols(files_payload, ["display", "build_and_show", "main", "launcher"])[:12]:
        steps.append(
            {
                "step": len(steps) + 1,
                "file": item["file"],
                "symbol": item["symbol"],
                "why": "startup-related symbol",
            }
        )

    return steps


def derive_timeline_chain(files_payload: list[dict]) -> list[dict]:
    matches = _find_matching_symbols(files_payload, ["timeline"])
    return [
        {
            "step": idx,
            "file": item["file"],
            "symbol": item["symbol"],
            "why": "timeline-related symbol",
        }
        for idx, item in enumerate(matches[:20], start=1)
    ]


def derive_topomap_chain(files_payload: list[dict]) -> list[dict]:
    matches = _find_matching_symbols(files_payload, ["topomap", "amplitude_map", "mcrvlt"])
    return [
        {
            "step": idx,
            "file": item["file"],
            "symbol": item["symbol"],
            "why": "topomap-related symbol",
        }
        for idx, item in enumerate(matches[:20], start=1)
    ]


def derive_reset_chain(files_payload: list[dict]) -> list[dict]:
    matches = _find_matching_symbols(files_payload, ["reset", "snapshot", "cleanup", "close"])
    return [
        {
            "step": idx,
            "file": item["file"],
            "symbol": item["symbol"],
            "why": "reset-related symbol",
        }
        for idx, item in enumerate(matches[:20], start=1)
    ]


def build_execution_chains(files_payload: list[dict], entry_files: list[str]) -> dict:
    return {
        "startup_chain": derive_startup_chain(files_payload, entry_files),
        "timeline_chain": derive_timeline_chain(files_payload),
        "topomap_chain": derive_topomap_chain(files_payload),
        "reset_chain": derive_reset_chain(files_payload),
    }