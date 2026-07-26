# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_evidence_models.py
"""Immutable evidence models for Advanced Quality Review runs."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from pathlib import PurePosixPath
from typing import Iterable

from .advanced_quality_review_contract import (
    AnalysisExecutionStatus,
    AnalysisIdentity,
    QualityDecision,
    analysis_identity_matches,
)
from .analyzer_capability_preflight import AnalyzerCapabilityEvidence
from .analyzer_process_runtime import ProcessExecutionEvidence

__all__ = [
    "ADVANCED_QUALITY_EVIDENCE_CORE_FEATURE_ID",
    "EvidenceAuthorizationState",
    "EvidenceAuthorizationEvent",
    "FindingLocation",
    "FindingSeverity",
    "NormalizedFinding",
    "QualityReviewRunRecord",
    "RawEvidenceReference",
    "build_normalized_finding",
    "build_quality_review_run_record",
    "evaluate_authorization_state",
    "validate_quality_review_run_record",
]

ADVANCED_QUALITY_EVIDENCE_CORE_FEATURE_ID = (
    "advanced-quality-review-evidence-core-persistence-v1"
)


class FindingSeverity(str, Enum):
    """Describe one normalized finding without deciding overall authorization."""

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    BLOCKER = "BLOCKER"
    ADVISORY = "ADVISORY"


class EvidenceAuthorizationState(str, Enum):
    """Describe whether historical evidence may authorize the active identity."""

    CURRENT = "CURRENT"
    STALE = "STALE"
    INVALIDATED = "INVALIDATED"


@dataclass(frozen=True)
class FindingLocation:
    """Store source location as metadata, not semantic finding identity."""

    line: int = 0
    column: int = 0
    end_line: int = 0
    end_column: int = 0

    def to_dict(self) -> dict[str, int]:
        """Return stable JSON-ready location metadata."""
        return asdict(self)


@dataclass(frozen=True)
class RawEvidenceReference:
    """Bind one finding to exact bounded raw analyzer evidence bytes."""

    engine_id: str
    relative_path: str
    sha256: str
    byte_size: int

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready raw-evidence reference."""
        return asdict(self)


@dataclass(frozen=True)
class NormalizedFinding:
    """Represent one analyzer finding through a stable cross-run contract."""

    engine_id: str
    engine_version: str
    rule_id: str
    normalized_relative_path: str
    symbol_identity: str
    normalized_message_signature: str
    severity: FindingSeverity
    location: FindingLocation
    raw_evidence_reference: RawEvidenceReference
    metadata: tuple[tuple[str, str], ...] = ()

    def to_dict(self) -> dict[str, object]:
        """Return stable JSON-ready normalized finding evidence."""
        return {
            "engine_id": self.engine_id,
            "engine_version": self.engine_version,
            "rule_id": self.rule_id,
            "normalized_relative_path": self.normalized_relative_path,
            "symbol_identity": self.symbol_identity,
            "normalized_message_signature": self.normalized_message_signature,
            "severity": self.severity.value,
            "location": self.location.to_dict(),
            "raw_evidence_reference": self.raw_evidence_reference.to_dict(),
            "metadata": [list(item) for item in self.metadata],
        }

    @property
    def semantic_key(self) -> str:
        """Return finding identity excluding line and column relocation metadata."""
        payload = {
            "engine_id": self.engine_id,
            "rule_id": self.rule_id,
            "normalized_relative_path": self.normalized_relative_path,
            "symbol_identity": self.symbol_identity,
            "normalized_message_signature": self.normalized_message_signature,
        }
        return _canonical_hash(payload)


@dataclass(frozen=True)
class QualityReviewRunRecord:
    """Store one immutable review run bound to exact analysis identity."""

    schema_version: str
    feature_id: str
    run_id: str
    created_at_utc: str
    analysis_identity: AnalysisIdentity
    analyzer_environment_identity_hash: str
    capabilities: tuple[AnalyzerCapabilityEvidence, ...]
    executions: tuple[ProcessExecutionEvidence, ...]
    findings: tuple[NormalizedFinding, ...]
    execution_status: AnalysisExecutionStatus
    quality_decision: QualityDecision
    initial_authorization_state: EvidenceAuthorizationState

    def to_dict(self) -> dict[str, object]:
        """Return deterministic JSON-ready run evidence."""
        return {
            "schema_version": self.schema_version,
            "feature_id": self.feature_id,
            "run_id": self.run_id,
            "created_at_utc": self.created_at_utc,
            "analysis_identity": self.analysis_identity.to_dict(),
            "analysis_identity_hash": self.analysis_identity.identity_hash,
            "analyzer_environment_identity_hash": (
                self.analyzer_environment_identity_hash
            ),
            "capabilities": [item.to_dict() for item in self.capabilities],
            "executions": [item.to_dict() for item in self.executions],
            "findings": [item.to_dict() for item in self.findings],
            "execution_status": self.execution_status.value,
            "quality_decision": self.quality_decision.value,
            "initial_authorization_state": self.initial_authorization_state.value,
        }

    @property
    def record_hash(self) -> str:
        """Return SHA-256 over the canonical run record payload."""
        return _canonical_hash(self.to_dict())


@dataclass(frozen=True)
class EvidenceAuthorizationEvent:
    """Append one immutable authorization-state transition for a stored run."""

    schema_version: str
    event_id: str
    created_at_utc: str
    run_id: str
    evidence_identity_hash: str
    current_identity_hash: str
    prior_state: EvidenceAuthorizationState
    new_state: EvidenceAuthorizationState
    reason: str
    superseding_preview_hash: str = ""

    def to_dict(self) -> dict[str, str]:
        """Return stable JSON-ready state transition evidence."""
        payload = asdict(self)
        payload["prior_state"] = self.prior_state.value
        payload["new_state"] = self.new_state.value
        return payload



def build_normalized_finding(
    *,
    engine_id: str,
    engine_version: str,
    rule_id: str,
    normalized_relative_path: str,
    symbol_identity: str,
    normalized_message_signature: str,
    severity: FindingSeverity,
    location: FindingLocation,
    raw_evidence_reference: RawEvidenceReference,
    metadata: Iterable[tuple[str, str]] = (),
) -> NormalizedFinding:
    """Validate and build one deterministic normalized finding."""
    path = _normalize_relative_path(normalized_relative_path)
    finding = NormalizedFinding(
        engine_id=_required(engine_id, "FINDING_ENGINE_ID_EMPTY"),
        engine_version=_required(engine_version, "FINDING_ENGINE_VERSION_EMPTY"),
        rule_id=_required(rule_id, "FINDING_RULE_ID_EMPTY"),
        normalized_relative_path=path,
        symbol_identity=str(symbol_identity or "").strip(),
        normalized_message_signature=_required(
            normalized_message_signature,
            "FINDING_MESSAGE_SIGNATURE_EMPTY",
        ),
        severity=severity,
        location=location,
        raw_evidence_reference=_validate_raw_reference(raw_evidence_reference),
        metadata=tuple(
            sorted(
                (
                    _required(key, "FINDING_METADATA_KEY_EMPTY"),
                    str(value),
                )
                for key, value in metadata
            )
        ),
    )
    return finding



def build_quality_review_run_record(
    *,
    run_id: str,
    created_at_utc: str,
    analysis_identity: AnalysisIdentity,
    analyzer_environment_identity_hash: str,
    capabilities: Iterable[AnalyzerCapabilityEvidence],
    executions: Iterable[ProcessExecutionEvidence],
    findings: Iterable[NormalizedFinding],
    execution_status: AnalysisExecutionStatus,
    quality_decision: QualityDecision,
    schema_version: str = "1.0",
) -> QualityReviewRunRecord:
    """Build one deterministic immutable review run record."""
    record = QualityReviewRunRecord(
        schema_version=_required(schema_version, "RUN_SCHEMA_VERSION_EMPTY"),
        feature_id=ADVANCED_QUALITY_EVIDENCE_CORE_FEATURE_ID,
        run_id=_safe_id(run_id, "RUN_ID"),
        created_at_utc=_required(created_at_utc, "RUN_CREATED_AT_EMPTY"),
        analysis_identity=analysis_identity,
        analyzer_environment_identity_hash=_hash_text(
            analyzer_environment_identity_hash,
            "ANALYZER_ENVIRONMENT_IDENTITY_HASH_INVALID",
        ),
        capabilities=tuple(sorted(capabilities, key=lambda item: item.engine_id)),
        executions=tuple(sorted(executions, key=lambda item: item.engine_id)),
        findings=tuple(sorted(findings, key=lambda item: item.semantic_key)),
        execution_status=execution_status,
        quality_decision=quality_decision,
        initial_authorization_state=EvidenceAuthorizationState.CURRENT,
    )
    blockers = validate_quality_review_run_record(record)
    if blockers:
        raise ValueError("QUALITY_REVIEW_RUN_INVALID:" + "|".join(blockers))
    return record



def validate_quality_review_run_record(
    record: QualityReviewRunRecord,
) -> tuple[str, ...]:
    """Return deterministic blockers for incomplete or contradictory evidence."""
    blockers: list[str] = []
    if record.feature_id != ADVANCED_QUALITY_EVIDENCE_CORE_FEATURE_ID:
        blockers.append("RUN_FEATURE_ID_MISMATCH")
    if record.initial_authorization_state != EvidenceAuthorizationState.CURRENT:
        blockers.append("RUN_INITIAL_AUTHORIZATION_NOT_CURRENT")
    capability_ids = [item.engine_id for item in record.capabilities]
    execution_ids = [item.engine_id for item in record.executions]
    if len(capability_ids) != len(set(capability_ids)):
        blockers.append("RUN_CAPABILITY_ENGINE_DUPLICATE")
    if len(execution_ids) != len(set(execution_ids)):
        blockers.append("RUN_EXECUTION_ENGINE_DUPLICATE")
    for finding in record.findings:
        if finding.engine_id not in set(capability_ids):
            blockers.append("FINDING_ENGINE_WITHOUT_CAPABILITY:" + finding.engine_id)
    if record.execution_status == AnalysisExecutionStatus.SUCCEEDED:
        failed = {
            AnalysisExecutionStatus.FAILED,
            AnalysisExecutionStatus.TIMED_OUT,
            AnalysisExecutionStatus.CANCELLED,
            AnalysisExecutionStatus.STALE,
        }
        if any(item.status in failed for item in record.executions):
            blockers.append("RUN_SUCCEEDED_WITH_FAILED_ENGINE_EXECUTION")
    return tuple(sorted(set(blockers)))



def evaluate_authorization_state(
    evidence_identity: AnalysisIdentity,
    current_identity: AnalysisIdentity,
) -> EvidenceAuthorizationState:
    """Return CURRENT only when the complete frozen analysis identity matches."""
    if analysis_identity_matches(evidence_identity, current_identity):
        return EvidenceAuthorizationState.CURRENT
    return EvidenceAuthorizationState.STALE



def _validate_raw_reference(reference: RawEvidenceReference) -> RawEvidenceReference:
    """Validate one raw evidence reference without touching the filesystem."""
    engine_id = _required(reference.engine_id, "RAW_REFERENCE_ENGINE_ID_EMPTY")
    relative_path = _normalize_relative_path(reference.relative_path)
    digest = _hash_text(reference.sha256, "RAW_REFERENCE_HASH_INVALID")
    if int(reference.byte_size) < 0:
        raise ValueError("RAW_REFERENCE_BYTE_SIZE_NEGATIVE")
    return RawEvidenceReference(
        engine_id=engine_id,
        relative_path=relative_path,
        sha256=digest,
        byte_size=int(reference.byte_size),
    )



def _normalize_relative_path(value: str) -> str:
    """Return normalized POSIX relative path and reject traversal or absolutes."""
    text = str(value or "").replace("\\", "/").strip()
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise ValueError("EVIDENCE_RELATIVE_PATH_INVALID:" + text)
    normalized = path.as_posix().lstrip("./")
    if not normalized or normalized.startswith("../"):
        raise ValueError("EVIDENCE_RELATIVE_PATH_INVALID:" + text)
    return normalized



def _required(value: str, error: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(error)
    return text



def _safe_id(value: str, label: str) -> str:
    text = _required(value, label + "_EMPTY")
    cleaned = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in text
    ).strip("_.-")
    if not cleaned:
        raise ValueError(label + "_INVALID")
    return cleaned[:96]



def _hash_text(value: str, error: str) -> str:
    text = str(value or "").strip().lower()
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise ValueError(error)
    return text



def _canonical_hash(payload: dict[str, object]) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
