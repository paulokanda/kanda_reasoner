# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/preview_static_quality.py
"""Static quality gates for generated Workbench preview Python files."""
from __future__ import annotations

import ast
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

__all__ = [
    "PreviewStaticQualityResult",
    "inspect_preview_static_quality",
]


@dataclass(frozen=True)
class PreviewStaticQualityResult:
    """Deterministic static quality evidence for one preview module."""

    path: str
    duplicate_all_assignment_lines: list[int] = field(default_factory=list)
    pointless_top_level_string_lines: list[int] = field(default_factory=list)
    fragmented_import_modules: list[str] = field(default_factory=list)
    duplicate_project_path_comment_lines: list[int] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready quality record."""
        return asdict(self)


def inspect_preview_static_quality(path: Path, text: str) -> PreviewStaticQualityResult:
    """Detect transform artifacts that compile but should block human review."""
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError:
        return PreviewStaticQualityResult(
            path=str(path),
            blockers=["PREVIEW_STATIC_QUALITY_AST_PARSE_FAILED"],
        )

    duplicate_all_lines = _duplicate_all_assignment_lines(tree)
    pointless_string_lines = _pointless_top_level_string_lines(tree)
    fragmented_modules = _fragmented_import_modules(tree)
    project_path_lines = _project_path_comment_lines(text)
    duplicate_project_path_lines = project_path_lines if len(project_path_lines) > 1 else []

    blockers: list[str] = []
    if duplicate_all_lines:
        blockers.append(
            "DUPLICATE_PUBLIC_API_ALL_ASSIGNMENT:"
            + ",".join(str(line) for line in duplicate_all_lines)
        )
    if pointless_string_lines:
        blockers.append(
            "POINTLESS_TOP_LEVEL_STRING_EXPRESSION:"
            + ",".join(str(line) for line in pointless_string_lines)
        )
    if fragmented_modules:
        blockers.extend(
            "FRAGMENTED_SAME_MODULE_IMPORTS:" + module
            for module in fragmented_modules
        )
    if duplicate_project_path_lines:
        blockers.append(
            "DUPLICATE_PROJECT_PATH_HEADER:"
            + ",".join(str(line) for line in duplicate_project_path_lines)
        )

    return PreviewStaticQualityResult(
        path=str(path),
        duplicate_all_assignment_lines=duplicate_all_lines,
        pointless_top_level_string_lines=pointless_string_lines,
        fragmented_import_modules=fragmented_modules,
        duplicate_project_path_comment_lines=duplicate_project_path_lines,
        blockers=blockers,
        warnings=[],
    )


def _duplicate_all_assignment_lines(tree: ast.Module) -> list[int]:
    """Return all __all__ assignment lines when more than one exists."""
    lines: list[int] = []
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if any(isinstance(target, ast.Name) and target.id == "__all__" for target in targets):
            lines.append(int(getattr(node, "lineno", 0) or 0))
    return lines if len(lines) > 1 else []


def _pointless_top_level_string_lines(tree: ast.Module) -> list[int]:
    """Return top-level string expressions other than the module docstring."""
    lines: list[int] = []
    for index, node in enumerate(tree.body):
        if not isinstance(node, ast.Expr):
            continue
        value = node.value
        if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
            continue
        if index == 0:
            continue
        lines.append(int(getattr(node, "lineno", 0) or 0))
    return lines


def _fragmented_import_modules(tree: ast.Module) -> list[str]:
    """Return relative modules imported by multiple top-level ImportFrom nodes."""
    counts: dict[tuple[int, str], int] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom):
            continue
        key = (int(node.level or 0), str(node.module or ""))
        counts[key] = counts.get(key, 0) + 1
    return sorted(
        "." * level + module
        for (level, module), count in counts.items()
        if count > 1
    )


def _project_path_comment_lines(text: str) -> list[int]:
    """Return line numbers for project-path header comments."""
    result: list[int] = []
    for index, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("# project-path:"):
            result.append(index)
    return result
