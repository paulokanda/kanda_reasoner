# project-path: kanda_reasoner_app/source_hygiene/ruff_quality_scope.py
"""Ruff discovery scope derived from canonical project exclusions."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Iterable

from kanda_reasoner_app.project_exclusion_policy import (
    load_reasoner_project_exclusion_rules,
)

__all__: list[str] = []


@dataclass(frozen=True)
class _RuffQualityScope:
    """Canonical exclusion evidence and Ruff CLI arguments."""

    exclusion_patterns: tuple[str, ...]
    global_argv: tuple[str, ...]
    command_argv: tuple[str, ...]
    fingerprint: str


def _build_ruff_quality_scope(project_root: Path) -> _RuffQualityScope:
    """Translate canonical project exclusions into Ruff-compatible arguments."""
    rules = load_reasoner_project_exclusion_rules(project_root)
    patterns: list[str] = []
    patterns.extend(_normalized_patterns(rules.get("folders", ())))
    patterns.extend(_normalized_patterns(rules.get("files", ())))
    patterns.extend(_extension_patterns(rules.get("extensions", ())))
    patterns.extend(_root_hidden_directory_patterns(project_root))

    deduplicated = _deduplicate_patterns(patterns)
    config_override = "extend-exclude = " + json.dumps(
        list(deduplicated),
        ensure_ascii=True,
        separators=(",", ":"),
    )

    digest = hashlib.sha256()
    for pattern in deduplicated:
        digest.update(pattern.encode("utf-8"))
        digest.update(b"\n")
    return _RuffQualityScope(
        exclusion_patterns=deduplicated,
        global_argv=("--config", config_override),
        command_argv=("--force-exclude",),
        fingerprint=digest.hexdigest(),
    )


def _normalized_patterns(values: Iterable[object]) -> list[str]:
    """Return non-empty Ruff-compatible path or glob patterns."""
    patterns: list[str] = []
    for value in values:
        text = str(value or "").strip().replace("\\", "/")
        if text:
            patterns.append(text)
    return patterns


def _extension_patterns(values: Iterable[object]) -> list[str]:
    """Convert excluded suffixes into Ruff glob patterns."""
    patterns: list[str] = []
    for value in values:
        suffix = str(value or "").strip().lower()
        if not suffix:
            continue
        if not suffix.startswith("."):
            suffix = "." + suffix
        patterns.append("*" + suffix)
    return patterns


def _root_hidden_directory_patterns(project_root: Path) -> list[str]:
    """Protect root-level hidden reference/tooling directories."""
    patterns: list[str] = []
    try:
        entries = tuple(project_root.iterdir())
    except OSError:
        return patterns
    for entry in entries:
        if entry.is_dir() and entry.name.startswith("."):
            patterns.append(entry.name)
    return patterns


def _deduplicate_patterns(values: Iterable[str]) -> tuple[str, ...]:
    """Return stable case-insensitive unique patterns."""
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        pattern = str(value or "").strip()
        marker = pattern.casefold()
        if not pattern or marker in seen:
            continue
        seen.add(marker)
        output.append(pattern)
    return tuple(output)
