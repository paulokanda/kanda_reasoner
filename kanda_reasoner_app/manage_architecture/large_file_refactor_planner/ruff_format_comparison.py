# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ruff_format_comparison.py  # noqa: E501
"""Read-only Ruff formatter comparison for sealed AQR baseline and Preview trees."""

from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from enum import Enum
import json
from pathlib import Path
import re
from typing import Iterable

from .advanced_quality_review_contract import AnalysisExecutionStatus
from .analyzer_adapter_contract import AdapterInputPair
from .analyzer_process_runtime import (
    BoundedProcessRequest,
    CancellationToken,
    ProcessExecutionEvidence,
    ProcessProgressEvent,
    run_bounded_process,
)

__all__ = [
    "RUFF_FORMAT_COMPARISON_EVIDENCE_PATH",
    "RuffFormatComparisonSummary",
    "RuffFormatReviewResult",
    "load_ruff_format_comparison_summary",
    "run_ruff_format_comparison",
]

RUFF_FORMAT_COMPARISON_EVIDENCE_PATH = "ruff/format_comparison.json"
_REQUIRED_LINE = re.compile(r"^Would reformat:\s+(?P<path>.+?)\s*$")


class RuffFormatState(str, Enum):
    """Describe one read-only Ruff formatter check result."""

    CLEAN = "CLEAN"
    NEEDS_FORMATTING = "NEEDS_FORMATTING"
    EXECUTION_FAILED = "EXECUTION_FAILED"


@dataclass(frozen=True)
class RuffFormatSideEvidence:
    """Store one formatter execution and normalized affected paths."""

    label: str
    state: RuffFormatState
    required_paths: tuple[str, ...]
    execution: ProcessExecutionEvidence

    def to_dict(self) -> dict[str, object]:
        """Return deterministic JSON-ready side evidence."""
        return {
            "label": self.label,
            "state": self.state.value,
            "required_paths": list(self.required_paths),
            "execution": self.execution.to_dict(),
        }


@dataclass(frozen=True)
class RuffFormatComparisonSummary:
    """Represent exact baseline-to-Preview formatter path deltas."""

    baseline_state: RuffFormatState
    preview_state: RuffFormatState
    baseline_required_paths: tuple[str, ...]
    preview_required_paths: tuple[str, ...]
    new_required_paths: tuple[str, ...]
    resolved_required_paths: tuple[str, ...]
    persistent_required_paths: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        """Return deterministic JSON-ready comparison evidence."""
        payload = asdict(self)
        payload["baseline_state"] = self.baseline_state.value
        payload["preview_state"] = self.preview_state.value
        for key in (
            "baseline_required_paths",
            "preview_required_paths",
            "new_required_paths",
            "resolved_required_paths",
            "persistent_required_paths",
        ):
            payload[key] = list(payload[key])
        return payload


@dataclass(frozen=True)
class RuffFormatReviewResult:
    """Return formatter status, raw evidence, and diagnostics to the Ruff adapter."""

    execution_status: AnalysisExecutionStatus
    summary: RuffFormatComparisonSummary
    baseline_execution: ProcessExecutionEvidence
    preview_execution: ProcessExecutionEvidence
    raw_evidence: tuple[tuple[str, bytes], ...]
    diagnostics: tuple[str, ...]


def run_ruff_format_comparison(
    inputs: AdapterInputPair,
    *,
    argv_prefix: Iterable[str],
    timeout_seconds: float = 60.0,
    cancellation_token: CancellationToken | None = None,
    progress_callback=None,
) -> RuffFormatReviewResult:
    """Compare formatter requirements without modifying either sealed source tree."""
    prefix = tuple(str(item) for item in argv_prefix)
    if not prefix or not prefix[0].strip():
        raise ValueError("RUFF_FORMAT_ARGV_PREFIX_EMPTY")
    token = cancellation_token or CancellationToken()
    baseline = _run_format_check(
        "baseline",
        Path(inputs.baseline.root_path),
        prefix=prefix,
        timeout_seconds=timeout_seconds,
        token=token,
        progress_callback=progress_callback,
    )
    preview = _run_format_check(
        "preview",
        Path(inputs.preview.root_path),
        prefix=prefix,
        timeout_seconds=timeout_seconds,
        token=token,
        progress_callback=progress_callback,
    )
    diagnostics: list[str] = []
    baseline_side = _interpret_format_execution(
        baseline,
        label="baseline",
        root=Path(inputs.baseline.root_path),
        diagnostics=diagnostics,
    )
    preview_side = _interpret_format_execution(
        preview,
        label="preview",
        root=Path(inputs.preview.root_path),
        diagnostics=diagnostics,
    )
    summary = _build_summary(baseline_side, preview_side)
    status = _combined_status(baseline_side, preview_side)
    comparison_payload = {
        "schema_version": "1.0",
        "execution_status": status.value,
        "baseline": baseline_side.to_dict(),
        "preview": preview_side.to_dict(),
        "comparison": summary.to_dict(),
    }
    comparison_bytes = (
        json.dumps(comparison_payload, sort_keys=True, indent=2, ensure_ascii=True)
        + "\n"
    ).encode("utf-8")
    raw_evidence = {
        "ruff/format_baseline.txt": _execution_text(baseline),
        "ruff/format_preview.txt": _execution_text(preview),
        RUFF_FORMAT_COMPARISON_EVIDENCE_PATH: comparison_bytes,
    }
    return RuffFormatReviewResult(
        execution_status=status,
        summary=summary,
        baseline_execution=baseline,
        preview_execution=preview,
        raw_evidence=tuple(sorted(raw_evidence.items())),
        diagnostics=tuple(sorted(set(diagnostics))),
    )


def load_ruff_format_comparison_summary(
    raw_evidence: dict[str, bytes],
) -> RuffFormatComparisonSummary | None:
    """Load persisted formatter comparison evidence for cross-check policy."""
    data = raw_evidence.get(RUFF_FORMAT_COMPARISON_EVIDENCE_PATH)
    if data is None:
        return None
    try:
        payload = json.loads(data.decode("utf-8"))
        comparison = payload["comparison"]
        return RuffFormatComparisonSummary(
            baseline_state=RuffFormatState(comparison["baseline_state"]),
            preview_state=RuffFormatState(comparison["preview_state"]),
            baseline_required_paths=_string_tuple(
                comparison["baseline_required_paths"]
            ),
            preview_required_paths=_string_tuple(comparison["preview_required_paths"]),
            new_required_paths=_string_tuple(comparison["new_required_paths"]),
            resolved_required_paths=_string_tuple(
                comparison["resolved_required_paths"]
            ),
            persistent_required_paths=_string_tuple(
                comparison["persistent_required_paths"]
            ),
        )
    except (
        KeyError,
        TypeError,
        ValueError,
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as error:
        raise ValueError("RUFF_FORMAT_COMPARISON_EVIDENCE_INVALID") from error


def _run_format_check(
    label: str,
    root: Path,
    *,
    prefix: tuple[str, ...],
    timeout_seconds: float,
    token: CancellationToken,
    progress_callback,
) -> ProcessExecutionEvidence:
    argv = [
        *prefix,
        "format",
        "--check",
        "--no-preview",
        "--no-cache",
        "--force-exclude",
        "--color",
        "never",
    ]
    argv.append(str(root))
    _validate_read_only_argv(argv)
    return run_bounded_process(
        BoundedProcessRequest(
            engine_id="ruff_format_" + label,
            argv=tuple(argv),
            cwd=str(root),
            timeout_seconds=timeout_seconds,
        ),
        cancellation_token=token,
        progress_callback=_prefix_progress(
            progress_callback,
            "ruff:format:" + label,
        ),
    )


def _interpret_format_execution(
    execution: ProcessExecutionEvidence,
    *,
    label: str,
    root: Path,
    diagnostics: list[str],
) -> RuffFormatSideEvidence:
    if (
        execution.status is AnalysisExecutionStatus.SUCCEEDED
        and execution.exit_code == 0
    ):
        return RuffFormatSideEvidence(label, RuffFormatState.CLEAN, (), execution)
    if execution.status is AnalysisExecutionStatus.FAILED and execution.exit_code == 1:
        required_paths = _parse_required_paths(execution, root=root)
        if not required_paths:
            diagnostics.append("RUFF_FORMAT_REQUIRED_PATHS_UNPARSED:" + label)
            return RuffFormatSideEvidence(
                label,
                RuffFormatState.EXECUTION_FAILED,
                (),
                execution,
            )
        return RuffFormatSideEvidence(
            label,
            RuffFormatState.NEEDS_FORMATTING,
            required_paths,
            execution,
        )
    diagnostics.append(
        "RUFF_FORMAT_EXECUTION_FAILED:"
        + label
        + ":"
        + execution.status.value
        + ":exit="
        + str(execution.exit_code)
    )
    return RuffFormatSideEvidence(
        label,
        RuffFormatState.EXECUTION_FAILED,
        (),
        execution,
    )


def _parse_required_paths(
    execution: ProcessExecutionEvidence,
    *,
    root: Path,
) -> tuple[str, ...]:
    result: list[str] = []
    combined = execution.stdout_text + "\n" + execution.stderr_text
    for raw_line in combined.splitlines():
        match = _REQUIRED_LINE.match(raw_line.strip())
        if not match:
            continue
        result.append(_relative_path(root, match.group("path")))
    return tuple(sorted(set(result)))


def _relative_path(root: Path, raw_path: str) -> str:
    candidate = Path(str(raw_path).strip().strip('"'))
    if not candidate.is_absolute():
        candidate = (root / candidate).resolve(strict=False)
    else:
        candidate = candidate.resolve(strict=False)
    try:
        return candidate.relative_to(root.resolve(strict=False)).as_posix()
    except ValueError as error:
        raise ValueError("RUFF_FORMAT_PATH_OUTSIDE_INPUT_ROOT") from error


def _build_summary(
    baseline: RuffFormatSideEvidence,
    preview: RuffFormatSideEvidence,
) -> RuffFormatComparisonSummary:
    baseline_paths = set(baseline.required_paths)
    preview_paths = set(preview.required_paths)
    return RuffFormatComparisonSummary(
        baseline_state=baseline.state,
        preview_state=preview.state,
        baseline_required_paths=tuple(sorted(baseline_paths)),
        preview_required_paths=tuple(sorted(preview_paths)),
        new_required_paths=tuple(sorted(preview_paths - baseline_paths)),
        resolved_required_paths=tuple(sorted(baseline_paths - preview_paths)),
        persistent_required_paths=tuple(sorted(baseline_paths & preview_paths)),
    )


def _combined_status(
    baseline: RuffFormatSideEvidence,
    preview: RuffFormatSideEvidence,
) -> AnalysisExecutionStatus:
    executions = (baseline.execution, preview.execution)
    statuses = {item.status for item in executions}
    if AnalysisExecutionStatus.CANCELLED in statuses:
        return AnalysisExecutionStatus.CANCELLED
    if AnalysisExecutionStatus.TIMED_OUT in statuses:
        return AnalysisExecutionStatus.TIMED_OUT
    if RuffFormatState.EXECUTION_FAILED in {baseline.state, preview.state}:
        return AnalysisExecutionStatus.FAILED
    return AnalysisExecutionStatus.SUCCEEDED


def _validate_read_only_argv(argv: Iterable[str]) -> None:
    values = tuple(str(item) for item in argv)
    forbidden = {"--fix", "--fix-only", "--unsafe-fixes"}
    if forbidden & set(values):
        raise ValueError("RUFF_FORMAT_MUTATING_ARGUMENT_FORBIDDEN")
    if "--check" not in values or "format" not in values:
        raise ValueError("RUFF_FORMAT_READ_ONLY_CHECK_REQUIRED")
    if "--output-format" in values:
        raise ValueError("RUFF_FORMAT_UNSUPPORTED_OUTPUT_FORMAT_FORBIDDEN")


def _execution_text(execution: ProcessExecutionEvidence) -> bytes:
    return (execution.stdout_text + "\n" + execution.stderr_text).encode("utf-8")


def _string_tuple(value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("RUFF_FORMAT_COMPARISON_PATHS_INVALID")
    return tuple(value)


def _prefix_progress(callback, prefix: str):
    if callback is None:
        return None

    def forward(event: ProcessProgressEvent) -> None:
        callback(replace(event, message=prefix + " " + event.message))

    return forward
