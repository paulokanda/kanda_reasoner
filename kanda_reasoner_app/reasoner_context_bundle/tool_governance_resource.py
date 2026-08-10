# project-path: kanda_reasoner_app/reasoner_context_bundle/tool_governance_resource.py
"""Load and synchronize the Tool-owned packaged governance resource.

The runtime authority is loaded only through :mod:`importlib.resources` from
inside the KANDA Reasoner package.  Source-install maintenance may compare or
synchronize that packaged copy against the canonical Prompt Library canon, but
Project roots, Project Support, working directories, and generated handoff
artifacts are never accepted as governance authority.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Mapping

__all__ = [
    "ToolGovernanceResource",
    "ToolGovernanceResourceError",
    "canonical_governance_source_path",
    "governance_source_package_sync",
    "load_tool_governance_resource",
    "project_overlay_policy_record",
    "sync_packaged_governance_resource",
    "tool_governance_trust_record",
    "validate_project_policy_overlay",
]

_RESOURCE_PACKAGE = "kanda_reasoner_app.reasoner_context_bundle"
_RESOURCE_RELATIVE = "resources/project_tool_boundary_canon.md"
_CANONICAL_SOURCE_RELATIVE = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "12_generalized_project_canons/project_tool_boundary_canon.md"
)
_EXPECTED_PROMPT_ID = "project_tool_boundary_canon"
_EXPECTED_PROMPT_CODE = "KPR-12-001"
_FORBIDDEN_OVERLAY_KEYS = frozenset(
    {
        "allow_tool_writes",
        "authorize_tool_writes",
        "disable_human_confirmation",
        "filesystem_authority",
        "owner_id",
        "owner_identity",
        "project_selection",
        "relax_tool_boundary",
        "replace_tool_governance",
        "selection_mode",
        "tool_source_owner",
    }
)
_ALLOWED_OVERLAY_KEYS = frozenset(
    {"additional_restrictions", "notes", "overlay_id"}
)


class ToolGovernanceResourceError(RuntimeError):
    """Raised when packaged Tool governance is absent or inconsistent."""


@dataclass(frozen=True)
class ToolGovernanceResource:
    """Immutable identity and text for the packaged Tool governance canon."""

    prompt_id: str
    prompt_code: str
    version: str
    status: str
    resource_package: str
    resource_relative_path: str
    sha256: str
    text: str

    def as_trust_record(self) -> dict[str, Any]:
        """Return the compact machine-readable handoff authority record."""
        return {
            "authority_kind": "TOOL_OWNED_PACKAGED_RESOURCE",
            "load_method": "importlib.resources",
            "prompt_id": self.prompt_id,
            "prompt_code": self.prompt_code,
            "version": self.version,
            "status": self.status,
            "resource_package": self.resource_package,
            "resource_relative_path": self.resource_relative_path,
            "sha256": self.sha256,
            "project_shadowing_allowed": False,
            "generated_handoff_can_replace_resource": False,
        }


def _sha256_bytes(content: bytes) -> str:
    """Return the SHA-256 digest for one byte sequence."""
    return hashlib.sha256(content).hexdigest()


def _resource_traversable():
    """Return the package-owned resource without consulting filesystem roots."""
    current = resources.files(_RESOURCE_PACKAGE)
    for part in _RESOURCE_RELATIVE.split("/"):
        current = current.joinpath(part)
    return current


def _read_packaged_bytes() -> bytes:
    """Read the runtime governance resource and fail closed when unavailable."""
    try:
        content = _resource_traversable().read_bytes()
    except (FileNotFoundError, ModuleNotFoundError, OSError) as exc:
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_PACKAGED_RESOURCE_UNREADABLE"
        ) from exc
    if not content.strip():
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_PACKAGED_RESOURCE_EMPTY"
        )
    return content


def _header_value(text: str, label: str) -> str:
    """Extract one exact human-readable canon header field."""
    prefix = label + ":"
    for line in text.splitlines()[:40]:
        if line.startswith(prefix):
            value = line[len(prefix) :].strip()
            if value:
                return value
    raise ToolGovernanceResourceError(
        "TOOL_GOVERNANCE_HEADER_MISSING:" + label
    )


def load_tool_governance_resource() -> ToolGovernanceResource:
    """Load the hard Tool governance authority from the packaged resource."""
    content = _read_packaged_bytes()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_PACKAGED_RESOURCE_NOT_UTF8"
        ) from exc
    prompt_id = _header_value(text, "Prompt ID")
    prompt_code = _header_value(text, "Prompt code")
    version = _header_value(text, "Version")
    status = _header_value(text, "Status")
    if prompt_id != _EXPECTED_PROMPT_ID or prompt_code != _EXPECTED_PROMPT_CODE:
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_PACKAGED_RESOURCE_IDENTITY_MISMATCH"
        )
    if status.casefold() not in {"active", "active prompt-library canon"}:
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_PACKAGED_RESOURCE_NOT_ACTIVE"
        )
    return ToolGovernanceResource(
        prompt_id=prompt_id,
        prompt_code=prompt_code,
        version=version,
        status=status,
        resource_package=_RESOURCE_PACKAGE,
        resource_relative_path=_RESOURCE_RELATIVE,
        sha256=_sha256_bytes(content),
        text=text,
    )


def canonical_governance_source_path(tool_root: str | Path) -> Path:
    """Return the canonical Prompt Library source path for source maintenance."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    return root / _CANONICAL_SOURCE_RELATIVE


def _packaged_source_path(tool_root: str | Path) -> Path:
    """Return the source-tree location of the generated packaged copy."""
    root = Path(tool_root).expanduser().resolve(strict=False)
    return root / "kanda_reasoner_app/reasoner_context_bundle" / _RESOURCE_RELATIVE


def governance_source_package_sync(tool_root: str | Path) -> dict[str, Any]:
    """Compare canonical source bytes with the source-tree packaged copy."""
    source = canonical_governance_source_path(tool_root)
    packaged = _packaged_source_path(tool_root)
    if not source.is_file():
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_CANONICAL_SOURCE_MISSING:" + str(source)
        )
    if not packaged.is_file():
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_PACKAGED_SOURCE_MISSING:" + str(packaged)
        )
    source_bytes = source.read_bytes()
    packaged_bytes = packaged.read_bytes()
    return {
        "canonical_source": str(_CANONICAL_SOURCE_RELATIVE).replace(os.sep, "/"),
        "packaged_resource": _RESOURCE_RELATIVE,
        "canonical_sha256": _sha256_bytes(source_bytes),
        "packaged_sha256": _sha256_bytes(packaged_bytes),
        "byte_identical": source_bytes == packaged_bytes,
    }


def sync_packaged_governance_resource(tool_root: str | Path) -> dict[str, Any]:
    """Synchronize the packaged copy from the canonical Prompt Library source."""
    source = canonical_governance_source_path(tool_root)
    target = _packaged_source_path(tool_root)
    if not source.is_file():
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_CANONICAL_SOURCE_MISSING:" + str(source)
        )
    content = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_bytes(content)
    os.replace(temporary, target)
    result = governance_source_package_sync(tool_root)
    if result["byte_identical"] is not True:
        raise ToolGovernanceResourceError(
            "TOOL_GOVERNANCE_SOURCE_PACKAGE_SYNC_FAILED"
        )
    return result


def validate_project_policy_overlay(
    overlay: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Accept only Project overlays that add restrictions without authority."""
    if overlay is None:
        return {
            "mode": "STRICTER_ONLY",
            "overlay_present": False,
            "additional_restrictions": [],
        }
    if not isinstance(overlay, Mapping):
        raise ToolGovernanceResourceError("PROJECT_POLICY_OVERLAY_NOT_OBJECT")
    keys = {str(key) for key in overlay}
    forbidden = sorted(keys & _FORBIDDEN_OVERLAY_KEYS)
    if forbidden:
        raise ToolGovernanceResourceError(
            "PROJECT_POLICY_OVERLAY_RELAXATION_REJECTED:" + ",".join(forbidden)
        )
    unknown = sorted(keys - _ALLOWED_OVERLAY_KEYS)
    if unknown:
        raise ToolGovernanceResourceError(
            "PROJECT_POLICY_OVERLAY_UNKNOWN_FIELD:" + ",".join(unknown)
        )
    raw_restrictions = overlay.get("additional_restrictions", [])
    if not isinstance(raw_restrictions, (list, tuple)):
        raise ToolGovernanceResourceError(
            "PROJECT_POLICY_OVERLAY_RESTRICTIONS_NOT_LIST"
        )
    restrictions: list[str] = []
    for raw in raw_restrictions:
        text = str(raw).strip()
        if not text:
            raise ToolGovernanceResourceError(
                "PROJECT_POLICY_OVERLAY_EMPTY_RESTRICTION"
            )
        restrictions.append(text)
    return {
        "mode": "STRICTER_ONLY",
        "overlay_present": True,
        "overlay_id": str(overlay.get("overlay_id", "")).strip(),
        "additional_restrictions": restrictions,
        "notes": str(overlay.get("notes", "")).strip(),
    }


def project_overlay_policy_record() -> dict[str, Any]:
    """Return immutable limits on Project-supplied governance overlays."""
    return {
        "mode": "STRICTER_ONLY",
        "allowed_capability": "ADD_RESTRICTIONS_ONLY",
        "cannot_relax_tool_boundaries": True,
        "cannot_authorize_tool_writes": True,
        "cannot_disable_human_confirmation": True,
        "cannot_replace_tool_governance": True,
        "cannot_change_project_selection": True,
        "cannot_change_owner_identity": True,
    }


def tool_governance_trust_record() -> dict[str, Any]:
    """Return the packaged authority descriptor used by handoff trust."""
    return load_tool_governance_resource().as_trust_record()
