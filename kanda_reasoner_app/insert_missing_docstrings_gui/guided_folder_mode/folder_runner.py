
"""Folder-scoped Safe Mode runner primitives for Tab 3 docstrings."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from .models import FolderQueueItem, GuidedFolderSession


@dataclass(frozen=True)
class FolderPreflight:
    """Summarize missing-docstring targets for one folder only."""

    folder_relative_path: str
    python_files: tuple[str, ...]
    files_parsed: int
    files_with_syntax_errors: tuple[str, ...]
    missing_module_docstrings: int
    missing_class_docstrings: int
    missing_function_docstrings: int
    missing_method_docstrings: int

    @property
    def total_missing_docstrings(self) -> int:
        """Return the total number of missing docstrings found in this folder."""
        return (
            self.missing_module_docstrings
            + self.missing_class_docstrings
            + self.missing_function_docstrings
            + self.missing_method_docstrings
        )

    @property
    def is_clean_to_generate(self) -> bool:
        """Return True when all files parsed successfully."""
        return not self.files_with_syntax_errors


@dataclass(frozen=True)
class FolderRunSettings:
    """Describe generation settings for one Safe Mode folder run."""

    include_module: bool = True
    include_classes: bool = True
    include_functions: bool = True
    include_init: bool = False
    include_private: bool = False
    ai_enabled: bool = True
    fallback_enabled: bool = True
    require_ai_success: bool = False
    workers: int = 1
    model: str = ""
    report_filename: str = ".docstring_safe_mode_report.jsonl"

    def to_backend_options(self) -> dict[str, Any]:
        """Return options suitable for a folder-scoped backend adapter."""
        return {
            "include_module": self.include_module,
            "include_classes": self.include_classes,
            "include_functions": self.include_functions,
            "include_init": self.include_init,
            "include_private": self.include_private,
            "ai_enabled": self.ai_enabled,
            "fallback_enabled": self.fallback_enabled,
            "require_ai_success": self.require_ai_success,
            "workers": self.workers,
            "model": self.model,
            "report_filename": self.report_filename,
        }


@dataclass(frozen=True)
class FolderRunPlan:
    """Bind one queue item to one backend-safe folder-scoped run."""

    project_root: str
    folder_relative_path: str
    python_files: tuple[str, ...]
    report_path: str
    settings: FolderRunSettings = field(default_factory=FolderRunSettings)

    def absolute_python_files(self) -> tuple[Path, ...]:
        """Return absolute source paths for this folder run."""
        root = Path(self.project_root)
        return tuple(root / file_name for file_name in self.python_files)


@dataclass(frozen=True)
class FolderRunResult:
    """Store the result of executing a Safe Mode folder-scoped backend run."""

    success: bool
    folder_relative_path: str
    processed_files: tuple[str, ...]
    report_path: str
    message: str = ""
    row_count: int = 0
    error: str = ""


FolderBackend = Callable[[FolderRunPlan], FolderRunResult]


def _is_overload_stub(node: ast.AST) -> bool:
    """Return True when a function node is an overload stub."""
    decorators = getattr(node, "decorator_list", [])
    for decorator in decorators:
        if isinstance(decorator, ast.Name) and decorator.id == "overload":
            return True
        if isinstance(decorator, ast.Attribute) and decorator.attr == "overload":
            return True
    return False


def _parent_map(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    """Return a mapping from child AST nodes to their parent nodes."""
    parents: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    return parents


def _is_direct_class_or_module_member(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> bool:
    """Return True for top-level functions/classes and class methods."""
    parent = parents.get(node)
    return isinstance(parent, (ast.Module, ast.ClassDef))


def _has_docstring(node: ast.AST) -> bool:
    """Return True when an AST node has a real Python docstring."""
    return ast.get_docstring(node) is not None


def _target_visible(name: str, include_private: bool) -> bool:
    """Return True when a target name is allowed by the private-symbol setting."""
    if include_private:
        return True
    if name.startswith("__") and name.endswith("__"):
        return True
    return not name.startswith("_")


def preflight_folder(
    project_root: str | Path,
    item: FolderQueueItem,
    settings: FolderRunSettings | None = None,
) -> FolderPreflight:
    """Inspect only one queued folder and summarize missing docstrings."""
    root = Path(project_root).resolve()
    active_settings = settings or FolderRunSettings()

    parsed_count = 0
    syntax_errors: list[str] = []
    missing_modules = 0
    missing_classes = 0
    missing_functions = 0
    missing_methods = 0

    for relative_file in item.python_files:
        source_path = root / relative_file
        try:
            source_text = source_path.read_text(encoding="utf-8")
            tree = ast.parse(source_text, filename=str(source_path))
        except SyntaxError:
            syntax_errors.append(relative_file)
            continue

        parsed_count += 1

        if active_settings.include_module and not _has_docstring(tree):
            missing_modules += 1

        parents = _parent_map(tree)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not _is_direct_class_or_module_member(node, parents):
                    continue
                if not _target_visible(node.name, active_settings.include_private):
                    continue
                if active_settings.include_classes and not _has_docstring(node):
                    missing_classes += 1
                continue

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if _is_overload_stub(node):
                    continue
                if not _is_direct_class_or_module_member(node, parents):
                    continue
                if node.name == "__init__" and not active_settings.include_init:
                    continue
                if not _target_visible(node.name, active_settings.include_private):
                    continue
                if not active_settings.include_functions:
                    continue

                parent = parents.get(node)
                if isinstance(parent, ast.ClassDef):
                    if not _has_docstring(node):
                        missing_methods += 1
                elif not _has_docstring(node):
                    missing_functions += 1

    return FolderPreflight(
        folder_relative_path=item.relative_path,
        python_files=item.python_files,
        files_parsed=parsed_count,
        files_with_syntax_errors=tuple(sorted(syntax_errors)),
        missing_module_docstrings=missing_modules,
        missing_class_docstrings=missing_classes,
        missing_function_docstrings=missing_functions,
        missing_method_docstrings=missing_methods,
    )


def create_folder_run_plan(
    session: GuidedFolderSession,
    index: int | None = None,
    settings: FolderRunSettings | None = None,
) -> FolderRunPlan:
    """Create a backend-safe run plan for one queued folder."""
    selected_index = session.current_index if index is None else index
    if selected_index < 0 or selected_index >= len(session.folder_queue):
        raise IndexError("Folder queue index is out of range.")

    item = session.folder_queue[selected_index]
    if item.is_resolved():
        raise ValueError("Resolved folders cannot be run again without explicit reset.")
    if item.is_blocked():
        raise ValueError("Blocked folders must be corrected or skipped before running.")

    active_settings = settings or FolderRunSettings()
    root = Path(session.project_root).resolve()
    folder_name = item.relative_path.replace("/", "_").replace("\\", "_")
    if folder_name in {"", "."}:
        folder_name = "project_root"
    report_path = root / f".docstring_safe_mode_{folder_name}.jsonl"

    return FolderRunPlan(
        project_root=str(root),
        folder_relative_path=item.relative_path,
        python_files=item.python_files,
        report_path=str(report_path),
        settings=active_settings,
    )


def validate_folder_run_plan(plan: FolderRunPlan) -> None:
    """Raise ValueError when a run plan points outside its selected folder."""
    root = Path(plan.project_root).resolve()
    folder_root = root if plan.folder_relative_path == "." else root / plan.folder_relative_path

    for relative_file in plan.python_files:
        absolute_file = (root / relative_file).resolve()
        if not absolute_file.exists():
            raise ValueError(f"Planned Python file does not exist: {relative_file}")
        try:
            absolute_file.relative_to(folder_root.resolve())
        except ValueError as exc:
            raise ValueError(
                f"Planned Python file is outside the selected folder: {relative_file}"
            ) from exc


def run_folder_with_backend(plan: FolderRunPlan, backend: FolderBackend) -> FolderRunResult:
    """Execute one folder run through an injected backend adapter."""
    validate_folder_run_plan(plan)
    result = backend(plan)

    allowed = set(plan.python_files)
    processed = set(result.processed_files)
    outside = sorted(processed - allowed)
    if outside:
        raise ValueError(
            "Backend processed files outside the selected folder: " + ", ".join(outside)
        )

    return result
