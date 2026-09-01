# project-path: kanda_reasoner_app/reasoner_symbol_atlas/module_scanner.py
"""Read-only Python module scanner for Project Symbol Atlas."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .schemas import ProjectModuleRecord, ProjectSymbolAtlasReport

__all__ = [
    "ProjectSymbolAtlasModuleScanOptions",
    "build_reasoner_symbol_atlas_module_report",
    "collect_reasoner_symbol_atlas_modules",
    "reasoner_symbol_atlas_module_name_for_path",
]

_DEFAULT_EXCLUDED_DIR_NAMES = (
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "env",
    "node_modules",
    "site-packages",
    "snippets",
    "DEVELOPER_TOOLS_older",
    "legacy_cleanup",
    "oldies_deprecated",
    "older_deprecated",
    "venv",
)

_DEFAULT_EXCLUDED_PATH_PARTS = (
    "_bundle_temp",
    "_generated",
    "_trash",
    "deprecated",
    "oldies",
    "older",
    "scratch",
)


@dataclass(frozen=True)
class ProjectSymbolAtlasModuleScanOptions:
    """Options for read-only module scanning."""

    include_tests: bool = True
    include_workbench: bool = False
    excluded_dir_names: tuple[str, ...] = field(
        default_factory=lambda: _DEFAULT_EXCLUDED_DIR_NAMES
    )
    excluded_path_parts: tuple[str, ...] = field(
        default_factory=lambda: _DEFAULT_EXCLUDED_PATH_PARTS
    )

    def normalized_excluded_dir_names(self) -> set[str]:
        """Return normalized directory names to skip."""
        return {str(name).strip().lower() for name in self.excluded_dir_names if name}

    def normalized_excluded_path_parts(self) -> set[str]:
        """Return normalized path parts to skip."""
        return {str(part).strip().lower() for part in self.excluded_path_parts if part}


def _coerce_project_root(project_root: str | Path) -> Path:
    """Support coerce project root behavior.
    
    Parameters
    ----------
    project_root : str | Path
        The project root path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    root = Path(project_root).resolve()
    if not root.exists():
        raise FileNotFoundError("Project root does not exist: " + str(project_root))
    if not root.is_dir():
        raise NotADirectoryError("Project root is not a directory: " + str(project_root))
    return root


def _safe_relative_path(project_root: Path, file_path: Path) -> Path:
    """Support safe relative path behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    file_path : Path
        The file path.
    
    Returns
    -------
    Path
        The resolved path.
    """
    
    try:
        return file_path.resolve().relative_to(project_root)
    except ValueError:
        return Path(file_path.name)


def _is_test_path(relative_path: Path) -> bool:
    """Support is test path behavior.
    
    Parameters
    ----------
    relative_path : Path
        The relative path value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    parts = {part.lower() for part in relative_path.parts}
    name = relative_path.name.lower()
    return "tests" in parts or name.startswith("test_") or name.endswith("_test.py")


def _is_workbench_path(relative_path: Path) -> bool:
    """Support is workbench path behavior.
    
    Parameters
    ----------
    relative_path : Path
        The relative path value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return any(part.lower() == "workbench" for part in relative_path.parts)


def _is_generated_or_stale_candidate(relative_path: Path) -> bool:
    """Support is generated or stale candidate behavior.
    
    Parameters
    ----------
    relative_path : Path
        The relative path value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    lowered_parts = [part.lower() for part in relative_path.parts]
    lowered_name = relative_path.name.lower()
    stale_tokens = (
        "archive",
        "backup",
        "deprecated",
        "generated",
        "legacy",
        "old",
        "stale",
        "tmp",
    )
    if any(part.startswith("_tmp") for part in lowered_parts):
        return True
    if any(token in lowered_name for token in stale_tokens):
        return True
    return any(part in {"archive", "backups", "legacy", "old"} for part in lowered_parts)


def _is_facade_candidate(relative_path: Path) -> bool:
    """Support is facade candidate behavior.
    
    Parameters
    ----------
    relative_path : Path
        The relative path value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    name = relative_path.name.lower()
    return name == "__init__.py" or "facade" in name or name.endswith("_shell.py")


def _is_helper_candidate(relative_path: Path) -> bool:
    """Support is helper candidate behavior.
    
    Parameters
    ----------
    relative_path : Path
        The relative path value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    name = relative_path.name.lower()
    helper_tokens = ("helper", "helpers", "util", "utils", "common")
    return any(token in name for token in helper_tokens)


def _should_skip_path(
    relative_path: Path,
    options: ProjectSymbolAtlasModuleScanOptions,
) -> bool:
    """Support should skip path behavior.
    
    Parameters
    ----------
    relative_path : Path
        The relative path value.
    options : ProjectSymbolAtlasModuleScanOptions
        The option values.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    excluded_dir_names = options.normalized_excluded_dir_names()
    excluded_path_parts = options.normalized_excluded_path_parts()
    parts = [part.lower() for part in relative_path.parts]
    if any(part in excluded_dir_names for part in parts[:-1]):
        return True
    if any(part in excluded_path_parts for part in parts):
        return True
    if any(part.startswith("_tmp") or part.startswith("tmp_") for part in parts):
        return True
    noisy_markers = ("backup", "deprecated", "oldies", "older", "scratch", "copy")
    if any(any(marker in part for marker in noisy_markers) for part in parts):
        return True
    if not options.include_tests and _is_test_path(relative_path):
        return True
    if not options.include_workbench and _is_workbench_path(relative_path):
        return True
    return False


def _iter_python_files(
    project_root: Path,
    options: ProjectSymbolAtlasModuleScanOptions,
) -> Iterable[Path]:
    """Support iter python files behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    options : ProjectSymbolAtlasModuleScanOptions
        The option values.
    
    Returns
    -------
    Iterable[Path]
        The sequence of values.
    """
    
    for file_path in project_root.rglob("*.py"):
        if not file_path.is_file():
            continue
        relative_path = _safe_relative_path(project_root, file_path)
        if _should_skip_path(relative_path, options):
            continue
        yield file_path


def _read_line_count(file_path: Path) -> tuple[int, tuple[str, ...]]:
    """Support read line count behavior.
    
    Parameters
    ----------
    file_path : Path
        The file path.
    
    Returns
    -------
    tuple[int, tuple[str, ...]]
        The tuple of values.
    """
    
    evidence: list[str] = []
    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        evidence.append("read_error: " + exc.__class__.__name__)
        return 0, tuple(evidence)
    if not text:
        return 0, tuple(evidence)
    line_count = text.count("\n")
    if not text.endswith("\n"):
        line_count += 1
    return line_count, tuple(evidence)


def reasoner_symbol_atlas_module_name_for_path(
    project_root: str | Path,
    file_path: str | Path,
) -> str:
    """Return a dotted module name for a Python file under a project root."""
    root = Path(project_root).resolve()
    path = Path(file_path).resolve()
    relative_path = _safe_relative_path(root, path)
    if relative_path.suffix.lower() != ".py":
        raise ValueError("Expected a Python file path: " + str(file_path))
    parts = list(relative_path.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else "__init__"


def _module_record_and_source(
    project_root: Path,
    file_path: Path,
) -> tuple[ProjectModuleRecord, str, tuple[str, ...]]:
    """Build one module record while retaining its already-read source text."""
    relative_path = _safe_relative_path(project_root, file_path)
    module_parts = list(relative_path.with_suffix("").parts)
    if module_parts and module_parts[-1] == "__init__":
        module_parts = module_parts[:-1]
    module_name = ".".join(module_parts) if module_parts else "__init__"
    read_evidence: list[str] = []
    try:
        source_text = file_path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        source_text = ""
        read_evidence.append("read_error: " + exc.__class__.__name__)
    line_count = source_text.count("\n")
    if source_text and not source_text.endswith("\n"):
        line_count += 1
    is_test_file = _is_test_path(relative_path)
    is_generated_or_stale = _is_generated_or_stale_candidate(relative_path)
    is_package_init = relative_path.name == "__init__.py"
    evidence = [
        "module_scan: read_only",
        "relative_path: " + str(relative_path),
        "is_package_init: " + str(is_package_init).lower(),
        "is_test_file: " + str(is_test_file).lower(),
        "facade_candidate: " + str(_is_facade_candidate(relative_path)).lower(),
        "helper_candidate: " + str(_is_helper_candidate(relative_path)).lower(),
        "generated_or_stale_candidate: " + str(is_generated_or_stale).lower(),
    ]
    evidence.extend(read_evidence)
    owner_role = "unknown"
    if is_test_file:
        owner_role = "test_only"
    elif is_generated_or_stale:
        owner_role = "generated_or_stale"
    record = ProjectModuleRecord(
        module=module_name,
        path=str(relative_path),
        line_count=line_count,
        is_package_init=is_package_init,
        is_test_file=is_test_file,
        owner_role=owner_role,
        evidence=tuple(evidence),
    )
    return record, source_text, tuple(read_evidence)


def _module_record_for_file(
    project_root: Path,
    file_path: Path,
) -> ProjectModuleRecord:
    """Build one module record without importing project code."""
    record, _source_text, _read_evidence = _module_record_and_source(
        project_root, file_path
    )
    return record


def _collect_reasoner_symbol_atlas_modules_with_sources(
    project_root: Path,
    options: ProjectSymbolAtlasModuleScanOptions,
) -> tuple[tuple[ProjectModuleRecord, str, tuple[str, ...]], ...]:
    """Collect module records plus source text for an internal single-pass analysis."""
    rows = [
        _module_record_and_source(project_root, path)
        for path in _iter_python_files(project_root, options)
    ]
    rows.sort(key=lambda item: (item[0].path, item[0].module))
    return tuple(rows)


def collect_reasoner_symbol_atlas_modules(
    project_root: str | Path,
    options: ProjectSymbolAtlasModuleScanOptions | None = None,
) -> tuple[ProjectModuleRecord, ...]:
    """Collect Python module records without importing or editing project code."""
    root = _coerce_project_root(project_root)
    scan_options = options or ProjectSymbolAtlasModuleScanOptions()
    records = [_module_record_for_file(root, path) for path in _iter_python_files(root, scan_options)]
    records.sort(key=lambda record: (record.path, record.module))
    return tuple(records)


def build_reasoner_symbol_atlas_module_report(
    project_root: str | Path,
    options: ProjectSymbolAtlasModuleScanOptions | None = None,
) -> ProjectSymbolAtlasReport:
    """Build a Project Symbol Atlas module-scan report."""
    root = _coerce_project_root(project_root)
    modules = collect_reasoner_symbol_atlas_modules(root, options=options)
    return ProjectSymbolAtlasReport(
        project_root=str(root),
        report_type="reasoner_symbol_atlas",
        summary="Read-only Python module scan completed. modules=" + str(len(modules)) + ".",
        modules=modules,
        input_sources=("reasoner_symbol_atlas.module_scanner",),
    )
