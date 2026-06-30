
"""Offline Adviser run-registry record builder and validator.

M6 builds deterministic records from supplied harness summaries, supplied gold
manifest metadata, and supplied candidate metadata. It does not execute
candidates, write registry files, scan source trees, or change runtime routing.
"""

from __future__ import annotations


__all__ = [
    'assert_run_registry_record_review_eligible',
    'assert_run_registry_record_valid',
    'build_run_registry_record',
    'RunRegistryValidationResult',
    'validate_run_registry_record',
]
from dataclasses import dataclass
from typing import Any, Mapping

from .gold_manifest import validate_gold_manifest_record
from .hash_utils import hash_record_without_field

FEATURE_ID = "routing_signal_scorer_v3_adviser_gold_manifest_run_registry_v1"
SCHEMA_VERSION = "3.45-adviser-gold-manifest-run-registry"
AUTHORITY_STATEMENT = "advisory_only"
PROMOTION_BLOCKING_STATUSES = frozenset({"blocked", "critical_failure", "unsafe"})


@dataclass(frozen=True)
class RunRegistryValidationResult:
    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    record_hash: str | None
    promotion_blocked: bool
    authority_statement: str = AUTHORITY_STATEMENT
    feature_id: str = FEATURE_ID
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "record_hash": self.record_hash,
            "promotion_blocked": self.promotion_blocked,
            "authority_statement": self.authority_statement,
            "feature_id": self.feature_id,
            "schema_version": self.schema_version,
        }


def build_run_registry_record(
    *,
    run_summary: Mapping[str, Any],
    gold_manifest: Mapping[str, Any],
    candidate_metadata: Mapping[str, Any],
    registry_record_id: str,
    recorded_by: str,
) -> dict[str, object]:
    """Build a deterministic run registry record from supplied objects only."""

    if not isinstance(run_summary, Mapping):
        raise TypeError("run_summary must be a mapping")
    if not isinstance(candidate_metadata, Mapping):
        raise TypeError("candidate_metadata must be a mapping")
    manifest_result = validate_gold_manifest_record(gold_manifest)
    if not manifest_result.get("ok"):
        raise ValueError("gold_manifest is invalid for run registry record")
    if not registry_record_id or not str(registry_record_id).strip():
        raise ValueError("registry_record_id is required")

    critical_failures = int(run_summary.get("critical_failures", 0))
    promotion_blockers = int(run_summary.get("promotion_blockers", 0))
    run_status = str(run_summary.get("status", "unknown"))
    promotion_blocked = bool(critical_failures or promotion_blockers or run_status in PROMOTION_BLOCKING_STATUSES)
    record = {
        "schema_version": SCHEMA_VERSION,
        "registry_record_id": str(registry_record_id),
        "run_id": str(run_summary.get("run_id", "")),
        "candidate_id": str(candidate_metadata.get("candidate_id") or run_summary.get("candidate_id", "")),
        "candidate_version": str(candidate_metadata.get("candidate_version") or run_summary.get("candidate_version", "")),
        "candidate_code_hash": str(candidate_metadata.get("candidate_code_hash") or run_summary.get("candidate_code_hash", "")),
        "gold_set_version": str(gold_manifest.get("gold_set_version", "")),
        "gold_manifest_hash": str(gold_manifest.get("manifest_hash", "")),
        "cases_run": int(run_summary.get("cases_run", 0)),
        "critical_failures": critical_failures,
        "promotion_blockers": promotion_blockers,
        "aggregate_severity": str(run_summary.get("aggregate_severity", "unknown")),
        "run_status": run_status,
        "promotion_blocked": promotion_blocked,
        "registry_status": "blocked" if promotion_blocked else "eligible_for_human_review",
        "recorded_by": str(recorded_by),
        "authority_statement": AUTHORITY_STATEMENT,
        "feature_id": FEATURE_ID,
    }
    record["record_hash"] = hash_record_without_field(record, "record_hash")
    return record


def validate_run_registry_record(record: Mapping[str, Any]) -> dict[str, object]:
    """Validate a supplied run registry record without side effects."""

    errors: list[str] = []
    warnings: list[str] = []
    record_hash = None
    if not isinstance(record, Mapping):
        return RunRegistryValidationResult(False, ("record must be a mapping",), (), None, True).to_dict()
    if record.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if record.get("authority_statement") != AUTHORITY_STATEMENT:
        errors.append("authority_statement must be advisory_only")
    for field in ("registry_record_id", "run_id", "candidate_id", "candidate_version", "candidate_code_hash", "gold_set_version", "gold_manifest_hash"):
        if not str(record.get(field, "")).strip():
            errors.append(f"missing required field: {field}")
    for field in ("cases_run", "critical_failures", "promotion_blockers"):
        try:
            if int(record.get(field, -1)) < 0:
                errors.append(f"{field} must be non-negative")
        except Exception:
            errors.append(f"{field} must be an integer")
    promotion_blocked = bool(record.get("promotion_blocked"))
    if int(record.get("critical_failures", 0)) > 0 and not promotion_blocked:
        errors.append("critical failures must mark promotion_blocked")
    if int(record.get("promotion_blockers", 0)) > 0 and not promotion_blocked:
        errors.append("promotion blockers must mark promotion_blocked")
    expected_status = "blocked" if promotion_blocked else "eligible_for_human_review"
    if record.get("registry_status") != expected_status:
        errors.append("registry_status inconsistent with promotion_blocked")
    supplied_hash = str(record.get("record_hash", ""))
    if not _looks_like_sha256(supplied_hash):
        errors.append("record_hash must be sha256")
    else:
        record_hash = supplied_hash
        expected_hash = hash_record_without_field(record, "record_hash")
        if supplied_hash != expected_hash:
            errors.append("record_hash mismatch")
    if int(record.get("cases_run", 0)) < 30:
        warnings.append("run record covers a small case count; promotion needs larger reviewed evaluations")
    return RunRegistryValidationResult(
        ok=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        record_hash=record_hash,
        promotion_blocked=promotion_blocked,
    ).to_dict()


def assert_run_registry_record_valid(record: Mapping[str, Any]) -> Mapping[str, Any]:
    """Raise if supplied run registry record is invalid."""

    result = validate_run_registry_record(record)
    if not result.get("ok"):
        raise ValueError("invalid Adviser run registry record: " + "; ".join(result.get("errors", [])))
    return record


def assert_run_registry_record_review_eligible(record: Mapping[str, Any]) -> Mapping[str, Any]:
    """Raise if supplied run registry record contains promotion blockers."""

    assert_run_registry_record_valid(record)
    if bool(record.get("promotion_blocked")):
        raise ValueError("Adviser run registry record is promotion-blocked")
    return record


def _looks_like_sha256(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value.lower())
