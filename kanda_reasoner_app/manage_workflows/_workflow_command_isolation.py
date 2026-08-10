# project-path: kanda_reasoner_app/manage_workflows/_workflow_command_isolation.py
"""Isolate external-Project Manage Workflows structured commands."""

from __future__ import annotations

import json
import os
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any, Mapping, Sequence

from kanda_reasoner_app.project_fire_shield import (
    FireShieldMode,
    build_fire_shield_context,
)


__all__: list[str] = []


def _check_result(*args: Any, **kwargs: Any) -> Any:
    """Construct one frozen helper CheckResult after package initialization."""
    from .manage_workflows_help.workflow_models import CheckResult

    return CheckResult(*args, **kwargs)


def _legacy_command_list_results(**kwargs: Any) -> list[Any]:
    """Resolve the frozen legacy command owner lazily for self-hosting."""
    from .manage_workflows_help.workflow_command_runner import (
        command_list_results as owner,
    )

    return owner(**kwargs)


def _resolve_project_python(root: Path) -> Path:
    """Resolve selected-Project Python through the frozen v2b owner lazily."""
    from .manage_workflows_help.workflow_python_runtime import (
        resolve_project_python as owner,
    )

    return owner(root)


def _run_project_python_probe(*args: Any, **kwargs: Any) -> Any:
    """Run one probe through the frozen v2b owner after package initialization."""
    from .manage_workflows_help.workflow_python_runtime import (
        run_project_python_probe as owner,
    )

    return owner(*args, **kwargs)


def _validate_expected_output_files(**kwargs: Any) -> Any:
    """Call the frozen expected-file contract lazily."""
    from .manage_workflows_help.workflow_file_contract import (
        validate_expected_output_files as owner,
    )

    return owner(**kwargs)


def _validate_expected_json_files(**kwargs: Any) -> Any:
    """Call the frozen expected-JSON contract lazily."""
    from .manage_workflows_help.workflow_file_contract import (
        validate_expected_json_files as owner,
    )

    return owner(**kwargs)


def _validate_command_output_content(**kwargs: Any) -> Any:
    """Call the frozen command-output contract lazily."""
    from .manage_workflows_help.workflow_output_contract import (
        validate_command_output_content as owner,
    )

    return owner(**kwargs)

_RELAY_MARKER = "KANDA_V2D_COMMAND_RESULT="
_RELAY_CODE = r'''import json
import os
import subprocess
import sys

payload = json.loads(sys.argv[1])
result = {
    "argv": payload["argv"],
    "cwd": payload["cwd"],
    "relay_python": sys.executable,
    "returncode": 125,
    "stdout": "",
    "stderr": "",
    "launch_error": "",
}
try:
    completed = subprocess.run(
        payload["argv"],
        shell=False,
        cwd=payload["cwd"],
        env=dict(os.environ),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    result["returncode"] = completed.returncode
    result["stdout"] = completed.stdout
    result["stderr"] = completed.stderr
except Exception as exc:
    result["launch_error"] = type(exc).__name__ + ": " + str(exc)
print("KANDA_V2D_COMMAND_RESULT=" + json.dumps(result, sort_keys=True))
'''


def _replace(value: str, *, root: Path) -> str:
    """Replace the two canonical command placeholders."""
    result = value.replace("{root}", str(root))
    if "{python}" in result:
        result = result.replace("{python}", str(_resolve_project_python(root)))
    return result


def _external_context(root: Path):
    """Return the current Fire Shield context for command routing."""
    return build_fire_shield_context(
        root,
        phase="VALIDATE_READ_ONLY",
        operation_id="manage-workflows-command-v2d-" + uuid.uuid4().hex,
    )


def _contained_cwd(root: Path, raw: object) -> Path:
    """Resolve a command cwd and require external-Project containment."""
    rendered = _replace(str(raw or "{root}"), root=root)
    cwd = Path(rendered).expanduser().resolve(strict=False)
    try:
        cwd.relative_to(root)
    except ValueError as exc:
        raise RuntimeError("V2D_COMMAND_CWD_OUTSIDE_PROJECT") from exc
    return cwd


def _command_environment(
    root: Path,
    spec: Mapping[str, Any],
    extra_env: Mapping[str, str] | None,
) -> dict[str, str]:
    """Build the command environment before v2a performs final sanitization."""
    env = dict(os.environ)
    for source in (extra_env or {}, spec.get("env") or {}):
        if not isinstance(source, Mapping):
            raise TypeError("command env must be a JSON object")
        for key, value in source.items():
            env[str(key)] = _replace(str(value), root=root)
    return env


def _display(argv: Sequence[str]) -> str:
    """Render structured argv for user-facing evidence."""
    return subprocess.list2cmdline([str(part) for part in argv])


def _relay_payload(stdout: str) -> dict[str, Any]:
    """Decode exactly one isolated child result from relay stdout."""
    payloads = [
        line[len(_RELAY_MARKER) :]
        for line in stdout.splitlines()
        if line.startswith(_RELAY_MARKER)
    ]
    if len(payloads) != 1:
        raise RuntimeError("V2D_COMMAND_RELAY_PAYLOAD_COUNT_INVALID")
    value = json.loads(payloads[0])
    if not isinstance(value, dict):
        raise RuntimeError("V2D_COMMAND_RELAY_PAYLOAD_INVALID")
    return value


def _expects_output(spec: Mapping[str, Any]) -> tuple[bool, str]:
    """Return the legacy output-presence contract without private reach-in."""
    expects = any(
        bool(spec.get(key))
        for key in ("expect_output", "require_output", "expect_nonempty_output")
    )
    stream = str(
        spec.get("expected_output_stream")
        or spec.get("expect_output_stream")
        or spec.get("require_output_stream")
        or "any"
    ).strip().lower()
    if stream not in {"any", "stdout", "stderr", "both"}:
        raise ValueError(
            "expected_output_stream must be one of: any, stdout, stderr, both."
        )
    return expects, stream


def _output_present(stdout: str, stderr: str, stream: str) -> bool:
    """Return whether the required output stream has informative text."""
    if stream == "stdout":
        return bool(stdout.strip())
    if stream == "stderr":
        return bool(stderr.strip())
    if stream == "both":
        return bool(stdout.strip()) and bool(stderr.strip())
    return bool(stdout.strip() or stderr.strip())


def _file_contract(
    spec: Mapping[str, Any],
    root: Path,
) -> tuple[str | None, dict[str, Any]]:
    """Apply only public expected-file and expected-JSON contract adapters."""
    missing, too_small = _validate_expected_output_files(spec=spec, root=root)
    invalid_json, missing_keys = _validate_expected_json_files(spec=spec, root=root)
    details: dict[str, Any] = {}
    if missing:
        details["missing_expected_files"] = missing
    if too_small:
        details["undersized_expected_files"] = too_small
    if invalid_json:
        details["invalid_expected_json_files"] = invalid_json
    if missing_keys:
        details["missing_expected_json_keys"] = missing_keys
    if details:
        return "Command output file contract was not satisfied.", details
    return None, {}


def _denied_shell_result(category: str, name: str, preview: str) -> CheckResult:
    """Return fail-closed evidence for external shell-string command specs."""
    return _check_result(
        category=category,
        name=name,
        status="fail",
        message=(
            "External Project shell-string execution is denied by Fire Shield v2d; "
            "use a structured non-empty 'args' list."
        ),
        command=preview,
        details={"fire_shield_v2d": "SHELL_STRING_DENIED_REQUIRE_ARGS"},
    )


def _run_external_structured_command(
    *,
    category: str,
    spec: Mapping[str, Any],
    root: Path,
    default_timeout: int | float,
    extra_env: Mapping[str, str] | None,
) -> CheckResult:
    """Run one external-Project argv command below frozen v2b/v2a authority."""
    name = str(spec.get("name") or category + " command")
    args_raw = spec.get("args")
    if not isinstance(args_raw, list) or not args_raw:
        return _denied_shell_result(
            category,
            name,
            str(spec.get("command") or ""),
        )

    argv = [_replace(str(part), root=root) for part in args_raw]
    try:
        cwd = _contained_cwd(root, spec.get("cwd") or "{root}")
    except RuntimeError as exc:
        return _check_result(
            category=category,
            name=name,
            status="fail",
            message="Fire Shield v2d denied command configuration: " + str(exc),
            command=_display(argv),
            details={"fire_shield_v2d": "COMMAND_CWD_DENIED"},
        )
    env = _command_environment(root, spec, extra_env)
    timeout = float(spec.get("timeout_seconds", default_timeout))
    expected_code = int(spec.get("expect_exit_code", 0))
    max_seconds_raw = spec.get("max_seconds")
    max_seconds = None if max_seconds_raw is None else float(max_seconds_raw)
    expects_output, expected_stream = _expects_output(spec)
    payload = json.dumps(
        {"argv": argv, "cwd": str(cwd)},
        ensure_ascii=True,
        separators=(",", ":"),
    )

    start = time.perf_counter()
    try:
        completed = _run_project_python_probe(
            root,
            ["-I", "-c", _RELAY_CODE, payload],
            cwd=root,
            env=env,
            timeout=timeout,
        )
        relay = _relay_payload(completed.stdout)
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - start
        return _check_result(
            category=category,
            name=name,
            status="fail",
            message="Timed out after " + str(timeout) + " second(s).",
            duration_seconds=duration,
            command=_display(argv),
            details={"stdout": exc.stdout or "", "stderr": exc.stderr or ""},
        )
    except Exception as exc:
        duration = time.perf_counter() - start
        return _check_result(
            category=category,
            name=name,
            status="fail",
            message="Isolated command failed to start: " + str(exc),
            duration_seconds=duration,
            command=_display(argv),
        )

    duration = time.perf_counter() - start
    launch_error = str(relay.get("launch_error") or "")
    stdout = str(relay.get("stdout") or "")
    stderr = str(relay.get("stderr") or "")
    returncode = int(relay.get("returncode", 125))
    status = "pass"
    message = "Exit code " + str(returncode) + "."
    missing_output: dict[str, list[str]] = {}
    missing_files: dict[str, Any] = {}

    if completed.returncode != 0:
        status = "fail"
        message = "Fire Shield command relay failed with exit code " + str(
            completed.returncode
        ) + "."
    elif launch_error:
        status = "fail"
        message = "Command failed to start inside Fire Shield: " + launch_error
    elif returncode != expected_code:
        status = "fail"
        message = (
            "Expected exit code "
            + str(expected_code)
            + ", got "
            + str(returncode)
            + "."
        )
    elif max_seconds is not None and duration > max_seconds:
        status = "fail"
        message = (
            "Duration " + format(duration, ".2f") + "s exceeded budget "
            + format(max_seconds, ".2f") + "s."
        )
    elif expects_output and not _output_present(stdout, stderr, expected_stream):
        status = "fail"
        message = (
            "Command exited successfully but produced no informative "
            + expected_stream
            + " output."
        )
    else:
        output_message, missing_output = _validate_command_output_content(
            stdout=stdout,
            stderr=stderr,
            spec=spec,
        )
        if output_message is not None:
            status = "fail"
            message = output_message
        else:
            file_message, missing_files = _file_contract(spec, root)
            if file_message is not None:
                status = "fail"
                message = file_message

    return _check_result(
        category=category,
        name=name,
        status=status,
        message=message,
        duration_seconds=duration,
        command=_display(argv),
        details={
            "stdout": stdout,
            "stderr": stderr,
            "returncode": returncode,
            "cwd": str(cwd),
            "relay_python": str(relay.get("relay_python") or ""),
            "fire_shield_v2d": "EXTERNAL_STRUCTURED_ARGV_ISOLATED",
            "expect_output": expects_output,
            "expected_output_stream": expected_stream,
            "missing_output_contract": missing_output,
            "missing_file_contract": missing_files,
        },
    )


def command_list_results(
    *,
    category: str,
    cfg: dict[str, Any],
    root: Path,
    extra_env: dict[str, str] | None = None,
) -> list[CheckResult]:
    """Run workflow commands; isolate structured argv for external Projects."""
    project_root = root.expanduser().resolve()
    context = _external_context(project_root)
    if context.mode is not FireShieldMode.EXTERNAL_PROJECT:
        return _legacy_command_list_results(
            category=category,
            cfg=cfg,
            root=project_root,
            extra_env=extra_env,
        )

    if not cfg.get("enabled", True):
        return [_check_result(category, category, "skip", "Workflow disabled.")]
    commands = cfg.get("commands") or []
    if not isinstance(commands, list):
        return [_check_result(category, category, "fail", "commands must be a list.")]
    if not commands:
        note = str(cfg.get("note") or "No commands configured.")
        return [_check_result(category, category, "warn", note)]

    default_timeout = cfg.get("timeout_seconds", 300)
    results: list[CheckResult] = []
    for index, raw in enumerate(commands, start=1):
        if isinstance(raw, str):
            results.append(
                _denied_shell_result(
                    category,
                    category + " #" + str(index),
                    raw,
                )
            )
            continue
        if not isinstance(raw, Mapping):
            results.append(
                _check_result(
                    category,
                    category + " #" + str(index),
                    "fail",
                    "command spec must be a string or JSON object.",
                )
            )
            continue
        results.append(
            _run_external_structured_command(
                category=category,
                spec=raw,
                root=project_root,
                default_timeout=default_timeout,
                extra_env=extra_env,
            )
        )
    return results
