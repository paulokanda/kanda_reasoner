"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations


def build_object_ownership_map(files_payload: list[dict]) -> list[dict]:
    results: list[dict] = []

    for file_record in files_payload:
        path = file_record["path"]

        for fn in file_record.get("functions", []):
            symbol = fn.get("qualname", fn.get("name", ""))
            for item in fn.get("assignments", []):
                target = item.get("target", "")
                if "." in target:
                    results.append(
                        {
                            "object_name": target,
                            "created_by_file": path,
                            "created_by_symbol": symbol,
                            "kind": item.get("value_type", ""),
                            "confidence": 0.7,
                        }
                    )

        for cls in file_record.get("classes", []):
            for method in cls.get("methods", []):
                symbol = method.get("qualname", method.get("name", ""))
                for item in method.get("assignments", []):
                    target = item.get("target", "")
                    if "." in target:
                        results.append(
                            {
                                "object_name": target,
                                "created_by_file": path,
                                "created_by_symbol": symbol,
                                "kind": item.get("value_type", ""),
                                "confidence": 0.7,
                            }
                        )

    return results