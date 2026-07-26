# project-path: kanda_reasoner_app/manage_architecture/large_module_target_queue.py
"""Audit-derived target queue helpers for large-module AST split audits."""
from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

__all__ = [
    "LargeModuleTarget",
    "count_python_lines",
    "format_target_counter",
    "normalize_target_text",
    "parse_module_too_large_findings",
    "resolve_target_path",
]

_MODULE_TOO_LARGE_RE = re.compile(
    r"^\s*(?:WARNING|ERROR)\s+MODULE_TOO_LARGE\s+(?P<path>.+?)\s+::\s+Module has\s+(?P<lines>\d+)\s+lines;",
    re.MULTILINE,
)


@dataclass(frozen=True, slots=True)
class LargeModuleTarget:
    """One oversized module target discovered in architecture validation output."""

    path: str
    line_count: int


def parse_module_too_large_findings(text: str) -> list[LargeModuleTarget]:
    """Return oversized module findings sorted from largest to smallest."""
    by_path: dict[str, int] = {}
    for match in _MODULE_TOO_LARGE_RE.finditer(text or ""):
        path = match.group("path").strip().replace("\\", "/")
        try:
            line_count = int(match.group("lines"))
        except ValueError:
            continue
        if line_count <= 500:
            continue
        previous = by_path.get(path)
        if previous is None or line_count > previous:
            by_path[path] = line_count
    targets = [LargeModuleTarget(path=path, line_count=count) for path, count in by_path.items()]
    targets.sort(key=lambda item: (-item.line_count, item.path.lower()))
    return targets


def resolve_target_path(project_root: str | Path, target_path: str | Path) -> Path:
    """Resolve a target path against the project root when it is relative."""
    root = Path(project_root)
    target = Path(str(target_path).strip())
    if target.is_absolute():
        return target
    return root / target


def normalize_target_text(project_root: str | Path, selected_path: str | Path) -> str:
    """Return a UI-friendly project-relative target when possible."""
    root = Path(project_root).resolve()
    selected = Path(selected_path).resolve()
    try:
        return str(selected.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(selected)


def count_python_lines(project_root: str | Path, target_path: str | Path) -> int:
    """Count physical lines for an existing target Python file."""
    path = resolve_target_path(project_root, target_path)
    if not path.exists() or not path.is_file():
        return 0
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return 0


def format_target_counter(targets: list[LargeModuleTarget], index: int) -> str:
    """Format the selector counter shown beside the AST target path."""
    if not targets:
        return "0 large modules"
    safe_index = max(0, min(index, len(targets) - 1))
    target = targets[safe_index]
    return f"{safe_index + 1}/{len(targets)} | {target.line_count} lines"
