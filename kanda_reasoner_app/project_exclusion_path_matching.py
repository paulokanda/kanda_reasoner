# project-path: kanda_reasoner_app/project_exclusion_path_matching.py
"""Path matching helpers for project exclusion rules.

Folder rules are evaluated only against directory components. A file basename
must never match a folder rule merely because it contains the same text.
"""

from __future__ import annotations

import fnmatch
from pathlib import Path
from typing import Mapping, Sequence

__all__ = [
    "file_rule_matches",
    "folder_rule_matches",
    "relative_posix_path",
    "should_exclude_path_with_rules",
]


def _safe_resolve(path: Path | str) -> Path:
    """Return a best-effort resolved path."""
    try:
        return Path(path).expanduser().resolve()
    except Exception:
        return Path(path).expanduser().absolute()


def relative_posix_path(path: Path, project_root: Path) -> str:
    """Return one project-relative path with POSIX separators."""
    try:
        return path.relative_to(project_root).as_posix()
    except Exception:
        return str(path).replace("\\", "/")


def folder_rule_matches(rel_path: str, rule: str, *, path_is_dir: bool) -> bool:
    """Return whether a folder rule matches directory components of a path."""
    rule_text = str(rule).strip().lower().replace("\\", "/").strip("/")
    if not rule_text:
        return False
    rel_low = rel_path.lower().replace("\\", "/").strip("/")
    parts = [part for part in rel_low.split("/") if part]
    folder_parts = parts if path_is_dir else parts[:-1]
    if not folder_parts:
        return False
    folder_rel = "/".join(folder_parts)
    return (
        rule_text in folder_parts
        or fnmatch.fnmatch(folder_rel, rule_text)
        or fnmatch.fnmatch(folder_rel, rule_text + "/*")
        or any(fnmatch.fnmatch(part, rule_text) for part in folder_parts)
    )


def file_rule_matches(rel_path: str, name: str, rule: str) -> bool:
    """Return whether a file rule matches a file basename or relative path."""
    pattern = str(rule).strip().lower().replace("\\", "/")
    if not pattern:
        return False
    return fnmatch.fnmatch(name.lower(), pattern) or fnmatch.fnmatch(
        rel_path.lower(), pattern
    )


def should_exclude_path_with_rules(
    path: Path | str,
    project_root: Path | str,
    rules: Mapping[str, Sequence[str]],
    *,
    hidden_root_prefix: str = ".",
) -> bool:
    """Apply normalized folder, file, and extension rules to one path."""
    root = _safe_resolve(project_root)
    resolved = _safe_resolve(path)
    try:
        resolved.relative_to(root)
    except Exception:
        return True

    rel_path = relative_posix_path(resolved, root)
    rel_low = rel_path.lower().replace("\\", "/").strip("/")
    if rel_low:
        first_part = rel_low.split("/", 1)[0]
        if first_part.startswith(hidden_root_prefix):
            return True

    path_is_dir = resolved.is_dir()
    for folder in rules.get("folders", ()):
        if folder_rule_matches(rel_path, str(folder), path_is_dir=path_is_dir):
            return True

    name_low = resolved.name.lower()
    if not path_is_dir:
        for file_rule in rules.get("files", ()):
            if file_rule_matches(rel_path, name_low, str(file_rule)):
                return True

    suffix_low = resolved.suffix.lower()
    normalized_extensions = {
        text if text.startswith(".") else "." + text
        for value in rules.get("extensions", ())
        if (text := str(value).strip().lower())
    }
    return suffix_low in normalized_extensions
