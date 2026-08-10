# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_command_runner.py
"""Own command building, execution, and test workflow execution."""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path
from typing import Any

from .workflow_file_contract import (
    validate_file_contract,
)
from .workflow_models import (
    CheckResult,
)
from .workflow_output_contract import (
    command_expects_output,
    output_contract_failure_message,
    output_contract_from_spec,
    output_requirement_is_met,
)
from .workflow_placeholder_contract import (
    placeholder_command_name,
    placeholder_command_preview,
    placeholder_contract_failure_message,
)
from .workflow_python_runtime import (
    resolve_project_python,
)
from .workflow_test_runner import (
    _run_project_tests,
)

__all__ = ["command_list_results", "run_tests"]

def replace_placeholders(value: str, *, root: Path) -> str:
    """Support replace placeholders behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    root : Path
        The root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    replaced = value.replace("{root}", str(root))
    if "{python}" in replaced:
        replaced = replaced.replace("{python}", str(resolve_project_python(root)))
    return replaced

def maybe_stringify_command(args: list[str], shell: bool) -> str:
    """Support maybe stringify command behavior.
    
    Parameters
    ----------
    args : list[str]
        The positional arguments.
    shell : bool
        The shell value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if shell:
        return args[0]
    return " ".join(args)

def build_command(
    spec: Any,
    *,
    category: str,
    root: Path,
    default_timeout: int | float,
    extra_env: dict[str, str] | None = None,
) -> tuple[
    str,
    list[str],
    bool,
    Path,
    dict[str, str],
    int | float,
    int,
    float | None,
    bool,
    str,
    dict[str, list[str]],
]:
    """Build a command.
    
    Parameters
    ----------
    spec : Any
        The spec value.
    category : str
        The category value.
    root : Path
        The root path.
    default_timeout : int | float
        The default timeout value.
    extra_env : dict[str, str] | None, optional
        The optional extra env value.
    
    Returns
    -------
    tuple[str, list[str], bool, Path, dict[str, str], int | float, int, float | None, bool, str, dict[str, list[str]]]
        The tuple of values.
    """
    
    if isinstance(spec, str):
        command = replace_placeholders(spec, root=root)
        env = dict(os.environ)
        if extra_env:
            env.update({k: replace_placeholders(v, root=root) for k, v in extra_env.items()})
        return (
            command,
            [command],
            True,
            root,
            env,
            default_timeout,
            0,
            None,
            False,
            "any",
            output_contract_from_spec(None),
        )

    if not isinstance(spec, dict):
        raise TypeError(f"{category} command spec must be a string or JSON object.")

    name = str(spec.get("name") or f"{category} command")
    cwd = Path(replace_placeholders(str(spec.get("cwd") or "{root}"), root=root)).resolve()

    env = dict(os.environ)
    env_spec = spec.get("env") or {}
    if not isinstance(env_spec, dict):
        raise TypeError(f"{category} env must be a JSON object.")
    if extra_env:
        env.update({k: replace_placeholders(v, root=root) for k, v in extra_env.items()})
    env.update({str(k): replace_placeholders(str(v), root=root) for k, v in env_spec.items()})

    timeout = spec.get("timeout_seconds", default_timeout)
    expect_exit_code = int(spec.get("expect_exit_code", 0))
    max_seconds = spec.get("max_seconds")
    if max_seconds is not None:
        max_seconds = float(max_seconds)

    expects_output, expected_output_stream = command_expects_output(spec)
    output_contract = output_contract_from_spec(spec)

    if "args" in spec:
        args_raw = spec["args"]
        if not isinstance(args_raw, list) or not args_raw:
            raise TypeError(f"{category} args must be a non-empty list.")
        args = [replace_placeholders(str(part), root=root) for part in args_raw]
        return (
            name,
            args,
            False,
            cwd,
            env,
            timeout,
            expect_exit_code,
            max_seconds,
            expects_output,
            expected_output_stream,
            output_contract,
        )

    if "command" in spec:
        command = replace_placeholders(str(spec["command"]), root=root)
        return (
            name,
            [command],
            True,
            cwd,
            env,
            timeout,
            expect_exit_code,
            max_seconds,
            expects_output,
            expected_output_stream,
            output_contract,
        )

    raise KeyError(f"{category} command spec requires 'args' or 'command'.")

def execute_command(
    *,
    category: str,
    spec: Any,
    root: Path,
    default_timeout: int | float,
    extra_env: dict[str, str] | None = None,
) -> CheckResult:
    """Support execute command behavior.
    
    Parameters
    ----------
    category : str
        The category value.
    spec : Any
        The spec value.
    root : Path
        The root path.
    default_timeout : int | float
        The default timeout value.
    extra_env : dict[str, str] | None, optional
        The optional extra env value.
    
    Returns
    -------
    CheckResult
        The check result result.
    """
    
    placeholder_message, placeholder_details = placeholder_contract_failure_message(
        spec=spec,
        extra_env=extra_env,
    )
    if placeholder_message is not None:
        return CheckResult(
            category=category,
            name=placeholder_command_name(category, spec),
            status="fail",
            message=placeholder_message,
            command=placeholder_command_preview(spec),
            details={"placeholder_contract": placeholder_details},
        )

    (
        name,
        args,
        shell,
        cwd,
        env,
        timeout,
        expect_exit_code,
        max_seconds,
        expects_output,
        expected_output_stream,
        output_contract,
    ) = build_command(
        spec,
        category=category,
        root=root,
        default_timeout=default_timeout,
        extra_env=extra_env,
    )

    start = time.perf_counter()
    try:
        completed = subprocess.run(
            args[0] if shell else args,
            shell=shell,
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - start
        return CheckResult(
            category=category,
            name=name,
            status="fail",
            message=f"Timed out after {timeout} second(s).",
            duration_seconds=duration,
            command=maybe_stringify_command(args, shell),
            details={"stdout": exc.stdout or "", "stderr": exc.stderr or ""},
        )
    except Exception as exc:
        duration = time.perf_counter() - start
        return CheckResult(
            category=category,
            name=name,
            status="fail",
            message=f"Command failed to start: {exc}",
            duration_seconds=duration,
            command=maybe_stringify_command(args, shell),
        )

    duration = time.perf_counter() - start
    status = "pass"
    message = f"Exit code {completed.returncode}."
    missing_output_contract: dict[str, list[str]] = {}
    missing_file_contract: dict[str, Any] = {}

    if completed.returncode != expect_exit_code:
        status = "fail"
        message = f"Expected exit code {expect_exit_code}, got {completed.returncode}."
    elif max_seconds is not None and duration > max_seconds:
        status = "fail"
        message = (
            f"Duration {duration:.2f}s exceeded budget {max_seconds:.2f}s."
        )
    elif expects_output and not output_requirement_is_met(
        stdout=completed.stdout,
        stderr=completed.stderr,
        expected_stream=expected_output_stream,
    ):
        status = "fail"
        message = (
            "Command exited successfully but produced no informative "
            + expected_output_stream
            + " output."
        )
    else:
        contract_message, missing_output_contract = output_contract_failure_message(
            stdout=completed.stdout,
            stderr=completed.stderr,
            contract=output_contract,
        )
        if contract_message is not None:
            status = "fail"
            message = contract_message
        else:
            file_message, missing_file_contract = validate_file_contract(
                spec=spec,
                root=root,
            )
            if file_message is not None:
                status = "fail"
                message = file_message

    return CheckResult(
        category=category,
        name=name,
        status=status,
        message=message,
        duration_seconds=duration,
        command=maybe_stringify_command(args, shell),
        details={
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "returncode": completed.returncode,
            "cwd": str(cwd),
            "expect_output": expects_output,
            "expected_output_stream": expected_output_stream,
            "missing_output_contract": missing_output_contract,
            "missing_file_contract": missing_file_contract,
        },
    )

def command_list_results(
    *,
    category: str,
    cfg: dict[str, Any],
    root: Path,
    extra_env: dict[str, str] | None = None,
) -> list[CheckResult]:
    """Support command list results behavior.
    
    Parameters
    ----------
    category : str
        The category value.
    cfg : dict[str, Any]
        The configuration data.
    root : Path
        The root path.
    extra_env : dict[str, str] | None, optional
        The optional extra env value.
    
    Returns
    -------
    list[CheckResult]
        The list of values.
    """
    
    if not cfg.get("enabled", True):
        return [CheckResult(category, category, "skip", "Workflow disabled.")]
    commands = cfg.get("commands") or []
    if not isinstance(commands, list):
        return [CheckResult(category, category, "fail", "commands must be a list.")]
    if not commands:
        note = str(cfg.get("note") or "No commands configured.")
        return [CheckResult(category, category, "warn", note)]

    default_timeout = cfg.get("timeout_seconds", 300)
    results: list[CheckResult] = []
    for index, spec in enumerate(commands, start=1):
        name = f"{category} #{index}"
        if isinstance(spec, dict) and spec.get("name"):
            name = str(spec["name"])
        result = execute_command(
            category=category,
            spec=spec if isinstance(spec, dict) else {"name": name, "command": spec},
            root=root,
            default_timeout=default_timeout,
            extra_env=extra_env,
        )
        results.append(result)
    return results

def run_tests(
    root: Path,
    discovered: dict[str, Any],
    cfg: dict[str, Any],
) -> list[CheckResult]:
    """Run Project tests through the dedicated governed test owner."""
    return _run_project_tests(root, discovered, cfg)
