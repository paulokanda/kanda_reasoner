# project-path: kanda_reasoner_app/freeze_after_update/freeze_state.py
"""Freeze-state parsing and indexing for the selected project external support box."""

from __future__ import annotations


__all__ = [
    'build_freezes',
    'build_index_payload',
    'entry_files',
    'load_freeze_index',
    'parse_frontmatter',
    'write_freeze_index',
]
import json
import re
from pathlib import Path
from typing import Any

from .paths import (
    ENTRIES_DIR_NAME,
    FREEZE_INDEX_NAME,
    MEMORY_DIR_NAME,
    build_paths,
    relative_to_project,
)
from .templates import SCHEMA_VERSION, utc_now_iso

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
_LIST_KEY_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*):\s*$")
_SCALAR_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*):\s*(?P<value>.*)$")
_LIST_ITEM_RE = re.compile(r"^\s*-\s*(?P<value>.*)$")


def _strip_quotes(value: str) -> str:
    """Support strip quotes behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    str
        The string result.
    """
    
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    if value == "null":
        return ""
    return value


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Parse the small YAML-like frontmatter used by freeze entries."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}

    data: dict[str, Any] = {}
    current_list_key: str | None = None

    for raw_line in match.group("body").splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            continue

        list_match = _LIST_ITEM_RE.match(line)
        if list_match and current_list_key:
            item = _strip_quotes(list_match.group("value"))
            current_value = data.setdefault(current_list_key, [])
            if isinstance(current_value, list):
                current_value.append(item)
            continue

        list_key_match = _LIST_KEY_RE.match(line)
        if list_key_match:
            current_list_key = list_key_match.group("key")
            data[current_list_key] = []
            continue

        scalar_match = _SCALAR_RE.match(line)
        if scalar_match:
            current_list_key = None
            data[scalar_match.group("key")] = _strip_quotes(scalar_match.group("value"))

    return data


def _legacy_entries_root(project_root: Path | str) -> Path:
    """Return legacy in-source freeze entries path."""
    paths = build_paths(project_root)
    return paths.legacy_box_root / MEMORY_DIR_NAME / ENTRIES_DIR_NAME


def _legacy_freeze_index(project_root: Path | str) -> Path:
    """Return legacy in-source freeze index path."""
    paths = build_paths(project_root)
    return paths.legacy_box_root / MEMORY_DIR_NAME / FREEZE_INDEX_NAME


def entry_files(project_root: Path | str) -> list[Path]:
    """Return project freeze entry files. Non-freeze Markdown is ignored.

    New canonical external state is read first. The legacy in-source folder is
    read only as a transition fallback when the new entries folder is absent or
    empty.
    """
    paths = build_paths(project_root)
    if paths.entries_root.is_dir():
        entries = sorted(
            path for path in paths.entries_root.glob("freeze-*.md")
            if path.is_file()
        )
        if entries:
            return entries
    legacy_entries = _legacy_entries_root(project_root)
    if not legacy_entries.is_dir():
        return []
    return sorted(
        path for path in legacy_entries.glob("freeze-*.md")
        if path.is_file()
    )


def build_freezes(project_root: Path | str) -> list[dict[str, Any]]:
    """Build freeze summaries from freeze entry frontmatter."""
    paths = build_paths(project_root)
    freezes: list[dict[str, Any]] = []

    for entry_path in entry_files(paths.project_root):
        text = entry_path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        rel_entry = relative_to_project(entry_path, paths.project_root).as_posix()
        freeze_id = str(meta.get("freeze_id") or entry_path.stem)
        protected_paths = meta.get("protected_paths")
        if not isinstance(protected_paths, list):
            protected_paths = []
        do_not_touch_summary = meta.get("do_not_touch_summary")
        if not isinstance(do_not_touch_summary, list):
            do_not_touch_summary = []

        freezes.append(
            {
                "freeze_id": freeze_id,
                "box": str(meta.get("box") or ""),
                "status": str(meta.get("status") or "frozen"),
                "date": str(meta.get("date") or ""),
                "entry": rel_entry,
                "protected_paths": [str(item) for item in protected_paths],
                "do_not_touch_summary": [str(item) for item in do_not_touch_summary],
                "superseded_by": meta.get("superseded_by") or None,
            }
        )

    return sorted(freezes, key=lambda item: str(item.get("freeze_id", "")))


def build_index_payload(project_root: Path | str) -> dict[str, Any]:
    """Build the freeze_index.json payload for the selected project external support box."""
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_by": "kanda_reasoner.freeze_after_update",
        "generated_at_utc": utc_now_iso(),
        "freezes": build_freezes(project_root),
    }


def write_freeze_index(project_root: Path | str) -> dict[str, Any]:
    """Write freeze_index.json and return the payload."""
    paths = build_paths(project_root)
    payload = build_index_payload(paths.project_root)
    paths.memory_root.mkdir(parents=True, exist_ok=True)
    paths.freeze_index.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return payload


def load_freeze_index(project_root: Path | str) -> dict[str, Any]:
    """Load and minimally validate freeze_index.json.

    New canonical external state is read first. The legacy in-source freeze
    index is read only as a transition fallback.
    """
    paths = build_paths(project_root)
    index_path = paths.freeze_index if paths.freeze_index.is_file() else _legacy_freeze_index(project_root)
    data = json.loads(index_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("freeze_index.json schema_version must be 1.0")
    if not isinstance(data.get("freezes"), list):
        raise ValueError("freeze_index.json must contain a freezes list")
    return data
