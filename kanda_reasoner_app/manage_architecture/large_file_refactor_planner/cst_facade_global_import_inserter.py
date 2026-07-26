# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_facade_global_import_inserter.py
"""Insert cycle-safe local imports for helper dependencies on facade globals."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

def _load_libcst_module() -> Any:
    """Return LibCST when installed, otherwise explicit unavailable evidence."""
    try:
        import libcst as libcst_module
    except Exception:  # pragma: no cover - optional dependency.
        return None
    return libcst_module


cst = _load_libcst_module()

from .models import RefactorPlan, SCHEMA_VERSION
from .workbench_dependency_readiness import WorkbenchDependencyReadinessResult

__all__ = [
    "FacadeGlobalImportInsertion",
    "FacadeGlobalImportInsertionReport",
    "insert_facade_global_dependency_imports",
]


@dataclass(frozen=True)
class FacadeGlobalImportInsertion:
    """Evidence for one cycle-safe function-local facade import insertion."""

    schema_version: str
    helper_filename: str
    symbol_name: str
    facade_module: str
    imported_names: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready insertion evidence."""
        return asdict(self)


@dataclass(frozen=True)
class FacadeGlobalImportInsertionReport:
    """Result of inserting local imports for facade-owned global dependencies."""

    schema_version: str
    status: str
    blocks: dict[str, str]
    insertions: tuple[FacadeGlobalImportInsertion, ...] = ()
    blockers: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready insertion report without duplicating source blocks."""
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "insertions": [item.to_dict() for item in self.insertions],
            "blockers": list(self.blockers),
            "warnings": list(self.warnings),
        }


def insert_facade_global_dependency_imports(
    *,
    plan: RefactorPlan,
    readiness: WorkbenchDependencyReadinessResult | None,
    blocks: dict[str, str],
) -> FacadeGlobalImportInsertionReport:
    """Insert function-local imports for facade globals used by moved helpers.

    The import is intentionally local to the moved function.  A helper-level
    import from the facade would create an import-time cycle because the facade
    imports its moved helper symbols.  Local imports preserve facade ownership
    while deferring resolution until after module initialization.
    """
    if cst is None:
        return _blocked(blocks, ["LIBCST_REQUIRED_FOR_FACADE_GLOBAL_IMPORT_INSERTION"])
    if readiness is None or readiness.dependency_report is None:
        return _blocked(blocks, ["DEPENDENCY_REPORT_REQUIRED_FOR_FACADE_GLOBAL_IMPORT_INSERTION"])

    facade_filename, facade_symbols = _facade_identity(plan, readiness)
    facade_module = Path(facade_filename).stem
    records = {record.name: record for record in readiness.dependency_report.symbols}
    updated = dict(blocks)
    insertions: list[FacadeGlobalImportInsertion] = []
    blockers: list[str] = []

    for module in plan.proposed_modules:
        if module.role == "public_facade":
            continue
        for symbol_name in module.symbols:
            record = records.get(symbol_name)
            if record is None:
                blockers.append(f"DEPENDENCY_RECORD_MISSING:{symbol_name}")
                continue
            globals_used = set(record.global_dependencies)
            facade_globals = sorted(globals_used & facade_symbols)
            unresolved = sorted(globals_used - facade_symbols)
            blockers.extend(
                f"UNRESOLVED_GLOBAL_DEPENDENCY:{symbol_name}:{name}"
                for name in unresolved
            )
            if not facade_globals:
                continue
            source = updated.get(symbol_name)
            if source is None:
                blockers.append(f"SYMBOL_BLOCK_MISSING:{symbol_name}")
                continue
            transformed, transform_blockers = _insert_function_local_import(
                source=source,
                symbol_name=symbol_name,
                facade_module=facade_module,
                names=facade_globals,
            )
            blockers.extend(transform_blockers)
            if transform_blockers:
                continue
            updated[symbol_name] = transformed
            insertions.append(
                FacadeGlobalImportInsertion(
                    schema_version=SCHEMA_VERSION,
                    helper_filename=module.filename,
                    symbol_name=symbol_name,
                    facade_module=facade_module,
                    imported_names=tuple(facade_globals),
                )
            )

    unique_blockers = tuple(sorted(set(blockers)))
    status = "facade_global_import_insertion_ready" if not unique_blockers else "blocked"
    warnings = (
        ("FUNCTION_LOCAL_FACADE_IMPORTS_SYNTHESIZED",)
        if insertions
        else ()
    )
    return FacadeGlobalImportInsertionReport(
        schema_version=SCHEMA_VERSION,
        status=status,
        blocks=updated,
        insertions=tuple(insertions),
        blockers=unique_blockers,
        warnings=warnings,
    )


def _facade_identity(
    plan: RefactorPlan,
    readiness: WorkbenchDependencyReadinessResult,
) -> tuple[str, set[str]]:
    """Return the facade filename and names retained by facade ownership."""
    assignment_names = set(readiness.dependency_report.module_assignments)
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            return module.filename, set(module.symbols) | assignment_names
    return Path(plan.target_file).name, assignment_names


def _insert_function_local_import(
    *,
    source: str,
    symbol_name: str,
    facade_module: str,
    names: list[str],
) -> tuple[str, list[str]]:
    """Insert one relative import after a function docstring, if present."""
    try:
        module = cst.parse_module(source)
    except Exception as exc:
        return source, [f"FACADE_GLOBAL_IMPORT_PARSE_FAILED:{symbol_name}:{type(exc).__name__}"]
    if len(module.body) != 1 or not isinstance(module.body[0], cst.FunctionDef):
        return source, [f"FACADE_GLOBAL_DEPENDENCY_UNSUPPORTED_SYMBOL_KIND:{symbol_name}"]
    function = module.body[0]
    if function.name.value != symbol_name:
        return source, [f"FACADE_GLOBAL_IMPORT_SYMBOL_MISMATCH:{symbol_name}"]
    if not isinstance(function.body, cst.IndentedBlock):
        return source, [f"FACADE_GLOBAL_IMPORT_SIMPLE_SUITE_UNSUPPORTED:{symbol_name}"]

    import_statement = cst.parse_statement(
        f"from .{facade_module} import {', '.join(names)}\n"
    )
    body = list(function.body.body)
    insert_at = 1 if body and _is_docstring_statement(body[0]) else 0
    body.insert(insert_at, import_statement)
    rewritten_function = function.with_changes(
        body=function.body.with_changes(body=tuple(body))
    )
    rewritten_module = module.with_changes(body=(rewritten_function,))
    return rewritten_module.code, []


def _is_docstring_statement(statement: object) -> bool:
    """Return whether a CST statement is a function docstring statement."""
    if not isinstance(statement, cst.SimpleStatementLine):
        return False
    if len(statement.body) != 1 or not isinstance(statement.body[0], cst.Expr):
        return False
    return isinstance(statement.body[0].value, (cst.SimpleString, cst.ConcatenatedString))


def _blocked(
    blocks: dict[str, str],
    blockers: list[str],
) -> FacadeGlobalImportInsertionReport:
    """Return a fail-closed report preserving the unmodified source blocks."""
    return FacadeGlobalImportInsertionReport(
        schema_version=SCHEMA_VERSION,
        status="blocked",
        blocks=dict(blocks),
        blockers=tuple(sorted(set(blockers))),
    )
