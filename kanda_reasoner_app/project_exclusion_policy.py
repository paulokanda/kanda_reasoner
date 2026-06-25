"""Unified Project Exclusion Rules policy for all Reasoner tabs."""

from __future__ import annotations

import fnmatch
import json
import os
from pathlib import Path
from typing import Iterable, Iterator

from kanda_reasoner_app.project_root_resolver import is_reasoner_project_root

PROJECT_EXCLUSION_RULE_ENV_NAMES = (
    "PROJECT_REASONER_TAB8_IGNORE_RULES_JSON",
    "PROJECT_REASONER_IGNORE_RULES_JSON",
    "KANDA_REASONER_TAB8_IGNORE_RULES_JSON",
)
DEFAULT_PROJECT_EXCLUDED_FOLDERS = (
    "__pycache__", ".git", ".hg", ".svn", ".idea", ".vscode",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".coverage",
    "htmlcov", ".venv", "venv", "env", "build", "dist",
    "node_modules", "site-packages", ".project_reference", "_project_reference", "project_freeze_ledger",
)
DEFAULT_PROJECT_EXCLUDED_FILES = ("*.log", "*.tmp")
DEFAULT_PROJECT_EXCLUDED_EXTENSIONS = (
    ".pyc", ".pyo", ".log", ".tmp", ".bak", ".swp",
)
REASONER_PROJECT_EXCLUDED_FOLDERS = (
    "legacy_project_older",
    "snippets",
    "legacy_cleanup",
    "oldies_deprecated",
    "older_deprecated",
    "logic_insert_mssg_dcstrngs",
    "chats_insrt_mssg_dcstrngs",
    "old",
    "older",
    "oldies",
    "deprecated",
    "archive",
    "backup",
    "backups",
    "original_backups",
    "_package_move_backup",
    "zz_scalp_mesh_viewer_old_deprecated",
    "dev_tools_docs",
    "*deprecated*",
    "*older*",
    "*oldies*",
    "*backup*",
    "*copy*",
    "*scratch*",
    "workbench",
)

# Dot-prefixed directories at project root are human/tooling/reference space,
# not active project source. Keep common VCS/IDE/cache names explicit above,
# and also protect user-maintained dot folders such as .project_reference.
PROJECT_ROOT_HIDDEN_REFERENCE_DIR_PREFIX = "."


__all__ = [
    "filter_reasoner_path_strings", "iter_reasoner_project_files", "load_reasoner_project_exclusion_rules",
    "normalize_project_exclusion_rules", "project_key_candidates",
    "should_exclude_reasoner_project_path",
]


def _safe_resolve(path: Path | str) -> Path:
    try:
        return Path(path).expanduser().resolve()
    except Exception:
        return Path(path).expanduser().absolute()


def _empty_rules() -> dict[str, list[str]]:
    return {"folders": [], "files": [], "extensions": []}


def _dedupe(values: Iterable[object], *, lower: bool = False) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip()
        if not text:
            continue
        stored = text.lower() if lower else text
        marker = stored.lower()
        if marker in seen:
            continue
        seen.add(marker)
        output.append(stored)
    return output


def _normalize_extensions(values: Iterable[object]) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value or "").strip().lower()
        if not text:
            continue
        if not text.startswith("."):
            text = "." + text
        if text in seen:
            continue
        seen.add(text)
        output.append(text)
    return output


def normalize_project_exclusion_rules(payload: object) -> dict[str, list[str]]:
    if not isinstance(payload, dict):
        return _empty_rules()
    return {
        "folders": _dedupe(payload.get("folders", []), lower=True),
        "files": _dedupe(payload.get("files", []), lower=False),
        "extensions": _normalize_extensions(payload.get("extensions", [])),
    }


def _merge_rules(*rule_sets: object) -> dict[str, list[str]]:
    merged = _empty_rules()
    for rules in rule_sets:
        normalized = normalize_project_exclusion_rules(rules)
        for key in ("folders", "files", "extensions"):
            merged[key] = _dedupe(
                [*merged[key], *normalized[key]], lower=(key != "files")
            )
        merged["extensions"] = _normalize_extensions(merged["extensions"])
    return merged


def _default_rules() -> dict[str, list[str]]:
    return {
        "folders": list(DEFAULT_PROJECT_EXCLUDED_FOLDERS),
        "files": list(DEFAULT_PROJECT_EXCLUDED_FILES),
        "extensions": list(DEFAULT_PROJECT_EXCLUDED_EXTENSIONS),
    }


def _is_reasoner_project_root(project_root: Path | str | None) -> bool:
    return is_reasoner_project_root(project_root)


def _reasoner_project_rules(project_root: Path | str | None) -> dict[str, list[str]]:
    if not _is_reasoner_project_root(project_root):
        return _empty_rules()
    return {
        "folders": list(REASONER_PROJECT_EXCLUDED_FOLDERS),
        "files": ["test_*.py", "*_test.py", "conftest.py"],
        "extensions": [],
    }


def project_key_candidates(project_root: Path | str | None) -> list[str]:
    if project_root is None:
        return ["__global__"]
    raw_path = Path(str(project_root)).expanduser()
    values: list[str] = []
    for candidate in (raw_path, _safe_resolve(raw_path)):
        text = str(candidate)
        values.append(text)
        values.append(text.replace("\\", "/"))
    return _dedupe(values)


def _iter_pref_paths(project_root: Path | str | None) -> Iterator[Path]:
    seen: set[str] = set()
    roots: list[Path] = []
    if project_root is not None:
        roots.append(_safe_resolve(project_root))
    roots.append(_safe_resolve(Path.cwd()))
    roots.append(_safe_resolve(Path(__file__)).parent)
    for root in roots:
        current = root
        for _ in range(12):
            for name in (".reasoner_tools_gui_prefs.json", ".collector_runner_prefs.json"):
                candidate = current / name
                key = str(candidate).lower()
                if key not in seen:
                    seen.add(key)
                    yield candidate
            if current.parent == current:
                break
            current = current.parent


def _rules_from_environment() -> dict[str, list[str]]:
    merged = _empty_rules()
    for env_name in PROJECT_EXCLUSION_RULE_ENV_NAMES:
        text = os.environ.get(env_name, "").strip()
        if not text:
            continue
        try:
            payload = json.loads(text)
        except Exception:
            continue
        merged = _merge_rules(merged, payload)
    return merged


def _rules_from_preferences(project_root: Path | str | None) -> dict[str, list[str]]:
    merged = _empty_rules()
    keys = project_key_candidates(project_root)
    for prefs_path in _iter_pref_paths(project_root):
        if not prefs_path.exists():
            continue
        try:
            payload = json.loads(prefs_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(payload, dict):
            continue
        project_rules = payload.get("project_ignore_rules", {})
        if isinstance(project_rules, dict):
            for key in keys:
                if key in project_rules:
                    merged = _merge_rules(merged, project_rules.get(key))
                    break
        merged = _merge_rules(
            merged, payload.get("ignore_rules"), payload.get("tab8_ignore_rules"),
            payload.get("project_exclusion_rules"),
        )
    return merged


def load_reasoner_project_exclusion_rules(project_root: Path | str | None) -> dict[str, list[str]]:
    return _merge_rules(
        _default_rules(),
        _reasoner_project_rules(project_root),
        _rules_from_preferences(project_root),
        _rules_from_environment(),
    )


def _relative_posix(path: Path, project_root: Path) -> str:
    try:
        return path.relative_to(project_root).as_posix()
    except Exception:
        return str(path).replace("\\", "/")


def _is_project_root_hidden_reference_path(rel_path: str) -> bool:
    """Return True for dot-prefixed root folders that are not active project source."""

    rel_low = rel_path.lower().replace("\\", "/").strip("/")
    if not rel_low:
        return False
    first_part = rel_low.split("/", 1)[0]
    return first_part.startswith(PROJECT_ROOT_HIDDEN_REFERENCE_DIR_PREFIX)


def _folder_rule_matches(rel_path: str, rule: str) -> bool:
    rule_text = rule.strip().lower().replace("\\", "/").strip("/")
    if not rule_text:
        return False
    rel_low = rel_path.lower().replace("\\", "/").strip("/")
    parts = [part.lower() for part in Path(rel_low).parts]
    return (
        rule_text in parts or fnmatch.fnmatch(rel_low, rule_text)
        or fnmatch.fnmatch(rel_low, rule_text + "/*")
        or any(fnmatch.fnmatch(part, rule_text) for part in parts)
    )


def should_exclude_reasoner_project_path(
    path: Path | str,
    project_root: Path | str | None,
    rules: dict[str, list[str]] | None = None,
) -> bool:
    root = _safe_resolve(project_root or Path.cwd())
    resolved = _safe_resolve(path)
    try:
        resolved.relative_to(root)
    except Exception:
        return True
    active_rules = rules if rules is not None else load_reasoner_project_exclusion_rules(root)
    rel_path = _relative_posix(resolved, root)
    if _is_project_root_hidden_reference_path(rel_path):
        return True
    name_low = resolved.name.lower()
    suffix_low = resolved.suffix.lower()
    for folder in active_rules.get("folders", []):
        if _folder_rule_matches(rel_path, str(folder)):
            return True
    for file_rule in active_rules.get("files", []):
        pattern = str(file_rule).strip().lower().replace("\\", "/")
        if pattern and (
            fnmatch.fnmatch(name_low, pattern) or fnmatch.fnmatch(rel_path.lower(), pattern)
        ):
            return True
    return suffix_low in set(_normalize_extensions(active_rules.get("extensions", [])))


def iter_reasoner_project_files(
    project_root: Path | str | None,
    suffixes: Iterable[str] | None = None,
    rules: dict[str, list[str]] | None = None,
) -> Iterator[Path]:
    root = _safe_resolve(project_root or Path.cwd())
    active_rules = rules if rules is not None else load_reasoner_project_exclusion_rules(root)
    wanted = {str(s).lower() for s in suffixes} if suffixes is not None else None

    def walk(current: Path) -> Iterator[Path]:
        try:
            entries = sorted(current.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower()))
        except OSError:
            return
        for entry in entries:
            if entry.is_symlink():
                continue
            if should_exclude_reasoner_project_path(entry, root, active_rules):
                continue
            if entry.is_dir():
                yield from walk(entry)
            elif entry.is_file() and (wanted is None or entry.suffix.lower() in wanted):
                yield entry
    yield from walk(root)


def filter_reasoner_path_strings(
    paths: Iterable[str],
    project_root: Path | str | None,
    rules: dict[str, list[str]] | None = None,
) -> list[str]:
    root = _safe_resolve(project_root or Path.cwd())
    active_rules = rules if rules is not None else load_reasoner_project_exclusion_rules(root)
    output: list[str] = []
    for value in paths:
        text = str(value)
        candidate = Path(text)
        if not candidate.is_absolute():
            candidate = root / candidate
        if not should_exclude_reasoner_project_path(candidate, root, active_rules):
            output.append(text)
    return output
