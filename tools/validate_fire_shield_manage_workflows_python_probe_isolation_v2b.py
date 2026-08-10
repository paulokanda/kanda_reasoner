# project-path: tools/validate_fire_shield_manage_workflows_python_probe_isolation_v2b.py
"""Validate Manage Workflows Project-Python probe isolation v2b."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import venv
from pathlib import Path

FEATURE_ID = (
    "kanda-reasoner-fire-shield-manage-workflows-python-probe-isolation-v2b"
)


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker + ": FAIL")
    print(marker + ": PASS")


def _text(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding="utf-8", errors="replace")


def validate_static(root: Path) -> None:
    runtime_rel = (
        "kanda_reasoner_app/manage_workflows/manage_workflows_help/"
        "workflow_python_runtime.py"
    )
    imports_rel = (
        "kanda_reasoner_app/manage_workflows/manage_workflows_help/"
        "workflow_import_checks.py"
    )
    runtime = _text(root, runtime_rel)
    imports = _text(root, imports_rel)

    require(
        "run_external_project_python_isolated" in runtime,
        "OS_FIRE_SHIELD_V2B_EXTERNAL_WORKER_BOUND",
    )
    require(
        'phase="VALIDATE_READ_ONLY"' in runtime,
        "OS_FIRE_SHIELD_V2B_READ_ONLY_FIRE_SHIELD_PHASE",
    )
    require(
        "FireShieldMode.EXTERNAL_PROJECT" in runtime,
        "OS_FIRE_SHIELD_V2B_EXTERNAL_MODE_GATE",
    )
    require(
        "run_project_python_probe(" in runtime
        and "run_project_python_probe(" in imports,
        "OS_FIRE_SHIELD_V2B_SHARED_PROBE_RUNNER",
    )
    require(
        "subprocess.run(" not in imports,
        "OS_FIRE_SHIELD_V2B_IMPORT_PROBE_NO_DIRECT_SUBPROCESS",
    )
    require(
        "project_python_has_module" in runtime
        and "run_project_python_probe(" in runtime.split(
            "def project_python_has_module", 1
        )[1],
        "OS_FIRE_SHIELD_V2B_MODULE_PROBE_ROUTED",
    )
    require(
        "E:\\" not in runtime + imports and "E:/" not in runtime + imports,
        "OS_FIRE_SHIELD_V2B_NO_FIXED_INSTALL_DRIVE",
    )
    for rel in (runtime_rel, imports_rel):
        lines = (root / rel).read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
        require(
            len(lines) <= 500,
            "OS_FIRE_SHIELD_V2B_MAX500_" + Path(rel).stem.upper(),
        )
    print("OS_FIRE_SHIELD_V2B_STATIC_VALIDATION: PASS")



def _validate_help_manifest(root: Path) -> None:
    import ast

    manifest_path = (
        root / "kanda_reasoner_app/manage_workflows/manage_workflows_help.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    spec = manifest["helpers"]["workflow_python_runtime.py"]
    runtime_path = (
        root
        / "kanda_reasoner_app/manage_workflows/manage_workflows_help/"
        "workflow_python_runtime.py"
    )
    tree = ast.parse(runtime_path.read_text(encoding="utf-8"))
    actual: list[str] = []
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == "__all__"
            for target in node.targets
        ):
            actual = list(ast.literal_eval(node.value))
            break
    require(
        sorted(actual) == sorted(spec.get("exports") or []),
        "OS_FIRE_SHIELD_V2B_HELP_MANIFEST_EXPORT_PARITY",
    )
    require(
        "run_project_python_probe" in (manifest.get("exports") or []),
        "OS_FIRE_SHIELD_V2B_HELP_MANIFEST_AGGREGATE_EXPORT",
    )
    require(
        "run_project_python_probe" not in (manifest.get("origin_all") or []),
        "OS_FIRE_SHIELD_V2B_HELPER_LOCAL_OWNERSHIP",
    )


def _fixture_python(fixture_root: Path) -> Path:
    venv.EnvBuilder(with_pip=False, clear=True).create(fixture_root / ".venv")
    python = fixture_root / ".venv" / "Scripts" / "python.exe"
    require(python.is_file(), "OS_FIRE_SHIELD_V2B_FIXTURE_PROJECT_PYTHON")
    return python


def _external_live(root: Path) -> None:
    if os.name != "nt":
        raise RuntimeError("OS_FIRE_SHIELD_V2B_WINDOWS_REQUIRED")

    from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_python_runtime import (
        run_project_python_probe,
    )
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from kanda_reasoner_app.project_support_boundary import (
        ProjectSelectionMode,
        canonical_project_support_root,
        canonical_transient_garbage_root,
    )

    tool_probe = root / "kanda_reasoner_app" / "project_fire_shield.py"
    before = tool_probe.read_bytes()

    with tempfile.TemporaryDirectory(prefix="kanda_v2b_") as temp:
        temp_root = Path(temp)
        fixture = temp_root / "external_project"
        fixture.mkdir()
        (fixture / "allowed.txt").write_text("PROJECT_OK", encoding="ascii")
        project_python = _fixture_python(fixture)
        registry_path = temp_root / "registry" / "projects.json"
        registry_path.parent.mkdir(parents=True)
        registry = ProjectSelectionRegistry(
            tool_source_root=root,
            registry_path=registry_path,
        )
        registry.register_explicit_selection(
            fixture,
            ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
        )

        code = (
            "import json,os,sys;from pathlib import Path;"
            "p=Path(sys.argv[1]);t=Path(sys.argv[2]);"
            "d={'project_read':False,'project_write_blocked':False,"
            "'tool_read_blocked':False,'transient_write':False};"
            "d['project_read']=(p/'allowed.txt').read_text()=='PROJECT_OK';"
            "\ntry:\n (p/'blocked.txt').write_text('BAD')\n"
            "except OSError:\n d['project_write_blocked']=True\n"
            "\ntry:\n t.read_bytes()\n"
            "except OSError:\n d['tool_read_blocked']=True\n"
            "tmp=Path(os.environ['TEMP']);"
            "(tmp/'probe.txt').write_text('OK');"
            "d['transient_write']=(tmp/'probe.txt').read_text()=='OK';"
            "print(json.dumps(d,sort_keys=True))"
        )
        completed = run_project_python_probe(
            fixture,
            ["-I", "-c", code, str(fixture), str(tool_probe)],
            timeout=30,
            tool_source_root=root,
            registry_path=registry_path,
        )
        require(
            completed.returncode == 0,
            "OS_FIRE_SHIELD_V2B_EXTERNAL_PROBE_EXIT_ZERO",
        )
        payload = json.loads((completed.stdout or "{}").strip())
        require(
            payload.get("project_read") is True,
            "OS_FIRE_SHIELD_V2B_EXTERNAL_PROJECT_READ_ALLOWED",
        )
        require(
            payload.get("project_write_blocked") is True,
            "OS_FIRE_SHIELD_V2B_EXTERNAL_PROJECT_WRITE_DENIED",
        )
        require(
            payload.get("tool_read_blocked") is True,
            "OS_FIRE_SHIELD_V2B_EXTERNAL_TOOL_READ_DENIED",
        )
        require(
            payload.get("transient_write") is True,
            "OS_FIRE_SHIELD_V2B_EXTERNAL_TRANSIENT_WRITE_ALLOWED",
        )
        require(
            Path(completed.args[0]).resolve() == project_python.resolve(),
            "OS_FIRE_SHIELD_V2B_SELECTED_PROJECT_PYTHON_USED",
        )
        require(
            not (fixture / "blocked.txt").exists(),
            "OS_FIRE_SHIELD_V2B_EXTERNAL_PROJECT_POST_STATE_UNCHANGED",
        )
        transient = canonical_transient_garbage_root(fixture)
        support = canonical_project_support_root(fixture)
        if transient.exists():
            shutil.rmtree(transient)
        if support.exists():
            shutil.rmtree(support)

    require(
        tool_probe.read_bytes() == before,
        "OS_FIRE_SHIELD_V2B_TOOL_POST_STATE_UNCHANGED",
    )
    print("OS_FIRE_SHIELD_V2B_EXTERNAL_WRAPPER_LIVE_VALIDATION: PASS")



def _anchor_validator_import_root(root: Path) -> None:
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    require(
        Path(sys.path[0]).resolve() == root,
        "OS_FIRE_SHIELD_V2BR1_VALIDATOR_PROJECT_ROOT_IMPORT_ANCHOR",
    )
    try:
        __import__("kanda_reasoner_app")
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "OS_FIRE_SHIELD_V2BR1_KANDA_PACKAGE_IMPORT_FAILED"
        ) from exc
    print("OS_FIRE_SHIELD_V2BR1_KANDA_PACKAGE_IMPORT: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    _anchor_validator_import_root(root)
    validate_static(root)
    _validate_help_manifest(root)
    if not args.static_only:
        _external_live(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
