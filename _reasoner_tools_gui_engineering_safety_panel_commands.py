# project-path: _reasoner_tools_gui_engineering_safety_panel_commands.py
"""Private command helpers for the Engineering Safety panel.

All implementation symbols in this module are private. The public GUI
contract is owned by reasoner_tools_gui_engineering_safety_panel.py.
"""

from __future__ import annotations

import contextlib as _contextlib
import io as _io
import subprocess as _subprocess
import sys as _sys
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field
from typing import Any as _Any

from _reasoner_tools_gui_engineering_safety_boundary import (
    ProjectContextUnavailable as _ProjectContextUnavailable,
    import_tool_module as _import_tool_module,
    project_command_context as _project_command_context,
    require_project_symbol as _require_project_symbol,
    tool_root as _tool_root,
)
__all__ = []

_root_resolver_module = _import_tool_module(
    "kanda_reasoner_app.project_root_resolver", "project_root_resolver"
)
_resolve_active_project_root = getattr(
    _root_resolver_module, "resolve_active_project_root", None
)
if not callable(_resolve_active_project_root):
    raise RuntimeError("TOOL_PROJECT_ROOT_RESOLVER_PUBLIC_CONTRACT_MISSING")
_tool_process_environment_module = _import_tool_module(
    "kanda_reasoner_app.tool_process_environment", "tool_process_environment"
)
_build_tool_child_environment = getattr(
    _tool_process_environment_module, "build_tool_child_environment"
)
_CLI_MODULE_PATH = "kanda_reasoner_app.safety_suite_cli.commands"
_PROJECT_CONTEXT_UNAVAILABLE = "PROJECT_CONTEXT_UNAVAILABLE"

_ROOT_COMMANDS = {
    "bom-scan",
    "shadow-audit",
    "shadow-plan",
    "facade-fix-plan",
    "push-plan",
    "ruff-quality",
}


class _PanelCommandArgs(list):
    """Raw CLI args that also compare equal to the legacy display form."""

    def __init__(self, raw_args: list[str], display_args: list[str]) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        raw_args : list[str]
            The raw args value.
        display_args : list[str]
            The display args value.
        """
        
        super().__init__(raw_args)
        self._display_args = list(display_args)

    @property
    def display_args(self) -> list[str]:
        """Return the legacy display command representation."""
        return list(self._display_args)

    def __iter__(self):
        """Support iter behavior.
        """
        
        return iter(self._display_args)

    def __eq__(self, other: object) -> bool:
        """Support eq behavior.
        
        Parameters
        ----------
        other : object
            The comparison value.
        
        Returns
        -------
        bool
            True if the condition is met; otherwise, False.
        """
        
        if isinstance(other, list) and other == self._display_args:
            return True
        return super().__eq__(other)


@_dataclass
class _PanelCommandResult:
    """Internal command result used by the public panel wrapper."""

    command_name: str
    stdout: str = ""
    stderr: str = ""
    status_code: int = 0
    extra: dict[str, _Any] = _field(default_factory=dict)

    @property
    def status(self) -> int:
        """Return the numeric status expected by existing panel tests."""
        return self.status_code

    @property
    def success(self) -> bool:
        """Return True when the command completed with status code 0."""
        return self.status_code == 0


def _root_value(project_root: object | None = None) -> str:
    """Return the project root string used for root-aware commands."""
    if project_root is None:
        return str(_resolve_active_project_root())
    return str(_resolve_active_project_root(project_root))


def _build_display_command(command_name: str) -> list[str]:
    """Build the legacy display command for GUI logs."""
    return ["python", "-m", _CLI_MODULE_PATH, command_name]


def _build_cli_args(command_name: str, project_root: object | None = None) -> list[str]:
    """Build runnable CLI arguments without borrowing Tool-specific Project targets."""
    root = _root_value(project_root)

    if command_name == "list-tools":
        return ["list-tools"]
    if command_name == "evidence-freshness":
        return ["evidence-freshness", "--root", root]
    if command_name in _ROOT_COMMANDS:
        return [command_name, "--root", root]
    if command_name == "crash-triage":
        return ["crash-triage", "--root", root]

    context = _project_command_context(root)

    if command_name == "stack-brief":
        return [
            "stack-brief", "--runtime", "Active Project: " + context.project_name,
            "--runtime", "Project root: " + str(context.root),
        ]
    if command_name == "atlas-report":
        args = [
            "atlas-report", "--root", root,
            "--query", "Complete Engineering Review project-scoped Symbol Atlas report.",
            "--target", context.target,
            "--task", "Review ownership and related source only inside the active Project.",
        ]
        if context.symbol:
            args.extend(["--symbol", context.symbol])
        return args
    if command_name in {"find-symbol", "find-owner"}:
        return [
            command_name, "--root", root, "--symbol",
            _require_project_symbol(context), "--exact",
        ]
    if command_name in {"facade-owner", "main-helpers", "related-files"}:
        return [command_name, "--root", root, "--target", context.target]
    if command_name == "pre-patch-gate":
        args = [
            "pre-patch-gate", "--root", root, "--target", context.target,
            "--task", "Review active-Project ownership before any source patch.",
        ]
        if context.symbol:
            args.extend(["--symbol", context.symbol, "--exact"])
        return args
    if command_name == "risk-radar":
        return [
            "risk-radar", "--root", root, "--changed-file", context.target,
            "--evidence", "Complete Engineering Review project-derived target seed.",
        ]
    if command_name == "refactor-playbook":
        return [
            "refactor-playbook", "--root", root, "--target", context.target,
            "--goal", "Review a project-owned target without changing backend logic.",
        ]
    if command_name == "release-notes":
        return [
            "release-notes", "--bundle-name", context.project_name + " Complete Engineering Review",
            "--title", context.project_name + " engineering review draft",
            "--summary", "Project-scoped draft derived from the active Project only.",
            "--status", "draft", "--changed-file", context.target,
        ]
    if command_name in {"property-test", "api-contract"}:
        symbol = _require_project_symbol(context)
        args = [command_name, "--module", context.module, "--function", symbol]
        if command_name == "property-test":
            args.extend([
                "--property",
                "Project-owned function preserves its explicit input/output contract.",
            ])
        return args
    return [command_name, "--root", root]


def _build_panel_command(command_name: str, project_root: object | None = None) -> _PanelCommandArgs:
    """Build a command object satisfying legacy display and raw CLI tests."""
    raw_args = _build_cli_args(command_name, project_root)
    display_args = _build_display_command(command_name)
    return _PanelCommandArgs(raw_args, display_args)


def _coerce_status_code(value: object) -> int:
    """Convert common CLI return values to an integer process status."""
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    status = getattr(value, "status_code", None)
    if isinstance(status, int):
        return status
    status = getattr(value, "status", None)
    if isinstance(status, int):
        return status
    return 0


def _run_cli_in_process(args: list[str]) -> _PanelCommandResult:
    """Run the safety-suite CLI in process and capture stdout/stderr."""
    stdout_buffer = _io.StringIO()
    stderr_buffer = _io.StringIO()
    status_code = 0

    with _contextlib.redirect_stdout(stdout_buffer), _contextlib.redirect_stderr(stderr_buffer):
        try:
            module = _import_tool_module(_CLI_MODULE_PATH, "safety_suite_cli.commands")
            main_func = getattr(module, "main", None)
            if main_func is None:
                raise AttributeError("safety_suite_cli.commands has no main function")
            try:
                result = main_func(args)
            except TypeError:
                old_argv = list(_sys.argv)
                try:
                    _sys.argv = ["safety-suite-cli", *args]
                    result = main_func()
                finally:
                    _sys.argv = old_argv
            status_code = _coerce_status_code(result)
        except SystemExit as exc:
            status_code = _coerce_status_code(exc.code)
        except Exception as exc:  # noqa: BLE001
            stderr_buffer.write(f"ERROR: {exc}\n")
            status_code = 1

    return _PanelCommandResult(
        command_name=args[0] if args else "",
        stdout=stdout_buffer.getvalue(),
        stderr=stderr_buffer.getvalue(),
        status_code=status_code,
    )


def _run_cli_subprocess(args: list[str]) -> _PanelCommandResult:
    """Run the safety-suite CLI as a fallback subprocess."""
    command = [_sys.executable, "-m", _CLI_MODULE_PATH, *args]
    try:
        env = _build_tool_child_environment()
        completed = _subprocess.run(
            command, capture_output=True, text=True, check=False,
            cwd=str(_tool_root()), env=env,
        )
        return _PanelCommandResult(
            command_name=args[0] if args else "",
            stdout=completed.stdout or "",
            stderr=completed.stderr or "",
            status_code=int(completed.returncode),
        )
    except Exception as exc:  # noqa: BLE001
        return _PanelCommandResult(
            command_name=args[0] if args else "",
            stderr=f"ERROR: {exc}\n",
            status_code=1,
        )



def _tool_execution_provider_command(kind: str, project_root: object | None = None) -> str:
    """Return an explicit Tool-owned validator command targeting the active Project."""
    root = _root_value(project_root)
    relative = {
        "architecture": "kanda_reasoner_app/manage_architecture/manage_architecture.py",
        "workflows": "kanda_reasoner_app/manage_workflows/manage_workflows.py",
    }.get(kind)
    if relative is None:
        raise RuntimeError("UNKNOWN_TOOL_EXECUTION_PROVIDER_COMMAND:" + str(kind))
    script = (_tool_root() / relative).resolve(strict=False)
    return (
        '[KANDA TOOL EXECUTION PROVIDER] "'
        + str(_sys.executable)
        + '" "'
        + str(script)
        + '" --root "'
        + str(root)
        + '" --validate'
    )


def _shield_external_project_guidance(
    text: str,
    project_root: object | None = None,
) -> str:
    """Rewrite ambiguous Tool-relative guidance at the Tool/Project boundary."""
    if not text:
        return text
    root = _root_value(project_root)

    architecture_needles = (
        r"python kanda_reasoner_app\manage_architecture\manage_architecture.py",
        "python kanda_reasoner_app/manage_architecture/manage_architecture.py",
    )
    workflow_needles = (
        r"python kanda_reasoner_app\manage_workflows\manage_workflows.py",
        "python kanda_reasoner_app/manage_workflows/manage_workflows.py",
    )
    smoke_needles = (
        'python -c "import kanda_reasoner_app; import reasoner_tools_gui; print(\'import smoke ok\')"',
        "python -c 'import kanda_reasoner_app; import reasoner_tools_gui; print(\"import smoke ok\")'",
    )

    def replace_from(line: str, needles: tuple[str, ...], replacement: str) -> str:
        positions = [line.find(needle) for needle in needles if needle in line]
        if not positions:
            return line
        return line[: min(positions)] + replacement

    rewritten: list[str] = []
    architecture = _tool_execution_provider_command("architecture", root)
    workflows = _tool_execution_provider_command("workflows", root)
    smoke = (
        "[KANDA TOOL EXECUTION PROVIDER] Tool import smoke is internal to "
        "KANDA Reasoner and is not emitted as a Project-local validation command."
    )
    for line in text.splitlines(keepends=True):
        ending = ""
        body = line
        if body.endswith("\r\n"):
            body, ending = body[:-2], "\r\n"
        elif body.endswith("\n"):
            body, ending = body[:-1], "\n"
        body = replace_from(body, architecture_needles, architecture)
        body = replace_from(body, workflow_needles, workflows)
        body = replace_from(body, smoke_needles, smoke)
        rewritten.append(body + ending)
    return "".join(rewritten)


def _run_command(command_name: str, project_root: object | None = None) -> _PanelCommandResult:
    """Run a panel command and fail closed when no Project-owned seed exists."""
    try:
        args = _build_cli_args(command_name, project_root)
    except _ProjectContextUnavailable as exc:
        return _PanelCommandResult(
            command_name=command_name,
            stdout=(
                _PROJECT_CONTEXT_UNAVAILABLE + ": " + str(exc)
                + "\nAudit target role: ACTIVE PROJECT"
                + "\nKANDA Tool role: AUDIT EXECUTION PROVIDER ONLY\n"
            ),
            status_code=0,
            extra={
                "boundary_disposition": "NOT_RUN_NO_SAFE_PROJECT_CONTEXT",
                "args": [],
            },
        )
    result = _run_cli_in_process(args)
    if result.status_code == 1 and "has no main function" in result.stderr:
        result = _run_cli_subprocess(args)
    result.stdout = _shield_external_project_guidance(result.stdout, project_root)
    result.stderr = _shield_external_project_guidance(result.stderr, project_root)
    result.command_name = command_name
    result.extra.setdefault("args", list(args))
    result.extra.setdefault(
        "tool_project_guidance_boundary",
        "EXPLICIT_TOOL_PROVIDER" if _root_value(project_root) != str(_tool_root()) else "SELF_HOSTING",
    )
    return result
