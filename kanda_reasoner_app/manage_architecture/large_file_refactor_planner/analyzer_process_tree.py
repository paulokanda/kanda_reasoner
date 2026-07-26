# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_process_tree.py
"""Cross-platform process-tree containment helpers for analyzer execution."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import os
import signal
import subprocess
import time
from typing import Any

__all__ = [
    "ProcessTreeCleanupEvidence",
    "process_tree_spawn_kwargs",
    "terminate_process_tree",
]


@dataclass(frozen=True)
class ProcessTreeCleanupEvidence:
    """Describe one bounded attempt to terminate and reap an analyzer tree."""

    process_id: int
    platform: str
    method: str
    requested: bool
    root_process_reaped: bool
    cleanup_ok: bool
    diagnostic: str

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready cleanup evidence."""
        return asdict(self)


def process_tree_spawn_kwargs() -> dict[str, Any]:
    """Return Popen options that establish a controllable process-tree boundary."""
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        return {"creationflags": creationflags}
    return {"start_new_session": True}


def terminate_process_tree(
    process: subprocess.Popen[bytes],
    *,
    grace_seconds: float = 1.0,
) -> ProcessTreeCleanupEvidence:
    """Terminate one analyzer process tree and return cleanup evidence."""
    if process.poll() is not None:
        return ProcessTreeCleanupEvidence(
            process_id=int(process.pid),
            platform=os.name,
            method="natural_exit",
            requested=False,
            root_process_reaped=True,
            cleanup_ok=True,
            diagnostic="Process had already exited before cleanup.",
        )
    if os.name == "nt":
        return _terminate_windows_tree(process, grace_seconds=grace_seconds)
    return _terminate_posix_tree(process, grace_seconds=grace_seconds)


def _terminate_windows_tree(
    process: subprocess.Popen[bytes],
    *,
    grace_seconds: float,
) -> ProcessTreeCleanupEvidence:
    """Use the Windows tree-aware taskkill contract and reap the root process."""
    diagnostic_parts: list[str] = []
    taskkill_ok = False
    try:
        completed = subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            check=False,
            timeout=max(2.0, grace_seconds + 1.0),
        )
        taskkill_ok = completed.returncode == 0
        stdout_text = completed.stdout.decode("utf-8", errors="replace").strip()
        stderr_text = completed.stderr.decode("utf-8", errors="replace").strip()
        if stdout_text:
            diagnostic_parts.append("stdout=" + stdout_text[:500])
        if stderr_text:
            diagnostic_parts.append("stderr=" + stderr_text[:500])
    except (OSError, subprocess.SubprocessError) as exc:
        diagnostic_parts.append("taskkill_error=" + str(exc))
    root_reaped = _wait_for_root_exit(process, grace_seconds)
    if not root_reaped:
        try:
            process.kill()
        except OSError as exc:
            diagnostic_parts.append("root_kill_error=" + str(exc))
        root_reaped = _wait_for_root_exit(process, grace_seconds)
    cleanup_ok = bool(root_reaped and taskkill_ok)
    return ProcessTreeCleanupEvidence(
        process_id=int(process.pid),
        platform=os.name,
        method="windows_taskkill_tree",
        requested=True,
        root_process_reaped=root_reaped,
        cleanup_ok=cleanup_ok,
        diagnostic="; ".join(diagnostic_parts)[:1200],
    )


def _terminate_posix_tree(
    process: subprocess.Popen[bytes],
    *,
    grace_seconds: float,
) -> ProcessTreeCleanupEvidence:
    """Terminate a process group created with start_new_session=True."""
    diagnostic_parts: list[str] = []
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    except OSError as exc:
        diagnostic_parts.append("sigterm_error=" + str(exc))
    root_reaped = _wait_for_root_exit(process, grace_seconds)
    if not root_reaped:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError as exc:
            diagnostic_parts.append("sigkill_error=" + str(exc))
        root_reaped = _wait_for_root_exit(process, grace_seconds)
    return ProcessTreeCleanupEvidence(
        process_id=int(process.pid),
        platform=os.name,
        method="posix_process_group",
        requested=True,
        root_process_reaped=root_reaped,
        cleanup_ok=root_reaped,
        diagnostic="; ".join(diagnostic_parts)[:1200],
    )


def _wait_for_root_exit(
    process: subprocess.Popen[bytes],
    grace_seconds: float,
) -> bool:
    """Wait for bounded root-process exit and report whether it was reaped."""
    deadline = time.monotonic() + max(0.1, float(grace_seconds))
    while time.monotonic() < deadline:
        try:
            process.wait(timeout=0.05)
            return True
        except subprocess.TimeoutExpired:
            continue
    return process.poll() is not None
