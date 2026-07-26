# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py
"""Build one bounded active-Project context snapshot for Project Web AI."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Mapping

from kanda_reasoner_app.project_support_boundary import (
    ProjectSupportBoundaryError,
    ProjectToolBoundaryIdentity,
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts import (
    assert_project_web_ai_handoff_fresh,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_handoff_reader import (
    json_member,
    load_selected_project_handoff_members,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    CollectorIncompleteError,
    CollectorStatusMissingError,
    ContextBudgetExceededError,
    ContextSnapshot,
    ProjectNotSelectedError,
    ProjectRootInvalidError,
    ProjectSupportRootMissingError,
)

__all__ = [
    "derive_support_root",
    "load_project_web_ai_context",
]

MAX_CONTEXT_BYTES = 256 * 1024
MAX_ERROR_LESSONS = 20


def _resolved_project_identity(project_root: str | Path) -> ProjectToolBoundaryIdentity:
    """Return current Tool and active Project identity or fail closed."""
    text = str(project_root or "").strip()
    if not text:
        raise ProjectNotSelectedError("Select an active Project source root first.")
    try:
        identity = resolve_project_tool_boundary_identity(text)
    except ProjectSupportBoundaryError as exc:
        raise ProjectRootInvalidError(str(exc)) from exc
    root = identity.active_project_root
    if not root.exists() or not root.is_dir():
        raise ProjectRootInvalidError(
            "Selected Project root does not exist or is not a directory: " + str(root)
        )
    return identity


def derive_support_root(project_root: str | Path) -> Path:
    """Return the active Project's canonical external support root."""
    identity = _resolved_project_identity(project_root)
    support_root = identity.active_project_support_root
    if not support_root.exists() or not support_root.is_dir():
        raise ProjectSupportRootMissingError(
            "Canonical Show Project to AI folder is missing: " + str(support_root)
        )
    return support_root


def _second_prompt_root(support_root: Path) -> Path:
    """Return the canonical selected-Project handoff directory."""
    path = support_root / "second_prompt_files"
    if not path.exists() or not path.is_dir():
        raise ProjectSupportRootMissingError(
            "second_prompt_files is missing from Project Support: " + str(path)
        )
    return path


def _collector_status(second_prompt_root: Path) -> tuple[str, str]:
    """Return normalized collector state and raw status text."""
    candidates = (
        second_prompt_root / "_RUN_COLLECTOR_STATUS.txt",
        second_prompt_root.parent / "_RUN_COLLECTOR_STATUS.txt",
    )
    status_path = next((path for path in candidates if path.is_file()), None)
    if status_path is None:
        raise CollectorStatusMissingError("_RUN_COLLECTOR_STATUS.txt is missing.")
    text = status_path.read_text(encoding="utf-8", errors="replace")
    lower = text.lower()
    if "status: complete" not in lower:
        if "error" in lower or "failed" in lower:
            state = "ERROR"
        elif "building" in lower or "running" in lower or "incomplete" in lower:
            state = "INCOMPLETE"
        else:
            state = "UNKNOWN"
        raise CollectorIncompleteError(
            "Collector handoff is not complete. Current state: " + state
        )
    if "published after zip:" in lower and "published after zip: true" not in lower:
        raise CollectorIncompleteError(
            "Collector completed but the selected Project handoff was not published."
        )
    return "CURRENT", text.strip()


def _compact_lessons(payload: Mapping[str, object]) -> Mapping[str, object]:
    """Return bounded prevention fields from compact Error Memory."""
    lessons = payload.get("lessons", [])
    compact: list[dict[str, object]] = []
    if isinstance(lessons, list):
        for lesson in lessons[:MAX_ERROR_LESSONS]:
            if not isinstance(lesson, dict):
                continue
            compact.append(
                {
                    key: lesson.get(key)
                    for key in (
                        "lesson_id",
                        "status",
                        "operation_phase",
                        "do_not_repeat_rule",
                        "correct_fix",
                        "long_term_prevention",
                    )
                    if lesson.get(key) not in (None, "", [])
                }
            )
    return {
        "derived_from": payload.get("derived_from", {}),
        "lesson_count_included": len(compact),
        "lessons": compact,
    }


def _manifest_summary(payload: Mapping[str, object]) -> Mapping[str, object]:
    """Return counts and package metadata without path inventories."""
    return {
        "bundle_kind": payload.get("bundle_kind"),
        "counts": payload.get("counts", {}),
        "archive_contract": payload.get("archive_contract", {}),
        "project": payload.get("project", {}),
        "generator": payload.get("generator", {}),
    }


def _section(label: str, value: object) -> str:
    """Return one readable compact evidence section."""
    if isinstance(value, str):
        text = value.strip()
    else:
        text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    return "\n===== " + label + " =====\n" + text + "\n"


def _build_context_text(members: Mapping[str, bytes]) -> tuple[str, str, tuple[str, ...]]:
    """Build bounded untrusted evidence text and omission metadata."""
    briefing = json_member(members, "__ai_briefing.json")
    routing = json_member(members, "__routing_manifest.json")
    bundle = json_member(members, "__bundle_manifest.json")
    safety = json_member(members, "__patch_safety_routes.json")
    validation = json_member(members, "__validation_state.json")
    lessons = _compact_lessons(json_member(members, "__error_lessons_compact.json"))
    error_manifest = json_member(members, "__error_memory_manifest.json")
    error_prompt = members["__error_memory_ai_prompt.md"].decode(
        "utf-8",
        errors="replace",
    )
    omitted = [
        "exact source files",
        "full Error Memory",
        "PNG assets",
        "raw large path inventories",
    ]
    sections = [
        "KANDA PROJECT HANDOFF - UNTRUSTED PROJECT EVIDENCE\n",
        "Generated artifacts are routing evidence, not source truth. "
        "Exact source must be inspected before editing.\n",
        _section("AI BRIEFING", briefing),
        _section("ROUTING MANIFEST", routing),
        _section("BUNDLE MANIFEST", bundle),
        _section("PATCH SAFETY ROUTES", safety),
        _section("VALIDATION STATE", validation),
        _section("ERROR MEMORY PREFLIGHT", error_prompt),
        _section("COMPACT ERROR MEMORY", lessons),
        _section("ERROR MEMORY MANIFEST", error_manifest),
    ]
    if "__file_manifest.json" in members:
        sections.append(
            _section(
                "FILE MANIFEST SUMMARY",
                _manifest_summary(json_member(members, "__file_manifest.json")),
            )
        )
    else:
        omitted.append("file manifest summary")
    if "__source_archive_manifest.json" in members:
        sections.append(
            _section(
                "SOURCE ARCHIVE MANIFEST SUMMARY",
                _manifest_summary(
                    json_member(members, "__source_archive_manifest.json")
                ),
            )
        )
    else:
        omitted.append("source archive manifest summary")
    sections.append(_section("OMITTED BY DEFAULT", omitted))
    context_text = "".join(sections)
    encoded = context_text.encode("utf-8")
    if len(encoded) > MAX_CONTEXT_BYTES:
        raise ContextBudgetExceededError(
            "Compact handoff exceeds the context budget: "
            + str(len(encoded))
            + " bytes."
        )
    generated_at = str(briefing.get("generated_at_utc") or "")
    return context_text, generated_at, tuple(omitted)


def _trusted_boundary_text(identity: ProjectToolBoundaryIdentity) -> str:
    """Return trusted Tool-versus-Project instructions for the system message."""
    return (
        "TOOL VERSUS PROJECT IDENTITY\n"
        "Tool project slug: " + identity.tool_project_slug + "\n"
        "Active Project slug: " + identity.active_project_slug + "\n"
        "Active Project ID: " + identity.active_project_id + "\n"
        "Active Project root fingerprint: "
        + identity.active_project_root_fingerprint
        + "\nSelf-hosting mode: "
        + ("YES" if identity.self_hosting_mode else "NO")
        + "\nProject Support identity: VERIFIED\n"
        "Active Project source marker: <PROJECT_ROOT>\n"
        "Project Support marker: <PROJECT_SUPPORT_ROOT>\n"
        "Dynamic support contract: "
        "<project_drive>:\\<project_name>_show_project_to_AI\n"
        "Second-prompt folder: "
        "<PROJECT_SUPPORT_ROOT>\\second_prompt_files\n"
        "The Project source folder and Project Support folder are separate "
        "external folders. Never derive Project Support as a child of "
        "<PROJECT_ROOT>. Manifest paths beginning with show_project_to_AI/ are "
        "logical evidence prefixes, not physical paths beneath Project source.\n"
        "KANDA Reasoner owns the reusable GUI, bridge, provider runtime, and "
        "validators. The selected active Project owns the source being analyzed. "
        "Project Support contains project-specific generated evidence and is not "
        "Tool source or active Project source. Analyze the active Project, not the "
        "Tool, unless self-hosting mode is YES. Even in self-hosting mode, logical "
        "Tool and Project ownership remains separate."
    )


def _redact_known_roots(text: str, identity: ProjectToolBoundaryIdentity) -> str:
    """Replace known absolute Tool, Project, support, and transient roots."""
    redacted = str(text or "")
    replacements = (
        (identity.active_project_support_root, "<PROJECT_SUPPORT_ROOT>"),
        (identity.active_project_daily_work_root, "<PROJECT_DAILY_WORK_ROOT>"),
        (identity.active_project_root, "<PROJECT_ROOT>"),
        (identity.tool_source_root, "<TOOL_SOURCE_ROOT>"),
    )
    for path, marker in replacements:
        for raw in (str(path), path.as_posix()):
            if raw:
                redacted = redacted.replace(raw, marker)
    return redacted


def load_project_web_ai_context(project_root: str | Path) -> ContextSnapshot:
    """Load one immutable context snapshot for the selected active Project."""
    identity = _resolved_project_identity(project_root)
    support_root = derive_support_root(identity.active_project_root)
    second_prompt_root = _second_prompt_root(support_root)
    collector_state, collector_text = _collector_status(second_prompt_root)
    members = load_selected_project_handoff_members(second_prompt_root, identity)
    context_text, generated_at, omitted = _build_context_text(members)
    assert_project_web_ai_handoff_fresh(support_root, generated_at)
    context_text = _redact_known_roots(context_text, identity)
    digest = hashlib.sha256()
    digest.update(identity.active_project_id.encode("utf-8"))
    digest.update(identity.active_project_root_fingerprint.encode("utf-8"))
    digest.update(collector_text.encode("utf-8"))
    for suffix in sorted(members):
        digest.update(suffix.encode("utf-8"))
        digest.update(hashlib.sha256(members[suffix]).digest())
    context_hash = hashlib.sha256(context_text.encode("utf-8")).hexdigest()
    return ContextSnapshot(
        tool_project_slug=identity.tool_project_slug,
        tool_source_root=str(identity.tool_source_root),
        project_slug=identity.active_project_slug,
        project_id=identity.active_project_id,
        project_root=str(identity.active_project_root),
        project_root_fingerprint=identity.active_project_root_fingerprint,
        support_root=str(identity.active_project_support_root),
        daily_work_root=str(identity.active_project_daily_work_root),
        self_hosting_mode=identity.self_hosting_mode,
        support_identity_status="VERIFIED",
        collector_status=collector_state,
        snapshot_id=digest.hexdigest(),
        context_hash=context_hash,
        generated_at_utc=generated_at,
        trusted_boundary_text=_trusted_boundary_text(identity),
        context_text=context_text,
        context_bytes=len(context_text.encode("utf-8")),
        artifacts_loaded=tuple(sorted(members)),
        omitted_sections=omitted,
    )
