# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_preview_rendering.py
"""Rendering helpers for real moved-code preview files."""
from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path

from .models import RefactorPlan

__all__ = [
    "PREVIEW_HEADER",
    "clean_preview_text",
    "render_preview_facade",
    "render_preview_helper",
]

PREVIEW_HEADER = "# KANDA PREVIEW ARTIFACT - NOT SOURCE TRUTH"


def render_preview_facade(
    plan: RefactorPlan,
    filename: str,
    imports: list[str],
    retained_blocks: list[str],
    helper_for_symbol: dict[str, str],
    extraction_backend: str,
    *,
    compatibility_import_names: set[str] | None = None,
) -> str:
    """Return facade preview text that re-exports moved symbols."""
    preamble_blocks, body_blocks = _partition_facade_blocks(retained_blocks)
    public = sorted(name for name in plan.public_api_after_expected if name.isidentifier())
    loaded_or_public_names = _loaded_names(retained_blocks) | set(public)
    compatibility_names = set(compatibility_import_names or set())
    retained_names = loaded_or_public_names | compatibility_names
    facade_imports = _filtered_import_blocks(imports, retained_names)
    moved_imports = _render_grouped_moved_imports(
        {name: helper for name, helper in helper_for_symbol.items() if name in retained_names},
        explicit_reexports=compatibility_names - loaded_or_public_names,
    )
    preamble_spacing = [""] if preamble_blocks else []
    synthetic_docstring = [] if preamble_blocks else [
        '"""Preview facade preserving the original module public surface."""',
        "",
    ]
    synthetic_all = [] if _contains_all_assignment(body_blocks) else [
        "__all__ = " + repr(public),
        "",
    ]
    body = [
        PREVIEW_HEADER,
        f"# Preview facade for {filename}.",
        f"# Target source: {plan.target_file}",
        f"# Source hash: {plan.source_content_hash}",
        f"# Extraction backend: {extraction_backend}",
        "# Source mutation is disabled; this file belongs only in selected project Preview support.",
        "",
        *preamble_blocks,
        *preamble_spacing,
        *synthetic_docstring,
        *facade_imports,
        "",
        *moved_imports,
        "",
        *synthetic_all,
        *body_blocks,
    ]
    return clean_preview_text(body)


def render_preview_helper(
    plan: RefactorPlan,
    filename: str,
    role: str,
    symbols: list[str],
    imports: list[str],
    by_symbol: dict[str, str],
    extraction_backend: str,
) -> str:
    """Return helper preview text containing actual moved symbol bodies."""
    blocks = [by_symbol[name] for name in symbols if name in by_symbol]
    missing = [name for name in symbols if name not in by_symbol]
    body = [
        PREVIEW_HEADER,
        f"# Preview helper role: {role}",
        f"# Target source: {plan.target_file}",
        f"# Source hash: {plan.source_content_hash}",
        f"# Extraction backend: {extraction_backend}",
        "# Source mutation is disabled; this file belongs only in selected project Preview support.",
        "",
        f'"""Preview helper module for {role.replace("_", " ")}."""',
        "",
        *imports,
        "",
    ]
    if missing:
        body.append("# Missing planned symbols: " + ", ".join(missing))
    body.extend(blocks or ["# No movable symbol body was available for this helper."])
    return clean_preview_text(body)


def clean_preview_text(parts: list[str]) -> str:
    """Join code parts with stable newline termination."""
    lines: list[str] = []
    blank_pending = False
    for part in parts:
        if part == "":
            if not blank_pending:
                lines.append("")
            blank_pending = True
            continue
        for line in str(part).splitlines():
            lines.append(line.rstrip())
        blank_pending = False
    return "\n".join(lines).rstrip() + "\n"



def _loaded_names(blocks: list[str]) -> set[str]:
    """Return loaded names referenced by retained facade blocks."""
    names: set[str] = set()
    for block in blocks:
        try:
            tree = ast.parse(block)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                names.add(node.id)
    return names


def _filtered_import_blocks(import_blocks: list[str], needed: set[str]) -> list[str]:
    """Return facade imports narrowed to names referenced by retained code."""
    rendered: list[str] = []
    for block in import_blocks:
        try:
            tree = ast.parse(block)
        except SyntaxError:
            rendered.append(block)
            continue
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == "__future__":
                rendered.append(ast.unparse(node))
                continue
            aliases = []
            if isinstance(node, ast.Import):
                aliases = [
                    alias
                    for alias in node.names
                    if (alias.asname or alias.name.split(".")[0]) in needed
                ]
                if aliases:
                    rendered.append(ast.unparse(ast.Import(names=aliases)))
            elif isinstance(node, ast.ImportFrom):
                aliases = [
                    alias
                    for alias in node.names
                    if alias.name == "*" or (alias.asname or alias.name) in needed
                ]
                if aliases:
                    rendered.append(
                        ast.unparse(ast.ImportFrom(module=node.module, names=aliases, level=node.level))
                    )
    return rendered

def _partition_facade_blocks(blocks: list[str]) -> tuple[list[str], list[str]]:
    """Move the original module docstring block to the facade preamble."""
    preamble: list[str] = []
    body: list[str] = []
    for block in blocks:
        if not preamble and _block_is_docstring(block):
            preamble.append(block)
        else:
            body.append(block)
    return preamble, body


def _block_is_docstring(block: str) -> bool:
    """Return whether one retained block is a module-docstring statement."""
    try:
        tree = ast.parse(block)
    except SyntaxError:
        return False
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
        return False
    value = tree.body[0].value
    return isinstance(value, ast.Constant) and isinstance(value.value, str)


def _contains_all_assignment(blocks: list[str]) -> bool:
    """Return whether retained facade blocks already define __all__."""
    source = "\n\n".join(blocks)
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
                return True
    return False


def _render_grouped_moved_imports(
    helper_for_symbol: dict[str, str],
    *,
    explicit_reexports: set[str] | None = None,
) -> list[str]:
    """Render stable helper imports and mark compatibility-only reexports."""
    grouped: dict[str, list[str]] = defaultdict(list)
    reexports = set(explicit_reexports or set())
    for symbol, helper in sorted(helper_for_symbol.items()):
        grouped[Path(helper).stem].append(symbol)

    rendered: list[str] = []
    for helper_stem in sorted(grouped):
        symbols = sorted(grouped[helper_stem])
        if len(symbols) == 1:
            symbol = symbols[0]
            imported = _render_imported_symbol(symbol, reexports)
            rendered.append(f"from .{helper_stem} import {imported}")
            continue
        rendered.append(f"from .{helper_stem} import (")
        rendered.extend(
            f"    {_render_imported_symbol(symbol, reexports)},"
            for symbol in symbols
        )
        rendered.append(")")
    return rendered


def _render_imported_symbol(symbol: str, explicit_reexports: set[str]) -> str:
    """Return a normal import name or Ruff-safe explicit compatibility reexport."""
    if symbol in explicit_reexports:
        return f"{symbol} as {symbol}"
    return symbol
