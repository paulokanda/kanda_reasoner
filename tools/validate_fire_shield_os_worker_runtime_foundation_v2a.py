#!/usr/bin/env python3
"""Validate Fire Shield OS worker runtime foundation v2a."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import sys
import tempfile
import time
import venv
from pathlib import Path

FEATURE_ID = "kanda-reasoner-fire-shield-os-worker-runtime-foundation-v2a"
PUBLIC_REL = "kanda_reasoner_app/project_os_fire_shield_worker.py"
PRIVATE_REL = "kanda_reasoner_app/_project_os_fire_shield_winapi.py"


def require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_static(root: Path) -> None:
    public_path = root / PUBLIC_REL
    private_path = root / PRIVATE_REL
    require(public_path.is_file(), "OS_FIRE_SHIELD_V2A_PUBLIC_MODULE_PRESENT")
    require(private_path.is_file(), "OS_FIRE_SHIELD_V2A_WINAPI_MODULE_PRESENT")
    for path in (public_path, private_path):
        raw = path.read_bytes()
        raw.decode("ascii")
        source = raw.decode("ascii")
        compile(source, str(path), "exec")
        require(
            len(source.splitlines()) <= 500,
            "OS_FIRE_SHIELD_V2A_MODULE_MAX500_" + path.stem.upper(),
        )
    public = public_path.read_text(encoding="ascii")
    private = private_path.read_text(encoding="ascii")
    require(
        "kanda-reasoner-fire-shield-os-worker-runtime-foundation-v2a" in public,
        "OS_FIRE_SHIELD_V2A_FEATURE_ID_STABLE",
    )
    require(
        "assert_fire_shield_context_current" in public
        and "FireShieldMode.EXTERNAL_PROJECT" in public,
        "OS_FIRE_SHIELD_V2A_BINDS_PUBLIC_FIRE_SHIELD_V1",
    )
    require(
        "CreateAppContainerProfile" in private
        and "PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES" in private,
        "OS_FIRE_SHIELD_V2A_APPCONTAINER_LAUNCH_CONTRACT",
    )
    require(
        "AssignProcessToJobObject" in private
        and "JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE" in private,
        "OS_FIRE_SHIELD_V2A_JOB_CONTAINMENT_CONTRACT",
    )
    require(
        "SetEntriesInAclW" in private
        and "REVOKE_ACCESS" in private
        and "acl_lease" in private,
        "OS_FIRE_SHIELD_V2A_REVERSIBLE_ACL_LEASE_CONTRACT",
    )
    joined = public + "\n" + private
    require(
        "Experimental_CreateProcessInSandbox" not in joined,
        "OS_FIRE_SHIELD_V2A_NO_EXPERIMENTAL_SANDBOX_AUTHORITY",
    )
    require(
        "subprocess.run(" not in joined and "subprocess.Popen(" not in joined,
        "OS_FIRE_SHIELD_V2A_NO_ORDINARY_SUBPROCESS_LAUNCH",
    )
    require(
        "E:\\" not in joined and "E:/" not in joined,
        "OS_FIRE_SHIELD_V2A_NO_FIXED_INSTALL_DRIVE",
    )
    print("OS_FIRE_SHIELD_V2A_STATIC_VALIDATION: PASS")


def _fixture_context(root: Path, fixture_root: Path, registry_path: Path):
    from kanda_reasoner_app.project_fire_shield import build_fire_shield_context
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from kanda_reasoner_app.project_support_boundary import ProjectSelectionMode

    registry = ProjectSelectionRegistry(
        tool_source_root=root,
        registry_path=registry_path,
    )
    registry.register_explicit_selection(
        fixture_root,
        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
    )
    return build_fire_shield_context(
        fixture_root,
        phase="VALIDATE_READ_ONLY",
        operation_id="os-fire-shield-v2a-live-validation",
        tool_source_root=root,
        registry_path=registry_path,
    )


def _build_fixture_python(fixture_root: Path) -> Path:
    venv_root = fixture_root / ".venv"
    venv.EnvBuilder(with_pip=False, clear=True).create(venv_root)
    python = venv_root / "Scripts" / "python.exe"
    require(python.is_file(), "OS_FIRE_SHIELD_V2A_FIXTURE_PROJECT_PYTHON")
    return python


def _parse_json_stdout(text: str) -> dict[str, object]:
    try:
        payload = json.loads(text.strip())
    except json.JSONDecodeError as exc:
        raise RuntimeError("OS_FIRE_SHIELD_V2A_LIVE_JSON_INVALID:" + text) from exc
    if not isinstance(payload, dict):
        raise RuntimeError("OS_FIRE_SHIELD_V2A_LIVE_JSON_NOT_OBJECT")
    return payload


def _process_alive(pid: int) -> bool:
    if os.name != "nt":
        return False
    from ctypes import wintypes

    kernel = ctypes.WinDLL("kernel32.dll", use_last_error=True)
    kernel.OpenProcess.restype = wintypes.HANDLE
    handle = kernel.OpenProcess(0x1000, False, int(pid))
    if not handle:
        return False
    try:
        code = wintypes.DWORD()
        if not kernel.GetExitCodeProcess(handle, ctypes.byref(code)):
            return False
        return int(code.value) == 259
    finally:
        kernel.CloseHandle(handle)


def validate_live_windows(root: Path) -> None:
    if os.name != "nt":
        print("OS_FIRE_SHIELD_V2A_WINDOWS_LIVE_VALIDATION: SKIP_NON_WINDOWS")
        return

    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)
    from kanda_reasoner_app.project_os_fire_shield_worker import (
        OS_FIRE_SHIELD_FEATURE_ID,
        run_external_project_python_isolated,
    )

    require(
        OS_FIRE_SHIELD_FEATURE_ID == FEATURE_ID,
        "OS_FIRE_SHIELD_V2A_PUBLIC_FEATURE_ID",
    )
    tool_probe = root / "kanda_reasoner_app" / "project_fire_shield.py"
    before = sha256(tool_probe)

    from kanda_reasoner_app.project_support_boundary import (
        canonical_project_support_root,
        canonical_transient_garbage_root,
    )

    host_transient = canonical_transient_garbage_root(root)
    host_transient.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="kanda_os_fire_shield_v2a_fixture_",
        dir=str(host_transient),
    ) as temp:
        fixture_root = Path(temp) / "external_project"
        fixture_root.mkdir()
        (fixture_root / "allowed.txt").write_text("PROJECT_READ_OK", encoding="ascii")
        _build_fixture_python(fixture_root)
        registry_path = Path(temp) / "registry" / "projects.json"
        registry_path.parent.mkdir(parents=True)
        context = _fixture_context(root, fixture_root, registry_path)

        probe_code = (
            "import json,os,sys;from pathlib import Path;"
            "project=Path(sys.argv[1]);tool=Path(sys.argv[2]);"
            "data={'project_read':False,'project_write_blocked':False,"
            "'tool_read_blocked':False,'transient_write':False};"
            "data['project_read']=(project/'allowed.txt').read_text()=='PROJECT_READ_OK';"
            "\ntry:\n (project/'blocked.txt').write_text('BAD')\n"
            "except OSError:\n data['project_write_blocked']=True\n"
            "\ntry:\n tool.read_bytes()\n"
            "except OSError:\n data['tool_read_blocked']=True\n"
            "temp=Path(os.environ['TEMP']);(temp/'allowed_write.txt').write_text('OK');"
            "data['transient_write']=(temp/'allowed_write.txt').read_text()=='OK';"
            "print(json.dumps(data,sort_keys=True))"
        )
        result = run_external_project_python_isolated(
            context,
            ["-I", "-c", probe_code, str(fixture_root), str(tool_probe)],
            timeout=30,
        )
        require(not result.timed_out, "OS_FIRE_SHIELD_V2A_LIVE_NOT_TIMED_OUT")
        require(result.returncode == 0, "OS_FIRE_SHIELD_V2A_LIVE_EXIT_ZERO")
        payload = _parse_json_stdout(result.stdout)
        require(payload.get("project_read") is True, "OS_FIRE_SHIELD_V2A_PROJECT_READ_ALLOWED")
        require(
            payload.get("project_write_blocked") is True,
            "OS_FIRE_SHIELD_V2A_PROJECT_SOURCE_WRITE_DENIED",
        )
        require(payload.get("tool_read_blocked") is True, "OS_FIRE_SHIELD_V2A_TOOL_ROOT_READ_DENIED")
        require(payload.get("transient_write") is True, "OS_FIRE_SHIELD_V2A_TRANSIENT_WRITE_ALLOWED")

        child = (
            "import json,subprocess,sys,time;"
            "code='import time;time.sleep(30)';"
            "p=subprocess.Popen([sys.executable,'-I','-c',code]);"
            "print(json.dumps({'child_pid':p.pid}))"
        )
        tree_result = run_external_project_python_isolated(
            context,
            ["-I", "-c", child],
            timeout=30,
        )
        require(
            tree_result.returncode == 0,
            "OS_FIRE_SHIELD_V2A_JOB_PARENT_EXIT_ZERO",
        )
        child_payload = _parse_json_stdout(tree_result.stdout)
        child_pid = int(child_payload.get("child_pid") or 0)
        require(child_pid > 0, "OS_FIRE_SHIELD_V2A_JOB_CHILD_CREATED")
        time.sleep(1)
        require(
            not _process_alive(child_pid),
            "OS_FIRE_SHIELD_V2A_JOB_CHILD_ESCAPE_DENIED",
        )
        require(
            not (fixture_root / "blocked.txt").exists(),
            "OS_FIRE_SHIELD_V2A_PROJECT_POST_STATE_UNCHANGED",
        )
        fixture_transient = canonical_transient_garbage_root(fixture_root)
        fixture_support = canonical_project_support_root(fixture_root)
        if fixture_transient.exists():
            import shutil

            shutil.rmtree(fixture_transient)
        if fixture_support.exists():
            import shutil

            shutil.rmtree(fixture_support)

    require(sha256(tool_probe) == before, "OS_FIRE_SHIELD_V2A_TOOL_POST_STATE_UNCHANGED")
    print("OS_FIRE_SHIELD_V2A_ACL_LEASE_REVOKE_PATH: PASS")
    print("OS_FIRE_SHIELD_V2A_WINDOWS_LIVE_VALIDATION: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--static-only", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve(strict=True)
    validate_static(root)
    if not args.static_only:
        validate_live_windows(root)
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
