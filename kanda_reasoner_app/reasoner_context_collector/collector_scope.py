# -*- coding: utf-8 -*-
"""Central scope helpers for Project Reasoner Tab 4 collection."""
from __future__ import annotations
import fnmatch
import json
import os
from pathlib import Path
from typing import Any, Iterable, Iterator
HARD_EXCLUDED_PARTS = {"_patch_backups", "snippets", "deprecated", "backup", "backups", "archive", "oldies", "older", "legacy_cleanup", "$recycle.bin", "envs", "site-packages", ".venv", "venv", "env", "__pycache__", "mne_py3.10", "legacy_project_older", "dev_tools_docs", "_project_reference", "project_freeze_ledger", ".git", ".idea", ".vscode", ".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov", "build", "dist", "node_modules"}
FORBIDDEN_TEXT_FRAGMENTS = ("$RECYCLE.BIN", "site-packages", "legacy_cleanup", "LEGACY_PROJECT_older", "eeg_kernel_ai_neural_data_analysis", "mne_py3.10")
FORBIDDEN_ROOT_RELATIVE_PARTS = ("snippets", "_patch_backups")
DOC_SUFFIXES = {".md", ".rst", ".txt"}
PACKAGING_NAMES = {"pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "requirements-dev.txt", "poetry.lock", "pdm.lock"}

__all__ = [
    "DOC_SUFFIXES",
    "FORBIDDEN_ROOT_RELATIVE_PARTS",
    "FORBIDDEN_TEXT_FRAGMENTS",
    "HARD_EXCLUDED_PARTS",
    "PACKAGING_NAMES",
    "assert_no_forbidden_fragments",
    "is_inside_project",
    "iter_project_documentation_files",
    "iter_project_files",
    "iter_project_packaging_files",
    "iter_project_python_files",
    "resolve_project_root",
    "sanitize_collector_outputs",
    "sanitize_json_file",
]
def _safe_resolve(path: Path | str) -> Path:
    try:
        return Path(path).expanduser().resolve()
    except Exception:
        return Path(path).absolute()
def resolve_project_root(project_root: Path | str | None = None) -> Path:
    raw = project_root or os.environ.get("PROJECT_REASONER_SCAN_ROOT") or os.environ.get("PROJECT_REASONER_PROJECT_ROOT") or os.environ.get("KANDA_RUNTIME_PROJECT_ROOT") or os.getcwd()
    return _safe_resolve(raw)
def _load_rules() -> dict[str, list[str]]:
    text = os.environ.get("PROJECT_REASONER_TAB8_IGNORE_RULES_JSON", "").strip() or os.environ.get("PROJECT_REASONER_IGNORE_RULES_JSON", "").strip()
    if not text:
        return {"folders": [], "files": [], "extensions": []}
    try:
        data = json.loads(text)
    except Exception:
        return {"folders": [], "files": [], "extensions": []}
    return {"folders": list(data.get("folders", []) or []), "files": list(data.get("files", []) or []), "extensions": list(data.get("extensions", []) or [])}
def is_inside_project(path: Path | str, project_root: Path | str | None = None) -> bool:
    root = resolve_project_root(project_root)
    resolved = _safe_resolve(path)
    try:
        resolved.relative_to(root)
        return True
    except Exception:
        return False
def _relative_posix(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except Exception:
        return str(path).replace("\\", "/")
def should_exclude_path(path: Path | str, project_root: Path | str | None = None, rules: dict[str, list[str]] | None = None) -> bool:
    root = resolve_project_root(project_root)
    resolved = _safe_resolve(path)
    if not is_inside_project(resolved, root):
        return True
    parts_low = [part.lower() for part in resolved.parts]
    if any(part in HARD_EXCLUDED_PARTS for part in parts_low):
        return True
    active_rules = rules if rules is not None else _load_rules()
    rel = _relative_posix(resolved, root)
    rel_low = rel.lower()
    name_low = resolved.name.lower()
    suffix_low = resolved.suffix.lower()
    rel_parts = [part.lower() for part in Path(rel).parts]
    for folder in active_rules.get("folders", []) or []:
        f = str(folder).strip().lower().replace("\\", "/").strip("/")
        if f and (f in rel_parts or fnmatch.fnmatch(rel_low, f) or fnmatch.fnmatch(rel_low, f + "/*")):
            return True
    for file_rule in active_rules.get("files", []) or []:
        f = str(file_rule).strip().lower().replace("\\", "/")
        if f and (fnmatch.fnmatch(name_low, f) or fnmatch.fnmatch(rel_low, f)):
            return True
    for ext in active_rules.get("extensions", []) or []:
        e = str(ext).strip().lower()
        if e and suffix_low == e:
            return True
    return False
def iter_project_files(project_root: Path | str | None = None, suffixes: Iterable[str] | None = None) -> Iterator[Path]:
    root = resolve_project_root(project_root)
    rules = _load_rules()
    wanted = {s.lower() for s in suffixes} if suffixes is not None else None
    def walk(current: Path) -> Iterator[Path]:
        try:
            entries = sorted(current.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError:
            return
        for entry in entries:
            if should_exclude_path(entry, root, rules):
                continue
            if entry.is_dir():
                if entry.is_symlink():
                    continue
                yield from walk(entry)
            elif entry.is_file() and (wanted is None or entry.suffix.lower() in wanted):
                yield entry
    yield from walk(root)
def iter_project_python_files(project_root: Path | str | None = None) -> Iterator[Path]:
    yield from iter_project_files(project_root, {".py"})
def iter_project_documentation_files(project_root: Path | str | None = None) -> Iterator[Path]:
    yield from iter_project_files(project_root, DOC_SUFFIXES)
def iter_project_packaging_files(project_root: Path | str | None = None) -> Iterator[Path]:
    for path in iter_project_files(project_root, {".toml", ".py", ".cfg", ".txt", ".lock"}):
        if path.name.lower() in PACKAGING_NAMES:
            yield path
def _contains_forbidden_text(value: str, project_root: Path | str | None = None) -> bool:
    low = value.lower()
    for fragment in FORBIDDEN_TEXT_FRAGMENTS:
        if fragment.lower() in low:
            return True
    root = resolve_project_root(project_root)
    root_text = str(root).lower()
    for part in FORBIDDEN_ROOT_RELATIVE_PARTS:
        if (root_text + "\\" + part).lower() in low or (root_text.replace("\\", "/") + "/" + part).lower() in low:
            return True
    return False
def _sanitize_value(value: Any, project_root: Path | str | None = None) -> Any:
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if _contains_forbidden_text(key_text, project_root):
                continue
            cleaned[key_text] = _sanitize_value(item, project_root)
        return cleaned
    if isinstance(value, list):
        result = []
        for item in value:
            if isinstance(item, str) and _contains_forbidden_text(item, project_root):
                continue
            result.append(_sanitize_value(item, project_root))
        return result
    if isinstance(value, str):
        if _contains_forbidden_text(value, project_root):
            return "[FILTERED_NON_PROJECT_PATH]"
        return value
    return value
def sanitize_json_file(json_path: Path | str, project_root: Path | str | None = None) -> bool:
    path = Path(json_path)
    if not path.exists() or not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return False
    cleaned = _sanitize_value(data, project_root)
    original = json.dumps(data, sort_keys=True, ensure_ascii=True)
    updated = json.dumps(cleaned, sort_keys=True, ensure_ascii=True)
    if original != updated:
        path.write_text(json.dumps(cleaned, indent=2, sort_keys=True, ensure_ascii=True), encoding="utf-8")
        return True
    return False
def assert_no_forbidden_fragments(json_path: Path | str, project_root: Path | str | None = None) -> None:
    path = Path(json_path)
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    low = text.lower()
    found: list[str] = []
    for fragment in FORBIDDEN_TEXT_FRAGMENTS:
        if fragment.lower() in low:
            found.append(fragment)
    root = resolve_project_root(project_root)
    root_text = str(root)
    for part in FORBIDDEN_ROOT_RELATIVE_PARTS:
        if (root_text + "\\" + part).lower() in low or (root_text.replace("\\", "/") + "/" + part).lower() in low:
            found.append(str(root / part))
    if found:
        raise RuntimeError("forbidden path fragments remain: " + ", ".join(sorted(set(found))))
def sanitize_collector_outputs(project_root: Path | str, output_json: Path | str | None = None, runtime_trace_json: Path | str | None = None) -> None:
    root = resolve_project_root(project_root)
    if runtime_trace_json:
        sanitize_json_file(runtime_trace_json, root)
    if output_json:
        sanitize_json_file(output_json, root)
        assert_no_forbidden_fragments(output_json, root)

# PA024_UNIFIED_PROJECT_EXCLUSION_POLICY_START
from kanda_reasoner_app.project_exclusion_policy import (  # noqa: E402
    iter_reasoner_project_files as _pa024_iter_reasoner_project_files,
    load_reasoner_project_exclusion_rules as _pa024_load_reasoner_project_exclusion_rules,
    should_exclude_reasoner_project_path as _pa024_should_exclude_reasoner_project_path,
)


def _load_rules() -> dict[str, list[str]]:
    return _pa024_load_reasoner_project_exclusion_rules(resolve_project_root())


def should_exclude_path(path: Path | str, project_root: Path | str | None = None, rules: dict[str, list[str]] | None = None) -> bool:
    root = resolve_project_root(project_root)
    active_rules = rules if rules is not None else _pa024_load_reasoner_project_exclusion_rules(root)
    return _pa024_should_exclude_reasoner_project_path(path, root, active_rules)


def iter_project_files(project_root: Path | str | None = None, suffixes: Iterable[str] | None = None) -> Iterator[Path]:
    root = resolve_project_root(project_root)
    rules = _pa024_load_reasoner_project_exclusion_rules(root)
    yield from _pa024_iter_reasoner_project_files(root, suffixes=suffixes, rules=rules)


def iter_project_python_files(project_root: Path | str | None = None) -> Iterator[Path]:
    yield from iter_project_files(project_root, {".py"})


def iter_project_documentation_files(project_root: Path | str | None = None) -> Iterator[Path]:
    yield from iter_project_files(project_root, DOC_SUFFIXES)


def iter_project_packaging_files(project_root: Path | str | None = None) -> Iterator[Path]:
    for path in iter_project_files(project_root, {".toml", ".py", ".cfg", ".txt", ".lock"}):
        if path.name.lower() in PACKAGING_NAMES:
            yield path
# PA024_UNIFIED_PROJECT_EXCLUSION_POLICY_END

