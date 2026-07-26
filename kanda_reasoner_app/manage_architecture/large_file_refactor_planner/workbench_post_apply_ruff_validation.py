# project-path: large_file_refactor_planner/workbench_post_apply_ruff_validation.py
"""Read-only Ruff verification for files written by Workbench apply."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
import os
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    canonical_transient_garbage_root,
)
import shutil
import subprocess
import sys
from typing import Any, Sequence

from kanda_reasoner_app.source_hygiene.ruff_policy_identity import (
    resolve_ruff_policy_identity,
)

from .workbench_project_support_paths import preview_root_blockers

__all__ = [
    "POST_APPLY_RUFF_FEATURE_ID",
    "WorkbenchPostApplyRuffResult",
    "validate_and_write_post_apply_ruff",
]

POST_APPLY_RUFF_FEATURE_ID = (
    "architecture-review-large-file-refactor-post-apply-ruff-verification-v1"
)
_REPORT_NAME = "SOURCE_APPLY_POST_APPLY_RUFF_VALIDATION.json"
_TIMEOUT_SECONDS = 180.0
_ALLOWED_SUFFIXES = frozenset({".py", ".pyi", ".pyw"})
_PROTECTED_PARTS = frozenset(
    {
        ".project_reference",
        "_project_reference",
        "project_freeze_after_update",
        "project_error_memory",
        "project_freeze_ledger",
        "show_project_to_ai",
        "_show_project_to_ai",
    }
)


@dataclass(frozen=True)
class WorkbenchPostApplyRuffResult:
    """Read-only Ruff evidence for the exact files written by one apply."""

    feature_id: str
    status: str
    project_root: str
    preview_root: str
    report_path: str
    policy_path: str
    policy_sha256: str
    required_version: str
    ruff_version: str
    ruff_command_source: str
    checked_files: list[str] = field(default_factory=list)
    lint_returncode: int | None = None
    format_returncode: int | None = None
    lint_stdout: str = ""
    lint_stderr: str = ""
    format_stdout: str = ""
    format_stderr: str = ""
    source_hashes_unchanged: bool = False
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready result."""
        return asdict(self)


def validate_and_write_post_apply_ruff(
    *,
    active_project_root: str | Path,
    preview_root: str | Path,
    checked_files: Sequence[str | Path],
    ruff_argv_prefix: Sequence[str] | None = None,
    skip_due_to_prior_blockers: bool = False,
) -> WorkbenchPostApplyRuffResult:
    """Run read-only Ruff lint and format checks on touched Python files."""
    project_root = Path(active_project_root).expanduser().resolve()
    evidence_root = Path(preview_root).expanduser().resolve()
    report_path = evidence_root / _REPORT_NAME
    blockers = _evidence_root_blockers(project_root, evidence_root)
    warnings: list[str] = []
    files = _validated_files(project_root, checked_files, blockers)
    policy_path = ""
    policy_sha256 = ""
    required_version = ""
    ruff_version = ""
    command_source = ""
    lint: tuple[int, str, str] | None = None
    formatting: tuple[int, str, str] | None = None
    checked_rules = [
        "touched_python_files_only",
        "ruff_evidence_inside_project_owned_preview_root",
    ]
    before = _hashes(files)

    if skip_due_to_prior_blockers:
        warnings.append("POST_APPLY_RUFF_SKIPPED_DUE_TO_PRIOR_BLOCKERS")
        status = "skipped"
    elif blockers:
        status = "blocked"
    elif not files:
        warnings.append("POST_APPLY_RUFF_NO_PYTHON_FILES")
        status = "passed"
    else:
        policy = _resolve_policy(project_root, blockers, warnings)
        if policy is not None:
            checked_rules.append(
                "canonical_ruff_policy_identity_required_when_configured"
            )
            policy_path = policy.config_path
            policy_sha256 = policy.config_sha256
            required_version = policy.required_version
            identity = _resolve_exact_ruff(
                project_root,
                required_version,
                explicit_prefix=ruff_argv_prefix,
            )
            if identity is None:
                blockers.append("POST_APPLY_RUFF_EXACT_VERSION_NOT_AVAILABLE")
            else:
                checked_rules.append(
                    "exact_pinned_ruff_version_required_when_configured"
                )
                prefix, ruff_version, command_source = identity
                lint, formatting = _run_ruff_checks(
                    prefix=prefix,
                    policy_path=policy_path,
                    files=files,
                    project_root=project_root,
                )
                checked_rules.extend(
                    [
                        "ruff_lint_read_only",
                        "ruff_format_check_read_only",
                    ]
                )
                if lint[0] != 0:
                    blockers.append("POST_APPLY_RUFF_LINT_BLOCKED")
                if formatting[0] != 0:
                    blockers.append("POST_APPLY_RUFF_FORMAT_BLOCKED")
        status = "blocked" if blockers else "passed"
        if policy is None and not blockers:
            status = "not_configured"

    after = _hashes(files)
    unchanged = before == after
    checked_rules.append("source_hashes_unchanged_during_post_apply_ruff_stage")
    if not unchanged:
        blockers.append("POST_APPLY_RUFF_SOURCE_MUTATION_DETECTED")
        status = "blocked"

    result = WorkbenchPostApplyRuffResult(
        feature_id=POST_APPLY_RUFF_FEATURE_ID,
        status=status,
        project_root=str(project_root),
        preview_root=str(evidence_root),
        report_path=str(report_path),
        policy_path=policy_path,
        policy_sha256=policy_sha256,
        required_version=required_version,
        ruff_version=ruff_version,
        ruff_command_source=command_source,
        checked_files=[str(path) for path in files],
        lint_returncode=lint[0] if lint is not None else None,
        format_returncode=formatting[0] if formatting is not None else None,
        lint_stdout=_bounded_text(lint[1], 4000) if lint is not None else "",
        lint_stderr=_bounded_text(lint[2], 4000) if lint is not None else "",
        format_stdout=(
            _bounded_text(formatting[1], 4000) if formatting is not None else ""
        ),
        format_stderr=(
            _bounded_text(formatting[2], 4000) if formatting is not None else ""
        ),
        source_hashes_unchanged=unchanged,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
        checked_rules=list(dict.fromkeys(checked_rules)),
    )
    if not _evidence_root_blockers(project_root, evidence_root):
        _write_report(result)
    return result


def _evidence_root_blockers(project_root: Path, evidence_root: Path) -> list[str]:
    """Return blockers when Ruff evidence escapes Workbench Preview support."""
    return [
        "POST_APPLY_RUFF_" + item
        for item in preview_root_blockers(project_root, evidence_root)
    ]


def _validated_files(
    project_root: Path,
    values: Sequence[str | Path],
    blockers: list[str],
) -> tuple[Path, ...]:
    """Return unique project-owned Python files and append containment blockers."""
    output: list[Path] = []
    seen: set[str] = set()
    for value in values:
        raw = Path(value).expanduser()
        path = (
            (project_root / raw).resolve() if not raw.is_absolute() else raw.resolve()
        )
        try:
            path.relative_to(project_root)
        except ValueError:
            blockers.append("POST_APPLY_RUFF_FILE_OUTSIDE_PROJECT_ROOT:" + str(path))
            continue
        if any(part.casefold() in _PROTECTED_PARTS for part in path.parts):
            blockers.append("POST_APPLY_RUFF_FILE_IN_PROTECTED_ROOT:" + str(path))
            continue
        if path.suffix.casefold() not in _ALLOWED_SUFFIXES:
            continue
        if not path.is_file():
            blockers.append("POST_APPLY_RUFF_FILE_MISSING:" + str(path))
            continue
        marker = str(path).casefold()
        if marker not in seen:
            seen.add(marker)
            output.append(path)
    return tuple(output)


def _resolve_policy(
    project_root: Path,
    blockers: list[str],
    warnings: list[str],
) -> Any | None:
    """Resolve canonical Ruff policy while allowing unconfigured projects."""
    try:
        return resolve_ruff_policy_identity(project_root)
    except ValueError as exc:
        if str(exc) == "RUFF_POLICY_CONFIG_MISSING":
            warnings.append("POST_APPLY_RUFF_POLICY_NOT_CONFIGURED")
        else:
            blockers.append("POST_APPLY_RUFF_POLICY_INVALID:" + _bounded_text(exc))
    except (OSError, UnicodeError) as exc:
        blockers.append("POST_APPLY_RUFF_POLICY_INVALID:" + _bounded_text(exc))
    return None


def _resolve_exact_ruff(
    project_root: Path,
    required_version: str,
    *,
    explicit_prefix: Sequence[str] | None,
) -> tuple[tuple[str, ...], str, str] | None:
    """Resolve an existing Ruff command matching the canonical pinned version."""
    required = required_version.removeprefix("==").strip()
    environment_name = "ruff_" + required.replace(".", "_") + "_env"
    candidates: list[tuple[tuple[str, ...], str]] = []
    if explicit_prefix:
        candidates.append((tuple(str(item) for item in explicit_prefix), "explicit"))
    env_value = os.environ.get("KANDA_RUFF_EXECUTABLE", "").strip()
    if env_value:
        candidates.append(((env_value,), "environment"))
    path_ruff = shutil.which("ruff")
    if path_ruff:
        candidates.append(((path_ruff,), "path"))
    daily_root = canonical_transient_garbage_root(project_root)
    candidates.extend(
        [
            (
                (str(daily_root / environment_name / "Scripts" / "ruff.exe"),),
                "daily_work_windows",
            ),
            (
                (str(daily_root / environment_name / "bin" / "ruff"),),
                "daily_work_posix",
            ),
            ((sys.executable, "-m", "ruff"), "python_module"),
        ]
    )
    seen: set[tuple[str, ...]] = set()
    for prefix, source in candidates:
        if prefix in seen:
            continue
        seen.add(prefix)
        executable = prefix[0]
        if len(prefix) == 1 and not Path(executable).is_file():
            resolved = shutil.which(executable)
            if not resolved:
                continue
            prefix = (resolved,)
        result = _run_process((*prefix, "--version"), cwd=project_root, timeout=20.0)
        version = _version_from_text(result[1] or result[2])
        if result[0] == 0 and version == required:
            return prefix, version, source
    return None


def _run_ruff_checks(
    *,
    prefix: Sequence[str],
    policy_path: str,
    files: Sequence[Path],
    project_root: Path,
) -> tuple[tuple[int, str, str], tuple[int, str, str]]:
    """Run read-only lint and formatter checks against exact touched files."""
    paths = tuple(str(path) for path in files)
    lint = _run_process(
        (
            *prefix,
            "check",
            "--no-fix",
            "--no-unsafe-fixes",
            "--no-preview",
            "--no-cache",
            "--force-exclude",
            "--color",
            "never",
            "--config",
            policy_path,
            *paths,
        ),
        cwd=project_root,
    )
    formatting = _run_process(
        (
            *prefix,
            "format",
            "--check",
            "--no-preview",
            "--no-cache",
            "--force-exclude",
            "--color",
            "never",
            "--config",
            policy_path,
            *paths,
        ),
        cwd=project_root,
    )
    return lint, formatting


def _run_process(
    argv: Sequence[str],
    *,
    cwd: Path,
    timeout: float = _TIMEOUT_SECONDS,
) -> tuple[int, str, str]:
    """Run one process without shell or project cache writes."""
    environment = dict(os.environ)
    environment["NO_COLOR"] = "1"
    environment["RUFF_NO_CACHE"] = "1"
    try:
        completed = subprocess.run(
            tuple(str(item) for item in argv),
            cwd=str(cwd),
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        return 124, _coerce_text(exc.stdout), _coerce_text(exc.stderr)
    except OSError as exc:
        return 127, "", str(exc)
    return completed.returncode, completed.stdout or "", completed.stderr or ""


def _write_report(result: WorkbenchPostApplyRuffResult) -> None:
    """Write Ruff evidence under the existing project-owned Preview root."""
    report = Path(result.report_path).resolve()
    root = Path(result.preview_root).resolve()
    try:
        report.relative_to(root)
    except ValueError as exc:
        raise RuntimeError("POST_APPLY_RUFF_REPORT_OUTSIDE_PREVIEW_ROOT") from exc
    root.mkdir(parents=True, exist_ok=True)
    report.write_bytes(
        (json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n").encode("utf-8")
    )


def _hashes(paths: Sequence[Path]) -> dict[str, str]:
    """Return exact byte hashes for checked files."""
    return {
        str(path): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in paths
        if path.is_file()
    }


def _version_from_text(value: str) -> str:
    """Return a semantic Ruff version from command output."""
    parts = str(value or "").strip().split()
    if len(parts) >= 2 and parts[0].casefold() == "ruff":
        return parts[1].strip()
    return ""


def _coerce_text(value: object) -> str:
    """Return decoded subprocess timeout text."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _bounded_text(value: object, limit: int = 1200) -> str:
    """Return bounded diagnostic text without terminal control output."""
    text = str(value or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."
