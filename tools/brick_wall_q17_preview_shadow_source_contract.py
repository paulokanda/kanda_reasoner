"""Semantic record contract for Brick Wall Q17 authority separation."""

from __future__ import annotations

import re
from pathlib import PurePath, PurePosixPath, PureWindowsPath
from typing import Mapping, Sequence

__all__: list[str] = []

AUTHORITY_CLASSES = {
    "FINAL_SOURCE",
    "DURABLE_PREVIEW",
    "DISPOSABLE_SHADOW",
}
RECORD_FIELDS = (
    "identity_basis",
    "primary_box",
    "separation_required",
    "no_separation_evidence",
    "operation_id",
    "authorization_id",
    "active_project_root",
    "project_support_root",
    "transient_garbage_root",
    "artifacts",
    "pairwise_distinct_roots",
    "preview_not_source_truth",
    "shadow_not_durable_truth",
    "source_excludes_preview_metadata",
    "exact_byte_identity_verified",
    "cross_authority_writes_blocked",
    "unresolved_artifacts",
    "blockers",
    "tests",
    "decision",
    "may_proceed_to_q18",
    "may_continue_implementation",
    "may_write_source",
)
ARTIFACT_FIELDS = (
    "artifact_id",
    "authority_class",
    "canonical_root",
    "resolved_path",
    "logical_owner",
    "public_owner",
    "lifetime",
    "source_truth",
    "durable_truth",
    "source_mutation_authority",
    "metadata_policy",
    "exact_byte_hash_verified",
    "containment_verified",
    "cleanup_or_retention_rule",
    "tests",
    "blocked_cross_writes",
)
EXPECTED = {
    "FINAL_SOURCE": {
        "lifetime": "CANONICAL_PROJECT_SOURCE",
        "source_truth": True,
        "durable_truth": True,
        "source_mutation_authority": True,
        "metadata_policy": "NO_PREVIEW_ONLY_METADATA",
        "cleanup_or_retention_rule": "RETAIN_CANONICAL_SOURCE",
    },
    "DURABLE_PREVIEW": {
        "lifetime": "DURABLE_PROJECT_SUPPORT",
        "source_truth": False,
        "durable_truth": True,
        "source_mutation_authority": False,
        "metadata_policy": "PREVIEW_METADATA_ALLOWED_NOT_SOURCE_TRUTH",
        "cleanup_or_retention_rule": "RETAIN_UNTIL_GOVERNED_REPLACEMENT",
    },
    "DISPOSABLE_SHADOW": {
        "lifetime": "TRANSIENT_GARBAGE",
        "source_truth": False,
        "durable_truth": False,
        "source_mutation_authority": False,
        "metadata_policy": "TRANSIENT_ONLY_NO_DURABLE_AUTHORITY",
        "cleanup_or_retention_rule": "DELETE_AFTER_TERMINAL_VALIDATION",
    },
}


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
    if re.match(r"^[A-Za-z]:[\\/]", text) or text.startswith("\\"):
        return PureWindowsPath(text)
    return PurePosixPath(text)


def _inside(candidate: PurePath, owner: PurePath) -> bool:
    if type(candidate) is not type(owner):
        return False
    try:
        relative = candidate.relative_to(owner)
    except ValueError:
        return False
    return bool(relative.parts)


def _validate_artifact(
    artifact: Mapping[str, object],
    roots: Mapping[str, PurePath],
) -> tuple[str, PurePath]:
    _fields(artifact, ARTIFACT_FIELDS)
    for field in (
        "artifact_id",
        "authority_class",
        "canonical_root",
        "resolved_path",
        "logical_owner",
        "public_owner",
        "lifetime",
        "metadata_policy",
        "cleanup_or_retention_rule",
    ):
        if not _nonempty(artifact[field]):
            raise AssertionError(f"empty artifact field: {field}")
    authority = str(artifact["authority_class"])
    if authority not in AUTHORITY_CLASSES:
        raise AssertionError("unknown authority class")
    expected = EXPECTED[authority]
    for field, value in expected.items():
        if artifact[field] != value:
            raise AssertionError(f"invalid {authority} field: {field}")
    for field in (
        "source_truth",
        "durable_truth",
        "source_mutation_authority",
        "exact_byte_hash_verified",
        "containment_verified",
    ):
        if not isinstance(artifact[field], bool):
            raise AssertionError(f"artifact field must be boolean: {field}")
    if artifact["exact_byte_hash_verified"] is not True:
        raise AssertionError("artifact byte identity is unresolved")
    if artifact["containment_verified"] is not True:
        raise AssertionError("artifact containment is unresolved")
    if not _text_list(artifact["tests"]):
        raise AssertionError("artifact tests are missing")
    if _text_list(artifact["blocked_cross_writes"]):
        raise AssertionError("artifact has a cross-authority write")
    root = _pure_path(artifact["canonical_root"])
    resolved = _pure_path(artifact["resolved_path"])
    expected_root = roots[authority]
    if root != expected_root or not _inside(resolved, root):
        raise AssertionError("artifact path escaped its authority root")
    return authority, resolved


def validate_record(record: Mapping[str, object]) -> None:
    """Validate one complete Q17 separation record."""
    _fields(record, RECORD_FIELDS)
    if not _nonempty(record["identity_basis"]) or not _nonempty(record["primary_box"]):
        raise AssertionError("identity basis or primary box missing")
    if not isinstance(record["separation_required"], bool):
        raise AssertionError("separation_required must be boolean")
    if record["may_write_source"] is not False:
        raise AssertionError("Q17 cannot grant source-write authority")
    if _text_list(record["unresolved_artifacts"]):
        raise AssertionError("unresolved artifacts remain")
    if _text_list(record["blockers"]):
        raise AssertionError("separation blockers remain")
    if not _text_list(record["tests"]):
        raise AssertionError("separation tests are missing")
    if record["separation_required"] is False:
        if not _text_list(record["no_separation_evidence"]):
            raise AssertionError("not-applicable evidence missing")
        if record["artifacts"] not in ([], None):
            raise AssertionError("not-applicable record carries artifacts")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("not-applicable decision invalid")
        if record["may_proceed_to_q18"] is not True:
            raise AssertionError("not-applicable record cannot progress")
        if record["may_continue_implementation"] is not True:
            raise AssertionError("not-applicable record blocks implementation")
        return
    for field in (
        "operation_id",
        "authorization_id",
        "active_project_root",
        "project_support_root",
        "transient_garbage_root",
    ):
        if not _nonempty(record[field]):
            raise AssertionError(f"empty separation field: {field}")
    active = _pure_path(record["active_project_root"])
    support = _pure_path(record["project_support_root"])
    transient = _pure_path(record["transient_garbage_root"])
    if len({str(active).casefold(), str(support).casefold(), str(transient).casefold()}) != 3:
        raise AssertionError("authority roots are not distinct")
    if record["pairwise_distinct_roots"] is not True:
        raise AssertionError("pairwise-distinct root proof missing")
    for field in (
        "preview_not_source_truth",
        "shadow_not_durable_truth",
        "source_excludes_preview_metadata",
        "exact_byte_identity_verified",
        "cross_authority_writes_blocked",
    ):
        if record[field] is not True:
            raise AssertionError(f"separation gate failed: {field}")
    roots = {
        "FINAL_SOURCE": active,
        "DURABLE_PREVIEW": support,
        "DISPOSABLE_SHADOW": transient,
    }
    artifacts = record["artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) != 3:
        raise AssertionError("exactly three authority artifacts are required")
    seen: set[str] = set()
    resolved_paths: list[str] = []
    for artifact in artifacts:
        if not isinstance(artifact, Mapping):
            raise AssertionError("artifact is not a mapping")
        authority, resolved = _validate_artifact(artifact, roots)
        if authority in seen:
            raise AssertionError("duplicate authority class")
        seen.add(authority)
        resolved_paths.append(str(resolved).casefold())
    if seen != AUTHORITY_CLASSES:
        raise AssertionError("authority class set is incomplete")
    if len(resolved_paths) != len(set(resolved_paths)):
        raise AssertionError("authority artifacts share one resolved path")
    if record["decision"] != "COMPLETE":
        raise AssertionError("required separation decision is not COMPLETE")
    if record["may_proceed_to_q18"] is not True:
        raise AssertionError("Q18 progression missing")
    if record["may_continue_implementation"] is not True:
        raise AssertionError("implementation continuation missing")


def _artifact(
    authority: str,
    root: PureWindowsPath,
    relative: str,
) -> dict[str, object]:
    expected = EXPECTED[authority]
    return {
        "artifact_id": authority.lower(),
        "authority_class": authority,
        "canonical_root": str(root),
        "resolved_path": str(root / PurePosixPath(relative)),
        "logical_owner": "Active Project" if authority == "FINAL_SOURCE" else "Project workflow",
        "public_owner": "workbench_project_support_paths",
        "lifetime": expected["lifetime"],
        "source_truth": expected["source_truth"],
        "durable_truth": expected["durable_truth"],
        "source_mutation_authority": expected["source_mutation_authority"],
        "metadata_policy": expected["metadata_policy"],
        "exact_byte_hash_verified": True,
        "containment_verified": True,
        "cleanup_or_retention_rule": expected["cleanup_or_retention_rule"],
        "tests": ["authority and lifetime regression"],
        "blocked_cross_writes": [],
    }


def valid_required_record() -> dict[str, object]:
    """Return one valid required Q17 record."""
    active = PureWindowsPath(r"E:\kanda_reasoner")
    support = PureWindowsPath(r"E:\kanda_reasoner_show_project_to_AI")
    transient = PureWindowsPath(r"E:\kanda_reasoner_delete_after_daily_work")
    return {
        "identity_basis": "q17-preview-shadow-source-v1",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "separation_required": True,
        "no_separation_evidence": [],
        "operation_id": "brick-wall-q17-operation",
        "authorization_id": "brick-wall-q17-authorization",
        "active_project_root": str(active),
        "project_support_root": str(support),
        "transient_garbage_root": str(transient),
        "artifacts": [
            _artifact("FINAL_SOURCE", active, "pkg/module.py"),
            _artifact(
                "DURABLE_PREVIEW",
                support,
                "large_file_refactor_workbench/preview/q17/pkg/module.py",
            ),
            _artifact(
                "DISPOSABLE_SHADOW",
                transient,
                "large_file_refactor_shadow/q17/pkg/module.py",
            ),
        ],
        "pairwise_distinct_roots": True,
        "preview_not_source_truth": True,
        "shadow_not_durable_truth": True,
        "source_excludes_preview_metadata": True,
        "exact_byte_identity_verified": True,
        "cross_authority_writes_blocked": True,
        "unresolved_artifacts": [],
        "blockers": [],
        "tests": ["Q17 positive and negative authority matrix"],
        "decision": "COMPLETE",
        "may_proceed_to_q18": True,
        "may_continue_implementation": True,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    """Return one valid not-applicable Q17 record."""
    record = valid_required_record()
    record.update(
        separation_required=False,
        no_separation_evidence=["Task creates no source, Preview, or Shadow artifact"],
        operation_id="",
        authorization_id="",
        active_project_root="",
        project_support_root="",
        transient_garbage_root="",
        artifacts=[],
        decision="NOT_APPLICABLE",
    )
    return record
