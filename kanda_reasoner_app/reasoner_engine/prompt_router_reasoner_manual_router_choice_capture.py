# project-path: kanda_reasoner_app/reasoner_engine/prompt_router_reasoner_manual_router_choice_capture.py
"""Manual Router Choice Capture helpers for Prompt Router Reasoner.

This module validates a browser-ChatGPT routing-choice block, resolves the
selected prompt codes/ids to project-local canonical prompt files, assembles an
editable final prompt, and stores an audit artifact under the Prompt Router
Reasoner review folder.

It intentionally does not call ML, mutate router configuration, mutate prompt
library files, write freeze memory, or append to the strict heuristic-vs-ML
review log used for pilot-readiness metrics.
"""

from __future__ import annotations


__all__ = [
    'assemble_final_prompt',
    'build_example_routing_choice_block',
    'candidate_prompt_paths',
    'capture_manual_router_choice',
    'extract_manual_router_choice_payload',
    'find_prompt_metadata_by_code',
    'ManualRouterChoiceCaptureError',
    'normalize_selected_prompt_choice',
    'read_prompt_text',
    'resolve_safe_active_prompt_path',
    'resolve_selected_prompt',
    'validate_manual_router_choice_payload',
    'write_manual_router_choice_capture',
]
from datetime import datetime, timezone
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from kanda_reasoner_app.reasoner_engine.prompt_router_reasoner_review_store import (
    REVIEW_FOLDER_NAME,
)

CHOICE_START_MARKER = "KANDA_ROUTING_CHOICE_START"
CHOICE_END_MARKER = "KANDA_ROUTING_CHOICE_END"
MANUAL_CAPTURE_FOLDER_NAME = "manual_router_choice_captures"
SUPPORTED_EVENT_TYPES = {
    "chatgpt_router_prompt_choice",
    "external_chatgpt_route_suggestion",
    "manual_router_choice_capture",
}
PROMPT_CODE_RE = re.compile(r"^KPR-\d{2}-\d{3}$")
BLOCKED_PART_NAMES = {
    "project_freeze_after_update",
    "project_freeze_ledger",
    "frozen_features_memory",
    "freeze_hint_intake",
}
FORBIDDEN_PAYLOAD_KEYS = {
    "final_route_decision",
    "write_files",
    "mutate_files",
    "apply_patch",
    "freeze_memory_write",
    "project_freeze_ledger_write",
    "selected_authoritative_router_mode",
}


class ManualRouterChoiceCaptureError(ValueError):
    """Raised when a manual router-choice block is unsafe or invalid."""


def utc_now_iso() -> str:
    """Return a UTC timestamp suitable for stored audit artifacts."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    """Return the SHA-256 hex digest for a UTF-8 text string."""
    return hashlib.sha256(str(text).encode("utf-8", errors="replace")).hexdigest()


def extract_manual_router_choice_payload(pasted_text: str) -> dict[str, Any]:
    """Extract a JSON routing-choice object from a pasted browser response.

    The preferred format is a JSON object between KANDA_ROUTING_CHOICE_START
    and KANDA_ROUTING_CHOICE_END markers. For convenience, a bare JSON object
    is also accepted. The parsed result must be a JSON object.
    """
    raw_text = str(pasted_text or "").strip()
    if not raw_text:
        raise ManualRouterChoiceCaptureError("Manual routing-choice paste is empty.")

    json_text = raw_text
    start_index = raw_text.find(CHOICE_START_MARKER)
    end_index = raw_text.find(CHOICE_END_MARKER)
    if start_index >= 0 or end_index >= 0:
        if start_index < 0 or end_index < 0 or end_index <= start_index:
            raise ManualRouterChoiceCaptureError("Routing-choice markers are incomplete or out of order.")
        json_text = raw_text[start_index + len(CHOICE_START_MARKER) : end_index].strip()

    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ManualRouterChoiceCaptureError("Routing-choice block is not valid JSON: " + str(exc)) from exc

    if not isinstance(payload, dict):
        raise ManualRouterChoiceCaptureError("Routing-choice JSON must be an object.")
    return dict(payload)


def capture_manual_router_choice(project_root: str | Path, pasted_text: str) -> dict[str, Any]:
    """Validate, resolve, assemble, and audit a manual router-choice capture."""
    root = Path(project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ManualRouterChoiceCaptureError("Project root does not exist: " + str(root))

    raw_text = str(pasted_text or "")
    payload = extract_manual_router_choice_payload(raw_text)
    validated = validate_manual_router_choice_payload(payload)

    selected_prompts = validated["selected_prompts"]
    resolved_prompts = [resolve_selected_prompt(root, choice) for choice in selected_prompts]
    assembled_prompt = assemble_final_prompt(validated, resolved_prompts)
    audit_record = write_manual_router_choice_capture(
        root,
        raw_paste_text=raw_text,
        payload=validated,
        resolved_prompts=resolved_prompts,
        assembled_prompt=assembled_prompt,
    )

    return {
        "ok": True,
        "event_type": "manual_router_choice_capture",
        "source": str(validated.get("source", "chatgpt_browser_with_startup_router_context")),
        "user_request": str(validated.get("user_request", "")),
        "selected_total": len(resolved_prompts),
        "selected_prompt_codes": tuple(str(item.get("prompt_code", "")) for item in resolved_prompts),
        "selected_prompt_ids": tuple(str(item.get("prompt_id", "")) for item in resolved_prompts),
        "selected_prompt_paths": tuple(str(item.get("prompt_path", "")) for item in resolved_prompts),
        "assembled_prompt": assembled_prompt,
        "audit_file": str(audit_record["audit_file"]),
        "audit_folder": str(audit_record["audit_folder"]),
        "capture_id": str(audit_record["capture_id"]),
        "metric_excluded": True,
        "ml_sleeping": True,
        "advisory_only": True,
    }


def validate_manual_router_choice_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a normalized safe routing-choice payload."""
    data = dict(payload)
    lower_keys = {str(key).lower() for key in data.keys()}
    forbidden = sorted(key for key in FORBIDDEN_PAYLOAD_KEYS if key in lower_keys)
    if forbidden:
        raise ManualRouterChoiceCaptureError(
            "Routing-choice JSON contains forbidden authority/mutation fields: " + ", ".join(forbidden)
        )

    event_type = str(data.get("event_type", "")).strip()
    if event_type not in SUPPORTED_EVENT_TYPES:
        raise ManualRouterChoiceCaptureError("Unsupported routing-choice event_type: " + event_type)

    if data.get("advisory_only") is not True:
        raise ManualRouterChoiceCaptureError("Routing-choice JSON must contain advisory_only: true.")

    user_request = str(data.get("user_request", "")).strip()
    if not user_request:
        raise ManualRouterChoiceCaptureError("Routing-choice JSON must include user_request.")

    selected = data.get("selected_prompts")
    if not isinstance(selected, list) or not selected:
        raise ManualRouterChoiceCaptureError("Routing-choice JSON must include a non-empty selected_prompts list.")

    normalized_selected: list[dict[str, Any]] = []
    for index, choice in enumerate(selected, start=1):
        if not isinstance(choice, dict):
            raise ManualRouterChoiceCaptureError("selected_prompts item " + str(index) + " must be an object.")
        normalized_choice = normalize_selected_prompt_choice(choice, fallback_rank=index)
        normalized_selected.append(normalized_choice)

    data["selected_prompts"] = normalized_selected
    data["schema_version"] = str(data.get("schema_version", "1.0") or "1.0")
    data["source"] = str(data.get("source", "chatgpt_browser_with_startup_router_context"))
    data["metric_excluded"] = True
    data["manual_capture"] = True
    data["ml_sleeping"] = True
    return data


def normalize_selected_prompt_choice(choice: Mapping[str, Any], *, fallback_rank: int) -> dict[str, Any]:
    """Normalize one selected prompt choice without resolving files yet."""
    prompt_code = str(choice.get("prompt_code", "")).strip()
    prompt_id = str(choice.get("prompt_id", "")).strip()
    folder_path = str(choice.get("folder_path", choice.get("folder", ""))).strip().replace("\\", "/")
    prompt_path = str(choice.get("prompt_path", choice.get("path", choice.get("file_path", "")))).strip().replace("\\", "/")
    reason = str(choice.get("reason", "")).strip()

    if prompt_code and not PROMPT_CODE_RE.match(prompt_code):
        raise ManualRouterChoiceCaptureError("Invalid prompt_code format: " + prompt_code)
    if not prompt_code and not prompt_id and not prompt_path:
        raise ManualRouterChoiceCaptureError("Selected prompt must include prompt_code, prompt_id, or prompt_path.")
    for label, value in (("folder_path", folder_path), ("prompt_path", prompt_path)):
        if ".." in Path(value).parts or "../" in value or "..\\" in value:
            raise ManualRouterChoiceCaptureError(label + " must not contain directory traversal: " + value)
    try:
        rank = int(choice.get("rank", fallback_rank))
    except (TypeError, ValueError):
        rank = fallback_rank

    return {
        "prompt_code": prompt_code,
        "prompt_id": prompt_id,
        "folder_path": folder_path,
        "prompt_path": prompt_path,
        "rank": rank,
        "reason": reason,
        "is_primary": bool(choice.get("is_primary", rank == 1)),
    }


def resolve_selected_prompt(project_root: Path, choice: Mapping[str, Any]) -> dict[str, Any]:
    """Resolve one selected prompt choice to a safe project-local prompt file."""
    active_root = (project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS").resolve()
    if not active_root.exists():
        raise ManualRouterChoiceCaptureError("ACTIVE_PROMPTS folder not found: " + str(active_root))

    prompt_code = str(choice.get("prompt_code", "")).strip()
    metadata_match: dict[str, Any] | None = None
    if prompt_code:
        metadata_match = find_prompt_metadata_by_code(project_root, prompt_code)

    prompt_path = str(choice.get("prompt_path", "")).strip()
    prompt_id = str(choice.get("prompt_id", "")).strip()
    folder_path = str(choice.get("folder_path", "")).strip()

    if metadata_match:
        prompt_id = prompt_id or str(metadata_match.get("prompt_id", "")).strip()
        prompt_path = prompt_path or str(
            metadata_match.get("path")
            or metadata_match.get("prompt_path")
            or metadata_match.get("canonical_path")
            or ""
        ).strip()
        folder_path = folder_path or str(metadata_match.get("folder") or metadata_match.get("folder_path") or "").strip()

    candidates = candidate_prompt_paths(project_root, prompt_path=prompt_path, folder_path=folder_path, prompt_id=prompt_id)
    resolved_path: Path | None = None
    for candidate in candidates:
        safe = resolve_safe_active_prompt_path(project_root, candidate)
        if safe is not None:
            resolved_path = safe
            break

    if resolved_path is None:
        raise ManualRouterChoiceCaptureError(
            "Could not resolve selected prompt to an ACTIVE_PROMPTS file. "
            + "prompt_code=" + prompt_code + ", prompt_id=" + prompt_id + ", prompt_path=" + prompt_path
        )

    prompt_text = read_prompt_text(resolved_path)
    relative_path = resolved_path.relative_to(project_root).as_posix()
    prompt_library_relative = resolved_path.relative_to(project_root / "kanda_prompt_workspace" / "prompt_library").as_posix()
    return {
        "prompt_code": prompt_code,
        "prompt_id": prompt_id or resolved_path.stem,
        "prompt_path": relative_path,
        "prompt_library_path": prompt_library_relative,
        "folder_path": folder_path,
        "rank": int(choice.get("rank", 0) or 0),
        "reason": str(choice.get("reason", "")),
        "is_primary": bool(choice.get("is_primary", False)),
        "prompt_hash": sha256_text(prompt_text),
        "prompt_text": prompt_text,
        "prompt_byte_count": len(prompt_text.encode("utf-8", errors="replace")),
    }


def find_prompt_metadata_by_code(project_root: Path, prompt_code: str) -> dict[str, Any] | None:
    """Find a prompt metadata JSON object with the given stable prompt_code."""
    metadata_root = project_root / "kanda_prompt_workspace" / "prompt_library" / "METADATA"
    if not metadata_root.exists():
        return None
    for path in sorted(metadata_root.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        if isinstance(data, dict) and str(data.get("prompt_code", "")).strip() == prompt_code:
            return dict(data)
    return None


def candidate_prompt_paths(
    project_root: Path,
    *,
    prompt_path: str,
    folder_path: str,
    prompt_id: str,
) -> list[Path]:
    """Build candidate paths for a selected prompt."""
    candidates: list[Path] = []
    for raw in (prompt_path,):
        if raw:
            candidates.append(Path(raw))

    if folder_path and prompt_id:
        folder = Path(folder_path)
        candidates.append(folder / (prompt_id + ".md"))
        normalized_id = prompt_id.strip().lower().replace(" ", "_").replace("-", "_")
        if normalized_id and normalized_id != prompt_id:
            candidates.append(folder / (normalized_id + ".md"))

    # Also allow paths already relative to prompt_library.
    library_root = project_root / "kanda_prompt_workspace" / "prompt_library"
    expanded: list[Path] = []
    for candidate in candidates:
        expanded.append(candidate)
        candidate_text = candidate.as_posix()
        if candidate_text.startswith("ACTIVE_PROMPTS/"):
            expanded.append(library_root / candidate_text)
    return expanded


def resolve_safe_active_prompt_path(project_root: Path, candidate: Path) -> Path | None:
    """Resolve a candidate path only if it is an existing ACTIVE_PROMPTS file."""
    try:
        root = project_root.resolve()
        library_root = (root / "kanda_prompt_workspace" / "prompt_library").resolve()
        active_root = (library_root / "ACTIVE_PROMPTS").resolve()
        raw = Path(candidate)
        if raw.is_absolute():
            resolved = raw.expanduser().resolve()
        else:
            if raw.as_posix().startswith("ACTIVE_PROMPTS/"):
                resolved = (library_root / raw).resolve()
            elif raw.as_posix().startswith("kanda_prompt_workspace/"):
                resolved = (root / raw).resolve()
            else:
                resolved = (root / raw).resolve()
        resolved.relative_to(active_root)
    except Exception:
        return None

    if any(part.lower() in BLOCKED_PART_NAMES for part in resolved.parts):
        return None
    if not resolved.is_file() or resolved.suffix.lower() != ".md":
        return None
    return resolved


def read_prompt_text(path: Path) -> str:
    """Read a UTF-8 prompt text file."""
    return path.read_text(encoding="utf-8-sig", errors="replace")


def assemble_final_prompt(payload: Mapping[str, Any], resolved_prompts: list[Mapping[str, Any]]) -> str:
    """Assemble an editable browser prompt from selected local prompt text."""
    user_request = str(payload.get("user_request", "")).strip()
    classification = str(payload.get("router_classification", payload.get("task_classification", ""))).strip()
    source = str(payload.get("source", "chatgpt_browser_with_startup_router_context"))
    lines: list[str] = [
        "# KANDA ROUTED PROMPT",
        "",
        "Source: Manual Router Choice Capture v1",
        "External selection source: " + source,
        "Advisory-only import: true",
        "ML status: sleeping / not in critical path",
        "Metric status: excluded from ML readiness and heuristic correctness metrics",
        "",
        "## Original user request",
        user_request or "[missing user_request]",
    ]
    if classification:
        lines.extend(["", "## Router classification", classification])

    lines.extend(["", "## Selected prompt addresses"])
    for prompt in sorted(resolved_prompts, key=lambda item: int(item.get("rank", 0) or 0)):
        lines.append(
            "- rank "
            + str(prompt.get("rank", ""))
            + ": "
            + str(prompt.get("prompt_code") or "[no prompt_code]")
            + " | "
            + str(prompt.get("prompt_id", ""))
            + " | "
            + str(prompt.get("prompt_library_path", ""))
        )
        reason = str(prompt.get("reason", "")).strip()
        if reason:
            lines.append("  Reason: " + reason)

    for prompt in sorted(resolved_prompts, key=lambda item: int(item.get("rank", 0) or 0)):
        lines.extend(
            [
                "",
                "---",
                "",
                "## Prompt " + str(prompt.get("rank", "")) + ": " + str(prompt.get("prompt_id", "")),
                "Prompt code: " + str(prompt.get("prompt_code") or "[not provided]"),
                "Prompt path: " + str(prompt.get("prompt_library_path", "")),
                "Prompt hash: " + str(prompt.get("prompt_hash", "")),
                "",
                str(prompt.get("prompt_text", "")),
            ]
        )

    lines.extend(["", "---", "", "## Task to answer now", user_request or "[missing user_request]"])
    return "\n".join(lines).strip() + "\n"


def write_manual_router_choice_capture(
    project_root: Path,
    *,
    raw_paste_text: str,
    payload: Mapping[str, Any],
    resolved_prompts: list[Mapping[str, Any]],
    assembled_prompt: str,
) -> dict[str, Any]:
    """Write one advisory manual capture artifact under prompt_router_reasoner_reviews."""
    review_dir = project_root / REVIEW_FOLDER_NAME
    capture_dir = review_dir / MANUAL_CAPTURE_FOLDER_NAME
    capture_dir.mkdir(parents=True, exist_ok=True)
    capture_id = "mrc_" + utc_now_iso().replace(":", "").replace("-", "").replace("Z", "") + "_" + uuid4().hex[:8]
    audit_file = capture_dir / (capture_id + ".json")
    record = {
        "schema_version": "1.0",
        "event_type": "manual_router_choice_capture",
        "capture_id": capture_id,
        "created_at": utc_now_iso(),
        "origin": "chatgpt_browser_with_startup_router_context",
        "advisory_only": True,
        "metric_excluded": True,
        "ml_sleeping": True,
        "review_status": "pending_manual_round_trip_review",
        "raw_paste_hash": sha256_text(raw_paste_text),
        "payload": dict(payload),
        "resolved_prompts": [
            {
                key: value
                for key, value in dict(prompt).items()
                if key not in {"prompt_text"}
            }
            for prompt in resolved_prompts
        ],
        "assembled_prompt_hash": sha256_text(assembled_prompt),
        "assembled_prompt_preview": assembled_prompt[:4000],
    }
    audit_file.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "capture_id": capture_id,
        "audit_file": audit_file,
        "audit_folder": capture_dir,
    }


def build_example_routing_choice_block() -> str:
    """Return an example browser-ChatGPT routing choice block."""
    payload = {
        "schema_version": "1.0",
        "event_type": "chatgpt_router_prompt_choice",
        "source": "chatgpt_browser_with_startup_router_context",
        "user_request": "gimme an example of box code",
        "router_classification": "box architecture / box logic code demo",
        "selected_prompts": [
            {
                "prompt_code": "KPR-04-001",
                "prompt_id": "box_architecture_and_boundaries",
                "folder_path": "ACTIVE_PROMPTS/04_box_architecture_and_boundaries",
                "rank": 1,
                "reason": "The request is primarily about box logic.",
                "is_primary": True,
            }
        ],
        "advisory_only": True,
    }
    return (
        CHOICE_START_MARKER
        + "\n"
        + json.dumps(payload, indent=2, ensure_ascii=False)
        + "\n"
        + CHOICE_END_MARKER
    )
