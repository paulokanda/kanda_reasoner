# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_help/
# PURPOSE       : Project-specific exclusion and scope selection helpers
# EXPORTS       : load_project_exclusion_rules, normalize_rel_path, should_exclude_path, iter_python_files, iter_selected_python_files, resolve_target_module_path, resolve_target_package_path, is_test_like_path, is_relaxed_path
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Project-specific exclusion and scope selection helpers."""

from __future__ import annotations

import logging

import fnmatch
import json
import os
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".coverage",
    "htmlcov",
    "build",
    "dist",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "tests",
    "test",
    ".project_reference",
    "_project_reference",
    "project_freeze_ledger",
}

RELAXED_PATH_PREFIXES = (
    "temp/",
    "developer_tools/",
    "original_backups/",
    "_phase3_tmp_project/",
)

__all__ = [
    "load_project_exclusion_rules",
    "normalize_rel_path",
    "should_exclude_path",
    "iter_python_files",
    "iter_selected_python_files",
    "resolve_target_module_path",
    "resolve_target_package_path",
    "is_test_like_path",
    "is_relaxed_path",
]


def _iter_prefs_path_candidates(root: Path | None) -> Iterable[Path]:
    """Yield candidate shared GUI prefs paths for project exclusion rules."""
    seen: set[Path] = set()

    if root is not None:
        try:
            current = root.expanduser().resolve()
        except Exception:
            current = root.expanduser()

        for _ in range(10):
            candidate = current / ".reasoner_tools_gui_prefs.json"
            if candidate not in seen:
                seen.add(candidate)
                yield candidate
            if current.parent == current:
                break
            current = current.parent

    current = Path(__file__).resolve().parent
    for _ in range(10):
        candidate = current / ".reasoner_tools_gui_prefs.json"
        if candidate not in seen:
            seen.add(candidate)
            yield candidate
        if current.parent == current:
            break
        current = current.parent

def _clean_rule_items(values: object, *, lower: bool = False) -> list[str]:
    """Return non-empty exclusion rule strings with optional normalization."""
    if not isinstance(values, list):
        return []

    cleaned: list[str] = []
    for value in values:
        item = str(value or "").strip()
        if not item:
            continue
        cleaned.append(item.lower() if lower else item)

    return list(dict.fromkeys(cleaned))

def _project_key_candidates(root: Path | None) -> list[str]:
    """Return possible project-specific keys stored by the unified GUI."""
    if root is None:
        return ["__global__"]

    keys: list[str] = []
    try:
        resolved = str(root.expanduser().resolve())
        keys.append(resolved)
        keys.append(resolved.replace("\\", "/"))
    except Exception:
        raw = str(root.expanduser())
        keys.append(raw)
        keys.append(raw.replace("\\", "/"))

    raw_text = str(root)
    keys.append(raw_text)
    keys.append(raw_text.replace("\\", "/"))
    return list(dict.fromkeys(keys))

def _rules_dict_from_payload(rules: object) -> dict[str, list[str]]:
    """Normalize a raw exclusion-rule payload from prefs."""
    if not isinstance(rules, dict):
        return {"folders": [], "files": [], "extensions": []}

    return {
        "folders": _clean_rule_items(rules.get("folders", []), lower=True),
        "files": _clean_rule_items(rules.get("files", []), lower=False),
        "extensions": _clean_rule_items(rules.get("extensions", []), lower=True),
    }

def load_project_exclusion_rules(root: Path) -> dict[str, list[str]]:
    """Load Tab 8 project-specific exclusions for the selected project root."""
    for prefs_path in _iter_prefs_path_candidates(root):
        if not prefs_path.exists():
            continue

        try:
            data = json.loads(prefs_path.read_text(encoding="utf-8"))
        except Exception:
            logging.exception("Boundary failure in load_project_exclusion_rules")
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

def _extension_set(project_exclusion_rules: dict[str, list[str]]) -> set[str]:
    """Return normalized extension exclusions with leading dots."""
    result: set[str] = set()
    for item in project_exclusion_rules.get("extensions", []):
        text = str(item or "").strip().lower()
        if not text:
            continue
        result.add(text if text.startswith(".") else f".{text}")
    return result

def _matches_project_folder_rule(
    part: str,
    project_exclusion_rules: dict[str, list[str]],
) -> bool:
    """Return whether a path component matches a project folder exclusion."""
    normalized = str(part or "").strip().lower()
    return any(
        fnmatch.fnmatch(normalized, pattern)
        for pattern in project_exclusion_rules.get("folders", [])
    )

def _matches_project_file_rule(
    filename: str,
    project_exclusion_rules: dict[str, list[str]],
) -> bool:
    """Return whether a filename matches a project file exclusion."""
    lowered = str(filename or "").strip().lower()
    return any(
        fnmatch.fnmatch(lowered, str(pattern).strip().lower())
        for pattern in project_exclusion_rules.get("files", [])
    )

def _matches_project_extension_rule(
    filename: str,
    project_exclusion_rules: dict[str, list[str]],
) -> bool:
    """Return whether a filename suffix is excluded for this project."""
    return Path(filename).suffix.lower() in _extension_set(project_exclusion_rules)

def _rel_path_has_project_folder_exclusion(
    rel_path: str,
    project_exclusion_rules: dict[str, list[str]],
) -> bool:
    """Return whether any relative path component is excluded."""
    parts = Path(rel_path.replace("\\", "/")).parts
    return any(
        _matches_project_folder_rule(part, project_exclusion_rules)
        for part in parts
    )

def normalize_rel_path(root: Path, path: Path) -> str:
    """Normalize  rel path."""
    
    return str(path.relative_to(root)).replace("\\", "/").lstrip("./")

def is_transitional_copy_filename(filename: str) -> bool:
    """Return whether transitional copy filename."""
    
    lowered = filename.lower()
    return " - copy" in lowered or lowered.startswith("copy of ")

def is_test_like_path(rel_path: str) -> bool:
    """Return whether test like path."""
    
    lowered = rel_path.lower()
    name = Path(lowered).name

    if lowered.startswith("step12_checks/"):
        return True
    if name == "conftest.py":
        return True
    if name.startswith("test_") and name.endswith(".py"):
        return True
    if name.endswith("_test.py"):
        return True

    return False

def is_relaxed_path(rel_path: str, filename: str) -> bool:
    """Return whether relaxed path."""
    
    lowered = rel_path.lower()

    if lowered.startswith(RELAXED_PATH_PREFIXES):
        return True
    if "/older/" in lowered:
        return True
    if "/backup/" in lowered or "/backups/" in lowered:
        return True
    if is_transitional_copy_filename(filename):
        return True
    if "to restore if needed" in filename.lower():
        return True

    return False

def should_exclude_path(
    rel_path: str,
    filename: str,
    *,
    include_relaxed_paths: bool,
    include_tests: bool,
    project_exclusion_rules: dict[str, list[str]] | None = None,
) -> bool:
    """Return whether a path should be skipped by scope or exclusion rules."""
    if not include_relaxed_paths and is_relaxed_path(rel_path, filename):
        return True
    if not include_tests and is_test_like_path(rel_path):
        return True

    rules = project_exclusion_rules or {"folders": [], "files": [], "extensions": []}
    if _rel_path_has_project_folder_exclusion(rel_path, rules):
        return True
    if _matches_project_file_rule(filename, rules):
        return True
    if _matches_project_extension_rule(filename, rules):
        return True

    return False

def iter_python_files(
    root: Path,
    project_exclusion_rules: dict[str, list[str]] | None = None,
) -> Iterable[Path]:
    """Yield Python files that are part of the selected project."""
    rules = project_exclusion_rules or {"folders": [], "files": [], "extensions": []}

    for dirpath, dirnames, filenames in os.walk(root):
        path_obj = Path(dirpath)

        dirnames[:] = [
            name
            for name in dirnames
            if name not in DEFAULT_EXCLUDE_DIRS
            and not _matches_project_folder_rule(name, rules)
        ]

        rel_dir = normalize_rel_path(root, path_obj) if path_obj != root else ""
        if rel_dir and _rel_path_has_project_folder_exclusion(rel_dir, rules):
            continue

        for filename in filenames:
            if _matches_project_file_rule(filename, rules):
                continue
            if _matches_project_extension_rule(filename, rules):
                continue
            if filename.endswith(".py"):
                yield path_obj / filename

def _is_within_root(root: Path, candidate: Path) -> bool:
    """Handle is within root."""
    
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False

def resolve_target_module_path(root: Path, target_module: str | None) -> Path | None:
    """Resolve  target module path."""
    
    if target_module is None:
        return None
    value = target_module.strip()
    if not value or value == "*":
        return None

    direct = Path(value)
    candidates: list[Path] = []

    if direct.is_absolute():
        candidates.append(direct)
    else:
        if any(sep in value for sep in ("/", "\\")) or value.endswith(".py"):
            candidates.append(root / direct)
        dotted_parts = [part for part in value.split(".") if part]
        if dotted_parts:
            candidates.append(root.joinpath(*dotted_parts).with_suffix(".py"))
            candidates.append(root.joinpath(*dotted_parts) / "__init__.py")

    for candidate in candidates:
        if not _is_within_root(root, candidate):
            continue
        resolved = candidate.resolve()
        if resolved.exists() and resolved.is_file() and resolved.suffix == ".py":
            return resolved

    return None

def resolve_target_package_path(root: Path, target_package: str | None) -> Path | None:
    """Resolve  target package path."""
    
    if target_package is None:
        return None
    value = target_package.strip()
    if not value or value == "*":
        return None

    direct = Path(value)
    candidates: list[Path] = []

    if direct.is_absolute():
        candidates.append(direct)
    else:
        if any(sep in value for sep in ("/", "\\")):
            candidates.append(root / direct)
        dotted_parts = [part for part in value.split(".") if part]
        if dotted_parts:
            candidates.append(root.joinpath(*dotted_parts))

    for candidate in candidates:
        if not _is_within_root(root, candidate):
            continue
        resolved = candidate.resolve()
        if resolved.exists() and resolved.is_dir():
            return resolved

    return None

def iter_selected_python_files(
    root: Path,
    target_module: str | None = None,
    target_package: str | None = None,
    project_exclusion_rules: dict[str, list[str]] | None = None,
) -> Iterable[Path]:
    """Handle iter selected python files."""
    
    if target_module and target_package:
        raise ValueError("Only one of target_module or target_package may be provided.")

    if target_package:
        selected_dir = resolve_target_package_path(root, target_package)
        if selected_dir is None:
            raise FileNotFoundError(
                "Target package/folder not found under project root: "
                f"{target_package!r}. Use a relative folder path, absolute folder path under the root, "
                "or dotted package name."
            )
        yield from iter_python_files(selected_dir, project_exclusion_rules)
        return

    selected = resolve_target_module_path(root, target_module)
    if selected is None:
        if target_module and target_module.strip() and target_module.strip() != "*":
            raise FileNotFoundError(
                "Target module not found under project root: "
                f"{target_module!r}. Use a relative .py path, absolute path under the root, "
                "or dotted module name."
            )
        yield from iter_python_files(root, project_exclusion_rules)
        return
    yield selected
