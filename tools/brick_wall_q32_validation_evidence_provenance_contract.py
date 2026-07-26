# project-path: tools/brick_wall_q32_validation_evidence_provenance_contract.py
"""Validation-only Q32 validation and evidence provenance contract."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

__all__: list[str] = []

REQUIRED_FIELDS = (
    "provenance_required",
    "no_provenance_evidence",
    "q31_decision_complete",
    "q31_frozen_baseline",
    "primary_box",
    "feature_id",
    "operation_id",
    "project_slug",
    "tool_source_root",
    "active_project_root",
    "project_support_root",
    "evidence_owner",
    "source_snapshot_id",
    "source_fingerprints",
    "error_memory_export",
    "prompt_revisions",
    "validator_revisions",
    "validation_runs",
    "environment",
    "durable_evidence",
    "limitations",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q33",
    "may_begin_coding",
    "may_write_source",
)

SOURCE_FIELDS = ("path", "role", "sha256")
PROMPT_FIELDS = (
    "path",
    "prompt_id",
    "prompt_code",
    "version",
    "source_stage",
    "sha256",
)
VALIDATOR_FIELDS = ("path", "revision_basis", "sha256")
RUN_FIELDS = (
    "run_id",
    "validator_path",
    "command",
    "expected_markers",
    "observed_markers",
    "environment_fingerprint",
    "exit_code",
    "status",
)
ENVIRONMENT_FIELDS = (
    "os_name",
    "platform",
    "python_version",
    "python_executable",
    "dependency_state",
    "timezone",
)
EVIDENCE_FIELDS = (
    "relative_path",
    "owner_root",
    "feature_id",
    "sha256",
    "encoding",
    "generated_at_utc",
    "status_markers",
    "transient_copy_authoritative",
)


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _valid_sha256(value: Any) -> bool:
    text = str(value)
    return len(text) == 64 and all(char in "0123456789abcdef" for char in text)


def _unique_paths(rows: list[Mapping[str, Any]], label: str) -> set[str]:
    paths = [str(row.get("path", "")) for row in rows]
    _assert(all(paths), f"Q32 {label} path is required")
    _assert(len(paths) == len(set(paths)), f"Q32 duplicate {label} path")
    return set(paths)


def _source_row(path: str, role: str, fill: str) -> dict[str, str]:
    return {"path": path, "role": role, "sha256": fill}


def valid_complete_record() -> dict[str, Any]:
    fill_a = "a" * 64
    fill_b = "b" * 64
    brick = (
        "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
        "03_governance_freeze_and_handoff/"
        "brick_wall_comprehensive_quality_gate.md"
    )
    validator = "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py"
    source_fingerprints = [
        _source_row(brick, "canonical_prompt", fill_a),
        _source_row(validator, "focused_validator", fill_b),
    ]
    return {
        "provenance_required": True,
        "no_provenance_evidence": [],
        "q31_decision_complete": True,
        "q31_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "feature_id": "brick-wall-q32-validation-evidence-provenance-enforcement-v1",
        "operation_id": "q32-validation-evidence-provenance-v1",
        "project_slug": "kanda_reasoner",
        "tool_source_root": "E:/kanda_reasoner",
        "active_project_root": "E:/kanda_reasoner",
        "project_support_root": "E:/kanda_reasoner_show_project_to_AI",
        "evidence_owner": "PROJECT_SUPPORT",
        "source_snapshot_id": "sha256-manifest-q32-v1",
        "source_fingerprints": source_fingerprints,
        "error_memory_export": {
            "artifact_type": "error_memory_manifest",
            "schema_version": "1.0",
            "exporter_version": "1.2",
            "fingerprint": fill_a,
            "lesson_ids": [
                "lesson-validation-evidence-explicit-utf8-contract-v1",
                "lesson-validate-freeze-evidence-path-contract-v1",
            ],
            "status": "CURRENT",
        },
        "prompt_revisions": [
            {
                "path": brick,
                "prompt_id": "brick_wall_comprehensive_quality_gate",
                "prompt_code": "KPR-03-001",
                "version": "3.14",
                "source_stage": "brick-wall-q32-validation-evidence-provenance-enforcement-v1",
                "sha256": fill_a,
            }
        ],
        "validator_revisions": [
            {
                "path": validator,
                "revision_basis": "SHA256",
                "sha256": fill_b,
            }
        ],
        "validation_runs": [
            {
                "run_id": "q32-focused",
                "validator_path": validator,
                "command": "python tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py --project-root E:/kanda_reasoner",
                "expected_markers": [
                    "Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS",
                    "VALIDATION OK: brick-wall-q32-validation-evidence-provenance-enforcement-v1",
                ],
                "observed_markers": [
                    "Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS",
                    "VALIDATION OK: brick-wall-q32-validation-evidence-provenance-enforcement-v1",
                ],
                "environment_fingerprint": fill_a,
                "exit_code": 0,
                "status": "PASSED",
            }
        ],
        "environment": {
            "os_name": "Windows",
            "platform": "win32",
            "python_version": "3.10+",
            "python_executable": "python",
            "dependency_state": ["PySide6 available for local Qt validation"],
            "timezone": "America/Sao_Paulo",
        },
        "durable_evidence": {
            "relative_path": (
                "project_validation_evidence/"
                "brick-wall-q32-validation-evidence-provenance-enforcement-v1.txt"
            ),
            "owner_root": "E:/kanda_reasoner_show_project_to_AI",
            "feature_id": "brick-wall-q32-validation-evidence-provenance-enforcement-v1",
            "sha256": fill_b,
            "encoding": "UTF-8-NO-BOM",
            "generated_at_utc": "2026-07-16T16:00:00Z",
            "status_markers": [
                "VALIDATION OK: brick-wall-q32-validation-evidence-provenance-enforcement-v1",
                "STATUS: IN_SYNC",
            ],
            "transient_copy_authoritative": False,
        },
        "limitations": [
            "Sandbox and user-local environments must be distinguished explicitly."
        ],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q33": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update(
        provenance_required=False,
        no_provenance_evidence=[
            "The audited activity performs no validation and creates no evidence artifact."
        ],
        source_fingerprints=[],
        prompt_revisions=[],
        validator_revisions=[],
        validation_runs=[],
        limitations=["No validation or evidence operation exists for this task."],
        durable_evidence={},
        decision="NOT_APPLICABLE",
    )
    return record


def _validate_source_rows(rows: Any) -> set[str]:
    _assert(isinstance(rows, list), "Q32 source_fingerprints must be a list")
    _assert(bool(rows), "Q32 COMPLETE requires source fingerprints")
    paths = _unique_paths(rows, "source")
    for row in rows:
        _assert(all(field in row for field in SOURCE_FIELDS), "Q32 source row incomplete")
        _assert(bool(str(row["role"]).strip()), "Q32 source role is required")
        _assert(_valid_sha256(row["sha256"]), "Q32 source SHA-256 invalid")
    return paths


def _validate_prompt_rows(rows: Any, source_paths: set[str]) -> None:
    _assert(isinstance(rows, list) and rows, "Q32 prompt revisions are required")
    _unique_paths(rows, "prompt")
    for row in rows:
        _assert(all(field in row for field in PROMPT_FIELDS), "Q32 prompt row incomplete")
        _assert(row["path"] in source_paths, "Q32 prompt path lacks source fingerprint")
        _assert(all(str(row[field]).strip() for field in PROMPT_FIELDS[:-1]), "Q32 prompt identity incomplete")
        _assert(_valid_sha256(row["sha256"]), "Q32 prompt SHA-256 invalid")


def _validate_validator_rows(rows: Any, source_paths: set[str]) -> set[str]:
    _assert(isinstance(rows, list) and rows, "Q32 validator revisions are required")
    paths = _unique_paths(rows, "validator")
    for row in rows:
        _assert(all(field in row for field in VALIDATOR_FIELDS), "Q32 validator row incomplete")
        _assert(row["path"] in source_paths, "Q32 validator path lacks source fingerprint")
        _assert(row["revision_basis"] == "SHA256", "Q32 validator revision basis must be SHA256")
        _assert(_valid_sha256(row["sha256"]), "Q32 validator SHA-256 invalid")
    return paths


def _validate_runs(rows: Any, validator_paths: set[str]) -> None:
    _assert(isinstance(rows, list) and rows, "Q32 validation runs are required")
    run_ids: list[str] = []
    for row in rows:
        _assert(all(field in row for field in RUN_FIELDS), "Q32 validation run incomplete")
        run_ids.append(str(row["run_id"]))
        _assert(row["validator_path"] in validator_paths, "Q32 run validator is not inventoried")
        _assert(bool(str(row["command"]).strip()), "Q32 exact command is required")
        expected = row["expected_markers"]
        observed = row["observed_markers"]
        _assert(isinstance(expected, list) and expected, "Q32 expected markers are required")
        _assert(isinstance(observed, list) and observed, "Q32 observed markers are required")
        _assert(set(expected).issubset(observed), "Q32 expected marker was not observed")
        _assert(_valid_sha256(row["environment_fingerprint"]), "Q32 environment fingerprint invalid")
        _assert(row["exit_code"] == 0 and row["status"] == "PASSED", "Q32 run did not pass")
    _assert(len(run_ids) == len(set(run_ids)), "Q32 duplicate validation run ID")


def _validate_environment(value: Any) -> None:
    _assert(isinstance(value, Mapping), "Q32 environment must be an object")
    _assert(all(field in value for field in ENVIRONMENT_FIELDS), "Q32 environment incomplete")
    for field in ENVIRONMENT_FIELDS:
        _assert(bool(value[field]), f"Q32 environment field required: {field}")


def _validate_evidence(value: Any, record: Mapping[str, Any]) -> None:
    _assert(isinstance(value, Mapping), "Q32 durable evidence must be an object")
    _assert(all(field in value for field in EVIDENCE_FIELDS), "Q32 durable evidence incomplete")
    _assert(str(value["relative_path"]).startswith("project_validation_evidence/"), "Q32 evidence path owner invalid")
    _assert(value["owner_root"] == record["project_support_root"], "Q32 evidence owner root mismatch")
    _assert(value["feature_id"] == record["feature_id"], "Q32 evidence feature mismatch")
    _assert(_valid_sha256(value["sha256"]), "Q32 evidence SHA-256 invalid")
    _assert(value["encoding"] == "UTF-8-NO-BOM", "Q32 evidence encoding invalid")
    _assert(str(value["generated_at_utc"]).endswith("Z"), "Q32 evidence UTC time is required")
    _assert(bool(value["status_markers"]), "Q32 evidence status markers are required")
    _assert(value["transient_copy_authoritative"] is False, "Q32 transient evidence cannot be authoritative")



def q32_release_coverage_record(paths: list[str]) -> dict[str, Any]:
    """Build the Q31 coverage map for the exact Q32 changed-file set."""
    q31 = "tools/validate_brick_wall_q31_changed_file_validator_coverage_map_v1.py"
    q32 = "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py"
    inventory = [q31, q32]
    rows = []
    for path in paths:
        focused = [q31, q32]
        rows.append({
            "path": path,
            "owner_box": "tools validation-only support" if path.startswith("tools/") else "kanda_prompt_workspace/prompt_library",
            "public_contract": "Q32 governed validation/evidence provenance release",
            "error_memory_lessons": ["lesson-brick-wall-q02-validator-forward-contract-rigidity-v1"],
            "frozen_behavior": ["freeze-20260716-brick-wall-q31-changed-file-to-validator-coverage-map-enforcement-v1"],
            "focused_tests": {"disposition": "APPLIES", "validators": focused, "expected_markers": ["Q32_EXACT_RELEASE_PROVENANCE: PASS"], "reason": "The exact Q32 release and forward-compatible validator behavior are checked."},
            "boundary_tests": {"disposition": "NOT_APPLICABLE", "validators": [], "expected_markers": [], "reason": "No cross-box runtime communication is introduced."},
            "gui_tests": {"disposition": "NOT_APPLICABLE", "validators": [], "expected_markers": [], "reason": "No GUI or Qt behavior is changed."},
            "delivery_tests": {"disposition": "APPLIES", "validators": [q32], "expected_markers": ["Q32_EXACT_RELEASE_PROVENANCE: PASS"], "reason": "The final payload and durable evidence provenance are checked."},
            "negative_tests": {"disposition": "APPLIES", "validators": [q31, q32], "expected_markers": ["Q32_NEGATIVE_SOURCE_HASH_MISMATCH: PASS"], "reason": "Negative records reject missing, stale, or mismatched coverage and provenance."},
        })
    return {
        "coverage_required": True, "no_coverage_evidence": [],
        "q30_decision_complete": True, "q30_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": paths, "coverage_rows": rows,
        "validator_discovery_method": "EXPLICIT_INVENTORY",
        "broad_substring_exclusion": False,
        "required_validator_inventory": inventory,
        "uncovered_files": [], "orphan_required_validators": [],
        "conflicting_dispositions": [], "unresolved_fields": [],
        "decision": "COMPLETE", "may_proceed_to_q32": True,
        "may_begin_coding": False, "may_write_source": False,
    }

def validate_record(record: Mapping[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    _assert(not missing, "Q32 record missing fields: " + ", ".join(missing))
    _assert(record["decision"] in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}, "Invalid Q32 decision")
    _assert(record["may_begin_coding"] is False, "Q32 may not directly authorize coding")
    _assert(record["may_write_source"] is False, "Q32 may not directly authorize source writing")
    _assert(record["q31_decision_complete"] is True, "Q31 decision must be complete")
    _assert(record["q31_frozen_baseline"] is True, "Q31 frozen baseline is required")
    _assert(bool(record["primary_box"]), "Q32 primary box is required")
    _assert(bool(record["feature_id"]), "Q32 feature ID is required")
    _assert(bool(record["operation_id"]), "Q32 operation ID is required")
    _assert(bool(record["project_slug"]), "Q32 project slug is required")
    _assert(record["evidence_owner"] == "PROJECT_SUPPORT", "Q32 evidence owner must be PROJECT_SUPPORT")
    for field in ("tool_source_root", "active_project_root", "project_support_root"):
        _assert(bool(str(record[field]).strip()), f"Q32 root required: {field}")
    _assert(bool(record["source_snapshot_id"]), "Q32 source snapshot identity is required")
    _assert(not record["unresolved_fields"], "Q32 unresolved fields remain")
    _assert(bool(record["limitations"]), "Q32 limitations are required")

    if record["decision"] == "COMPLETE":
        _assert(record["provenance_required"] is True, "Q32 COMPLETE requires provenance")
        _assert(record["may_proceed_to_q33"] is True, "Q32 COMPLETE must permit Q33")
        source_paths = _validate_source_rows(record["source_fingerprints"])
        export = record["error_memory_export"]
        _assert(isinstance(export, Mapping), "Q32 Error Memory export must be an object")
        _assert(export.get("artifact_type") == "error_memory_manifest", "Q32 Error Memory artifact type invalid")
        _assert(bool(export.get("schema_version")), "Q32 Error Memory schema version is required")
        _assert(bool(export.get("exporter_version")), "Q32 Error Memory exporter version is required")
        _assert(_valid_sha256(export.get("fingerprint")), "Q32 Error Memory fingerprint invalid")
        _assert(bool(export.get("lesson_ids")), "Q32 relevant lesson IDs are required")
        _assert(export.get("status") == "CURRENT", "Q32 Error Memory export must be current")
        _validate_prompt_rows(record["prompt_revisions"], source_paths)
        validators = _validate_validator_rows(record["validator_revisions"], source_paths)
        _validate_runs(record["validation_runs"], validators)
        _validate_environment(record["environment"])
        _validate_evidence(record["durable_evidence"], record)
    elif record["decision"] == "NOT_APPLICABLE":
        _assert(record["provenance_required"] is False, "Q32 N/A must disable provenance")
        _assert(bool(record["no_provenance_evidence"]), "Q32 N/A requires evidence")
        _assert(not record["source_fingerprints"], "Q32 N/A must not list sources")
        _assert(not record["prompt_revisions"], "Q32 N/A must not list prompts")
        _assert(not record["validator_revisions"], "Q32 N/A must not list validators")
        _assert(not record["validation_runs"], "Q32 N/A must not list runs")
        _assert(not record["durable_evidence"], "Q32 N/A must not list durable evidence")
        _assert(record["may_proceed_to_q33"] is True, "Evidence-backed Q32 N/A may proceed")
    else:
        _assert(record["may_proceed_to_q33"] is False, "Blocked Q32 may not proceed")
