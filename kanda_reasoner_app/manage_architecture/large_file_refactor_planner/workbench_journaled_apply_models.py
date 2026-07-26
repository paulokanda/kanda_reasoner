# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_journaled_apply_models.py
"""Immutable authorization and result contracts for journaled Workbench apply."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
import json
from typing import Any

from .models import SCHEMA_VERSION

__all__ = [
    "JOURNALED_APPLY_EXECUTOR_FEATURE_ID",
    "JournaledApplyAuthorization",
    "JournaledApplyResult",
    "build_journaled_apply_authorization",
]

JOURNALED_APPLY_EXECUTOR_FEATURE_ID = (
    "architecture-review-large-file-refactor-workbench-patch5-journaled-apply-executor-v1"
)


@dataclass(frozen=True)
class JournaledApplyAuthorization:
    """Hash-checked authorization built from immutable review evidence."""

    transaction_id: str
    contract_hash: str
    payload_hash: str
    semantic_reviewed: bool
    warnings_acknowledged: bool
    transaction_summary_confirmed: bool
    executor_proof_available: bool
    authorization_hash: str

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready authorization evidence."""
        return asdict(self)

    def integrity_valid(self) -> bool:
        """Return whether immutable authorization fields match their digest."""
        return self.authorization_hash == _authorization_hash(self)

    @property
    def authorized(self) -> bool:
        """Return whether every independent authorization dimension passed."""
        return bool(
            self.integrity_valid()
            and self.semantic_reviewed
            and self.warnings_acknowledged
            and self.transaction_summary_confirmed
            and self.executor_proof_available
        )


@dataclass(frozen=True)
class JournaledApplyResult:
    """Compatibility-rich result for journaled multi-file source application."""

    schema_version: str
    feature_id: str
    status: str
    transaction_id: str
    target_file: str
    source_content_hash_before: str
    source_content_hash_after: str
    preview_root: str
    rollback_manifest_path: str
    execution_manifest_path: str
    source_mutation_enabled: bool
    import_rewrite_enabled: bool
    lane_state: str
    transaction_state: str
    written_files: list[str] = field(default_factory=list)
    generated_files: list[str] = field(default_factory=list)
    operations_verified: int = 0
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checked_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return JSON-ready execution evidence."""
        return asdict(self)


def build_journaled_apply_authorization(
    *,
    transaction_id: str,
    contract_hash: str,
    payload_hash: str,
    semantic_reviewed: bool,
    warnings_acknowledged: bool,
    transaction_summary_confirmed: bool,
    executor_proof_available: bool,
) -> JournaledApplyAuthorization:
    """Build deterministic authorization evidence without GUI-state ownership."""
    provisional = JournaledApplyAuthorization(
        transaction_id=transaction_id,
        contract_hash=contract_hash,
        payload_hash=payload_hash,
        semantic_reviewed=semantic_reviewed,
        warnings_acknowledged=warnings_acknowledged,
        transaction_summary_confirmed=transaction_summary_confirmed,
        executor_proof_available=executor_proof_available,
        authorization_hash="",
    )
    return JournaledApplyAuthorization(
        **{**provisional.__dict__, "authorization_hash": _authorization_hash(provisional)}
    )


def build_blocked_apply_result(
    *,
    transaction_id: str,
    target_file: str,
    source_hash_before: str,
    preview_root: str,
    transaction_root: str,
    lane_state: str,
    transaction_state: str,
    blockers: list[str],
    checked_rules: list[str],
) -> JournaledApplyResult:
    """Build a zero-write blocked execution result."""
    root = str(transaction_root)
    return JournaledApplyResult(
        schema_version=SCHEMA_VERSION,
        feature_id=JOURNALED_APPLY_EXECUTOR_FEATURE_ID,
        status="blocked",
        transaction_id=transaction_id,
        target_file=target_file,
        source_content_hash_before=source_hash_before,
        source_content_hash_after="",
        preview_root=preview_root,
        rollback_manifest_path=root + "/JOURNALED_ROLLBACK_MANIFEST.json",
        execution_manifest_path=root + "/JOURNALED_APPLY_EXECUTION.json",
        source_mutation_enabled=False,
        import_rewrite_enabled=False,
        lane_state=lane_state,
        transaction_state=transaction_state,
        blockers=sorted(set(blockers)),
        warnings=["ZERO_SOURCE_WRITES_ON_ENTRY_GATE_FAILURE"],
        checked_rules=checked_rules,
    )


def _authorization_hash(authorization: JournaledApplyAuthorization) -> str:
    body = {
        key: value
        for key, value in authorization.to_dict().items()
        if key != "authorization_hash"
    }
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
