# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_execution_basis.py
"""Explicit execution-basis ownership and hash evidence for Workbench gates."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
from pathlib import Path
from typing import Any, Iterable

from .models import RefactorPlan, SCHEMA_VERSION

__all__ = [
    "WORKBENCH_EXECUTION_BASIS_FEATURE_ID",
    "ExecutionBasisFile",
    "WorkbenchExecutionBasisSet",
    "build_workbench_execution_basis_set",
    "execution_basis_is_fresh",
]

WORKBENCH_EXECUTION_BASIS_FEATURE_ID = (
    "architecture-review-large-file-refactor-execution-basis-v1"
)
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_ai",
    "_show_project_to_ai",
    "large_file_refactor_preview",
}


@dataclass(frozen=True)
class ExecutionBasisFile:
    """One path whose identity contributes to execution evidence validity."""

    path: str
    role: str
    exists: bool
    content_hash: str
    project_relative_path: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready basis record."""
        return asdict(self)


@dataclass(frozen=True)
class WorkbenchExecutionBasisSet:
    """Canonical set of source paths that downstream evidence depends on."""

    schema_version: str
    feature_id: str
    status: str
    active_project_root: str
    target_file: str
    mutation_basis: list[ExecutionBasisFile] = field(default_factory=list)
    api_basis: list[ExecutionBasisFile] = field(default_factory=list)
    dependency_basis: list[ExecutionBasisFile] = field(default_factory=list)
    validation_basis: list[ExecutionBasisFile] = field(default_factory=list)
    all_basis: list[ExecutionBasisFile] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready execution-basis dictionary."""
        data = asdict(self)
        for name in (
            "mutation_basis",
            "api_basis",
            "dependency_basis",
            "validation_basis",
            "all_basis",
        ):
            data[name] = [item.to_dict() for item in getattr(self, name)]
        return data


def build_workbench_execution_basis_set(
    *,
    plan: RefactorPlan | None,
    active_project_root: str,
    api_basis_paths: Iterable[str | Path] = (),
    dependency_basis_paths: Iterable[str | Path] = (),
    validation_basis_paths: Iterable[str | Path] = (),
) -> WorkbenchExecutionBasisSet:
    """Build explicit basis groups without reading mutable Planner GUI state."""
    root = Path(active_project_root).resolve()
    blockers: list[str] = []
    if plan is None:
        blockers.append("PLANNER_PLAN_MISSING")
        return _empty_result(root, blockers)
    target = Path(plan.target_file).resolve()
    if not _is_relative_to(target, root):
        blockers.append("TARGET_OUTSIDE_ACTIVE_PROJECT_ROOT")
    if _protected_parts(target):
        blockers.append("TARGET_INSIDE_PROTECTED_ROOT")

    mutation_paths = [target]
    for module in plan.proposed_modules:
        mutation_paths.append((target.parent / module.filename).resolve())
    api_paths = [target, *[Path(item).resolve() for item in api_basis_paths]]
    dependency_paths = [target, *[Path(item).resolve() for item in dependency_basis_paths]]
    validation_paths = [Path(item).resolve() for item in validation_basis_paths]

    mutation_basis = _records(root, mutation_paths, "mutation", blockers, allow_missing=True)
    api_basis = _records(root, api_paths, "api", blockers, allow_missing=False)
    dependency_basis = _records(root, dependency_paths, "dependency", blockers, allow_missing=False)
    validation_basis = _records(root, validation_paths, "validation", blockers, allow_missing=False)
    all_basis = _merge_records(
        mutation_basis,
        api_basis,
        dependency_basis,
        validation_basis,
    )
    status = "execution_basis_ready" if not blockers else "blocked"
    return WorkbenchExecutionBasisSet(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_EXECUTION_BASIS_FEATURE_ID,
        status=status,
        active_project_root=str(root),
        target_file=str(target),
        mutation_basis=mutation_basis,
        api_basis=api_basis,
        dependency_basis=dependency_basis,
        validation_basis=validation_basis,
        all_basis=all_basis,
        blockers=sorted(set(blockers)),
        warnings=_warnings(),
    )


def execution_basis_is_fresh(basis: WorkbenchExecutionBasisSet) -> tuple[bool, list[str]]:
    """Recheck existing basis files against their recorded content hashes."""
    blockers: list[str] = []
    root = Path(basis.active_project_root).resolve()
    for item in basis.all_basis:
        path = Path(item.path).resolve()
        if not _is_relative_to(path, root):
            blockers.append("BASIS_PATH_OUTSIDE_PROJECT_ROOT:" + item.path)
            continue
        exists_now = path.is_file()
        if item.exists != exists_now:
            blockers.append("BASIS_EXISTENCE_CHANGED:" + item.path)
            continue
        if item.exists and _sha256_file(path) != item.content_hash:
            blockers.append("BASIS_HASH_CHANGED:" + item.path)
    return not blockers, sorted(set(blockers))


def _records(
    root: Path,
    paths: Iterable[Path],
    role: str,
    blockers: list[str],
    *,
    allow_missing: bool,
) -> list[ExecutionBasisFile]:
    """Build deduplicated basis records and apply containment checks."""
    records: list[ExecutionBasisFile] = []
    seen: set[Path] = set()
    for raw in paths:
        path = raw.resolve()
        if path in seen:
            continue
        seen.add(path)
        if not _is_relative_to(path, root):
            blockers.append(f"{role.upper()}_BASIS_OUTSIDE_PROJECT_ROOT:{path}")
        if _protected_parts(path):
            blockers.append(f"{role.upper()}_BASIS_INSIDE_PROTECTED_ROOT:{path}")
        exists = path.is_file()
        if not exists and not allow_missing:
            blockers.append(f"{role.upper()}_BASIS_FILE_MISSING:{path}")
        records.append(
            ExecutionBasisFile(
                path=str(path),
                role=role,
                exists=exists,
                content_hash=_sha256_file(path) if exists else "",
                project_relative_path=_relative_text(path, root),
            )
        )
    return records


def _merge_records(*groups: list[ExecutionBasisFile]) -> list[ExecutionBasisFile]:
    """Merge basis groups by physical path while preserving first-seen order."""
    merged: list[ExecutionBasisFile] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            key = str(Path(item.path).resolve())
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)
    return merged


def _empty_result(root: Path, blockers: list[str]) -> WorkbenchExecutionBasisSet:
    """Return a stable blocked result when no plan exists."""
    return WorkbenchExecutionBasisSet(
        schema_version=SCHEMA_VERSION,
        feature_id=WORKBENCH_EXECUTION_BASIS_FEATURE_ID,
        status="blocked",
        active_project_root=str(root),
        target_file="",
        blockers=sorted(set(blockers)),
        warnings=_warnings(),
    )


def _relative_text(path: Path, root: Path) -> str:
    """Return stable project-relative text or absolute evidence when outside."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def _warnings() -> list[str]:
    """Return stable basis-model warnings."""
    return [
        "EXECUTION_BASIS_IS_WORKBENCH_OWNED_EVIDENCE",
        "MISSING_MUTATION_DESTINATIONS_ARE_ALLOWED_FOR_PLANNED_CREATES",
        "UNRELATED_PROJECT_FILES_ARE_NOT_HASHED_BY_DEFAULT",
    ]


def _sha256_file(path: Path) -> str:
    """Return SHA-256 for one file or an empty value on read failure."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _protected_parts(path: Path) -> list[str]:
    """Return protected path components present after resolution."""
    return [part for part in (item.lower() for item in path.parts) if part in _PROTECTED_PARTS]


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return whether one resolved path is contained by another."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False
