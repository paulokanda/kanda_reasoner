# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_task_contracts.py
"""Immutable request identity and source-bound items for Docstring AI jobs."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    ProjectSupportBoundaryError,
    ProjectToolBoundaryIdentity,
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.tab3_manual_review_runtime import (
    ai_docstring_row_bridge_runtime,
    ai_web_controls_runtime,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderRequest,
    AIProviderResult,
)

__all__ = [
    "DocstringTaskIdentity",
    "DocstringTaskItem",
    "DocstringTaskOutcome",
    "build_identity",
    "build_items",
    "current_project_identity",
    "job_input_hash",
    "payload_bytes",
    "row_snapshot_hash",
    "text_hash",
]

_DRAFT_FIELDS = (
    "draft_docstring",
    "ai_draft_docstring",
    "ai_provider",
    "ai_status",
    "ai_error",
    "ai_used_fallback",
    "selected_draft_source",
    "ai_docstring_verbosity",
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DocstringTaskIdentity:
    """Bind one draft job to an immutable Project and assistant selection."""

    request_id: str
    session_id: str
    tab_id: str
    operation_id: str
    active_project_id: str
    active_project_slug: str
    active_project_root_fingerprint: str
    active_project_support_root: str
    input_snapshot_hash: str
    schema_id: str
    schema_version: str
    assistant_mode: str
    gateway_id: str
    model_id: str
    privacy_approval_id: str
    created_at_utc: str
    configuration_revision: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class DocstringTaskItem:
    """Describe one immutable row request sent to a worker."""

    item_id: str
    request: AIProviderRequest
    source_path: str
    source_hash: str
    row_snapshot_hash: str


@dataclass(frozen=True, slots=True, kw_only=True)
class DocstringTaskOutcome:
    """Return one provider result without mutating GUI-owned rows."""

    item_id: str
    result: AIProviderResult


def current_project_identity(owner: object) -> ProjectToolBoundaryIdentity:
    """Resolve the exact selected Project through the canonical owner."""
    widget = getattr(owner, "_root_path_edit", None)
    method = getattr(widget, "text", None)
    root = str(method() or "").strip() if callable(method) else ""
    if not root:
        raise ProjectSupportBoundaryError("ACTIVE_PROJECT_ROOT_NOT_SELECTED")
    return resolve_project_tool_boundary_identity(Path(root))


def build_items(
    owner: object,
    identity: ProjectToolBoundaryIdentity,
    rows: list[dict],
) -> tuple[tuple[DocstringTaskItem, ...], dict[str, dict], list[dict]]:
    """Build immutable requests and GUI-owned row mappings."""
    items: list[DocstringTaskItem] = []
    row_map: dict[str, dict] = {}
    snapshot: list[dict] = []
    for row in rows:
        source_path = _row_source_path(identity.active_project_root, row)
        module_text = source_path.read_text(encoding="utf-8", errors="replace")
        request = ai_docstring_row_bridge_runtime.build_review_row_ai_request(
            owner,
            row,
            module_text,
        )
        item_id = uuid.uuid4().hex
        items.append(
            DocstringTaskItem(
                item_id=item_id,
                request=request,
                source_path=str(source_path),
                source_hash=text_hash(module_text),
                row_snapshot_hash=row_snapshot_hash(row, request),
            )
        )
        row_map[item_id] = row
        fields = {name: row.get(name) for name in _DRAFT_FIELDS}
        present = [name for name in _DRAFT_FIELDS if name in row]
        snapshot.append({"row": row, "fields": fields, "present": present})
    return tuple(items), row_map, snapshot


def build_identity(
    owner: object,
    project: ProjectToolBoundaryIdentity,
    *,
    operation_id: str,
    input_hash: str,
    gateway_id: str,
    approval_id: str,
) -> DocstringTaskIdentity:
    """Return the complete immutable task request identity."""
    mode = ai_web_controls_runtime.provider_mode_from_owner(owner)
    session_id = str(getattr(owner, "_docstring_ai_session_id", "") or "")
    if not session_id:
        session_id = uuid.uuid4().hex
        owner._docstring_ai_session_id = session_id
    return DocstringTaskIdentity(
        request_id=uuid.uuid4().hex,
        session_id=session_id,
        tab_id="docstring_assistant",
        operation_id=operation_id,
        active_project_id=project.active_project_id,
        active_project_slug=project.active_project_slug,
        active_project_root_fingerprint=project.active_project_root_fingerprint,
        active_project_support_root=str(project.active_project_support_root),
        input_snapshot_hash=input_hash,
        schema_id="docstring_draft",
        schema_version="1.0",
        assistant_mode=mode,
        gateway_id=gateway_id,
        model_id=ai_web_controls_runtime.selected_model_id(owner),
        privacy_approval_id=approval_id,
        configuration_revision=ai_web_controls_runtime.configuration_revision(owner),
        created_at_utc=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    )


def row_snapshot_hash(row: dict, request: AIProviderRequest) -> str:
    """Hash row identity and exact task input fields."""
    payload = {
        "file": row.get("file") or row.get("path"),
        "line": row.get("line") or row.get("insert_line"),
        "target": row.get("target_name") or row.get("name"),
        "signature": row.get("signature") or row.get("target_signature"),
        "request": {
            "relative_file_path": request.relative_file_path,
            "symbol_kind": request.symbol_kind,
            "symbol_name": request.symbol_name,
            "signature": request.signature,
            "source_snippet": request.source_snippet,
            "heuristic_draft": request.heuristic_draft,
            "docstring_style": request.docstring_style,
            "docstring_verbosity": request.docstring_verbosity,
        },
    }
    return text_hash(json.dumps(payload, sort_keys=True, ensure_ascii=False))


def job_input_hash(items: tuple[DocstringTaskItem, ...]) -> str:
    """Hash the ordered immutable task items."""
    payload = [
        {
            "source_hash": item.source_hash,
            "row_snapshot_hash": item.row_snapshot_hash,
            "relative_file_path": item.request.relative_file_path,
        }
        for item in items
    ]
    return text_hash(json.dumps(payload, sort_keys=True, ensure_ascii=False))


def payload_bytes(items: tuple[DocstringTaskItem, ...]) -> int:
    """Return a conservative UTF-8 cloud-payload estimate."""
    return sum(
        len(item.request.source_snippet.encode("utf-8"))
        + len(item.request.heuristic_draft.encode("utf-8"))
        + len(item.request.signature.encode("utf-8"))
        for item in items
    )


def text_hash(text: str) -> str:
    """Return a stable UTF-8 SHA-256 digest."""
    return hashlib.sha256(str(text).encode("utf-8")).hexdigest()


def _row_source_path(project_root: Path, row: dict) -> Path:
    """Resolve one row path and block reads outside active Project source."""
    raw = Path(str(row.get("file") or row.get("path") or "").strip())
    path = raw if raw.is_absolute() else project_root / raw
    path = path.resolve(strict=False)
    try:
        path.relative_to(project_root.resolve(strict=False))
    except ValueError as exc:
        raise ProjectSupportBoundaryError(
            "DOCSTRING_SOURCE_OUTSIDE_ACTIVE_PROJECT"
        ) from exc
    if not path.exists() or not path.is_file():
        raise OSError("Docstring source file is missing: " + str(path))
    return path
