"""Semantic contract for Brick Wall Q20 isolated filesystem fixtures."""

from __future__ import annotations

from copy import deepcopy
from typing import Mapping

__all__: list[str] = []

RECORD_FIELDS = {
    "identity_basis",
    "primary_box",
    "filesystem_fixture_required",
    "no_fixture_evidence",
    "shared_fixture_owner",
    "shared_fixture_facade",
    "protected_real_roots",
    "cases",
    "unresolved_cases",
    "blockers",
    "tests",
    "decision",
    "may_proceed_to_q21",
    "may_begin_coding",
    "may_write_source",
}

CASE_FIELDS = {
    "case_id",
    "validator_owner",
    "validator_path",
    "fixture_purpose",
    "fixture_root_class",
    "source_fixture_path",
    "support_fixture_path",
    "transient_fixture_path",
    "durable_evidence_fixture_path",
    "production_paths_read_only",
    "write_targets",
    "owner_overrides",
    "before_snapshots",
    "after_snapshots",
    "cleanup_policy",
    "cleanup_assertions",
    "copy_exclusions",
    "no_real_root_mutation",
    "no_drive_root_creation",
    "no_source_tree_fixture",
    "no_durable_evidence_in_transient",
    "cross_platform_formula_mode",
    "expected_markers",
}

ROOT_CLASSES = {
    "OS_TEMPORARY_DIRECTORY",
    "ACTIVE_PROJECT_TRANSIENT_GARBAGE",
}

CLEANUP_POLICIES = {
    "CONTEXT_MANAGER",
    "EXPLICIT_FINALLY",
}


def _fields(mapping: Mapping[str, object], required: set[str]) -> None:
    missing = required.difference(mapping)
    extra = set(mapping).difference(required)
    if missing or extra:
        raise AssertionError(
            "Q20 field mismatch missing="
            + repr(sorted(missing))
            + " extra="
            + repr(sorted(extra))
        )


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _fixture_relative(value: object) -> bool:
    return _nonempty(value) and str(value).startswith("<fixture_root>/")


def _validate_case(case: Mapping[str, object]) -> str:
    _fields(case, CASE_FIELDS)
    for field in (
        "case_id",
        "validator_owner",
        "validator_path",
        "fixture_purpose",
    ):
        if not _nonempty(case[field]):
            raise AssertionError("missing Q20 case field: " + field)
    if case["fixture_root_class"] not in ROOT_CLASSES:
        raise AssertionError("invalid Q20 fixture root class")
    fixture_paths = {
        str(case[field])
        for field in (
            "source_fixture_path",
            "support_fixture_path",
            "transient_fixture_path",
            "durable_evidence_fixture_path",
        )
        if _fixture_relative(case[field])
    }
    if len(fixture_paths) != 4:
        raise AssertionError("fixture paths must be distinct and fixture-relative")
    for field in (
        "production_paths_read_only",
        "write_targets",
        "before_snapshots",
        "after_snapshots",
        "cleanup_assertions",
        "expected_markers",
    ):
        if not _text_list(case[field]):
            raise AssertionError("missing Q20 case list: " + field)
    writes = _text_list(case["write_targets"])
    if any(not target.startswith("<fixture_root>/") for target in writes):
        raise AssertionError("Q20 write target escapes fixture root")
    read_only = set(_text_list(case["production_paths_read_only"]))
    if read_only.intersection(writes):
        raise AssertionError("production read-only path appears in write targets")
    if case["cleanup_policy"] not in CLEANUP_POLICIES:
        raise AssertionError("invalid Q20 cleanup policy")
    if case["cross_platform_formula_mode"] != "READ_ONLY_EXPECTATION":
        raise AssertionError("production path formula must remain read-only")
    for field in (
        "no_real_root_mutation",
        "no_drive_root_creation",
        "no_source_tree_fixture",
        "no_durable_evidence_in_transient",
    ):
        if case[field] is not True:
            raise AssertionError("Q20 isolation assertion missing: " + field)
    if "__pycache__" not in _text_list(case["copy_exclusions"]):
        raise AssertionError("fixture copy exclusions omit __pycache__")
    if ".git" not in _text_list(case["copy_exclusions"]):
        raise AssertionError("fixture copy exclusions omit .git")
    return str(case["case_id"])


def validate_record(record: Mapping[str, object]) -> None:
    """Validate one complete Q20 fixture decision record."""
    _fields(record, RECORD_FIELDS)
    for field in (
        "identity_basis",
        "primary_box",
        "shared_fixture_owner",
        "shared_fixture_facade",
    ):
        if not _nonempty(record[field]):
            raise AssertionError("missing Q20 record field: " + field)
    if not isinstance(record["filesystem_fixture_required"], bool):
        raise AssertionError("filesystem_fixture_required must be boolean")
    if record["may_begin_coding"] is not False:
        raise AssertionError("Q20 cannot authorize coding")
    if record["may_write_source"] is not False:
        raise AssertionError("Q20 cannot authorize source writes")
    if _text_list(record["unresolved_cases"]):
        raise AssertionError("unresolved Q20 cases remain")
    if _text_list(record["blockers"]):
        raise AssertionError("Q20 blockers remain")
    if not _text_list(record["tests"]):
        raise AssertionError("Q20 tests missing")
    if not _text_list(record["protected_real_roots"]):
        raise AssertionError("protected real roots missing")
    if record["filesystem_fixture_required"] is False:
        if not _text_list(record["no_fixture_evidence"]):
            raise AssertionError("not-applicable fixture evidence missing")
        if record["cases"] not in ([], None):
            raise AssertionError("not-applicable Q20 record carries cases")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("invalid Q20 not-applicable decision")
        if record["may_proceed_to_q21"] is not True:
            raise AssertionError("Q20 not-applicable record cannot progress")
        return
    cases = record["cases"]
    if not isinstance(cases, list) or not cases:
        raise AssertionError("required Q20 cases missing")
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, Mapping):
            raise AssertionError("Q20 case is not a mapping")
        case_id = _validate_case(case)
        if case_id in seen:
            raise AssertionError("duplicate Q20 case")
        seen.add(case_id)
    if record["decision"] != "COMPLETE":
        raise AssertionError("required Q20 decision is not COMPLETE")
    if record["may_proceed_to_q21"] is not True:
        raise AssertionError("Q21 progression missing")


def _base_case(case_id: str) -> dict[str, object]:
    return {
        "case_id": case_id,
        "validator_owner": "tools validation support",
        "validator_path": "tools/validator.py",
        "fixture_purpose": "bounded synthetic filesystem validation",
        "fixture_root_class": "OS_TEMPORARY_DIRECTORY",
        "source_fixture_path": "<fixture_root>/synthetic_source",
        "support_fixture_path": "<fixture_root>/synthetic_project_support",
        "transient_fixture_path": "<fixture_root>/synthetic_transient_garbage",
        "durable_evidence_fixture_path": "<fixture_root>/synthetic_durable_evidence",
        "production_paths_read_only": [
            "<active_project_root>",
            "<canonical_project_support_root>",
            "<canonical_transient_garbage_root>",
        ],
        "write_targets": [
            "<fixture_root>/synthetic_source",
            "<fixture_root>/synthetic_project_support",
            "<fixture_root>/synthetic_transient_garbage",
            "<fixture_root>/synthetic_durable_evidence",
        ],
        "owner_overrides": ["scoped support owner", "scoped transient owner"],
        "before_snapshots": ["protected probe paths"],
        "after_snapshots": ["protected probe paths unchanged"],
        "cleanup_policy": "CONTEXT_MANAGER",
        "cleanup_assertions": ["sandbox absent after context exit"],
        "copy_exclusions": [".git", "__pycache__", ".pytest_cache"],
        "no_real_root_mutation": True,
        "no_drive_root_creation": True,
        "no_source_tree_fixture": True,
        "no_durable_evidence_in_transient": True,
        "cross_platform_formula_mode": "READ_ONLY_EXPECTATION",
        "expected_markers": ["Q20_SHARED_ISOLATED_FILESYSTEM_FIXTURE: PASS"],
    }


def valid_required_record() -> dict[str, object]:
    """Return a complete required Q20 fixture record."""
    workbench = _base_case("workbench_support_and_daily_roots")
    workbench.update(
        validator_owner="architecture_review_workbench",
        validator_path=(
            "tools/validate_large_file_refactor_workbench_"
            "project_support_boundary_v3.py"
        ),
    )
    patch5 = _base_case("patch5_frozen_proof_support")
    patch5.update(
        validator_owner="architecture_review_patch5_proof",
        validator_path=(
            "tools/validate_workbench_patch5_executor_"
            "proof_status_projection_v1.py"
        ),
    )
    return {
        "identity_basis": "current Q19 freeze and exact validator inventory",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "filesystem_fixture_required": True,
        "no_fixture_evidence": [],
        "shared_fixture_owner": (
            "tools/brick_wall_q20_isolated_filesystem_fixture.py"
        ),
        "shared_fixture_facade": "isolated_filesystem_fixture",
        "protected_real_roots": [
            "active project source",
            "canonical project support",
            "canonical transient garbage",
            "Windows drive root",
        ],
        "cases": [workbench, patch5],
        "unresolved_cases": [],
        "blockers": [],
        "tests": [
            "required record matrix",
            "protected path snapshot",
            "cleanup verification",
        ],
        "decision": "COMPLETE",
        "may_proceed_to_q21": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    """Return an evidence-backed not-applicable Q20 record."""
    record = valid_required_record()
    record.update(
        filesystem_fixture_required=False,
        no_fixture_evidence=[
            "bounded prompt text task creates no synthetic filesystem state"
        ],
        cases=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    """Return an independent required record for negative tests."""
    return deepcopy(valid_required_record())
