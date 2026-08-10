# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_import_checks.py
"""Own isolated import-probe workflow checks."""

from __future__ import annotations

import fnmatch
import json
import logging
import subprocess
import time
from pathlib import Path
from typing import Any

from .workflow_constants import (
    IMPORT_PROBE_CODE,
)
from .workflow_python_runtime import (
    resolve_project_python,
    run_project_python_probe,
)
from .workflow_models import (
    CheckResult,
)

__all__ = [
    "run_import_checks",
]


def _probe_argv(project_python: Path, root: Path, module: str) -> list[str]:
    """Return the exact argument vector used for an isolated import probe."""
    return [
        str(project_python),
        "-I",
        "-c",
        IMPORT_PROBE_CODE,
        str(root),
        module,
    ]


def _render_probe_argv(argv: list[str]) -> str:
    """Render the exact probe argument vector without shell re-interpretation."""
    return "argv=" + json.dumps(argv, ensure_ascii=True)

def run_import_checks(root: Path, discovered: dict[str, Any], cfg: dict[str, Any]) -> list[CheckResult]:
    """Run the import checks.
    
    Parameters
    ----------
    root : Path
        The root path.
    discovered : dict[str, Any]
        The discovered value.
    cfg : dict[str, Any]
        The configuration data.
    
    Returns
    -------
    list[CheckResult]
        The list of values.
    """
    
    if not cfg.get("enabled", True):
        return [CheckResult("imports", "imports", "skip", "Workflow disabled.")]

    include_modules = cfg.get("include_modules") or []
    if include_modules and not isinstance(include_modules, list):
        return [CheckResult("imports", "imports", "fail", "include_modules must be a list.")]

    exclude_patterns = cfg.get("exclude_patterns") or []
    if not isinstance(exclude_patterns, list):
        return [CheckResult("imports", "imports", "fail", "exclude_patterns must be a list.")]

    module_limit = int(cfg.get("module_limit", 25))
    timeout = cfg.get("timeout_seconds", 20)

    modules = [str(m) for m in include_modules] if include_modules else list(discovered["importable_modules"])

    filtered: list[str] = []
    for module in modules:
        if any(fnmatch.fnmatch(module, pattern) for pattern in exclude_patterns):
            continue
        filtered.append(module)

    if not filtered:
        return [CheckResult("imports", "imports", "warn", "No eligible modules for import probing.")]

    try:
        project_python = resolve_project_python(root)
    except RuntimeError as exc:
        return [CheckResult("imports", "imports", "fail", str(exc))]

    results: list[CheckResult] = []
    for module in filtered[:module_limit]:
        start = time.perf_counter()
        try:
            probe_argv = _probe_argv(project_python, root, module)
            completed = run_project_python_probe(
                root,
                probe_argv[1:],
                cwd=root,
                timeout=float(timeout),
            )
        except subprocess.TimeoutExpired as exc:
            results.append(
                CheckResult(
                    "imports",
                    module,
                    "fail",
                    f"Import probe timed out after {timeout} second(s).",
                    duration_seconds=time.perf_counter() - start,
                    command=_render_probe_argv(probe_argv),
                    details={"stdout": exc.stdout or "", "stderr": exc.stderr or ""},
                )
            )
            continue

        duration = time.perf_counter() - start
        if completed.returncode != 0:
            results.append(
                CheckResult(
                    "imports",
                    module,
                    "fail",
                    f"Import probe process exited with code {completed.returncode}.",
                    duration_seconds=duration,
                    command=_render_probe_argv(probe_argv),
                    details={"stdout": completed.stdout, "stderr": completed.stderr},
                )
            )
            continue

        try:
            payload = json.loads(completed.stdout.strip() or "{}")
        except Exception as exc:
            logging.exception("Import probe returned invalid JSON")
            results.append(
                CheckResult(
                    "imports",
                    module,
                    "fail",
                    f"Import probe returned invalid JSON: {exc}",
                    duration_seconds=duration,
                    command=_render_probe_argv(probe_argv),
                    details={"stdout": completed.stdout, "stderr": completed.stderr},
                )
            )
            continue

        status = "pass"
        message_parts: list[str] = []
        if payload.get("status") != "pass":
            status = "fail"
            message_parts.append(payload.get("error") or "Import failed.")
        if payload.get("stdout"):
            status = "fail"
            message_parts.append("stdout emitted during import")
        if payload.get("stderr"):
            status = "fail"
            message_parts.append("stderr emitted during import")
        if payload.get("cwd_changed"):
            status = "fail"
            message_parts.append("cwd changed during import")
        if payload.get("sys_path_changed"):
            status = "fail"
            message_parts.append("sys.path changed during import")
        if not message_parts:
            message_parts.append("Import probe passed with no visible side effects.")

        results.append(
            CheckResult(
                "imports",
                module,
                status,
                "; ".join(message_parts),
                duration_seconds=float(payload.get("duration_seconds", duration)),
                command=_render_probe_argv(probe_argv),
                details=payload,
            )
        )

    if len(filtered) > module_limit:
        results.append(
            CheckResult(
                "imports",
                "imports",
                "warn",
                f"Only the first {module_limit} modules were probed. Increase module_limit to cover more.",
            )
        )

    return results
