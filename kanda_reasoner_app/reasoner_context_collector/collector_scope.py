# -*- coding: utf-8 -*-
# project-path: kanda_reasoner_app/reasoner_context_collector/collector_scope.py
"""Central scope helpers for Project Reasoner Tab 4 collection."""
from __future__ import annotations
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
    """Support safe resolve behavior.
    
    Parameters
    ----------
    path : Path | str
        The file or folder path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    try:
        return Path(path).expanduser().resolve()
    except Exception:
        return Path(path).absolute()
def resolve_project_root(project_root: Path | str | None = None) -> Path:
    """Resolve the project root.
    
    Parameters
    ----------
    project_root : Path | str | None, optional
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    raw = project_root or os.environ.get("PROJECT_REASONER_SCAN_ROOT") or os.environ.get("PROJECT_REASONER_PROJECT_ROOT") or os.environ.get("KANDA_RUNTIME_PROJECT_ROOT") or os.getcwd()
    return _safe_resolve(raw)
def _load_rules() -> dict[str, list[str]]:
    """Support load rules behavior.
    
    Returns
    -------
    dict[str, list[str]]
        The mapped values.
    """
    
    text = os.environ.get("PROJECT_REASONER_TAB8_IGNORE_RULES_JSON", "").strip() or os.environ.get("PROJECT_REASONER_IGNORE_RULES_JSON", "").strip()
    if not text:
        return {"folders": [], "files": [], "extensions": []}
    try:
        data = json.loads(text)
    except Exception:
        return {"folders": [], "files": [], "extensions": []}
    return {"folders": list(data.get("folders", []) or []), "files": list(data.get("files", []) or []), "extensions": list(data.get("extensions", []) or [])}
def is_inside_project(path: Path | str, project_root: Path | str | None = None) -> bool:
    """Return whether inside project.
    
    Parameters
    ----------
    path : Path | str
        The file or folder path.
    project_root : Path | str | None, optional
        The project root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    root = resolve_project_root(project_root)
    resolved = _safe_resolve(path)
    try:
        resolved.relative_to(root)
        return True
    except Exception:
        return False
def _relative_posix(path: Path, root: Path) -> str:
    """Support relative posix behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    try:
        return path.relative_to(root).as_posix()
    except Exception:
        return str(path).replace("\\", "/")
def _contains_forbidden_text(value: str, project_root: Path | str | None = None) -> bool:
    """Support contains forbidden text behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    project_root : Path | str | None, optional
        The project root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
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
    """Support sanitize value behavior.
    
    Parameters
    ----------
    value : Any
        The input value.
    project_root : Path | str | None, optional
        The project root path.
    
    Returns
    -------
    Any
        The any result.
    """
    
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
    """Support sanitize json file behavior.
    
    Parameters
    ----------
    json_path : Path | str
        The json path value.
    project_root : Path | str | None, optional
        The project root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
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
    """Support assert no forbidden fragments behavior.
    
    Parameters
    ----------
    json_path : Path | str
        The json path value.
    project_root : Path | str | None, optional
        The project root path.
    """
    
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
    """Support sanitize collector outputs behavior.
    
    Parameters
    ----------
    project_root : Path | str
        The project root path.
    output_json : Path | str | None, optional
        The optional output json value.
    runtime_trace_json : Path | str | None, optional
        The optional runtime trace json value.
    """
    
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
    """Support load rules behavior.
    
    Returns
    -------
    dict[str, list[str]]
        The mapped values.
    """
    
    return _pa024_load_reasoner_project_exclusion_rules(resolve_project_root())

def should_exclude_path(path: Path | str, project_root: Path | str | None = None, rules: dict[str, list[str]] | None = None) -> bool:
    """Support should exclude path behavior.
    
    Parameters
    ----------
    path : Path | str
        The file or folder path.
    project_root : Path | str | None, optional
        The project root path.
    rules : dict[str, list[str]] | None, optional
        The optional rules value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    root = resolve_project_root(project_root)
    active_rules = rules if rules is not None else _pa024_load_reasoner_project_exclusion_rules(root)
    return _pa024_should_exclude_reasoner_project_path(path, root, active_rules)

def iter_project_files(project_root: Path | str | None = None, suffixes: Iterable[str] | None = None) -> Iterator[Path]:
    """Support iter project files behavior.
    
    Parameters
    ----------
    project_root : Path | str | None, optional
        The project root path.
    suffixes : Iterable[str] | None, optional
        The optional suffixes value.
    
    Returns
    -------
    Iterator[Path]
        The iterator result.
    """
    
    root = resolve_project_root(project_root)
    rules = _pa024_load_reasoner_project_exclusion_rules(root)
    yield from _pa024_iter_reasoner_project_files(root, suffixes=suffixes, rules=rules)

def iter_project_python_files(project_root: Path | str | None = None) -> Iterator[Path]:
    """Support iter project python files behavior.
    
    Parameters
    ----------
    project_root : Path | str | None, optional
        The project root path.
    
    Returns
    -------
    Iterator[Path]
        The iterator result.
    """
    
    yield from iter_project_files(project_root, {".py"})

def iter_project_documentation_files(project_root: Path | str | None = None) -> Iterator[Path]:
    """Support iter project documentation files behavior.
    
    Parameters
    ----------
    project_root : Path | str | None, optional
        The project root path.
    
    Returns
    -------
    Iterator[Path]
        The iterator result.
    """
    
    yield from iter_project_files(project_root, DOC_SUFFIXES)

def iter_project_packaging_files(project_root: Path | str | None = None) -> Iterator[Path]:
    """Support iter project packaging files behavior.
    
    Parameters
    ----------
    project_root : Path | str | None, optional
        The project root path.
    
    Returns
    -------
    Iterator[Path]
        The iterator result.
    """
    
    for path in iter_project_files(project_root, {".toml", ".py", ".cfg", ".txt", ".lock"}):
        if path.name.lower() in PACKAGING_NAMES:
            yield path
# PA024_UNIFIED_PROJECT_EXCLUSION_POLICY_END

