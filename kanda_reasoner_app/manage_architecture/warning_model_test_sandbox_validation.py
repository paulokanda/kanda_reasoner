# project-path: kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py
"""Validate Local AI test-only proposals in a disposable project copy before apply."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
import os
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    canonical_transient_garbage_root,
)
import py_compile
import shutil
import subprocess
import sys

from kanda_reasoner_app.manage_architecture.warning_model_test_generation_contract import (
    ModelTestMutationProposal,
)

__all__ = [
    "SandboxMutationOutcome",
    "SandboxValidationReport",
    "validate_mutation_proposals",
]

ProgressCallback = Callable[[int, int, int, int, str, str], None]
Runner = Callable[..., subprocess.CompletedProcess[str]]
_COPY_IGNORE_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
}


@dataclass(frozen=True, slots=True)
class SandboxMutationOutcome:
    """Describe disposable-copy validation for one proposed test change."""

    source_path: str
    target_test_path: str
    accepted: bool
    reason: str


@dataclass(frozen=True, slots=True)
class SandboxValidationReport:
    """Hold one disposable project validation run and its per-source outcomes."""

    sandbox_root: str
    outcomes: tuple[SandboxMutationOutcome, ...]
    targeted_pytest_return_codes: tuple[tuple[str, int], ...]
    audit_return_code: int

    def outcome_by_source(self) -> dict[str, SandboxMutationOutcome]:
        return {item.source_path: item for item in self.outcomes}


def _sandbox_parent(project_root: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    daily_work = canonical_transient_garbage_root(project_root)
    return daily_work / "warning_local_ai_resolver" / "test_generation" / timestamp


def _ignore_copy(directory: str, names: list[str]) -> set[str]:
    del directory
    ignored = {name for name in names if name in _COPY_IGNORE_NAMES}
    ignored.update(name for name in names if name.endswith((".pyc", ".pyo")))
    return ignored


def _prepare_disposable_project(project_root: Path) -> Path:
    parent = _sandbox_parent(project_root)
    sandbox = parent / "project"
    parent.mkdir(parents=True, exist_ok=False)
    shutil.copytree(
        project_root,
        sandbox,
        dirs_exist_ok=False,
        ignore=_ignore_copy,
    )
    return sandbox


def _proposal_collisions(
    proposals: tuple[ModelTestMutationProposal, ...],
) -> set[str]:
    owners: dict[str, list[str]] = {}
    for item in proposals:
        owners.setdefault(item.target_test_path, []).append(item.source_path)
    return {
        source
        for sources in owners.values()
        if len(sources) > 1
        for source in sources
    }


def _overlay_proposals(
    sandbox: Path,
    proposals: tuple[ModelTestMutationProposal, ...],
    collisions: set[str],
) -> None:
    for item in proposals:
        if item.source_path in collisions:
            continue
        path = sandbox / Path(item.target_test_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(item.rendered_test_text, encoding="utf-8", newline="")
        py_compile.compile(str(path), doraise=True)


def _run_targeted_pytest(
    sandbox: Path,
    test_path: str,
    *,
    runner: Runner,
    timeout_seconds: int,
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(sandbox)
    return runner(
        [sys.executable, "-m", "pytest", test_path, "-q", "--disable-warnings", "--maxfail=1"],
        cwd=str(sandbox),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
        check=False,
    )


def _run_architecture_audit(
    sandbox: Path,
    *,
    runner: Runner,
    timeout_seconds: int,
) -> subprocess.CompletedProcess[str]:
    cli = sandbox / "kanda_reasoner_app" / "manage_architecture" / "manage_architecture.py"
    if not cli.is_file():
        return subprocess.CompletedProcess(
            args=[],
            returncode=97,
            stdout="",
            stderr="Architecture Review CLI missing from disposable project.",
        )
    env = dict(os.environ)
    env["PYTHONPATH"] = str(sandbox)
    return runner(
        [sys.executable, str(cli), "--root", str(sandbox), "--validate"],
        cwd=str(sandbox),
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
        check=False,
    )


def _remaining_test_protection_sources(output: str) -> set[str]:
    remaining: set[str] = set()
    for raw_line in str(output or "").splitlines():
        line = raw_line.strip()
        if "TEST_PROTECTION_GAP" not in line or "::" not in line:
            continue
        before_message = line.split("::", 1)[0].strip()
        tokens = before_message.split()
        if len(tokens) >= 3:
            remaining.add(tokens[-1].replace("\\", "/"))
    return remaining


def _diagnostic_excerpt(completed: subprocess.CompletedProcess[str]) -> str:
    text = (completed.stdout or "") + ("\n" + completed.stderr if completed.stderr else "")
    compact = " ".join(text.split())
    return compact[:600]


def validate_mutation_proposals(
    project_root: str | Path,
    proposals: tuple[ModelTestMutationProposal, ...],
    *,
    progress_callback: ProgressCallback | None = None,
    runner: Runner = subprocess.run,
    pytest_timeout_seconds: int = 120,
    audit_timeout_seconds: int = 240,
) -> SandboxValidationReport:
    """Run proposed tests in a disposable copy and require fresh audit evidence."""
    root = Path(project_root).expanduser().resolve()
    if not proposals:
        return SandboxValidationReport("", (), (), 0)
    collisions = _proposal_collisions(proposals)
    sandbox = _prepare_disposable_project(root)
    try:
        _overlay_proposals(sandbox, proposals, collisions)
    except Exception as exc:
        outcomes = tuple(
            SandboxMutationOutcome(
                source_path=item.source_path,
                target_test_path=item.target_test_path,
                accepted=False,
                reason="Disposable project overlay failed: " + type(exc).__name__ + ": " + str(exc),
            )
            for item in proposals
        )
        return SandboxValidationReport(str(sandbox), outcomes, (), 98)

    pytest_results: dict[str, subprocess.CompletedProcess[str]] = {}
    unique_targets = sorted(
        {
            item.target_test_path
            for item in proposals
            if item.source_path not in collisions
        }
    )
    for index, target in enumerate(unique_targets, start=1):
        if progress_callback is not None:
            progress_callback(
                len(proposals),
                len(proposals) - index + 1,
                0,
                0,
                target,
                "sandbox_pytest",
            )
        try:
            pytest_results[target] = _run_targeted_pytest(
                sandbox,
                target,
                runner=runner,
                timeout_seconds=pytest_timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            pytest_results[target] = subprocess.CompletedProcess(
                args=exc.cmd,
                returncode=124,
                stdout=str(exc.stdout or ""),
                stderr="Targeted pytest timed out.",
            )

    if progress_callback is not None:
        progress_callback(
            len(proposals),
            0,
            0,
            0,
            "Architecture Review",
            "sandbox_audit",
        )
    try:
        audit = _run_architecture_audit(
            sandbox,
            runner=runner,
            timeout_seconds=audit_timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        audit = subprocess.CompletedProcess(
            args=exc.cmd,
            returncode=124,
            stdout=str(exc.stdout or ""),
            stderr="Architecture Review timed out in disposable project.",
        )
    audit_text = (audit.stdout or "") + ("\n" + audit.stderr if audit.stderr else "")
    audit_available = "ARCHITECTURE VALIDATION SUMMARY" in audit_text
    remaining = _remaining_test_protection_sources(audit_text) if audit_available else set()

    outcomes: list[SandboxMutationOutcome] = []
    for item in proposals:
        if item.source_path in collisions:
            accepted = False
            reason = "Multiple Local AI proposals target the same test file; collision kept fail-closed."
        else:
            pytest_result = pytest_results[item.target_test_path]
            if pytest_result.returncode != 0:
                accepted = False
                reason = "Targeted pytest failed: " + _diagnostic_excerpt(pytest_result)
            elif not audit_available:
                accepted = False
                reason = "Fresh Architecture Review evidence was unavailable in the disposable project."
            elif item.source_path.replace("\\", "/") in remaining:
                accepted = False
                reason = "TEST_PROTECTION_GAP remained after the disposable-project test change."
            else:
                accepted = True
                reason = "Targeted pytest passed and fresh Architecture Review removed the source gap."
        outcomes.append(
            SandboxMutationOutcome(
                source_path=item.source_path,
                target_test_path=item.target_test_path,
                accepted=accepted,
                reason=reason,
            )
        )
    return SandboxValidationReport(
        sandbox_root=str(sandbox),
        outcomes=tuple(outcomes),
        targeted_pytest_return_codes=tuple(
            (path, completed.returncode)
            for path, completed in sorted(pytest_results.items())
        ),
        audit_return_code=audit.returncode,
    )
