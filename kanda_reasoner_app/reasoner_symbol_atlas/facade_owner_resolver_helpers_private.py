# project-path: kanda_reasoner_app/reasoner_symbol_atlas/facade_owner_resolver_helpers_private.py
"""Private helpers for Project Symbol Atlas facade owner resolution."""

from __future__ import annotations

from pathlib import Path

from .output_policy import is_active_owner_candidate
from .schemas import ProjectModuleRecord, ProjectSymbol

_STATUS_NO_FACADE = "no_facade"
_STATUS_NEEDS_OWNER_REVIEW = "needs_owner_review"
_STATUS_OWNER_NOT_FOUND = "owner_not_found"

__all__: list[str] = []


def _coerce_project_root(project_root: str | Path) -> Path:
    """Support coerce project root behavior.
    
    Parameters
    ----------
    project_root : str | Path
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    root = Path(project_root).expanduser().resolve(strict=False)
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError("Project root is not a directory: " + str(project_root))
    return root


def _normalize_relative_path(path_text: str) -> str:
    """Support normalize relative path behavior.
    
    Parameters
    ----------
    path_text : str
        The path text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not path_text:
        return ""
    return str(Path(path_text)).replace("\\", "/")


def _find_target_record(
    project_root: Path,
    modules: tuple[ProjectModuleRecord, ...],
    target_path: str,
) -> ProjectModuleRecord | None:
    """Support find target record behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    target_path : str
        The target path value.
    
    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """
    
    if not target_path:
        return None
    target = Path(target_path)
    if target.is_absolute():
        try:
            target_key = str(target.resolve(strict=False).relative_to(project_root)).replace("\\", "/")
        except ValueError:
            target_key = str(target).replace("\\", "/")
    else:
        target_key = _normalize_relative_path(target_path)
    for record in modules:
        record_key = _normalize_relative_path(record.path)
        if record_key == target_key:
            return record
    target_name = target.name
    matches = [record for record in modules if Path(record.path).name == target_name]
    if len(matches) == 1:
        return matches[0]
    return None


def _record_is_facade(record: ProjectModuleRecord) -> bool:
    """Support record is facade behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if record.owner_role in {"facade", "compatibility_facade"}:
        return True
    evidence_text = "\n".join(record.evidence).lower()
    if "facade_shape_candidate: true" in evidence_text:
        return True
    if "module_getattr_export_detected: true" in evidence_text:
        return True
    if "reexport_" in evidence_text:
        return True
    import_symbol_count = len([symbol for symbol in record.symbols if symbol.kind == "import"])
    local_public_count = len(
        [
            symbol
            for symbol in record.symbols
            if symbol.kind != "import" and symbol.is_public and symbol.name != "__all__"
        ]
    )
    return import_symbol_count > 0 and local_public_count == 0


def _facade_evidence(record: ProjectModuleRecord) -> tuple[str, ...]:
    """Support facade evidence behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    values: list[str] = []
    for item in record.evidence:
        lowered = item.lower()
        if "facade" in lowered or "reexport" in lowered or "explicit_all" in lowered or "getattr" in lowered:
            values.append(item)
    for symbol in record.symbols:
        if symbol.kind == "import":
            values.extend(symbol.evidence)
    return tuple(dict.fromkeys(values))


def _source_modules_from_import_symbol(symbol: ProjectSymbol) -> tuple[str, ...]:
    """Support source modules from import symbol behavior.
    
    Parameters
    ----------
    symbol : ProjectSymbol
        The symbol value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    values: list[str] = []
    for item in symbol.evidence:
        if not item.startswith("source: "):
            continue
        source = item[len("source: ") :].strip()
        if not source:
            continue
        if source.startswith("."):
            continue
        parts = source.split(".")
        if len(parts) > 1:
            values.append(".".join(parts[:-1]))
        values.append(source)
    return tuple(dict.fromkeys(values))


def _record_for_module_name(
    modules: tuple[ProjectModuleRecord, ...],
    module_name: str,
) -> ProjectModuleRecord | None:
    """Support record for module name behavior.
    
    Parameters
    ----------
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    module_name : str
        The module name value.
    
    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """
    
    if not module_name:
        return None
    for record in modules:
        if record.module == module_name:
            return record
    module_suffix = "." + module_name
    for record in modules:
        if record.module.endswith(module_suffix):
            return record
    return None


def _all_candidate_owner_paths(
    target_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
    symbols: tuple[ProjectSymbol, ...],
    symbol_name: str,
) -> tuple[str, ...]:
    """Return all evidence-backed owner paths before active-scope partitioning."""
    candidates: list[str] = []
    for symbol in target_record.symbols:
        if symbol.kind != "import":
            continue
        if symbol_name and symbol.name != symbol_name:
            continue
        for module_name in _source_modules_from_import_symbol(symbol):
            record = _record_for_module_name(modules, module_name)
            if record is not None and record.path != target_record.path:
                candidates.append(record.path)
    if symbol_name:
        for symbol in symbols:
            if symbol.name != symbol_name or symbol.path == target_record.path:
                continue
            if symbol.kind == "import":
                continue
            record = _record_for_path(modules, symbol.path)
            if record is not None and not _record_is_facade(record):
                candidates.append(record.path)
    return tuple(dict.fromkeys(candidates))


def _candidate_owner_paths(
    target_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
    symbols: tuple[ProjectSymbol, ...],
    symbol_name: str,
) -> tuple[str, ...]:
    """Return active owner candidates before canonical owner ranking."""
    candidates = _all_candidate_owner_paths(
        target_record,
        modules,
        symbols,
        symbol_name,
    )
    return tuple(
        path
        for path in candidates
        if _record_is_active_owner_candidate(_record_for_path(modules, path))
    )


def _inactive_candidate_owner_paths(
    target_record: ProjectModuleRecord,
    modules: tuple[ProjectModuleRecord, ...],
    symbols: tuple[ProjectSymbol, ...],
    symbol_name: str,
) -> tuple[str, ...]:
    """Return owner candidates excluded from active canonical ranking."""
    candidates = _all_candidate_owner_paths(
        target_record,
        modules,
        symbols,
        symbol_name,
    )
    return tuple(
        path
        for path in candidates
        if not _record_is_active_owner_candidate(_record_for_path(modules, path))
    )


def _record_for_path(
    modules: tuple[ProjectModuleRecord, ...],
    path_text: str,
) -> ProjectModuleRecord | None:
    """Support record for path behavior.
    
    Parameters
    ----------
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    path_text : str
        The path text value.
    
    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """
    
    key = _normalize_relative_path(path_text)
    for record in modules:
        if _normalize_relative_path(record.path) == key:
            return record
    return None


def _record_is_active_owner_candidate(
    record: ProjectModuleRecord | None,
) -> bool:
    """Return True when a module may compete for canonical ownership."""
    if record is None:
        return False
    return is_active_owner_candidate(
        record.path,
        record.owner_role,
        record.is_test_file,
    )


def _select_likely_owner(
    modules: tuple[ProjectModuleRecord, ...],
    candidate_paths: tuple[str, ...],
) -> ProjectModuleRecord | None:
    """Support select likely owner behavior.
    
    Parameters
    ----------
    modules : tuple[ProjectModuleRecord, ...]
        The modules value.
    candidate_paths : tuple[str, ...]
        The candidate paths value.
    
    Returns
    -------
    ProjectModuleRecord | None
        The project module record result.
    """
    
    records = [_record_for_path(modules, path) for path in candidate_paths]
    records = [
        record for record in records if _record_is_active_owner_candidate(record)
    ]
    if not records:
        return None
    non_facades = [record for record in records if not _record_is_facade(record)]
    if non_facades:
        records = non_facades
    role_order = {
        "canonical_owner": 0,
        "private_helper": 1,
        "unknown": 2,
        "ambiguous_owner": 3,
        "facade": 4,
        "compatibility_facade": 4,
    }
    records.sort(key=lambda record: (role_order.get(record.owner_role, 9), record.path))
    return records[0]


def _decision_status(
    target_record: ProjectModuleRecord,
    target_is_facade: bool,
    likely_owner: ProjectModuleRecord | None,
    owner_candidates: tuple[str, ...],
    inactive_owner_candidates: tuple[str, ...],
    merge_status: str,
) -> tuple[str, str, bool, tuple[str, ...]]:
    """Support decision status behavior.
    
    Parameters
    ----------
    target_record : ProjectModuleRecord
        The target record value.
    target_is_facade : bool
        The target is facade value.
    likely_owner : ProjectModuleRecord | None
        The likely owner value.
    owner_candidates : tuple[str, ...]
        The owner candidates value.
    inactive_owner_candidates : tuple[str, ...]
        The owner candidates excluded from active ranking.
    merge_status : str
        The merge status value.
    
    Returns
    -------
    tuple[str, str, bool, tuple[str, ...]]
        The tuple of values.
    """
    
    reasons: list[str] = []
    reasons.append("Target owner role: " + target_record.owner_role + ".")
    reasons.append("Evidence merge status: " + merge_status + ".")
    if inactive_owner_candidates:
        reasons.append(
            "Inactive owner candidates excluded before ranking: "
            + str(len(inactive_owner_candidates))
        )
    if target_is_facade:
        reasons.append("Target appears to be a facade or compatibility re-export surface.")
        if likely_owner is not None:
            reasons.append("Patch the likely real owner instead of the facade.")
            return (
                _STATUS_NEEDS_OWNER_REVIEW,
                "high",
                False,
                tuple(reasons),
            )
        reasons.append("No active real owner candidate was identified from current evidence.")
        return (
            _STATUS_OWNER_NOT_FOUND,
            "medium" if owner_candidates else "low",
            False,
            tuple(reasons),
        )
    reasons.append("Target does not look like a facade from current evidence.")
    return (
        _STATUS_NO_FACADE,
        "medium",
        True,
        tuple(reasons),
    )
