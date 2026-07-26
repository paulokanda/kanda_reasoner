# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_behavior_validation.py
"""Optional behavior/test validation for Workbench guarded source apply."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import os
from pathlib import Path
import shlex
import subprocess
from typing import Any

from .workbench_project_support_paths import preview_runs_root
from .workbench_project_support_paths import preview_root_blockers as project_preview_root_blockers
from .models import SCHEMA_VERSION
from .workbench_guarded_source_apply import GuardedSourceApplyResult
from .workbench_post_apply_validator import PostApplyValidationResult
from .workbench_source_payload_builder import SourceApplyPayloadReadinessResult

__all__ = [
    "BEHAVIOR_VALIDATION_FEATURE_ID",
    "WorkbenchBehaviorValidationResult",
    "run_workbench_behavior_validation",
]

BEHAVIOR_VALIDATION_FEATURE_ID = "architecture-review-large-file-refactor-behavior-validation-v1"
_BEHAVIOR_REPORT = "SOURCE_APPLY_BEHAVIOR_VALIDATION.json"
_TIMEOUT_SECONDS = 180
_FORBIDDEN_COMMAND_CHARS = {";", "&", "|", "<", ">", "`", "\n", "\r"}
_PROTECTED_PARTS = {
    ".project_reference",
    "_project_reference",
    "project_freeze_after_update",
    "project_error_memory",
    "project_freeze_ledger",
    "show_project_to_AI",
    "_show_project_to_AI",
}


@dataclass(frozen=True)
class WorkbenchBehaviorValidationResult:
    """Result of an optional post-apply behavior/test validation command."""

    schema_version: str
    feature_id: str
    status: str
    behavior_status: str
    target_file: str
    preview_root: str
    report_path: str
    test_command: str
    command_allowed: bool
    command_exit_code: int | None
    command_timed_out: bool
    behavior_validation_claimed: bool
    stdout_excerpt: str = ""
    stderr_excerpt: str = ""
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready behavior validation result."""
        return asdict(self)


def run_workbench_behavior_validation(
    *,
    apply_result: GuardedSourceApplyResult | None,
    post_apply_validation: PostApplyValidationResult | None,
    source_payload: SourceApplyPayloadReadinessResult | None,
    active_project_root: str,
    test_command: str,
) -> WorkbenchBehaviorValidationResult:
    """Run an allow-listed test command after structural post-apply validation."""
    project_root = Path(active_project_root).resolve()
    preview_root = _preview_root(project_root, apply_result)
    blockers = _entry_blockers(apply_result, post_apply_validation, source_payload)
    blockers.extend(_root_blockers(project_root, preview_root))
    command = test_command.strip()
    allowed, tokens, command_blockers = _parse_allowed_command(command)
    if command:
        blockers.extend(command_blockers)
    if blockers:
        result = _result(
            apply_result=apply_result,
            preview_root=preview_root,
            command=command,
            command_allowed=allowed,
            exit_code=None,
            timed_out=False,
            status="blocked",
            behavior_status="BEHAVIOR_VALIDATION_BLOCKED",
            behavior_claimed=False,
            stdout="",
            stderr="",
            blockers=blockers,
        )
        _write_report(result)
        return result
    if not command:
        result = _result(
            apply_result=apply_result,
            preview_root=preview_root,
            command=command,
            command_allowed=False,
            exit_code=None,
            timed_out=False,
            status="behavior_validation_not_run",
            behavior_status="BEHAVIOR_VALIDATION_NOT_RUN",
            behavior_claimed=False,
            stdout="",
            stderr="",
            blockers=[],
        )
        _write_report(result)
        return result
    run_result = _run_command(tokens, project_root)
    status = "behavior_validated_pass" if run_result[0] == 0 and not run_result[1] else "behavior_validation_failed"
    behavior_status = "BEHAVIOR_VALIDATED_PASS" if status == "behavior_validated_pass" else "BEHAVIOR_VALIDATION_FAILED"
    result = _result(
        apply_result=apply_result,
        preview_root=preview_root,
        command=command,
        command_allowed=True,
        exit_code=run_result[0],
        timed_out=run_result[1],
        status=status,
        behavior_status=behavior_status,
        behavior_claimed=status == "behavior_validated_pass",
        stdout=run_result[2],
        stderr=run_result[3],
        blockers=[] if status == "behavior_validated_pass" else ["BEHAVIOR_TEST_COMMAND_FAILED"],
    )
    _write_report(result)
    return result


def _entry_blockers(
    apply_result: GuardedSourceApplyResult | None,
    post_apply: PostApplyValidationResult | None,
    payload: SourceApplyPayloadReadinessResult | None,
) -> list[str]:
    """Return prerequisite blockers before optional behavior validation."""
    blockers: list[str] = []
    if apply_result is None or apply_result.status != "applied":
        blockers.append("GUARDED_SOURCE_APPLY_NOT_SUCCESSFUL")
    if post_apply is None or post_apply.status != "post_apply_validated":
        blockers.append("POST_APPLY_STRUCTURAL_VALIDATION_NOT_SUCCESSFUL")
    if payload is None or payload.status != "source_apply_payload_ready":
        blockers.append("SOURCE_APPLY_PAYLOAD_NOT_READY")
    if apply_result is not None and apply_result.import_rewrite_enabled:
        blockers.append("IMPORT_REWRITE_MUST_REMAIN_DISABLED")
    return blockers


def _parse_allowed_command(command: str) -> tuple[bool, list[str], list[str]]:
    """Parse and allow only project-test commands without shell metacharacters."""
    if not command:
        return False, [], []
    if any(char in command for char in _FORBIDDEN_COMMAND_CHARS):
        return False, [], ["COMMAND_CONTAINS_FORBIDDEN_SHELL_CHARACTER"]
    try:
        tokens = shlex.split(command)
    except ValueError:
        return False, [], ["COMMAND_PARSE_FAILED"]
    if not tokens:
        return False, [], []
    exe_name = Path(tokens[0]).name.lower()
    normalized = [exe_name, *[token.lower() for token in tokens[1:3]]]
    if exe_name in {"pytest", "pytest.exe"}:
        return True, tokens, []
    if len(normalized) >= 3 and _is_python_executable(exe_name) and normalized[1] == "-m":
        if normalized[2] in {"pytest", "unittest"}:
            return True, tokens, []
    return False, tokens, ["COMMAND_NOT_ALLOWLISTED_FOR_BEHAVIOR_VALIDATION"]


def _run_command(tokens: list[str], project_root: Path) -> tuple[int | None, bool, str, str]:
    """Run a test command without a shell and return exit code, timeout, stdout, stderr."""
    env = dict(os.environ)
    current_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(project_root) if not current_pythonpath else str(project_root) + os.pathsep + current_pythonpath
    try:
        completed = subprocess.run(
            tokens,
            cwd=str(project_root),
            env=env,
            text=True,
            capture_output=True,
            timeout=_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return None, True, exc.stdout or "", exc.stderr or ""
    except OSError as exc:
        return None, False, "", str(exc)
    return completed.returncode, False, completed.stdout, completed.stderr


def _root_blockers(project_root: Path, preview_root: Path) -> list[str]:
    """Return root containment blockers for behavior evidence output."""
    blockers: list[str] = []
    blockers.extend(project_preview_root_blockers(project_root, preview_root))
    if _protected_parts(preview_root):
        blockers.append("PREVIEW_ROOT_IN_PROTECTED_ROOT")
    return blockers


def _result(
    *,
    apply_result: GuardedSourceApplyResult | None,
    preview_root: Path,
    command: str,
    command_allowed: bool,
    exit_code: int | None,
    timed_out: bool,
    status: str,
    behavior_status: str,
    behavior_claimed: bool,
    stdout: str,
    stderr: str,
    blockers: list[str],
) -> WorkbenchBehaviorValidationResult:
    """Create a stable behavior validation result."""
    target = apply_result.target_file if apply_result else ""
    return WorkbenchBehaviorValidationResult(
        schema_version=SCHEMA_VERSION,
        feature_id=BEHAVIOR_VALIDATION_FEATURE_ID,
        status=status,
        behavior_status=behavior_status,
        target_file=target,
        preview_root=str(preview_root),
        report_path=str(preview_root / _BEHAVIOR_REPORT),
        test_command=command,
        command_allowed=command_allowed,
        command_exit_code=exit_code,
        command_timed_out=timed_out,
        behavior_validation_claimed=behavior_claimed,
        stdout_excerpt=_excerpt(stdout),
        stderr_excerpt=_excerpt(stderr),
        blockers=sorted(set(blockers)),
        warnings=_warnings(status),
        checked_rules=_checked_rules(),
    )


def _write_report(result: WorkbenchBehaviorValidationResult) -> None:
    """Write behavior validation evidence inside the project-support Preview root."""
    path = Path(result.report_path).resolve()
    root = Path(result.preview_root).resolve()
    if not _is_relative_to(path, root):
        raise RuntimeError("Behavior validation report outside preview root: " + str(path))
    root.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _preview_root(project_root: Path, apply_result: GuardedSourceApplyResult | None) -> Path:
    """Return the governed preview root for behavior validation evidence."""
    if apply_result and apply_result.preview_root:
        return Path(apply_result.preview_root).resolve()
    return _daily_preview_root(project_root)


def _daily_preview_root(project_root: Path) -> Path:
    """Return dynamic selected-project Preview support root."""
    return preview_runs_root(project_root)


def _is_python_executable(name: str) -> bool:
    """Return True for normal Python launcher names."""
    return name.startswith("python") or name in {"py", "py.exe"}


def _protected_parts(path: Path) -> list[str]:
    """Return protected path parts found in a path."""
    return [part for part in path.resolve().parts if part in _PROTECTED_PARTS]


def _is_relative_to(path: Path, root: Path) -> bool:
    """Return True if path is inside root after resolution."""
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _excerpt(text: str, limit: int = 4000) -> str:
    """Return a bounded command-output excerpt."""
    if len(text) <= limit:
        return text
    return text[:limit] + "\n...<truncated>"


def _checked_rules() -> list[str]:
    """Return stable checked-rule labels."""
    return [
        "guarded_source_apply_succeeded_before_behavior_validation",
        "post_apply_structural_validation_required",
        "test_command_allowlisted",
        "test_command_runs_without_shell",
        "behavior_validation_claimed_only_on_zero_exit",
        "behavior_report_written_under_daily_work_preview_root",
        "import_rewrite_disabled",
    ]


def _warnings(status: str) -> list[str]:
    """Return stable behavior-validation warnings."""
    warnings = ["IMPORT_MIGRATION_REMAINS_PREVIEW_ONLY"]
    if status == "behavior_validation_not_run":
        warnings.append("BEHAVIOR_VALIDATION_OPTIONAL_AND_NOT_RUN")
    if status == "behavior_validation_failed":
        warnings.append("BEHAVIOR_TEST_COMMAND_FAILED")
    if status == "blocked":
        warnings.append("BEHAVIOR_VALIDATION_BLOCKED")
    return warnings
