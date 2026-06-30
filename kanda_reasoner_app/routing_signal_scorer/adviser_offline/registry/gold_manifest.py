
"""Offline Adviser gold-manifest record builder and validator.

M6 defines manifest metadata mechanics only. It does not create a gold set, load
case files, write manifest files, or treat teacher answers as ground truth.
Gold case records must be supplied by the caller and must already be human
reviewed.
"""

from __future__ import annotations


__all__ = [
    'assert_gold_manifest_valid',
    'build_case_manifest_entry',
    'build_gold_manifest_record',
    'GoldManifestValidationResult',
    'validate_gold_manifest_record',
]
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .hash_utils import hash_mapping, hash_record_without_field

FEATURE_ID = "routing_signal_scorer_v3_adviser_gold_manifest_run_registry_v1"
SCHEMA_VERSION = "3.45-adviser-gold-manifest-run-registry"
AUTHORITY_STATEMENT = "advisory_only"
APPROVED_REVIEW_STATUSES = frozenset({"human_reviewed", "approved_as_gold"})


@dataclass(frozen=True)
class GoldManifestValidationResult:
    ok: bool
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    manifest_hash: str | None
    case_count: int
    authority_statement: str = AUTHORITY_STATEMENT
    feature_id: str = FEATURE_ID
    schema_version: str = SCHEMA_VERSION

    def to_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
            "manifest_hash": self.manifest_hash,
            "case_count": self.case_count,
            "authority_statement": self.authority_statement,
            "feature_id": self.feature_id,
            "schema_version": self.schema_version,
        }


def build_case_manifest_entry(case: Mapping[str, Any]) -> dict[str, object]:
    """Build a manifest entry from one supplied, reviewed case record."""

    if not isinstance(case, Mapping):
        raise TypeError("case must be a mapping")
    case_id = str(case.get("case_id", "")).strip()
    if not case_id:
        raise ValueError("case_id is required")
    review_status = str(case.get("human_review_status") or case.get("review_status") or "").strip()
    if review_status not in APPROVED_REVIEW_STATUSES:
        raise ValueError("case must be human reviewed before it can enter a gold manifest")
    entry = {
        "case_id": case_id,
        "case_hash": hash_mapping(case),
        "human_review_status": review_status,
        "expected_severity_if_missed": str(case.get("expected_severity_if_missed", "unknown")),
        "supersedes": case.get("supersedes"),
    }
    return entry


def build_gold_manifest_record(
    *,
    manifest_id: str,
    gold_set_version: str,
    case_entries: Sequence[Mapping[str, Any]],
    created_by: str,
    review_status_summary: str = "all_cases_human_reviewed",
    supersedes_manifest_id: str | None = None,
) -> dict[str, object]:
    """Build a deterministic manifest record from supplied case entries."""

    if not manifest_id or not str(manifest_id).strip():
        raise ValueError("manifest_id is required")
    if not gold_set_version or not str(gold_set_version).strip():
        raise ValueError("gold_set_version is required")
    if isinstance(case_entries, (str, bytes, bytearray)) or not isinstance(case_entries, Sequence):
        raise TypeError("case_entries must be a sequence")
    entries = [dict(entry) for entry in case_entries]
    if not entries:
        raise ValueError("at least one reviewed case entry is required")
    case_ids = []
    case_hashes = []
    for entry in entries:
        case_id = str(entry.get("case_id", "")).strip()
        case_hash = str(entry.get("case_hash", "")).strip()
        status = str(entry.get("human_review_status", "")).strip()
        if not case_id:
            raise ValueError("each manifest entry requires case_id")
        if not _looks_like_sha256(case_hash):
            raise ValueError(f"case entry {case_id} requires sha256 case_hash")
        if status not in APPROVED_REVIEW_STATUSES:
            raise ValueError(f"case entry {case_id} is not approved for gold manifest")
        case_ids.append(case_id)
        case_hashes.append(case_hash)
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("case_ids must be unique inside a gold manifest")

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "manifest_id": str(manifest_id),
        "gold_set_version": str(gold_set_version),
        "case_count": len(entries),
        "case_entries": entries,
        "case_hashes": case_hashes,
        "review_status_summary": str(review_status_summary),
        "created_by": str(created_by),
        "supersedes_manifest_id": supersedes_manifest_id,
        "authority_statement": AUTHORITY_STATEMENT,
        "feature_id": FEATURE_ID,
    }
    manifest["manifest_hash"] = hash_record_without_field(manifest, "manifest_hash")
    return manifest


def validate_gold_manifest_record(manifest: Mapping[str, Any]) -> dict[str, object]:
    """Validate a supplied gold manifest record without reading or writing files."""

    errors: list[str] = []
    warnings: list[str] = []
    manifest_hash = None
    case_count = 0

    if not isinstance(manifest, Mapping):
        return GoldManifestValidationResult(False, ("manifest must be a mapping",), (), None, 0).to_dict()

    if manifest.get("schema_version") != SCHEMA_VERSION:
        errors.append("schema_version mismatch")
    if manifest.get("authority_statement") != AUTHORITY_STATEMENT:
        errors.append("authority_statement must be advisory_only")
    entries = manifest.get("case_entries")
    if isinstance(entries, Sequence) and not isinstance(entries, (str, bytes, bytearray)):
        case_count = len(entries)
    else:
        errors.append("case_entries must be a sequence")
        entries = []
    if not entries:
        errors.append("case_entries must not be empty")
    if int(manifest.get("case_count", -1)) != case_count:
        errors.append("case_count mismatch")
    seen: set[str] = set()
    hashes: list[str] = []
    for entry in entries:
        if not isinstance(entry, Mapping):
            errors.append("case entry must be a mapping")
            continue
        case_id = str(entry.get("case_id", "")).strip()
        case_hash = str(entry.get("case_hash", "")).strip()
        status = str(entry.get("human_review_status", "")).strip()
        if not case_id:
            errors.append("case entry missing case_id")
        elif case_id in seen:
            errors.append(f"duplicate case_id: {case_id}")
        else:
            seen.add(case_id)
        if not _looks_like_sha256(case_hash):
            errors.append(f"case entry {case_id or '<missing>'} missing sha256 case_hash")
        else:
            hashes.append(case_hash)
        if status not in APPROVED_REVIEW_STATUSES:
            errors.append(f"case entry {case_id or '<missing>'} is not human reviewed")
    if list(manifest.get("case_hashes", [])) != hashes:
        errors.append("case_hashes do not match case_entries")
    supplied_hash = manifest.get("manifest_hash")
    if not _looks_like_sha256(str(supplied_hash or "")):
        errors.append("manifest_hash must be sha256")
    else:
        manifest_hash = str(supplied_hash)
        expected = hash_record_without_field(manifest, "manifest_hash")
        if supplied_hash != expected:
            errors.append("manifest_hash mismatch")
    if case_count < 30:
        warnings.append("gold manifest is small; M6 allows infrastructure tests but promotion needs larger reviewed sets")

    return GoldManifestValidationResult(
        ok=not errors,
        errors=tuple(errors),
        warnings=tuple(warnings),
        manifest_hash=manifest_hash,
        case_count=case_count,
    ).to_dict()


def assert_gold_manifest_valid(manifest: Mapping[str, Any]) -> Mapping[str, Any]:
    """Raise if supplied manifest is not valid."""

    result = validate_gold_manifest_record(manifest)
    if not result.get("ok"):
        raise ValueError("invalid Adviser gold manifest: " + "; ".join(result.get("errors", [])))
    return manifest


def _looks_like_sha256(value: str) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(ch in "0123456789abcdef" for ch in value.lower())
