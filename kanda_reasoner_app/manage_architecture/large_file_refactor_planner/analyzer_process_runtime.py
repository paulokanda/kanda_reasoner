# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_process_runtime.py
"""Bounded subprocess runtime for external Advanced Quality Review analyzers."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import os
from pathlib import Path
import subprocess
import threading
import time
from typing import Callable

from .advanced_quality_review_contract import AnalysisExecutionStatus
from .analyzer_process_tree import (
    ProcessTreeCleanupEvidence,
    process_tree_spawn_kwargs,
    terminate_process_tree,
)

__all__ = [
    "BoundedProcessRequest",
    "CancellationToken",
    "ProcessExecutionEvidence",
    "ProcessProgressEvent",
    "run_bounded_process",
]

ProgressCallback = Callable[["ProcessProgressEvent"], None]


class CancellationToken:
    """Thread-safe cooperative cancellation token for one analyzer execution."""

    def __init__(self) -> None:
        self._event = threading.Event()

    def cancel(self) -> None:
        """Request cancellation without blocking the caller."""
        self._event.set()

    @property
    def cancelled(self) -> bool:
        """Return whether cancellation has been requested."""
        return self._event.is_set()


@dataclass(frozen=True)
class BoundedProcessRequest:
    """Describe one shell-free, bounded analyzer process invocation."""

    engine_id: str
    argv: tuple[str, ...]
    cwd: str
    environment_overrides: tuple[tuple[str, str], ...] = ()
    timeout_seconds: float = 60.0
    max_stdout_bytes: int = 1_000_000
    max_stderr_bytes: int = 1_000_000
    poll_interval_seconds: float = 0.05


@dataclass(frozen=True)
class ProcessProgressEvent:
    """Emit one observable lifecycle event from the bounded runtime."""

    engine_id: str
    phase: str
    elapsed_ms: int
    message: str


@dataclass(frozen=True)
class ProcessExecutionEvidence:
    """Immutable execution evidence for one analyzer process."""

    engine_id: str
    status: AnalysisExecutionStatus
    process_id: int
    argv: tuple[str, ...]
    cwd: str
    exit_code: int | None
    duration_ms: int
    stdout_text: str
    stderr_text: str
    stdout_bytes_observed: int
    stderr_bytes_observed: int
    stdout_truncated: bool
    stderr_truncated: bool
    cleanup: ProcessTreeCleanupEvidence

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready execution evidence."""
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


class _BoundedByteCollector:
    """Drain one process stream while retaining only bounded evidence bytes."""

    def __init__(self, limit: int) -> None:
        if int(limit) < 0:
            raise ValueError("PROCESS_OUTPUT_LIMIT_NEGATIVE")
        self._limit = int(limit)
        self._chunks: list[bytes] = []
        self._stored = 0
        self._observed = 0
        self._lock = threading.Lock()

    def consume(self, chunk: bytes) -> None:
        """Record observed bytes and retain only the configured bounded prefix."""
        if not chunk:
            return
        with self._lock:
            self._observed += len(chunk)
            remaining = self._limit - self._stored
            if remaining > 0:
                selected = chunk[:remaining]
                self._chunks.append(selected)
                self._stored += len(selected)

    @property
    def observed(self) -> int:
        """Return total bytes drained from the stream."""
        with self._lock:
            return self._observed

    @property
    def truncated(self) -> bool:
        """Return whether observed bytes exceeded retained evidence bytes."""
        with self._lock:
            return self._observed > self._stored

    def text(self) -> str:
        """Decode retained evidence with explicit replacement for invalid bytes."""
        with self._lock:
            data = b"".join(self._chunks)
        return data.decode("utf-8", errors="replace")


def run_bounded_process(
    request: BoundedProcessRequest,
    *,
    cancellation_token: CancellationToken | None = None,
    progress_callback: ProgressCallback | None = None,
) -> ProcessExecutionEvidence:
    """Run one analyzer process with timeout, cancellation, and bounded evidence."""
    _validate_request(request)
    token = cancellation_token or CancellationToken()
    start = time.monotonic()
    _emit(progress_callback, request, start, "STAGE_START", "Launching analyzer process.")
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.update(dict(request.environment_overrides))
    popen_kwargs = process_tree_spawn_kwargs()
    process = subprocess.Popen(
        list(request.argv),
        cwd=str(Path(request.cwd).resolve(strict=False)),
        env=environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        bufsize=0,
        **popen_kwargs,
    )
    stdout_collector = _BoundedByteCollector(request.max_stdout_bytes)
    stderr_collector = _BoundedByteCollector(request.max_stderr_bytes)
    stdout_thread = _start_reader(process.stdout, stdout_collector)
    stderr_thread = _start_reader(process.stderr, stderr_collector)

    terminal_status: AnalysisExecutionStatus | None = None
    cleanup: ProcessTreeCleanupEvidence | None = None
    while process.poll() is None:
        elapsed = time.monotonic() - start
        if token.cancelled:
            terminal_status = AnalysisExecutionStatus.CANCELLED
            _emit(progress_callback, request, start, "STAGE_CANCEL", "Cancellation requested.")
            cleanup = terminate_process_tree(process)
            break
        if elapsed >= request.timeout_seconds:
            terminal_status = AnalysisExecutionStatus.TIMED_OUT
            _emit(progress_callback, request, start, "STAGE_TIMEOUT", "Analyzer timeout reached.")
            cleanup = terminate_process_tree(process)
            break
        time.sleep(request.poll_interval_seconds)

    if terminal_status is None:
        process.wait()
        terminal_status = (
            AnalysisExecutionStatus.SUCCEEDED
            if process.returncode == 0
            else AnalysisExecutionStatus.FAILED
        )
        cleanup = ProcessTreeCleanupEvidence(
            process_id=int(process.pid),
            platform=os.name,
            method="natural_exit",
            requested=False,
            root_process_reaped=True,
            cleanup_ok=True,
            diagnostic="Process exited without forced cleanup.",
        )

    stdout_thread.join(timeout=2.0)
    stderr_thread.join(timeout=2.0)
    duration_ms = int((time.monotonic() - start) * 1000)
    _emit(
        progress_callback,
        request,
        start,
        "STAGE_TERMINAL",
        "Analyzer finished with status " + terminal_status.value + ".",
    )
    assert cleanup is not None
    return ProcessExecutionEvidence(
        engine_id=request.engine_id,
        status=terminal_status,
        process_id=int(process.pid),
        argv=request.argv,
        cwd=str(Path(request.cwd).resolve(strict=False)),
        exit_code=process.returncode,
        duration_ms=duration_ms,
        stdout_text=stdout_collector.text(),
        stderr_text=stderr_collector.text(),
        stdout_bytes_observed=stdout_collector.observed,
        stderr_bytes_observed=stderr_collector.observed,
        stdout_truncated=stdout_collector.truncated,
        stderr_truncated=stderr_collector.truncated,
        cleanup=cleanup,
    )


def _start_reader(
    stream: object,
    collector: _BoundedByteCollector,
) -> threading.Thread:
    """Start one daemon reader that drains a binary subprocess pipe."""
    def read_stream() -> None:
        reader = stream
        if reader is None:
            return
        while True:
            chunk = reader.read(4096)
            if not chunk:
                break
            collector.consume(chunk)

    thread = threading.Thread(target=read_stream, daemon=True)
    thread.start()
    return thread


def _validate_request(request: BoundedProcessRequest) -> None:
    """Reject unsafe or unbounded runtime requests before process creation."""
    if not str(request.engine_id or "").strip():
        raise ValueError("PROCESS_ENGINE_ID_EMPTY")
    if not request.argv or not str(request.argv[0] or "").strip():
        raise ValueError("PROCESS_ARGV_EMPTY")
    if not str(request.cwd or "").strip():
        raise ValueError("PROCESS_CWD_EMPTY")
    if float(request.timeout_seconds) <= 0:
        raise ValueError("PROCESS_TIMEOUT_NOT_POSITIVE")
    if float(request.poll_interval_seconds) <= 0:
        raise ValueError("PROCESS_POLL_INTERVAL_NOT_POSITIVE")
    if int(request.max_stdout_bytes) < 0 or int(request.max_stderr_bytes) < 0:
        raise ValueError("PROCESS_OUTPUT_LIMIT_NEGATIVE")


def _emit(
    callback: ProgressCallback | None,
    request: BoundedProcessRequest,
    start: float,
    phase: str,
    message: str,
) -> None:
    """Emit one bounded lifecycle event without giving callbacks runtime ownership."""
    if callback is None:
        return
    callback(
        ProcessProgressEvent(
            engine_id=request.engine_id,
            phase=phase,
            elapsed_ms=int((time.monotonic() - start) * 1000),
            message=message,
        )
    )
