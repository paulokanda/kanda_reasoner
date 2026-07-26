# project-path: kanda_reasoner_app/freeze_after_update/frozen_entry_management.py
"""Safe management operations for existing frozen-feature entry files."""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .freeze_state import entry_files, parse_frontmatter, write_freeze_index
from .paths import build_paths

__all__ = [
    "activate_frozen_entries",
    "delete_last_deprecated_entry",
    "delete_selected_deprecated_entries",
    "inactivate_frozen_entries",
    "list_managed_frozen_entries",
    "undelete_last_frozen_entry",
]

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
_ACTIVE_STATUSES = {"active", "frozen"}
_DELETED_SUFFIX = ".deleted"
_DELETED_SEPARATOR = "__"


def _entry_sort_key(path: Path) -> tuple[str, int, str]:
    """Return a newest-sortable key for one freeze entry."""
    try:
        meta = parse_frontmatter(path.read_text(encoding="utf-8-sig"))
    except Exception:
        meta = {}
    try:
        modified_ns = path.stat().st_mtime_ns
    except OSError:
        modified_ns = 0
    return str(meta.get("date") or ""), modified_ns, path.name


def _entry_metadata(path: Path) -> dict[str, Any]:
    """Return normalized display metadata for one freeze entry."""
    text = path.read_text(encoding="utf-8-sig")
    meta = parse_frontmatter(text)
    status = str(meta.get("status") or "frozen").strip().casefold()
    superseded_by = str(meta.get("superseded_by") or "").strip()
    active = status in _ACTIVE_STATUSES and not superseded_by
    return {
        "path": path,
        "filename": path.name,
        "freeze_id": str(meta.get("freeze_id") or path.stem),
        "feature_title": str(meta.get("feature_title") or meta.get("title") or path.stem),
        "box": str(meta.get("box") or meta.get("primary_box") or ""),
        "status": "active" if active else "deprecated",
        "raw_status": status or "frozen",
        "date": str(meta.get("date") or ""),
        "superseded_by": superseded_by,
        "active": active,
    }


def list_managed_frozen_entries(project_root: Path | str) -> list[dict[str, Any]]:
    """Return all canonical frozen entries, newest first."""
    candidates = sorted(entry_files(project_root), key=_entry_sort_key, reverse=True)
    result: list[dict[str, Any]] = []
    for path in candidates:
        try:
            result.append(_entry_metadata(path))
        except Exception as exc:
            result.append(
                {
                    "path": path,
                    "filename": path.name,
                    "freeze_id": path.stem,
                    "feature_title": path.stem,
                    "box": "",
                    "status": "deprecated",
                    "raw_status": "unreadable",
                    "date": "",
                    "superseded_by": "",
                    "active": False,
                    "error": str(exc),
                }
            )
    return result


def _validated_entry_paths(project_root: Path | str, paths: Iterable[Path | str]) -> list[Path]:
    """Return canonical selected entry paths or raise on path escape."""
    entries_root = build_paths(project_root).entries_root.resolve(strict=False)
    selected: list[Path] = []
    seen: set[str] = set()
    for value in paths:
        path = Path(value).expanduser().resolve(strict=False)
        try:
            path.relative_to(entries_root)
        except ValueError as exc:
            raise ValueError("Selected freeze entry is outside the canonical entries folder: " + str(path)) from exc
        if not path.is_file() or not path.name.startswith("freeze-") or path.suffix.casefold() != ".md":
            raise FileNotFoundError("Selected freeze entry is unavailable: " + str(path))
        key = str(path).casefold()
        if key not in seen:
            seen.add(key)
            selected.append(path)
    if not selected:
        raise ValueError("Select at least one frozen entry.")
    return selected


def _yaml_scalar(value: str | None) -> str:
    """Return one safe scalar for the small freeze-entry frontmatter."""
    if value is None:
        return "null"
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return '"' + escaped + '"'


def _set_frontmatter_scalars(text: str, updates: dict[str, str | None]) -> str:
    """Return entry text with selected scalar frontmatter keys updated."""
    match = _FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("Freeze entry frontmatter is missing.")
    body = match.group("body")
    for key, value in updates.items():
        replacement = key + ": " + _yaml_scalar(value)
        pattern = re.compile(r"^" + re.escape(key) + r":\s*.*$", re.MULTILINE)
        if pattern.search(body):
            body = pattern.sub(replacement, body, count=1)
        else:
            body = body.rstrip() + "\n" + replacement
    return "---\n" + body.rstrip() + "\n---\n" + text[match.end():]


def _atomic_write(path: Path, text: str) -> None:
    """Atomically replace one UTF-8 freeze entry."""
    temp_path = path.with_name(path.name + ".tmp")
    temp_path.write_text(text, encoding="utf-8", newline="\n")
    os.replace(temp_path, path)


def _set_active_state(project_root: Path | str, paths: Iterable[Path | str], *, active: bool) -> dict[str, Any]:
    """Set selected entries active or deprecated and refresh the index."""
    selected = _validated_entry_paths(project_root, paths)
    changed: list[str] = []
    for path in selected:
        text = path.read_text(encoding="utf-8-sig")
        updates: dict[str, str | None] = {"status": "frozen" if active else "deprecated"}
        if active:
            updates["superseded_by"] = None
        updated = _set_frontmatter_scalars(text, updates)
        if updated != text:
            _atomic_write(path, updated)
            changed.append(str(path))
    write_freeze_index(project_root)
    return {"ok": True, "changed_paths": changed, "active": active}


def activate_frozen_entries(project_root: Path | str, paths: Iterable[Path | str]) -> dict[str, Any]:
    """Activate selected frozen entries."""
    return _set_active_state(project_root, paths, active=True)


def inactivate_frozen_entries(project_root: Path | str, paths: Iterable[Path | str]) -> dict[str, Any]:
    """Mark selected frozen entries deprecated."""
    return _set_active_state(project_root, paths, active=False)


def _deleted_root(project_root: Path | str) -> Path:
    """Return the reversible deleted-entry folder."""
    return build_paths(project_root).memory_root / "deleted_entries"


def _deleted_name(path: Path) -> str:
    """Return a unique reversible deleted-entry filename."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return stamp + _DELETED_SEPARATOR + path.name + _DELETED_SUFFIX


def delete_selected_deprecated_entries(
    project_root: Path | str,
    paths: Iterable[Path | str],
) -> dict[str, Any]:
    """Move selected deprecated entries to reversible deleted storage."""
    selected = _validated_entry_paths(project_root, paths)
    active_paths = [path for path in selected if _entry_metadata(path)["active"]]
    if active_paths:
        raise ValueError(
            "Active frozen entries cannot be deleted. Inactivate them first: "
            + ", ".join(path.name for path in active_paths)
        )
    deleted_root = _deleted_root(project_root)
    deleted_root.mkdir(parents=True, exist_ok=True)
    moved: list[dict[str, str]] = []
    for path in selected:
        destination = deleted_root / _deleted_name(path)
        os.replace(path, destination)
        moved.append({"from": str(path), "to": str(destination)})
    write_freeze_index(project_root)
    return {"ok": True, "deleted": moved}


def delete_last_deprecated_entry(project_root: Path | str) -> dict[str, Any]:
    """Delete the newest deprecated entry."""
    for item in list_managed_frozen_entries(project_root):
        if not item["active"]:
            result = delete_selected_deprecated_entries(project_root, [item["path"]])
            result["deleted_last"] = str(item["path"])
            return result
    raise ValueError("No deprecated frozen entry is available to delete.")


def _deleted_candidates(project_root: Path | str) -> list[Path]:
    """Return reversible deletions newest first."""
    root = _deleted_root(project_root)
    if not root.is_dir():
        return []
    return sorted(
        (path for path in root.glob("*" + _DELETED_SUFFIX) if path.is_file()),
        key=lambda path: (path.stat().st_mtime_ns, path.name),
        reverse=True,
    )


def undelete_last_frozen_entry(project_root: Path | str) -> dict[str, Any]:
    """Restore the most recently deleted frozen entry."""
    candidates = _deleted_candidates(project_root)
    if not candidates:
        raise ValueError("No deleted frozen entry is available to restore.")
    deleted_path = candidates[0]
    encoded_name = deleted_path.name[: -len(_DELETED_SUFFIX)]
    if _DELETED_SEPARATOR not in encoded_name:
        raise ValueError("Deleted frozen entry has an invalid reversible name: " + deleted_path.name)
    original_name = encoded_name.split(_DELETED_SEPARATOR, 1)[1]
    destination = build_paths(project_root).entries_root / original_name
    if destination.exists():
        raise FileExistsError("Cannot restore because the original entry already exists: " + str(destination))
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.replace(deleted_path, destination)
    write_freeze_index(project_root)
    return {"ok": True, "restored_from": str(deleted_path), "restored_to": str(destination)}
