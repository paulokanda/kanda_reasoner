# project-path: kanda_reasoner_app/reasoner_context_collector/collector_walker.py
"""Walk project Python files while applying collector exclusion rules."""

from __future__ import annotations

import fnmatch
import json
import os
from pathlib import Path

from .collector_config import CollectorConfig
from .collector_filters import should_exclude_dir, should_exclude_file
from kanda_reasoner_app.project_exclusion_policy import (  # PA024_UNIFIED_PROJECT_EXCLUSION_POLICY_IMPORT
    load_reasoner_project_exclusion_rules as _pa024_load_reasoner_project_exclusion_rules,
)

_ALWAYS_EXCLUDED_PARTS = {
    ".env",
    ".git",
    ".hg",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "dist",
    "site-packages",
    "venv",
    ".venv",
    "env",
    "node_modules",
    "tests",
    "test",
    "dev_tools_docs",
    ".project_reference",
    "_project_reference",
    "project_freeze_ledger",
    "chat",
    "chats",
    "archive",
    "archives",
    "backup",
    "backups",
    "old",
    "older",
    "deprecated",
    "prompts",
    "prompt",
    "scratches",
    "scratch",
    "consoles",
    "console",
    "external libraries",
    "external_libraries",

    "_patch_backups",
    "snippets",
    "oldies_deprecated",
    "older_deprecated",
    "daily_refactor_report_deprecated",
    "manage_workflows_deprecated",
    "oldies",
    "tests_archive",
    "root_tests",}

_ALWAYS_EXCLUDED_FILE_MARKERS = (
    ".deprecated.",
    "_deprecated.",
    ".bak",
    ".old",
    ".orig",
)


_ALWAYS_EXCLUDED_PART_MARKERS = (
    "deprecated",
    "_deprecated",
    "backup",
    "backups",
    "archive",
    "archives",
    "oldies",
    "older",
    "legacy_cleanup",
    "import_owner_backups",
    "tab4_structure_probe",
    "tab4_post_068a_audit",
)


def _iter_prefs_path_candidates(root: Path) -> list[Path]:
    """Return possible shared GUI-prefs locations for project exclusions."""
    candidates: list[Path] = []

    for base in (root.resolve(), Path(__file__).resolve().parent):
        current = base
        for _ in range(10):
            candidate = current / ".reasoner_tools_gui_prefs.json"
            if candidate not in candidates:
                candidates.append(candidate)
            if current.parent == current:
                break
            current = current.parent

    return candidates


def _project_key_candidates(root: Path | None) -> list[str]:
    """Return possible prefs keys for a project root."""
    if root is None:
        return ["__global__"]

    keys: list[str] = []
    try:
        resolved = str(root.expanduser().resolve())
        keys.append(resolved)
        keys.append(resolved.replace("\\\\", "/"))
    except Exception:
        raw = str(root.expanduser())
        keys.append(raw)
        keys.append(raw.replace("\\\\", "/"))

    keys.append(str(root))
    keys.append(str(root).replace("\\\\", "/"))
    return list(dict.fromkeys(keys))


def _clean_rule_items(values: object, *, lower: bool = False) -> list[str]:
    """Return non-empty string rules with optional lowercase normalization."""
    if not isinstance(values, list):
        return []

    cleaned: list[str] = []
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        cleaned.append(text.lower() if lower else text)

    return list(dict.fromkeys(cleaned))


def _rules_dict_from_payload(rules: object) -> dict[str, list[str]]:
    """Convert a rules payload into normalized project-exclusion lists."""
    if not isinstance(rules, dict):
        return {"folders": [], "files": [], "extensions": []}

    return {
        "folders": _clean_rule_items(rules.get("folders", []), lower=True),
        "files": _clean_rule_items(rules.get("files", []), lower=False),
        "extensions": _clean_rule_items(rules.get("extensions", []), lower=True),
    }


def _load_project_exclusion_rules(root: Path) -> dict[str, list[str]]:
    """Load folders, files, and extensions excluded for this project root."""
    for prefs_path in _iter_prefs_path_candidates(root):
        if not prefs_path.exists():
            continue

        try:
            data = json.loads(prefs_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        project_rules = data.get("project_ignore_rules", {})
        if isinstance(project_rules, dict):
            for key in _project_key_candidates(root):
                if key in project_rules:
                    return _rules_dict_from_payload(project_rules.get(key))

        legacy_rules = data.get("ignore_rules", {})
        if isinstance(legacy_rules, dict):
            return _rules_dict_from_payload(legacy_rules)

    return {"folders": [], "files": [], "extensions": []}



def _load_env_exclusion_rules() -> dict[str, list[str]]:
    """Load Tab 8 rules exported by the GUI subprocess environment."""
    merged: dict[str, list[str]] = {"folders": [], "files": [], "extensions": []}

    for env_name in (
        "PROJECT_REASONER_TAB8_IGNORE_RULES_JSON",
        "PROJECT_REASONER_IGNORE_RULES_JSON",
    ):
        raw = os.environ.get(env_name, "").strip()
        if not raw:
            continue
        try:
            payload = json.loads(raw)
        except Exception:
            continue

        rules = _rules_dict_from_payload(payload)
        merged = _merge_exclusion_rules(merged, rules)

    return merged


def _merge_exclusion_rules(
    first: dict[str, list[str]],
    second: dict[str, list[str]],
) -> dict[str, list[str]]:
    """Merge exclusion rule dictionaries while preserving stable order."""
    merged: dict[str, list[str]] = {"folders": [], "files": [], "extensions": []}
    for key in ("folders", "files", "extensions"):
        values: list[str] = []
        for source in (first, second):
            for value in source.get(key, []):
                text = str(value or "").strip()
                if text and text not in values:
                    values.append(text)
        merged[key] = values
    return merged


def _has_excluded_part_marker(parts: list[str]) -> bool:
    """Return True when any path part is clearly marked non-project."""
    for part in parts:
        for marker in _ALWAYS_EXCLUDED_PART_MARKERS:
            if marker in part:
                return True
    return False


def _extension_set(rules: dict[str, list[str]]) -> set[str]:
    """Return normalized extension exclusions with leading dots."""
    out: set[str] = set()
    for ext in rules.get("extensions", []):
        text = str(ext or "").strip().lower()
        if not text:
            continue
        out.add(text if text.startswith(".") else f".{text}")
    return out


def _matches_user_folder_rule(part: str, rules: dict[str, list[str]]) -> bool:
    """Return True when a path part matches a user folder exclusion rule."""
    normalized = str(part or "").strip().lower()
    return any(
        fnmatch.fnmatch(normalized, pattern)
        for pattern in rules.get("folders", [])
    )


def _matches_user_file_rule(name: str, rules: dict[str, list[str]]) -> bool:
    """Return True when a file name matches an exact or glob exclusion rule."""
    lowered = str(name or "").strip().lower()
    return any(
        fnmatch.fnmatch(lowered, str(pattern).strip().lower())
        for pattern in rules.get("files", [])
    )


def _matches_user_extension_rule(name: str, rules: dict[str, list[str]]) -> bool:
    """Return True when a file extension is excluded by user rules."""
    return Path(name).suffix.lower() in _extension_set(rules)


def _normalized_parts_from_root(path: Path, root: Path) -> list[str]:
    """Support normalized parts from root behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    try:
        rel_parts = path.relative_to(root).parts
    except Exception:
        rel_parts = path.parts
    return [part.strip().lower() for part in rel_parts]


def _should_exclude_dir_path(
    entry: Path,
    root: Path,
    config: CollectorConfig,
    project_exclusion_rules: dict[str, list[str]],
) -> bool:
    """Return True when a directory is outside the project scope."""
    if should_exclude_dir(entry.name, config):
        return True

    normalized_parts = _normalized_parts_from_root(entry, root)
    if any(part in _ALWAYS_EXCLUDED_PARTS for part in normalized_parts):
        return True

    if _has_excluded_part_marker(normalized_parts):
        return True

    return any(
        _matches_user_folder_rule(part, project_exclusion_rules)
        for part in normalized_parts
    )


def _should_exclude_file_path(
    entry: Path,
    root: Path,
    config: CollectorConfig,
    project_exclusion_rules: dict[str, list[str]],
) -> bool:
    """Return True when a file is outside the project scope."""
    if should_exclude_file(entry, config):
        return True

    if _matches_user_file_rule(entry.name, project_exclusion_rules):
        return True

    if _matches_user_extension_rule(entry.name, project_exclusion_rules):
        return True

    lowered_name = entry.name.lower()
    if any(marker in lowered_name for marker in _ALWAYS_EXCLUDED_FILE_MARKERS):
        return True

    normalized_parts = _normalized_parts_from_root(entry, root)
    if any(part in _ALWAYS_EXCLUDED_PARTS for part in normalized_parts):
        return True

    if _has_excluded_part_marker(normalized_parts):
        return True

    return any(
        _matches_user_folder_rule(part, project_exclusion_rules)
        for part in normalized_parts
    )


def walk_python_files_filtered(root: Path, config: CollectorConfig) -> list[Path]:
    """Return Python files after applying config and Tab 8 exclusions."""
    project_exclusion_rules = _pa024_load_reasoner_project_exclusion_rules(root)
    results: list[Path] = []

    def _walk(current: Path) -> None:
        try:
            entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except Exception:
            return

        for entry in entries:
            if entry.is_symlink():
                continue

            if entry.is_dir():
                if _should_exclude_dir_path(entry, root, config, project_exclusion_rules):
                    continue
                _walk(entry)
                continue

            if entry.is_file() and entry.suffix.lower() == ".py":
                if _should_exclude_file_path(entry, root, config, project_exclusion_rules):
                    continue
                results.append(entry)

    _walk(root)
    return sorted(results)
