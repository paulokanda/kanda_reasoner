"""Build validation-state metadata for one reasoner context bundle."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping, Sequence

from .json_writer import write_json_atomic
from .output_paths import bundle_artifact_paths
from .project_context import resolve_project_context
from .schema_models import ProjectContext

__all__ = [
    "DEFAULT_VALIDATION_COMMANDS",
    "build_validation_state_payload",
    "run_validation_commands",
    "write_validation_state_json",
]

SCHEMA_VERSION = 1
BUNDLE_KIND = "validation_state"
GENERATOR_NAME = "reasoner_context_bundle.validation_state_builder"
GENERATOR_VERSION = "1.2.0"

DEFAULT_VALIDATION_COMMANDS = (
    {
        "name": "architecture_validate",
        "command": (
            "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py "
            "--root <PROJECT_ROOT> --validate"
        ),
        "argv": (
            "kanda_reasoner_app/manage_architecture/manage_architecture.py",
            "--root",
            "<PROJECT_ROOT>",
            "--validate",
        ),
        "required_for_freeze": True,
        "run_by_default": True,
    },
    {
        "name": "architecture_diff",
        "command": (
            "python kanda_reasoner_app\\manage_architecture\\manage_architecture.py "
            "--root <PROJECT_ROOT> --diff"
        ),
        "argv": (
            "kanda_reasoner_app/manage_architecture/manage_architecture.py",
            "--root",
            "<PROJECT_ROOT>",
            "--diff",
        ),
        "required_for_freeze": False,
        "run_by_default": False,
    },
    {
        "name": "workflow_validate",
        "command": (
            "python kanda_reasoner_app\\manage_workflows\\manage_workflows.py "
            "--root <PROJECT_ROOT> --validate"
        ),
        "argv": (
            "kanda_reasoner_app/manage_workflows/manage_workflows.py",
            "--root",
            "<PROJECT_ROOT>",
            "--validate",
        ),
        "required_for_freeze": True,
        "run_by_default": True,
    },
)

_ALLOWED_STATUSES = {"pass", "fail", "not_run", "stale", "unknown"}
_TAIL_LIMIT = 6000


def _utc_now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _context(project: str | Path | ProjectContext) -> ProjectContext:
    if isinstance(project, ProjectContext):
        return project
    return resolve_project_context(project)


def _clip_text(value: object) -> str:
    text = "" if value is None else str(value)
    if len(text) <= _TAIL_LIMIT:
        return text
    return text[-_TAIL_LIMIT:]


def _coerce_exit_code(value: object) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_status(value: object, ran: bool, exit_code: int | None) -> str:
    status = "" if value is None else str(value).strip().lower()
    if status in _ALLOWED_STATUSES:
        return status
    if not ran:
        return "not_run"
    if exit_code == 0:
        return "pass"
    if exit_code is not None:
        return "fail"
    return "unknown"


def _normalize_command_result(
    command_spec: Mapping[str, object],
    result: Mapping[str, object] | None,
) -> dict[str, Any]:
    result_data: Mapping[str, object] = result or {}
    ran = bool(result_data.get("ran", False))
    exit_code = _coerce_exit_code(result_data.get("exit_code"))
    status = _normalize_status(result_data.get("status"), ran, exit_code)
    summary = str(result_data.get("summary") or "")
    if not summary:
        if status == "not_run":
            summary = "Not run during this bundle generation."
        elif status == "pass":
            summary = "Validation command passed."
        elif status == "fail":
            summary = "Validation command failed."
        else:
            summary = "Validation status is unknown."

    record = {
        "name": str(command_spec["name"]),
        "command": str(command_spec["command"]),
        "required_for_freeze": bool(command_spec.get("required_for_freeze", False)),
        "ran": ran,
        "exit_code": exit_code,
        "status": status,
        "summary": summary,
        "stdout_tail": _clip_text(result_data.get("stdout_tail")),
        "stderr_tail": _clip_text(result_data.get("stderr_tail")),
    }
    captured_at = result_data.get("captured_at_utc")
    if captured_at:
        record["captured_at_utc"] = str(captured_at)
    return record


def _normalize_results(
    command_results: Mapping[str, Mapping[str, object]] | None,
) -> list[dict[str, Any]]:
    by_name = command_results or {}
    normalized: list[dict[str, Any]] = []
    for command_spec in DEFAULT_VALIDATION_COMMANDS:
        name = str(command_spec["name"])
        normalized.append(_normalize_command_result(command_spec, by_name.get(name)))
    return normalized


def _overall_status(commands: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = [str(item.get("status", "unknown")) for item in commands]
    required = [item for item in commands if item.get("required_for_freeze")]
    optional = [item for item in commands if not item.get("required_for_freeze")]
    required_statuses = [str(item.get("status", "unknown")) for item in required]
    optional_statuses = [str(item.get("status", "unknown")) for item in optional]

    required_pass = bool(required) and all(status == "pass" for status in required_statuses)
    if any(status == "fail" for status in statuses):
        status = "fail"
    elif required_pass and all(status in {"pass", "not_run"} for status in optional_statuses):
        status = "pass"
    elif all(status == "pass" for status in statuses):
        status = "pass"
    elif any(status == "pass" for status in statuses):
        status = "partial"
    elif all(status == "not_run" for status in statuses):
        status = "not_run"
    else:
        status = "unknown"

    return {
        "status": status,
        "required_status": "pass" if required_pass else "not_pass",
        "freeze_ready_required_commands": required_pass,
        "commands_total": len(commands),
        "commands_passed": sum(1 for item in commands if item.get("status") == "pass"),
        "commands_failed": sum(1 for item in commands if item.get("status") == "fail"),
        "commands_not_run": sum(1 for item in commands if item.get("status") == "not_run"),
    }


def _argv_for_command(command_spec: Mapping[str, object], context: ProjectContext) -> list[str]:
    argv_obj = command_spec.get("argv")
    if not isinstance(argv_obj, Sequence) or isinstance(argv_obj, (str, bytes)):
        raise ValueError("Validation command is missing argv: " + str(command_spec.get("name")))
    argv = [sys.executable]
    for part in argv_obj:
        text = str(part)
        if text == "<PROJECT_ROOT>":
            text = str(context.root)
        argv.append(text)
    return argv


def _not_run_result(command_spec: Mapping[str, object]) -> dict[str, object]:
    return {
        "ran": False,
        "exit_code": None,
        "status": "not_run",
        "summary": "Not run by the explicit validation capture command.",
        "stdout_tail": "",
        "stderr_tail": "",
    }


def _run_one_validation_command(
    command_spec: Mapping[str, object],
    context: ProjectContext,
) -> dict[str, object]:
    argv = _argv_for_command(command_spec, context)
    try:
        completed = subprocess.run(
            argv,
            cwd=str(context.root),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return {
            "ran": True,
            "exit_code": None,
            "status": "fail",
            "summary": "Validation command could not be started: " + str(exc),
            "stdout_tail": "",
            "stderr_tail": str(exc),
            "captured_at_utc": _utc_now(),
        }
    status = "pass" if completed.returncode == 0 else "fail"
    return {
        "ran": True,
        "exit_code": completed.returncode,
        "status": status,
        "summary": "Validation command passed." if status == "pass" else "Validation command failed.",
        "stdout_tail": _clip_text(completed.stdout),
        "stderr_tail": _clip_text(completed.stderr),
        "captured_at_utc": _utc_now(),
    }


def run_validation_commands(
    project: str | Path | ProjectContext,
    *,
    include_optional: bool = False,
) -> dict[str, dict[str, object]]:
    """Run local validation commands and return normalized command results.

    This function is explicit and local-only. It never contacts an AI service,
    never uses the internet, and only runs the deterministic validation commands
    declared in DEFAULT_VALIDATION_COMMANDS. Optional commands are recorded as
    not_run unless include_optional is true.
    """
    context = _context(project)
    results: dict[str, dict[str, object]] = {}
    for command_spec in DEFAULT_VALIDATION_COMMANDS:
        name = str(command_spec["name"])
        should_run = bool(command_spec.get("run_by_default", False))
        if include_optional and not should_run:
            should_run = True
        if should_run:
            results[name] = _run_one_validation_command(command_spec, context)
        else:
            results[name] = _not_run_result(command_spec)
    return results


def build_validation_state_payload(
    project: str | Path | ProjectContext,
    command_results: Mapping[str, Mapping[str, object]] | None = None,
    *,
    commands_run_by_bundle: bool = False,
) -> dict[str, Any]:
    """Build validation-state JSON without false validation claims.

    The caller may provide current command results. When no results are provided,
    commands are recorded as not_run. If commands_run_by_bundle is true, the
    payload states that local deterministic validation commands were run by this
    bundle flow.
    """
    context = _context(project)
    commands = _normalize_results(command_results)
    if commands_run_by_bundle:
        mode = "local_commands_run"
    elif command_results:
        mode = "provided_results"
    else:
        mode = "provided_results_or_not_run"
    return {
        "schema_version": SCHEMA_VERSION,
        "bundle_kind": BUNDLE_KIND,
        "generator": {
            "name": GENERATOR_NAME,
            "version": GENERATOR_VERSION,
        },
        "generated_at_utc": _utc_now(),
        "project": {
            "project_slug": context.project_slug,
            "project_root_marker": "<PROJECT_ROOT>",
            "evidence_root_relative": "show_project_to_AI",
            "json_complete_relative": "show_project_to_AI/second_prompt_files",
        },
        "capture_mode": {
            "mode": mode,
            "runs_commands": commands_run_by_bundle,
            "internet_or_ai_contact": False,
            "honesty_policy": "Do not claim validation passed unless current results were provided or locally captured.",
        },
        "overall": _overall_status(commands),
        "commands": commands,
    }


def write_validation_state_json(
    project: str | Path | ProjectContext,
    command_results: Mapping[str, Mapping[str, object]] | None = None,
    *,
    commands_run_by_bundle: bool = False,
) -> Path:
    """Write <project_slug>__validation_state.json for one project."""
    context = _context(project)
    paths = bundle_artifact_paths(context)
    payload = build_validation_state_payload(
        context,
        command_results=command_results,
        commands_run_by_bundle=commands_run_by_bundle,
    )
    return write_json_atomic(paths.validation_state_json, payload)
