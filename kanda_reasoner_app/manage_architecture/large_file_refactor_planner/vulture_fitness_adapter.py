# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/vulture_fitness_adapter.py
"""Vulture advisory fitness adapter for newly orphaned code candidates."""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
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
from .analyzer_process_runtime import (
    BoundedProcessRequest,
    CancellationToken,
    ProcessExecutionEvidence,
    run_bounded_process,
)
from .analyzer_specific_delta_strategies import (
    VultureCandidateDelta,
    build_vulture_candidate_deltas,
)

__all__ = [
    "VULTURE_FITNESS_CHARACTERISTIC",
    "VultureAdapterOptions",
    "VultureFitnessReviewResult",
    "run_vulture_fitness_review",
]

VULTURE_FITNESS_CHARACTERISTIC = "newly_orphaned_code_candidate_advisory"
_LINE_PATTERN = re.compile(
    r"^(.*):(\d+):\s+(.*?)\s+\((\d+)% confidence\)\s*$"
)
_UNUSED_PATTERN = re.compile(r"^unused\s+(.+?)\s+'([^']+)'$")


@dataclass(frozen=True)
class VultureFitnessReviewResult:
    """Keep advisory Vulture evidence and candidate deltas explicit."""

    bundle: AdapterEvidenceBundle
    candidate_deltas: tuple[VultureCandidateDelta, ...]


class VultureAdapterOptions:
    """Immutable command policy for one Vulture baseline/Preview review."""

    __slots__ = (
        "argv_prefix",
        "engine_version",
        "extra_args",
        "min_confidence",
        "timeout_seconds",
    )

    def __init__(
        self,
        *,
        argv_prefix: Iterable[str],
        engine_version: str,
        min_confidence: int = 60,
        extra_args: Iterable[str] = (),
        timeout_seconds: float = 60.0,
    ) -> None:
        prefix = tuple(str(item) for item in argv_prefix)
        if not prefix or not prefix[0].strip():
            raise ValueError("VULTURE_ARGV_PREFIX_EMPTY")
        if not str(engine_version or "").strip():
            raise ValueError("VULTURE_ENGINE_VERSION_EMPTY")
        confidence = int(min_confidence)
        if confidence < 0 or confidence > 100:
            raise ValueError("VULTURE_MIN_CONFIDENCE_OUT_OF_RANGE")
        if float(timeout_seconds) <= 0:
            raise ValueError("VULTURE_TIMEOUT_NOT_POSITIVE")
        self.argv_prefix = prefix
        self.engine_version = str(engine_version).strip()
        self.min_confidence = confidence
        self.extra_args = tuple(str(item) for item in extra_args)
        self.timeout_seconds = float(timeout_seconds)


def run_vulture_fitness_review(
    inputs: AdapterInputPair,
    options: VultureAdapterOptions,
    *,
    cancellation_token: CancellationToken | None = None,
    progress_callback=None,
) -> VultureFitnessReviewResult:
    """Run advisory Vulture evidence collection on sealed baseline and Preview."""
    blockers = validate_adapter_preconditions(
        inputs,
        engine_id="vulture",
        engine_version=options.engine_version,
    )
    if blockers:
        raise ValueError("VULTURE_PRECONDITION_BLOCKED:" + "|".join(blockers))
    token = cancellation_token or CancellationToken()
    baseline_execution = _run_vulture(
        "baseline",
        Path(inputs.baseline.root_path),
        options,
        token,
        progress_callback,
    )
    preview_execution = _run_vulture(
        "preview",
        Path(inputs.preview.root_path),
        options,
        token,
        progress_callback,
    )
    baseline_execution = _normalize_expected_vulture_exit(baseline_execution)
    preview_execution = _normalize_expected_vulture_exit(preview_execution)
    raw_evidence = {
        "vulture/baseline.txt": _execution_text(baseline_execution).encode("utf-8"),
        "vulture/preview.txt": _execution_text(preview_execution).encode("utf-8"),
    }
    diagnostics: list[str] = []
    baseline_findings = _parse_vulture_findings(
        baseline_execution,
        root=Path(inputs.baseline.root_path),
        raw_path="vulture/baseline.txt",
        engine_version=options.engine_version,
        diagnostics=diagnostics,
    )
    preview_findings = _parse_vulture_findings(
        preview_execution,
        root=Path(inputs.preview.root_path),
        raw_path="vulture/preview.txt",
        engine_version=options.engine_version,
        diagnostics=diagnostics,
    )
    post_blockers = validate_adapter_postconditions(inputs, raw_evidence=raw_evidence)
    if post_blockers:
        raise RuntimeError("VULTURE_POSTCONDITION_BLOCKED:" + "|".join(post_blockers))
    execution_status = _combined_status(
        baseline_execution,
        preview_execution,
        diagnostics,
    )
    bundle = AdapterEvidenceBundle(
        engine_id="vulture",
        engine_version=options.engine_version,
        protected_characteristic=VULTURE_FITNESS_CHARACTERISTIC,
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
    return VultureFitnessReviewResult(
        bundle=bundle,
        candidate_deltas=build_vulture_candidate_deltas(
            baseline_findings,
            preview_findings,
        ),
    )


def _run_vulture(
    label: str,
    root: Path,
    options: VultureAdapterOptions,
    token: CancellationToken,
    progress_callback,
) -> ProcessExecutionEvidence:
    """Run one Vulture CLI analysis through the frozen bounded runtime."""
    argv = (
        *options.argv_prefix,
        str(root),
        "--min-confidence",
        str(options.min_confidence),
        *options.extra_args,
    )
    return run_bounded_process(
        BoundedProcessRequest(
            engine_id="vulture_" + label,
            argv=tuple(argv),
            cwd=str(root),
            timeout_seconds=options.timeout_seconds,
        ),
        cancellation_token=token,
        progress_callback=progress_callback,
    )


def _normalize_expected_vulture_exit(
    execution: ProcessExecutionEvidence,
) -> ProcessExecutionEvidence:
    """Treat Vulture exit code 3 as completed analysis with dead-code findings."""
    if execution.exit_code == 3 and execution.status is AnalysisExecutionStatus.FAILED:
        return replace(execution, status=AnalysisExecutionStatus.SUCCEEDED)
    return execution


def _parse_vulture_findings(
    execution: ProcessExecutionEvidence,
    *,
    root: Path,
    raw_path: str,
    engine_version: str,
    diagnostics: list[str],
) -> tuple:
    """Parse documented Vulture text findings while keeping confidence advisory."""
    if execution.status is not AnalysisExecutionStatus.SUCCEEDED:
        diagnostics.append(execution.engine_id + ":PROCESS_STATUS=" + execution.status.value)
        return ()
    raw_bytes = _execution_text(execution).encode("utf-8")
    reference = RawEvidenceReference(
        engine_id="vulture",
        relative_path=raw_path,
        sha256=hashlib.sha256(raw_bytes).hexdigest(),
        byte_size=len(raw_bytes),
    )
    findings = []
    for line_number, line in enumerate(execution.stdout_text.splitlines(), start=1):
        if not line.strip():
            continue
        match = _LINE_PATTERN.match(line)
        if match is None:
            diagnostics.append(
                execution.engine_id + f":OUTPUT_LINE_{line_number}_UNPARSEABLE"
            )
            continue
        filename, source_line, body, confidence_text = match.groups()
        try:
            relative_path = _relative_path(root, filename)
            confidence = int(confidence_text)
        except ValueError as error:
            diagnostics.append(
                execution.engine_id + f":OUTPUT_LINE_{line_number}_INVALID:{error}"
            )
            continue
        kind, symbol = _candidate_identity(body)
        findings.append(
            build_normalized_finding(
                engine_id="vulture",
                engine_version=engine_version,
                rule_id="VULTURE_" + _rule_token(kind),
                normalized_relative_path=relative_path,
                symbol_identity=symbol,
                normalized_message_signature="unused candidate:" + kind,
                severity=FindingSeverity.ADVISORY,
                location=FindingLocation(line=int(source_line)),
                raw_evidence_reference=reference,
                metadata=(
                    ("candidate_kind", kind),
                    ("engine_confidence", str(confidence)),
                    ("engine_confidence_semantics", "vulture_heuristic_not_probability"),
                    ("raw_message", body),
                ),
            )
        )
    return tuple(sorted(findings, key=lambda item: item.semantic_key))


def _candidate_identity(body: str) -> tuple[str, str]:
    """Return stable Vulture candidate kind and symbol identity."""
    text = " ".join(str(body or "").split())
    match = _UNUSED_PATTERN.match(text)
    if match is not None:
        kind = match.group(1).strip().lower().replace(" ", "_")
        symbol = match.group(2).strip()
        return kind, symbol
    if text.lower().startswith("unreachable code"):
        return "unreachable_code", text.lower()
    return "candidate", text


def _rule_token(kind: str) -> str:
    """Return safe uppercase rule token from candidate kind."""
    token = re.sub(r"[^A-Za-z0-9_]+", "_", str(kind or "candidate"))
    return token.strip("_").upper() or "CANDIDATE"


def _relative_path(root: Path, filename: str) -> str:
    """Normalize Vulture path against one sealed analyzed tree."""
    candidate = Path(filename)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve(strict=False)
    try:
        return resolved.relative_to(root.resolve(strict=False)).as_posix()
    except ValueError as error:
        raise ValueError("VULTURE_FINDING_PATH_OUTSIDE_ANALYSIS_ROOT") from error


def _execution_text(execution: ProcessExecutionEvidence) -> str:
    """Return deterministic raw Vulture text evidence including stderr diagnostics."""
    parts = [execution.stdout_text]
    if execution.stderr_text:
        parts.append("--- STDERR ---\n" + execution.stderr_text)
    return "\n".join(parts)


def _combined_status(
    baseline: ProcessExecutionEvidence,
    preview: ProcessExecutionEvidence,
    diagnostics: list[str],
) -> AnalysisExecutionStatus:
    """Combine process and parser states while preserving advisory failure evidence."""
    statuses = (baseline.status, preview.status)
    if any(status is AnalysisExecutionStatus.TIMED_OUT for status in statuses):
        return AnalysisExecutionStatus.TIMED_OUT
    if any(status is AnalysisExecutionStatus.CANCELLED for status in statuses):
        return AnalysisExecutionStatus.CANCELLED
    if any(status is not AnalysisExecutionStatus.SUCCEEDED for status in statuses):
        return AnalysisExecutionStatus.FAILED
    if diagnostics:
        return AnalysisExecutionStatus.FAILED
    return AnalysisExecutionStatus.SUCCEEDED
