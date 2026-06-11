"""Support static evidence collection for Project Reasoner."""

from __future__ import annotations

import ast
import warnings
from pathlib import Path
from typing import Any


def parse_python_source_with_warnings(source: str) -> tuple[ast.AST | None, str | None, list[dict[str, Any]]]:
    captured: list[dict[str, Any]] = []

    try:
        with warnings.catch_warnings(record=True) as records:
            warnings.simplefilter("always")
            tree = ast.parse(source)

        for item in records:
            captured.append(
                {
                    "category": getattr(item.category, "__name__", ""),
                    "message": str(item.message),
                    "line": getattr(item, "lineno", None),
                }
            )

        return tree, None, captured

    except Exception as exc:
        return None, str(exc), captured


def normalize_file_warning_records(path: Path, warning_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []

    for item in warning_records:
        normalized.append(
            {
                "file": str(path),
                "category": item.get("category", ""),
                "message": item.get("message", ""),
                "line": item.get("line"),
            }
        )

    return normalized