# project-path: kanda_reasoner_app/reasoner_symbol_atlas/import_analyzer.py
"""AST-only import, facade, and re-export analyzer for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .module_scanner import (
    ProjectSymbolAtlasModuleScanOptions,
    collect_reasoner_symbol_atlas_modules,
)
from .schemas import ProjectModuleRecord, ProjectSymbol, ProjectSymbolAtlasReport

from .import_analyzer_ast_private import (
    _evidence_from_tree,
    _format_import_node,
    _import_symbols_from_tree,
    _owner_role_from_analysis,
    _parse_python_source,
    _read_python_source,
)

__all__ = [
    "ProjectSymbolAtlasImportAnalysisOptions",
    "analyze_reasoner_symbol_atlas_imports",
    "build_reasoner_symbol_atlas_import_report",
    "collect_reasoner_symbol_atlas_imports",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasImportAnalysisOptions:
    """Options for AST-only import and facade analysis."""

    include_tests: bool = True
    include_workbench: bool = False
    include_private_reexports: bool = False
    include_wildcard_symbols: bool = False

    def to_module_scan_options(self) -> ProjectSymbolAtlasModuleScanOptions:
        """Return compatible module-scan options."""
        return ProjectSymbolAtlasModuleScanOptions(
            include_tests=self.include_tests,
            include_workbench=self.include_workbench,
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


def _analyze_module_record(
    project_root: Path,
    module_record: ProjectModuleRecord,
    options: ProjectSymbolAtlasImportAnalysisOptions,
) -> ProjectModuleRecord:
    """Support analyze module record behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    module_record : ProjectModuleRecord
        The module record value.
    options : ProjectSymbolAtlasImportAnalysisOptions
        The option values.
    
    Returns
    -------
    ProjectModuleRecord
        The project module record result.
    """
    
    source_path = project_root / module_record.path
    source_text, read_evidence = _read_python_source(source_path)
    tree, parse_evidence = _parse_python_source(source_text, source_path)
    evidence = list(module_record.evidence)
    evidence.extend(read_evidence)
    evidence.extend(parse_evidence)
    if tree is None:
        return ProjectModuleRecord(
            module=module_record.module,
            path=module_record.path,
            line_count=module_record.line_count,
            is_package_init=module_record.is_package_init,
            is_test_file=module_record.is_test_file,
            owner_role=module_record.owner_role,
            symbols=module_record.symbols,
            imports=tuple(module_record.imports),
            evidence=tuple(evidence),
        )
    imports: list[str] = []
    for node in tree.body:
        imports.extend(_format_import_node(node))
    import_tuple = tuple(dict.fromkeys(imports))
    import_symbols = _import_symbols_from_tree(tree, module_record, options)
    evidence.extend(_evidence_from_tree(tree, import_tuple))
    owner_role = _owner_role_from_analysis(module_record, tree, import_tuple)
    return ProjectModuleRecord(
        module=module_record.module,
        path=module_record.path,
        line_count=module_record.line_count,
        is_package_init=module_record.is_package_init,
        is_test_file=module_record.is_test_file,
        owner_role=owner_role,
        symbols=tuple(module_record.symbols) + import_symbols,
        imports=import_tuple,
        evidence=tuple(evidence),
    )


def analyze_reasoner_symbol_atlas_imports(
    project_root: str | Path,
    options: ProjectSymbolAtlasImportAnalysisOptions | None = None,
) -> tuple[ProjectModuleRecord, ...]:
    """Return module records enriched with AST import and facade evidence."""
    root = _coerce_project_root(project_root)
    analysis_options = options or ProjectSymbolAtlasImportAnalysisOptions()
    modules = collect_reasoner_symbol_atlas_modules(
        root,
        options=analysis_options.to_module_scan_options(),
    )
    analyzed = [_analyze_module_record(root, module, analysis_options) for module in modules]
    analyzed.sort(key=lambda record: (record.path, record.module))
    return tuple(analyzed)


def collect_reasoner_symbol_atlas_imports(
    project_root: str | Path,
    options: ProjectSymbolAtlasImportAnalysisOptions | None = None,
) -> tuple[str, ...]:
    """Collect formatted import statements without importing project code."""
    modules = analyze_reasoner_symbol_atlas_imports(project_root, options=options)
    imports: list[str] = []
    for module in modules:
        imports.extend(module.imports)
    return tuple(dict.fromkeys(imports))


def build_reasoner_symbol_atlas_import_report(
    project_root: str | Path,
    options: ProjectSymbolAtlasImportAnalysisOptions | None = None,
) -> ProjectSymbolAtlasReport:
    """Build a Project Symbol Atlas import and facade analysis report."""
    root = _coerce_project_root(project_root)
    modules = analyze_reasoner_symbol_atlas_imports(root, options=options)
    symbols: list[ProjectSymbol] = []
    import_count = 0
    for module in modules:
        import_count += len(module.imports)
        symbols.extend(module.symbols)
    return ProjectSymbolAtlasReport(
        project_root=str(root),
        report_type="reasoner_symbol_atlas",
        summary="AST import/facade analysis completed. modules="
        + str(len(modules))
        + "; imports="
        + str(import_count)
        + "; reexport_symbols="
        + str(len(symbols))
        + ".",
        modules=modules,
        symbols=tuple(symbols),
        input_sources=(
            "reasoner_symbol_atlas.module_scanner",
            "reasoner_symbol_atlas.import_analyzer",
        ),
    )
