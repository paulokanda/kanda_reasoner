# project-path: kanda_reasoner_app/freeze_after_update/ownership.py
"""Owner-scoped Freeze evidence and Project Freeze Memory contracts."""

from __future__ import annotations

import json
import os
import re
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping

from kanda_reasoner_app.memory_ownership import (
    MemoryOwnerContext,
    OwnerScope,
    project_owner_context,
    tool_owner_context,
)

__all__ = [
    "FreezeOwnershipError",
    "FreezeStoreKind",
    "assert_project_freeze_memory_owner",
    "assert_tool_freeze_evidence_owner",
    "inject_freeze_owner_metadata",
    "project_freeze_memory_owner",
    "tool_freeze_evidence_owner",
    "tool_freeze_evidence_root",
    "write_tool_freeze_evidence",
]


class FreezeOwnershipError(RuntimeError):
    """Raised when a Freeze operation targets the wrong logical owner."""


class FreezeStoreKind(str, Enum):
    """Durable Freeze store roles."""

    PROJECT_MEMORY = "PROJECT_MEMORY"
    TOOL_EVIDENCE = "TOOL_EVIDENCE"


@dataclass(frozen=True)
class FreezeOwnerBinding:
    """Bind one Freeze store kind to one system owner context."""

    owner: MemoryOwnerContext
    store_kind: FreezeStoreKind
    store_root: Path

    def canonical_fields(self) -> dict[str, str]:
        fields = self.owner.canonical_fields()
        fields["freeze_store_kind"] = self.store_kind.value
        return fields


def _same_path(first: Path, second: Path) -> bool:
    """Return whether two paths identify the same canonical location."""
    return os.path.normcase(str(first.resolve(strict=False))) == os.path.normcase(
        str(second.resolve(strict=False))
    )


def project_freeze_memory_owner(
    project_root: str | Path,
) -> FreezeOwnerBinding:
    """Return the selected Project Freeze Memory owner binding."""
    owner = project_owner_context(
        project_root,
        affected_box="Project Freeze Memory",
    )
    return FreezeOwnerBinding(
        owner=owner,
        store_kind=FreezeStoreKind.PROJECT_MEMORY,
        store_root=owner.support_root / "project_freeze_after_update",
    )


def tool_freeze_evidence_root(
    tool_source_root: str | Path | None = None,
) -> Path:
    """Return the Tool-only Freeze evidence root."""
    return tool_owner_context(tool_source_root).support_root / "tool_freeze_evidence"


def tool_freeze_evidence_owner(
    tool_source_root: str | Path | None = None,
) -> FreezeOwnerBinding:
    """Return the Tool Freeze evidence owner binding."""
    owner = tool_owner_context(
        tool_source_root,
        affected_box="Tool Freeze Evidence",
    )
    return FreezeOwnerBinding(
        owner=owner,
        store_kind=FreezeStoreKind.TOOL_EVIDENCE,
        store_root=tool_freeze_evidence_root(tool_source_root),
    )


def assert_project_freeze_memory_owner(
    binding: FreezeOwnerBinding,
    project_root: str | Path,
) -> None:
    """Reject Tool or stale Project authority for Project Freeze Memory."""
    if binding.owner.owner_scope is not OwnerScope.PROJECT:
        raise FreezeOwnershipError("TOOL_FREEZE_PROJECT_STORE_REJECTED")
    expected = project_freeze_memory_owner(project_root)
    if binding.store_kind is not FreezeStoreKind.PROJECT_MEMORY:
        raise FreezeOwnershipError("PROJECT_FREEZE_STORE_KIND_INVALID")
    if binding.owner.owner_id != expected.owner.owner_id:
        raise FreezeOwnershipError("STALE_PROJECT_CONTEXT_MEMORY_WRITE_REJECTED")
    if not _same_path(binding.store_root, expected.store_root):
        raise FreezeOwnershipError("PROJECT_FREEZE_OWNER_ROOT_MISMATCH")


def assert_tool_freeze_evidence_owner(
    binding: FreezeOwnerBinding,
    tool_source_root: str | Path | None = None,
) -> None:
    """Reject Project authority for Tool Freeze evidence."""
    if binding.owner.owner_scope is not OwnerScope.TOOL:
        raise FreezeOwnershipError("PROJECT_FREEZE_TOOL_STORE_REJECTED")
    expected = tool_freeze_evidence_owner(tool_source_root)
    if binding.store_kind is not FreezeStoreKind.TOOL_EVIDENCE:
        raise FreezeOwnershipError("TOOL_FREEZE_STORE_KIND_INVALID")
    if binding.owner.owner_id != expected.owner.owner_id:
        raise FreezeOwnershipError("TOOL_FREEZE_OWNER_ID_MISMATCH")
    if not _same_path(binding.store_root, expected.store_root):
        raise FreezeOwnershipError("TOOL_FREEZE_OWNER_ROOT_MISMATCH")


def _inject_frontmatter(markdown: str, fields: Mapping[str, str]) -> str:
    """Insert system owner fields into one generated Freeze entry Markdown."""
    lines = str(markdown or "").splitlines()
    if not lines or lines[0].strip() != "---":
        return markdown
    insert_at = 1
    while insert_at < len(lines) and not lines[insert_at].startswith("protected_paths:"):
        insert_at += 1
    owner_lines = [f'{key}: "{str(value).replace(chr(34), chr(39))}"' for key, value in fields.items()]
    lines[insert_at:insert_at] = owner_lines
    section = [
        "",
        "## memory ownership",
        "",
        *[f"{key}: `{value}`" for key, value in fields.items()],
    ]
    try:
        summary_index = lines.index("## summary")
    except ValueError:
        lines.extend(section)
    else:
        lines[summary_index:summary_index] = section + [""]
    return "\n".join(lines)


def inject_freeze_owner_metadata(
    preview: Mapping[str, Any],
    binding: FreezeOwnerBinding,
) -> dict[str, Any]:
    """Overwrite any supplied owner fields with system-assigned metadata."""
    result = dict(preview)
    fields = binding.canonical_fields()
    result.update(fields)
    result["markdown"] = _inject_frontmatter(
        str(result.get("markdown") or ""),
        fields,
    )
    return result


def _safe_feature_id(value: str) -> str:
    """Return a deterministic filename-safe feature ID."""
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", str(value or "")).strip("._-")
    if not safe:
        raise FreezeOwnershipError("TOOL_FREEZE_FEATURE_ID_REQUIRED")
    return safe


def _atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    """Atomically write one UTF-8 JSON record."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temp_name = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(dict(payload), stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def write_tool_freeze_evidence(
    tool_source_root: str | Path,
    feature_id: str,
    evidence: Mapping[str, Any],
    *,
    owner_binding: FreezeOwnerBinding | None = None,
) -> Path:
    """Write Tool-owned validation evidence, never Project Freeze Memory."""
    binding = owner_binding or tool_freeze_evidence_owner(tool_source_root)
    assert_tool_freeze_evidence_owner(binding, tool_source_root)
    payload = dict(evidence)
    payload.update(binding.canonical_fields())
    payload["schema_version"] = "1.0"
    payload["artifact_type"] = "tool_freeze_evidence"
    payload["feature_id"] = str(feature_id)
    path = binding.store_root / (_safe_feature_id(feature_id) + ".json")
    _atomic_write_json(path, payload)
    return path
