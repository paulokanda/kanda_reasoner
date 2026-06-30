# project-path: kanda_reasoner_app/source_hygiene/shadow_audit.py
"""Read-only audit for public symbol shadowing and unsafe facades."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .schemas import SourceHygieneFinding, SourceHygieneReport

DEFAULT_SHADOW_AUDIT_SUFFIXES = frozenset({".py", ".pyi"})
DEFAULT_SHADOW_SKIP_DIR_NAMES = frozenset(
    {
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
        "htmlcov",
        "site-packages",
        "venv",
    }
)

__all__ = [
    "DEFAULT_SHADOW_AUDIT_SUFFIXES",
    "DEFAULT_SHADOW_SKIP_DIR_NAMES",
    "ShadowAuditFileSummary",
    "audit_project_for_shadow_conflicts",
    "audit_python_file_for_shadow_conflicts",
    "iter_shadow_audit_files",
]


@dataclass(frozen=True)
class ShadowAuditFileSummary:
    """Read-only public surface summary for one Python file."""

    path: str
    public_symbols: tuple[str, ...]
    explicit_all: tuple[str, ...]
    findings: tuple[SourceHygieneFinding, ...]


def iter_shadow_audit_files(
    project_root: str | Path,
    suffixes: Iterable[str] | None = None,
) -> list[Path]:
    """Return active Python files considered by the shadow conflict audit."""
    root = Path(project_root).resolve()
    allowed = _normalize_suffixes(suffixes)
    files: list[Path] = []
    for candidate in root.rglob("*"):
        if not candidate.is_file():
            continue
        if candidate.suffix.lower() not in allowed:
            continue
        if _is_in_skipped_dir(candidate, root):
            continue
        files.append(candidate)
    return sorted(files, key=lambda item: str(item).lower())


def audit_python_file_for_shadow_conflicts(
    path: str | Path,
    project_root: str | Path | None = None,
) -> ShadowAuditFileSummary:
    """Audit one Python file for facade and public-surface conflicts."""
    file_path = Path(path).resolve()
    root = Path(project_root).resolve() if project_root is not None else None
    display_path = _display_path(file_path, root)

    try:
        text = file_path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return ShadowAuditFileSummary(
            path=display_path,
            public_symbols=(),
            explicit_all=(),
            findings=(
                SourceHygieneFinding(
                    code="SHADOW_AUDIT_READ_ERROR",
                    path=display_path,
                    message="Could not read file during shadow audit: " + str(exc),
                    severity="error",
                    confidence="high",
                    suggested_action="Inspect file permissions or path validity.",
                ),
            ),
        )

    try:
        module = ast.parse(text, filename=str(file_path))
    except SyntaxError as exc:
        return ShadowAuditFileSummary(
            path=display_path,
            public_symbols=(),
            explicit_all=(),
            findings=(
                SourceHygieneFinding(
                    code="SHADOW_AUDIT_PARSE_ERROR",
                    path=display_path,
                    line=exc.lineno,
                    message="Could not parse file during shadow audit: " + str(exc),
                    severity="error",
                    confidence="high",
                    suggested_action="Repair syntax before public-surface auditing.",
                ),
            ),
        )

    public_symbols = _collect_public_symbols(module)
    explicit_all, all_dynamic = _collect_explicit_all(module)
    findings: list[SourceHygieneFinding] = []

    if all_dynamic:
        findings.append(
            SourceHygieneFinding(
                code="DYNAMIC_ALL_EXPORT",
                path=display_path,
                message="Module assigns __all__ dynamically or with non-string values.",
                severity="warning",
                confidence="high",
                suggested_action="Replace dynamic __all__ with an explicit string list when safe.",
            )
        )

    for exported_name in explicit_all:
        if exported_name not in public_symbols:
            findings.append(
                SourceHygieneFinding(
                    code="UNBOUND_ALL_EXPORT",
                    path=display_path,
                    message="__all__ exports a name that is not bound at module top level: "
                    + exported_name,
                    severity="warning",
                    confidence="high",
                    evidence={"exported_name": exported_name},
                    suggested_action="Remove the stale export or bind it from the canonical owner.",
                )
            )

    is_facade = file_path.name == "__init__.py"
    if is_facade:
        findings.extend(_audit_init_facade(module, display_path, explicit_all))

    return ShadowAuditFileSummary(
        path=display_path,
        public_symbols=tuple(sorted(public_symbols)),
        explicit_all=tuple(explicit_all),
        findings=tuple(findings),
    )


def audit_project_for_shadow_conflicts(
    project_root: str | Path,
    suffixes: Iterable[str] | None = None,
    max_files: int | None = None,
) -> SourceHygieneReport:
    """Build a read-only report for shadow conflict and unsafe facade risks."""
    root = Path(project_root).resolve()
    files = iter_shadow_audit_files(root, suffixes=suffixes)
    if max_files is not None:
        files = files[: max(0, int(max_files))]

    summaries = [audit_python_file_for_shadow_conflicts(path, root) for path in files]
    findings: list[SourceHygieneFinding] = []
    symbol_owners: dict[str, list[str]] = {}

    for summary in summaries:
        findings.extend(summary.findings)
        for symbol in summary.public_symbols:
            symbol_owners.setdefault(symbol, []).append(summary.path)

    for symbol, owners in sorted(symbol_owners.items()):
        active_owners = sorted(set(owners))
        if len(active_owners) < 2:
            continue
        findings.append(
            SourceHygieneFinding(
                code="DUPLICATE_PUBLIC_SYMBOL",
                path="<project>",
                message="Public symbol appears in multiple active modules: " + symbol,
                severity="warning",
                confidence="medium",
                evidence={"symbol": symbol, "owners": active_owners},
                suggested_action="Decide the canonical owner before changing this symbol.",
            )
        )

    summary_text = (
        "Shadow conflict audit completed. "
        + "files_scanned="
        + str(len(files))
        + "; findings="
        + str(len(findings))
        + "."
    )
    return SourceHygieneReport(
        project_root=str(root),
        report_type="shadow_conflict_audit",
        summary=summary_text,
        findings=tuple(findings),
        input_sources=("project_root",),
    )


def _audit_init_facade(
    module: ast.Module,
    display_path: str,
    explicit_all: tuple[str, ...],
) -> list[SourceHygieneFinding]:
    """Support audit init facade behavior.
    
    Parameters
    ----------
    module : ast.Module
        The module value.
    display_path : str
        The display path value.
    explicit_all : tuple[str, ...]
        The explicit all value.
    
    Returns
    -------
    list[SourceHygieneFinding]
        The list of values.
    """
    
    findings: list[SourceHygieneFinding] = []
    has_public_import = False

    for node in module.body:
        if isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" for alias in node.names):
                findings.append(
                    SourceHygieneFinding(
                        code="WILDCARD_IMPORT_IN_FACADE",
                        path=display_path,
                        line=getattr(node, "lineno", None),
                        message="Package facade uses a wildcard import.",
                        severity="warning",
                        confidence="high",
                        suggested_action="Replace wildcard import with explicit imports.",
                    )
                )
            if not _is_type_checking_import(node):
                has_public_import = True
        elif isinstance(node, ast.Import):
            if not _is_type_checking_import(node):
                has_public_import = True
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            findings.append(
                SourceHygieneFinding(
                    code="BEHAVIOR_DEFINED_IN_FACADE",
                    path=display_path,
                    line=getattr(node, "lineno", None),
                    message="Package __init__.py defines runtime behavior: " + node.name,
                    severity="warning",
                    confidence="high",
                    evidence={"symbol": node.name},
                    suggested_action="Move behavior to an owner module and re-export if needed.",
                )
            )
        elif _is_runtime_statement(node):
            findings.append(
                SourceHygieneFinding(
                    code="RUNTIME_LOGIC_IN_FACADE",
                    path=display_path,
                    line=getattr(node, "lineno", None),
                    message="Package __init__.py contains runtime logic.",
                    severity="warning",
                    confidence="medium",
                    suggested_action="Keep package facades import-only and side-effect free.",
                )
            )

    if has_public_import and not explicit_all:
        findings.append(
            SourceHygieneFinding(
                code="FACADE_WITHOUT_ALL",
                path=display_path,
                message="Package facade imports public names but does not define __all__.",
                severity="warning",
                confidence="medium",
                suggested_action="Declare the intended public facade exports explicitly.",
            )
        )
    return findings


def _collect_public_symbols(module: ast.Module) -> set[str]:
    """Support collect public symbols behavior.
    
    Parameters
    ----------
    module : ast.Module
        The module value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    symbols: set[str] = set()
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                symbols.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                symbols.update(_public_names_from_target(target))
        elif isinstance(node, ast.AnnAssign):
            symbols.update(_public_names_from_target(node.target))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                if not name.startswith("_"):
                    symbols.add(name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                name = alias.asname or alias.name
                if not name.startswith("_"):
                    symbols.add(name)
    symbols.discard("__all__")
    return symbols


def _collect_explicit_all(module: ast.Module) -> tuple[tuple[str, ...], bool]:
    """Support collect explicit all behavior.
    
    Parameters
    ----------
    module : ast.Module
        The module value.
    
    Returns
    -------
    tuple[tuple[str, ...], bool]
        The tuple of values.
    """
    
    names: list[str] = []
    found_dynamic = False
    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            continue
        extracted = _literal_string_sequence(node.value)
        if extracted is None:
            found_dynamic = True
        else:
            names.extend(extracted)
    return tuple(names), found_dynamic


def _literal_string_sequence(node: ast.AST) -> tuple[str, ...] | None:
    """Support literal string sequence behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    tuple[str, ...] | None
        The tuple of values.
    """
    
    if not isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return None
    values: list[str] = []
    for item in node.elts:
        if not isinstance(item, ast.Constant) or not isinstance(item.value, str):
            return None
        values.append(item.value)
    return tuple(values)


def _public_names_from_target(target: ast.AST) -> set[str]:
    """Support public names from target behavior.
    
    Parameters
    ----------
    target : ast.AST
        The target value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    names: set[str] = set()
    if isinstance(target, ast.Name):
        if not target.id.startswith("_"):
            names.add(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for item in target.elts:
            names.update(_public_names_from_target(item))
    return names


def _is_runtime_statement(node: ast.AST) -> bool:
    """Support is runtime statement behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if isinstance(node, ast.Expr):
        return not _is_module_docstring(node)
    if isinstance(node, ast.Assign):
        if any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets):
            return False
        return True
    if isinstance(node, ast.AnnAssign):
        return not (isinstance(node.target, ast.Name) and node.target.id == "__all__")
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return False
    return isinstance(node, (ast.For, ast.While, ast.If, ast.Try, ast.With, ast.Call))


def _is_module_docstring(node: ast.AST) -> bool:
    """Support is module docstring behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    )


def _is_type_checking_import(node: ast.AST) -> bool:
    """Support is type checking import behavior.
    
    Parameters
    ----------
    node : ast.AST
        The syntax tree node.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return False


def _normalize_suffixes(suffixes: Iterable[str] | None) -> set[str]:
    """Support normalize suffixes behavior.
    
    Parameters
    ----------
    suffixes : Iterable[str] | None
        The suffixes value.
    
    Returns
    -------
    set[str]
        The set result.
    """
    
    if suffixes is None:
        return set(DEFAULT_SHADOW_AUDIT_SUFFIXES)
    normalized: set[str] = set()
    for suffix in suffixes:
        value = str(suffix).strip().lower()
        if not value:
            continue
        if not value.startswith("."):
            value = "." + value
        normalized.add(value)
    return normalized


def _is_in_skipped_dir(path: Path, root: Path) -> bool:
    """Support is in skipped dir behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path
        The root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    try:
        parts = path.relative_to(root).parts[:-1]
    except ValueError:
        parts = path.parts[:-1]
    return any(part in DEFAULT_SHADOW_SKIP_DIR_NAMES for part in parts)


def _display_path(path: Path, root: Path | None) -> str:
    """Support display path behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    root : Path | None
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    if root is None:
        return str(path)
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path)
