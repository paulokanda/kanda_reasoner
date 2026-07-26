"""Semantic record contract for Brick Wall Q16 path containment."""

from __future__ import annotations

import re
from pathlib import PurePath, PurePosixPath, PureWindowsPath
from typing import Mapping, Sequence

__all__: list[str] = []

ALLOWED_PATH_TYPES = {
    "FILE",
    "DIRECTORY",
    "NEW_FILE",
    "NEW_DIRECTORY",
}
ALLOWED_LINK_STATUS = {
    "NO_LINK_COMPONENTS",
    "LINK_RESOLVED_INSIDE_OWNER",
    "NEW_PATH_PARENT_VERIFIED",
}
RECORD_FIELDS = (
    "identity_basis",
    "primary_box",
    "containment_required",
    "no_containment_evidence",
    "operation_id",
    "authorization_id",
    "owner_root",
    "owner_facade",
    "resolved_owner_root",
    "candidate_paths",
    "traversal_rejected",
    "sibling_prefix_rejected",
    "absolute_escape_rejected",
    "cross_drive_rejected",
    "unc_escape_rejected",
    "case_ambiguity_rejected",
    "link_escape_rejected",
    "unresolved_paths",
    "blockers",
    "tests",
    "decision",
    "may_proceed_to_final_precode",
    "may_begin_coding",
    "may_write_source",
)
CANDIDATE_FIELDS = (
    "path_id",
    "bounded_relative_input",
    "nearest_existing_parent",
    "resolved_owner_root",
    "resolved_candidate",
    "logical_owner",
    "path_type",
    "exists",
    "link_status",
    "drive_or_share_match",
    "case_key",
    "structural_relative_path",
    "containment_verified",
    "write_route",
    "tests",
    "blocked_escape",
)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _fields(record: Mapping[str, object], fields: Sequence[str]) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise AssertionError("missing fields: " + ", ".join(missing))


def _pure_path(value: object) -> PurePath:
    if not _nonempty(value):
        raise AssertionError("path value is empty")
    text = str(value).strip()
    if re.match(r"^[A-Za-z]:[\\/]", text) or text.startswith("\\\\"):
        return PureWindowsPath(text)
    return PurePosixPath(text)


def _relative_input(value: object) -> PurePosixPath:
    if not _nonempty(value):
        raise AssertionError("bounded relative input is empty")
    text = str(value).replace("\\", "/").strip()
    path = PurePosixPath(text)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise AssertionError("bounded relative input is unsafe")
    return path


def _structural_relative(candidate: PurePath, owner: PurePath) -> PurePath:
    if type(candidate) is not type(owner):
        raise AssertionError("candidate and owner path flavors differ")
    try:
        relative = candidate.relative_to(owner)
    except ValueError as exc:
        raise AssertionError("resolved candidate escaped owner") from exc
    if not relative.parts:
        raise AssertionError("owner root itself cannot be a candidate")
    return relative


def _case_key(path: PurePath) -> str:
    normalized = str(path).replace("\\", "/")
    if isinstance(path, PureWindowsPath):
        return normalized.casefold()
    return normalized


def _validate_candidate(candidate: Mapping[str, object]) -> tuple[str, str]:
    _fields(candidate, CANDIDATE_FIELDS)
    text_fields = (
        "path_id",
        "nearest_existing_parent",
        "resolved_owner_root",
        "resolved_candidate",
        "logical_owner",
        "path_type",
        "link_status",
        "case_key",
        "structural_relative_path",
        "write_route",
    )
    for field in text_fields:
        if not _nonempty(candidate[field]):
            raise AssertionError(f"empty candidate field: {field}")
    relative_input = _relative_input(candidate["bounded_relative_input"])
    owner = _pure_path(candidate["resolved_owner_root"])
    resolved = _pure_path(candidate["resolved_candidate"])
    parent = _pure_path(candidate["nearest_existing_parent"])
    if not owner.is_absolute() or not resolved.is_absolute() or not parent.is_absolute():
        raise AssertionError("resolved paths must be absolute")
    structural = _structural_relative(resolved, owner)
    _structural_relative(parent, owner)
    supplied = PurePosixPath(str(candidate["structural_relative_path"]).replace("\\", "/"))
    if supplied != PurePosixPath(*structural.parts):
        raise AssertionError("structural relative path is inconsistent")
    if relative_input != supplied:
        raise AssertionError("bounded input and structural result differ")
    if candidate["path_type"] not in ALLOWED_PATH_TYPES:
        raise AssertionError("invalid path type")
    if not isinstance(candidate["exists"], bool):
        raise AssertionError("exists must be boolean")
    if candidate["link_status"] not in ALLOWED_LINK_STATUS:
        raise AssertionError("link or reparse status is unsafe")
    if candidate["path_type"].startswith("NEW_"):
        if candidate["exists"] is not False:
            raise AssertionError("new path unexpectedly exists")
        if candidate["link_status"] != "NEW_PATH_PARENT_VERIFIED":
            raise AssertionError("new path parent is not verified")
    elif candidate["exists"] is not True:
        raise AssertionError("existing path is missing")
    if candidate["drive_or_share_match"] is not True:
        raise AssertionError("drive or UNC share mismatch")
    if candidate["containment_verified"] is not True:
        raise AssertionError("candidate containment is unresolved")
    if str(candidate["case_key"]) != _case_key(resolved):
        raise AssertionError("candidate case key is inconsistent")
    if _text_list(candidate["blocked_escape"]):
        raise AssertionError("candidate has a blocked escape")
    if not _text_list(candidate["tests"]):
        raise AssertionError("candidate tests are missing")
    return str(candidate["path_id"]), str(candidate["case_key"])


def validate_record(record: Mapping[str, object]) -> None:
    """Validate one complete Q16 containment record."""
    _fields(record, RECORD_FIELDS)
    if not _nonempty(record["identity_basis"]) or not _nonempty(record["primary_box"]):
        raise AssertionError("identity basis or primary box missing")
    if not isinstance(record["containment_required"], bool):
        raise AssertionError("containment_required must be boolean")
    if record["may_begin_coding"] is not False:
        raise AssertionError("Q16 cannot authorize coding")
    if record["may_write_source"] is not False:
        raise AssertionError("Q16 cannot authorize source writing")
    if _text_list(record["unresolved_paths"]):
        raise AssertionError("unresolved paths remain")
    if _text_list(record["blockers"]):
        raise AssertionError("containment blockers remain")
    if not _text_list(record["tests"]):
        raise AssertionError("containment tests are missing")
    if record["containment_required"] is False:
        if not _text_list(record["no_containment_evidence"]):
            raise AssertionError("not-applicable containment evidence missing")
        if record["candidate_paths"] not in ([], None):
            raise AssertionError("not-applicable record carries candidates")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("not-applicable decision invalid")
        if record["may_proceed_to_final_precode"] is not True:
            raise AssertionError("not-applicable record cannot progress")
        return
    for field in ("operation_id", "authorization_id", "owner_root", "owner_facade"):
        if not _nonempty(record[field]):
            raise AssertionError(f"empty containment field: {field}")
    owner = _pure_path(record["resolved_owner_root"])
    declared_owner = _pure_path(record["owner_root"])
    if owner != declared_owner or not owner.is_absolute():
        raise AssertionError("resolved owner root is inconsistent")
    for field in (
        "traversal_rejected",
        "sibling_prefix_rejected",
        "absolute_escape_rejected",
        "cross_drive_rejected",
        "unc_escape_rejected",
        "case_ambiguity_rejected",
        "link_escape_rejected",
    ):
        if record[field] is not True:
            raise AssertionError(f"negative containment gate failed: {field}")
    if record["decision"] != "COMPLETE":
        raise AssertionError("required containment decision is not COMPLETE")
    if record["may_proceed_to_final_precode"] is not True:
        raise AssertionError("final pre-code progression missing")
    candidates = record["candidate_paths"]
    if not isinstance(candidates, list) or not candidates:
        raise AssertionError("candidate path set missing")
    path_ids: list[str] = []
    case_keys: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            raise AssertionError("candidate path is not a mapping")
        path_id, case_key = _validate_candidate(candidate)
        path_ids.append(path_id)
        case_keys.append(case_key)
    if len(path_ids) != len(set(path_ids)):
        raise AssertionError("duplicate candidate path ID")
    if len(case_keys) != len(set(case_keys)):
        raise AssertionError("case-colliding candidate paths")


def _candidate(path_id: str, relative: str, path_type: str, exists: bool) -> dict[str, object]:
    owner = PureWindowsPath(r"E:\\kanda_reasoner")
    resolved = owner / PurePosixPath(relative)
    parent = resolved.parent
    return {
        "path_id": path_id,
        "bounded_relative_input": relative,
        "nearest_existing_parent": str(parent),
        "resolved_owner_root": str(owner),
        "resolved_candidate": str(resolved),
        "logical_owner": "Prompt library governance",
        "path_type": path_type,
        "exists": exists,
        "link_status": "NO_LINK_COMPONENTS" if exists else "NEW_PATH_PARENT_VERIFIED",
        "drive_or_share_match": True,
        "case_key": _case_key(resolved),
        "structural_relative_path": relative,
        "containment_verified": True,
        "write_route": "governed manifest installation",
        "tests": ["Q16 structural containment matrix"],
        "blocked_escape": [],
    }


def valid_required_record() -> dict[str, object]:
    """Return a complete required Q16 record for regression tests."""
    return {
        "identity_basis": "Current Q12-Q15 identity and exact source",
        "primary_box": "Prompt library governance",
        "containment_required": True,
        "no_containment_evidence": [],
        "operation_id": "brick-wall-q16-operation-v1",
        "authorization_id": "brick-wall-q16-authorization-v1",
        "owner_root": r"E:\\kanda_reasoner",
        "owner_facade": "current Q15 canonical path owner",
        "resolved_owner_root": r"E:\\kanda_reasoner",
        "candidate_paths": [
            _candidate(
                "brick_prompt",
                "kanda_prompt_workspace/prompt_library/brick.md",
                "FILE",
                True,
            ),
            _candidate(
                "q16_validator",
                "tools/validate_brick_wall_q16_resolved_path_containment_v1.py",
                "NEW_FILE",
                False,
            ),
        ],
        "traversal_rejected": True,
        "sibling_prefix_rejected": True,
        "absolute_escape_rejected": True,
        "cross_drive_rejected": True,
        "unc_escape_rejected": True,
        "case_ambiguity_rejected": True,
        "link_escape_rejected": True,
        "unresolved_paths": [],
        "blockers": [],
        "tests": ["Q16 positive and negative containment cases"],
        "decision": "COMPLETE",
        "may_proceed_to_final_precode": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    """Return an evidence-backed Q16 not-applicable record."""
    record = valid_required_record()
    record.update(
        containment_required=False,
        no_containment_evidence=["No filesystem path is read, created, or mutated"],
        operation_id="N/A",
        authorization_id="N/A",
        owner_root="N/A",
        owner_facade="N/A",
        resolved_owner_root="N/A",
        candidate_paths=[],
        decision="NOT_APPLICABLE",
    )
    return record
