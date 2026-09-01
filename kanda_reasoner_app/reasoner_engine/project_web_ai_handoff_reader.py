# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_handoff_reader.py
"""Safely read and identify one active Project's AI handoff package."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from typing import Mapping

from kanda_reasoner_app.project_support_boundary import ProjectToolBoundaryIdentity
from kanda_reasoner_app.web_ai_provider_contracts import (
    HandoffCorruptError,
    HandoffMemberMissingError,
    HandoffMemberTooLargeError,
    HandoffMissingError,
    SupportIdentityMismatchError,
    SupportIdentityMissingError,
    UnsafeArchiveMemberError,
)

__all__ = [
    "ALLOWED_SUFFIXES",
    "OPTIONAL_SUFFIXES",
    "REQUIRED_SUFFIXES",
    "json_member",
    "load_selected_project_handoff_members",
]

MAX_MEMBER_BYTES = 8 * 1024 * 1024
MAX_TOTAL_READ_BYTES = 16 * 1024 * 1024

REQUIRED_SUFFIXES = (
    "__ai_briefing.json",
    "__routing_manifest.json",
    "__bundle_manifest.json",
    "__patch_safety_routes.json",
    "__validation_state.json",
)
OPTIONAL_SUFFIXES = (
    "__file_manifest.json",
    "__exclusion_rules.json",
    "__source_archive_manifest.json",
    "__error_lessons_compact.json",
    "__error_memory_ai_prompt.md",
    "__error_memory_manifest.json",
)
ALLOWED_SUFFIXES = REQUIRED_SUFFIXES + OPTIONAL_SUFFIXES + ("UPLOAD_README.txt",)
_IDENTITY_SUFFIXES = (
    "__ai_briefing.json",
    "__bundle_manifest.json",
)


def _handoff_archives(second_prompt_root: Path, project_slug: str) -> list[Path]:
    """Return only this active Project's upload ZIP parts."""
    archives = sorted(
        second_prompt_root.glob(project_slug + "__ai_handoff_upload*.zip"),
        key=lambda path: path.name.casefold(),
    )
    if archives:
        return archives
    fallback = sorted(
        second_prompt_root.glob(project_slug + "__ai_handoff_all_in_one*.zip"),
        key=lambda path: path.name.casefold(),
    )
    if fallback:
        return fallback
    raise HandoffMissingError(
        "No handoff ZIP for active Project '" + project_slug + "' was found."
    )


def _raw_member_name(info: zipfile.ZipInfo) -> str:
    """Return the raw member name preserved by ``ZipInfo``."""
    value = getattr(info, "orig_filename", None)
    if value is None:
        value = info.filename
    return str(value or "")


def _validate_member_name(raw_name: str) -> str:
    """Validate raw ZIP spelling and return one canonical POSIX name."""
    if not raw_name or "\x00" in raw_name:
        raise UnsafeArchiveMemberError("ZIP member name is empty or contains NUL.")
    if "\\" in raw_name:
        raise UnsafeArchiveMemberError(
            "ZIP member uses a Windows backslash: " + raw_name
        )
    if raw_name.startswith(("/", "//")) or re.match(r"^[A-Za-z]:", raw_name):
        raise UnsafeArchiveMemberError(
            "ZIP member is absolute or drive-qualified: " + raw_name
        )
    parts = PurePosixPath(raw_name.rstrip("/")).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise UnsafeArchiveMemberError(
            "ZIP member contains traversal or empty components: " + raw_name
        )
    return "/".join(parts)


def _archive_member_map(archive: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    """Validate every member and return canonical names to entries."""
    members: dict[str, zipfile.ZipInfo] = {}
    seen_casefold: set[str] = set()
    for info in archive.infolist():
        canonical = _validate_member_name(_raw_member_name(info))
        key = canonical.casefold()
        if key in seen_casefold:
            raise UnsafeArchiveMemberError(
                "Duplicate or case-colliding ZIP member: " + canonical
            )
        seen_casefold.add(key)
        members[canonical] = info
    return members


def _matching_suffix(canonical_name: str) -> str | None:
    """Return the allowlisted suffix for one canonical member name."""
    for suffix in ALLOWED_SUFFIXES:
        if canonical_name.endswith(suffix):
            return suffix
    return None


def _read_allowlisted_members(archives: list[Path]) -> dict[str, bytes]:
    """Read bounded allowlisted members across active-Project ZIP parts."""
    collected: dict[str, bytes] = {}
    total_bytes = 0
    for archive_path in archives:
        try:
            with zipfile.ZipFile(archive_path, "r") as archive:
                for canonical, info in _archive_member_map(archive).items():
                    suffix = _matching_suffix(canonical)
                    if suffix is None or info.is_dir():
                        continue
                    if suffix in collected:
                        raise UnsafeArchiveMemberError(
                            "Duplicate handoff artifact suffix: " + suffix
                        )
                    if info.flag_bits & 0x1:
                        raise UnsafeArchiveMemberError(
                            "Encrypted handoff members are not supported."
                        )
                    if info.file_size > MAX_MEMBER_BYTES:
                        raise HandoffMemberTooLargeError(
                            "Handoff member exceeds size limit: " + canonical
                        )
                    if info.compress_size and info.file_size / max(1, info.compress_size) > 250:
                        raise UnsafeArchiveMemberError(
                            "Suspicious ZIP compression ratio: " + canonical
                        )
                    data = archive.read(info)
                    total_bytes += len(data)
                    if total_bytes > MAX_TOTAL_READ_BYTES:
                        raise HandoffMemberTooLargeError(
                            "Selected Project handoff read budget exceeded."
                        )
                    collected[suffix] = data
        except zipfile.BadZipFile as exc:
            raise HandoffCorruptError(
                "AI handoff ZIP is corrupt: " + archive_path.name
            ) from exc
    return _require_members(collected)


def _load_loose_members(second_prompt_root: Path, project_slug: str) -> dict[str, bytes]:
    """Load only exact active-Project loose artifacts."""
    collected: dict[str, bytes] = {}
    for suffix in ALLOWED_SUFFIXES:
        if suffix == "UPLOAD_README.txt":
            pattern = project_slug + "__ai_handoff_upload_readme*.txt"
        else:
            pattern = project_slug + "*" + suffix
        candidates = list(second_prompt_root.glob(pattern))
        if not candidates:
            continue
        path = sorted(candidates, key=lambda item: item.name.casefold())[0]
        if path.stat().st_size > MAX_MEMBER_BYTES:
            raise HandoffMemberTooLargeError(
                "Loose handoff artifact exceeds size limit: " + path.name
            )
        collected[suffix] = path.read_bytes()
    if not collected:
        raise HandoffMissingError(
            "No exact handoff artifacts for active Project '"
            + project_slug
            + "' were found."
        )
    return _require_members(collected)


def _require_members(collected: dict[str, bytes]) -> dict[str, bytes]:
    """Require the complete compact handoff inventory."""
    missing = [suffix for suffix in REQUIRED_SUFFIXES if suffix not in collected]
    if missing:
        raise HandoffMemberMissingError(
            "Required active-Project handoff artifacts are missing: "
            + ", ".join(missing)
        )
    return collected


def json_member(members: Mapping[str, bytes], suffix: str) -> Mapping[str, object]:
    """Decode one JSON handoff artifact as an object."""
    try:
        payload = json.loads(members[suffix].decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HandoffCorruptError("Malformed handoff JSON: " + suffix) from exc
    if not isinstance(payload, dict):
        raise HandoffCorruptError("Handoff JSON must be an object: " + suffix)
    return payload


def _required_identity_value(
    project: Mapping[str, object],
    key: str,
    suffix: str,
) -> str:
    """Return one required handoff identity value."""
    value = str(project.get(key) or "").strip()
    if not value:
        raise SupportIdentityMissingError(
            "Handoff identity field '" + key + "' is missing from " + suffix
            + ". Run Show Project to AI again with the updated Tool."
        )
    return value


def _validate_handoff_identity(
    members: Mapping[str, bytes],
    identity: ProjectToolBoundaryIdentity,
) -> None:
    """Prove Project Support belongs to the selected active Project."""
    expected_slug = identity.active_project_slug
    for suffix in REQUIRED_SUFFIXES + OPTIONAL_SUFFIXES:
        if not suffix.endswith(".json") or suffix not in members:
            continue
        payload = json_member(members, suffix)
        project = payload.get("project")
        if isinstance(project, Mapping):
            actual_slug = str(project.get("project_slug") or "").strip()
            if actual_slug and actual_slug.casefold() != expected_slug.casefold():
                raise SupportIdentityMismatchError(
                    "Project Support handoff slug mismatch in " + suffix
                    + ": expected " + expected_slug + ", found " + actual_slug
                )
        if suffix in _IDENTITY_SUFFIXES:
            if not isinstance(project, Mapping):
                raise SupportIdentityMissingError(
                    "Handoff project identity is missing from " + suffix
                )
            project_id = _required_identity_value(project, "active_project_id", suffix)
            fingerprint = _required_identity_value(
                project,
                "active_project_root_fingerprint",
                suffix,
            )
            if project_id != identity.active_project_id:
                raise SupportIdentityMismatchError(
                    "Project Support belongs to a different physical Project. "
                    "Run Show Project to AI for the selected Project."
                )
            if fingerprint != identity.active_project_root_fingerprint:
                raise SupportIdentityMismatchError(
                    "Project Support is stale or belongs to a moved Project. "
                    "Run Show Project to AI again before cloud transmission."
                )
    if "__error_memory_manifest.json" in members:
        error_manifest = json_member(members, "__error_memory_manifest.json")
        error_slug = str(error_manifest.get("project_slug") or "").strip()
        if error_slug and error_slug.casefold() != expected_slug.casefold():
            raise SupportIdentityMismatchError(
                "Compact Error Memory belongs to a different Project: "
                + error_slug
            )


def load_selected_project_handoff_members(
    second_prompt_root: Path,
    identity: ProjectToolBoundaryIdentity,
) -> dict[str, bytes]:
    """Load and verify one active Project's compact handoff."""
    try:
        archives = _handoff_archives(second_prompt_root, identity.active_project_slug)
    except HandoffMissingError:
        members = _load_loose_members(
            second_prompt_root,
            identity.active_project_slug,
        )
    else:
        members = _read_allowlisted_members(archives)
    _validate_handoff_identity(members, identity)
    return members
