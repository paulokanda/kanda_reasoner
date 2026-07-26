# project-path: kanda_reasoner_app/reasoner_symbol_atlas/existing_code_finder_matching_private.py
"""Private matching helpers for existing-code finder."""

from __future__ import annotations

from .schemas import (
    ProjectSymbol,
    normalize_project_atlas_sequence,
    normalize_project_atlas_text,
)
from .shadow_report import collect_reasoner_symbol_atlas_shadow_findings

__all__: list[str] = []


def _choose_query_type(options: ProjectSymbolAtlasExistingCodeFinderOptions) -> str:
    """Support choose query type behavior.
    
    Parameters
    ----------
    options : ProjectSymbolAtlasExistingCodeFinderOptions
        The option values.
    
    Returns
    -------
    str
        The string result.
    """
    
    query_type = options.normalized_query_type()
    if query_type != "auto":
        return query_type
    if options.target_path and (options.task_description or options.symbol_name):
        return "pre_patch_gate"
    if options.target_path:
        return "related_files"
    if options.symbol_name or options.query_text:
        return "symbol"
    return "auto"


def _matching_symbols(
    symbols: tuple[ProjectSymbol, ...],
    symbol_name: str,
    exact: bool,
    include_private: bool,
    max_matches: int,
) -> tuple[ProjectSymbol, ...]:
    """Support matching symbols behavior.
    
    Parameters
    ----------
    symbols : tuple[ProjectSymbol, ...]
        The symbols value.
    symbol_name : str
        The symbol name value.
    exact : bool
        The exact value.
    include_private : bool
        The include private value.
    max_matches : int
        The max matches value.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    if not symbol_name:
        return ()
    needle = symbol_name.lower()
    matches: list[ProjectSymbol] = []
    for symbol in symbols:
        if not include_private and not symbol.is_public:
            continue
        name = symbol.name.lower()
        if (exact and name == needle) or (not exact and needle in name):
            matches.append(symbol)
    matches.sort(key=lambda item: (item.name.lower(), item.path, item.line or 0))
    return tuple(matches[: max(1, int(max_matches))])


def _matching_duplicate_symbols(
    options: ProjectSymbolAtlasExistingCodeFinderOptions,
    symbol_name: str,
) -> tuple[ProjectSymbol, ...]:
    """Support matching duplicate symbols behavior.
    
    Parameters
    ----------
    options : ProjectSymbolAtlasExistingCodeFinderOptions
        The option values.
    symbol_name : str
        The symbol name value.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    if not symbol_name:
        return ()
    try:
        duplicates = collect_reasoner_symbol_atlas_shadow_findings(
            options.project_root,
            options=options.to_shadow_options(),
        )
    except (FileNotFoundError, NotADirectoryError, OSError, ValueError):
        return ()
    needle = symbol_name.lower()
    return tuple(symbol for symbol in duplicates if symbol.name.lower() == needle)


def _owner_paths(matches: tuple[ProjectSymbol, ...], facade_owner_path: str) -> tuple[str, ...]:
    """Support owner paths behavior.
    
    Parameters
    ----------
    matches : tuple[ProjectSymbol, ...]
        The matches value.
    facade_owner_path : str
        The facade owner path value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    paths = [symbol.path for symbol in matches if symbol.path]
    if facade_owner_path:
        paths.append(facade_owner_path)
    return _unique_strings(paths)


def _query_reasons(
    query_type: str,
    matches: tuple[ProjectSymbol, ...],
    duplicate_symbols: tuple[ProjectSymbol, ...],
) -> tuple[str, ...]:
    """Support query reasons behavior.
    
    Parameters
    ----------
    query_type : str
        The query type value.
    matches : tuple[ProjectSymbol, ...]
        The matches value.
    duplicate_symbols : tuple[ProjectSymbol, ...]
        The duplicate symbols value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    reasons = ["Existing code finder query type: " + query_type]
    if matches:
        reasons.append("Symbol matches found: " + str(len(matches)))
    else:
        reasons.append("No live symbol matches found for query.")
    if duplicate_symbols:
        reasons.append("Duplicate public symbol risk found for query.")
    return tuple(reasons)


def _merge_reasons(*groups: tuple[str, ...]) -> tuple[str, ...]:
    """Support merge reasons behavior.
    
    Parameters
    ----------
    *groups : tuple[str, ...]
        The groups value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    values: list[str] = []
    for group in groups:
        values.extend(group)
    return _unique_strings(values)


def _unique_strings(values: Any) -> tuple[str, ...]:
    """Support unique strings behavior.
    
    Parameters
    ----------
    values : Any
        The input values.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    output: list[str] = []
    seen: set[str] = set()
    for value in normalize_project_atlas_sequence(values):
        item = normalize_project_atlas_text(value)
        if item and item not in seen:
            output.append(item)
            seen.add(item)
    return tuple(output)
