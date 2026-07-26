# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_transform_fidelity.py
"""Transformation fidelity checks for real preview generation."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
import importlib.util
from typing import Any

__all__ = [
    "CstTransformFidelityReport",
    "build_cst_transform_fidelity_report",
]


@dataclass(frozen=True)
class CstTransformFidelityReport:
    """Read-only evidence that planned moved symbols are safely transformable."""

    transform_backend: str
    moved_symbols_requested: list[str]
    moved_symbols_found: list[str]
    missing_symbols: list[str]
    top_level_definitions: list[str]
    retained_top_level_symbols: list[str]
    top_level_import_count: int
    retained_module_docstring: bool
    retained_main_guard: bool
    source_has_future_imports: bool
    cst_available: bool
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready fidelity report."""
        return asdict(self)


def build_cst_transform_fidelity_report(
    source_text: str,
    moved_symbols: set[str] | list[str] | tuple[str, ...],
) -> CstTransformFidelityReport:
    """Build non-mutating CST/AST evidence for stronger preview movement."""
    requested = sorted({str(item) for item in moved_symbols if str(item).strip()})
    if _libcst_available():
        report = _build_libcst_report(source_text, requested)
        if report is not None:
            return report
    return _build_ast_report(source_text, requested)


def _build_libcst_report(source_text: str, requested: list[str]) -> CstTransformFidelityReport | None:
    """Build a LibCST-backed report when LibCST can parse the file."""
    try:
        import libcst as cst  # type: ignore[import-not-found]
    except Exception:
        return None
    try:
        module = cst.parse_module(source_text)
    except Exception as exc:
        ast_report = _build_ast_report(source_text, requested)
        return CstTransformFidelityReport(
            transform_backend="libcst_parse_failed_ast_fallback",
            moved_symbols_requested=requested,
            moved_symbols_found=ast_report.moved_symbols_found,
            missing_symbols=ast_report.missing_symbols,
            top_level_definitions=ast_report.top_level_definitions,
            retained_top_level_symbols=ast_report.retained_top_level_symbols,
            top_level_import_count=ast_report.top_level_import_count,
            retained_module_docstring=ast_report.retained_module_docstring,
            retained_main_guard=ast_report.retained_main_guard,
            source_has_future_imports=ast_report.source_has_future_imports,
            cst_available=True,
            blockers=ast_report.blockers,
            warnings=[*ast_report.warnings, f"LIBCST_PARSE_FAILED:{exc}"],
        )
    definitions: list[str] = []
    imports = 0
    module_docstring = False
    main_guard = False
    future_imports = False
    for index, statement in enumerate(module.body):
        if isinstance(statement, (cst.FunctionDef, cst.ClassDef)):
            definitions.append(statement.name.value)
            continue
        if isinstance(statement, cst.SimpleStatementLine):
            imports += _count_simple_imports(cst, statement)
            future_imports = future_imports or _has_future_import(cst, statement)
            if index == 0 and _is_cst_docstring(statement):
                module_docstring = True
            continue
        main_guard = main_guard or _is_cst_main_guard(cst, statement)
    found = sorted(set(requested) & set(definitions))
    missing = sorted(set(requested) - set(definitions))
    blockers = [f"MISSING_MOVED_SYMBOL:{name}" for name in missing]
    return CstTransformFidelityReport(
        transform_backend="libcst_transform_partition",
        moved_symbols_requested=requested,
        moved_symbols_found=found,
        missing_symbols=missing,
        top_level_definitions=definitions,
        retained_top_level_symbols=[name for name in definitions if name not in set(requested)],
        top_level_import_count=imports,
        retained_module_docstring=module_docstring,
        retained_main_guard=main_guard,
        source_has_future_imports=future_imports,
        cst_available=True,
        blockers=blockers,
        warnings=["LIBCST_TRANSFORM_PARTITION_USED"],
    )


def _build_ast_report(source_text: str, requested: list[str]) -> CstTransformFidelityReport:
    """Build an AST-backed report when LibCST is unavailable."""
    try:
        tree = ast.parse(source_text, type_comments=True)
    except SyntaxError as exc:
        return CstTransformFidelityReport(
            transform_backend="blocked",
            moved_symbols_requested=requested,
            moved_symbols_found=[],
            missing_symbols=requested,
            top_level_definitions=[],
            retained_top_level_symbols=[],
            top_level_import_count=0,
            retained_module_docstring=False,
            retained_main_guard=False,
            source_has_future_imports=False,
            cst_available=_libcst_available(),
            blockers=[f"AST_PARSE_FAILED:{exc}"],
            warnings=[],
        )
    definitions: list[str] = []
    imports = 0
    future_imports = False
    main_guard = False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.append(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            imports += 1
            future_imports = future_imports or (
                isinstance(node, ast.ImportFrom) and node.module == "__future__"
            )
        elif isinstance(node, ast.If):
            main_guard = main_guard or _is_ast_main_guard(node)
    module_docstring = ast.get_docstring(tree) is not None
    found = sorted(set(requested) & set(definitions))
    missing = sorted(set(requested) - set(definitions))
    blockers = [f"MISSING_MOVED_SYMBOL:{name}" for name in missing]
    return CstTransformFidelityReport(
        transform_backend="ast_transform_partition_fallback",
        moved_symbols_requested=requested,
        moved_symbols_found=found,
        missing_symbols=missing,
        top_level_definitions=definitions,
        retained_top_level_symbols=[name for name in definitions if name not in set(requested)],
        top_level_import_count=imports,
        retained_module_docstring=module_docstring,
        retained_main_guard=main_guard,
        source_has_future_imports=future_imports,
        cst_available=_libcst_available(),
        blockers=blockers,
        warnings=["AST_TRANSFORM_PARTITION_FALLBACK_USED"],
    )


def _count_simple_imports(cst_module: Any, statement: Any) -> int:
    """Return import count for one LibCST simple statement."""
    return sum(isinstance(item, (cst_module.Import, cst_module.ImportFrom)) for item in statement.body)


def _has_future_import(cst_module: Any, statement: Any) -> bool:
    """Return whether a LibCST statement imports from __future__."""
    for item in statement.body:
        if isinstance(item, cst_module.ImportFrom) and item.module is not None:
            if getattr(item.module, "value", "") == "__future__":
                return True
    return False


def _is_cst_docstring(statement: Any) -> bool:
    """Return whether a LibCST simple statement is a module docstring."""
    try:
        first = statement.body[0]
        return first.__class__.__name__ == "Expr" and first.value.__class__.__name__ == "SimpleString"
    except Exception:
        return False


def _is_cst_main_guard(cst_module: Any, statement: Any) -> bool:
    """Return whether a LibCST statement looks like an if __name__ guard."""
    if not isinstance(statement, cst_module.If):
        return False
    return "__name__" in statement.test.deep_clone().code and "__main__" in statement.test.deep_clone().code


def _is_ast_main_guard(node: ast.If) -> bool:
    """Return whether an AST if node is `if __name__ == "__main__"`."""
    test = node.test
    if not isinstance(test, ast.Compare) or not isinstance(test.left, ast.Name):
        return False
    if test.left.id != "__name__" or len(test.comparators) != 1:
        return False
    comparator = test.comparators[0]
    return isinstance(comparator, ast.Constant) and comparator.value == "__main__"


def _libcst_available() -> bool:
    """Return whether LibCST is importable."""
    return importlib.util.find_spec("libcst") is not None
