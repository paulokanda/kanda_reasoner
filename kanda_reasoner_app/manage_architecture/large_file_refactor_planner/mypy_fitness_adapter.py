# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/mypy_fitness_adapter.py
"""Conditional mypy fitness adapter with conservative relocation-aware deltas."""
from __future__ import annotations

from dataclasses import dataclass, replace
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
from .analyzer_environment_contract import AnalyzerCapabilityMode
from .analyzer_process_runtime import (
    BoundedProcessRequest,
    CancellationToken,
    ProcessExecutionEvidence,
    run_bounded_process,
)
from .analyzer_specific_delta_strategies import (
    MypyFindingDelta,
    build_mypy_relocation_deltas,
)
from .workbench_project_support_paths import (
    analyzer_cache_root_blockers,
    analyzer_engine_cache_root,
)

__all__ = [
    "MYPY_FITNESS_CHARACTERISTIC",
    "MypyAdapterOptions",
    "MypyFitnessReviewResult",
    "run_mypy_fitness_review",
]

MYPY_FITNESS_CHARACTERISTIC = "type_contract_regression"


@dataclass(frozen=True)
class MypyFitnessReviewResult:
    """Return conditional mypy evidence without pretending unconfigured means PASS."""

    capability_mode: AnalyzerCapabilityMode
    executed: bool
    bundle: AdapterEvidenceBundle | None
    relocation_deltas: tuple[MypyFindingDelta, ...]
    diagnostic: str


class MypyAdapterOptions:
    """Immutable command, capability, config, and cache policy for mypy review."""

    __slots__ = (
        "active_project_root",
        "analysis_key",
        "argv_prefix",
        "capability_mode",
        "config_file",
        "config_hash",
        "engine_version",
        "extra_args",
        "timeout_seconds",
    )

    def __init__(
        self,
        *,
        argv_prefix: Iterable[str],
        engine_version: str,
        capability_mode: AnalyzerCapabilityMode,
        active_project_root: str | Path,
        config_hash: str,
        analysis_key: str,
        config_file: str | Path | None = None,
        extra_args: Iterable[str] = (),
        timeout_seconds: float = 120.0,
    ) -> None:
        prefix = tuple(str(item) for item in argv_prefix)
        if not prefix or not prefix[0].strip():
            raise ValueError("MYPY_ARGV_PREFIX_EMPTY")
        if not str(engine_version or "").strip():
            raise ValueError("MYPY_ENGINE_VERSION_EMPTY")
        if not str(config_hash or "").strip():
            raise ValueError("MYPY_CONFIG_HASH_EMPTY")
        if not str(analysis_key or "").strip():
            raise ValueError("MYPY_ANALYSIS_KEY_EMPTY")
        if float(timeout_seconds) <= 0:
            raise ValueError("MYPY_TIMEOUT_NOT_POSITIVE")
        self.argv_prefix = prefix
        self.engine_version = str(engine_version).strip()
        self.capability_mode = capability_mode
        self.active_project_root = str(
            Path(active_project_root).expanduser().resolve(strict=False)
        )
        self.config_hash = str(config_hash).strip()
        self.analysis_key = str(analysis_key).strip()
        self.config_file = (
            str(Path(config_file).expanduser().resolve(strict=False))
            if config_file is not None
            else ""
        )
        self.extra_args = tuple(str(item) for item in extra_args)
        self.timeout_seconds = float(timeout_seconds)


def run_mypy_fitness_review(
    inputs: AdapterInputPair,
    options: MypyAdapterOptions,
    *,
    cancellation_token: CancellationToken | None = None,
    progress_callback=None,
) -> MypyFitnessReviewResult:
    """Run mypy only when capability policy permits execution."""
    if options.capability_mode in {
        AnalyzerCapabilityMode.NOT_CONFIGURED,
        AnalyzerCapabilityMode.UNAVAILABLE,
    }:
        return MypyFitnessReviewResult(
            capability_mode=options.capability_mode,
            executed=False,
            bundle=None,
            relocation_deltas=(),
            diagnostic="MYPY_CAPABILITY_MODE=" + options.capability_mode.value,
        )
    blockers = validate_adapter_preconditions(
        inputs,
        engine_id="mypy",
        engine_version=options.engine_version,
    )
    if blockers:
        raise ValueError("MYPY_PRECONDITION_BLOCKED:" + "|".join(blockers))
    cache_root = analyzer_engine_cache_root(
        options.active_project_root,
        engine_id="mypy",
        engine_version=options.engine_version,
        config_hash=options.config_hash,
        analysis_key=options.analysis_key,
    )
    cache_blockers = analyzer_cache_root_blockers(
        options.active_project_root,
        cache_root,
    )
    if cache_blockers:
        raise ValueError("MYPY_CACHE_OWNERSHIP_BLOCKED:" + "|".join(cache_blockers))
    cache_root.mkdir(parents=True, exist_ok=True)
    token = cancellation_token or CancellationToken()
    analysis_target = _analysis_target_relative(
        inputs.analysis_identity.target_relative_path
    )
    baseline_execution = _run_mypy(
        "baseline",
        Path(inputs.baseline.root_path),
        cache_root / "baseline",
        options,
        token,
        progress_callback,
        analysis_target,
    )
    preview_execution = _run_mypy(
        "preview",
        Path(inputs.preview.root_path),
        cache_root / "preview",
        options,
        token,
        progress_callback,
        analysis_target,
    )
    baseline_execution = _normalize_expected_mypy_exit(baseline_execution)
    preview_execution = _normalize_expected_mypy_exit(preview_execution)
    raw_evidence = {
        "mypy/baseline.jsonl": baseline_execution.stdout_text.encode("utf-8"),
        "mypy/preview.jsonl": preview_execution.stdout_text.encode("utf-8"),
    }
    diagnostics: list[str] = []
    baseline_findings = _parse_mypy_findings(
        baseline_execution,
        root=Path(inputs.baseline.root_path),
        raw_path="mypy/baseline.jsonl",
        engine_version=options.engine_version,
        diagnostics=diagnostics,
    )
    preview_findings = _parse_mypy_findings(
        preview_execution,
        root=Path(inputs.preview.root_path),
        raw_path="mypy/preview.jsonl",
        engine_version=options.engine_version,
        diagnostics=diagnostics,
    )
    post_blockers = validate_adapter_postconditions(inputs, raw_evidence=raw_evidence)
    if post_blockers:
        raise RuntimeError("MYPY_POSTCONDITION_BLOCKED:" + "|".join(post_blockers))
    execution_status = _combined_status(
        baseline_execution,
        preview_execution,
        diagnostics,
    )
    bundle = AdapterEvidenceBundle(
        engine_id="mypy",
        engine_version=options.engine_version,
        protected_characteristic=MYPY_FITNESS_CHARACTERISTIC,
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
    return MypyFitnessReviewResult(
        capability_mode=options.capability_mode,
        executed=True,
        bundle=bundle,
        relocation_deltas=build_mypy_relocation_deltas(
            baseline_findings,
            preview_findings,
        ),
        diagnostic="",
    )


def _run_mypy(
    label: str,
    root: Path,
    cache_dir: Path,
    options: MypyAdapterOptions,
    token: CancellationToken,
    progress_callback,
    analysis_target: str,
) -> ProcessExecutionEvidence:
    """Run mypy JSON output through the frozen bounded process runtime."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    argv = [
        *options.argv_prefix,
        "--output",
        "json",
        "--show-error-end",
        "--no-error-summary",
        "--explicit-package-bases",
        "--cache-dir",
        str(cache_dir),
    ]
    if options.config_file:
        argv.extend(("--config-file", options.config_file))
    argv.extend(options.extra_args)
    argv.append(analysis_target)
    return run_bounded_process(
        BoundedProcessRequest(
            engine_id="mypy_" + label,
            argv=tuple(argv),
            cwd=str(root),
            timeout_seconds=options.timeout_seconds,
        ),
        cancellation_token=token,
        progress_callback=progress_callback,
    )


def _analysis_target_relative(target_relative_path: str) -> str:
    """Return the bounded package directory containing the refactor target."""
    path = Path(str(target_relative_path or "").replace("\\", "/"))
    if not str(path).strip() or path.is_absolute() or ".." in path.parts:
        raise ValueError("MYPY_TARGET_RELATIVE_PATH_INVALID")
    parent = path.parent
    if str(parent) in {"", "."}:
        return path.as_posix()
    return parent.as_posix()


def _normalize_expected_mypy_exit(
    execution: ProcessExecutionEvidence,
) -> ProcessExecutionEvidence:
    """Treat mypy exit code 1 as completed analysis with reported type findings."""
    if execution.exit_code == 1 and execution.status is AnalysisExecutionStatus.FAILED:
        return replace(execution, status=AnalysisExecutionStatus.SUCCEEDED)
    return execution


def _parse_mypy_findings(
    execution: ProcessExecutionEvidence,
    *,
    root: Path,
    raw_path: str,
    engine_version: str,
    diagnostics: list[str],
) -> tuple:
    """Parse current JSON-lines output while also accepting list/object wrappers."""
    if execution.status is not AnalysisExecutionStatus.SUCCEEDED:
        diagnostics.append(execution.engine_id + ":PROCESS_STATUS=" + execution.status.value)
        return ()
    try:
        items = _json_items(execution.stdout_text)
    except ValueError as error:
        diagnostics.append(execution.engine_id + ":MALFORMED_JSON:" + str(error))
        return ()
    raw_bytes = execution.stdout_text.encode("utf-8")
    reference = RawEvidenceReference(
        engine_id="mypy",
        relative_path=raw_path,
        sha256=hashlib.sha256(raw_bytes).hexdigest(),
        byte_size=len(raw_bytes),
    )
    findings = []
    for index, item in enumerate(items):
        try:
            path = _relative_path(root, str(item["file"]))
            message = str(item["message"]).strip()
            code = str(item.get("code") or "MYPY_UNCODED").strip()
            severity_text = str(item.get("severity") or "error").strip().lower()
            hint = str(item.get("hint") or "").strip()
            findings.append(
                build_normalized_finding(
                    engine_id="mypy",
                    engine_version=engine_version,
                    rule_id=code,
                    normalized_relative_path=path,
                    symbol_identity="",
                    normalized_message_signature=_message_signature(message),
                    severity=_severity(severity_text),
                    location=FindingLocation(
                        line=int(item.get("line") or 0),
                        column=int(item.get("column") or 0),
                        end_line=int(item.get("end_line") or 0),
                        end_column=int(item.get("end_column") or 0),
                    ),
                    raw_evidence_reference=reference,
                    metadata=(
                        ("message", message),
                        ("hint", hint),
                        ("reported_severity", severity_text),
                    ),
                )
            )
        except (KeyError, TypeError, ValueError) as error:
            diagnostics.append(execution.engine_id + f":ITEM_{index}_INVALID:{error}")
    return tuple(sorted(findings, key=lambda item: item.semantic_key))


def _json_items(text: str) -> tuple[dict[str, object], ...]:
    """Extract mypy JSON items from JSON lines, list, or messages wrapper."""
    stripped = str(text or "").strip()
    if not stripped:
        return ()
    try:
        payload = json.loads(stripped)
    except json.JSONDecodeError:
        items = []
        for line_number, line in enumerate(stripped.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"JSON_LINE_{line_number}_INVALID:{error}") from error
            if not isinstance(item, dict):
                raise ValueError(f"JSON_LINE_{line_number}_NOT_OBJECT")
            items.append(item)
        return tuple(items)
    if isinstance(payload, list):
        if not all(isinstance(item, dict) for item in payload):
            raise ValueError("JSON_LIST_CONTAINS_NON_OBJECT")
        return tuple(payload)
    if isinstance(payload, dict) and isinstance(payload.get("messages"), list):
        messages = payload["messages"]
        if not all(isinstance(item, dict) for item in messages):
            raise ValueError("JSON_MESSAGES_CONTAINS_NON_OBJECT")
        return tuple(messages)
    if isinstance(payload, dict):
        return (payload,)
    raise ValueError("JSON_ROOT_UNSUPPORTED")


def _relative_path(root: Path, filename: str) -> str:
    """Normalize mypy file path against the analyzed sealed tree."""
    candidate = Path(filename)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve(strict=False)
    try:
        return resolved.relative_to(root.resolve(strict=False)).as_posix()
    except ValueError as error:
        raise ValueError("MYPY_FINDING_PATH_OUTSIDE_ANALYSIS_ROOT") from error


def _message_signature(message: str) -> str:
    """Normalize volatile numeric fragments while preserving diagnostic meaning."""
    normalized = " ".join(str(message or "").split())
    return re.sub(r"\b\d+\b", "<n>", normalized)


def _severity(value: str) -> FindingSeverity:
    """Map mypy severity labels without deciding overall authorization."""
    if value == "note":
        return FindingSeverity.INFO
    if value == "warning":
        return FindingSeverity.WARNING
    return FindingSeverity.ERROR


def _combined_status(
    baseline: ProcessExecutionEvidence,
    preview: ProcessExecutionEvidence,
    diagnostics: list[str],
) -> AnalysisExecutionStatus:
    """Combine process and parser states without treating missing evidence as PASS."""
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
