# project-path: kanda_reasoner_app/reasoner_symbol_atlas/_related_file_finder_support.py
"""Private helpers for the Project Symbol Atlas related file finder."""

from __future__ import annotations

from pathlib import Path as _Path

from .output_policy import is_active_atlas_path
from .schemas import (
    ProjectModuleRecord as _ProjectModuleRecord,
    normalize_project_atlas_text as _normalize_project_atlas_text,
)

from ._related_file_finder_path_helpers_private import (
    _contains_any,
    _limited_unique_paths,
    _normalize_path,
    _relative_path,
    _unique_paths,
    _unique_strings,
)

__all__: list[str] = []

_GENERIC_SEARCH_TERMS = {
    "ai",
    "ask",
    "project",
    "reasoner",
    "tools",
    "tool",
    "gui",
    "panel",
    "safety",
    "engineering",
    "symbol",
    "atlas",
}

_RELATED_SUPPORT_SUFFIXES = (
    "_commands",
    "_command",
    "_helpers",
    "_helper",
    "_actions",
    "_action",
    "_adapter",
    "_adapters",
    "_writer",
    "_writers",
    "_schema",
    "_schemas",
    "_mapper",
    "_resolver",
    "_classifier",
    "_scanner",
    "_indexer",
    "_report",
    "_reports",
    "_utils",
    "_utility",
    "_utilities",
)


def _resolve_target_module(
    modules: tuple[_ProjectModuleRecord, ...],
    target_path: str,
    symbol_name: str,
) -> _ProjectModuleRecord | None:
    """Support resolve target module behavior.
    
    Parameters
    ----------
    modules : tuple[_ProjectModuleRecord, ...]
        The modules value.
    target_path : str
        The target path value.
    symbol_name : str
        The symbol name value.
    
    Returns
    -------
    _ProjectModuleRecord | None
        The project module record result.
    """
    
    normalized_target = _normalize_path(target_path)
    if normalized_target:
        for module in modules:
            if _normalize_path(module.path) == normalized_target:
                return module
            if _normalize_path(module.path).endswith("/" + normalized_target):
                return module
    normalized_symbol = _normalize_project_atlas_text(symbol_name)
    if normalized_symbol:
        for module in modules:
            for symbol in module.symbols:
                if symbol.name == normalized_symbol:
                    return module
    return None


def _search_terms(target_path: str, symbol_name: str) -> tuple[str, ...]:
    """Support search terms behavior.
    
    Parameters
    ----------
    target_path : str
        The target path value.
    symbol_name : str
        The symbol name value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    terms: list[str] = []
    normalized_target = _normalize_path(target_path)
    if normalized_target:
        stem = _Path(normalized_target).stem
        terms.extend(_stem_terms(stem))
        terms.append(normalized_target)
    normalized_symbol = _normalize_project_atlas_text(symbol_name)
    if normalized_symbol:
        terms.extend(_stem_terms(normalized_symbol))
        terms.append(normalized_symbol)
    return _unique_strings(_filter_search_terms(terms))


def _filter_search_terms(terms: list[str]) -> list[str]:
    """Support filter search terms behavior.
    
    Parameters
    ----------
    terms : list[str]
        The terms value.
    
    Returns
    -------
    list[str]
        The list of values.
    """
    
    filtered: list[str] = []
    for term in terms:
        cleaned = _normalize_project_atlas_text(term).lower().replace("-", "_")
        if not cleaned:
            continue
        if cleaned in _GENERIC_SEARCH_TERMS:
            continue
        if len(cleaned) < 3:
            continue
        filtered.append(term)
    return filtered


def _stem_terms(stem: str) -> tuple[str, ...]:
    """Support stem terms behavior.
    
    Parameters
    ----------
    stem : str
        The stem value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    cleaned = _normalize_project_atlas_text(stem).replace("-", "_")
    if not cleaned:
        return tuple()
    parts = [part for part in cleaned.split("_") if part]
    terms = [cleaned]
    if len(parts) > 1:
        terms.append("_".join(parts[: min(len(parts), 4)]))
        if len(parts) >= 3:
            terms.append("_".join(parts[-3:]))
        if len(parts) >= 4:
            terms.append("_".join(parts[-4:]))
        for index in range(0, len(parts) - 1):
            terms.append("_".join(parts[index : index + 2]))
        for index in range(0, len(parts) - 2):
            terms.append("_".join(parts[index : index + 3]))
        terms.extend(parts)
    return tuple(terms)


def _support_helpers_from_modules(
    modules: tuple[_ProjectModuleRecord, ...],
    search_terms: tuple[str, ...],
) -> tuple[str, ...]:
    """Support support helpers from modules behavior.
    
    Parameters
    ----------
    modules : tuple[_ProjectModuleRecord, ...]
        The modules value.
    search_terms : tuple[str, ...]
        The search terms value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    paths: list[str] = []
    for module in modules:
        normalized = _normalize_path(module.path)
        if not is_active_atlas_path(normalized):
            continue
        stem = _Path(normalized).stem.lower()
        if not _contains_any(stem, search_terms):
            continue
        if any(stem.endswith(suffix) for suffix in _RELATED_SUPPORT_SUFFIXES):
            paths.append(module.path)
    return tuple(paths)


def _related_test_files(
    project_root: _Path,
    modules: tuple[_ProjectModuleRecord, ...],
    search_terms: tuple[str, ...],
    include_tests: bool,
) -> tuple[str, ...]:
    """Support related test files behavior.
    
    Parameters
    ----------
    project_root : _Path
        The project root path.
    modules : tuple[_ProjectModuleRecord, ...]
        The modules value.
    search_terms : tuple[str, ...]
        The search terms value.
    include_tests : bool
        The include tests value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    if not include_tests:
        return tuple()
    paths: list[str] = []
    for module in modules:
        if not module.is_test_file:
            continue
        normalized = _normalize_path(module.path).lower()
        if not is_active_atlas_path(normalized):
            continue
        if _contains_any(normalized, search_terms):
            paths.append(module.path)
    tests_root = project_root / "tests"
    if tests_root.exists():
        for file_path in tests_root.rglob("test_*.py"):
            relative = _relative_path(project_root, file_path)
            if is_active_atlas_path(relative) and _contains_any(relative.lower(), search_terms):
                paths.append(relative)
    return _unique_paths(tuple(paths))


def _related_workbench_files(
    project_root: _Path,
    search_terms: tuple[str, ...],
    category: str,
    include_workbench: bool,
) -> tuple[str, ...]:
    """Support related workbench files behavior.
    
    Parameters
    ----------
    project_root : _Path
        The project root path.
    search_terms : tuple[str, ...]
        The search terms value.
    category : str
        The category value.
    include_workbench : bool
        The include workbench value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    if not include_workbench:
        return tuple()
    workbench_root = project_root / "workbench"
    if not workbench_root.exists():
        return tuple()
    paths: list[str] = []
    for pattern in _workbench_patterns(category):
        for file_path in workbench_root.rglob(pattern):
            relative = _relative_path(project_root, file_path)
            if _contains_any(relative.lower(), search_terms):
                paths.append(relative)
    return _unique_paths(tuple(paths))


def _workbench_patterns(category: str) -> tuple[str, ...]:
    """Support workbench patterns behavior.
    
    Parameters
    ----------
    category : str
        The category value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    if category == "manifest":
        return ("BUNDLE_MANIFEST*.txt", "*manifest*.md", "*manifest*.json")
    if category == "diagnostic":
        return ("*diagnostic*.py", "*diagnostic*.txt", "*diagnostic*.json", "*status*.md")
    if category == "patch_apply":
        return ("*APPLY*.py", "*APPLY*.ps1", "*patch*.py", "*repair*.py")
    return ("*",)


def _related_evidence_files(
    project_root: _Path,
    search_terms: tuple[str, ...],
    include_evidence_files: bool,
) -> tuple[str, ...]:
    """Support related evidence files behavior.
    
    Parameters
    ----------
    project_root : _Path
        The project root path.
    search_terms : tuple[str, ...]
        The search terms value.
    include_evidence_files : bool
        The include evidence files value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    if not include_evidence_files:
        return tuple()
    evidence_root = project_root / "project_analysis_evidence"
    if not evidence_root.exists():
        return tuple()
    paths: list[str] = []
    for file_path in evidence_root.rglob("*.json"):
        relative = _relative_path(project_root, file_path)
        if _contains_any(relative.lower(), search_terms) or "complete" in relative.lower():
            paths.append(relative)
    return _unique_paths(tuple(paths))


def _tests_to_run(test_files: tuple[str, ...], target_path: str) -> tuple[str, ...]:
    """Support tests to run behavior.
    
    Parameters
    ----------
    test_files : tuple[str, ...]
        The test files value.
    target_path : str
        The target path value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    commands: list[str] = []
    for path in test_files:
        if path.endswith(".py"):
            commands.append("python " + path)
    if target_path.endswith(".py"):
        commands.append("python -m py_compile " + target_path)
    commands.append(
        "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py "
        "--root <PROJECT_ROOT> --validate"
    )
    commands.append(
        "python kanda_reasoner_app\\manage_workflows\\manage_workflows.py "
        "--root <PROJECT_ROOT> --validate"
    )
    return _unique_strings(commands)


def _evidence_lines(
    merge_status: str,
    target_path: str,
    main_helper_status: str,
    facade_status: str,
    search_terms: tuple[str, ...],
    related_files: tuple[str, ...],
) -> tuple[str, ...]:
    """Support evidence lines behavior.
    
    Parameters
    ----------
    merge_status : str
        The merge status value.
    target_path : str
        The target path value.
    main_helper_status : str
        The main helper status value.
    facade_status : str
        The facade status value.
    search_terms : tuple[str, ...]
        The search terms value.
    related_files : tuple[str, ...]
        The related files value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return (
        "related_file_finder: read_only",
        "merge_status: " + merge_status,
        "target_path: " + target_path,
        "main_helper_status: " + main_helper_status,
        "facade_status: " + facade_status,
        "search_terms: " + ", ".join(search_terms),
        "related_file_count: " + str(len(related_files)),
    )


def _looks_like_main(path_value: str) -> bool:
    """Support looks like main behavior.
    
    Parameters
    ----------
    path_value : str
        The path value value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    stem = _Path(_normalize_path(path_value)).stem.lower()
    if not stem:
        return False
    return not any(stem.endswith(suffix) for suffix in _RELATED_SUPPORT_SUFFIXES)


