# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/ruff_fitness_adapter.py  # noqa: E501
"""Ruff fitness adapter for local static quality evidence."""

from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable

from .advanced_quality_evidence_models import (
    FindingLocation,
    FindingSeverity,
    RawEvidenceReference,
    build_normalized_finding,
)
from .advanced_quality_review_contract import AnalysisExecutionStatus
from .analyzer_adapter_contract import (
    AdapterEvidenceBundle,
    AdapterInputPair,
    build_finding_deltas,
    validate_adapter_postconditions,
    validate_adapter_preconditions,
)
from .analyzer_machine_output import (
    load_machine_output_as_stdout,
    prepare_machine_output_path,
)
from .analyzer_process_runtime import (
    BoundedProcessRequest,
    CancellationToken,
    ProcessExecutionEvidence,
    ProcessProgressEvent,
    run_bounded_process,
)
from .ruff_format_comparison import run_ruff_format_comparison

__all__ = [
    "RUFF_FITNESS_CHARACTERISTIC",
    "RuffAdapterOptions",
    "run_ruff_fitness_review",
]

RUFF_FITNESS_CHARACTERISTIC = "local_static_source_quality"


class RuffAdapterOptions:
    """Immutable command policy for one Ruff baseline/Preview review."""

    __slots__ = (
        "argv_prefix",
        "engine_version",
        "extra_check_args",
        "include_format_check",
        "timeout_seconds",
    )

    def __init__(
        self,
        *,
        argv_prefix: Iterable[str],
        engine_version: str,
        extra_check_args: Iterable[str] = (),
        include_format_check: bool = False,
        timeout_seconds: float = 60.0,
    ) -> None:
        prefix = tuple(str(item) for item in argv_prefix)
        if not prefix or not prefix[0].strip():
            raise ValueError("RUFF_ARGV_PREFIX_EMPTY")
        if not str(engine_version or "").strip():
            raise ValueError("RUFF_ENGINE_VERSION_EMPTY")
        if float(timeout_seconds) <= 0:
            raise ValueError("RUFF_TIMEOUT_NOT_POSITIVE")
        self.argv_prefix = prefix
        self.engine_version = str(engine_version).strip()
        self.extra_check_args = tuple(str(item) for item in extra_check_args)
        self.include_format_check = bool(include_format_check)
        self.timeout_seconds = float(timeout_seconds)


def run_ruff_fitness_review(
    inputs: AdapterInputPair,
    options: RuffAdapterOptions,
    *,
    cancellation_token: CancellationToken | None = None,
    progress_callback=None,
) -> AdapterEvidenceBundle:
    """Run Ruff on sealed baseline and Preview trees and compute semantic deltas."""
    blockers = validate_adapter_preconditions(
        inputs,
        engine_id="ruff",
        engine_version=options.engine_version,
    )
    if blockers:
        raise ValueError("RUFF_PRECONDITION_BLOCKED:" + "|".join(blockers))
    token = cancellation_token or CancellationToken()
    baseline_execution = _run_check(
        "baseline",
        Path(inputs.baseline.root_path),
        options,
        token,
        progress_callback,
    )
    preview_execution = _run_check(
        "preview",
        Path(inputs.preview.root_path),
        options,
        token,
        progress_callback,
    )
    raw_evidence = {
        "ruff/baseline.json": baseline_execution.stdout_text.encode("utf-8"),
        "ruff/preview.json": preview_execution.stdout_text.encode("utf-8"),
    }
    diagnostics: list[str] = []
    baseline_findings = _parse_ruff_findings(
        baseline_execution,
        root=Path(inputs.baseline.root_path),
        raw_path="ruff/baseline.json",
        engine_version=options.engine_version,
        diagnostics=diagnostics,
    )
    preview_findings = _parse_ruff_findings(
        preview_execution,
        root=Path(inputs.preview.root_path),
        raw_path="ruff/preview.json",
        engine_version=options.engine_version,
        diagnostics=diagnostics,
    )
    format_status = AnalysisExecutionStatus.SUCCEEDED
    if options.include_format_check:
        format_review = run_ruff_format_comparison(
            inputs,
            argv_prefix=options.argv_prefix,
            timeout_seconds=options.timeout_seconds,
            cancellation_token=token,
            progress_callback=progress_callback,
        )
        format_status = format_review.execution_status
        raw_evidence.update(dict(format_review.raw_evidence))
        diagnostics.extend(format_review.diagnostics)
    post_blockers = validate_adapter_postconditions(inputs, raw_evidence=raw_evidence)
    if post_blockers:
        raise RuntimeError("RUFF_POSTCONDITION_BLOCKED:" + "|".join(post_blockers))
    execution_status = _combined_status(
        baseline_execution,
        preview_execution,
        diagnostics,
        format_status=format_status,
    )
    return AdapterEvidenceBundle(
        engine_id="ruff",
        engine_version=options.engine_version,
        protected_characteristic=RUFF_FITNESS_CHARACTERISTIC,
        analysis_identity_hash=inputs.analysis_identity.identity_hash,
        execution_status=execution_status,
        baseline_execution=baseline_execution,
        preview_execution=preview_execution,
        baseline_findings=baseline_findings,
        preview_findings=preview_findings,
        deltas=build_finding_deltas(baseline_findings, preview_findings),
        raw_evidence=tuple(sorted(raw_evidence.items())),
        diagnostics=tuple(sorted(set(diagnostics))),
    )


def _run_check(
    label: str,
    root: Path,
    options: RuffAdapterOptions,
    token: CancellationToken,
    progress_callback,
) -> ProcessExecutionEvidence:
    output_path = prepare_machine_output_path(root, "ruff", label, ".json")
    argv_items = [
        *options.argv_prefix,
        "check",
        str(root),
        "--output-format",
        "json",
        "--output-file",
        str(output_path),
        "--exit-zero",
        "--no-fix",
        "--no-unsafe-fixes",
        "--no-preview",
        "--no-cache",
        "--force-exclude",
        "--color",
        "never",
    ]
    for item in options.extra_check_args:
        if item not in argv_items:
            argv_items.append(item)
    argv = tuple(argv_items)
    if "--fix" in argv or "--unsafe-fixes" in argv:
        raise ValueError("RUFF_MUTATING_ARGUMENT_FORBIDDEN")
    execution = run_bounded_process(
        BoundedProcessRequest(
            engine_id="ruff_" + label,
            argv=tuple(argv),
            cwd=str(root),
            timeout_seconds=options.timeout_seconds,
        ),
        cancellation_token=token,
        progress_callback=_prefix_progress(progress_callback, "ruff:" + label),
    )
    return load_machine_output_as_stdout(execution, output_path)


def _parse_ruff_findings(
    execution: ProcessExecutionEvidence,
    *,
    root: Path,
    raw_path: str,
    engine_version: str,
    diagnostics: list[str],
) -> tuple:
    if execution.status is not AnalysisExecutionStatus.SUCCEEDED:
        diagnostics.append(
            execution.engine_id + ":PROCESS_STATUS=" + execution.status.value
        )
        return ()
    try:
        payload = json.loads(execution.stdout_text or "[]")
    except json.JSONDecodeError as error:
        diagnostics.append(execution.engine_id + ":MALFORMED_JSON:" + str(error))
        return ()
    if not isinstance(payload, list):
        diagnostics.append(execution.engine_id + ":RUFF_JSON_ROOT_NOT_LIST")
        return ()
    raw_bytes = execution.stdout_text.encode("utf-8")
    reference = RawEvidenceReference(
        engine_id="ruff",
        relative_path=raw_path,
        sha256=hashlib.sha256(raw_bytes).hexdigest(),
        byte_size=len(raw_bytes),
    )
    findings = []
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            diagnostics.append(execution.engine_id + f":ITEM_{index}_NOT_OBJECT")
            continue
        try:
            code = str(item["code"]).strip()
            message = str(item["message"]).strip()
            path = _relative_path(root, str(item["filename"]))
            location = item.get("location") or {}
            end_location = item.get("end_location") or {}
            findings.append(
                build_normalized_finding(
                    engine_id="ruff",
                    engine_version=engine_version,
                    rule_id=code,
                    normalized_relative_path=path,
                    symbol_identity="",
                    normalized_message_signature=_message_signature(message),
                    severity=FindingSeverity.ERROR,
                    location=FindingLocation(
                        line=int(location.get("row") or 0),
                        column=int(location.get("column") or 0),
                        end_line=int(end_location.get("row") or 0),
                        end_column=int(end_location.get("column") or 0),
                    ),
                    raw_evidence_reference=reference,
                    metadata=(("message", message),),
                )
            )
        except (KeyError, TypeError, ValueError) as error:
            diagnostics.append(execution.engine_id + f":ITEM_{index}_INVALID:{error}")
    return tuple(sorted(findings, key=lambda item: item.semantic_key))


def _combined_status(
    baseline: ProcessExecutionEvidence,
    preview: ProcessExecutionEvidence,
    diagnostics: list[str],
    *,
    format_status: AnalysisExecutionStatus,
) -> AnalysisExecutionStatus:
    statuses = {baseline.status, preview.status}
    if AnalysisExecutionStatus.CANCELLED in statuses:
        return AnalysisExecutionStatus.CANCELLED
    if AnalysisExecutionStatus.TIMED_OUT in statuses:
        return AnalysisExecutionStatus.TIMED_OUT
    if AnalysisExecutionStatus.FAILED in statuses:
        return AnalysisExecutionStatus.FAILED
    if format_status is not AnalysisExecutionStatus.SUCCEEDED:
        return format_status
    if diagnostics:
        return AnalysisExecutionStatus.FAILED
    return AnalysisExecutionStatus.SUCCEEDED


def _relative_path(root: Path, filename: str) -> str:
    candidate = Path(filename)
    if not candidate.is_absolute():
        candidate = (root / candidate).resolve(strict=False)
    else:
        candidate = candidate.resolve(strict=False)
    try:
        return candidate.relative_to(root.resolve(strict=False)).as_posix()
    except ValueError as error:
        raise ValueError("RUFF_FINDING_PATH_OUTSIDE_INPUT_ROOT") from error


def _message_signature(message: str) -> str:
    compact = re.sub(r"\s+", " ", str(message or "").strip().lower())
    return re.sub(r"\b\d+\b", "<n>", compact)


def _prefix_progress(callback, prefix: str):
    if callback is None:
        return None

    def forward(event: ProcessProgressEvent) -> None:
        callback(
            replace(
                event,
                message=prefix + " " + event.message,
            )
        )

    return forward
