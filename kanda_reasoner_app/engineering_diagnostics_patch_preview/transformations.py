# project-path: kanda_reasoner_app/engineering_diagnostics_patch_preview/transformations.py
"""Narrow isolated transformations for eligible Wave 2U previews."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
from typing import Callable, Sequence

from .models import GovernedPatchPreviewPlan

__all__ = ["build_isolated_proposed_bytes"]

CommandRunner = Callable[[Sequence[str], Path], tuple[int, str, str]]


def _default_runner(command: Sequence[str], cwd: Path) -> tuple[int, str, str]:
    completed = subprocess.run(
        tuple(command),
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
        timeout=120.0,
    )
    return completed.returncode, completed.stdout, completed.stderr


def _ruff_prefix(explicit: Sequence[str] | None) -> tuple[str, ...]:
    if explicit:
        return tuple(str(item) for item in explicit)
    return (sys.executable, "-m", "ruff")


def _compile_python(relative_path: str, payload: bytes) -> None:
    if not relative_path.lower().endswith((".py", ".pyi", ".pyw")):
        return
    try:
        text = payload.decode("utf-8")
        compile(text, relative_path, "exec")
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise RuntimeError("PATCH_PREVIEW_PROPOSED_PYTHON_INVALID") from exc


def build_isolated_proposed_bytes(
    project_root: Path,
    workspace_file: Path,
    plan: GovernedPatchPreviewPlan,
    *,
    ruff_argv_prefix: Sequence[str] | None = None,
    command_runner: CommandRunner | None = None,
) -> tuple[bytes, tuple[str, ...]]:
    """Transform one copied file and return exact proposed bytes plus evidence."""
    runner = command_runner or _default_runner
    if plan.correction_kind == "UTF8_BOM_REMOVAL":
        payload = workspace_file.read_bytes()
        if not payload.startswith(b"\xef\xbb\xbf"):
            raise RuntimeError("PATCH_PREVIEW_EXPECTED_UTF8_BOM_MISSING")
        proposed = payload[3:]
        _compile_python(plan.relative_path, proposed)
        workspace_file.write_bytes(proposed)
        return proposed, (
            "PATCH_PREVIEW_UTF8_BOM_REMOVAL: PASS",
            "PATCH_PREVIEW_ISOLATED_PYTHON_COMPILE: PASS",
        )

    if plan.correction_kind not in {
        "RUFF_SAFE_UNUSED_IMPORT",
        "RUFF_SAFE_IMPORT_FORMAT",
    }:
        raise RuntimeError("PATCH_PREVIEW_TRANSFORMATION_NOT_SUPPORTED")
    command = (
        *_ruff_prefix(ruff_argv_prefix),
        "check",
        "--fix-only",
        "--no-cache",
        "--no-preview",
        "--select",
        plan.code,
        str(workspace_file),
    )
    returncode, stdout, stderr = runner(command, project_root)
    if returncode != 0:
        raise RuntimeError(
            "PATCH_PREVIEW_ISOLATED_RUFF_FIX_FAILED:"
            + (stderr.strip() or stdout.strip() or str(returncode))
        )
    proposed = workspace_file.read_bytes()
    _compile_python(plan.relative_path, proposed)
    verify = (
        *_ruff_prefix(ruff_argv_prefix),
        "check",
        "--no-cache",
        "--no-preview",
        "--select",
        plan.code,
        str(workspace_file),
    )
    returncode, stdout, stderr = runner(verify, project_root)
    if returncode != 0:
        raise RuntimeError(
            "PATCH_PREVIEW_ISOLATED_RUFF_VALIDATION_FAILED:"
            + (stderr.strip() or stdout.strip() or str(returncode))
        )
    return proposed, (
        "PATCH_PREVIEW_ISOLATED_RUFF_RULE: " + plan.code + " PASS",
        "PATCH_PREVIEW_ISOLATED_PYTHON_COMPILE: PASS",
        "PATCH_PREVIEW_GLOBAL_RUFF_FIX_EXECUTED: NO",
    )
