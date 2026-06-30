# project-path: kanda_reasoner_app/reasoner_symbol_atlas/owner_classifier.py
"""Read-only owner classification for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .import_analyzer import (
    ProjectSymbolAtlasImportAnalysisOptions,
    analyze_reasoner_symbol_atlas_imports,
)
from .schemas import ProjectModuleRecord, ProjectSymbol, ProjectSymbolAtlasReport
from .symbol_indexer import (
    ProjectSymbolAtlasSymbolIndexOptions,
    index_reasoner_symbol_atlas_modules,
)

__all__ = [
    "ProjectSymbolAtlasOwnerClassifyOptions",
    "build_reasoner_symbol_atlas_owner_report",
    "classify_reasoner_symbol_atlas_owners",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasOwnerClassifyOptions:
    """Options for read-only owner classification."""

    include_tests: bool = True
    include_workbench: bool = False
    include_private: bool = False
    include_constants: bool = True
    include_private_reexports: bool = False
    include_wildcard_symbols: bool = False

    def to_symbol_index_options(self) -> ProjectSymbolAtlasSymbolIndexOptions:
        """Return compatible symbol-index options."""
        return ProjectSymbolAtlasSymbolIndexOptions(
            include_private=self.include_private,
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_constants=self.include_constants,
            include_imports=False,
        )

    def to_import_analysis_options(self) -> ProjectSymbolAtlasImportAnalysisOptions:
        """Return compatible import-analysis options."""
        return ProjectSymbolAtlasImportAnalysisOptions(
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
            include_private_reexports=self.include_private_reexports,
            include_wildcard_symbols=self.include_wildcard_symbols,
        )


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
    
    root = Path(project_root).resolve()
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError("Project root is not a directory: " + str(project_root))
    return root


def _path_parts(record: ProjectModuleRecord) -> tuple[str, ...]:
    """Support path parts behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    return tuple(part.lower() for part in Path(record.path).parts)


def _path_name(record: ProjectModuleRecord) -> str:
    """Support path name behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    return Path(record.path).name.lower()


def _has_evidence(record: ProjectModuleRecord, token: str) -> bool:
    """Support has evidence behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    token : str
        The token value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered = token.lower()
    return any(lowered in item.lower() for item in record.evidence)


def _has_public_definition(record: ProjectModuleRecord) -> bool:
    """Support has public definition behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for symbol in record.symbols:
        if symbol.kind in {"function", "class", "dataclass", "constant"} and symbol.is_public:
            return True
    return False


def _has_public_reexport(record: ProjectModuleRecord) -> bool:
    """Support has public reexport behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for symbol in record.symbols:
        if symbol.kind == "import" and symbol.is_public:
            return True
    return False


def _is_helper_path(record: ProjectModuleRecord) -> bool:
    """Support is helper path behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    name = _path_name(record)
    parts = _path_parts(record)
    helper_tokens = ("helper", "helpers", "util", "utils", "common")
    if any(token in name for token in helper_tokens):
        return True
    return any(part in {"helpers", "utils", "common"} for part in parts)


def _is_generated_or_stale(record: ProjectModuleRecord) -> bool:
    """Support is generated or stale behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if record.owner_role == "generated_or_stale":
        return True
    name = _path_name(record)
    parts = _path_parts(record)
    stale_tokens = ("archive", "backup", "deprecated", "generated", "legacy", "old", "stale", "tmp")
    if any(token in name for token in stale_tokens):
        return True
    if any(part.startswith("_tmp") for part in parts):
        return True
    return _has_evidence(record, "generated_or_stale_candidate: true")


def _module_role(record: ProjectModuleRecord) -> str:
    """Support module role behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if record.is_test_file or record.owner_role == "test_only":
        return "test_only"
    if _is_generated_or_stale(record):
        return "generated_or_stale"
    if record.owner_role == "compatibility_facade":
        return "compatibility_facade"
    if record.owner_role == "facade":
        return "facade"
    if _has_evidence(record, "module_getattr_export_detected: true"):
        return "compatibility_facade"
    if _has_evidence(record, "facade_shape_candidate: true"):
        if _has_public_definition(record) and _has_public_reexport(record):
            return "ambiguous_owner"
        return "facade"
    if record.is_package_init and _has_public_reexport(record):
        return "facade"
    if _is_helper_path(record):
        return "private_helper"
    if _has_public_definition(record):
        return "canonical_owner"
    if _has_public_reexport(record):
        return "facade"
    return "unknown"


def _symbol_role(symbol: ProjectSymbol, module_role: str) -> str:
    """Support symbol role behavior.
    
    Parameters
    ----------
    symbol : ProjectSymbol
        The symbol value.
    module_role : str
        The module role value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not symbol.is_public:
        return "private_helper"
    if module_role in {
        "test_only",
        "generated_or_stale",
        "facade",
        "compatibility_facade",
        "private_helper",
        "ambiguous_owner",
    }:
        return module_role
    if symbol.kind == "import":
        return "facade"
    if symbol.kind in {"function", "class", "dataclass", "constant"}:
        return "canonical_owner"
    return module_role if module_role != "unknown" else "unknown"


def _copy_symbol_with_role(symbol: ProjectSymbol, owner_role: str, evidence: tuple[str, ...]) -> ProjectSymbol:
    """Support copy symbol with role behavior.
    
    Parameters
    ----------
    symbol : ProjectSymbol
        The symbol value.
    owner_role : str
        The owner role value.
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
        owner_role=owner_role,
        exported_by_all=symbol.exported_by_all,
        evidence=merged_evidence,
    )


def _copy_record_with_role(record: ProjectModuleRecord, owner_role: str) -> ProjectModuleRecord:
    """Support copy record with role behavior.
    
    Parameters
    ----------
    record : ProjectModuleRecord
        The record value.
    owner_role : str
        The owner role value.
    
    Returns
    -------
    ProjectModuleRecord
        The project module record result.
    """
    
    evidence = tuple(dict.fromkeys(tuple(record.evidence) + ("owner_classification: " + owner_role,)))
    symbols = tuple(
        _copy_symbol_with_role(
            symbol,
            _symbol_role(symbol, owner_role),
            ("owner_classification: " + _symbol_role(symbol, owner_role),),
        )
        for symbol in record.symbols
    )
    return ProjectModuleRecord(
        module=record.module,
        path=record.path,
        line_count=record.line_count,
        is_package_init=record.is_package_init,
        is_test_file=record.is_test_file,
        owner_role=owner_role,
        symbols=symbols,
        imports=record.imports,
        evidence=evidence,
    )


def _merge_index_and_import_records(
    indexed_records: tuple[ProjectModuleRecord, ...],
    import_records: tuple[ProjectModuleRecord, ...],
) -> tuple[ProjectModuleRecord, ...]:
    """Support merge index and import records behavior.
    
    Parameters
    ----------
    indexed_records : tuple[ProjectModuleRecord, ...]
        The indexed records value.
    import_records : tuple[ProjectModuleRecord, ...]
        The import records value.
    
    Returns
    -------
    tuple[ProjectModuleRecord, ...]
        The tuple of values.
    """
    
    indexed_by_path = {record.path: record for record in indexed_records}
    import_by_path = {record.path: record for record in import_records}
    paths = sorted(set(indexed_by_path) | set(import_by_path))
    merged: list[ProjectModuleRecord] = []
    for path in paths:
        index_record = indexed_by_path.get(path)
        import_record = import_by_path.get(path)
        base = index_record or import_record
        if base is None:
            continue
        import_symbols: tuple[ProjectSymbol, ...] = tuple()
        imports: tuple[str, ...] = tuple(base.imports)
        owner_role = base.owner_role
        evidence = list(base.evidence)
        if import_record is not None:
            import_symbols = tuple(symbol for symbol in import_record.symbols if symbol.kind == "import")
            imports = import_record.imports
            if import_record.owner_role != "unknown":
                owner_role = import_record.owner_role
            evidence.extend(import_record.evidence)
        symbols = tuple(base.symbols) + import_symbols
        merged.append(
            ProjectModuleRecord(
                module=base.module,
                path=base.path,
                line_count=base.line_count,
                is_package_init=base.is_package_init,
                is_test_file=base.is_test_file,
                owner_role=owner_role,
                symbols=tuple(dict.fromkeys(symbols)),
                imports=imports,
                evidence=tuple(dict.fromkeys(evidence)),
            )
        )
    return tuple(merged)


def classify_reasoner_symbol_atlas_owners(
    project_root: str | Path,
    options: ProjectSymbolAtlasOwnerClassifyOptions | None = None,
) -> tuple[ProjectModuleRecord, ...]:
    """Classify likely module and symbol owners without importing project code."""
    root = _coerce_project_root(project_root)
    classify_options = options or ProjectSymbolAtlasOwnerClassifyOptions()
    indexed_records = index_reasoner_symbol_atlas_modules(
        root,
        options=classify_options.to_symbol_index_options(),
    )
    import_records = analyze_reasoner_symbol_atlas_imports(
        root,
        options=classify_options.to_import_analysis_options(),
    )
    merged_records = _merge_index_and_import_records(indexed_records, import_records)
    classified = [_copy_record_with_role(record, _module_role(record)) for record in merged_records]
    classified.sort(key=lambda record: (record.path, record.module))
    return tuple(classified)


def build_reasoner_symbol_atlas_owner_report(
    project_root: str | Path,
    options: ProjectSymbolAtlasOwnerClassifyOptions | None = None,
) -> ProjectSymbolAtlasReport:
    """Build a Project Symbol Atlas owner-classification report."""
    root = _coerce_project_root(project_root)
    modules = classify_reasoner_symbol_atlas_owners(root, options=options)
    symbols: list[ProjectSymbol] = []
    role_counts: dict[str, int] = {}
    for module in modules:
        role_counts[module.owner_role] = role_counts.get(module.owner_role, 0) + 1
        symbols.extend(module.symbols)
    role_summary = ", ".join(
        role + "=" + str(count) for role, count in sorted(role_counts.items())
    )
    return ProjectSymbolAtlasReport(
        project_root=str(root),
        report_type="owner_map",
        summary="Owner classification completed. modules="
        + str(len(modules))
        + "; symbols="
        + str(len(symbols))
        + "; roles="
        + role_summary
        + ".",
        modules=modules,
        symbols=tuple(symbols),
        input_sources=(
            "reasoner_symbol_atlas.module_scanner",
            "reasoner_symbol_atlas.symbol_indexer",
            "reasoner_symbol_atlas.import_analyzer",
            "reasoner_symbol_atlas.owner_classifier",
        ),
    )
