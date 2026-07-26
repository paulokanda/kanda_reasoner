# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/aqr_expected_topology.py
"""Derive approved Preview import edges for AQR topology delta review."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

__all__ = ["derive_expected_preview_import_edges"]


def derive_expected_preview_import_edges(
    *,
    target_relative_path: str,
    preview_result: object,
) -> tuple[str, ...]:
    """Return import edges explicitly justified by Preview generation evidence."""
    target = Path(str(target_relative_path).replace("\\", "/"))
    package_parts = target.parent.parts
    if not package_parts:
        return ()
    package_prefix = ".".join(package_parts)
    project_package = package_parts[0]
    facade_module = package_prefix + "." + target.stem
    edges: set[str] = set()

    files = tuple(getattr(preview_result, "files", ()) or ())
    for item in files:
        role = str(getattr(item, "role", "") or "")
        relative = str(getattr(item, "relative_path", "") or "")
        if role == "public_facade" or not relative:
            continue
        helper_module = package_prefix + "." + Path(relative).stem
        edges.add(helper_module_edge(facade_module, helper_module))

    synthesis = dict(getattr(preview_result, "helper_import_synthesis", {}) or {})
    for record in synthesis.get("records", []) or []:
        if not isinstance(record, dict):
            continue
        helper_filename = str(record.get("helper_filename", "") or "")
        if not helper_filename:
            continue
        importer = package_prefix + "." + Path(helper_filename).stem
        for block in record.get("synthesized_import_blocks", []) or []:
            for imported in _project_imports_from_block(
                str(block),
                package_parts=package_parts,
                project_package=project_package,
            ):
                edges.add(helper_module_edge(importer, imported))

    insertions = dict(
        getattr(preview_result, "facade_global_import_insertion", {}) or {}
    )
    for item in insertions.get("insertions", []) or []:
        if not isinstance(item, dict):
            continue
        helper_filename = str(item.get("helper_filename", "") or "")
        if helper_filename:
            importer = package_prefix + "." + Path(helper_filename).stem
            edges.add(helper_module_edge(importer, facade_module))
    return tuple(sorted(edges))


def helper_module_edge(importer: str, imported: str) -> str:
    """Return canonical edge identity used by Grimp cross-check evidence."""
    return str(importer) + "->" + str(imported)


def _project_imports_from_block(
    block: str,
    *,
    package_parts: tuple[str, ...],
    project_package: str,
) -> tuple[str, ...]:
    """Return project-local modules imported by one approved import block."""
    try:
        tree = ast.parse(block)
    except SyntaxError:
        return ()
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imported = _resolve_import_from(node, package_parts)
            if imported and imported.split(".", 1)[0] == project_package:
                modules.add(imported)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".", 1)[0] == project_package:
                    modules.add(alias.name)
    return tuple(sorted(modules))


def _resolve_import_from(
    node: ast.ImportFrom,
    package_parts: tuple[str, ...],
) -> str:
    """Resolve one relative import to a project module identity."""
    module = str(node.module or "")
    if node.level <= 0:
        return module
    keep = max(0, len(package_parts) - node.level + 1)
    base = list(package_parts[:keep])
    if module:
        base.extend(part for part in module.split(".") if part)
    return ".".join(base)
