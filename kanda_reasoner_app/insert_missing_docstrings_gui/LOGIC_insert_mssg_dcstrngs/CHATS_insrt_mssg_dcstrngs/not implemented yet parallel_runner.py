#!/usr/bin/env python3
"""Parallel file-processing engine for the docstring inserter.

Wraps the per-file ``collect_missing_docstring_insertions`` + AI pipeline in a
``ThreadPoolExecutor`` so LLM HTTP calls (I/O-bound, GIL-releasing) run
concurrently across files.

Public API
----------
run_parallel(...)
    Process a list of Python files concurrently and return the same
    ``(changes, skipped_messages)`` structure that ``collect_changes``
    previously returned.  Drop-in replacement for the sequential loop.
"""

from __future__ import annotations

import threading
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

# Deferred import so this module has no hard dependency on the AI stack.
# The caller passes the processor function directly.
from typing import Protocol


# ---------------------------------------------------------------------------
# Progress reporting
# ---------------------------------------------------------------------------


@dataclass
class FileProgress:
    """Snapshot of progress for a single file.

    Parameters
    ----------
    path : Path
        Absolute path to the Python file being processed.
    symbols_found : int
        Number of missing-docstring symbols detected in this file.
    symbols_done : int
        Number of docstrings generated so far for this file.
    ai_used : bool
        True when the AI generator was invoked (vs pure heuristic).
    fallback_count : int
        Number of symbols that fell back to heuristic within this file.
    error : str
        Non-empty if a fatal error occurred for this file.
    """

    path: Path
    symbols_found: int = 0
    symbols_done: int = 0
    ai_used: bool = False
    fallback_count: int = 0
    error: str = ""

    @property
    def done(self) -> bool:
        """Return True when all symbols in this file have been processed.

        Returns
        -------
        bool
            Whether symbols_done equals symbols_found (and symbols_found > 0).
        """
        return self.symbols_found > 0 and self.symbols_done >= self.symbols_found


@dataclass
class RunSummary:
    """Aggregated result from a full parallel run.

    Parameters
    ----------
    changes : dict
        Mapping of Path -> (new_source_text, had_bom) for files that gained
        docstrings.
    skipped_messages : list[str]
        Human-readable messages for skipped or errored symbols/files.
    files_scanned : int
        Total number of Python files examined.
    files_changed : int
        Number of files that will be (or were) written.
    ai_calls : int
        Total number of AI LLM calls made.
    fallback_calls : int
        Total number of symbols that fell back to the heuristic generator.
    """

    changes: dict[Path, tuple[str, bool]] = field(default_factory=dict)
    skipped_messages: list[str] = field(default_factory=list)
    files_scanned: int = 0
    files_changed: int = 0
    ai_calls: int = 0
    fallback_calls: int = 0


# ---------------------------------------------------------------------------
# Processor protocol — satisfied by the patched collect_missing_*  function
# ---------------------------------------------------------------------------


class FileProcessorFn(Protocol):
    """Callable protocol for per-file docstring collection.

    Implementations must be thread-safe (read-only on shared state,
    writes only to returned values).
    """

    def __call__(
        self,
        path: Path,
        *,
        on_symbol_done: Callable[[str, bool], None] | None,
    ) -> tuple[list[tuple[int, list[str]]], list[str], str, bool]:
        """Process one file and return insertion data.

        Parameters
        ----------
        path : Path
            Python source file to process.
        on_symbol_done : callable, optional
            Called with ``(symbol_name, used_ai)`` for each completed symbol.

        Returns
        -------
        insertions : list[tuple[int, list[str]]]
            Line-indexed payloads ready to splice into the source.
        skipped : list[str]
            Human-readable skip/error messages.
        current_text : str
            Original source text of the file.
        had_bom : bool
            Whether the file had a UTF-8 BOM.
        """
        ...


# ---------------------------------------------------------------------------
# Internal per-file worker
# ---------------------------------------------------------------------------


def _process_one_file(
    path: Path,
    processor: FileProcessorFn,
    parse_source_fn: Callable[[str, Path], object],
    apply_insertions_fn: Callable[[str, list], str],
    on_progress: Callable[[FileProgress], None] | None,
    progress: FileProgress,
    stats_lock: threading.Lock,
    ai_calls_counter: list[int],   # mutable int via list
    fallback_counter: list[int],
) -> tuple[Path, tuple[str, bool] | None, list[str]]:
    """Run the full pipeline for a single file and return its result.

    Parameters
    ----------
    path : Path
        Python source file.
    processor : FileProcessorFn
        Per-file insertion collector (thread-safe, read-only on shared state).
    parse_source_fn : callable
        ``parse_source`` from the main module — validates generated output.
    apply_insertions_fn : callable
        ``apply_insertions_to_text`` from the main module.
    on_progress : callable, optional
        Called after each symbol completes with a FileProgress snapshot.
    progress : FileProgress
        Mutable progress object for this file (not shared across files).
    stats_lock : threading.Lock
        Protects the shared counters.
    ai_calls_counter : list[int]
        Single-element list used as a mutable integer counter for AI calls.
    fallback_counter : list[int]
        Single-element list used as a mutable integer counter for fallbacks.

    Returns
    -------
    tuple
        ``(path, (desired_text, had_bom) | None, skipped_messages)``
    """

    def _on_symbol_done(symbol_name: str, used_ai: bool) -> None:
        progress.symbols_done += 1
        if used_ai:
            progress.ai_used = True
            with stats_lock:
                ai_calls_counter[0] += 1
        if on_progress:
            on_progress(FileProgress(
                path=progress.path,
                symbols_found=progress.symbols_found,
                symbols_done=progress.symbols_done,
                ai_used=progress.ai_used,
                fallback_count=progress.fallback_count,
            ))

    def _on_fallback(symbol_name: str, _reason: str) -> None:
        progress.fallback_count += 1
        with stats_lock:
            fallback_counter[0] += 1

    try:
        insertions, skipped, current, had_bom = processor(
            path,
            on_symbol_done=_on_symbol_done,
        )
    except Exception as exc:
        progress.error = str(exc)
        return path, None, [f"{path}: unhandled error during processing; skipped ({exc})"]

    if not insertions:
        return path, None, skipped

    desired = apply_insertions_fn(current, insertions)
    if desired == current:
        return path, None, skipped

    try:
        parse_source_fn(desired, path)
    except SyntaxError as exc:
        skipped.append(
            f"{path}: generated insertion would create invalid syntax; skipped ({exc})"
        )
        return path, None, skipped

    return path, (desired, had_bom), skipped


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def run_parallel(
    paths: list[Path],
    processor: FileProcessorFn,
    parse_source_fn: Callable,
    apply_insertions_fn: Callable,
    *,
    workers: int = 4,
    on_file_progress: Callable[[FileProgress], None] | None = None,
    on_file_complete: Callable[[FileProgress], None] | None = None,
) -> RunSummary:
    """Process *paths* concurrently and return a :class:`RunSummary`.

    This is a drop-in replacement for the sequential ``for path in ...`` loop
    inside ``collect_changes``.  All thread safety is handled internally;
    the caller receives a plain dict of results.

    Parameters
    ----------
    paths : list[Path]
        Python source files to process (already filtered by exclusion rules).
    processor : FileProcessorFn
        Thread-safe per-file insertion collector.
    parse_source_fn : callable
        ``parse_source(text, path) -> ast.Module`` — used to validate output.
    apply_insertions_fn : callable
        ``apply_insertions_to_text(text, insertions) -> str``.
    workers : int, optional
        Maximum concurrent threads.  Default 4.  Set to 1 to disable
        parallelism (useful for debugging).
    on_file_progress : callable, optional
        Called from worker threads with a :class:`FileProgress` snapshot
        after each symbol is processed.  Must be thread-safe (e.g. emit a
        Qt signal rather than touching widgets directly).
    on_file_complete : callable, optional
        Called from worker threads when an entire file finishes.

    Returns
    -------
    RunSummary
        Aggregated results including ``changes`` dict and ``skipped_messages``.
    """
    summary = RunSummary(files_scanned=len(paths))
    stats_lock = threading.Lock()
    ai_calls_counter = [0]
    fallback_counter = [0]

    # Build one FileProgress per path up-front so threads own their own object.
    progress_map: dict[Path, FileProgress] = {
        p: FileProgress(path=p) for p in paths
    }

    futures: dict[Future, Path] = {}

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        for path in paths:
            fut = pool.submit(
                _process_one_file,
                path,
                processor,
                parse_source_fn,
                apply_insertions_fn,
                on_file_progress,
                progress_map[path],
                stats_lock,
                ai_calls_counter,
                fallback_counter,
            )
            futures[fut] = path

        for fut in as_completed(futures):
            path = futures[fut]
            try:
                result_path, file_result, skipped = fut.result()
            except Exception as exc:
                summary.skipped_messages.append(
                    f"{path}: unexpected executor error; skipped ({exc})"
                )
                continue

            summary.skipped_messages.extend(skipped)

            if file_result is not None:
                summary.changes[result_path] = file_result
                summary.files_changed += 1

            prog = progress_map[path]
            if on_file_complete:
                on_file_complete(FileProgress(
                    path=prog.path,
                    symbols_found=prog.symbols_found,
                    symbols_done=prog.symbols_done,
                    ai_used=prog.ai_used,
                    fallback_count=prog.fallback_count,
                    error=prog.error,
                ))

    summary.ai_calls = ai_calls_counter[0]
    summary.fallback_calls = fallback_counter[0]
    return summary
