# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/cst_symbol_source_extractor.py
"""Source-block extraction for real moved-code preview generation."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
import importlib.util
from pathlib import Path
from typing import Any

__all__ = [
    "SourceExtractionResult",
    "extract_source_blocks",
    "libcst_available",
]


@dataclass(frozen=True)
class SourceExtractionResult:
    """Source blocks used by the preview writer."""

    extraction_backend: str
    symbol_blocks: dict[str, str]
    import_blocks: list[str]
    retained_facade_blocks: list[str]
    symbol_order: list[str]
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready extraction report."""
        return asdict(self)


def extract_source_blocks(path: Path, moved_symbols: set[str]) -> SourceExtractionResult:
    """Extract top-level source blocks with LibCST when present, else AST spans."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return _blocked([f"SOURCE_READ_FAILED:{exc}"])
    libcst_result = _extract_with_libcst(source, moved_symbols)
    if libcst_result is not None:
        return libcst_result
    return _extract_with_ast(source, moved_symbols)


def libcst_available() -> bool:
    """Return whether LibCST is importable in this environment."""
    return importlib.util.find_spec("libcst") is not None


def _extract_with_libcst(source: str, moved_symbols: set[str]) -> SourceExtractionResult | None:
    """Return LibCST-position extraction evidence, or None when unavailable."""
    if not libcst_available():
        return None
    try:
        import libcst as cst  # type: ignore[import-not-found]
        from libcst.metadata import MetadataWrapper, PositionProvider  # type: ignore[import-not-found]
    except Exception:
        return None
    try:
        wrapper = MetadataWrapper(cst.parse_module(source))
        positions = wrapper.resolve(PositionProvider)
        module = wrapper.module
    except Exception as exc:
        return SourceExtractionResult(
            extraction_backend="libcst_parse_failed_ast_not_attempted",
            symbol_blocks={},
            import_blocks=[],
            retained_facade_blocks=[],
            symbol_order=[],
            blockers=[f"LIBCST_PARSE_FAILED:{exc}"],
            warnings=["LIBCST_AVAILABLE_BUT_PARSE_FAILED"],
        )
    lines = source.splitlines()
    imports: list[str] = []
    retained: list[str] = []
    symbols: dict[str, str] = {}
    order: list[str] = []
    for statement in module.body:
        position = positions.get(statement)
        if position is None:
            continue
        start = _include_leading_comments(lines, position.start.line)
        end = position.end.line
        if isinstance(statement, (cst.FunctionDef, cst.ClassDef)):
            start = _libcst_symbol_start_line(
                lines,
                statement,
                positions,
                position.start.line,
            )
        text = _slice_lines(lines, start, end)
        if isinstance(statement, (cst.FunctionDef, cst.ClassDef)):
            name = statement.name.value
            order.append(name)
            if name in moved_symbols:
                symbols[name] = text
            else:
                retained.append(text)
        elif isinstance(statement, cst.SimpleStatementLine) and _is_libcst_import_statement(cst, statement):
            imports.append(text)
        else:
            retained.append(text)
    return SourceExtractionResult(
        extraction_backend="libcst_position_provider",
        symbol_blocks=symbols,
        import_blocks=_dedupe_preserve(imports),
        retained_facade_blocks=retained,
        symbol_order=order,
        warnings=["LIBCST_POSITION_EXTRACTION_USED"],
    )


def _extract_with_ast(source: str, moved_symbols: set[str]) -> SourceExtractionResult:
    """Return source blocks using AST source spans without requiring LibCST."""
    try:
        tree = ast.parse(source, type_comments=True)
    except SyntaxError as exc:
        return _blocked([f"AST_PARSE_FAILED:{exc}"])
    lines = source.splitlines()
    imports: list[str] = []
    retained: list[str] = []
    symbols: dict[str, str] = {}
    order: list[str] = []
    for node in tree.body:
        start = getattr(node, "lineno", 0)
        end = getattr(node, "end_lineno", start)
        if not start or not end:
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(_slice_lines(lines, start, end))
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = _symbol_start_line(lines, node)
            text = _slice_lines(lines, start, end)
            order.append(node.name)
            if node.name in moved_symbols:
                symbols[node.name] = text
            else:
                retained.append(text)
            continue
        retained.append(_slice_lines(lines, start, end))
    return SourceExtractionResult(
        extraction_backend="ast_source_span_fallback",
        symbol_blocks=symbols,
        import_blocks=_dedupe_preserve(imports),
        retained_facade_blocks=retained,
        symbol_order=order,
        warnings=["AST_SOURCE_SPAN_EXTRACTION_USED", "LIBCST_NOT_AVAILABLE_OR_NOT_USED"],
    )



def _libcst_symbol_start_line(
    lines: list[str],
    statement: Any,
    positions: dict[Any, Any],
    fallback_line: int,
) -> int:
    """Return a LibCST symbol start line including decorators and comments."""
    start = fallback_line
    for decorator in getattr(statement, "decorators", ()):
        position = positions.get(decorator)
        if position is not None:
            start = min(start, position.start.line)
    return _include_leading_comments(lines, start)

def _is_libcst_import_statement(cst_module: Any, statement: Any) -> bool:
    """Return whether a LibCST simple statement contains an import node."""
    return any(isinstance(item, (cst_module.Import, cst_module.ImportFrom)) for item in statement.body)


def _symbol_start_line(lines: list[str], node: ast.AST) -> int:
    """Return the start line including decorators and attached comments."""
    start = getattr(node, "lineno", 1)
    decorators = getattr(node, "decorator_list", [])
    if decorators:
        start = min(start, *(getattr(item, "lineno", start) for item in decorators))
    return _include_leading_comments(lines, start)


def _include_leading_comments(lines: list[str], start_line: int) -> int:
    """Include immediately attached comments above a top-level block."""
    index = max(start_line - 2, -1)
    while index >= 0:
        stripped = lines[index].strip()
        if stripped.startswith("#"):
            index -= 1
            continue
        if stripped == "" and index > 0 and lines[index - 1].strip().startswith("#"):
            index -= 1
            continue
        break
    return index + 2


def _slice_lines(lines: list[str], start_line: int, end_line: int) -> str:
    """Return one-based inclusive source text."""
    return "\n".join(lines[start_line - 1 : end_line]).rstrip()


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


def _blocked(blockers: list[str]) -> SourceExtractionResult:
    """Return blocked extraction evidence."""
    return SourceExtractionResult(
        extraction_backend="blocked",
        symbol_blocks={},
        import_blocks=[],
        retained_facade_blocks=[],
        symbol_order=[],
        blockers=sorted(set(blockers)),
        warnings=[],
    )
