# project-path: kanda_reasoner_app/source_hygiene/ruff_quality_runtime.py
"""Bounded Ruff command discovery and process execution."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Sequence

__all__: list[str] = []

_DEFAULT_RUFF_TIMEOUT_SECONDS = 180.0


@dataclass(frozen=True)
class _RuffCommandIdentity:
    """Resolved Ruff command prefix and version evidence."""

    argv_prefix: tuple[str, ...]
    version: str
    source: str


@dataclass(frozen=True)
class _RuffProcessResult:
    """Bounded subprocess result used by the Ruff integration."""

    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


def _resolve_ruff_command(
    argv_prefix: Sequence[str] | None = None,
    *,
    timeout_seconds: float = _DEFAULT_RUFF_TIMEOUT_SECONDS,
) -> _RuffCommandIdentity:
    """Resolve Ruff without importing Workbench-owned analyzer internals."""
    candidates: list[tuple[tuple[str, ...], str]] = []
    if argv_prefix:
        candidates.append((tuple(str(item) for item in argv_prefix), "explicit"))
    else:
        executable = shutil.which("ruff")
        if executable:
            candidates.append(((executable,), "path"))
        candidates.append(((sys.executable, "-m", "ruff"), "python_module"))

    failures: list[str] = []
    for candidate, source in candidates:
        if not candidate or not candidate[0].strip():
            continue
        result = _run_ruff_process(
            (*candidate, "--version"),
            cwd=None,
            timeout_seconds=timeout_seconds,
        )
        version_text = (result.stdout or result.stderr).strip()
        if result.returncode == 0 and version_text:
            return _RuffCommandIdentity(
                argv_prefix=candidate,
                version=version_text.splitlines()[0].strip(),
                source=source,
            )
        failures.append(source + ":" + _bounded_text(result.stderr or result.stdout))

    detail = " | ".join(item for item in failures if item)
    if not detail:
        detail = "No Ruff executable or importable Ruff module was found."
    raise RuntimeError("RUFF_NOT_AVAILABLE:" + detail)


def _run_ruff_process(
    argv: Sequence[str],
    *,
    cwd: Path | None,
    timeout_seconds: float,
) -> _RuffProcessResult:
    """Run one Ruff command without shell execution or project cache writes."""
    environment = dict(os.environ)
    environment["NO_COLOR"] = "1"
    environment["RUFF_NO_CACHE"] = "1"
    try:
        completed = subprocess.run(
            tuple(str(item) for item in argv),
            cwd=str(cwd) if cwd is not None else None,
            env=environment,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=float(timeout_seconds),
            check=False,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        return _RuffProcessResult(
            argv=tuple(str(item) for item in argv),
            returncode=124,
            stdout=_coerce_text(exc.stdout),
            stderr=_coerce_text(exc.stderr),
            timed_out=True,
        )
    except OSError as exc:
        return _RuffProcessResult(
            argv=tuple(str(item) for item in argv),
            returncode=127,
            stdout="",
            stderr=str(exc),
        )
    return _RuffProcessResult(
        argv=tuple(str(item) for item in argv),
        returncode=int(completed.returncode),
        stdout=completed.stdout or "",
        stderr=completed.stderr or "",
    )


def _coerce_text(value: object) -> str:
    """Decode timeout output into plain text."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _bounded_text(value: object, limit: int = 1200) -> str:
    """Return one bounded, whitespace-normalized diagnostic string."""
    compact = " ".join(str(value or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."
