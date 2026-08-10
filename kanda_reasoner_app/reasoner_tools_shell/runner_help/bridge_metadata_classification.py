# project-path: kanda_reasoner_app/reasoner_tools_shell/runner_help/bridge_metadata_classification.py
"""Metadata helpers for current startup and on-demand bridge classification."""

from __future__ import annotations

import json
import re
from pathlib import Path

__all__ = [
    "bridge_display_name",
    "is_active_on_demand_bridge",
    "prompt_front_matter",
    "startup_source_records",
]

_FRONT_MATTER_FIELD_RE = re.compile(
    r"(?:^|\s)(prompt_id|title|status|load_type|active_route):\s*"
    r"(.*?)(?=\s+(?:prompt_code|prompt_id|title|version|status|load_type|active_route|"
    r"owner_box|owner_group|created_by_patch|source_stage|updated_for):|$)",
    re.IGNORECASE,
)
_ACTIVE_PROMPT_STATUSES = {"active", "current"}
_BLOCKED_ON_DEMAND_LOAD_TYPES = {"always_startup", "never"}


def startup_source_records(workspace: Path | None) -> list[dict[str, object]]:
    """Return current startup source-map records, or an empty list."""
    if workspace is None:
        return []
    source_map = workspace / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"
    try:
        payload = json.loads(source_map.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    records = payload.get("startup_sources") if isinstance(payload, dict) else None
    if not isinstance(records, list):
        return []
    return [record for record in records if isinstance(record, dict)]


def prompt_front_matter(text: str) -> dict[str, str]:
    """Parse the compact front-matter fields used for bridge routing."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    front_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        front_lines.append(line.strip())
    front = " ".join(front_lines)
    metadata: dict[str, str] = {}
    for match in _FRONT_MATTER_FIELD_RE.finditer(front):
        metadata[match.group(1).lower()] = match.group(2).strip().strip("\"'")
    return metadata


def is_active_on_demand_bridge(metadata: dict[str, str]) -> bool:
    """Return True only for current non-startup, non-tombstone bridges."""
    status = metadata.get("status", "").strip().lower()
    load_type = metadata.get("load_type", "").strip().lower()
    active_route = metadata.get("active_route", "").strip().lower()
    if status not in _ACTIVE_PROMPT_STATUSES:
        return False
    if load_type in _BLOCKED_ON_DEMAND_LOAD_TYPES or not load_type:
        return False
    return active_route not in {"false", "no", "0"}


def bridge_display_name(path: object, metadata: dict[str, str]) -> str:
    """Return a stable bridge display identity."""
    prompt_id = metadata.get("prompt_id", "").strip()
    if prompt_id:
        return prompt_id
    title = metadata.get("title", "").strip()
    if title:
        return title
    name = getattr(path, "name", str(path))
    for suffix in (".meta.json", ".md", ".json", ".txt"):
        if name.lower().endswith(suffix):
            return name[: -len(suffix)]
    return name
