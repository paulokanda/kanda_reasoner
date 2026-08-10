# project-path: tools/
# validate_fire_shield_manage_workflows_command_execution_isolation_v2d.py
"""Validate OS-isolated Manage Workflows structured command execution v2d."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import sys
import tempfile
import venv
from pathlib import Path
from typing import Any

FEATURE_ID = (
    "kanda-reasoner-fire-shield-manage-workflows-command-execution-isolation-v2d"
)


def require(condition: bool, marker: str) -> None:
    """Print one PASS marker or fail closed."""
    if not condition:
        raise RuntimeError(marker + ": FAIL")
    print(marker + ": PASS")


def _sha(path: Path) -> str:
    """Return SHA-256 for one file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _anchor_validator_import_root(root: Path) -> None:
    """Make validator-owned KANDA imports independent of script location."""
    root_text = str(root)
    remaining: list[str] = []
    for item in sys.path:
        try:
            same_root = Path(item or ".").resolve() == root
        except OSError:
            same_root = False
        if not same_root:
            remaining.append(item)
    sys.path[:] = [root_text, *remaining]
    require(
        Path(sys.path[0]).resolve() == root,
        "OS_FIRE_SHIELD_V2D_VALIDATOR_PROJECT_ROOT_IMPORT_ANCHOR",
    )
    __import__("kanda_reasoner_app")
    print("OS_FIRE_SHIELD_V2D_KANDA_PACKAGE_IMPORT: PASS")


def _called_names(path: Path) -> set[str]:
    """Return dotted names invoked by AST calls outside string constants."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        target = node.func
        parts: list[str] = []
        while isinstance(target, ast.Attribute):
            parts.append(target.attr)
            target = target.value
        if isinstance(target, ast.Name):
            parts.append(target.id)
        if parts:
            names.add(".".join(reversed(parts)))
    return names


def _static_validation(root: Path) -> None:
    """Validate v2d ownership, routing, and frozen-path contracts."""
    require("json" in globals(), "OS_FIRE_SHIELD_V2DR5_DIAGNOSTIC_JSON_IMPORT")
    package = root / "kanda_reasoner_app/manage_workflows"
    owner = package / "_workflow_command_isolation.py"
    cli = package / "manage_workflows_help/workflow_cli.py"
    frozen_command = package / "manage_workflows_help/workflow_command_runner.py"
    frozen_test = package / "manage_workflows_help/workflow_test_runner.py"
    frozen_runtime = package / "manage_workflows_help/workflow_python_runtime.py"

    owner_text = owner.read_text(encoding="utf-8")
    cli_text = cli.read_text(encoding="utf-8")
    calls = _called_names(owner)
    owner_tree = ast.parse(owner_text)
    top_help_imports = [
        node
        for node in owner_tree.body
        if isinstance(node, ast.ImportFrom)
        and str(node.module or "").startswith("manage_workflows_help")
    ]
    require(
        not top_help_imports,
        "OS_FIRE_SHIELD_V2DR2_NO_HELP_PACKAGE_IMPORT_AT_MODULE_INIT",
    )

    import importlib

    helper_facade = importlib.import_module(
        "kanda_reasoner_app.manage_workflows.manage_workflows_help"
    )
    isolation_owner = importlib.import_module(
        "kanda_reasoner_app.manage_workflows._workflow_command_isolation"
    )
    require(
        callable(getattr(helper_facade, "validate_project", None))
        and callable(getattr(isolation_owner, "command_list_results", None)),
        "OS_FIRE_SHIELD_V2DR2_IMPORT_CYCLE_BROKEN",
    )

    require(
        (
            "from .._workflow_command_isolation import (\n"
            "    command_list_results,"
        )
        in cli_text,
        "OS_FIRE_SHIELD_V2D_CLI_USES_ISOLATED_COMMAND_OWNER",
    )
    require(
        "command_list_results," not in cli_text.split(
            "from .workflow_command_runner import (", 1
        )[1].split(")", 1)[0],
        "OS_FIRE_SHIELD_V2D_CLI_NO_LEGACY_COMMAND_IMPORT",
    )
    require(
        "run_project_python_probe(" in owner_text,
        "OS_FIRE_SHIELD_V2D_FROZEN_V2B_RUNNER_REUSED",
    )
    require(
        "SHELL_STRING_DENIED_REQUIRE_ARGS" in owner_text,
        "OS_FIRE_SHIELD_V2D_EXTERNAL_SHELL_STRING_FAIL_CLOSED",
    )
    require(
        "V2D_COMMAND_CWD_OUTSIDE_PROJECT" in owner_text,
        "OS_FIRE_SHIELD_V2D_EXTERNAL_CWD_ESCAPE_FAIL_CLOSED",
    )
    require(
        "COMMAND_CWD_DENIED" in owner_text
        and "Fire Shield v2d denied command configuration:" in owner_text,
        "OS_FIRE_SHIELD_V2DR3_CWD_DENIAL_NORMALIZED_CHECK_RESULT",
    )
    require(
        "subprocess.run" not in calls,
        "OS_FIRE_SHIELD_V2D_NO_HOST_DIRECT_SUBPROCESS_RUN",
    )
    require(
        "shell=True" not in owner_text,
        "OS_FIRE_SHIELD_V2D_NO_HOST_SHELL_TRUE",
    )
    require(
        "_legacy_command_list_results(" in owner_text,
        "OS_FIRE_SHIELD_V2D_SELF_HOST_LEGACY_BEHAVIOR_PRESERVED",
    )
    require(
        "EXTERNAL_STRUCTURED_ARGV_ISOLATED" in owner_text,
        "OS_FIRE_SHIELD_V2D_EXTERNAL_STRUCTURED_ARGV_MODE",
    )
    require(
        "E:\\" not in owner_text and "E:\\" not in cli_text,
        "OS_FIRE_SHIELD_V2D_NO_FIXED_INSTALL_DRIVE",
    )
    require(
        len(owner_text.splitlines()) <= 500,
        "OS_FIRE_SHIELD_V2D_MAX500_COMMAND_ISOLATION_OWNER",
    )
    require(
        len(cli_text.splitlines()) <= 500,
        "OS_FIRE_SHIELD_V2D_MAX500_WORKFLOW_CLI",
    )
    require(
        all(ord(ch) < 128 for ch in owner_text + cli_text),
        "OS_FIRE_SHIELD_V2D_ASCII_TOUCHED_MODULES",
    )

    frozen_hashes = {
        frozen_command: (
            "fa0e990fc43eb5a3943f3f2d6f30a1c71b4960593df1d75b367430cf45a4e412"
        ),
        frozen_test: "d1cace649e9548b4e029c7f915888f2a212944db1c5cd2ed3b48362141faf9ee",
        frozen_runtime: (
            "a969b6024b4e2abc949a5bbd88b67794890173cca7b3f16ad14d3e3208dbd19a"
        ),
    }
    require(
        all(
            path.is_file() and _sha(path) == expected
            for path, expected in frozen_hashes.items()
        ),
        "OS_FIRE_SHIELD_V2D_FROZEN_V2B_V2C_COMMAND_PATHS_UNCHANGED",
    )
    print("OS_FIRE_SHIELD_V2D_STATIC_VALIDATION: PASS")


def _fixture_python(fixture_root: Path) -> Path:
    """Create one no-network Windows Project virtual environment."""
    venv.EnvBuilder(with_pip=False, clear=True).create(fixture_root / ".venv")
    python = fixture_root / ".venv" / "Scripts" / "python.exe"
    require(python.is_file(), "OS_FIRE_SHIELD_V2D_FIXTURE_PROJECT_PYTHON")
    return python.resolve()


def _write_cmd_fixture(fixture: Path) -> None:
    """Write a structured non-Python child command boundary probe."""
    script = r'''@echo off
setlocal

type "%CD%\allowed.txt" >nul 2>&1
if errorlevel 1 (echo KANDA_V2D_PROJECT_READ=0) else (echo KANDA_V2D_PROJECT_READ=1)

>"%CD%\blocked_cmd.txt" echo BAD 2>nul
if exist "%CD%\blocked_cmd.txt" (
  echo KANDA_V2D_PROJECT_WRITE_DENIED=0
) else (
  echo KANDA_V2D_PROJECT_WRITE_DENIED=1
)

type "%KANDA_V2D_TOOL_PROBE%" >nul 2>&1
if errorlevel 1 (
  echo KANDA_V2D_TOOL_READ_DENIED=1
) else (
  echo KANDA_V2D_TOOL_READ_DENIED=0
)

>"%TEMP%\v2d_cmd.txt" echo OK 2>nul
if exist "%TEMP%\v2d_cmd.txt" (
  echo KANDA_V2D_TRANSIENT_WRITE=1
) else (
  echo KANDA_V2D_TRANSIENT_WRITE=0
)

exit /b 0
'''
    (fixture / "boundary_v2d.cmd").write_text(script, encoding="ascii")


def _source_snapshot(fixture: Path) -> dict[str, str]:
    """Hash fixture source while excluding the Project virtual environment."""
    result: dict[str, str] = {}
    for path in sorted(fixture.rglob("*")):
        if not path.is_file() or ".venv" in path.parts:
            continue
        result[path.relative_to(fixture).as_posix()] = _sha(path)
    return result


def _has_line(text: str, line: str) -> bool:
    """Return whether output contains one exact trimmed marker line."""
    return line in {item.strip() for item in text.splitlines()}


def _external_live(root: Path) -> None:
    """Exercise the actual production v2d command owner on Windows."""
    if os.name != "nt":
        raise RuntimeError("OS_FIRE_SHIELD_V2D_WINDOWS_REQUIRED")

    from kanda_reasoner_app.manage_workflows import (
        _workflow_command_isolation as isolation,
    )
    from kanda_reasoner_app.manage_workflows.manage_workflows_help import (
        workflow_python_runtime,
    )
    from kanda_reasoner_app.project_fire_shield import build_fire_shield_context
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from kanda_reasoner_app.project_support_boundary import ProjectSelectionMode

    tool_probe = root / "kanda_reasoner_app/project_fire_shield.py"
    tool_before = tool_probe.read_bytes()

    with tempfile.TemporaryDirectory(prefix="kanda_v2d_") as temp:
        temp_root = Path(temp)
        fixture = temp_root / "external_project"
        fixture.mkdir()
        (fixture / "allowed.txt").write_text("PROJECT_OK", encoding="ascii")
        project_python = _fixture_python(fixture)
        _write_cmd_fixture(fixture)

        registry_path = temp_root / "registry/projects.json"
        registry_path.parent.mkdir(parents=True)
        registry = ProjectSelectionRegistry(
            tool_source_root=root,
            registry_path=registry_path,
        )
        registry.register_explicit_selection(
            fixture,
            ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
        )

        def injected_context(project_root, *, phase, operation_id):
            return build_fire_shield_context(
                project_root,
                phase=phase,
                operation_id=operation_id,
                tool_source_root=root,
                registry_path=registry_path,
            )

        def injected_probe(project_root, python_args, **kwargs):
            kwargs["tool_source_root"] = root
            kwargs["registry_path"] = registry_path
            return workflow_python_runtime.run_project_python_probe(
                project_root,
                python_args,
                **kwargs,
            )

        isolation.build_fire_shield_context = injected_context
        isolation._run_project_python_probe = injected_probe
        require(
            isolation._run_project_python_probe is injected_probe,
            "OS_FIRE_SHIELD_V2DR4_VALIDATOR_PROBE_ADAPTER_INJECTION",
        )
        os.environ["KANDA_V2D_TOOL_PROBE"] = str(tool_probe)
        before = _source_snapshot(fixture)

        denied = isolation.command_list_results(
            category="runtime_smoke",
            cfg={"enabled": True, "commands": ["echo SHOULD_NOT_RUN > shell.txt"]},
            root=fixture,
        )[0]
        require(
            denied.status == "fail"
            and denied.details.get("fire_shield_v2d")
            == "SHELL_STRING_DENIED_REQUIRE_ARGS"
            and not (fixture / "shell.txt").exists(),
            "OS_FIRE_SHIELD_V2D_EXTERNAL_SHELL_STRING_DENIED_LIVE",
        )

        escaped = isolation.command_list_results(
            category="integration",
            cfg={
                "enabled": True,
                "commands": [
                    {
                        "name": "escape",
                        "args": ["cmd.exe", "/c", "echo BAD"],
                        "cwd": str(root),
                    }
                ],
            },
            root=fixture,
        )[0]
        require(
            escaped.status == "fail"
            and "V2D_COMMAND_CWD_OUTSIDE_PROJECT" in escaped.message,
            "OS_FIRE_SHIELD_V2D_CWD_ESCAPE_DENIED_LIVE",
        )

        fixture_token = r".\boundary_v2d.cmd"
        rendered_script = str(fixture / "boundary_v2d.cmd")
        require(
            "{root}" not in rendered_script
            and str(fixture / "boundary_v2d.cmd") in rendered_script,
            "OS_FIRE_SHIELD_V2DR1_VALIDATOR_FIXTURE_ROOT_RENDERED",
        )
        structured_argv = ["cmd.exe", "/d", "/c", fixture_token]
        require(
            structured_argv == ["cmd.exe", "/d", "/c", r".\boundary_v2d.cmd"]
            and "call " not in fixture_token.lower()
            and '"' not in fixture_token
            and "{root}" not in fixture_token,
            "OS_FIRE_SHIELD_V2DR6_VALIDATOR_RELATIVE_CMD_FIXTURE_ARGV",
        )

        result = isolation.command_list_results(
            category="runtime_smoke",
            cfg={
                "enabled": True,
                "commands": [
                    {
                        "name": "cmd boundary",
                        "args": structured_argv,
                        "expect_exit_code": 0,
                        "timeout_seconds": 30,
                        "allow_error_output": True,
                    }
                ],
            },
            root=fixture,
        )[0]
        if result.status != "pass":
            print(
                "OS_FIRE_SHIELD_V2DR4_STRUCTURED_CMD_DIAGNOSTIC="
                + json.dumps(
                    {
                        "status": result.status,
                        "message": result.message,
                        "details": result.details,
                    },
                    sort_keys=True,
                    default=str,
                )
            )
        require(result.status == "pass", "OS_FIRE_SHIELD_V2D_STRUCTURED_CMD_EXIT_ZERO")
        stdout = str(result.details.get("stdout") or "")
        require(
            _has_line(stdout, "KANDA_V2D_PROJECT_READ=1"),
            "OS_FIRE_SHIELD_V2D_CHILD_PROJECT_READ_ALLOWED",
        )
        require(
            _has_line(stdout, "KANDA_V2D_PROJECT_WRITE_DENIED=1"),
            "OS_FIRE_SHIELD_V2D_CHILD_PROJECT_WRITE_DENIED",
        )
        require(
            _has_line(stdout, "KANDA_V2D_TOOL_READ_DENIED=1"),
            "OS_FIRE_SHIELD_V2D_CHILD_TOOL_READ_DENIED",
        )
        require(
            _has_line(stdout, "KANDA_V2D_TRANSIENT_WRITE=1"),
            "OS_FIRE_SHIELD_V2D_CHILD_TRANSIENT_WRITE_ALLOWED",
        )
        require(
            Path(str(result.details.get("relay_python") or "")).resolve()
            == project_python,
            "OS_FIRE_SHIELD_V2D_SELECTED_PROJECT_PYTHON_BROKER_USED",
        )
        require(
            str(result.details.get("fire_shield_v2d") or "")
            == "EXTERNAL_STRUCTURED_ARGV_ISOLATED",
            "OS_FIRE_SHIELD_V2D_EXTERNAL_STRUCTURED_ARGV_LIVE",
        )

        after = _source_snapshot(fixture)
        require(
            before == after,
            "OS_FIRE_SHIELD_V2D_EXTERNAL_PROJECT_POST_STATE_UNCHANGED",
        )
        require(
            tool_probe.read_bytes() == tool_before,
            "OS_FIRE_SHIELD_V2D_TOOL_POST_STATE_UNCHANGED",
        )

    print("OS_FIRE_SHIELD_V2D_EXTERNAL_COMMAND_EXECUTION_LIVE_VALIDATION: PASS")


def main() -> int:
    """Run static validation and optional live Windows boundary validation."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).expanduser().resolve(strict=True)
    _anchor_validator_import_root(root)
    _static_validation(root)
    if not args.static_only:
        _external_live(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
