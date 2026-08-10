# project-path: kanda_reasoner_app/project_os_fire_shield_worker.py
"""Public OS-enforced worker foundation beneath Fire Shield v1.

The v2a foundation is intentionally narrow. It runs only the verified external
Project's own Python interpreter, grants an ephemeral AppContainer SID read and
execute access to the Project/runtime, grants write access only to a per-run
Project transient directory, and contains the process tree in a Job Object.
"""

from __future__ import annotations

import os
import uuid
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from kanda_reasoner_app import _project_os_fire_shield_winapi as _winapi
from kanda_reasoner_app.project_fire_shield import (
    FireShieldContext,
    FireShieldMode,
    assert_fire_shield_context_current,
)
from kanda_reasoner_app.project_support_boundary import (
    canonical_project_support_root,
    canonical_transient_garbage_root,
)

__all__ = [
    "OS_FIRE_SHIELD_FEATURE_ID",
    "OsFireShieldError",
    "OsFireShieldProcessResult",
    "run_external_project_python_isolated",
]

OS_FIRE_SHIELD_FEATURE_ID = (
    "kanda-reasoner-fire-shield-os-worker-runtime-foundation-v2a"
)


class OsFireShieldError(RuntimeError):
    """Raised when OS-enforced external-Project isolation fails closed."""


@dataclass(frozen=True)
class OsFireShieldProcessResult:
    """Captured result from one isolated external-Project Python run."""

    argv: tuple[str, ...]
    cwd: Path
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool
    appcontainer_profile: str


def _project_python(context: FireShieldContext) -> Path:
    root = context.boundary.active_project_root
    candidates = (
        root / ".venv" / "Scripts" / "python.exe",
        root / ".venv" / "bin" / "python",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise OsFireShieldError("OS_FIRE_SHIELD_PROJECT_PYTHON_NOT_FOUND")


def _base_python_root(project_python: Path) -> Path | None:
    cfg = project_python.parents[1] / "pyvenv.cfg"
    if not cfg.is_file():
        return None
    lines = cfg.read_text(encoding="utf-8", errors="replace").splitlines()
    for raw in lines:
        key, sep, value = raw.partition("=")
        if sep and key.strip().casefold() == "home":
            resolved = Path(value.strip()).expanduser().resolve(strict=False)
            return resolved if resolved.exists() else None
    return None


def _sanitized_environment(
    env: Mapping[str, str] | None,
    transient_root: Path,
) -> dict[str, str]:
    values = dict(os.environ if env is None else env)
    for key in ("PYTHONHOME", "PYTHONPATH", "VIRTUAL_ENV"):
        values.pop(key, None)
    values["PYTHONDONTWRITEBYTECODE"] = "1"
    values["PYTHONNOUSERSITE"] = "1"
    values["TEMP"] = str(transient_root)
    values["TMP"] = str(transient_root)
    return {str(key): str(value) for key, value in values.items()}


def _read_capture(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _governed_cwd(context: FireShieldContext, cwd: str | Path | None) -> tuple[Path, bool]:
    boundary = context.boundary
    project_root = boundary.active_project_root.resolve()
    support_root = boundary.active_project_support_root.resolve()
    daily_root = boundary.active_project_daily_work_root.resolve()
    tool_root = boundary.tool_source_root.resolve()
    tool_support = canonical_project_support_root(tool_root).resolve()
    tool_daily = canonical_transient_garbage_root(tool_root).resolve()
    run_cwd = Path(cwd or project_root).expanduser().resolve(strict=False)
    if any(_inside(run_cwd, root) for root in (tool_root, tool_support, tool_daily)):
        raise OsFireShieldError("OS_FIRE_SHIELD_CWD_INSIDE_TOOL_OWNED_ROOT")
    if not run_cwd.is_dir():
        raise OsFireShieldError("OS_FIRE_SHIELD_CWD_NOT_DIRECTORY")
    if _inside(run_cwd, project_root):
        return run_cwd, False
    if _inside(run_cwd, support_root) or _inside(run_cwd, daily_root):
        return run_cwd, True
    raise OsFireShieldError("OS_FIRE_SHIELD_CWD_OUTSIDE_PROJECT_OWNED_ROOTS")


def run_external_project_python_isolated(
    context: FireShieldContext,
    python_args: Sequence[str],
    *,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float = 30.0,
) -> OsFireShieldProcessResult:
    """Run Active Project Python under AppContainer plus Job containment."""
    if os.name != "nt":
        raise OsFireShieldError("OS_FIRE_SHIELD_WINDOWS_REQUIRED")
    try:
        assert_fire_shield_context_current(context)
    except Exception as exc:
        raise OsFireShieldError(
            "OS_FIRE_SHIELD_CONTEXT_NOT_CURRENT:" + str(exc)
        ) from exc
    if context.mode is not FireShieldMode.EXTERNAL_PROJECT:
        raise OsFireShieldError("OS_FIRE_SHIELD_EXTERNAL_PROJECT_REQUIRED")

    project_root = context.boundary.active_project_root.resolve()
    run_cwd, lease_cwd = _governed_cwd(context, cwd)

    python = _project_python(context)
    transient = canonical_transient_garbage_root(project_root)
    transient.mkdir(parents=True, exist_ok=True)
    run_root = transient / ("os_fire_shield_v2a_" + uuid.uuid4().hex)
    run_root.mkdir(parents=True, exist_ok=False)
    stdout_path = run_root / "stdout.bin"
    stderr_path = run_root / "stderr.bin"
    profile = "KandaFireShieldV2a." + uuid.uuid4().hex[:24]
    argv = (str(python), *[str(part) for part in python_args])
    base_root = _base_python_root(python)
    code = 1
    timed_out = False

    try:
        try:
            with _winapi.appcontainer_profile(profile) as sid, ExitStack() as stack:
                read_mask = _winapi.GENERIC_READ | _winapi.GENERIC_EXECUTE
                write_mask = read_mask | _winapi.GENERIC_WRITE | _winapi.DELETE
                stack.enter_context(
                    _winapi.acl_lease(project_root, sid, read_mask)
                )
                if lease_cwd:
                    stack.enter_context(
                        _winapi.acl_lease(run_cwd, sid, read_mask)
                    )
                if base_root is not None and base_root != project_root:
                    stack.enter_context(
                        _winapi.acl_lease(base_root, sid, read_mask)
                    )
                stack.enter_context(
                    _winapi.acl_lease(run_root, sid, write_mask)
                )
                stdout_stream, stdout_handle = _winapi.open_inheritable_file(
                    stdout_path
                )
                stderr_stream, stderr_handle = _winapi.open_inheritable_file(
                    stderr_path
                )
                stdin_handle = _winapi.open_null_input_handle()
                try:
                    code, timed_out = _winapi.launch_appcontainer_process(
                        argv=argv,
                        cwd=run_cwd,
                        env=_sanitized_environment(env, run_root),
                        timeout=float(timeout),
                        sid=sid,
                        stdout_handle=stdout_handle,
                        stderr_handle=stderr_handle,
                        stdin_handle=stdin_handle,
                    )
                finally:
                    stdout_stream.close()
                    stderr_stream.close()
                    _winapi.close_handle(stdin_handle)
        except _winapi.WinApiIsolationError as exc:
            raise OsFireShieldError(str(exc)) from exc

        return OsFireShieldProcessResult(
            argv=tuple(argv),
            cwd=run_cwd,
            returncode=code,
            stdout=_read_capture(stdout_path),
            stderr=_read_capture(stderr_path),
            timed_out=timed_out,
            appcontainer_profile=profile,
        )
    finally:
        for child in (stdout_path, stderr_path):
            try:
                child.unlink()
            except FileNotFoundError:
                pass
        try:
            run_root.rmdir()
        except OSError:
            pass
