# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_apply_contracts.py
"""Define one-use authorization contracts for Project Web AI source apply.

The Web AI provider never creates or holds these authorizations. They are built
locally only after a validated Shadow Preview and explicit human confirmation.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from kanda_reasoner_app.reasoner_engine.project_web_ai_change_contracts import (
    ProjectWebAIChangeOperation,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
    ProjectWebAISessionIdentity,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
    ProjectWebAIShadowPreview,
)
from kanda_reasoner_app.web_ai_provider_contracts import ContextSnapshot

__all__ = [
    "ProjectWebAIApplyAuthorization",
    "ProjectWebAIApplyContractError",
    "build_apply_authorization",
    "preview_fingerprint",
    "required_confirmation_phrase",
]


class ProjectWebAIApplyContractError(RuntimeError):
    """Raised when Preview identity or human authorization is invalid."""


@dataclass(frozen=True)
class ProjectWebAIApplyAuthorization:
    """Bind one human approval to one exact immutable source transaction."""

    authorization_id: str
    transaction_id: str
    operation_id: str
    project_id: str
    project_root_fingerprint: str
    project_epoch: int
    snapshot_id: str
    preview_fingerprint: str
    target_paths: tuple[str, ...]
    source_sha256: tuple[str, ...]
    proposed_sha256: tuple[str, ...]
    authorized_at_utc: str


def required_confirmation_phrase(
    operation: ProjectWebAIChangeOperation,
    preview: ProjectWebAIShadowPreview,
) -> str:
    """Return the exact human phrase required for this Preview."""
    return (
        "APPLY "
        + operation.operation_id[:8].upper()
        + " TO "
        + str(len(preview.targets))
        + " FILES"
    )


def preview_fingerprint(preview: ProjectWebAIShadowPreview) -> str:
    """Return a deterministic fingerprint for the exact reviewed Preview."""
    payload = {
        "operation_id": preview.operation_id,
        "targets": [
            {
                "relative_path": item.relative_path,
                "original_sha256": item.original_sha256,
                "proposed_sha256": item.proposed_sha256,
                "unified_diff_sha256": hashlib.sha256(
                    item.unified_diff.encode("utf-8")
                ).hexdigest(),
            }
            for item in preview.targets
        ],
        "validation_markers": list(preview.validation_markers),
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_apply_authorization(
    *,
    operation: ProjectWebAIChangeOperation,
    preview: ProjectWebAIShadowPreview,
    session_identity: ProjectWebAISessionIdentity,
    context: ContextSnapshot,
    typed_phrase: str,
) -> ProjectWebAIApplyAuthorization:
    """Create one local one-use authorization after exact human confirmation."""
    if preview.operation_id != operation.operation_id:
        raise ProjectWebAIApplyContractError("APPLY_PREVIEW_OPERATION_MISMATCH")
    if not session_identity.accepts_request(operation.request_identity, context):
        raise ProjectWebAIApplyContractError("APPLY_SESSION_IDENTITY_STALE")
    expected_phrase = required_confirmation_phrase(operation, preview)
    if str(typed_phrase or "").strip() != expected_phrase:
        raise ProjectWebAIApplyContractError("APPLY_CONFIRMATION_PHRASE_MISMATCH")
    source_map = operation.source_by_path()
    target_paths = tuple(item.relative_path for item in preview.targets)
    if not target_paths or len(set(target_paths)) != len(target_paths):
        raise ProjectWebAIApplyContractError("APPLY_TARGET_SET_INVALID")
    source_hashes: list[str] = []
    proposed_hashes: list[str] = []
    for item in preview.targets:
        source = source_map.get(item.relative_path)
        if source is None or source.sha256 != item.original_sha256:
            raise ProjectWebAIApplyContractError(
                "APPLY_PREVIEW_SOURCE_IDENTITY_MISMATCH:" + item.relative_path
            )
        source_hashes.append(item.original_sha256)
        proposed_hashes.append(item.proposed_sha256)
    return ProjectWebAIApplyAuthorization(
        authorization_id=uuid.uuid4().hex,
        transaction_id=uuid.uuid4().hex,
        operation_id=operation.operation_id,
        project_id=operation.request_identity.project_id,
        project_root_fingerprint=(
            operation.request_identity.project_root_fingerprint
        ),
        project_epoch=operation.request_identity.project_epoch,
        snapshot_id=operation.request_identity.snapshot_id,
        preview_fingerprint=preview_fingerprint(preview),
        target_paths=target_paths,
        source_sha256=tuple(source_hashes),
        proposed_sha256=tuple(proposed_hashes),
        authorized_at_utc=datetime.now(timezone.utc).isoformat(),
    )
