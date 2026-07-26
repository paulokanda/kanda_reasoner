"""Source-map parsing helpers for startup prompt candidate audits."""

from __future__ import annotations
__all__: list[str] = []


import re
from pathlib import Path
from typing import Any

from .audit_startup_candidates_models import (
    ALLOWED_SOURCE_MAP_KEYS,
    GENERATED_FILENAME_RE,
    PROMPT_ID_RE,
    REQUIRED_SOURCE_MAP_KEYS,
    SourceMapEntry,
    read_json_file,
)

def parse_source_map(source_map_path: Path) -> tuple[list[SourceMapEntry], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    raw = read_json_file(source_map_path)
    if not isinstance(raw, dict):
        raise ValueError("Source map must be a JSON object.")

    if "schema_version" not in raw:
        warnings.append("Source map has no schema_version field. Consider adding schema_version: 1 later.")

    sources = raw.get("startup_sources")
    if not isinstance(sources, list):
        raise ValueError("Source map must contain a startup_sources list.")

    entries: list[SourceMapEntry] = []
    seen_orders: dict[int, str] = {}
    seen_canonical: dict[str, str] = {}
    seen_generated: dict[str, str] = {}
    seen_prompt_ids: dict[str, str] = {}

    for index, item in enumerate(sources, start=1):
        label = f"startup_sources[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label}: entry must be a JSON object.")
            continue

        missing_keys = sorted(REQUIRED_SOURCE_MAP_KEYS - set(item.keys()))
        extra_keys = sorted(set(item.keys()) - ALLOWED_SOURCE_MAP_KEYS)
        if missing_keys:
            errors.append(f"{label}: missing required keys: {missing_keys}")
            continue
        if extra_keys:
            warnings.append(f"{label}: extra keys present: {extra_keys}")

        try:
            load_order = int(item["load_order"])
        except (TypeError, ValueError):
            errors.append(f"{label}: load_order must be an integer.")
            continue

        canonical_source = str(item["canonical_source"])
        generated_filename = str(item["generated_filename"])
        prompt_id = str(item["prompt_id"])
        load_mode = str(item["load_mode"])
        role = str(item["role"])

        if "\\" in canonical_source:
            warnings.append(f"{label}: canonical_source should use forward slashes: {canonical_source}")

        if "/" in generated_filename or "\\" in generated_filename:
            errors.append(f"{label}: generated_filename must not contain path separators: {generated_filename}")
        elif not generated_filename.endswith(".md"):
            errors.append(f"{label}: generated_filename must end with .md: {generated_filename}")
        elif not GENERATED_FILENAME_RE.match(generated_filename):
            warnings.append(
                f"{label}: generated_filename should be numbered like 08_name.md: {generated_filename}"
            )

        if load_mode != "always_startup":
            warnings.append(f"{label}: v1 expects load_mode always_startup, got {load_mode}")

        if not role.strip():
            errors.append(f"{label}: role must be non-empty.")

        if not prompt_id.strip():
            errors.append(f"{label}: prompt_id must be non-empty.")
        elif not PROMPT_ID_RE.match(prompt_id):
            warnings.append(
                f"{label}: prompt_id should be lowercase alphanumeric plus underscores: {prompt_id}"
            )

        if load_order in seen_orders:
            errors.append(
                f"{label}: duplicate load_order {load_order}; already used by {seen_orders[load_order]}"
            )
        seen_orders[load_order] = label

        canonical_key = canonical_source.replace("\\", "/")
        if canonical_key in seen_canonical:
            errors.append(
                f"{label}: duplicate canonical_source {canonical_key}; already used by {seen_canonical[canonical_key]}"
            )
        seen_canonical[canonical_key] = label

        if generated_filename in seen_generated:
            errors.append(
                f"{label}: duplicate generated_filename {generated_filename}; already used by {seen_generated[generated_filename]}"
            )
        seen_generated[generated_filename] = label

        if prompt_id in seen_prompt_ids:
            errors.append(
                f"{label}: duplicate prompt_id {prompt_id}; already used by {seen_prompt_ids[prompt_id]}"
            )
        seen_prompt_ids[prompt_id] = label

        entries.append(
            SourceMapEntry(
                load_order=load_order,
                canonical_source=canonical_key,
                generated_filename=generated_filename,
                prompt_id=prompt_id,
                load_mode=load_mode,
                role=role,
                raw=item,
            )
        )

    if entries:
        actual_orders = sorted(entry.load_order for entry in entries)
        expected_orders = list(range(1, len(entries) + 1))
        if actual_orders != expected_orders:
            errors.append(
                "load_order values must be contiguous starting at 1. "
                f"Expected {expected_orders}, got {actual_orders}."
            )

    return entries, errors, warnings
def detect_stale_entries(workspace_root: Path, entries: list[SourceMapEntry]) -> list[str]:
    stale: list[str] = []
    for entry in entries:
        source_path = workspace_root / entry.canonical_source
        if not source_path.exists():
            stale.append(
                f"{entry.generated_filename}: canonical_source missing: {entry.canonical_source}"
            )
    return stale
def load_source_map_object(source_map_path: Path) -> dict[str, Any]:
    raw = read_json_file(source_map_path)
    if not isinstance(raw, dict):
        raise ValueError("Source map must be a JSON object.")
    if not isinstance(raw.get("startup_sources"), list):
        raise ValueError("Source map must contain a startup_sources list.")
    return raw
def suggested_next_load_order(entries: list[SourceMapEntry]) -> int:
    return max((entry.load_order for entry in entries), default=0) + 1
def suggested_next_filename_number(entries: list[SourceMapEntry]) -> int:
    numbers: list[int] = []
    for entry in entries:
        match = re.match(r"^([0-9]{2})_", entry.generated_filename)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1
