#!/usr/bin/env python3
"""Validate dynamic Active-Project Python authority for Workflow Review."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import types
from pathlib import Path
from typing import Any

FEATURE_ID = "kanda-reasoner-workflow-review-dynamic-project-python-v1"

INSTALLED_HASHES = {
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_python_runtime.py":
        "6531efa9814631f9070fb141d077769534173ed86be93883ed9234f79bfc27c1",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_command_runner.py":
        "e8d27d385292c398700781715679d81bb7935d242592a92721c9d06a853eca3a",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_import_checks.py":
        "57ddede91aa1411d79898b4288e04279ed422dea1e4b13c513230498552945ff",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_generation.py":
        "686ba4905b303b487034ecbf148ebaab6b3b9aee351c9947b3668c8db2e73df4",
    "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_worker.py":
        "11eb673e2ed8ef77cf342d5b52010889516c295dd103fcec94ab0ed5ce439c9f",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help.json":
        "ced92a3fe6a115b92898180f0c3cf3ba0a970062a85a1fdf3e8f1d293bfff958",
    "WORKFLOWS.md":
        "b6681f58d927a1dbf09ec27393e2d3caea796d53a5d013cfce8634aa5b60353a",
}

PYTHON_FILES = tuple(
    path for path in INSTALLED_HASHES if path.endswith(".py")
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal_all(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            continue
        value = ast.literal_eval(node.value)
        require(isinstance(value, list), "HELPER_ALL_NOT_LIST: " + str(path))
        require(
            all(isinstance(item, str) for item in value),
            "HELPER_ALL_NON_STRING: " + str(path),
        )
        return list(value)
    return []


def load_help_manifest(root: Path) -> dict[str, Any]:
    path = root / "kanda_reasoner_app/manage_workflows/manage_workflows_help.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(payload, dict), "WORKFLOW_HELP_MANIFEST_NOT_OBJECT")
    return payload


def validate_hashes_and_compile(root: Path) -> None:
    for relative, expected in INSTALLED_HASHES.items():
        path = root / relative
        require(path.is_file(), "INSTALLED_FILE_MISSING: " + relative)
        require(sha256(path) == expected, "INSTALLED_HASH_MISMATCH: " + relative)
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_INSTALLED_HASHES: PASS")

    for relative in PYTHON_FILES:
        path = root / relative
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
        require(
            len(source.splitlines()) <= 500,
            "TOUCHED_MODULE_OVER_500_LINES: " + relative,
        )
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_COMPILE: PASS")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_MODULE_SIZE_MAX_500: PASS")


def validate_helper_manifest(root: Path) -> None:
    manifest = load_help_manifest(root)
    helper_root = root / "kanda_reasoner_app/manage_workflows/manage_workflows_help"
    helper_specs = manifest.get("helpers")
    require(isinstance(helper_specs, dict), "WORKFLOW_HELPERS_NOT_OBJECT")

    union: list[str] = []
    for helper_name in sorted(helper_specs):
        spec = helper_specs[helper_name]
        require(isinstance(spec, dict), "WORKFLOW_HELPER_SPEC_NOT_OBJECT")
        helper_path = helper_root / helper_name
        require(helper_path.is_file(), "WORKFLOW_HELPER_MISSING: " + helper_name)
        actual = literal_all(helper_path)
        declared = spec.get("exports")
        require(isinstance(declared, list), "WORKFLOW_HELPER_EXPORTS_NOT_LIST")
        require(sorted(actual) == sorted(declared), "WORKFLOW_HELPER_EXPORT_MISMATCH: " + helper_name)
        union.extend(actual)

    require(
        sorted(union) == sorted(manifest.get("exports") or []),
        "WORKFLOW_HELPER_UNION_EXPORT_MISMATCH",
    )
    runtime_spec = helper_specs.get("workflow_python_runtime.py")
    require(isinstance(runtime_spec, dict), "WORKFLOW_PYTHON_RUNTIME_MANIFEST_MISSING")
    require(
        sorted(runtime_spec.get("exports") or [])
        == ["project_python_has_module", "resolve_project_python"],
        "WORKFLOW_PYTHON_RUNTIME_MANIFEST_EXPORT_MISMATCH",
    )
    origin_all = set(manifest.get("origin_all") or [])
    require(
        not {"project_python_has_module", "resolve_project_python"} & origin_all,
        "WORKFLOW_PYTHON_RUNTIME_PROMOTED_TO_FACADE",
    )
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_HELPER_MANIFEST: PASS")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_HELPER_LOCAL_OWNERSHIP: PASS")


def canonical_imports(root: Path) -> tuple[Any, Any, Any, Any]:
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    runtime = importlib.import_module(
        "kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_python_runtime"
    )
    runner = importlib.import_module(
        "kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_command_runner"
    )
    imports = importlib.import_module(
        "kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_import_checks"
    )
    constants = importlib.import_module(
        "kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_constants"
    )
    return runtime, runner, imports, constants


def expected_project_python(root: Path) -> Path:
    windows = root / ".venv" / "Scripts" / "python.exe"
    posix = root / ".venv" / "bin" / "python"
    if windows.is_file():
        return windows.resolve()
    if posix.is_file():
        return posix.resolve()
    raise RuntimeError("ACTIVE_PROJECT_VENV_MISSING_FOR_VALIDATION")


def validate_runtime_authority(root: Path) -> None:
    runtime, runner, imports, constants = canonical_imports(root)
    expected = expected_project_python(root)
    require(runtime.resolve_project_python(root) == expected, "ACTIVE_PROJECT_PYTHON_RESOLUTION_MISMATCH")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_ACTIVE_ROOT_RESOLUTION: PASS")

    runner_text = (
        root
        / "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_command_runner.py"
    ).read_text(encoding="utf-8")
    imports_text = (
        root
        / "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_import_checks.py"
    ).read_text(encoding="utf-8")
    require("sys.executable" not in runner_text, "COMMAND_RUNNER_SYS_EXECUTABLE_REINTRODUCED")
    require("sys.executable" not in imports_text, "IMPORT_CHECK_SYS_EXECUTABLE_REINTRODUCED")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_NO_HOST_SYS_EXECUTABLE: PASS")

    replaced = runner.replace_placeholders("{python}", root=root)
    require(Path(replaced).resolve() == expected, "PYTHON_PLACEHOLDER_NOT_ACTIVE_PROJECT_VENV")
    spec = {
        "name": "dynamic-python-fixture",
        "args": ["{python}", "-c", "print('ok')"],
        "cwd": "{root}",
    }
    built = runner.build_command(
        spec,
        category="runtime_smoke",
        root=root,
        default_timeout=10,
    )
    require(Path(built[1][0]).resolve() == expected, "BUILT_COMMAND_NOT_ACTIVE_PROJECT_VENV")
    require(built[3] == root.resolve(), "BUILT_COMMAND_CWD_NOT_ACTIVE_PROJECT")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_PLACEHOLDER_AUTHORITY: PASS")

    original_executable = sys.executable
    try:
        sys.executable = str(root / "__FAKE_HOST_GLOBAL_PYTHON__.exe")
        replaced_under_fake_host = runner.replace_placeholders("{python}", root=root)
    finally:
        sys.executable = original_executable
    require(
        Path(replaced_under_fake_host).resolve() == expected,
        "HOST_INTERPRETER_LEAKED_INTO_PROJECT_PLACEHOLDER",
    )
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_HOST_SENTINEL_IGNORED: PASS")

    discovered = {"importable_modules": ["json"]}
    cfg = {
        "enabled": True,
        "include_modules": ["json"],
        "exclude_patterns": [],
        "module_limit": 1,
        "timeout_seconds": 15,
    }
    probe_results = imports.run_import_checks(root, discovered, cfg)
    require(len(probe_results) == 1, "IMPORT_PROBE_FIXTURE_RESULT_COUNT_MISMATCH")
    result = probe_results[0]
    require(result.status == "pass", "IMPORT_PROBE_FIXTURE_FAILED: " + result.message)
    require(result.command.startswith("argv="), "IMPORT_PROBE_COMMAND_NOT_ARGV_ENCODED")
    argv = json.loads(result.command[len("argv="):])
    require(isinstance(argv, list) and len(argv) == 6, "IMPORT_PROBE_ARGV_SHAPE_INVALID")
    require(Path(argv[0]).resolve() == expected, "IMPORT_PROBE_NOT_ACTIVE_PROJECT_VENV")
    require(argv[1:3] == ["-I", "-c"], "IMPORT_PROBE_FLAGS_CHANGED")
    require(argv[3] == constants.IMPORT_PROBE_CODE, "IMPORT_PROBE_LOG_CODE_NOT_EXECUTED_CODE")
    require(Path(argv[4]).resolve() == root.resolve(), "IMPORT_PROBE_ARGV_ROOT_MISMATCH")
    require(argv[5] == "json", "IMPORT_PROBE_ARGV_MODULE_MISMATCH")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_IMPORT_PROBE_ARGV_EXACT: PASS")

    with tempfile.TemporaryDirectory(prefix="kanda_workflow_missing_venv_") as temp:
        missing_root = Path(temp)
        try:
            runtime.resolve_project_python(missing_root)
        except RuntimeError as exc:
            require(
                "PROJECT_PYTHON_INTERPRETER_NOT_FOUND" in str(exc),
                "MISSING_VENV_WRONG_FAILURE",
            )
        else:
            raise RuntimeError("MISSING_VENV_DID_NOT_FAIL_CLOSED")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_MISSING_VENV_FAILS_CLOSED: PASS")

    with tempfile.TemporaryDirectory(prefix="kanda_workflow_fake_project_") as temp:
        fake_root = Path(temp)
        fake_python = fake_root / ".venv" / "Scripts" / "python.exe"
        fake_python.parent.mkdir(parents=True)
        fake_python.write_bytes(b"fixture")
        require(
            runtime.resolve_project_python(fake_root) == fake_python.resolve(),
            "FAKE_ACTIVE_PROJECT_ROOT_NOT_SELECTED",
        )
        require(
            Path(runner.replace_placeholders("{python}", root=fake_root)).resolve()
            == fake_python.resolve(),
            "FAKE_ACTIVE_PROJECT_PLACEHOLDER_NOT_SELECTED",
        )
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_EXTERNAL_ROOT_SELECTION: PASS")


def validate_worker_context(root: Path) -> None:
    qtcore = types.ModuleType("PySide6.QtCore")

    class QObject:
        pass

    class Signal:
        def __init__(self, *args: object) -> None:
            self.args = args

    qtcore.QObject = QObject
    qtcore.Signal = Signal
    pyside = types.ModuleType("PySide6")
    pyside.QtCore = qtcore
    previous_pyside = sys.modules.get("PySide6")
    previous_qtcore = sys.modules.get("PySide6.QtCore")
    sys.modules["PySide6"] = pyside
    sys.modules["PySide6.QtCore"] = qtcore
    try:
        path = (
            root
            / "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_worker.py"
        )
        spec = importlib.util.spec_from_file_location(
            "_kanda_workflow_dynamic_python_worker_fixture",
            path,
        )
        require(spec is not None and spec.loader is not None, "WORKER_SPEC_UNAVAILABLE")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        manager = root / "kanda_reasoner_app/manage_workflows/manage_workflows.py"
        context = module.build_workflow_execution_context(
            str(manager),
            str(root),
            "validate",
        )
    finally:
        if previous_pyside is None:
            sys.modules.pop("PySide6", None)
        else:
            sys.modules["PySide6"] = previous_pyside
        if previous_qtcore is None:
            sys.modules.pop("PySide6.QtCore", None)
        else:
            sys.modules["PySide6.QtCore"] = previous_qtcore

    expected = str(expected_project_python(root))
    require("Tool role: KANDA TOOL EXECUTION PROVIDER" in context, "TOOL_ROLE_CONTEXT_LOST")
    require("Active Project root: " + str(root.resolve()) in context, "PROJECT_ROOT_CONTEXT_LOST")
    require("Active Project Python: " + expected in context, "PROJECT_PYTHON_CONTEXT_MISSING")
    require("Tool/Project logical roles merged: NO" in context, "LOGICAL_ROLE_SEPARATION_CONTEXT_LOST")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_EXECUTION_CONTEXT_VISIBLE: PASS")


def validate_documentation_contract(root: Path) -> None:
    generation = (
        root
        / "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_generation.py"
    ).read_text(encoding="utf-8")
    workflows = (root / "WORKFLOWS.md").read_text(encoding="utf-8")
    expected_line = "- `{python}` => selected Active Project `.venv` Python interpreter"
    require(expected_line in generation, "WORKFLOW_GENERATOR_PYTHON_AUTHORITY_DOC_MISSING")
    require(expected_line in workflows, "WORKFLOWS_PYTHON_AUTHORITY_DOC_MISSING")
    require("{python}` => current Python executable" not in workflows, "STALE_WORKFLOWS_PYTHON_DOC_PRESENT")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_DOCUMENTATION_CONTRACT: PASS")


def validate_live_workflow(root: Path) -> None:
    project_python = expected_project_python(root)
    script = root / "kanda_reasoner_app/manage_workflows/manage_workflows.py"
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment.setdefault("QT_QPA_PLATFORM", "offscreen")
    completed = subprocess.run(
        [str(project_python), str(script), "--root", str(root), "--validate"],
        cwd=str(root),
        env=environment,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=300,
    )
    output = (completed.stdout or "") + (completed.stderr or "")
    print(output, end="" if output.endswith("\n") else "\n")
    require(completed.returncode == 0, "LIVE_WORKFLOW_VALIDATE_NONZERO")
    require("Summary:" in output, "LIVE_WORKFLOW_SUMMARY_MISSING")
    require("fail=0" in output, "LIVE_WORKFLOW_FAILURE_PRESENT")
    require("warn=0" in output, "LIVE_WORKFLOW_WARNING_PRESENT")

    command_lines = [
        line.split("command:", 1)[1].strip()
        for line in output.splitlines()
        if "command:" in line
    ]
    require(command_lines, "LIVE_WORKFLOW_COMMAND_EVIDENCE_MISSING")
    python_command_count = 0
    for command in command_lines:
        if command.startswith("argv="):
            argv = json.loads(command[len("argv="):])
            require(isinstance(argv, list) and argv, "LIVE_IMPORT_ARGV_INVALID")
            require(
                Path(str(argv[0])).resolve() == project_python,
                "LIVE_IMPORT_PROBE_WRONG_PYTHON: " + str(argv[0]),
            )
            python_command_count += 1
            continue
        if "python" in command.casefold():
            require(
                command.casefold().startswith(str(project_python).casefold()),
                "LIVE_WORKFLOW_COMMAND_WRONG_PYTHON: " + command,
            )
            python_command_count += 1
    require(python_command_count >= 7, "LIVE_PROJECT_PYTHON_COMMAND_EVIDENCE_INCOMPLETE")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_LIVE_VALIDATE: PASS")
    print("WORKFLOW_DYNAMIC_PROJECT_PYTHON_LIVE_COMMAND_AUTHORITY: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)

    validate_hashes_and_compile(root)
    validate_helper_manifest(root)
    validate_runtime_authority(root)
    validate_worker_context(root)
    validate_documentation_contract(root)
    validate_live_workflow(root)

    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
