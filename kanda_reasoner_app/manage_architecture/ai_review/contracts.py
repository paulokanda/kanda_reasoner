# project-path: kanda_reasoner_app/manage_architecture/ai_review/contracts.py
"""Immutable Project/input/configuration identity for Audit Project review."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_support_boundary import (
    ProjectToolBoundaryIdentity,
    resolve_project_tool_boundary_identity,
)

from .models import WEB_AI_MODE

__all__ = [
    "AuditReviewIdentity",
    "audit_snapshot_hash",
    "build_audit_review_identity",
    "current_project_identity",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class AuditReviewIdentity:
    """Bind one advisory review to exact Project, audit text, and provider."""

    request_id: str
    operation_id: str
    generation: int
    active_project_id: str
    active_project_slug: str
    active_project_root_fingerprint: str
    active_project_support_root: str
    audit_snapshot_hash: str
    provider_mode: str
    gateway_id: str
    model_id: str
    configuration_revision: str
    privacy_approval_id: str
    created_at_utc: str


def current_project_identity(window: Any) -> ProjectToolBoundaryIdentity:
    """Resolve the exact Project selected in Audit Project."""
    root = Path(str(window._root_path_edit.text() or "").strip())
    return resolve_project_tool_boundary_identity(root)


def audit_snapshot_hash(audit_text: str) -> str:
    """Hash the exact UTF-8 Project Audit Results text sent for review."""
    return hashlib.sha256(str(audit_text).encode("utf-8")).hexdigest()


def build_audit_review_identity(
    window: Any,
    *,
    generation: int,
    audit_text: str,
    provider_mode: str,
    approval_id: str,
    local_model_id: str = "auto",
) -> tuple[AuditReviewIdentity, ProjectToolBoundaryIdentity]:
    """Return one complete immutable review identity and resolved Project."""
    project = current_project_identity(window)
    gateway_id = "local"
    model_id = str(local_model_id or "auto")
    revision = ""
    if provider_mode == "local":
        snapshot = window._audit_local_ai_configuration.snapshot()
        model_id = snapshot.model_id
        revision = snapshot.revision
    elif provider_mode == WEB_AI_MODE:
        snapshot = window._audit_web_ai_configuration.snapshot()
        gateway_id = snapshot.gateway_id
        model_id = snapshot.model_id
        revision = snapshot.revision
    identity = AuditReviewIdentity(
        request_id=uuid.uuid4().hex,
        operation_id=uuid.uuid4().hex,
        generation=int(generation),
        active_project_id=project.active_project_id,
        active_project_slug=project.active_project_slug,
        active_project_root_fingerprint=project.active_project_root_fingerprint,
        active_project_support_root=str(project.active_project_support_root),
        audit_snapshot_hash=audit_snapshot_hash(audit_text),
        provider_mode=str(provider_mode),
        gateway_id=gateway_id,
        model_id=model_id,
        configuration_revision=revision,
        privacy_approval_id=str(approval_id or ""),
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )
    return identity, project
