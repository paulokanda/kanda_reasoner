# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_completion_payload_evidence.py
"""Derive Completion Review facts from exact sealed payload bytes."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable

from .workbench_sealed_payload import WorkbenchSealedPayload

__all__ = [
    "sealed_payload_import_map",
    "sealed_payload_size_map",
    "sealed_payload_dependency_warnings",
    "plan_size_estimate_warnings",
]


def sealed_payload_size_map(
    payload: WorkbenchSealedPayload,
) -> tuple[tuple[str, int], ...]:
    """Return resulting physical sizes from sealed manifest records only."""
    return tuple(
        sorted(
            (
                (str(Path(item.destination_path).resolve()), int(item.physical_lines))
                for item in payload.files
            ),
            key=lambda item: item[0].casefold(),
        )
    )


def sealed_payload_import_map(
    payload: WorkbenchSealedPayload,
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Return exact import evidence parsed from each sealed Python payload file."""
    records: list[tuple[str, tuple[str, ...]]] = []
    for item in sorted(payload.files, key=lambda value: value.relative_path.casefold()):
        path = Path(item.payload_path).resolve()
        if path.suffix != ".py":
            records.append((item.relative_path, tuple()))
            continue
        tree = ast.parse(path.read_bytes().decode("utf-8"), filename=str(path), type_comments=True)
        imports = _ImportEvidenceCollector().collect(tree)
        records.append((item.relative_path, imports))
    return tuple(records)


def sealed_payload_dependency_warnings(
    payload: WorkbenchSealedPayload,
    *,
    target_file: str | Path,
) -> tuple[str, ...]:
    """Surface deferred/type-only helper back-references without inventing runtime cycles."""
    facade_stem = Path(target_file).stem
    warnings: set[str] = set()
    for module, imports in sealed_payload_import_map(payload):
        if Path(module).stem == facade_stem:
            continue
        for item in imports:
            category, _, imported = item.partition(":")
            imported_module = _imported_module_name(imported)
            if imported_module != facade_stem:
                continue
            edge = f"{Path(module).stem}->{facade_stem}"
            if category == "deferred":
                warnings.add("DEFERRED_FACADE_BACK_REFERENCE:" + edge)
            elif category == "type_checking":
                warnings.add("TYPE_CHECKING_FACADE_BACK_REFERENCE:" + edge)
    return tuple(sorted(warnings))


def plan_size_estimate_warnings(
    estimated_size_map: dict[str, int],
    payload: WorkbenchSealedPayload,
) -> tuple[str, ...]:
    """Report plan estimates that differ from sealed byte truth without replacing truth."""
    exact = dict(sealed_payload_size_map(payload))
    warnings: list[str] = []
    for raw_path, estimated in sorted(estimated_size_map.items(), key=lambda item: item[0].casefold()):
        path = str(Path(raw_path).resolve())
        if path not in exact:
            warnings.append("PLAN_SIZE_ESTIMATE_HAS_NO_SEALED_FILE:" + path)
            continue
        actual = exact[path]
        if int(estimated) != actual:
            warnings.append(
                "PLAN_SIZE_ESTIMATE_DIFFERS_FROM_SEALED_PAYLOAD:"
                + path
                + f":estimated={int(estimated)}:sealed={actual}"
            )
    return tuple(warnings)


class _ImportEvidenceCollector(ast.NodeVisitor):
    """Collect runtime, TYPE_CHECKING-only, and function-local deferred imports."""

    def __init__(self) -> None:
        self._function_depth = 0
        self._type_checking_depth = 0
        self._records: set[str] = set()

    def collect(self, tree: ast.Module) -> tuple[str, ...]:
        self.visit(tree)
        return tuple(sorted(self._records, key=str.casefold))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._visit_function(node)

    def visit_If(self, node: ast.If) -> None:
        if _is_type_checking_test(node.test):
            self._type_checking_depth += 1
            for statement in node.body:
                self.visit(statement)
            self._type_checking_depth -= 1
            for statement in node.orelse:
                self.visit(statement)
            return
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        category = self._category()
        for alias in node.names:
            self._records.add(f"{category}:{alias.name}")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        category = self._category()
        prefix = "." * int(node.level) + str(node.module or "")
        for alias in node.names:
            name = prefix + ("." if prefix and not prefix.endswith(".") else "") + alias.name
            self._records.add(f"{category}:{name}")

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        self._function_depth += 1
        for statement in node.body:
            self.visit(statement)
        self._function_depth -= 1

    def _category(self) -> str:
        if self._type_checking_depth:
            return "type_checking"
        if self._function_depth:
            return "deferred"
        return "runtime"


def _is_type_checking_test(node: ast.expr) -> bool:
    if isinstance(node, ast.Name):
        return node.id == "TYPE_CHECKING"
    if isinstance(node, ast.Attribute) and node.attr == "TYPE_CHECKING":
        return isinstance(node.value, ast.Name) and node.value.id == "typing"
    return False


def _imported_module_name(imported: str) -> str:
    """Return the leaf module from normalized from-import evidence."""
    clean = imported.lstrip(".")
    parts = clean.split(".")
    if len(parts) <= 1:
        return parts[0] if parts else ""
    return parts[-2]
