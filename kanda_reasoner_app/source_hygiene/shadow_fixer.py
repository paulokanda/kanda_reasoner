# project-path: kanda_reasoner_app/source_hygiene/shadow_fixer.py
"""Safe mechanical facade fixes for source hygiene."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.project_source_proposal_boundary import (
    PROJECT_REPAIR_PROPOSAL_ONLY_MARKER,
)

from ._active_scope import _build_active_source_scope
from .schemas import SourceHygieneFinding, SourceHygieneReport

__all__ = [
    "FacadeFixResult",
    "apply_safe_package_marker_fix",
    "build_safe_facade_fix_plan",
    "iter_empty_init_files",
    "plan_safe_package_marker_fix",
]

_SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".project_reference",
        "_project_reference",
        "project_freeze_ledger",
        "__pycache__",
        "build",
        "dist",
        "htmlcov",
        "node_modules",
        "venv",
        ".venv",
    }
)


@dataclass(frozen=True)
class FacadeFixResult:
    """Result for one safe mechanical facade fix attempt."""

    path: str
    action: str
    changed: bool
    dry_run: bool
    backup_path: str = ""
    error: str = ""
    proposal_only: bool = False

    def to_finding(self) -> SourceHygieneFinding:
        """Represent this fix result as a source hygiene finding."""
        severity = "error" if self.error else "info"
        code = "SAFE_FACADE_FIX_FAILED" if self.error else "SAFE_FACADE_FIX_RESULT"
        message = self.error or self.action
        return SourceHygieneFinding(
            code=code,
            path=self.path,
            severity=severity,
            confidence="high",
            message=message,
            evidence={
                "changed": self.changed,
                "dry_run": self.dry_run,
                "backup_path": self.backup_path,
                "proposal_only": self.proposal_only,
            },
            suggested_action="Review the fix result and validate the project gates.",
        )


def iter_empty_init_files(project_root: str | Path) -> tuple[Path, ...]:
    """Return empty package marker candidates under the project root."""
    root = Path(project_root).resolve()
    if not root.exists() or not root.is_dir():
        return ()
    scope = _build_active_source_scope(root)
    results: list[Path] = []
    for path in root.rglob("__init__.py"):
        if not scope.includes(path, exclude_tests=True):
            continue
        if _is_empty_init_file(path):
            results.append(path)
    return tuple(sorted(results))


def plan_safe_package_marker_fix(
    path: str | Path,
    project_root: str | Path,
) -> SourceHygieneFinding | None:
    """Return a safe package-marker fix finding for one file when applicable."""
    root = Path(project_root).resolve()
    candidate = Path(path).resolve()
    if not _is_inside(candidate, root):
        return None
    if candidate.name != "__init__.py":
        return None
    if not _is_empty_init_file(candidate):
        return None
    relative = candidate.relative_to(root).as_posix()
    package_name = candidate.parent.name or "package"
    return SourceHygieneFinding(
        code="EMPTY_INIT_PACKAGE_MARKER_FIX_AVAILABLE",
        path=relative,
        severity="info",
        confidence="high",
        message="Empty __init__.py can be converted to an explicit package marker.",
        evidence={
            "fix_type": "package_marker",
            "package_name": package_name,
        },
        suggested_action=(
            "Add a package docstring and __all__ = [] without changing imports or "
            "runtime behavior."
        ),
    )


def build_safe_facade_fix_plan(project_root: str | Path) -> SourceHygieneReport:
    """Build a read-only plan for safe mechanical facade fixes."""
    root = Path(project_root).resolve()
    findings = []
    for path in iter_empty_init_files(root):
        finding = plan_safe_package_marker_fix(path, root)
        if finding is not None:
            findings.append(finding)
    summary = "Safe facade fix candidates: " + str(len(findings))
    return SourceHygieneReport(
        project_root=str(root),
        report_type="facade_fix_plan",
        summary=summary,
        findings=tuple(findings),
        input_sources=("shadow_conflict_audit", "safe_facade_fix_scan"),
    )


def apply_safe_package_marker_fix(
    path: str | Path,
    project_root: str | Path,
    *,
    dry_run: bool = True,
    backup_dir: str | Path | None = None,
) -> FacadeFixResult:
    """Return a package-marker proposal without mutating Project source."""
    del backup_dir
    root = Path(project_root).resolve()
    candidate = Path(path).resolve()
    if not _is_inside(candidate, root):
        return _failed(
            candidate,
            dry_run,
            "Refusing to edit a file outside the project root.",
        )
    if candidate.name != "__init__.py":
        return _failed(
            candidate,
            dry_run,
            "Only __init__.py package marker files are supported.",
        )
    if not _is_empty_init_file(candidate):
        return _failed(
            candidate,
            dry_run,
            "File is not empty; no mechanical package-marker fix was applied.",
        )
    new_text = _package_marker_text(candidate)
    compile(new_text, str(candidate), "exec")
    if dry_run:
        return FacadeFixResult(
            path=str(candidate),
            action="Would propose explicit package marker and __all__ = [].",
            changed=False,
            dry_run=True,
            proposal_only=True,
        )
    return FacadeFixResult(
        path=str(candidate),
        action=(
            PROJECT_REPAIR_PROPOSAL_ONLY_MARKER
            + ":SAFE_PACKAGE_MARKER"
        ),
        changed=False,
        dry_run=False,
        proposal_only=True,
    )


def _is_skipped(path: Path, root: Path) -> bool:
    """Return whether a path is outside active production facade scope."""
    scope = _build_active_source_scope(root)
    return not scope.includes(path, exclude_tests=True)


def _is_empty_init_file(path: Path) -> bool:
    """Support is empty init file behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    if not path.exists() or not path.is_file():
        return False
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return data.strip() == b""


def _is_inside(path: Path, root: Path) -> bool:
    """Support is inside behavior.
    
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
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _package_marker_text(path: Path) -> str:
    """Support package marker text behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    package_name = path.parent.name or "package"
    return '\"\"\"Package marker for ' + package_name + '.\"\"\"\n\n__all__ = []\n'


def _failed(path: Path, dry_run: bool, error: str) -> FacadeFixResult:
    """Support failed behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    dry_run : bool
        The dry run value.
    error : str
        The error value.
    
    Returns
    -------
    FacadeFixResult
        The facade fix result result.
    """
    
    return FacadeFixResult(
        path=str(path),
        action="No change applied.",
        changed=False,
        dry_run=dry_run,
        error=error,
    )
