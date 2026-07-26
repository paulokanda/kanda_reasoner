# project-path: kanda_reasoner_app/reasoner_symbol_atlas/evidence_merger_helpers_private.py
"""Private helpers for Project Symbol Atlas evidence merging."""

from __future__ import annotations

from .schemas import (
    ProjectModuleRecord,
    ProjectSymbol,
    normalize_project_atlas_text,
)

_MERGE_STATUS_LIVE_ONLY = "live_only"
_MERGE_STATUS_JSON_ADVISORY = "json_advisory"
_MERGE_STATUS_JSON_REJECTED = "json_rejected"

__all__: list[str] = []


def _merge_canonical_modules(
    live_modules: tuple[ProjectModuleRecord, ...],
    json_modules: tuple[ProjectModuleRecord, ...],
) -> tuple[ProjectModuleRecord, ...]:
    """Support merge canonical modules behavior.
    
    Parameters
    ----------
    live_modules : tuple[ProjectModuleRecord, ...]
        The live modules value.
    json_modules : tuple[ProjectModuleRecord, ...]
        The json modules value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    json_by_path = {module.path.replace("\\", "/"): module for module in json_modules}
    live_by_path = {module.path.replace("\\", "/"): module for module in live_modules}
    merged: list[ProjectModuleRecord] = []
    for path_key in sorted(set(json_by_path) | set(live_by_path)):
        live = live_by_path.get(path_key)
        json_module = json_by_path.get(path_key)
        if live is not None and json_module is not None:
            merged.append(
                _copy_module_with_extra_evidence(
                    live,
                    tuple(json_module.evidence) + ("merge: canonical_json_enrichment",),
                )
            )
        elif json_module is not None:
            merged.append(
                _copy_module_with_extra_evidence(
                    json_module,
                    ("merge: canonical_json_only",),
                )
            )
        elif live is not None:
            merged.append(
                _copy_module_with_extra_evidence(
                    live,
                    ("merge: live_post_evidence_candidate",),
                )
            )
    return tuple(sorted(merged, key=lambda item: (item.path, item.module)))


def _merge_fresh_modules(
    live_modules: tuple[ProjectModuleRecord, ...],
    json_modules: tuple[ProjectModuleRecord, ...],
) -> tuple[ProjectModuleRecord, ...]:
    """Support merge fresh modules behavior.
    
    Parameters
    ----------
    live_modules : tuple[ProjectModuleRecord, ...]
        The live modules value.
    json_modules : tuple[ProjectModuleRecord, ...]
        The json modules value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    json_by_path = {module.path.replace("\\", "/"): module for module in json_modules}
    merged: list[ProjectModuleRecord] = []
    for live in live_modules:
        json_module = json_by_path.get(live.path.replace("\\", "/"))
        if json_module is None:
            merged.append(_copy_module_with_extra_evidence(live, ("merge: live_ast_only",)))
        else:
            merged.append(
                _copy_module_with_extra_evidence(
                    live,
                    tuple(json_module.evidence) + ("merge: fresh_json_enrichment",),
                )
            )
    return tuple(sorted(merged, key=lambda item: (item.path, item.module)))


def _merge_fresh_symbols(
    live_symbols: tuple[ProjectSymbol, ...],
    json_symbols: tuple[ProjectSymbol, ...],
) -> tuple[ProjectSymbol, ...]:
    """Support merge fresh symbols behavior.
    
    Parameters
    ----------
    live_symbols : tuple[ProjectSymbol, ...]
        The live symbols value.
    json_symbols : tuple[ProjectSymbol, ...]
        The json symbols value.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    merged_by_key: dict[tuple[str, str, str], ProjectSymbol] = {
        _symbol_key(symbol): symbol for symbol in live_symbols
    }
    for json_symbol in json_symbols:
        key = _symbol_key(json_symbol)
        existing = merged_by_key.get(key)
        if existing is None:
            merged_by_key[key] = _copy_symbol_with_extra_evidence(
                json_symbol,
                ("merge: json_symbol_not_seen_in_live_ast",),
            )
        else:
            merged_by_key[key] = _copy_symbol_with_extra_evidence(
                existing,
                tuple(json_symbol.evidence) + ("merge: fresh_json_symbol_enrichment",),
            )
    return tuple(sorted(merged_by_key.values(), key=lambda item: (item.path, item.line or 0, item.name)))


def _tag_live_modules_for_advisory_status(
    modules: tuple[ProjectModuleRecord, ...],
    merge_status: str,
) -> tuple[ProjectModuleRecord, ...]:
    """Support tag live modules for advisory status behavior.
    
    Parameters
    ----------
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    merge_status : str
        The merge status value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    evidence = ("merge: " + merge_status,)
    return tuple(_copy_module_with_extra_evidence(module, evidence) for module in modules)


def _copy_module_with_extra_evidence(
    module: ProjectModuleRecord,
    evidence: tuple[str, ...],
) -> ProjectModuleRecord:
    """Support copy module with extra evidence behavior.
    
    Parameters
    ----------
    module : ProjectModuleRecord
        The module value.
    evidence : tuple[str, ...]
        The evidence value.
    
    Returns
    -------
    ProjectModuleRecord
        The project module record result.
    """
    
    merged_evidence = tuple(dict.fromkeys(tuple(module.evidence) + evidence))
    symbols = tuple(_copy_symbol_with_extra_evidence(symbol, evidence) for symbol in module.symbols)
    return ProjectModuleRecord(
        module=module.module,
        path=module.path,
        line_count=module.line_count,
        is_package_init=module.is_package_init,
        is_test_file=module.is_test_file,
        owner_role=module.owner_role,
        symbols=symbols,
        imports=module.imports,
        evidence=merged_evidence,
    )


def _copy_symbol_with_extra_evidence(
    symbol: ProjectSymbol,
    evidence: tuple[str, ...],
) -> ProjectSymbol:
    """Support copy symbol with extra evidence behavior.
    
    Parameters
    ----------
    symbol : ProjectSymbol
        The symbol value.
    evidence : tuple[str, ...]
        The evidence value.
    
    Returns
    -------
    ProjectSymbol
        The project symbol result.
    """
    
    merged_evidence = tuple(dict.fromkeys(tuple(symbol.evidence) + evidence))
    return ProjectSymbol(
        name=symbol.name,
        kind=symbol.kind,
        module=symbol.module,
        path=symbol.path,
        line=symbol.line,
        is_public=symbol.is_public,
        owner_role=symbol.owner_role,
        exported_by_all=symbol.exported_by_all,
        evidence=merged_evidence,
    )


def _symbols_from_modules(modules: tuple[ProjectModuleRecord, ...]) -> tuple[ProjectSymbol, ...]:
    """Support symbols from modules behavior.
    
    Parameters
    ----------
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    symbols: list[ProjectSymbol] = []
    for module in modules:
        symbols.extend(module.symbols)
    return tuple(sorted(symbols, key=lambda item: (item.path, item.line or 0, item.name)))


def _symbol_key(symbol: ProjectSymbol) -> tuple[str, str, str]:
    """Support symbol key behavior.
    
    Parameters
    ----------
    symbol : ProjectSymbol
        The symbol value.
    
    Returns
    -------
    tuple[str, str, str]
        The tuple of values.
    """
    
    return (
        normalize_project_atlas_text(symbol.path).replace("\\", "/"),
        normalize_project_atlas_text(symbol.name),
        normalize_project_atlas_text(symbol.kind),
    )


def _input_sources_for_non_enriched_merge(status: str, json_path: str) -> tuple[str, ...]:
    """Support input sources for non enriched merge behavior.
    
    Parameters
    ----------
    status : str
        The status value.
    json_path : str
        The json path value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    if status == _MERGE_STATUS_LIVE_ONLY:
        return ("live_ast", "owner_classifier")
    if status == _MERGE_STATUS_JSON_ADVISORY:
        return ("live_ast", "owner_classifier", "complete_json_advisory", json_path)
    if status == _MERGE_STATUS_JSON_REJECTED:
        return ("live_ast", "owner_classifier", "complete_json_rejected", json_path)
    return ("live_ast", "owner_classifier")
