# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/candidate_discovery.py
"""Candidate discovery for the Architecture Review Large File Refactor Planner."""
from __future__ import annotations

import ast
from pathlib import Path
from typing import Iterable, Sequence

from .models import LargeFileCandidate, MAX_PHYSICAL_LINES, SCHEMA_VERSION

_EXCLUDED_PARTS = {
    "__pycache__",
    ".git",
    ".hg",
    ".mypy_cache",
    ".pytest_cache",
    "build",
    "dist",
    "htmlcov",
}
_EXCLUDED_FRAGMENTS = (
    "_delete_after_daily_work",
    "show_project_to_AI",
    "first_prompt_files",
    "project_freeze_after_update",
    "project_error_memory",
    ".project_reference",
    "_project_reference",
    "large_file_refactor_preview",
    "handoff",
    "freeze_hint_intake",
)
_GENERATED_SUFFIXES = (
    "_FREEZE_HINT.json",
    ".zip",
    ".pyc",
)


def discover_candidates(
    active_project_root: str | Path,
    *,
    threshold: int = MAX_PHYSICAL_LINES,
    audit_targets: Sequence[object] | None = None,
    scan_fallback: bool = True,
) -> list[LargeFileCandidate]:
    """Return planner candidates from audit state, then fallback scan."""
    root = Path(active_project_root).expanduser().resolve()
    if not root.exists():
        return []
    candidates = _from_audit_targets(root, audit_targets or (), threshold)
    if candidates:
        return _dedupe_candidates(candidates)
    if not scan_fallback:
        return []
    return _dedupe_candidates(_scan_project_root(root, threshold))


def count_physical_lines(path: Path) -> int:
    """Count physical file lines with tolerant decoding."""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            return sum(1 for _line in handle)
    except OSError:
        return 0


def _from_audit_targets(
    root: Path,
    audit_targets: Iterable[object],
    threshold: int,
) -> list[LargeFileCandidate]:
    """Build candidates from the existing AST audit target queue."""
    candidates: list[LargeFileCandidate] = []
    for target in audit_targets:
        target_path_text = str(getattr(target, "path", "") or "").strip()
        if not target_path_text:
            continue
        path = Path(target_path_text)
        if not path.is_absolute():
            path = root / path
        path = path.resolve()
        line_count = int(getattr(target, "line_count", 0) or 0)
        if line_count <= 0:
            line_count = count_physical_lines(path)
        candidate = _candidate_for_path(root, path, threshold, line_count=line_count)
        candidates.append(candidate)
    return candidates


def _scan_project_root(root: Path, threshold: int) -> list[LargeFileCandidate]:
    """Scan the active project root for oversized Python source files."""
    candidates: list[LargeFileCandidate] = []
    for path in root.rglob("*.py"):
        if _path_is_excluded(root, path):
            continue
        line_count = count_physical_lines(path)
        if line_count <= threshold:
            continue
        candidates.append(
            _candidate_for_path(root, path.resolve(), threshold, line_count=line_count)
        )
    candidates.sort(key=lambda item: (-item.line_count_physical, item.relative_path))
    return candidates


def _candidate_for_path(
    root: Path,
    path: Path,
    threshold: int,
    *,
    line_count: int,
) -> LargeFileCandidate:
    """Classify one path into an eligible or blocked candidate."""
    if path.suffix != ".py":
        return LargeFileCandidate.blocked(
            path=path,
            root=root,
            line_count=line_count,
            reason="NOT_PYTHON_SOURCE",
            suggested_action="Blocked: not Python source",
        )
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return LargeFileCandidate.blocked(
            path=path,
            root=root,
            line_count=line_count,
            reason="WRONG_BOX",
            suggested_action="Blocked: wrong box",
        )
    if _path_is_excluded(root, path):
        return LargeFileCandidate.blocked(
            path=path,
            root=root,
            line_count=line_count,
            reason="GENERATED_OR_SUPPORT_ARTIFACT",
            suggested_action="Blocked: generated artifact",
        )
    if line_count <= threshold:
        action = "Already compliant"
    else:
        action = "Analyze"
    return _eligible_candidate(root, path, line_count, action)


def _eligible_candidate(
    root: Path,
    path: Path,
    line_count: int,
    suggested_action: str,
) -> LargeFileCandidate:
    """Build an eligible candidate with lightweight AST counts."""
    class_count = 0
    function_count = 0
    missing_docstrings = 0
    public_count = 0
    risk_flags: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        risk_flags.append("NEEDS_SOURCE_INSPECTION")
    except OSError:
        risk_flags.append("NEEDS_SOURCE_INSPECTION")
    else:
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                class_count += 1
                if not node.name.startswith("_"):
                    public_count += 1
                    if ast.get_docstring(node) is None:
                        missing_docstrings += 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_count += 1
                if not node.name.startswith("_"):
                    public_count += 1
                    if ast.get_docstring(node) is None:
                        missing_docstrings += 1
            elif isinstance(node, ast.ImportFrom) and node.level > 0:
                risk_flags.append("RELATIVE_IMPORT_RISK")
            elif isinstance(node, ast.ImportFrom):
                if any(alias.name == "*" for alias in node.names):
                    risk_flags.append("STAR_IMPORT")
    relative_path = str(path.resolve().relative_to(root.resolve())).replace("\\", "/")
    return LargeFileCandidate(
        schema_version=SCHEMA_VERSION,
        path=str(path.resolve()),
        relative_path=relative_path,
        line_count_physical=line_count,
        public_symbol_count=public_count,
        class_count=class_count,
        function_count=function_count,
        missing_docstring_count=missing_docstrings,
        risk_flags=sorted(set(risk_flags)),
        is_eligible=suggested_action != "Already compliant",
        suggested_action=suggested_action,
    )


def _path_is_excluded(root: Path, path: Path) -> bool:
    """Return whether the path is generated, support, or transient output."""
    if any(part in _EXCLUDED_PARTS for part in path.parts):
        return True
    lowered = str(path).replace("\\", "/").lower()
    if any(fragment.lower() in lowered for fragment in _EXCLUDED_FRAGMENTS):
        return True
    if any(str(path).endswith(suffix) for suffix in _GENERATED_SUFFIXES):
        return True
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return True
    return False


def _dedupe_candidates(candidates: Iterable[LargeFileCandidate]) -> list[LargeFileCandidate]:
    """Remove duplicate candidate paths while preserving highest line count."""
    by_path: dict[str, LargeFileCandidate] = {}
    for candidate in candidates:
        existing = by_path.get(candidate.path)
        if existing is None or candidate.line_count_physical > existing.line_count_physical:
            by_path[candidate.path] = candidate
    result = list(by_path.values())
    result.sort(key=lambda item: (-item.line_count_physical, item.relative_path))
    return result
