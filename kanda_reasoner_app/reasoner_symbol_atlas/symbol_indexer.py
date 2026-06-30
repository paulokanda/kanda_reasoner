# project-path: kanda_reasoner_app/reasoner_symbol_atlas/symbol_indexer.py
"""AST-only public symbol indexer for Project Symbol Atlas."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

from .module_scanner import (
    ProjectSymbolAtlasModuleScanOptions,
    collect_reasoner_symbol_atlas_modules,
)
from .schemas import ProjectModuleRecord, ProjectSymbol, ProjectSymbolAtlasReport

__all__ = [
    "ProjectSymbolAtlasSymbolIndexOptions",
    "build_reasoner_symbol_atlas_symbol_report",
    "collect_reasoner_symbol_atlas_symbols",
    "index_reasoner_symbol_atlas_modules",
]


@dataclass(frozen=True)
class ProjectSymbolAtlasSymbolIndexOptions:
    """Options for AST-only public symbol indexing."""

    include_private: bool = False
    include_tests: bool = True
    include_workbench: bool = False
    include_constants: bool = True
    include_imports: bool = False

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


def _read_python_source(file_path: Path) -> tuple[str, tuple[str, ...]]:
    """Support read python source behavior.
    
    Parameters
    ----------
    file_path : Path
        The file path.
    
    Returns
    -------
    tuple[str, tuple[str, ...]]
        The tuple of values.
    """
    
    evidence: list[str] = []
    try:
        return file_path.read_text(encoding="utf-8-sig", errors="replace"), tuple(evidence)
    except OSError as exc:
        evidence.append("read_error: " + exc.__class__.__name__)
        return "", tuple(evidence)


def _parse_python_source(source_text: str, file_path: Path) -> tuple[ast.Module | None, tuple[str, ...]]:
    """Support parse python source behavior.
    
    Parameters
    ----------
    source_text : str
        The source text.
    file_path : Path
        The file path.
    
    Returns
    -------
    tuple[ast.Module | None, tuple[str, ...]]
        The tuple of values.
    """
    
    evidence: list[str] = []
    try:
        return ast.parse(source_text, filename=str(file_path)), tuple(evidence)
    except SyntaxError as exc:
        detail = str(exc.lineno or "unknown")
        evidence.append("syntax_error_line: " + detail)
        return None, tuple(evidence)


def _is_public_name(name: str) -> bool:
    """Support is public name behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return bool(name) and not name.startswith("_")


def _decorator_name(decorator: ast.expr) -> str:
    """Support decorator name behavior.
    
    Parameters
    ----------
    decorator : ast.expr
        The decorator value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if isinstance(decorator, ast.Name):
        return decorator.id
    if isinstance(decorator, ast.Attribute):
        base = _decorator_name(decorator.value)
        return (base + "." if base else "") + decorator.attr
    if isinstance(decorator, ast.Call):
        return _decorator_name(decorator.func)
    return ""


def _is_dataclass_definition(node: ast.ClassDef) -> bool:
    """Support is dataclass definition behavior.
    
    Parameters
    ----------
    node : ast.ClassDef
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for decorator in node.decorator_list:
        if _decorator_name(decorator).endswith("dataclass"):
            return True
    return False


def _constant_names_from_target(target: ast.expr) -> tuple[str, ...]:
    """Support constant names from target behavior.
    
    Parameters
    ----------
    target : ast.expr
        The target value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    if isinstance(target, ast.Name):
        return (target.id,)
    if isinstance(target, (ast.Tuple, ast.List)):
        names: list[str] = []
        for element in target.elts:
            names.extend(_constant_names_from_target(element))
        return tuple(names)
    return tuple()


def _extract_all_names(node: ast.AST) -> tuple[str, ...]:
    """Support extract all names behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        names: list[str] = []
        for element in node.elts:
            if isinstance(element, ast.Constant) and isinstance(element.value, str):
                names.append(element.value)
        return tuple(names)
    return tuple()


def _module_all_names(tree: ast.Module) -> tuple[str, ...]:
    """Support module all names behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    names.extend(_extract_all_names(node.value))
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__" and node.value is not None:
                names.extend(_extract_all_names(node.value))
    return tuple(dict.fromkeys(names))


def _symbol_from_definition(
    name: str,
    kind: str,
    module_record: ProjectModuleRecord,
    line: int | None,
    all_names: set[str],
    evidence: tuple[str, ...],
    options: ProjectSymbolAtlasSymbolIndexOptions,
) -> ProjectSymbol | None:
    """Support symbol from definition behavior.
    
    Parameters
    ----------
    name : str
        The name value.
    kind : str
        The kind value.
    module_record : ProjectModuleRecord
        The module record value.
    line : int | None
        The line value.
    all_names : set[str]
        The all names value.
    evidence : tuple[str, ...]
        The evidence value.
    options : ProjectSymbolAtlasSymbolIndexOptions
        The option values.
    
    Returns
    -------
    ProjectSymbol | None
        The project symbol result.
    """
    
    is_public = _is_public_name(name)
    if not is_public and not options.include_private:
        return None
    exported_by_all = name in all_names
    return ProjectSymbol(
        name=name,
        kind=kind,
        module=module_record.module,
        path=module_record.path,
        line=line,
        is_public=is_public,
        owner_role=module_record.owner_role,
        exported_by_all=exported_by_all,
        evidence=evidence,
    )


def _iter_symbols_from_tree(
    tree: ast.Module,
    module_record: ProjectModuleRecord,
    options: ProjectSymbolAtlasSymbolIndexOptions,
) -> tuple[ProjectSymbol, ...]:
    """Support iter symbols from tree behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    module_record : ProjectModuleRecord
        The module record value.
    options : ProjectSymbolAtlasSymbolIndexOptions
        The option values.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    all_names = set(_module_all_names(tree))
    symbols: list[ProjectSymbol] = []
    for node in tree.body:
        candidate: ProjectSymbol | None = None
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            candidate = _symbol_from_definition(
                node.name,
                "function",
                module_record,
                node.lineno,
                all_names,
                ("ast_definition: function",),
                options,
            )
        elif isinstance(node, ast.ClassDef):
            kind = "dataclass" if _is_dataclass_definition(node) else "class"
            candidate = _symbol_from_definition(
                node.name,
                kind,
                module_record,
                node.lineno,
                all_names,
                ("ast_definition: " + kind,),
                options,
            )
        if candidate is not None:
            symbols.append(candidate)
            continue
        if options.include_constants and isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets: tuple[ast.expr, ...]
            if isinstance(node, ast.Assign):
                targets = tuple(node.targets)
            else:
                targets = (node.target,)
            for target in targets:
                for name in _constant_names_from_target(target):
                    if name == "__all__":
                        continue
                    if not name.isupper() and name not in all_names:
                        continue
                    constant_symbol = _symbol_from_definition(
                        name,
                        "constant",
                        module_record,
                        getattr(node, "lineno", None),
                        all_names,
                        ("ast_definition: constant",),
                        options,
                    )
                    if constant_symbol is not None:
                        symbols.append(constant_symbol)
    symbols.sort(key=lambda item: (item.path, item.line or 0, item.name))
    return tuple(symbols)


def _index_module_record(
    project_root: Path,
    module_record: ProjectModuleRecord,
    options: ProjectSymbolAtlasSymbolIndexOptions,
) -> ProjectModuleRecord:
    """Support index module record behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    module_record : ProjectModuleRecord
        The module record value.
    options : ProjectSymbolAtlasSymbolIndexOptions
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
            symbols=tuple(),
            imports=module_record.imports,
            evidence=tuple(evidence),
        )
    symbols = _iter_symbols_from_tree(tree, module_record, options)
    evidence.append("symbol_index: ast_only")
    evidence.append("symbol_count: " + str(len(symbols)))
    return ProjectModuleRecord(
        module=module_record.module,
        path=module_record.path,
        line_count=module_record.line_count,
        is_package_init=module_record.is_package_init,
        is_test_file=module_record.is_test_file,
        owner_role=module_record.owner_role,
        symbols=symbols,
        imports=module_record.imports,
        evidence=tuple(evidence),
    )


def index_reasoner_symbol_atlas_modules(
    project_root: str | Path,
    options: ProjectSymbolAtlasSymbolIndexOptions | None = None,
) -> tuple[ProjectModuleRecord, ...]:
    """Return module records enriched with AST-discovered symbols."""
    root = _coerce_project_root(project_root)
    index_options = options or ProjectSymbolAtlasSymbolIndexOptions()
    modules = collect_reasoner_symbol_atlas_modules(
        root,
        options=index_options.to_module_scan_options(),
    )
    indexed = [_index_module_record(root, module, index_options) for module in modules]
    indexed.sort(key=lambda record: (record.path, record.module))
    return tuple(indexed)


def collect_reasoner_symbol_atlas_symbols(
    project_root: str | Path,
    options: ProjectSymbolAtlasSymbolIndexOptions | None = None,
) -> tuple[ProjectSymbol, ...]:
    """Collect AST-discovered project symbols without importing project code."""
    modules = index_reasoner_symbol_atlas_modules(project_root, options=options)
    symbols: list[ProjectSymbol] = []
    for module in modules:
        symbols.extend(module.symbols)
    symbols.sort(key=lambda item: (item.path, item.line or 0, item.name))
    return tuple(symbols)


def build_reasoner_symbol_atlas_symbol_report(
    project_root: str | Path,
    options: ProjectSymbolAtlasSymbolIndexOptions | None = None,
) -> ProjectSymbolAtlasReport:
    """Build a Project Symbol Atlas symbol-index report."""
    root = _coerce_project_root(project_root)
    modules = index_reasoner_symbol_atlas_modules(root, options=options)
    symbols: list[ProjectSymbol] = []
    for module in modules:
        symbols.extend(module.symbols)
    return ProjectSymbolAtlasReport(
        project_root=str(root),
        report_type="reasoner_symbol_atlas",
        summary="AST public symbol index completed. modules="
        + str(len(modules))
        + "; symbols="
        + str(len(symbols))
        + ".",
        modules=modules,
        symbols=tuple(symbols),
        input_sources=(
            "reasoner_symbol_atlas.module_scanner",
            "reasoner_symbol_atlas.symbol_indexer",
        ),
    )
