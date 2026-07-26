#!/usr/bin/env python3
# project-path: kanda_prompt_workspace/prompt_tools/startup_freeze_entry_summary.py
"""Render current freeze-entry evidence for the startup context."""

from __future__ import annotations

from pathlib import Path

__all__ = [
    "latest_freeze_entry_files",
    "parse_freeze_entry_frontmatter",
    "render_latest_freeze_entries_summary",
    "render_latest_freeze_rules_summary",
]


def parse_freeze_entry_frontmatter(text: str) -> dict[str, str]:
    """Return scalar values from one freeze-entry frontmatter block."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    result: dict[str, str] = {}
    for raw_line in parts[1].splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        if raw_line[:1].isspace() or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        clean_key = key.strip()
        clean_value = value.strip().strip('"').strip("'")
        if clean_key:
            result[clean_key] = clean_value
    return result


def _frontmatter_list(text: str, key: str) -> list[str]:
    """Return one simple YAML list from freeze-entry frontmatter."""
    if not text.startswith("---"):
        return []
    parts = text.split("---", 2)
    if len(parts) < 3:
        return []
    lines = parts[1].splitlines()
    target = key.strip() + ":"
    collecting = False
    values: list[str] = []
    for raw_line in lines:
        stripped = raw_line.strip()
        if not collecting:
            if raw_line == target:
                collecting = True
            continue
        if raw_line and not raw_line[:1].isspace():
            break
        if stripped.startswith("-"):
            value = stripped[1:].strip().strip('"').strip("'")
            if value:
                values.append(value)
    return values


def _markdown_bullets(text: str, heading: str) -> list[str]:
    """Return bullets from one exact Markdown section heading."""
    lines = text.splitlines()
    heading_key = heading.strip().casefold()
    collecting = False
    values: list[str] = []
    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith("## "):
            if collecting:
                break
            collecting = stripped.casefold() == heading_key
            continue
        if collecting and stripped.startswith("-"):
            value = stripped[1:].strip()
            if value:
                values.append(value)
    return values


def _entry_rules(text: str) -> list[str]:
    """Return deduplicated do-not-regress rules from one entry."""
    candidates = _frontmatter_list(text, "do_not_touch_summary")
    candidates.extend(_frontmatter_list(text, "do_not_regress_rules"))
    candidates.extend(_markdown_bullets(text, "## do-not-regress rules"))
    candidates.extend(_markdown_bullets(text, "## do not regress rules"))
    candidates.extend(_markdown_bullets(text, "## do not touch summary"))
    candidates.extend(_markdown_bullets(text, "## do-not-touch summary"))
    result: list[str] = []
    seen: set[str] = set()
    for value in candidates:
        normalized = " ".join(str(value).split())
        key = normalized.casefold()
        if normalized and key not in seen:
            seen.add(key)
            result.append(normalized)
    return result


def _freeze_entry_recency_key(entry_path: Path) -> tuple[str, int, str]:
    """Return a newest-sortable key for one freeze entry."""
    try:
        metadata = parse_freeze_entry_frontmatter(
            entry_path.read_text(encoding="utf-8-sig")
        )
    except OSError:
        metadata = {}
    date_text = str(metadata.get("date") or "")
    try:
        modified_ns = entry_path.stat().st_mtime_ns
    except OSError:
        modified_ns = 0
    return date_text, modified_ns, entry_path.name


def _entry_is_active(entry_path: Path) -> bool:
    """Return whether one entry is active frozen memory."""
    try:
        metadata = parse_freeze_entry_frontmatter(
            entry_path.read_text(encoding="utf-8-sig")
        )
    except OSError:
        return False
    status = str(metadata.get("status") or "frozen").strip().casefold()
    superseded_by = str(metadata.get("superseded_by") or "").strip().casefold()
    return status in {"active", "frozen"} and superseded_by in {"", "null"}


def latest_freeze_entry_files(
    memory_root: Path,
    *,
    limit: int = 12,
) -> list[Path]:
    """Return newest active freeze entries first from canonical memory."""
    entries_root = memory_root / "entries"
    if not entries_root.is_dir():
        return []
    candidates = [
        path for path in entries_root.glob("freeze-*.md")
        if path.is_file() and _entry_is_active(path)
    ]
    bounded_limit = max(1, int(limit))
    return sorted(
        candidates,
        key=_freeze_entry_recency_key,
        reverse=True,
    )[:bounded_limit]


def _relative_entry_path(entry_path: Path, memory_root: Path) -> str:
    """Return a stable relative path when possible."""
    try:
        return entry_path.relative_to(memory_root).as_posix()
    except ValueError:
        return entry_path.as_posix()


def render_latest_freeze_entries_summary(
    memory_root: Path,
    *,
    limit: int = 12,
) -> str:
    """Render newest-first freeze-entry identity evidence."""
    entries = latest_freeze_entry_files(memory_root, limit=limit)
    if not entries:
        return (
            "No freeze entry files found in the canonical external "
            "freeze memory root."
        )

    lines = [
        "LATEST_FREEZE_ENTRIES_ORDER: newest first from canonical external "
        "freeze memory.",
        "LATEST_FREEZE_ENTRIES_RULE: newest direct entry evidence overrides "
        "conflicting historical compact inventory items.",
        "FROZEN_ENTRY_AUTHORITY_RULE: frontmatter status, superseded_by, and "
        "newer corrective entries override historical pre-validation or "
        "planned-next-step prose inside already frozen entries.",
    ]
    for index, entry_path in enumerate(entries, start=1):
        try:
            text = entry_path.read_text(encoding="utf-8-sig")
            metadata = parse_freeze_entry_frontmatter(text)
        except OSError as exc:
            lines.append(
                f"{index}. unreadable entry={entry_path.as_posix()} error={exc}"
            )
            continue
        freeze_id = metadata.get("freeze_id") or entry_path.stem
        title = metadata.get("feature_title") or "untitled"
        status = metadata.get("status") or "unknown"
        date_text = metadata.get("date") or "unknown-date"
        box = metadata.get("box") or metadata.get("primary_box") or "unknown-box"
        relative = _relative_entry_path(entry_path, memory_root)
        lines.append(
            f"{index}. freeze_id={freeze_id} | title={title} | "
            f"status={status} | date={date_text} | box={box} | "
            f"entry={relative}"
        )
    return "\n".join(lines)


def render_latest_freeze_rules_summary(
    memory_root: Path,
    *,
    limit: int = 12,
    max_rules_per_entry: int = 24,
    max_total_rules: int = 160,
) -> str:
    """Render current rules from the newest directly scanned entries."""
    entries = latest_freeze_entry_files(memory_root, limit=limit)
    if not entries:
        return "No current freeze rules were available from direct entry scanning."

    lines = [
        "CURRENT_FREEZE_RULES_ORDER: newest freeze entries first.",
        "CURRENT_FREEZE_RULES_PRECEDENCE: these directly scanned rules "
        "override conflicting historical compact inventory lines.",
        "CURRENT_FREEZE_RULES_SCOPE: older entries remain available on demand "
        "and are not rewritten by this exposure view.",
        "FROZEN_ENTRY_AUTHORITY_RULE: status and newer corrective entries "
        "override historical pre-validation or planned-next-step prose.",
    ]
    total_rules = 0
    for entry_path in entries:
        try:
            text = entry_path.read_text(encoding="utf-8-sig")
            metadata = parse_freeze_entry_frontmatter(text)
        except OSError as exc:
            lines.append(
                "- unreadable entry=" + entry_path.as_posix() + " error=" + str(exc)
            )
            continue
        rules = _entry_rules(text)
        if not rules:
            continue
        freeze_id = metadata.get("freeze_id") or entry_path.stem
        title = metadata.get("feature_title") or "untitled"
        date_text = metadata.get("date") or "unknown-date"
        lines.append(
            f"ENTRY: freeze_id={freeze_id} | date={date_text} | title={title}"
        )
        for rule in rules[: max(1, int(max_rules_per_entry))]:
            if total_rules >= max(1, int(max_total_rules)):
                lines.append("- ... additional current rules hidden by startup limit")
                return "\n".join(lines)
            lines.append("- " + rule)
            total_rules += 1
    if total_rules == 0:
        lines.append("No do-not-regress rules were found in the newest entry set.")
    return "\n".join(lines)
