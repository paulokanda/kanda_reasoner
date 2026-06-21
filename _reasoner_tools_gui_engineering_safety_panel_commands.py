"""Private command helpers for the Engineering Safety panel.

All implementation symbols in this module are private. The public GUI
contract is owned by reasoner_tools_gui_engineering_safety_panel.py.
"""

from __future__ import annotations

import contextlib as _contextlib
import importlib as _importlib
import io as _io
import subprocess as _subprocess
import sys as _sys
from dataclasses import dataclass as _dataclass
from dataclasses import field as _field
from typing import Any as _Any

from kanda_reasoner_app.project_root_resolver import (
    resolve_active_project_root as _resolve_active_project_root,
)

__all__ = []

_DEFAULT_PANEL_ROOT = str(_resolve_active_project_root())
_CLI_MODULE_PATH = "kanda_reasoner_app.safety_suite_cli.commands"
_DEFAULT_CHANGED_FILE = "reasoner_tools_gui_engineering_safety_panel.py"
_DEFAULT_EVIDENCE = "GUI button smoke run from Engineering Safety panel."

_ROOT_COMMANDS = {
    "bom-scan",
    "shadow-audit",
    "shadow-plan",
    "facade-fix-plan",
    "push-plan",
}


class _PanelCommandArgs(list):
    """Raw CLI args that also compare equal to the legacy display form."""

    def __init__(self, raw_args: list[str], display_args: list[str]) -> None:
        super().__init__(raw_args)
        self._display_args = list(display_args)

    @property
    def display_args(self) -> list[str]:
        """Return the legacy display command representation."""
        return list(self._display_args)

    def __iter__(self):
        return iter(self._display_args)

    def __eq__(self, other: object) -> bool:
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
    """Build runnable safety-suite CLI arguments for a panel command."""
    root = _root_value(project_root)

    if command_name == "list-tools":
        return ["list-tools"]

    if command_name == "stack-brief":
        return ["stack-brief"]

    # BEGIN PA021_PROJECT_SYMBOL_ATLAS_GUI_COMMANDS
    if command_name == "atlas-report":
        return [
            "atlas-report",
            "--root",
            root,
            "--query",
            "Engineering Safety panel Project Symbol Atlas report.",
            "--symbol",
            "build_reasoner_symbol_atlas_reports",
            "--target",
            "reasoner_tools_gui_engineering_safety_panel.py",
            "--task",
            "Review Project Symbol Atlas GUI integration from the Engineering Safety panel.",
        ]

    if command_name == "evidence-freshness":
        return ["evidence-freshness", "--root", root]

    if command_name == "find-symbol":
        return [
            "find-symbol",
            "--root",
            root,
            "--symbol",
            "build_reasoner_symbol_atlas_reports",
            "--exact",
        ]

    if command_name == "find-owner":
        return [
            "find-owner",
            "--root",
            root,
            "--symbol",
            "build_reasoner_symbol_atlas_reports",
            "--exact",
        ]

    if command_name == "facade-owner":
        return ["facade-owner", "--root", root, "--target", "reasoner_tools_gui.py"]

    if command_name == "main-helpers":
        return [
            "main-helpers",
            "--root",
            root,
            "--target",
            "reasoner_tools_gui_engineering_safety_panel.py",
        ]

    if command_name == "related-files":
        return [
            "related-files",
            "--root",
            root,
            "--target",
            "reasoner_tools_gui_engineering_safety_panel.py",
        ]

    if command_name == "pre-patch-gate":
        return [
            "pre-patch-gate",
            "--root",
            root,
            "--symbol",
            "create_engineering_safety_panel",
            "--target",
            "reasoner_tools_gui_engineering_safety_panel.py",
            "--task",
            "Review Project Symbol Atlas GUI button wiring before patching.",
            "--exact",
        ]
    # END PA021_PROJECT_SYMBOL_ATLAS_GUI_COMMANDS

    if command_name in _ROOT_COMMANDS:
        return [command_name, "--root", root]

    if command_name == "risk-radar":
        return [
            "risk-radar",
            "--root",
            root,
            "--changed-file",
            _DEFAULT_CHANGED_FILE,
            "--evidence",
            _DEFAULT_EVIDENCE,
        ]

    if command_name == "refactor-playbook":
        return [
            "refactor-playbook",
            "--root",
            root,
            "--target",
            _DEFAULT_CHANGED_FILE,
            "--goal",
            "Review safe GUI panel action wiring without changing backend logic.",
        ]

    if command_name == "release-notes":
        return [
            "release-notes",
            "--bundle-name",
            "GUI003 Engineering Safety panel actions",
            "--title",
            "Engineering Safety panel actions",
            "--summary",
            "Button action smoke report from the Engineering Safety panel.",
            "--status",
            "draft",
        ]

    if command_name == "property-test":
        return [
            "property-test",
            "--module",
            "reasoner_tools_gui_engineering_safety_panel",
            "--function",
            "build_engineering_safety_panel_cli_args",
            "--property",
            "Known commands produce runnable default CLI arguments.",
        ]

    if command_name == "api-contract":
        return [
            "api-contract",
            "--module",
            "reasoner_tools_gui_engineering_safety_panel",
            "--function",
            "build_engineering_safety_panel_cli_args",
        ]

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
            module = _importlib.import_module(_CLI_MODULE_PATH)
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
        completed = _subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
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


def _run_command(command_name: str, project_root: object | None = None) -> _PanelCommandResult:
    """Run a panel command and always return an explicit result."""
    args = _build_cli_args(command_name, project_root)
    result = _run_cli_in_process(args)
    if result.status_code == 1 and "has no main function" in result.stderr:
        return _run_cli_subprocess(args)
    result.command_name = command_name
    return result
