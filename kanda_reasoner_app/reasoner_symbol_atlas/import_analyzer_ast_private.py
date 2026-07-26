# project-path: kanda_reasoner_app/reasoner_symbol_atlas/import_analyzer_ast_private.py
"""Private AST helpers for Project Symbol Atlas import analysis."""

from __future__ import annotations

import ast
from pathlib import Path

from .schemas import ProjectModuleRecord, ProjectSymbol

__all__: list[str] = []


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


def _extract_string_sequence(node: ast.AST) -> tuple[str, ...]:
    """Support extract string sequence behavior.
    
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
                    names.extend(_extract_string_sequence(node.value))
        elif isinstance(node, ast.AnnAssign):
            target = node.target
            if isinstance(target, ast.Name) and target.id == "__all__" and node.value is not None:
                names.extend(_extract_string_sequence(node.value))
    return tuple(dict.fromkeys(names))


def _import_source_for_from(node: ast.ImportFrom) -> str:
    """Support import source for from behavior.
    
    Parameters
    ----------
    node : ast.ImportFrom
        The syntax tree node.
    
    Returns
    -------
    str
        The string result.
    """
    
    prefix = "." * int(node.level or 0)
    return prefix + str(node.module or "")


def _alias_local_name(alias: ast.alias) -> str:
    """Support alias local name behavior.
    
    Parameters
    ----------
    alias : ast.alias
        The alias value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if alias.asname:
        return alias.asname
    return alias.name.rsplit(".", 1)[-1]


def _format_import_node(node: ast.stmt) -> tuple[str, ...]:
    """Support format import node behavior.
    
    Parameters
    ----------
    node : ast.stmt
        The syntax tree node.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    values: list[str] = []
    if isinstance(node, ast.Import):
        for alias in node.names:
            if alias.asname:
                values.append("import " + alias.name + " as " + alias.asname)
            else:
                values.append("import " + alias.name)
    elif isinstance(node, ast.ImportFrom):
        source = _import_source_for_from(node)
        for alias in node.names:
            if alias.asname:
                values.append("from " + source + " import " + alias.name + " as " + alias.asname)
            else:
                values.append("from " + source + " import " + alias.name)
    return tuple(values)


def _module_has_public_definition(tree: ast.Module) -> bool:
    """Support module has public definition behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if _is_public_name(node.name) and node.name != "__getattr__":
                return True
    return False


def _module_has_getattr_export(tree: ast.Module) -> bool:
    """Support module has getattr export behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "__getattr__":
            return True
    return False


def _module_has_delegation_map(tree: ast.Module) -> bool:
    """Support module has delegation map behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets: tuple[ast.expr, ...]
        if isinstance(node, ast.Assign):
            targets = tuple(node.targets)
        else:
            targets = (node.target,)
        for target in targets:
            if isinstance(target, ast.Name):
                lowered = target.id.lower()
                if "map" in lowered or "registry" in lowered or "exports" in lowered:
                    return True
    return False


def _import_symbols_from_tree(
    tree: ast.Module,
    module_record: ProjectModuleRecord,
    options: ProjectSymbolAtlasImportAnalysisOptions,
) -> tuple[ProjectSymbol, ...]:
    """Support import symbols from tree behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    module_record : ProjectModuleRecord
        The module record value.
    options : ProjectSymbolAtlasImportAnalysisOptions
        The option values.
    
    Returns
    -------
    tuple[ProjectSymbol, ...]
        The tuple of values.
    """
    
    all_names = set(_module_all_names(tree))
    module_is_facade_shape = module_record.is_package_init or "facade" in module_record.path.lower()
    symbols: list[ProjectSymbol] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                local_name = _alias_local_name(alias)
                if local_name not in all_names and not module_is_facade_shape:
                    continue
                if not _is_public_name(local_name) and not options.include_private_reexports:
                    continue
                symbols.append(
                    ProjectSymbol(
                        name=local_name,
                        kind="import",
                        module=module_record.module,
                        path=module_record.path,
                        line=node.lineno,
                        is_public=_is_public_name(local_name),
                        owner_role="facade" if module_is_facade_shape else module_record.owner_role,
                        exported_by_all=local_name in all_names,
                        evidence=("reexport_import: ast_only", "source: " + alias.name),
                    )
                )
        elif isinstance(node, ast.ImportFrom):
            source = _import_source_for_from(node)
            for alias in node.names:
                if alias.name == "*":
                    if options.include_wildcard_symbols:
                        symbols.append(
                            ProjectSymbol(
                                name="*",
                                kind="import",
                                module=module_record.module,
                                path=module_record.path,
                                line=node.lineno,
                                is_public=False,
                                owner_role="facade" if module_is_facade_shape else module_record.owner_role,
                                exported_by_all=False,
                                evidence=("wildcard_import: " + source,),
                            )
                        )
                    continue
                local_name = _alias_local_name(alias)
                if local_name not in all_names and not module_is_facade_shape:
                    continue
                if not _is_public_name(local_name) and not options.include_private_reexports:
                    continue
                symbols.append(
                    ProjectSymbol(
                        name=local_name,
                        kind="import",
                        module=module_record.module,
                        path=module_record.path,
                        line=node.lineno,
                        is_public=_is_public_name(local_name),
                        owner_role="facade" if module_is_facade_shape else module_record.owner_role,
                        exported_by_all=local_name in all_names,
                        evidence=("reexport_from_import: ast_only", "source: " + source + "." + alias.name),
                    )
                )
    symbols.sort(key=lambda item: (item.path, item.line or 0, item.name))
    return tuple(symbols)


def _evidence_from_tree(tree: ast.Module, imports: tuple[str, ...]) -> tuple[str, ...]:
    """Support evidence from tree behavior.
    
    Parameters
    ----------
    tree : ast.Module
        The parsed syntax tree.
    imports : tuple[str, ...]
        The imports value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    evidence: list[str] = ["import_analysis: ast_only", "import_count: " + str(len(imports))]
    all_names = _module_all_names(tree)
    if all_names:
        evidence.append("explicit_all: " + ", ".join(all_names))
    if any(" import *" in value for value in imports):
        evidence.append("wildcard_import_detected: true")
    if _module_has_getattr_export(tree):
        evidence.append("module_getattr_export_detected: true")
    if _module_has_delegation_map(tree):
        evidence.append("delegation_map_candidate: true")
    if imports and not _module_has_public_definition(tree):
        evidence.append("facade_shape_candidate: true")
    return tuple(evidence)


def _owner_role_from_analysis(
    module_record: ProjectModuleRecord,
    tree: ast.Module,
    imports: tuple[str, ...],
) -> str:
    """Support owner role from analysis behavior.
    
    Parameters
    ----------
    module_record : ProjectModuleRecord
        The module record value.
    tree : ast.Module
        The parsed syntax tree.
    imports : tuple[str, ...]
        The imports value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if module_record.owner_role in {"test_only", "generated_or_stale"}:
        return module_record.owner_role
    has_reexport_signals = bool(imports) and (
        bool(_module_all_names(tree))
        or module_record.is_package_init
        or _module_has_getattr_export(tree)
        or _module_has_delegation_map(tree)
    )
    if has_reexport_signals:
        if "compat" in module_record.path.lower() or _module_has_getattr_export(tree):
            return "compatibility_facade"
        return "facade"
    return module_record.owner_role
