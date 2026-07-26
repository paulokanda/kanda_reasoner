# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/helper_import_synthesizer.py
"""Synthesize helper import blocks from dependency-readiness evidence."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .models import RefactorPlan, SCHEMA_VERSION
from .symbol_dependency_builder import SymbolDependencyReport, SymbolDependencyRecord
from .workbench_dependency_readiness import WorkbenchDependencyReadinessResult

__all__ = [
    "HelperImportSynthesisRecord",
    "HelperImportSynthesisReport",
    "synthesize_helper_imports",
]


@dataclass(frozen=True)
class HelperImportSynthesisRecord:
    """Import synthesis evidence for one generated helper module."""

    schema_version: str
    helper_filename: str
    helper_role: str
    symbols: list[str]
    required_import_names: list[str] = field(default_factory=list)
    synthesized_import_blocks: list[str] = field(default_factory=list)
    unresolved_import_names: list[str] = field(default_factory=list)
    global_dependency_names: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready record."""
        return asdict(self)


@dataclass(frozen=True)
class HelperImportSynthesisReport:
    """Synthesis report for helper import blocks."""

    schema_version: str
    status: str
    target_file: str
    records: list[HelperImportSynthesisRecord]
    fallback_all_imports: bool = False
    source_mutation_enabled: bool = False
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready synthesis report."""
        data = asdict(self)
        data["records"] = [item.to_dict() for item in self.records]
        return data

    def imports_for_module(self, filename: str) -> list[str]:
        """Return synthesized import blocks for one helper filename."""
        for record in self.records:
            if record.helper_filename == filename:
                return list(record.synthesized_import_blocks)
        return []


def synthesize_helper_imports(
    *,
    plan: RefactorPlan,
    readiness: WorkbenchDependencyReadinessResult | None,
    import_blocks: list[str],
) -> HelperImportSynthesisReport:
    """Build per-helper import blocks from symbol dependency evidence."""
    report = readiness.dependency_report if readiness is not None else None
    if report is None:
        return _fallback_report(plan, import_blocks, ["DEPENDENCY_REPORT_MISSING"])
    import_index = _build_import_index(import_blocks)
    future_imports = _future_import_blocks(import_blocks)
    symbol_records = {record.name: record for record in report.symbols}
    facade_filename, facade_symbols = _facade_identity(plan)
    facade_module = Path(facade_filename).stem
    records: list[HelperImportSynthesisRecord] = []
    warnings: set[str] = set(_module_import_warnings(import_blocks, report))
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            continue
        records.append(
            _record_for_helper(
                module.filename,
                module.role,
                module.symbols,
                symbol_records,
                import_index,
                import_blocks,
                future_imports,
                facade_module,
                facade_symbols,
            )
        )
    warnings.update(warning for item in records for warning in item.warnings)
    return HelperImportSynthesisReport(
        schema_version=SCHEMA_VERSION,
        status="helper_import_synthesis_ready",
        target_file=str(Path(plan.target_file)),
        records=records,
        fallback_all_imports=False,
        source_mutation_enabled=False,
        blockers=[],
        warnings=sorted(warnings | set(_stable_warnings())),
    )


def _record_for_helper(
    filename: str,
    role: str,
    symbols: list[str],
    symbol_records: dict[str, SymbolDependencyRecord],
    import_index: dict[str, list[str]],
    import_blocks: list[str],
    future_imports: list[str],
    facade_module: str,
    facade_symbols: set[str],
) -> HelperImportSynthesisRecord:
    """Return import synthesis for one helper module."""
    required: set[str] = set()
    globals_used: set[str] = set()
    type_hints_used: set[str] = set()
    missing_records: list[str] = []
    for symbol in symbols:
        record = symbol_records.get(symbol)
        if record is None:
            missing_records.append(symbol)
            continue
        required.update(record.import_dependencies)
        globals_used.update(record.global_dependencies)
        type_hints_used.update(record.type_hint_dependencies)
        required.update(name for name in record.decorator_dependencies if name in import_index)
        required.update(name for name in record.type_hint_dependencies if name in import_index)
    blocks: list[str] = list(future_imports)
    unresolved = sorted(name for name in required if name not in import_index)
    blocks.extend(_filtered_import_blocks(import_blocks, required))
    type_only_facade = sorted((type_hints_used & facade_symbols) - globals_used)
    if type_only_facade:
        blocks.extend(_type_checking_import_blocks(facade_module, type_only_facade))
    warnings: set[str] = set()
    if missing_records:
        warnings.add("SYMBOL_DEPENDENCY_RECORD_MISSING")
    if globals_used:
        warnings.add("GLOBAL_DEPENDENCY_REQUIRES_FACADE_OR_MANUAL_REVIEW")
    if unresolved:
        warnings.add("UNRESOLVED_HELPER_IMPORT_DEPENDENCY")
    return HelperImportSynthesisRecord(
        schema_version=SCHEMA_VERSION,
        helper_filename=filename,
        helper_role=role,
        symbols=list(symbols),
        required_import_names=sorted(required),
        synthesized_import_blocks=_dedupe_preserve(blocks),
        unresolved_import_names=sorted(unresolved),
        global_dependency_names=sorted(globals_used),
        warnings=sorted(warnings),
    )




def _facade_identity(plan: RefactorPlan) -> tuple[str, set[str]]:
    """Return facade filename and symbols retained as public ownership."""
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            return module.filename, set(module.symbols)
    return Path(plan.target_file).name, set()


def _type_checking_import_blocks(facade_module: str, names: list[str]) -> list[str]:
    """Return cycle-safe imports for facade-owned annotation dependencies."""
    joined = ", ".join(names)
    return [
        "from typing import TYPE_CHECKING",
        f"if TYPE_CHECKING:\n    from .{facade_module} import {joined}",
    ]

def _filtered_import_blocks(import_blocks: list[str], required: set[str]) -> list[str]:
    """Return import statements narrowed to names required by one helper."""
    rendered: list[str] = []
    for block in import_blocks:
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                continue
            narrowed = _narrow_import_node(node, required)
            if narrowed is not None:
                rendered.append(ast.unparse(narrowed))
    return _dedupe_preserve(rendered)


def _narrow_import_node(node: ast.AST, required: set[str]) -> ast.AST | None:
    """Return one import node containing only locally required aliases."""
    if isinstance(node, ast.Import):
        aliases = [
            alias
            for alias in node.names
            if (alias.asname or alias.name.split(".")[0]) in required
        ]
        return ast.Import(names=aliases) if aliases else None
    if isinstance(node, ast.ImportFrom):
        aliases = [
            alias
            for alias in node.names
            if alias.name == "*" or (alias.asname or alias.name) in required
        ]
        if not aliases:
            return None
        return ast.ImportFrom(module=node.module, names=aliases, level=node.level)
    return None

def _build_import_index(import_blocks: list[str]) -> dict[str, list[str]]:
    """Map imported root names to their original import statements."""
    index: dict[str, list[str]] = {}
    for block in import_blocks:
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        for node in tree.body:
            for name in _names_from_import_node(node):
                index.setdefault(name, []).append(block)
    return {name: _dedupe_preserve(blocks) for name, blocks in index.items()}


def _names_from_import_node(node: ast.AST) -> list[str]:
    """Return local names owned by one import node."""
    names: list[str] = []
    if isinstance(node, ast.Import):
        for alias in node.names:
            names.append(alias.asname or alias.name.split(".")[0])
    elif isinstance(node, ast.ImportFrom):
        for alias in node.names:
            if alias.name == "*":
                names.append("*")
            else:
                names.append(alias.asname or alias.name)
    return names


def _future_import_blocks(import_blocks: list[str]) -> list[str]:
    """Return future import blocks that should remain first in helpers."""
    result: list[str] = []
    for block in import_blocks:
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        if any(isinstance(node, ast.ImportFrom) and node.module == "__future__" for node in tree.body):
            result.append(block)
    return _dedupe_preserve(result)


def _module_import_warnings(import_blocks: list[str], report: SymbolDependencyReport) -> list[str]:
    """Return warnings about import forms that require manual review."""
    warnings: set[str] = set()
    for block in import_blocks:
        try:
            tree = ast.parse(block)
        except SyntaxError:
            warnings.add("IMPORT_BLOCK_PARSE_FAILED_REVIEW_REQUIRED")
            continue
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.level:
                warnings.add("RELATIVE_IMPORT_REVIEW_REQUIRED")
            if isinstance(node, ast.ImportFrom) and any(alias.name == "*" for alias in node.names):
                warnings.add("STAR_IMPORT_REVIEW_REQUIRED")
    if any(record.global_dependencies for record in report.symbols):
        warnings.add("GLOBAL_DEPENDENCY_REVIEW_REQUIRED")
    return sorted(warnings)


def _fallback_report(
    plan: RefactorPlan,
    import_blocks: list[str],
    warnings: list[str],
) -> HelperImportSynthesisReport:
    """Return a safe all-import fallback when dependency evidence is unavailable."""
    records: list[HelperImportSynthesisRecord] = []
    for module in plan.proposed_modules:
        if module.role == "public_facade":
            continue
        records.append(
            HelperImportSynthesisRecord(
                schema_version=SCHEMA_VERSION,
                helper_filename=module.filename,
                helper_role=module.role,
                symbols=list(module.symbols),
                synthesized_import_blocks=_dedupe_preserve(import_blocks),
                warnings=["FALLBACK_ALL_IMPORTS_USED"],
            )
        )
    return HelperImportSynthesisReport(
        schema_version=SCHEMA_VERSION,
        status="helper_import_synthesis_fallback",
        target_file=str(Path(plan.target_file)),
        records=records,
        fallback_all_imports=True,
        source_mutation_enabled=False,
        blockers=[],
        warnings=sorted(set(warnings + ["FALLBACK_ALL_IMPORTS_USED", *_stable_warnings()])),
    )


def _dedupe_preserve(items: list[str]) -> list[str]:
    """Dedupe strings while preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _stable_warnings() -> list[str]:
    """Return stable warnings for this preview-only synthesis train."""
    return [
        "HELPER_IMPORT_SYNTHESIS_PREVIEW_ONLY",
        "SOURCE_MUTATION_DISABLED",
        "IMPORT_REWRITE_DISABLED",
    ]
