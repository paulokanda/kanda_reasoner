# project-path: kanda_reasoner_app/error_memory_gui/_ai_correction_contracts.py
"""Immutable request identity for Error Memory correction jobs."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kanda_reasoner_app.error_memory_gui import _ai_mode_runtime
from kanda_reasoner_app.project_support_boundary import (
    ProjectToolBoundaryIdentity,
    resolve_project_tool_boundary_identity,
)

__all__ = [
    "ErrorMemoryCorrectionIdentity",
    "build_correction_identity",
    "current_project_identity",
    "input_snapshot_hash",
    "payload_size_bytes",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class ErrorMemoryCorrectionIdentity:
    """Bind one correction to Project, input, mode, and Web configuration."""

    request_id: str
    operation_id: str
    generation: int
    active_project_id: str
    active_project_slug: str
    active_project_root_fingerprint: str
    active_project_support_root: str
    input_snapshot_hash: str
    assistant_mode: str
    gateway_id: str
    model_id: str
    configuration_revision: str
    privacy_approval_id: str
    created_at_utc: str


def current_project_identity(tab: Any) -> ProjectToolBoundaryIdentity:
    """Resolve the exact Project selected by the Error Memory tab."""
    root = Path(getattr(tab, "_project_root", ""))
    return resolve_project_tool_boundary_identity(root)


def input_snapshot_hash(intake_text: str, editor_text: str) -> str:
    """Hash the exact ordered Error Memory text sent for correction."""
    payload = json.dumps(
        {"intake_text": str(intake_text), "editor_text": str(editor_text)},
        ensure_ascii=False,
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def payload_size_bytes(intake_text: str, editor_text: str) -> int:
    """Return the exact UTF-8 payload size before prompt framing."""
    return len(str(intake_text).encode("utf-8")) + len(
        str(editor_text).encode("utf-8")
    )


def build_correction_identity(
    tab: Any,
    *,
    generation: int,
    intake_text: str,
    editor_text: str,
    approval_id: str,
    local_model_id: str = "",
) -> tuple[ErrorMemoryCorrectionIdentity, ProjectToolBoundaryIdentity]:
    """Return one complete immutable identity and its resolved Project."""
    project = current_project_identity(tab)
    mode = _ai_mode_runtime.selected_mode(tab)
    gateway_id = "local"
    model_id = str(local_model_id or "auto")
    revision = ""
    if mode == _ai_mode_runtime.LOCAL_AI_MODE:
        snapshot = _ai_mode_runtime.local_configuration(tab).snapshot()
        model_id = snapshot.model_id
        revision = snapshot.revision
    elif mode == _ai_mode_runtime.WEB_AI_MODE:
        snapshot = _ai_mode_runtime.central_configuration(tab).snapshot()
        gateway_id = snapshot.gateway_id
        model_id = snapshot.model_id
        revision = snapshot.revision
    identity = ErrorMemoryCorrectionIdentity(
        request_id=uuid.uuid4().hex,
        operation_id=uuid.uuid4().hex,
        generation=int(generation),
        active_project_id=project.active_project_id,
        active_project_slug=project.active_project_slug,
        active_project_root_fingerprint=project.active_project_root_fingerprint,
        active_project_support_root=str(project.active_project_support_root),
        input_snapshot_hash=input_snapshot_hash(intake_text, editor_text),
        assistant_mode=mode,
        gateway_id=gateway_id,
        model_id=model_id,
        configuration_revision=revision,
        privacy_approval_id=str(approval_id or ""),
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )
    return identity, project
