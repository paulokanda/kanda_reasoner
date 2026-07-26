# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_shadow_backend.py
"""Shadow backend implementations for isolated validation of one sealed payload."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import shutil
import subprocess
from typing import Any, Protocol

from .models import SCHEMA_VERSION
from .workbench_sealed_payload import WorkbenchSealedPayload, verify_sealed_payload

__all__ = [
    "SHADOW_BACKEND_FEATURE_ID",
    "ShadowBackendEligibility",
    "ShadowMaterializationResult",
    "ShadowBackend",
    "ControlledMirrorBackend",
    "GitWorktreeBackend",
    "choose_shadow_backend",
]

SHADOW_BACKEND_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-shadow-backend-v1"
)


@dataclass(frozen=True)
class ShadowBackendEligibility:
    """Eligibility evidence for one shadow backend and physical project."""

    backend_name: str
    eligible: bool
    project_root: str
    reasons: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["reasons"] = list(self.reasons)
        data["warnings"] = list(self.warnings)
        return data


@dataclass(frozen=True)
class ShadowMaterializationResult:
    """Evidence that the exact sealed payload was materialized in an isolated root."""

    schema_version: str
    feature_id: str
    status: str
    backend_name: str
    project_root: str
    shadow_root: str
    payload_hash: str
    applied_files: tuple[str, ...]
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    source_mutation_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["applied_files"] = list(self.applied_files)
        data["blockers"] = list(self.blockers)
        data["warnings"] = list(self.warnings)
        return data


class ShadowBackend(Protocol):
    """Public backend seam; implementations may not mutate the active project tree."""

    name: str

    def eligibility(self, project_root: str | Path) -> ShadowBackendEligibility:
        ...

    def materialize(
        self,
        *,
        project_root: str | Path,
        shadow_root: str | Path,
        sealed_payload: WorkbenchSealedPayload,
    ) -> ShadowMaterializationResult:
        ...


class ControlledMirrorBackend:
    """Create a controlled full project mirror and apply exact sealed bytes inside it."""

    name = "controlled_mirror"

    def eligibility(self, project_root: str | Path) -> ShadowBackendEligibility:
        root = Path(project_root).resolve()
        reasons: list[str] = []
        if not root.is_dir():
            reasons.append("PROJECT_ROOT_NOT_DIRECTORY")
        parent = root.parent
        if not parent.exists() or not os_access_write(parent):
            reasons.append("PROJECT_PARENT_NOT_WRITABLE")
        return ShadowBackendEligibility(
            backend_name=self.name,
            eligible=not reasons,
            project_root=str(root),
            reasons=tuple(reasons),
            warnings=("MIRROR_EXCLUDES_VCS_AND_CACHE_DIRECTORIES",),
        )

    def materialize(
        self,
        *,
        project_root: str | Path,
        shadow_root: str | Path,
        sealed_payload: WorkbenchSealedPayload,
    ) -> ShadowMaterializationResult:
        root = Path(project_root).resolve()
        shadow = Path(shadow_root).resolve()
        eligibility = self.eligibility(root)
        blockers = list(eligibility.reasons)
        blockers.extend(_shadow_root_blockers(root, shadow))
        valid, seal_blockers = verify_sealed_payload(sealed_payload)
        if not valid:
            blockers.extend(seal_blockers)
        if blockers:
            return _result(self.name, root, shadow, sealed_payload, [], blockers, eligibility.warnings)
        if shadow.exists():
            shutil.rmtree(shadow)
        shutil.copytree(root, shadow, ignore=_mirror_ignore)
        applied, apply_blockers = _apply_exact_payload(root, shadow, sealed_payload)
        blockers.extend(apply_blockers)
        return _result(self.name, root, shadow, sealed_payload, applied, blockers, eligibility.warnings)


class GitWorktreeBackend:
    """Create a detached linked worktree only when Git state can represent live source truth."""

    name = "git_worktree"

    def eligibility(self, project_root: str | Path) -> ShadowBackendEligibility:
        root = Path(project_root).resolve()
        reasons: list[str] = []
        warnings: list[str] = []
        git = shutil.which("git")
        if not git:
            reasons.append("GIT_EXECUTABLE_UNAVAILABLE")
            return ShadowBackendEligibility(self.name, False, str(root), tuple(reasons), tuple(warnings))
        top = _run_git(root, ["rev-parse", "--show-toplevel"])
        if top.returncode != 0:
            reasons.append("PROJECT_NOT_GIT_WORKTREE")
        else:
            try:
                if Path(top.stdout.strip()).resolve() != root:
                    reasons.append("PROJECT_ROOT_NOT_GIT_TOPLEVEL")
            except OSError:
                reasons.append("GIT_TOPLEVEL_RESOLUTION_FAILED")
        status = _run_git(root, ["status", "--porcelain", "--untracked-files=all"])
        if status.returncode != 0:
            reasons.append("GIT_STATUS_FAILED")
        elif status.stdout.strip():
            reasons.append("GIT_WORKTREE_DIRTY_OR_UNTRACKED")
        submodules = _run_git(root, ["submodule", "status", "--recursive"])
        if submodules.returncode == 0 and submodules.stdout.strip():
            reasons.append("GIT_SUBMODULES_REQUIRE_CONTROLLED_MIRROR")
        warnings.append("WORKTREE_SHADOW_REPRESENTS_COMMITTED_HEAD_ONLY")
        return ShadowBackendEligibility(
            backend_name=self.name,
            eligible=not reasons,
            project_root=str(root),
            reasons=tuple(reasons),
            warnings=tuple(warnings),
        )

    def materialize(
        self,
        *,
        project_root: str | Path,
        shadow_root: str | Path,
        sealed_payload: WorkbenchSealedPayload,
    ) -> ShadowMaterializationResult:
        root = Path(project_root).resolve()
        shadow = Path(shadow_root).resolve()
        eligibility = self.eligibility(root)
        blockers = list(eligibility.reasons)
        blockers.extend(_shadow_root_blockers(root, shadow))
        valid, seal_blockers = verify_sealed_payload(sealed_payload)
        if not valid:
            blockers.extend(seal_blockers)
        if blockers:
            return _result(self.name, root, shadow, sealed_payload, [], blockers, eligibility.warnings)
        if shadow.exists():
            shutil.rmtree(shadow)
        shadow.parent.mkdir(parents=True, exist_ok=True)
        completed = _run_git(root, ["worktree", "add", "--detach", str(shadow), "HEAD"])
        if completed.returncode != 0:
            blockers.append("GIT_WORKTREE_ADD_FAILED:" + completed.stderr.strip())
            return _result(self.name, root, shadow, sealed_payload, [], blockers, eligibility.warnings)
        applied, apply_blockers = _apply_exact_payload(root, shadow, sealed_payload)
        blockers.extend(apply_blockers)
        return _result(self.name, root, shadow, sealed_payload, applied, blockers, eligibility.warnings)


def choose_shadow_backend(project_root: str | Path) -> tuple[ShadowBackend, ShadowBackendEligibility]:
    """Prefer a clean exact Git worktree, otherwise use the controlled mirror backend."""
    worktree = GitWorktreeBackend()
    evidence = worktree.eligibility(project_root)
    if evidence.eligible:
        return worktree, evidence
    mirror = ControlledMirrorBackend()
    mirror_evidence = mirror.eligibility(project_root)
    combined_warnings = tuple(sorted(set((*mirror_evidence.warnings, *evidence.reasons))))
    return mirror, ShadowBackendEligibility(
        backend_name=mirror.name,
        eligible=mirror_evidence.eligible,
        project_root=mirror_evidence.project_root,
        reasons=mirror_evidence.reasons,
        warnings=combined_warnings,
    )


def _apply_exact_payload(
    project_root: Path,
    shadow_root: Path,
    payload: WorkbenchSealedPayload,
) -> tuple[list[str], list[str]]:
    applied: list[str] = []
    blockers: list[str] = []
    for item in payload.files:
        source = Path(item.payload_path).resolve()
        destination = Path(item.destination_path).resolve()
        try:
            relative = destination.relative_to(project_root)
        except ValueError:
            blockers.append(f"PAYLOAD_DESTINATION_OUTSIDE_PROJECT:{item.relative_path}")
            continue
        shadow_destination = (shadow_root / relative).resolve()
        try:
            shadow_destination.relative_to(shadow_root)
        except ValueError:
            blockers.append(f"SHADOW_DESTINATION_ESCAPE:{item.relative_path}")
            continue
        raw = source.read_bytes()
        shadow_destination.parent.mkdir(parents=True, exist_ok=True)
        shadow_destination.write_bytes(raw)
        if shadow_destination.read_bytes() != raw:
            blockers.append(f"SHADOW_PAYLOAD_BYTE_MISMATCH:{item.relative_path}")
            continue
        applied.append(str(shadow_destination))
    return applied, blockers


def _shadow_root_blockers(project_root: Path, shadow_root: Path) -> list[str]:
    blockers: list[str] = []
    if shadow_root == project_root:
        blockers.append("SHADOW_ROOT_EQUALS_PROJECT_ROOT")
    try:
        shadow_root.relative_to(project_root)
    except ValueError:
        pass
    else:
        blockers.append("SHADOW_ROOT_INSIDE_ACTIVE_PROJECT")
    return blockers


def _mirror_ignore(_directory: str, names: list[str]) -> set[str]:
    ignored = {".git", ".hg", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
    return {name for name in names if name in ignored or name.endswith(".pyc")}


def _run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=str(root),
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(["git", *args], 127, "", str(exc))


def os_access_write(path: Path) -> bool:
    """Return a conservative write-readiness signal without creating project artifacts."""
    import os

    return os.access(path, os.W_OK)


def _result(
    backend_name: str,
    project_root: Path,
    shadow_root: Path,
    payload: WorkbenchSealedPayload,
    applied: list[str],
    blockers: list[str],
    warnings: tuple[str, ...],
) -> ShadowMaterializationResult:
    unique_blockers = tuple(sorted(set(blockers)))
    return ShadowMaterializationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=SHADOW_BACKEND_FEATURE_ID,
        status="shadow_materialized" if not unique_blockers else "blocked",
        backend_name=backend_name,
        project_root=str(project_root),
        shadow_root=str(shadow_root),
        payload_hash=payload.payload_hash,
        applied_files=tuple(applied),
        blockers=unique_blockers,
        warnings=tuple(sorted(set(warnings))),
        source_mutation_enabled=False,
    )
