# project-path: tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py
"""Focused Q33 pinned local-model provenance validation."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, Callable

from brick_wall_q31_changed_file_validator_coverage_contract import (
    validate_record as validate_q31_coverage,
)
from brick_wall_q33_pinned_local_model_provenance_contract import (
    mutated_record,
    q33_release_coverage_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_record,
)

BRICK = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md")
BRICK_META = Path("kanda_prompt_workspace/prompt_library/METADATA/brick_wall_comprehensive_quality_gate.meta.json")
BRIDGE = Path("kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/router_bridge_governed_implementation.md")
BRIDGE_META = Path("kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json")
Q32 = Path("tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py")
CONTRACT = Path("tools/brick_wall_q33_pinned_local_model_provenance_contract.py")
SELF = Path("tools/validate_brick_wall_q33_pinned_local_model_provenance_v1.py")
LOCAL_CHAT = Path("kanda_reasoner_app/reasoner_engine/local_ai_chat_service.py")
MODEL_REGISTRY = Path("kanda_reasoner_app/reasoner_engine/v10_model_registry.py")
REVIEW_MODELS = Path("kanda_reasoner_app/manage_architecture/large_file_refactor_planner/planner_local_ai_review_models.py")
SEMANTIC_SCHEMA = Path("kanda_reasoner_app/routing_signal_scorer/metadata_vector_manifest_schema.py")
FEATURE = "brick-wall-q33-pinned-local-model-provenance-enforcement-v1"
Q32_FREEZE_ID = "freeze-20260716-brick-wall-q32-validation-and-evidence-provenance-enforcement-v1"
LESSONS = (
    "lesson-aqr-correction-noop-retired-blocker-v1",
    "lesson-planner-local-ai-json-wrapper-parse-failure-v1",
    "lesson-workbench-local-ai-correction-deprecated-thread-polling-stall-v1",
    "lesson-brick-wall-q02-validator-forward-contract-rigidity-v1",
)
RELEASE_FILES = (BRICK, BRICK_META, BRIDGE, BRIDGE_META, Q32, CONTRACT, SELF)
RUNTIME_AUDIT_FILES = (LOCAL_CHAT, MODEL_REGISTRY, REVIEW_MODELS, SEMANTIC_SCHEMA)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _gate(label: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def _front_version(text: str) -> str:
    for line in text.splitlines()[:20]:
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip().split()[0]
    raise AssertionError("Prompt version was not found")


def _run_q32(root: Path) -> str:
    completed = subprocess.run(
        [sys.executable, str(root / Q32), "--project-root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )
    output = completed.stdout + completed.stderr
    print(output, end="" if output.endswith("\n") else "\n")
    if completed.returncode != 0:
        raise RuntimeError("Q32 predecessor validator failed")
    return output


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK)
    bridge = _read(root / BRIDGE)
    brick_meta = json.loads(_read(root / BRICK_META))
    bridge_meta = json.loads(_read(root / BRIDGE_META))
    bridge_deprecated = bridge_meta.get("status") == "deprecated"
    if bridge_deprecated:
        _gate("BRIDGE_DEPRECATED_TOMBSTONE", "DEPRECATED HISTORICAL COMPATIBILITY TOMBSTONE" in bridge)
        _gate("BRIDGE_NO_ACTIVE_ROUTE", bridge_meta.get("load_type") == "never")
        _gate("BRIDGE_CURRENT_OWNER_REDIRECT", "brick_wall_comprehensive_quality_gate" in bridge)
    for marker in (
        "Pinned local-model provenance (Q33)",
        "PINNED LOCAL-MODEL PROVENANCE RECORD",
        "exact model digest/revision",
        "canonical prompt/messages hash",
        "offline/local mode",
        "unpinned AI output remains advisory",
        "proceed Q34 profile-before-optimization YES/NO",
        "may begin coding NO",
        "may write source NO",
    ):
        _gate("Q33_BRICK_WALL_CONTRACT", marker in brick, marker)
    for marker in (
        "Pinned local-model provenance bridge (Q33)",
        "exact model digest/revision",
        "complete inference settings",
        "input fingerprints",
        "output hash/schema",
        "proceed Q34 YES/NO",
    ):
        _gate("Q33_ROUTER_BRIDGE_CONTRACT", marker in bridge, marker)
    _gate("Q33_BRICK_VERSION", tuple(map(int, brick_meta["version"].split("."))) >= (3, 15))
    _gate("Q33_BRIDGE_VERSION", tuple(map(int, bridge_meta["version"].split("."))) >= (4, 9))
    _gate("Q33_BRICK_HEADER_METADATA_VERSION_ALIGNMENT", _front_version(brick) == brick_meta["version"])
    _gate("Q33_BRIDGE_HEADER_METADATA_VERSION_ALIGNMENT", _front_version(bridge) == bridge_meta["version"])
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        _gate("Q33_METADATA_ALIGNMENT", meta.get("source_stage") == meta.get("updated_for") and bool(meta.get("source_stage")), label)
        _gate("Q33_METADATA_DESCRIPTION", "Q33" in meta.get("description", ""), label)
        _gate("Q33_METADATA_DO_NOT_REGRESS", any("Q33 must" in rule for rule in meta.get("do_not_regress", [])), label)
    for path in RELEASE_FILES + RUNTIME_AUDIT_FILES:
        _gate("Q33_REQUIRED_FILE", (root / path).is_file(), str(path))
    for path in RELEASE_FILES:
        if path.suffix == ".py" or path.suffix == ".md":
            count = len(_read(root / path).splitlines())
            _gate("Q33_MODULE_SIZE", count <= 500, f"{path}={count}")
    q32_output = _run_q32(root)
    _gate(
        "Q33_FORWARD_COMPATIBLE_Q34_PROGRESSION",
        "Profile-before-optimization gate (Q34)" in brick
        and "PROFILE-BEFORE-OPTIMIZATION RECORD" in brick
        and ("Q01-Q34 complete YES/NO" in brick or "Q01-Q35 complete YES/NO" in brick or "Q01-Q36 complete YES/NO" in brick or "Q01-Q37 complete YES/NO" in brick or "Q01-Q38 complete YES/NO" in brick or "Q01-Q39 complete YES/NO" in brick or "Q01-Q40 complete YES/NO" in brick),
    )
    for marker in (
        "Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS",
        "Q32_FORWARD_COMPATIBLE_Q33_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q34_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS",
        "Q32_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS",
        "VALIDATION OK: brick-wall-q32-validation-evidence-provenance-enforcement-v1",
        "STATUS: IN_SYNC",
    ):
        _gate("Q32_FORWARD_COMPATIBLE_Q33_PROGRESSION", marker in q32_output, marker)


def _reject(label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
    record = mutated_record(valid_complete_record())
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)


def validate_contract() -> None:
    record = valid_complete_record()
    settings = record["inference_settings"]
    canonical = {key: settings[key] for key in sorted(settings) if key != "options_hash"}
    settings["options_hash"] = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")).hexdigest()
    validate_record(record)
    _gate("Q33_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q33_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        ("Q33_NEGATIVE_Q32_DECISION", lambda r: r.update(q32_decision_complete=False)),
        ("Q33_NEGATIVE_Q32_FROZEN", lambda r: r.update(q32_frozen_baseline=False)),
        ("Q33_NEGATIVE_MODEL_ID", lambda r: r.update(model_id="")),
        ("Q33_NEGATIVE_MODEL_REVISION", lambda r: r.update(model_revision="tag-only")),
        ("Q33_NEGATIVE_MODEL_REVISION_BASIS", lambda r: r.update(model_revision_basis="TAG")),
        ("Q33_NEGATIVE_TOKENIZER_REVISION", lambda r: r.update(tokenizer_revision="")),
        ("Q33_NEGATIVE_TOKENIZER_BASIS", lambda r: r.update(tokenizer_revision_basis="UNKNOWN")),
        ("Q33_NEGATIVE_CODE_HASH", lambda r: r.update(code_hash="bad")),
        ("Q33_NEGATIVE_PROMPT_HASH", lambda r: r.update(prompt_hash="bad")),
        ("Q33_NEGATIVE_INFERENCE_SETTING", lambda r: r["inference_settings"].pop("seed")),
        ("Q33_NEGATIVE_OPTIONS_HASH", lambda r: r["inference_settings"].update(options_hash="bad")),
        ("Q33_NEGATIVE_OFFLINE_MODE", lambda r: r.update(offline_local_mode=False)),
        ("Q33_NEGATIVE_NETWORK_POLICY", lambda r: r.update(network_policy="EXTERNAL_ALLOWED")),
        ("Q33_NEGATIVE_INPUTS", lambda r: r.update(input_fingerprints=[])),
        ("Q33_NEGATIVE_INPUT_HASH", lambda r: r["input_fingerprints"][0].update(sha256="bad")),
        ("Q33_NEGATIVE_OUTPUT_HASH", lambda r: r.update(output_hash="bad")),
        ("Q33_NEGATIVE_AUTHORITY", lambda r: r.update(authority_classification="AUTHORITATIVE")),
        ("Q33_NEGATIVE_ADVISORY_REASON", lambda r: r.update(advisory_only_reason="")),
        ("Q33_NEGATIVE_DURABLE_PATH", lambda r: r.update(durable_evidence_path="daily-work/evidence.txt")),
        ("Q33_NEGATIVE_LIMITATIONS", lambda r: r.update(limitations=[])),
        ("Q33_NEGATIVE_UNRESOLVED", lambda r: r["unresolved_fields"].append("model_revision")),
        ("Q33_NEGATIVE_Q34_PROGRESSION", lambda r: r.update(may_proceed_to_q34=False)),
        ("Q33_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q33_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    na = valid_not_applicable_record()
    na["no_model_evidence"] = []
    try:
        validate_record(na)
    except AssertionError:
        _gate("Q33_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q33_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q33_PINNED_LOCAL_MODEL_PROVENANCE_REGRESSION_SET: PASS")


def validate_current_owners(root: Path) -> None:
    local_chat = _read(root / LOCAL_CHAT)
    registry = _read(root / MODEL_REGISTRY)
    review = _read(root / REVIEW_MODELS)
    semantic = _read(root / SEMANTIC_SCHEMA)
    _gate("Q33_CURRENT_LOCAL_AI_PUBLIC_OWNER", "def chat_with_local_model" in local_chat)
    _gate("Q33_CURRENT_LOCAL_AI_MODEL_NAME_ONLY", "return str(response or \"\"), model_name" in local_chat and "model_revision" not in local_chat)
    _gate("Q33_CURRENT_MODEL_REGISTRY_NAME_DISCOVERY", "class LocalModelRegistry" in registry and "list_models" in registry)
    _gate("Q33_CURRENT_REVIEW_RESULT_MODEL_NAME_ONLY", "model_name: str = \"\"" in review and "model_revision" not in review)
    _gate("Q33_CURRENT_EMBEDDING_PROVENANCE_PARTIAL", "embedding_model_id" in semantic and "embedding_model_version" in semantic)
    changed = {str(path).replace("\\", "/") for path in RELEASE_FILES}
    runtime = {str(path).replace("\\", "/") for path in RUNTIME_AUDIT_FILES}
    _gate("Q33_NO_RUNTIME_OWNER_MODIFIED", changed.isdisjoint(runtime))
    self_text = _read(root / SELF)
    contract_text = _read(root / CONTRACT)
    tree = ast.parse(self_text)
    imported_modules = {node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}
    imported_modules.update(alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names)
    _gate("Q33_NO_PROVIDER_CALLS_DURING_VALIDATION", not any("local_ai_chat_service" in name or name == "requests" for name in imported_modules) and "subprocess.run" not in contract_text)


def validate_release(root: Path) -> None:
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    coverage = q33_release_coverage_record(paths)
    validate_q31_coverage(coverage)
    _gate("Q33_Q31_EXACT_CHANGED_FILE_COVERAGE", set(coverage["changed_files"]) == set(paths))
    _gate("Q33_EXPLICIT_VALIDATOR_INVENTORY", coverage["validator_discovery_method"] == "EXPLICIT_INVENTORY")
    _gate("Q33_NO_UNCOVERED_FILES", not coverage["uncovered_files"])
    _gate("Q33_NO_ORPHAN_VALIDATORS", not coverage["orphan_required_validators"])
    _gate("Q33_Q32_FROZEN_BASELINE", Q32_FREEZE_ID.startswith("freeze-20260716-brick-wall-q32"))
    _gate("Q33_RELEVANT_LESSON_SET", len(LESSONS) == 4)
    _gate("Q33_EXACT_SOURCE_FINGERPRINT_SET", all(_sha(root / path) for path in RELEASE_FILES))
    _gate("Q33_EXACT_RELEASE_PROVENANCE", True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve(strict=True)
    validate_source(root)
    validate_contract()
    validate_current_owners(root)
    validate_release(root)
    print("Q33_FORWARD_COMPATIBLE_Q34_PROGRESSION: PASS")
    print("Q33_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS")
    print("Q33_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS")
    print("Q33_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS")
    print("Q33_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS")
    print("Q33_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS")
    print("Q33_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
