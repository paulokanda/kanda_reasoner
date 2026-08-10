# project-path: kanda_reasoner_app/reasoner_context_bundle/handoff_boundary_contract.py
"""Build and verify the read-only Tool/Project handoff trust envelope."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from .schema_models import ProjectContext
from .tool_governance_resource import (
    project_overlay_policy_record,
    tool_governance_trust_record,
)

__all__ = [
    "HANDOFF_TRUST_SCHEMA_VERSION",
    "build_handoff_trust_envelope",
    "handoff_trust_contract_failures",
]

HANDOFF_TRUST_SCHEMA_VERSION = "1.1"


def _path_fingerprint(path: Path) -> str:
    """Return a non-reversible fingerprint for one canonical filesystem root."""
    resolved = path.expanduser().resolve(strict=False)
    key = os.path.normcase(str(resolved))
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def _canonical_json_bytes(payload: Mapping[str, Any]) -> bytes:
    """Return deterministic JSON bytes for digest generation."""
    text = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return text.encode("utf-8")


def _boundary_payload(context: ProjectContext) -> dict[str, Any]:
    """Return the deterministic Tool/Project ownership declaration."""
    return {
        "tool": {
            "role": "KANDA_REASONER_TOOL",
            "project_slug": context.tool_project_slug,
            "source_root_marker": "<TOOL_ROOT>",
            "source_root_fingerprint": _path_fingerprint(
                context.tool_source_root
            ),
            "logical_source_owner": "KANDA_REASONER_TOOL",
        },
        "active_project": {
            "role": "ACTIVE_PROJECT",
            "project_slug": context.project_slug,
            "stable_project_id": context.active_project_id,
            "project_root_marker": "<PROJECT_ROOT>",
            "project_root_fingerprint": (
                context.active_project_root_fingerprint
            ),
            "project_support_root_marker": "<PROJECT_SUPPORT_ROOT>",
            "project_daily_work_root_marker": "<PROJECT_DAILY_WORK_ROOT>",
            "selection_mode": context.selection_mode,
            "same_physical_root": context.same_canonical_resolved_root,
            "self_hosting_mode": context.self_hosting_mode,
        },
        "ownership": {
            "tool_source_owner": "KANDA_REASONER_TOOL",
            "project_source_owner": "ACTIVE_PROJECT",
            "project_support_owner": "ACTIVE_PROJECT",
            "generated_handoff_owner": "REASONER_CONTEXT_BUNDLE",
            "filesystem_mutation_authority": (
                "KANDA_TOOL_RUNTIME_GOVERNED_APPLY"
            ),
        },
        "invariants": {
            "mixed_tool_project_patch_prohibited": True,
            "project_support_cannot_self_authorize": True,
            "generated_handoff_is_evidence_not_authority": True,
            "same_physical_root_does_not_merge_logical_roles": True,
            "remote_ai_filesystem_authority": "NONE",
            "write_enforcement_location": "OUTSIDE_REMOTE_AI",
        },
    }


def _content_trust_payload() -> dict[str, Any]:
    """Return the stable content-trust classification for remote handoff."""
    return {
        "tool_governance": {
            "classification": "TOOL_OWNED_PACKAGED_RESOURCE",
            "current_authority": "PROJECT_TOOL_BOUNDARY_CANON",
            "packaged_resource_anchor": tool_governance_trust_record(),
        },
        "project_policy_overlay": project_overlay_policy_record(),
        "project_content": {
            "classification": "UNTRUSTED_AS_TOOL_INSTRUCTIONS",
            "may_describe_project": True,
            "may_grant_tool_authority": False,
        },
        "generated_handoff": {
            "classification": "EVIDENCE_NOT_AUTHORITY",
            "may_orient_remote_ai": True,
            "may_grant_filesystem_authority": False,
        },
        "source_truth": {
            "classification": "EXACT_SOURCE_INSPECTION_REQUIRED",
            "generated_summary_can_replace_source": False,
        },
        "remote_ai": {
            "classification": "READ_ONLY_REASONING_PARTICIPANT",
            "filesystem_authority": "NONE",
            "write_authorization_owner": "KANDA_TOOL_RUNTIME",
        },
    }


def build_handoff_trust_envelope(
    context: ProjectContext,
) -> dict[str, Any]:
    """Build one deterministic trust envelope for all handoff artifacts."""
    digest_payload = {
        "schema_version": HANDOFF_TRUST_SCHEMA_VERSION,
        "tool_project_boundary": _boundary_payload(context),
        "content_trust": _content_trust_payload(),
    }
    digest = hashlib.sha256(_canonical_json_bytes(digest_payload)).hexdigest()
    return {
        **digest_payload,
        "boundary_digest_sha256": digest,
    }


def handoff_trust_contract_failures(
    payload: object,
    context: ProjectContext,
) -> list[str]:
    """Return deterministic failures for one handoff trust envelope."""
    if not isinstance(payload, Mapping):
        return ["handoff_trust must be an object"]
    expected = build_handoff_trust_envelope(context)
    failures: list[str] = []
    if payload.get("schema_version") != HANDOFF_TRUST_SCHEMA_VERSION:
        failures.append("handoff_trust schema_version mismatch")
    if payload.get("boundary_digest_sha256") != expected[
        "boundary_digest_sha256"
    ]:
        failures.append("handoff_trust boundary digest mismatch")
    if payload.get("tool_project_boundary") != expected[
        "tool_project_boundary"
    ]:
        failures.append("handoff_trust Tool/Project boundary mismatch")
    if payload.get("content_trust") != expected["content_trust"]:
        failures.append("handoff_trust content classification mismatch")
    return failures
