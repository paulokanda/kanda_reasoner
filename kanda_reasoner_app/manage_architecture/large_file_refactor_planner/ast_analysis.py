# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ast_analysis.py
"""AST evidence extraction for the Large File Refactor Planner."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from typing import Iterable

from .candidate_discovery import count_physical_lines
from .guards import compute_content_hash
from .models import (
    FEATURE_ID,
    SCHEMA_VERSION,
    ImportRecord,
    ModuleAnalysisReport,
    RefactorSymbol,
)

__all__ = ["analyze_python_file"]


def analyze_python_file(path: str | Path) -> ModuleAnalysisReport:
    """Return read-only AST evidence for one Python source file."""
    source_path = Path(path).expanduser().resolve()
    source = source_path.read_text(encoding="utf-8", errors="replace")
    line_count = count_physical_lines(source_path)
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return _syntax_error_report(source_path, line_count, exc)
    all_names = _extract_all_names(tree)
    imports = _extract_imports(tree, source_path)
    symbols = _extract_symbols(tree, source)
    public_symbols = _public_api_symbols(tree, symbols, all_names)
    constants, assignments = _extract_assignments(tree)
    global_names, nonlocal_names = _extract_scope_statements(tree)
    module_calls = _extract_module_level_calls(tree)
    risk_flags = _collect_module_risks(tree, imports, symbols, all_names)
    module_docstring = ast.get_docstring(tree) or ""
    missing_docstrings = _count_missing_docstrings(tree, symbols, bool(module_docstring))
    return ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(source_path),
        source_content_hash=compute_content_hash(source_path),
        line_count_physical=line_count,
        module_docstring_present=bool(module_docstring),
        module_docstring_preview=_preview_docstring(module_docstring),
        all_names=all_names,
        public_api_symbols=public_symbols,
        imports=imports,
        symbols=symbols,
        constants=constants,
        assignments=assignments,
        global_statements=global_names,
        nonlocal_statements=nonlocal_names,
        module_level_calls=module_calls,
        if_main_present=_has_if_main(tree),
        nested_symbol_count=_count_nested_symbols(tree),
        missing_docstring_count=missing_docstrings,
        risk_flags=sorted(set(risk_flags)),
        analysis_errors=[],
    )


def _syntax_error_report(
    source_path: Path,
    line_count: int,
    exc: SyntaxError,
) -> ModuleAnalysisReport:
    """Build an analysis report for a file that cannot be parsed."""
    message = f"SyntaxError at line {exc.lineno}: {exc.msg}"
    return ModuleAnalysisReport(
        schema_version=SCHEMA_VERSION,
        feature_id=FEATURE_ID,
        target_file=str(source_path),
        source_content_hash=compute_content_hash(source_path),
        line_count_physical=line_count,
        module_docstring_present=False,
        module_docstring_preview="",
        all_names=[],
        public_api_symbols=[],
        imports=[],
        symbols=[],
        constants=[],
        assignments=[],
        global_statements=[],
        nonlocal_statements=[],
        module_level_calls=[],
        if_main_present=False,
        nested_symbol_count=0,
        missing_docstring_count=0,
        risk_flags=["NEEDS_SOURCE_INSPECTION"],
        analysis_errors=[message],
    )


def _extract_all_names(tree: ast.Module) -> list[str]:
    """Return literal names from a simple module-level __all__ assignment."""
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
                values = _literal_string_sequence(node.value)
                if values:
                    return values
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                values = _literal_string_sequence(node.value)
                if values:
                    return values
    return []


def _literal_string_sequence(node: ast.AST | None) -> list[str]:
    """Return a list of literal strings when the AST node is a sequence."""
    if not isinstance(node, (ast.List, ast.Tuple)):
        return []
    values: list[str] = []
    for item in node.elts:
        if isinstance(item, ast.Constant) and isinstance(item.value, str):
            values.append(item.value)
    return values


def _extract_imports(tree: ast.Module, source_path: Path) -> list[ImportRecord]:
    """Extract top-level import records without rewriting anything."""
    records: list[ImportRecord] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            records.extend(_records_for_import(node, source_path))
        elif isinstance(node, ast.ImportFrom):
            records.extend(_records_for_import_from(node, source_path))
    return records


def _records_for_import(node: ast.Import, source_path: Path) -> list[ImportRecord]:
    """Return records for an import statement."""
    records: list[ImportRecord] = []
    for alias in node.names:
        records.append(
            ImportRecord(
                schema_version=SCHEMA_VERSION,
                original_module=str(source_path),
                imported_name=alias.name,
                alias=alias.asname or "",
                line_span=(node.lineno, getattr(node, "end_lineno", node.lineno)),
            )
        )
    return records


def _records_for_import_from(node: ast.ImportFrom, source_path: Path) -> list[ImportRecord]:
    """Return records for a from-import statement."""
    module = "." * int(node.level or 0) + (node.module or "")
    records: list[ImportRecord] = []
    for alias in node.names:
        flags = []
        if node.level:
            flags.append("RELATIVE_IMPORT_RISK")
        if alias.name == "*":
            flags.append("STAR_IMPORT")
        records.append(
            ImportRecord(
                schema_version=SCHEMA_VERSION,
                original_module=str(source_path),
                imported_name=f"{module}.{alias.name}" if module else alias.name,
                alias=alias.asname or "",
                is_relative=bool(node.level),
                relative_level=int(node.level or 0),
                is_star=alias.name == "*",
                line_span=(node.lineno, getattr(node, "end_lineno", node.lineno)),
                risk_flags=flags,
            )
        )
    return records


def _extract_symbols(tree: ast.Module, source: str) -> list[RefactorSymbol]:
    """Extract top-level class and function symbols."""
    symbols: list[RefactorSymbol] = []
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            symbols.append(_symbol_from_node(node, "class", source))
        elif isinstance(node, ast.AsyncFunctionDef):
            symbols.append(_symbol_from_node(node, "async_function", source))
        elif isinstance(node, ast.FunctionDef):
            symbols.append(_symbol_from_node(node, "function", source))
    return symbols


def _symbol_from_node(node: ast.AST, kind: str, source: str) -> RefactorSymbol:
    """Build one RefactorSymbol from a class or function AST node."""
    name = getattr(node, "name", "")
    start = int(getattr(node, "lineno", 0) or 0)
    end = int(getattr(node, "end_lineno", start) or start)
    text = _source_segment_by_lines(source, start, end)
    decorators = [_safe_unparse(item) for item in getattr(node, "decorator_list", [])]
    docstring = ast.get_docstring(node) or ""
    flags: list[str] = []
    if decorators:
        flags.append("DECORATOR_RISK")
    if _node_has_nested_symbol(node):
        flags.append("NESTED_SYMBOL_CLUSTER")
    if _node_has_global_statement(node):
        flags.append("GLOBAL_STATE")
    return RefactorSymbol(
        schema_version=SCHEMA_VERSION,
        name=name,
        kind=kind,
        visibility="private" if name.startswith("_") else "public",
        start_line=start,
        end_line=end,
        physical_lines=max(0, end - start + 1),
        decorators=decorators,
        signature=_signature_for_node(node),
        return_annotation=_return_annotation(node),
        has_docstring=bool(docstring),
        docstring_text=docstring,
        docstring_provenance="existing" if docstring else "manual_required",
        references=sorted(_name_references(node)),
        globals_used=sorted(_global_names_in_node(node)),
        atomic_cluster_id=f"symbol:{name}",
        risk_flags=sorted(set(flags)),
        content_hash=hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest(),
    )


def _signature_for_node(node: ast.AST) -> str:
    """Return a compact signature for functions and classes."""
    if isinstance(node, ast.ClassDef):
        bases = [_safe_unparse(base) for base in node.bases]
        return f"class {node.name}({', '.join(bases)})" if bases else f"class {node.name}"
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        args = [arg.arg for arg in node.args.args]
        prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
        return f"{prefix} {node.name}({', '.join(args)})"
    return ""


def _return_annotation(node: ast.AST) -> str:
    """Return a function return annotation when present."""
    returns = getattr(node, "returns", None)
    return _safe_unparse(returns) if returns is not None else ""


def _safe_unparse(node: ast.AST | None) -> str:
    """Return ast.unparse output without propagating parser quirks."""
    if node is None:
        return ""
    try:
        return ast.unparse(node)
    except Exception:
        return type(node).__name__


def _source_segment_by_lines(source: str, start: int, end: int) -> str:
    """Return source lines for hashing without changing formatting."""
    lines = source.splitlines()
    if start <= 0 or end <= 0:
        return ""
    return "\n".join(lines[start - 1:end])


def _name_references(node: ast.AST) -> set[str]:
    """Collect referenced names inside one symbol."""
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
            names.add(child.id)
    return names


def _global_names_in_node(node: ast.AST) -> set[str]:
    """Collect names declared by global statements."""
    names: set[str] = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Global):
            names.update(child.names)
    return names


def _public_api_symbols(
    tree: ast.Module,
    symbols: Iterable[RefactorSymbol],
    all_names: list[str],
) -> list[str]:
    """Return public API symbols based on __all__ or public top-level names."""
    if all_names:
        return sorted(all_names)
    public = [symbol.name for symbol in symbols if symbol.visibility == "public"]
    for name in _top_level_assignment_names(tree):
        if not name.startswith("_"):
            public.append(name)
    return sorted(set(public))


def _top_level_assignment_names(tree: ast.Module) -> list[str]:
    """Return simple top-level assignment target names."""
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.append(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.append(node.target.id)
    return names


def _extract_assignments(tree: ast.Module) -> tuple[list[str], list[str]]:
    """Separate likely constants from other top-level assignment names."""
    constants: list[str] = []
    assignments: list[str] = []
    for name in _top_level_assignment_names(tree):
        if name == "__all__":
            continue
        if name.isupper():
            constants.append(name)
        else:
            assignments.append(name)
    return sorted(set(constants)), sorted(set(assignments))


def _extract_scope_statements(tree: ast.Module) -> tuple[list[str], list[str]]:
    """Collect global and nonlocal declarations anywhere in the module."""
    global_names: set[str] = set()
    nonlocal_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            global_names.update(node.names)
        elif isinstance(node, ast.Nonlocal):
            nonlocal_names.update(node.names)
    return sorted(global_names), sorted(nonlocal_names)


def _extract_module_level_calls(tree: ast.Module) -> list[str]:
    """Collect top-level expression calls that may indicate import side effects."""
    calls: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            calls.append(_safe_unparse(node.value.func))
        elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            calls.append(_safe_unparse(node.value.func))
    return sorted(set(call for call in calls if call))


def _collect_module_risks(
    tree: ast.Module,
    imports: Iterable[ImportRecord],
    symbols: Iterable[RefactorSymbol],
    all_names: list[str],
) -> list[str]:
    """Return module-level risk badges for the evidence panel."""
    risks: list[str] = []
    for item in imports:
        risks.extend(item.risk_flags)
    for item in symbols:
        risks.extend(item.risk_flags)
    if all_names:
        risks.append("PUBLIC_API_RISK")
    if _has_if_main(tree):
        risks.append("PUBLIC_API_RISK")
    if _extract_module_level_calls(tree):
        risks.append("GLOBAL_STATE")
    if any(isinstance(node, ast.Try) for node in tree.body):
        risks.append("DYNAMIC_IMPORT")
    return sorted(set(risks))


def _count_missing_docstrings(
    tree: ast.Module,
    symbols: Iterable[RefactorSymbol],
    module_has_docstring: bool,
) -> int:
    """Count missing docstrings for module and public top-level symbols."""
    count = 0 if module_has_docstring else 1
    for symbol in symbols:
        if symbol.visibility == "public" and not symbol.has_docstring:
            count += 1
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            if ast.get_docstring(node) is None and not _is_top_level(tree, node):
                count += 1
    return count


def _is_top_level(tree: ast.Module, node: ast.AST) -> bool:
    """Return whether a node is a direct module body item."""
    return any(item is node for item in tree.body)


def _count_nested_symbols(tree: ast.Module) -> int:
    """Count nested classes and functions below top-level symbols."""
    count = 0
    for top in tree.body:
        if isinstance(top, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            for child in ast.walk(top):
                if child is top:
                    continue
                if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    count += 1
    return count


def _node_has_nested_symbol(node: ast.AST) -> bool:
    """Return whether a top-level symbol contains nested symbols."""
    for child in ast.walk(node):
        if child is node:
            continue
        if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            return True
    return False


def _node_has_global_statement(node: ast.AST) -> bool:
    """Return whether a symbol uses a global statement."""
    return any(isinstance(child, ast.Global) for child in ast.walk(node))


def _has_if_main(tree: ast.Module) -> bool:
    """Return whether the module has an if __name__ == '__main__' block."""
    for node in tree.body:
        if isinstance(node, ast.If) and _is_if_main_test(node.test):
            return True
    return False


def _is_if_main_test(node: ast.AST) -> bool:
    """Detect the common __name__ == '__main__' test."""
    if not isinstance(node, ast.Compare):
        return False
    if not isinstance(node.left, ast.Name) or node.left.id != "__name__":
        return False
    if not any(isinstance(op, ast.Eq) for op in node.ops):
        return False
    for comparator in node.comparators:
        if isinstance(comparator, ast.Constant) and comparator.value == "__main__":
            return True
    return False


def _preview_docstring(text: str) -> str:
    """Return a compact docstring preview for the evidence panel."""
    if not text:
        return ""
    first = text.strip().splitlines()[0].strip()
    if len(first) > 160:
        return first[:157] + "..."
    return first
