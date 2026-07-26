# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/symbol_dependency_builder.py
"""Read-only symbol dependency analysis for real refactor preview readiness."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from .models import FEATURE_ID, SCHEMA_VERSION
from .source_encoding_profile import build_source_encoding_profile, read_source_text

__all__ = [
    "SymbolDependencyRecord",
    "SymbolDependencyReport",
    "build_symbol_dependency_report",
]


@dataclass(frozen=True)
class SymbolDependencyRecord:
    """Dependency evidence for one top-level movable symbol."""

    schema_version: str
    name: str
    kind: str
    start_line: int
    end_line: int
    internal_dependencies: list[str] = field(default_factory=list)
    import_dependencies: list[str] = field(default_factory=list)
    global_dependencies: list[str] = field(default_factory=list)
    decorator_dependencies: list[str] = field(default_factory=list)
    type_hint_dependencies: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready symbol dependency record."""
        return asdict(self)


@dataclass(frozen=True)
class SymbolDependencyReport:
    """Read-only dependency topology for one Python source file."""

    schema_version: str
    feature_id: str
    target_file: str
    source_content_hash: str
    encoding: str
    newline_style: str
    symbols: list[SymbolDependencyRecord]
    module_import_aliases: list[str]
    module_assignments: list[str]
    risk_flags: list[str]
    blockers: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready dependency report."""
        data = asdict(self)
        data["symbols"] = [symbol.to_dict() for symbol in self.symbols]
        return data


def build_symbol_dependency_report(path: str | Path) -> SymbolDependencyReport:
    """Build a read-only symbol dependency report for preview readiness."""
    source_path = Path(path).expanduser().resolve()
    profile = build_source_encoding_profile(source_path)
    source = read_source_text(source_path, profile)
    tree = ast.parse(source)
    imports = _import_aliases(tree)
    assignments = _module_assignments(tree)
    top_symbols = _top_level_symbols(tree)
    records = [
        _record_for_symbol(node, top_symbols, imports, assignments)
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    ]
    risk_flags = sorted({risk for record in records for risk in record.risk_flags})
    blockers = _module_blockers(records)
    warnings = _module_warnings(tree, records, profile.read_errors)
    return SymbolDependencyReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(source_path),
        source_content_hash=profile.byte_hash,
        encoding=profile.encoding,
        newline_style=profile.newline_style,
        symbols=records,
        module_import_aliases=sorted(imports),
        module_assignments=sorted(assignments),
        risk_flags=risk_flags,
        blockers=blockers,
        warnings=warnings,
    )


def _top_level_symbols(tree: ast.Module) -> set[str]:
    """Return names owned by top-level functions/classes."""
    result: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            result.add(node.name)
    return result


def _import_aliases(tree: ast.Module) -> set[str]:
    """Return names created by top-level imports."""
    aliases: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                aliases.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    aliases.add("*")
                else:
                    aliases.add(alias.asname or alias.name)
    return aliases


def _module_assignments(tree: ast.Module) -> set[str]:
    """Return names assigned at module level."""
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            names.update(_assigned_names(node))
    return names


def _assigned_names(node: ast.AST) -> set[str]:
    """Return simple names assigned by a module-level assignment."""
    targets: list[ast.AST] = []
    if isinstance(node, ast.Assign):
        targets.extend(node.targets)
    elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
        targets.append(node.target)
    names: set[str] = set()
    for target in targets:
        for item in ast.walk(target):
            if isinstance(item, ast.Name):
                names.add(item.id)
    return names


def _record_for_symbol(
    node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef,
    top_symbols: set[str],
    imports: set[str],
    assignments: set[str],
) -> SymbolDependencyRecord:
    """Return dependency evidence for a top-level function or class."""
    referenced = _loaded_names(node)
    decorators = _decorator_names(node)
    type_hints = _type_hint_names(node)
    internal = sorted((referenced | decorators | type_hints) & top_symbols - {node.name})
    import_deps = sorted((referenced | decorators | type_hints) & imports)
    global_deps = sorted((referenced | decorators | type_hints) & assignments - {node.name})
    risks = _symbol_risks(node, decorators, type_hints, referenced, global_deps)
    return SymbolDependencyRecord(
        schema_version=SCHEMA_VERSION,
        name=node.name,
        kind=_node_kind(node),
        start_line=getattr(node, "lineno", 0),
        end_line=getattr(node, "end_lineno", getattr(node, "lineno", 0)),
        internal_dependencies=internal,
        import_dependencies=import_deps,
        global_dependencies=global_deps,
        decorator_dependencies=sorted(decorators),
        type_hint_dependencies=sorted(type_hints),
        risk_flags=sorted(risks),
    )


def _loaded_names(node: ast.AST) -> set[str]:
    """Return names loaded by a symbol body."""
    return {
        item.id
        for item in ast.walk(node)
        if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Load)
    }


def _decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> set[str]:
    """Return root names used by decorators."""
    names: set[str] = set()
    for decorator in getattr(node, "decorator_list", []):
        names.update(_root_names(decorator))
    return names


def _type_hint_names(node: ast.AST) -> set[str]:
    """Return root names used in annotations, returns, and class bases."""
    hints: list[ast.AST] = []
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        hints.extend(_function_annotation_nodes(node))
    if isinstance(node, ast.ClassDef):
        hints.extend(node.bases)
        hints.extend(node.keywords)
        for child in node.body:
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                hints.extend(_function_annotation_nodes(child))
            elif isinstance(child, ast.AnnAssign):
                hints.append(child.annotation)
    names: set[str] = set()
    for hint in hints:
        names.update(_root_names(hint))
    return names


def _function_annotation_nodes(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[ast.AST]:
    """Return annotation nodes from a function signature."""
    items: list[ast.AST] = []
    for arg in list(node.args.posonlyargs) + list(node.args.args) + list(node.args.kwonlyargs):
        if arg.annotation is not None:
            items.append(arg.annotation)
    if node.args.vararg and node.args.vararg.annotation is not None:
        items.append(node.args.vararg.annotation)
    if node.args.kwarg and node.args.kwarg.annotation is not None:
        items.append(node.args.kwarg.annotation)
    if node.returns is not None:
        items.append(node.returns)
    return items


def _root_names(node: ast.AST) -> set[str]:
    """Return root loaded names used by an AST node."""
    names: set[str] = set()
    for item in ast.walk(node):
        if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Load):
            names.add(item.id)
    return names


def _symbol_risks(
    node: ast.AST,
    decorators: Iterable[str],
    type_hints: Iterable[str],
    referenced: set[str],
    global_deps: list[str],
) -> list[str]:
    """Return risk flags for moving one symbol."""
    risks: set[str] = set()
    if decorators:
        risks.add("DECORATOR_DEPENDENCY_RISK")
    if type_hints:
        risks.add("TYPE_HINT_IMPORT_RISK")
    if global_deps:
        risks.add("GLOBAL_DEPENDENCY_RISK")
    if any(isinstance(item, ast.Global) for item in ast.walk(node)):
        risks.add("GLOBAL_MUTATION_RISK")
    if any(isinstance(item, ast.Nonlocal) for item in ast.walk(node)):
        risks.add("NONLOCAL_RISK")
    dynamic_names = {"globals", "locals", "getattr", "setattr", "eval", "exec", "__import__"}
    if referenced & dynamic_names:
        risks.add("DYNAMIC_NAMESPACE_RISK")
    return sorted(risks)


def _module_blockers(records: list[SymbolDependencyRecord]) -> list[str]:
    """Return hard blockers for real preview readiness."""
    blockers: set[str] = set()
    for record in records:
        if "NONLOCAL_RISK" in record.risk_flags:
            blockers.add("NONLOCAL_SYMBOL_MOVE_BLOCKED")
        if "GLOBAL_MUTATION_RISK" in record.risk_flags:
            blockers.add("GLOBAL_MUTATION_REQUIRES_MANUAL_REVIEW")
    return sorted(blockers)


def _module_warnings(
    tree: ast.Module,
    records: list[SymbolDependencyRecord],
    read_errors: list[str],
) -> list[str]:
    """Return module-level warnings for real preview readiness."""
    warnings: set[str] = set(read_errors)
    if any(isinstance(node, ast.ImportFrom) and node.level for node in tree.body):
        warnings.add("RELATIVE_IMPORT_RISK")
    if any(isinstance(node, ast.ImportFrom) and any(alias.name == "*" for alias in node.names) for node in tree.body):
        warnings.add("STAR_IMPORT_RISK")
    if any(isinstance(node, ast.Expr) and not isinstance(node.value, ast.Constant) for node in tree.body):
        warnings.add("MODULE_SIDE_EFFECT_RISK")
    if any(record.internal_dependencies for record in records):
        warnings.add("INTERNAL_SYMBOL_DEPENDENCIES_DETECTED")
    return sorted(warnings)


def _node_kind(node: ast.AST) -> str:
    """Return a stable symbol kind."""
    if isinstance(node, ast.AsyncFunctionDef):
        return "async_function"
    if isinstance(node, ast.FunctionDef):
        return "function"
    return "class"
