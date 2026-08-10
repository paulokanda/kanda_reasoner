# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_capability_preflight.py
"""Capability preflight for externally installed analyzer executables."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import shutil

from .advanced_quality_review_contract import (
    AnalysisExecutionStatus,
    AnalyzerAuthorityRole,
)
from .analyzer_environment_contract import (
    AnalyzerCapabilityMode,
    AnalyzerEnvironmentLock,
    AnalyzerLockEntry,
    validate_analyzer_environment_lock,
)
from .analyzer_process_runtime import BoundedProcessRequest, run_bounded_process

__all__ = [
    "AnalyzerCapabilityEvidence",
    "preflight_analyzer_capabilities",
    "preflight_analyzer_capability",
]


@dataclass(frozen=True)
class AnalyzerCapabilityEvidence:
    """Structured capability evidence for one analyzer before review execution."""

    engine_id: str
    available: bool
    observed_version: str
    expected_version: str
    compatible: bool
    execution_path: str
    capability_mode: AnalyzerCapabilityMode
    configuration_source: str
    cache_routing_supported: bool
    authority_role: AnalyzerAuthorityRole
    execution_status: AnalysisExecutionStatus
    diagnostic: str

    def to_dict(self) -> dict[str, object]:
        """Return JSON-ready capability evidence."""
        payload = asdict(self)
        payload["capability_mode"] = self.capability_mode.value
        payload["authority_role"] = self.authority_role.value
        payload["execution_status"] = self.execution_status.value
        return payload


def preflight_analyzer_capabilities(
    environment_lock: AnalyzerEnvironmentLock,
    *,
    cwd: str | Path,
) -> tuple[AnalyzerCapabilityEvidence, ...]:
    """Probe every locked analyzer without installing or modifying any package."""
    blockers = validate_analyzer_environment_lock(environment_lock)
    if blockers:
        raise ValueError("ANALYZER_ENVIRONMENT_LOCK_INVALID:" + "|".join(blockers))
    return tuple(
        preflight_analyzer_capability(entry, cwd=cwd)
        for entry in environment_lock.entries
    )


def preflight_analyzer_capability(
    entry: AnalyzerLockEntry,
    *,
    cwd: str | Path,
) -> AnalyzerCapabilityEvidence:
    """Probe one executable and compare observed version to the lock contract."""
    execution_path = _resolve_executable(entry.executable)
    if not execution_path:
        return _unavailable_evidence(entry)
    request = BoundedProcessRequest(
        engine_id=entry.engine_id + "_version_probe",
        argv=(execution_path, *entry.version_args),
        cwd=str(Path(cwd).resolve(strict=False)),
        timeout_seconds=10.0,
        max_stdout_bytes=16_384,
        max_stderr_bytes=16_384,
    )
    result = run_bounded_process(request)
    observed = _version_text(result.stdout_text, result.stderr_text)
    compatible = bool(
        result.status is AnalysisExecutionStatus.SUCCEEDED
        and entry.expected_version.lower() in observed.lower()
    )
    diagnostic_parts: list[str] = []
    if result.status is not AnalysisExecutionStatus.SUCCEEDED:
        diagnostic_parts.append("version_probe_status=" + result.status.value)
    if not observed:
        diagnostic_parts.append("version_output_empty")
    if observed and not compatible:
        diagnostic_parts.append("version_mismatch")
    capability_mode = entry.capability_mode
    if result.status is not AnalysisExecutionStatus.SUCCEEDED or not compatible:
        capability_mode = AnalyzerCapabilityMode.UNAVAILABLE
    return AnalyzerCapabilityEvidence(
        engine_id=entry.engine_id,
        available=result.status is AnalysisExecutionStatus.SUCCEEDED,
        observed_version=observed,
        expected_version=entry.expected_version,
        compatible=compatible,
        execution_path=execution_path,
        capability_mode=capability_mode,
        configuration_source=entry.configuration_source,
        cache_routing_supported=entry.cache_routing_supported,
        authority_role=entry.authority_role,
        execution_status=result.status,
        diagnostic="; ".join(diagnostic_parts),
    )


def _resolve_executable(executable: str) -> str:
    """Resolve explicit or PATH-based executable without provisioning software."""
    text = str(executable or "").strip()
    if not text:
        return ""
    candidate = Path(text).expanduser()
    if candidate.is_absolute():
        return str(candidate.resolve(strict=False)) if candidate.is_file() else ""
    found = shutil.which(text)
    return str(Path(found).resolve(strict=False)) if found else ""


def _version_text(stdout_text: str, stderr_text: str) -> str:
    """Return one normalized bounded version evidence string."""
    combined = "\n".join(
        part.strip() for part in (stdout_text, stderr_text) if part.strip()
    )
    return " ".join(combined.split())[:1000]


def _unavailable_evidence(entry: AnalyzerLockEntry) -> AnalyzerCapabilityEvidence:
    """Return explicit unavailable evidence without synthetic success."""
    return AnalyzerCapabilityEvidence(
        engine_id=entry.engine_id,
        available=False,
        observed_version="",
        expected_version=entry.expected_version,
        compatible=False,
        execution_path="",
        capability_mode=AnalyzerCapabilityMode.UNAVAILABLE,
        configuration_source=entry.configuration_source,
        cache_routing_supported=entry.cache_routing_supported,
        authority_role=entry.authority_role,
        execution_status=AnalysisExecutionStatus.UNAVAILABLE,
        diagnostic="ANALYZER_EXECUTABLE_UNAVAILABLE",
    )
