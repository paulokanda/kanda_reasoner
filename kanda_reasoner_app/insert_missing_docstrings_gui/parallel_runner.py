#!/usr/bin/env python3
# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/parallel_runner.py
"""Parallel file-processing engine for the docstring inserter."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Protocol


@dataclass
class FileProgress:
    """Represent file progress."""
    
    path: Path
    symbols_found: int = 0
    symbols_done: int = 0
    ai_used: bool = False
    fallback_count: int = 0
    error: str = ""


@dataclass
class RunSummary:
    """Represent run summary."""
    
    changes: dict[Path, tuple[str, bool]] = field(default_factory=dict)
    skipped_messages: list[str] = field(default_factory=list)
    files_scanned: int = 0
    files_changed: int = 0
    ai_calls: int = 0
    fallback_calls: int = 0


class FileProcessorFn(Protocol):
    """Represent file processor fn."""
    
    def __call__(
        self,
        path: Path,
        *,
        on_symbol_done: Callable[[str, bool], None] | None = None,
    ) -> tuple[list[tuple[int, list[str]]], list[str], str, bool]:
        """Support call behavior.
        
        Parameters
        ----------
        path : Path
            The file or folder path.
        on_symbol_done : Callable[[str, bool], None] | None, optional
            The optional on symbol done value.
        
        Returns
        -------
        tuple[list[tuple[int, list[str]]], list[str], str, bool]
            The tuple of values.
        """
        
        ...


def _process_one_file(
    path: Path,
    processor: FileProcessorFn,
    parse_source_fn: Callable[[str, Path], object],
    apply_insertions_fn: Callable[[str, list], str],
) -> tuple[Path, tuple[str, bool] | None, list[str], FileProgress]:
    """Support process one file behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    processor : FileProcessorFn
        The processor value.
    parse_source_fn : Callable[[str, Path], object]
        The parse source fn value.
    apply_insertions_fn : Callable[[str, list], str]
        The apply insertions fn value.
    
    Returns
    -------
    tuple[Path, tuple[str, bool] | None, list[str], FileProgress]
        The tuple of values.
    """
    
    progress = FileProgress(path=path)

    def _on_symbol_done(_symbol_name: str, used_ai: bool) -> None:
        progress.symbols_found += 1
        progress.symbols_done += 1
        if used_ai:
            progress.ai_used = True
        else:
            progress.fallback_count += 1

    insertions, skipped, current, had_bom = processor(path, on_symbol_done=_on_symbol_done)
    if progress.symbols_found == 0 and insertions:
        progress.symbols_found = len(insertions)
        progress.symbols_done = len(insertions)

    if not insertions:
        return path, None, skipped, progress

    desired = apply_insertions_fn(current, insertions)
    if desired != current:
        try:
            parse_source_fn(desired, path)
        except SyntaxError as exc:
            progress.error = str(exc)
            skipped = list(skipped) + [
                f"{path}: generated insertion would create invalid syntax; skipped ({exc})"
            ]
            return path, None, skipped, progress
        return path, (desired, had_bom), skipped, progress

    return path, None, skipped, progress


def run_parallel(
    *,
    paths: list[Path],
    processor: FileProcessorFn,
    parse_source_fn: Callable[[str, Path], object],
    apply_insertions_fn: Callable[[str, list], str],
    max_workers: int,
    on_file_progress: Callable[[int, int], None] | None = None,
    on_file_complete: Callable[[FileProgress], None] | None = None,
) -> RunSummary:
    """Run the parallel.
    
    Parameters
    ----------
    paths : list[Path]
        The file or folder paths.
    processor : FileProcessorFn
        The processor value.
    parse_source_fn : Callable[[str, Path], object]
        The parse source fn value.
    apply_insertions_fn : Callable[[str, list], str]
        The apply insertions fn value.
    max_workers : int
        The max workers value.
    on_file_progress : Callable[[int, int], None] | None, optional
        The optional on file progress value.
    on_file_complete : Callable[[FileProgress], None] | None, optional
        The optional on file complete value.
    
    Returns
    -------
    RunSummary
        The run summary result.
    """
    
    summary = RunSummary(files_scanned=len(paths))
    done = 0

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(
                _process_one_file,
                path,
                processor,
                parse_source_fn,
                apply_insertions_fn,
            ): path
            for path in paths
        }
        for future in as_completed(futures):
            path, changed, skipped, progress = future.result()
            done += 1
            summary.skipped_messages.extend(skipped)
            if changed is not None:
                summary.changes[path] = changed
                summary.files_changed += 1
            if progress.ai_used:
                summary.ai_calls += progress.symbols_done
            summary.fallback_calls += progress.fallback_count
            if on_file_complete is not None:
                on_file_complete(progress)
            if on_file_progress is not None:
                on_file_progress(done, len(paths))

    return summary
