# project-path: kanda_reasoner_app/engineering_diagnostics/collectors/ruff_collector.py
"""Read-only native JSON Ruff collector for Engineering Diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
from threading import Event

from kanda_reasoner_app.project_fire_shield import (
    FireShieldMode,
    build_fire_shield_context,
)
from time import monotonic
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from ..models import EngineeringDiagnosticsError

__all__ = [
    "RUFF_COLLECTOR_CONTRACT_VERSION",
    "RUFF_PRODUCER_ID",
    "RuffCollectionCancelled",
    "RuffCollectionError",
    "RuffCollectionResult",
    "collect_ruff_json",
]

RUFF_PRODUCER_ID = "ruff.check"
RUFF_COLLECTOR_CONTRACT_VERSION = "1.0"
_MAX_FINDINGS = 100000
_DEFAULT_TIMEOUT_SECONDS = 600.0


class RuffCollectionError(EngineeringDiagnosticsError):
    """Raised when native Ruff evidence cannot be collected safely."""


class RuffCollectionCancelled(RuffCollectionError):
    """Raised when a cooperative Ruff collection is cancelled."""


@dataclass(frozen=True, slots=True)
class RuffCollectionResult:
    """Completed immutable Ruff JSON collection and configuration evidence."""

    project_root: str
    ruff_version: str
    command_source: str
    config_relative_path: str
    config_sha256: str
    started_at_utc: str
    completed_at_utc: str
    raw_findings: tuple[Mapping[str, Any], ...]
    stdout_sha256: str

    @property
    def configuration_token(self) -> str:
        """Return deterministic configuration and tool-version identity."""
        return (
            self.config_relative_path
            + ":"
            + self.config_sha256
            + ":"
            + self.ruff_version
            + ":collector="
            + RUFF_COLLECTOR_CONTRACT_VERSION
        )


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _bounded_text(value: object, limit: int = 1200) -> str:
    compact = " ".join(str(value or "").split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _canonical_config(root: Path) -> tuple[Path, str]:
    config = root / "ruff.toml"
    if not config.is_file():
        raise RuffCollectionError("RUFF_CANONICAL_CONFIG_MISSING:ruff.toml")
    competing: list[str] = []
    alternate = root / ".ruff.toml"
    if alternate.is_file():
        competing.append(alternate.name)
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        text = pyproject.read_text(encoding="utf-8", errors="strict")
        if any(line.strip() == "[tool.ruff]" for line in text.splitlines()):
            competing.append(pyproject.name)
    if competing:
        raise RuffCollectionError(
            "RUFF_COMPETING_ROOT_CONFIG:" + "|".join(sorted(competing))
        )
    data = config.read_bytes()
    return config, _sha256_bytes(data)


def _candidate_prefixes(
    root: Path,
    explicit: Sequence[str] | None,
) -> tuple[tuple[tuple[str, ...], str], ...]:
    context = build_fire_shield_context(
        root,
        phase="VALIDATE_READ_ONLY",
        operation_id="ruff-collector-v2e-" + uuid.uuid4().hex,
    )
    if context.mode is FireShieldMode.EXTERNAL_PROJECT:
        if explicit:
            raise RuffCollectionError("RUFF_EXTERNAL_EXPLICIT_COMMAND_DENIED")
        return (((sys.executable, "-I", "-m", "ruff"), "tool_python_isolated_module"),)
    if explicit:
        prefix = tuple(str(item) for item in explicit)
        if not prefix or not prefix[0].strip():
            raise RuffCollectionError("RUFF_EXPLICIT_COMMAND_EMPTY")
        return ((prefix, "explicit"),)
    candidates: list[tuple[tuple[str, ...], str]] = []
    local = root / ".venv" / "Scripts" / "ruff.exe"
    if local.is_file():
        candidates.append(((str(local),), "project_venv"))
    discovered = shutil.which("ruff")
    if discovered:
        candidates.append(((str(Path(discovered).resolve()),), "path"))
    candidates.append(((sys.executable, "-m", "ruff"), "python_module"))
    return tuple(candidates)


def _environment() -> dict[str, str]:
    environment = dict(os.environ)
    environment["NO_COLOR"] = "1"
    environment["RUFF_NO_CACHE"] = "1"
    return environment


def _run_process(
    argv: Sequence[str],
    *,
    cwd: Path,
    timeout_seconds: float,
    cancellation: Event | None,
) -> tuple[int, str, str]:
    process = subprocess.Popen(
        tuple(str(item) for item in argv),
        cwd=str(cwd),
        env=_environment(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
    )
    deadline = monotonic() + float(timeout_seconds)
    stdout = ""
    stderr = ""
    while True:
        if cancellation is not None and cancellation.is_set():
            process.terminate()
            try:
                stdout, stderr = process.communicate(timeout=2.0)
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate(timeout=2.0)
            raise RuffCollectionCancelled("RUFF_COLLECTION_CANCELLED")
        remaining = deadline - monotonic()
        if remaining <= 0:
            process.kill()
            stdout, stderr = process.communicate()
            raise RuffCollectionError(
                "RUFF_COLLECTION_TIMEOUT:" + _bounded_text(stderr or stdout)
            )
        try:
            stdout, stderr = process.communicate(timeout=min(0.10, remaining))
        except subprocess.TimeoutExpired:
            continue
        break
    if cancellation is not None and cancellation.is_set():
        raise RuffCollectionCancelled("RUFF_COLLECTION_CANCELLED")
    return int(process.returncode), stdout or "", stderr or ""


def _resolve_command(
    root: Path,
    *,
    explicit: Sequence[str] | None,
    timeout_seconds: float,
    cancellation: Event | None,
) -> tuple[tuple[str, ...], str, str]:
    failures: list[str] = []
    for prefix, source in _candidate_prefixes(root, explicit):
        try:
            code, stdout, stderr = _run_process(
                (*prefix, "--version"),
                cwd=root,
                timeout_seconds=timeout_seconds,
                cancellation=cancellation,
            )
        except OSError as exc:
            failures.append(source + ":" + str(exc))
            continue
        if code == 0:
            version = (stdout or stderr).strip().splitlines()
            if version and version[0].strip():
                return prefix, source, version[0].strip()
        failures.append(source + ":" + _bounded_text(stderr or stdout))
    raise RuffCollectionError(
        "RUFF_NOT_AVAILABLE:" + " | ".join(item for item in failures if item)
    )


def _load_findings(stdout: str) -> tuple[Mapping[str, Any], ...]:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuffCollectionError(
            "RUFF_JSON_MALFORMED:" + _bounded_text(stdout, 500)
        ) from exc
    if not isinstance(payload, list):
        raise RuffCollectionError("RUFF_JSON_ROOT_NOT_LIST")
    if len(payload) > _MAX_FINDINGS:
        raise RuffCollectionError("RUFF_FINDING_LIMIT_EXCEEDED")
    findings: list[Mapping[str, Any]] = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            raise RuffCollectionError("RUFF_FINDING_NOT_OBJECT:" + str(index))
        findings.append(MappingProxyType(dict(item)))
    return tuple(findings)


def collect_ruff_json(
    project_root: str | Path,
    *,
    argv_prefix: Sequence[str] | None = None,
    timeout_seconds: float = _DEFAULT_TIMEOUT_SECONDS,
    cancellation: Event | None = None,
) -> RuffCollectionResult:
    """Execute Ruff read-only and return its machine-readable JSON findings."""
    root = Path(project_root).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise RuffCollectionError("RUFF_PROJECT_ROOT_NOT_DIRECTORY")
    if float(timeout_seconds) <= 0:
        raise RuffCollectionError("RUFF_TIMEOUT_NOT_POSITIVE")
    config, config_sha256 = _canonical_config(root)
    started = _utc_now()
    prefix, command_source, version = _resolve_command(
        root,
        explicit=argv_prefix,
        timeout_seconds=float(timeout_seconds),
        cancellation=cancellation,
    )
    command = (
        *prefix,
        "--config",
        str(config),
        "check",
        "--output-format",
        "json",
        "--exit-zero",
        "--no-cache",
        "--no-fix",
        "--color",
        "never",
        str(root),
    )
    try:
        code, stdout, stderr = _run_process(
            command,
            cwd=root,
            timeout_seconds=float(timeout_seconds),
            cancellation=cancellation,
        )
    except OSError as exc:
        raise RuffCollectionError("RUFF_EXECUTION_FAILED:" + str(exc)) from exc
    if code != 0:
        raise RuffCollectionError(
            "RUFF_EXECUTION_FAILED:"
            + str(code)
            + ":"
            + _bounded_text(stderr or stdout)
        )
    findings = _load_findings(stdout)
    return RuffCollectionResult(
        project_root=str(root),
        ruff_version=version,
        command_source=command_source,
        config_relative_path=config.relative_to(root).as_posix(),
        config_sha256=config_sha256,
        started_at_utc=started,
        completed_at_utc=_utc_now(),
        raw_findings=findings,
        stdout_sha256=_sha256_bytes(stdout.encode("utf-8")),
    )
