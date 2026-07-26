# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/facade_consumer_compatibility.py
"""Discover moved symbols that project consumers still import from a facade."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .models import SCHEMA_VERSION

__all__ = [
    "FacadeConsumerCompatibilityReport",
    "build_facade_consumer_compatibility_report",
]

_SKIP_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "env",
    "venv",
}


@dataclass(frozen=True)
class FacadeConsumerCompatibilityReport:
    """Describe moved symbols that must remain importable from the facade."""

    schema_version: str
    status: str
    target_module: str
    imported_moved_symbols: tuple[str, ...]
    importer_files: tuple[str, ...]
    blockers: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready compatibility evidence."""
        return asdict(self)


def build_facade_consumer_compatibility_report(
    *,
    active_project_root: str | Path,
    target_file: str | Path,
    moved_symbols: Iterable[str],
) -> FacadeConsumerCompatibilityReport:
    """Find moved symbols imported from the target module by project consumers."""
    root = Path(active_project_root).resolve()
    target = Path(target_file).resolve()
    moved = {str(name) for name in moved_symbols if str(name).isidentifier()}
    blockers: set[str] = set()
    warnings: set[str] = set()
    imported: set[str] = set()
    importers: set[str] = set()

    if not _is_relative_to(target, root):
        blockers.add("FACADE_TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT")
        return _report(root, target, moved, imported, importers, blockers, warnings)

    target_module = _module_name_for_path(target, root)
    if not target_module:
        blockers.add("FACADE_TARGET_MODULE_IDENTITY_UNRESOLVED")
        return _report(root, target, moved, imported, importers, blockers, warnings)

    target_stem = target.stem
    for path in _iter_python_files(root):
        if path.resolve() == target:
            continue
        try:
            source = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if target_stem not in source and target_module not in source:
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError:
            blockers.add(
                "FACADE_CONSUMER_IMPORTER_PARSE_FAILED:" + _safe_relative(path, root)
            )
            continue

        names, star_import, needs_review = _consumer_names(
            tree=tree,
            importer_path=path,
            project_root=root,
            target_module=target_module,
            moved_symbols=moved,
        )
        if names:
            imported.update(names)
            importers.add(_safe_relative(path, root))
        if star_import:
            blockers.add(
                "FACADE_CONSUMER_STAR_IMPORT_REQUIRES_MANUAL_REVIEW:"
                + _safe_relative(path, root)
            )
        if needs_review:
            warnings.add(
                "FACADE_CONSUMER_DOTTED_MODULE_IMPORT_REVIEW:"
                + _safe_relative(path, root)
            )

    if imported:
        warnings.add("FACADE_CONSUMER_COMPATIBILITY_REEXPORTS_REQUIRED")
    else:
        warnings.add("NO_MOVED_SYMBOL_CONSUMER_REEXPORTS_REQUIRED")

    return _report(root, target, moved, imported, importers, blockers, warnings)


def _report(
    root: Path,
    target: Path,
    moved: set[str],
    imported: set[str],
    importers: set[str],
    blockers: set[str],
    warnings: set[str],
) -> FacadeConsumerCompatibilityReport:
    target_module = _module_name_for_path(target, root) if _is_relative_to(target, root) else ""
    invalid = sorted(imported - moved)
    if invalid:
        blockers.add("FACADE_CONSUMER_SYMBOL_OUTSIDE_MOVED_SET:" + ",".join(invalid))
    return FacadeConsumerCompatibilityReport(
        schema_version=SCHEMA_VERSION,
        status="blocked" if blockers else "facade_consumer_compatibility_ready",
        target_module=target_module,
        imported_moved_symbols=tuple(sorted(imported & moved)),
        importer_files=tuple(sorted(importers)),
        blockers=tuple(sorted(blockers)),
        warnings=tuple(sorted(warnings)),
    )


def _consumer_names(
    *,
    tree: ast.Module,
    importer_path: Path,
    project_root: Path,
    target_module: str,
    moved_symbols: set[str],
) -> tuple[set[str], bool, bool]:
    imported: set[str] = set()
    module_aliases: set[str] = set()
    star_import = False
    needs_review = False
    package_parts = _package_parts_for_importer(importer_path, project_root)
    target_parts = target_module.split(".")
    target_parent = ".".join(target_parts[:-1])
    target_name = target_parts[-1]

    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            resolved = _resolve_from_module(node, package_parts)
            if resolved == target_module:
                for alias in node.names:
                    if alias.name == "*":
                        star_import = True
                    elif alias.name in moved_symbols:
                        imported.add(alias.name)
                continue
            if resolved == target_parent:
                for alias in node.names:
                    if alias.name == target_name:
                        module_aliases.add(alias.asname or alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == target_module:
                    if alias.asname:
                        module_aliases.add(alias.asname)
                    else:
                        needs_review = True

    if module_aliases:
        imported.update(_attribute_names_for_aliases(tree, module_aliases) & moved_symbols)
        imported.update(_getattr_names_for_aliases(tree, module_aliases) & moved_symbols)
    return imported, star_import, needs_review


def _attribute_names_for_aliases(tree: ast.AST, aliases: set[str]) -> set[str]:
    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id in aliases
    }


def _getattr_names_for_aliases(tree: ast.AST, aliases: set[str]) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or len(node.args) < 2:
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "getattr":
            continue
        owner, name = node.args[0], node.args[1]
        if (
            isinstance(owner, ast.Name)
            and owner.id in aliases
            and isinstance(name, ast.Constant)
            and isinstance(name.value, str)
        ):
            names.add(name.value)
    return names


def _resolve_from_module(node: ast.ImportFrom, package_parts: list[str]) -> str:
    if node.level == 0:
        return str(node.module or "")
    ascend = node.level - 1
    if ascend > len(package_parts):
        return ""
    base = package_parts[: len(package_parts) - ascend]
    if node.module:
        base.extend(str(node.module).split("."))
    return ".".join(base)


def _package_parts_for_importer(path: Path, root: Path) -> list[str]:
    relative = path.resolve().relative_to(root.resolve())
    parts = list(relative.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        return parts[:-1]
    return parts[:-1]


def _module_name_for_path(path: Path, root: Path) -> str:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        return ""
    parts = list(relative.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _iter_python_files(root: Path):
    for path in root.rglob("*.py"):
        if any(part in _SKIP_DIR_NAMES for part in path.parts):
            continue
        yield path


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path.resolve()).replace("\\", "/")


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
