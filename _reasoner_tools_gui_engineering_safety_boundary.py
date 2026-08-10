# project-path: _reasoner_tools_gui_engineering_safety_boundary.py
"""Private Tool/Project boundary helpers for Engineering Safety commands."""

from __future__ import annotations

import ast
import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

__all__: list[str] = []

_TOOL_ROOT = Path(__file__).resolve().parent


class ProjectContextUnavailable(RuntimeError):
    """Raised when no safe selected-Project target can seed a targeted audit."""


@dataclass(frozen=True)
class ProjectCommandContext:
    """Project-owned target seed for Complete Review targeted commands."""

    root: Path
    target: str
    module: str
    symbol: str
    project_name: str


def tool_root() -> Path:
    """Return the KANDA Tool implementation root, never the audit target."""
    return _TOOL_ROOT


def is_within(path: Path, root: Path) -> bool:
    """Return whether path resolves inside root without lexical-prefix tricks."""
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
    except ValueError:
        return False
    return True


def require_tool_module_origin(module: ModuleType, label: str) -> None:
    """Reject a Project-shadowed implementation of a Tool-owned module."""
    origin_text = str(getattr(module, "__file__", "") or "").strip()
    if not origin_text:
        raise RuntimeError("TOOL_MODULE_PROVENANCE_MISSING:" + label)
    origin = Path(origin_text).resolve(strict=False)
    if not is_within(origin, _TOOL_ROOT):
        raise RuntimeError(
            "TOOL_MODULE_PROVENANCE_VIOLATION:" + label + ":" + str(origin)
        )


def import_tool_module(module_name: str, label: str) -> ModuleType:
    """Import Tool code without allowing the selected Project to shadow it."""
    top_name = module_name.split(".", 1)[0]
    loaded_top = sys.modules.get(top_name)
    if loaded_top is not None:
        require_tool_module_origin(loaded_top, top_name)

    loaded = sys.modules.get(module_name)
    if loaded is not None:
        require_tool_module_origin(loaded, label)
        return loaded

    tool_text = str(_TOOL_ROOT)
    original_path = list(sys.path)
    try:
        sys.path[:] = [tool_text, *(value for value in original_path if value != tool_text)]
        module = importlib.import_module(module_name)
    finally:
        sys.path[:] = original_path
    require_tool_module_origin(module, label)
    return module


def _file_rank(path: Path, root: Path) -> tuple[object, ...]:
    relative = path.relative_to(root)
    lower_parts = tuple(part.casefold() for part in relative.parts)
    name = relative.name.casefold()
    test_like = any(
        part in {"test", "tests", "testing", "dev_tools_tests"}
        or part.startswith("test_")
        for part in lower_parts[:-1]
    ) or name.startswith("test_") or name.endswith("_test.py")
    preferred = name in {
        "main.py",
        "app.py",
        "cli.py",
        "gui.py",
        root.name.casefold() + ".py",
    }
    return (
        int(test_like),
        int(not preferred),
        int(name == "__init__.py"),
        int(name.startswith("_")),
        len(relative.parts),
        relative.as_posix().casefold(),
    )


def _module_text(relative: Path) -> str:
    parts = list(relative.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    if parts and all(part.isidentifier() for part in parts):
        return ".".join(parts)
    return relative.as_posix()


def project_command_context(project_root: str | Path) -> ProjectCommandContext:
    """Derive one audit seed exclusively from canonical selected-Project source."""
    root = Path(project_root).expanduser().resolve(strict=False)
    if not root.is_dir():
        raise ProjectContextUnavailable("active Project root does not exist")

    collector = import_tool_module(
        "kanda_reasoner_app.reasoner_context_collector",
        "reasoner_context_collector",
    )
    collect = getattr(collector, "collect_canonical_project_python_files", None)
    if not callable(collect):
        raise RuntimeError("CANONICAL_PROJECT_SCOPE_PUBLIC_FACADE_REQUIRED")

    candidates: list[Path] = []
    for value in collect(root):
        path = Path(value).resolve(strict=False)
        if not is_within(path, root):
            raise RuntimeError("CANONICAL_PROJECT_SCOPE_ESCAPED_ACTIVE_ROOT:" + str(path))
        if path.is_file():
            candidates.append(path)
    candidates = sorted(set(candidates), key=lambda item: _file_rank(item, root))
    if not candidates:
        raise ProjectContextUnavailable("no canonical Project Python files")

    first_parseable: tuple[Path, ast.Module] | None = None
    symbol_match: tuple[Path, str] | None = None
    for path in candidates:
        try:
            tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except (OSError, UnicodeError, SyntaxError):
            continue
        if first_parseable is None:
            first_parseable = (path, tree)
        functions = [
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not node.name.startswith("_")
        ]
        if not functions:
            functions = [
                node.name
                for node in tree.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
        if functions:
            symbol_match = (path, "main" if "main" in functions else functions[0])
            break

    if symbol_match is not None:
        target_path, symbol = symbol_match
    elif first_parseable is not None:
        target_path, _ = first_parseable
        symbol = ""
    else:
        raise ProjectContextUnavailable("no parseable canonical Project Python file")

    if not is_within(target_path, root):
        raise RuntimeError("PROJECT_CONTEXT_TARGET_ESCAPED_ACTIVE_ROOT")
    relative = target_path.relative_to(root)
    return ProjectCommandContext(
        root=root,
        target=relative.as_posix(),
        module=_module_text(relative),
        symbol=symbol,
        project_name=root.name,
    )


def require_project_symbol(context: ProjectCommandContext) -> str:
    """Return a Project-owned function symbol or fail without Tool fallback."""
    if context.symbol:
        return context.symbol
    raise ProjectContextUnavailable("no callable Project symbol for targeted command")
