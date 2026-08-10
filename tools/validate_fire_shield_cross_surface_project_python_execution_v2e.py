#!/usr/bin/env python3
"""Validate Fire Shield cross-surface external Project Python execution v2e."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import shutil
import sys
import tempfile
import uuid
import venv
from pathlib import Path

FEATURE_ID = "kanda-reasoner-fire-shield-cross-surface-project-python-execution-v2e"
TOUCHED = (
    "kanda_reasoner_app/project_os_fire_shield_worker.py",
    "kanda_reasoner_app/project_python_fire_shield.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_shadow_provenance.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_shadow_validation.py",
    "kanda_reasoner_app/manage_architecture/warning_model_test_sandbox_validation.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_behavior_validation.py",
    "kanda_reasoner_app/reasoner_context_bundle/validation_state_builder.py",
    "kanda_reasoner_app/manage_architecture/warning_model_live_audit.py",
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_shadow_backend.py",
    "kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py",
)
FROZEN = {
    "kanda_reasoner_app/project_fire_shield.py": "cd2c95b494967dce36c77ccd2f00e9da660cb8823f2e603119783bd211ac6540",
    "kanda_reasoner_app/_project_os_fire_shield_winapi.py": "e209d273cb98df65ab156649326c7271cbda8da3b2e9faa28c9bff15b000900c",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_cli.py": "b018e1076f59b74a7ec9c4a615c0053d9fc49700ec65cf1446002dc2bade364e",
    "kanda_reasoner_app/manage_workflows/_workflow_command_isolation.py": "eb2aa299164f90a4efda74637649ff1dd0d29892e8c828dc396541ef68206ecb",
    "tools/validate_fire_shield_manage_workflows_command_execution_isolation_v2d.py": "3745e3475a10ac78cbcc52e03dbd49eeabe8475f0d100f7e44edac8dff58871b",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_command_runner.py": "fa0e990fc43eb5a3943f3f2d6f30a1c71b4960593df1d75b367430cf45a4e412",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_test_runner.py": "d1cace649e9548b4e029c7f915888f2a212944db1c5cd2ed3b48362141faf9ee",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_python_runtime.py": "a969b6024b4e2abc949a5bbd88b67794890173cca7b3f16ad14d3e3208dbd19a",
    "kanda_reasoner_app/manage_workflows/manage_workflows_help.json": "28295cd247cb4e766c6664e9cca9d7f99193ad56136c61b8e41ac31cb2cde213",
}


def require(value: bool, marker: str) -> None:
    if not value:
        raise RuntimeError(marker + ": FAIL")
    print(marker + ": PASS")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def anchor(root: Path) -> None:
    root_text = str(root)
    sys.path[:] = [root_text, *[item for item in sys.path if item != root_text]]
    require(Path(sys.path[0]).resolve() == root, "OS_FIRE_SHIELD_V2E_VALIDATOR_PROJECT_ROOT_IMPORT_ANCHOR")
    __import__("kanda_reasoner_app")
    print("OS_FIRE_SHIELD_V2E_KANDA_PACKAGE_IMPORT: PASS")


def called_names(path: Path) -> set[str]:
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


def static_validation(root: Path) -> None:
    texts = {rel: (root / rel).read_text(encoding="ascii") for rel in TOUCHED}
    for rel, text in texts.items():
        compile(text, str(root / rel), "exec")
        require(len(text.splitlines()) <= 500, "OS_FIRE_SHIELD_V2E_MAX500_" + Path(rel).stem.upper())
    print("OS_FIRE_SHIELD_V2E_ASCII_AND_COMPILE: PASS")

    worker = texts[TOUCHED[0]]
    broker = texts[TOUCHED[1]]
    require(
        "active_project_support_root" in worker
        and "active_project_daily_work_root" in worker
        and "OS_FIRE_SHIELD_CWD_OUTSIDE_PROJECT_OWNED_ROOTS" in worker,
        "OS_FIRE_SHIELD_V2E_PROJECT_OWNED_CWD_EXTENSION",
    )
    require(
        "OS_FIRE_SHIELD_CWD_INSIDE_TOOL_OWNED_ROOT" in worker
        and "_winapi.acl_lease(run_cwd, sid, read_mask)" in worker,
        "OS_FIRE_SHIELD_V2E_TOOL_CWD_DENY_AND_READ_ONLY_LEASE",
    )
    require(
        "run_external_project_python_isolated(" in broker
        and "FireShieldMode.EXTERNAL_PROJECT" in broker
        and "runner = self_host_runner or subprocess.run" in broker,
        "OS_FIRE_SHIELD_V2E_PUBLIC_PROJECT_PYTHON_BROKER",
    )
    require(
        "PROJECT_PYTHON_FIRE_SHIELD_FEATURE_ID" in broker
        and FEATURE_ID in broker,
        "OS_FIRE_SHIELD_V2E_FEATURE_ID_STABLE",
    )

    routed = TOUCHED[2:8]
    for rel in routed:
        text = texts[rel]
        require(
            "run_project_python_governed(" in text,
            "OS_FIRE_SHIELD_V2E_ROUTED_" + Path(rel).stem.upper(),
        )
        calls = called_names(root / rel)
        require(
            "subprocess.run" not in calls,
            "OS_FIRE_SHIELD_V2E_NO_DIRECT_PROJECT_RUN_" + Path(rel).stem.upper(),
        )

    backend = texts[TOUCHED[8]]
    require(
        "EXTERNAL_PROJECT_GIT_WORKTREE_DISABLED_BY_FIRE_SHIELD_V2E" in backend
        and "FireShieldMode.EXTERNAL_PROJECT" in backend,
        "OS_FIRE_SHIELD_V2E_EXTERNAL_GIT_WORKTREE_DISABLED",
    )
    ruff = texts[TOUCHED[9]]
    require(
        "RUFF_EXTERNAL_EXPLICIT_COMMAND_DENIED" in ruff
        and '(sys.executable, "-I", "-m", "ruff")' in ruff
        and "tool_python_isolated_module" in ruff,
        "OS_FIRE_SHIELD_V2E_EXTERNAL_RUFF_TOOL_OWNED_ISOLATED",
    )

    joined = "\n".join(texts.values())
    require("E:\\" not in joined and "E:/" not in joined, "OS_FIRE_SHIELD_V2E_NO_FIXED_INSTALL_DRIVE")
    require(
        all((root / rel).is_file() and sha(root / rel) == expected for rel, expected in FROZEN.items()),
        "OS_FIRE_SHIELD_V2E_FROZEN_V1_V2B_V2C_V2D_AND_WINAPI_UNCHANGED",
    )
    validator_text = (
        root
        / "tools/validate_fire_shield_cross_surface_project_python_execution_v2e.py"
    ).read_text(encoding="ascii")
    require(
        "OS_FIRE_SHIELD_V2ER1_DAILY_WORK_DIAGNOSTIC=" in validator_text,
        "OS_FIRE_SHIELD_V2ER1_DAILY_WORK_DIAGNOSTIC_INSTALLED",
    )
    validator_source = (
        root
        / "tools/validate_fire_shield_cross_surface_project_python_execution_v2e.py"
    ).read_text(encoding="ascii")
    require(
        'probe = "\\n".join([' in validator_source
        and "probe = r\'\'\'import json" not in validator_source,
        "OS_FIRE_SHIELD_V2ER2_PYTHON_C_PROBE_BUILDER",
    )
    print("OS_FIRE_SHIELD_V2E_STATIC_VALIDATION: PASS")


def fixture_python(project: Path) -> Path:
    venv.EnvBuilder(with_pip=False, clear=True).create(project / ".venv")
    path = project / ".venv" / "Scripts" / "python.exe"
    require(path.is_file(), "OS_FIRE_SHIELD_V2E_FIXTURE_PROJECT_PYTHON")
    return path.resolve()


def snapshot(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not root.exists():
        return result
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".venv" not in path.parts:
            result[path.relative_to(root).as_posix()] = sha(path)
    return result


def parse_json(text: str) -> dict[str, object]:
    try:
        value = json.loads(text.strip())
    except json.JSONDecodeError as exc:
        raise RuntimeError("OS_FIRE_SHIELD_V2E_LIVE_JSON_INVALID:" + text) from exc
    if not isinstance(value, dict):
        raise RuntimeError("OS_FIRE_SHIELD_V2E_LIVE_JSON_NOT_OBJECT")
    return value


def live_windows(root: Path) -> None:
    if os.name != "nt":
        raise RuntimeError("OS_FIRE_SHIELD_V2E_WINDOWS_REQUIRED")
    from kanda_reasoner_app.project_os_fire_shield_worker import OsFireShieldError
    from kanda_reasoner_app.project_python_fire_shield import run_project_python_governed
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from kanda_reasoner_app.project_support_boundary import (
        ProjectSelectionMode,
        canonical_project_support_root,
        canonical_transient_garbage_root,
    )

    tool_probe = root / "kanda_reasoner_app/project_fire_shield.py"
    tool_before = tool_probe.read_bytes()
    support = None
    daily = None
    with tempfile.TemporaryDirectory(prefix="kanda_v2e_") as temp:
        temp_root = Path(temp)
        project = temp_root / ("external_project_" + uuid.uuid4().hex[:10])
        project.mkdir()
        (project / "project_read.txt").write_text("PROJECT_OK", encoding="ascii")
        project_python = fixture_python(project)
        registry_path = temp_root / "registry/projects.json"
        registry_path.parent.mkdir(parents=True)
        registry = ProjectSelectionRegistry(tool_source_root=root, registry_path=registry_path)
        registry.register_explicit_selection(project, ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT)

        support = canonical_project_support_root(project)
        daily = canonical_transient_garbage_root(project)
        shadow = daily / "v2e_live" / "shadow"
        support_probe = support / "v2e_live" / "support"
        shadow.mkdir(parents=True, exist_ok=False)
        support_probe.mkdir(parents=True, exist_ok=False)
        (shadow / "shadow_read.txt").write_text("SHADOW_OK", encoding="ascii")
        project_before = snapshot(project)
        shadow_before = snapshot(shadow)

        probe = "\n".join([
            "import json, os, sys",
            "from pathlib import Path",
            "def can_read(path):",
            "    try:",
            "        Path(path).read_bytes(); return True",
            "    except OSError:",
            "        return False",
            "def can_write(path):",
            "    try:",
            "        Path(path).write_text(\"BAD\", encoding=\"ascii\"); return True",
            "    except OSError:",
            "        return False",
            "tmp = Path(os.environ[\"TEMP\"]) / \"v2e_write.txt\"",
            "print(json.dumps({",
            " \"python\": sys.executable,",
            " \"project_read\": can_read(os.environ[\"KANDA_V2E_PROJECT_PROBE\"]),",
            " \"shadow_read\": can_read(Path.cwd() / \"shadow_read.txt\"),",
            " \"shadow_write\": can_write(Path.cwd() / \"blocked.txt\"),",
            " \"tool_read\": can_read(os.environ[\"KANDA_V2E_TOOL_PROBE\"]),",
            " \"transient_write\": can_write(tmp),",
            "}, sort_keys=True))",
        ])
        require(
            "\\n" not in probe and "\n" in probe,
            "OS_FIRE_SHIELD_V2ER2_PYTHON_C_PROBE_REAL_NEWLINES",
        )
        env = dict(os.environ)
        env["KANDA_V2E_PROJECT_PROBE"] = str(project / "project_read.txt")
        env["KANDA_V2E_TOOL_PROBE"] = str(tool_probe)
        result = run_project_python_governed(
            project, ["-c", probe], cwd=shadow, env=env, timeout=30,
            tool_source_root=root, registry_path=registry_path,
        )
        diagnostic = {
            "args": [str(part) for part in result.args],
            "returncode": int(result.returncode),
            "stdout": result.stdout,
            "stderr": result.stderr,
            "project_root": str(project),
            "support_root": str(support),
            "daily_root": str(daily),
            "shadow_cwd": str(shadow),
        }
        print(
            "OS_FIRE_SHIELD_V2ER1_DAILY_WORK_DIAGNOSTIC="
            + json.dumps(diagnostic, sort_keys=True)
        )
        require(
            result.returncode == 0,
            "OS_FIRE_SHIELD_V2E_DAILY_WORK_EXIT_ZERO",
        )
        payload = parse_json(result.stdout)
        require(Path(str(payload["python"])).resolve() == project_python, "OS_FIRE_SHIELD_V2E_SELECTED_PROJECT_PYTHON_USED")
        require(payload.get("project_read") is True and payload.get("shadow_read") is True, "OS_FIRE_SHIELD_V2E_PROJECT_AND_SHADOW_READ_ALLOWED")
        require(payload.get("shadow_write") is False, "OS_FIRE_SHIELD_V2E_SHADOW_WRITE_DENIED")
        require(payload.get("tool_read") is False, "OS_FIRE_SHIELD_V2E_TOOL_READ_DENIED")
        require(payload.get("transient_write") is True, "OS_FIRE_SHIELD_V2E_TRANSIENT_WRITE_ALLOWED")

        support_run = run_project_python_governed(
            project, ["-c", "import os; print(os.getcwd())"], cwd=support_probe,
            timeout=30, tool_source_root=root, registry_path=registry_path,
        )
        require(support_run.returncode == 0 and Path(support_run.stdout.strip()).resolve() == support_probe.resolve(), "OS_FIRE_SHIELD_V2E_SUPPORT_CWD_ALLOWED")

        outside = temp_root / "outside"
        outside.mkdir()
        try:
            run_project_python_governed(
                project, ["-c", "print('BAD')"], cwd=outside, timeout=10,
                tool_source_root=root, registry_path=registry_path,
            )
        except OsFireShieldError as exc:
            outside_denied = "OS_FIRE_SHIELD_CWD_OUTSIDE_PROJECT_OWNED_ROOTS" in str(exc)
        else:
            outside_denied = False
        require(outside_denied, "OS_FIRE_SHIELD_V2E_OUTSIDE_CWD_DENIED")

        try:
            run_project_python_governed(
                project, ["-c", "print('BAD')"], cwd=root, timeout=10,
                tool_source_root=root, registry_path=registry_path,
            )
        except OsFireShieldError as exc:
            tool_denied = "OS_FIRE_SHIELD_CWD_INSIDE_TOOL_OWNED_ROOT" in str(exc)
        else:
            tool_denied = False
        require(tool_denied, "OS_FIRE_SHIELD_V2E_TOOL_CWD_DENIED")
        require(project_before == snapshot(project), "OS_FIRE_SHIELD_V2E_EXTERNAL_PROJECT_POST_STATE_UNCHANGED")
        require(shadow_before == snapshot(shadow), "OS_FIRE_SHIELD_V2E_SHADOW_POST_STATE_UNCHANGED")
        require(tool_probe.read_bytes() == tool_before, "OS_FIRE_SHIELD_V2E_TOOL_POST_STATE_UNCHANGED")

        from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import workbench_shadow_backend as backend
        from kanda_reasoner_app.engineering_diagnostics.collectors import ruff_collector
        from kanda_reasoner_app.project_fire_shield import FireShieldMode
        fake = type("C", (), {"mode": FireShieldMode.EXTERNAL_PROJECT})()
        backend.build_fire_shield_context = lambda *args, **kwargs: fake
        eligibility = backend.GitWorktreeBackend().eligibility(project)
        require(not eligibility.eligible and "EXTERNAL_PROJECT_GIT_WORKTREE_DISABLED_BY_FIRE_SHIELD_V2E" in eligibility.reasons, "OS_FIRE_SHIELD_V2E_GIT_WORKTREE_EXTERNAL_LIVE_DENIED")
        ruff_collector.build_fire_shield_context = lambda *args, **kwargs: fake
        prefixes = ruff_collector._candidate_prefixes(project, None)
        require(prefixes == (((sys.executable, "-I", "-m", "ruff"), "tool_python_isolated_module"),), "OS_FIRE_SHIELD_V2E_RUFF_EXTERNAL_TOOL_PYTHON_LIVE")
        try:
            ruff_collector._candidate_prefixes(project, ["ruff.exe"])
        except ruff_collector.RuffCollectionError as exc:
            explicit_denied = "RUFF_EXTERNAL_EXPLICIT_COMMAND_DENIED" in str(exc)
        else:
            explicit_denied = False
        require(explicit_denied, "OS_FIRE_SHIELD_V2E_RUFF_EXTERNAL_EXPLICIT_DENIED_LIVE")

    for path in (support, daily):
        if path is not None:
            shutil.rmtree(path, ignore_errors=True)
    print("OS_FIRE_SHIELD_V2E_EXTERNAL_PROJECT_PYTHON_LIVE_VALIDATION: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    anchor(root)
    static_validation(root)
    if not args.static_only:
        live_windows(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
