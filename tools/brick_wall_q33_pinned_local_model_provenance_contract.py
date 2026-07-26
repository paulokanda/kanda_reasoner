# project-path: tools/brick_wall_q33_pinned_local_model_provenance_contract.py
"""Validation-only Q33 pinned local-model provenance contract."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

__all__: list[str] = []

SHA256_HEX_LENGTH = 64
REQUIRED_FIELDS = {
    "provenance_required",
    "no_model_evidence",
    "q32_decision_complete",
    "q32_frozen_baseline",
    "primary_box",
    "feature_id",
    "operation_id",
    "run_id",
    "provider",
    "runtime_owner",
    "model_id",
    "model_revision",
    "model_revision_basis",
    "tokenizer_id",
    "tokenizer_revision",
    "tokenizer_revision_basis",
    "code_revision",
    "code_hash",
    "prompt_hash",
    "prompt_serialization",
    "inference_settings",
    "offline_local_mode",
    "network_policy",
    "input_fingerprints",
    "output_hash",
    "output_normalization",
    "output_schema",
    "authority_classification",
    "advisory_only_reason",
    "durable_evidence_path",
    "validators",
    "expected_markers",
    "limitations",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q34",
    "may_begin_coding",
    "may_write_source",
}
SETTINGS_FIELDS = {
    "temperature",
    "seed",
    "top_p",
    "top_k",
    "context_window",
    "max_output_tokens",
    "stop",
    "options_hash",
}
TOKENIZER_BASES = {
    "EXACT_REVISION",
    "PROVIDER_BUNDLED_IN_MODEL_DIGEST",
}
REVISION_BASES = {
    "MODEL_BLOB_DIGEST",
    "IMMUTABLE_REVISION",
}


def _assert(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def _sha(value: str) -> bool:
    text = str(value)
    return len(text) == SHA256_HEX_LENGTH and all(
        char in "0123456789abcdef" for char in text.lower()
    )


def _hash_json(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def valid_complete_record() -> dict[str, Any]:
    digest = "a" * 64
    settings = {
        "temperature": 0.02,
        "seed": 0,
        "top_p": 1.0,
        "top_k": 40,
        "context_window": 32768,
        "max_output_tokens": 2600,
        "stop": [],
        "options_hash": "8a528473168a5ba6056bde9f3c2df8306e20d6360bb9d0cf11912f6c7ea83a96",
    }
    return {
        "provenance_required": True,
        "no_model_evidence": [],
        "q32_decision_complete": True,
        "q32_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "feature_id": "brick-wall-q33-pinned-local-model-provenance-enforcement-v1",
        "operation_id": "q33-provenance-gate-validation",
        "run_id": "local-ai-run-0001",
        "provider": "OLLAMA_LOCAL",
        "runtime_owner": "kanda_reasoner_app.reasoner_engine.local_ai_chat_service",
        "model_id": "example-model:tag",
        "model_revision": digest,
        "model_revision_basis": "MODEL_BLOB_DIGEST",
        "tokenizer_id": "PROVIDER_BUNDLED",
        "tokenizer_revision": digest,
        "tokenizer_revision_basis": "PROVIDER_BUNDLED_IN_MODEL_DIGEST",
        "code_revision": "SOURCE_SHA256_SET",
        "code_hash": digest,
        "prompt_hash": digest,
        "prompt_serialization": "CANONICAL_JSON_UTF8",
        "inference_settings": settings,
        "offline_local_mode": True,
        "network_policy": "LOOPBACK_ONLY_NO_EXTERNAL_PROVIDER",
        "input_fingerprints": [
            {"path": "input/project.json", "role": "MODEL_INPUT", "sha256": digest}
        ],
        "output_hash": digest,
        "output_normalization": "RAW_UTF8_BYTES",
        "output_schema": "STRICT_JSON_OBJECT_V1",
        "authority_classification": "ADVISORY_ONLY",
        "advisory_only_reason": (
            "Model output requires deterministic owner validation and never directly "
            "authorizes source, routing, validation, or freeze writes."
        ),
        "durable_evidence_path": (
            "project_validation_evidence/"
            "brick-wall-q33-pinned-local-model-provenance-enforcement-v1.txt"
        ),
        "validators": [
            "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py"
        ],
        "expected_markers": [
            "Q33_PINNED_LOCAL_MODEL_PROVENANCE_REGRESSION_SET: PASS",
            "Q33_EXACT_RELEASE_PROVENANCE: PASS",
        ],
        "limitations": [
            "A model digest cannot prove deterministic output on nondeterministic hardware.",
            "Deterministic validators remain the authority for acceptance."
        ],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q34": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, Any]:
    record = valid_complete_record()
    record.update({
        "provenance_required": False,
        "no_model_evidence": [
            "No local model, embedding model, or AI-assisted output was used as evidence."
        ],
        "provider": "",
        "runtime_owner": "",
        "model_id": "",
        "model_revision": "",
        "model_revision_basis": "",
        "tokenizer_id": "",
        "tokenizer_revision": "",
        "tokenizer_revision_basis": "",
        "code_revision": "",
        "code_hash": "",
        "prompt_hash": "",
        "prompt_serialization": "",
        "inference_settings": {},
        "offline_local_mode": False,
        "network_policy": "",
        "input_fingerprints": [],
        "output_hash": "",
        "output_normalization": "",
        "output_schema": "",
        "authority_classification": "",
        "advisory_only_reason": "",
        "durable_evidence_path": "",
        "validators": [],
        "expected_markers": [],
        "limitations": ["No model-assisted evidence exists for this task."],
        "decision": "NOT_APPLICABLE",
    })
    return record


def mutated_record(record: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(record))


def _validate_inputs(rows: Any) -> None:
    _assert(isinstance(rows, list) and rows, "Q33 input fingerprints are required")
    paths: list[str] = []
    for row in rows:
        _assert(isinstance(row, Mapping), "Q33 input row must be an object")
        _assert(all(field in row for field in ("path", "role", "sha256")), "Q33 input row incomplete")
        _assert(bool(str(row["path"]).strip()), "Q33 input path is required")
        _assert(bool(str(row["role"]).strip()), "Q33 input role is required")
        _assert(_sha(row["sha256"]), "Q33 input SHA-256 invalid")
        paths.append(str(row["path"]))
    _assert(len(paths) == len(set(paths)), "Q33 duplicate input path")


def _validate_settings(value: Any) -> None:
    _assert(isinstance(value, Mapping), "Q33 inference settings must be an object")
    _assert(SETTINGS_FIELDS.issubset(value), "Q33 inference settings incomplete")
    _assert(isinstance(value["temperature"], (int, float)), "Q33 temperature invalid")
    _assert(isinstance(value["seed"], int), "Q33 seed invalid")
    _assert(isinstance(value["top_p"], (int, float)), "Q33 top_p invalid")
    _assert(isinstance(value["top_k"], int), "Q33 top_k invalid")
    _assert(int(value["context_window"]) > 0, "Q33 context window invalid")
    _assert(int(value["max_output_tokens"]) > 0, "Q33 max output tokens invalid")
    _assert(isinstance(value["stop"], list), "Q33 stop settings invalid")
    _assert(_sha(value["options_hash"]), "Q33 options hash invalid")
    canonical = {key: value[key] for key in sorted(SETTINGS_FIELDS) if key != "options_hash"}
    _assert(
        value["options_hash"] == _hash_json(canonical),
        "Q33 inference options hash mismatch",
    )


def validate_record(record: Mapping[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS.difference(record))
    _assert(not missing, "Q33 record missing fields: " + ", ".join(missing))
    _assert(record["decision"] in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}, "Invalid Q33 decision")
    _assert(record["may_begin_coding"] is False, "Q33 may not authorize coding")
    _assert(record["may_write_source"] is False, "Q33 may not authorize source writing")
    _assert(record["q32_decision_complete"] is True, "Q32 decision must be complete")
    _assert(record["q32_frozen_baseline"] is True, "Q32 frozen baseline is required")
    _assert(bool(record["primary_box"]), "Q33 primary box is required")
    _assert(bool(record["feature_id"]), "Q33 feature ID is required")
    _assert(bool(record["operation_id"]), "Q33 operation ID is required")
    _assert(bool(record["run_id"]), "Q33 run ID is required")
    _assert(bool(record["limitations"]), "Q33 limitations are required")
    _assert(not record["unresolved_fields"], "Q33 unresolved fields remain")

    if record["decision"] == "COMPLETE":
        _assert(record["provenance_required"] is True, "Q33 COMPLETE requires provenance")
        _assert(record["may_proceed_to_q34"] is True, "Q33 COMPLETE must permit Q34")
        for field in (
            "provider", "runtime_owner", "model_id", "model_revision",
            "model_revision_basis", "tokenizer_id", "tokenizer_revision",
            "tokenizer_revision_basis", "code_revision", "code_hash",
            "prompt_hash", "prompt_serialization", "network_policy",
            "output_hash", "output_normalization", "output_schema",
            "authority_classification", "advisory_only_reason",
            "durable_evidence_path",
        ):
            _assert(bool(str(record[field]).strip()), f"Q33 field required: {field}")
        _assert(_sha(record["model_revision"]), "Q33 model revision must be exact SHA-256")
        _assert(record["model_revision_basis"] in REVISION_BASES, "Q33 model revision basis invalid")
        _assert(_sha(record["tokenizer_revision"]), "Q33 tokenizer revision invalid")
        _assert(record["tokenizer_revision_basis"] in TOKENIZER_BASES, "Q33 tokenizer basis invalid")
        _assert(_sha(record["code_hash"]), "Q33 code hash invalid")
        _assert(_sha(record["prompt_hash"]), "Q33 prompt hash invalid")
        _validate_settings(record["inference_settings"])
        _assert(record["offline_local_mode"] is True, "Q33 local/offline mode must be explicit")
        _assert(record["network_policy"] == "LOOPBACK_ONLY_NO_EXTERNAL_PROVIDER", "Q33 network policy invalid")
        _validate_inputs(record["input_fingerprints"])
        _assert(_sha(record["output_hash"]), "Q33 output hash invalid")
        _assert(record["authority_classification"] == "ADVISORY_ONLY", "Q33 model output must remain advisory")
        _assert(str(record["durable_evidence_path"]).startswith("project_validation_evidence/"), "Q33 durable evidence owner invalid")
        _assert(isinstance(record["validators"], list) and record["validators"], "Q33 validators required")
        _assert(isinstance(record["expected_markers"], list) and record["expected_markers"], "Q33 expected markers required")
    elif record["decision"] == "NOT_APPLICABLE":
        _assert(record["provenance_required"] is False, "Q33 N/A must disable provenance")
        _assert(bool(record["no_model_evidence"]), "Q33 N/A requires no-model evidence")
        _assert(record["may_proceed_to_q34"] is True, "Evidence-backed Q33 N/A may proceed")
        for field in (
            "provider", "runtime_owner", "model_id", "model_revision",
            "model_revision_basis", "tokenizer_id", "tokenizer_revision",
            "tokenizer_revision_basis", "code_revision", "code_hash",
            "prompt_hash", "prompt_serialization", "network_policy",
            "output_hash", "output_normalization", "output_schema",
            "authority_classification", "advisory_only_reason",
            "durable_evidence_path",
        ):
            _assert(not record[field], f"Q33 N/A must not set {field}")
        _assert(not record["inference_settings"], "Q33 N/A must not set inference settings")
        _assert(not record["input_fingerprints"], "Q33 N/A must not set inputs")
        _assert(not record["validators"], "Q33 N/A must not set validators")
    else:
        _assert(record["may_proceed_to_q34"] is False, "Blocked Q33 may not proceed")


def q33_release_coverage_record(paths: list[str]) -> dict[str, Any]:
    q32 = "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py"
    q33 = "tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py"
    lessons = [
        "lesson-aqr-correction-noop-retired-blocker-v1",
        "lesson-planner-local-ai-json-wrapper-parse-failure-v1",
        "lesson-workbench-local-ai-correction-deprecated-thread-polling-stall-v1",
        "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
    ]
    rows = []
    for path in paths:
        rows.append({
            "path": path,
            "owner_box": "tools validation-only support" if path.startswith("tools/") else "kanda_prompt_workspace/prompt_library",
            "public_contract": "Q33 governed pinned local-model provenance release",
            "error_memory_lessons": lessons,
            "frozen_behavior": ["freeze-20260716-brick-wall-q32-validation-and-evidence-provenance-enforcement-v1"],
            "focused_tests": {"disposition": "APPLIES", "validators": [q32, q33], "expected_markers": ["Q33_EXACT_RELEASE_PROVENANCE: PASS"], "reason": "Q32 forward compatibility and the Q33 contract are checked."},
            "boundary_tests": {"disposition": "APPLIES", "validators": [q33], "expected_markers": ["Q33_NO_RUNTIME_OWNER_MODIFIED: PASS"], "reason": "The release must not move model ownership into the prompt-library box."},
            "gui_tests": {"disposition": "NOT_APPLICABLE", "validators": [], "expected_markers": [], "reason": "No GUI or Qt behavior is changed."},
            "delivery_tests": {"disposition": "APPLIES", "validators": [q33], "expected_markers": ["Q33_EXACT_RELEASE_PROVENANCE: PASS"], "reason": "The final payload and evidence contract are checked."},
            "negative_tests": {"disposition": "APPLIES", "validators": [q33], "expected_markers": ["Q33_NEGATIVE_MODEL_REVISION: PASS"], "reason": "Unpinned or authoritative model evidence fails closed."},
        })
    return {
        "coverage_required": True,
        "no_coverage_evidence": [],
        "q30_decision_complete": True,
        "q30_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "changed_files": paths,
        "coverage_rows": rows,
        "validator_discovery_method": "EXPLICIT_INVENTORY",
        "broad_substring_exclusion": False,
        "required_validator_inventory": [q32, q33],
        "uncovered_files": [],
        "orphan_required_validators": [],
        "conflicting_dispositions": [],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q32": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }
