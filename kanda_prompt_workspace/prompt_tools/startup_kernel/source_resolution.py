"""Startup source-map loading and canonical source resolution helpers."""

from __future__ import annotations

import json
from pathlib import Path

from startup_kernel.constants import (
    DEFAULT_SOURCE_MAP,
    SOURCE_MAP_FILENAME,
    TOOLS_DIR_NAME,
    SourceEntry,
)
from startup_kernel.generic_helpers import read_text_utf8


__all__ = []


def load_source_map(workspace_root: Path) -> list[SourceEntry]:
    candidates = [
        workspace_root / TOOLS_DIR_NAME / SOURCE_MAP_FILENAME,
        workspace_root / SOURCE_MAP_FILENAME,  # backward compatibility with v1
    ]
    source_map_path = next((p for p in candidates if p.exists()), None)

    if source_map_path is not None:
        raw = json.loads(read_text_utf8(source_map_path))
        entries = raw.get("startup_sources", raw if isinstance(raw, list) else [])
    else:
        entries = DEFAULT_SOURCE_MAP

    parsed: list[SourceEntry] = []
    seen_orders: set[int] = set()
    seen_generated: set[str] = set()
    for item in entries:
        entry = SourceEntry(
            load_order=int(item["load_order"]),
            canonical_source=str(item["canonical_source"]),
            generated_filename=str(item["generated_filename"]),
            prompt_id=str(item.get("prompt_id", Path(str(item["generated_filename"])).stem)),
            load_mode=str(item.get("load_mode", "always_startup")),
            role=str(item.get("role", "Startup prompt request kernel file.")),
        )
        if entry.load_order in seen_orders:
            raise ValueError(f"Duplicate load_order in source map: {entry.load_order}")
        if entry.generated_filename in seen_generated:
            raise ValueError(f"Duplicate generated_filename in source map: {entry.generated_filename}")
        if not entry.generated_filename.endswith(".md"):
            raise ValueError(f"Generated prompt filename must be .md: {entry.generated_filename}")
        seen_orders.add(entry.load_order)
        seen_generated.add(entry.generated_filename)
        parsed.append(entry)

    parsed.sort(key=lambda e: e.load_order)
    expected = list(range(1, len(parsed) + 1))
    actual = [e.load_order for e in parsed]
    if actual != expected:
        raise ValueError(f"load_order must be contiguous starting at 1. Expected {expected}, got {actual}")
    return parsed


def resolve_source(workspace_root: Path, entry: SourceEntry) -> tuple[Path | None, str]:
    expected = workspace_root / entry.canonical_source
    if expected.exists():
        return expected, "FOUND_BY_DECLARED_PATH"

    search_root = workspace_root / "prompt_library"
    basename = Path(entry.canonical_source).name
    if not search_root.exists():
        return None, "MISSING_PROMPT_LIBRARY_ROOT"

    matches = [p for p in search_root.rglob(basename) if p.is_file()]
    if len(matches) == 1:
        return matches[0], "FOUND_BY_UNIQUE_FILENAME_SEARCH"
    if len(matches) > 1:
        return None, f"AMBIGUOUS_FILENAME_SEARCH:{len(matches)}_matches"
    return None, "MISSING_SOURCE"
