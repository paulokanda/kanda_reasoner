# project-path: kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_contracts.py
"""Immutable request identity for Freeze formulary provider jobs."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.project_support_boundary import (
    ProjectToolBoundaryIdentity,
    resolve_project_tool_boundary_identity,
)

__all__ = [
    "FreezeFormularyIdentity",
    "build_freeze_formulary_identity",
    "form_snapshot_hash",
    "form_payload_size_bytes",
]


@dataclass(frozen=True, slots=True, kw_only=True)
class FreezeFormularyIdentity:
    """Bind one formulary request to Project, form, mode, and Web config."""

    request_id: str
    operation_id: str
    generation: int
    active_project_id: str
    active_project_slug: str
    active_project_root_fingerprint: str
    active_project_support_root: str
    form_snapshot_hash: str
    assistant_mode: str
    gateway_id: str
    model_id: str
    configuration_revision: str
    privacy_approval_id: str
    created_at_utc: str


def _canonical_inputs(inputs: Mapping[str, Any]) -> dict[str, str]:
    """Return a deterministic string-only freeze form payload."""
    return {
        str(key): str(value or "")
        for key, value in sorted(inputs.items(), key=lambda item: str(item[0]))
    }


def form_snapshot_hash(inputs: Mapping[str, Any]) -> str:
    """Hash the exact freeze form snapshot sent to a provider."""
    payload = json.dumps(
        _canonical_inputs(inputs),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def form_payload_size_bytes(inputs: Mapping[str, Any]) -> int:
    """Return the exact UTF-8 payload size before prompt framing."""
    return len(
        json.dumps(
            _canonical_inputs(inputs),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )


def build_freeze_formulary_identity(
    *,
    project_root: str | Path,
    generation: int,
    inputs: Mapping[str, Any],
    assistant_mode: str,
    approval_id: str = "",
    gateway_id: str = "",
    model_id: str = "",
    configuration_revision: str = "",
) -> tuple[FreezeFormularyIdentity, ProjectToolBoundaryIdentity]:
    """Return one complete immutable identity and resolved Project boundary."""
    project = resolve_project_tool_boundary_identity(project_root)
    mode = str(assistant_mode or "heuristic").strip().lower()
    identity = FreezeFormularyIdentity(
        request_id=uuid.uuid4().hex,
        operation_id=uuid.uuid4().hex,
        generation=int(generation),
        active_project_id=project.active_project_id,
        active_project_slug=project.active_project_slug,
        active_project_root_fingerprint=project.active_project_root_fingerprint,
        active_project_support_root=str(project.active_project_support_root),
        form_snapshot_hash=form_snapshot_hash(inputs),
        assistant_mode=mode,
        gateway_id=str(gateway_id or ("local" if mode == "local" else "")),
        model_id=str(model_id or ("auto" if mode == "local" else "")),
        configuration_revision=str(configuration_revision or ""),
        privacy_approval_id=str(approval_id or ""),
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )
    return identity, project
