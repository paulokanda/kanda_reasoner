# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_python_runtime.py
"""Resolve and execute selected-Project Python under governed authority."""

from __future__ import annotations

import subprocess
import uuid
from pathlib import Path
from typing import Mapping, Sequence

from kanda_reasoner_app.project_fire_shield import (
    FireShieldMode,
    build_fire_shield_context,
)
from kanda_reasoner_app.project_os_fire_shield_worker import (
    run_external_project_python_isolated,
)

__all__ = [
    "project_python_has_module",
    "resolve_project_python",
    "run_project_python_probe",
]


def _project_python_candidates(root: Path) -> tuple[Path, ...]:
    """Return supported Project-local virtual-environment interpreter paths."""
    project_root = root.expanduser().resolve()
    return (
        project_root / ".venv" / "Scripts" / "python.exe",
        project_root / ".venv" / "bin" / "python",
    )


def resolve_project_python(root: Path) -> Path:
    """Return the selected Project's own Python interpreter or fail closed."""
    candidates = _project_python_candidates(root)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    rendered = "; ".join(str(candidate) for candidate in candidates)
    raise RuntimeError(
        "PROJECT_PYTHON_INTERPRETER_NOT_FOUND: expected Active Project "
        ".venv interpreter at one of: " + rendered
    )


def run_project_python_probe(
    root: Path,
    python_args: Sequence[str],
    *,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
    timeout: float = 30.0,
    tool_source_root: Path | None = None,
    registry_path: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run Project Python, OS-isolated whenever Active Project is external."""
    project_root = root.expanduser().resolve()
    python = resolve_project_python(project_root)
    context = build_fire_shield_context(
        project_root,
        phase="VALIDATE_READ_ONLY",
        operation_id="manage-workflows-python-probe-" + uuid.uuid4().hex,
        tool_source_root=tool_source_root,
        registry_path=registry_path,
    )
    if context.mode is FireShieldMode.EXTERNAL_PROJECT:
        isolated = run_external_project_python_isolated(
            context,
            [str(part) for part in python_args],
            cwd=cwd or project_root,
            env=env,
            timeout=float(timeout),
        )
        if isolated.timed_out:
            raise subprocess.TimeoutExpired(
                cmd=list(isolated.argv),
                timeout=timeout,
                output=isolated.stdout,
                stderr=isolated.stderr,
            )
        return subprocess.CompletedProcess(
            args=list(isolated.argv),
            returncode=isolated.returncode,
            stdout=isolated.stdout,
            stderr=isolated.stderr,
        )

    return subprocess.run(
        [str(python), *[str(part) for part in python_args]],
        cwd=str(cwd or project_root),
        env=None if env is None else dict(env),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=timeout,
    )


def project_python_has_module(root: Path, module_name: str) -> bool:
    """Return whether a module is importable by the Active Project interpreter."""
    probe = (
        "import importlib.util,sys;"
        "sys.exit(0 if importlib.util.find_spec(sys.argv[1]) else 1)"
    )
    completed = run_project_python_probe(
        root,
        ["-I", "-c", probe, module_name],
        timeout=15,
    )
    return completed.returncode == 0
