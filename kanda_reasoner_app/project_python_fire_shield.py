# project-path: kanda_reasoner_app/project_python_fire_shield.py
"""Route Project Python through Fire Shield without duplicating OS isolation."""

from __future__ import annotations

import subprocess
import uuid
from pathlib import Path
from collections.abc import Callable
from typing import Mapping, Sequence

from kanda_reasoner_app.project_fire_shield import (
    FireShieldMode,
    build_fire_shield_context,
)
from kanda_reasoner_app.project_os_fire_shield_worker import (
    run_external_project_python_isolated,
)

__all__ = [
    "PROJECT_PYTHON_FIRE_SHIELD_FEATURE_ID",
    "run_project_python_governed",
]

PROJECT_PYTHON_FIRE_SHIELD_FEATURE_ID = (
    "kanda-reasoner-fire-shield-cross-surface-project-python-execution-v2e"
)


def _selected_project_python(root: Path) -> Path:
    """Resolve the observed Project interpreter without Tool fallback."""
    candidates = (
        root / ".venv" / "Scripts" / "python.exe",
        root / ".venv" / "bin" / "python",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise RuntimeError("PROJECT_PYTHON_INTERPRETER_NOT_FOUND")


def _completed_from_isolated(result) -> subprocess.CompletedProcess[str]:
    """Convert one v2a result to the standard subprocess result contract."""
    if result.timed_out:
        raise subprocess.TimeoutExpired(
            cmd=list(result.argv),
            timeout=0,
            output=result.stdout,
            stderr=result.stderr,
        )
    return subprocess.CompletedProcess(
        args=list(result.argv),
        returncode=int(result.returncode),
        stdout=result.stdout,
        stderr=result.stderr,
    )


def run_project_python_governed(
    selected_project_root: str | Path,
    python_args: Sequence[str],
    *,
    cwd: str | Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float = 30.0,
    tool_source_root: str | Path | None = None,
    registry_path: str | Path | None = None,
    self_host_python: str | Path | None = None,
    self_host_runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run Python for the selected Project with external mode OS isolation.

    External Projects always use the selected Project ``.venv`` through the
    frozen v2a AppContainer/Job worker. Verified KANDA self-hosting keeps a
    local subprocess path for compatibility with existing Tool workflows.
    """
    root = Path(selected_project_root).expanduser().resolve(strict=True)
    run_cwd = Path(cwd or root).expanduser().resolve(strict=False)
    context = build_fire_shield_context(
        root,
        phase="VALIDATE_READ_ONLY",
        operation_id="project-python-v2e-" + uuid.uuid4().hex,
        tool_source_root=tool_source_root,
        registry_path=registry_path,
    )
    if context.mode is FireShieldMode.EXTERNAL_PROJECT:
        result = run_external_project_python_isolated(
            context,
            [str(part) for part in python_args],
            cwd=run_cwd,
            env=env,
            timeout=float(timeout),
        )
        if result.timed_out:
            raise subprocess.TimeoutExpired(
                cmd=list(result.argv),
                timeout=float(timeout),
                output=result.stdout,
                stderr=result.stderr,
            )
        return _completed_from_isolated(result)

    python = (
        Path(self_host_python).expanduser().resolve(strict=False)
        if self_host_python is not None
        else _selected_project_python(root)
    )
    runner = self_host_runner or subprocess.run
    return runner(
        [str(python), *[str(part) for part in python_args]],
        cwd=str(run_cwd),
        env=None if env is None else dict(env),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=float(timeout),
        shell=False,
    )
