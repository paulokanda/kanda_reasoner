# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_machine_output.py
"""Read complete analyzer machine output from transient files outside sealed views."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from .advanced_quality_review_contract import AnalysisExecutionStatus
from .analyzer_process_runtime import ProcessExecutionEvidence

__all__ = [
    "load_machine_output_as_stdout",
    "prepare_machine_output_path",
]


def prepare_machine_output_path(
    root: Path,
    engine_id: str,
    label: str,
    suffix: str,
) -> Path:
    """Return one clean transient output path outside the sealed analysis view."""
    path = root.parent / "_aqr_machine_output" / engine_id / (label + suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    return path


def load_machine_output_as_stdout(
    execution: ProcessExecutionEvidence,
    output_path: Path,
) -> ProcessExecutionEvidence:
    """Return execution evidence carrying complete machine-readable output."""
    if execution.status is not AnalysisExecutionStatus.SUCCEEDED:
        return execution
    try:
        data = output_path.read_bytes()
    except OSError:
        return replace(execution, status=AnalysisExecutionStatus.FAILED)
    return replace(
        execution,
        stdout_text=data.decode("utf-8", errors="replace"),
        stdout_bytes_observed=len(data),
        stdout_truncated=False,
    )
