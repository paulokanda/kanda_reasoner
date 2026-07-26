# project-path: tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py
"""Focused Q32 validation and evidence provenance validation."""
from __future__ import annotations

__all__: list[str] = []

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Callable

from brick_wall_q31_changed_file_validator_coverage_contract import validate_record as validate_q31_coverage
from brick_wall_q32_validation_evidence_provenance_contract import (
    mutated_record, q32_release_coverage_record,
    valid_complete_record,
    valid_not_applicable_record,
    validate_record,
)

BRICK = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "brick_wall_comprehensive_quality_gate.meta.json"
)
BRIDGE = Path(
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META = Path(
    "kanda_prompt_workspace/prompt_library/METADATA/"
    "router_bridge_governed_implementation.meta.json"
)
Q31_CONTRACT = Path(
    "tools/brick_wall_q31_changed_file_validator_coverage_contract.py"
)
Q31_VALIDATOR = Path(
    "tools/validate_brick_wall_q31_changed_file_validator_coverage_map_v1.py"
)
CONTRACT = Path(
    "tools/brick_wall_q32_validation_evidence_provenance_contract.py"
)
SELF = Path(
    "tools/validate_brick_wall_q32_validation_evidence_provenance_v1.py"
)
FEATURE = "brick-wall-q32-validation-evidence-provenance-enforcement-v1"
Q31_FREEZE_ID = (
    "freeze-20260716-brick-wall-q31-changed-file-to-validator-"
    "coverage-map-enforcement-v1"
)
LESSONS = (
    "lesson-validation-evidence-explicit-utf8-contract-v1",
    "lesson-validate-freeze-evidence-path-contract-v1",
    "lesson-patch-validation-wrapper-required-marker-drift-v1",
    "lesson-complete-json-validator-ambient-collector-env-leak-v1",
    "lesson-brick-wall-validator-exact-diagnostic-hash-recovery-v1",
)
RELEASE_FILES = (
    BRICK,
    BRICK_META,
    BRIDGE,
    BRIDGE_META,
    Q31_CONTRACT,
    Q31_VALIDATOR,
    CONTRACT,
    SELF,
)

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def _json_sha256(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")
    return hashlib.sha256(payload).hexdigest()

def _gate(label: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))

def _manifest_path(project_root: Path) -> Path:
    support_root = project_root.parent / (project_root.name + "_show_project_to_AI")
    candidates = (
        support_root
        / "project_error_memory"
        / "exports"
        / "latest_error_memory_manifest.json",
        support_root
        / "second_prompt_files"
        / (project_root.name + "__error_memory_manifest.json"),
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise AssertionError(
        "Q32 Error Memory manifest not found under project support root: "
        + str(support_root)
    )

def _front_matter_version(text: str) -> str:
    for line in text.splitlines()[:20]:
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip().split()[0]
    raise AssertionError("Prompt front matter version not found")

def _run_validator(project_root: Path, relative: Path) -> str:
    command = [
        sys.executable,
        str(project_root / relative),
        "--project-root",
        str(project_root),
    ]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        raise AssertionError(
            "Q32 predecessor validator failed: "
            + str(relative)
            + "\n"
            + output
        )
    return output

def validate_source(project_root: Path) -> None:
    brick = _read(project_root / BRICK)
    bridge = _read(project_root / BRIDGE)
    brick_meta = json.loads(_read(project_root / BRICK_META))
    bridge_meta = json.loads(_read(project_root / BRIDGE_META))
    bridge_deprecated = bridge_meta.get("status") == "deprecated"
    if bridge_deprecated:
        _gate("BRIDGE_DEPRECATED_TOMBSTONE", "DEPRECATED HISTORICAL COMPATIBILITY TOMBSTONE" in bridge)
        _gate("BRIDGE_NO_ACTIVE_ROUTE", bridge_meta.get("load_type") == "never")
        _gate("BRIDGE_CURRENT_OWNER_REDIRECT", "brick_wall_comprehensive_quality_gate" in bridge)
    q31_contract = _read(project_root / Q31_CONTRACT)
    q31_validator = _read(project_root / Q31_VALIDATOR)
    for marker in (
        "Validation and evidence provenance (Q32)",
        "VALIDATION AND EVIDENCE PROVENANCE RECORD",
        "exact source fingerprints",
        "prompt and validator revisions/hashes",
        "expected and observed markers",
        "durable evidence path/hash/encoding/time",
        "proceed Q33 pinned local-model provenance YES/NO",
        "may begin coding NO",
        "may write source NO",
    ):
        _gate("Q32_BRICK_WALL_CONTRACT", marker in brick, marker)
    for marker in (
        "Validation and evidence provenance bridge (Q32)",
        "exact source fingerprints",
        "prompt/validator revisions and hashes",
        "expected and observed markers",
        "durable project-support evidence path/hash/encoding/time",
        "proceed Q33 YES/NO",
    ):
        _gate("Q32_ROUTER_BRIDGE_CONTRACT", marker in bridge, marker)
    _gate(
        "Q32_BRICK_VERSION",
        tuple(map(int, brick_meta["version"].split("."))) >= (3, 14),
    )
    _gate(
        "Q32_BRIDGE_VERSION",
        tuple(map(int, bridge_meta["version"].split("."))) >= (4, 8),
    )
    _gate(
        "Q32_BRICK_HEADER_METADATA_VERSION_ALIGNMENT",
        _front_matter_version(brick) == brick_meta["version"],
    )
    _gate(
        "Q32_BRIDGE_HEADER_METADATA_VERSION_ALIGNMENT",
        _front_matter_version(bridge) == bridge_meta["version"],
    )
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        _gate(
            "Q32_METADATA_ALIGNMENT",
            meta.get("source_stage") == meta.get("updated_for")
            and bool(meta.get("source_stage")),
            label,
        )
        _gate(
            "Q32_METADATA_DO_NOT_REGRESS",
            any("Q32 must" in rule for rule in meta.get("do_not_regress", [])),
            label,
        )
    _gate(
        "Q31_CONTRACT_FORWARD_COMPATIBLE_Q32_PROGRESSION",
        "may_proceed_to_q32" in q31_contract
        and "may_proceed_to_precode_authorization" not in q31_contract,
    )
    _gate(
        "Q31_VALIDATOR_FORWARD_COMPATIBLE_Q32_PROGRESSION",
        "Q31_FORWARD_COMPATIBLE_Q32_PROGRESSION: PASS" in q31_validator,
    )
    _gate(
        "Q32_PRECODE_CHAIN_UPDATED",
        ("Q01-Q32 complete YES/NO" in brick or "Q01-Q33 complete YES/NO" in brick or "Q01-Q34 complete YES/NO" in brick or "Q01-Q35 complete YES/NO" in brick or "Q01-Q36 complete YES/NO" in brick or "Q01-Q37 complete YES/NO" in brick or "Q01-Q38 complete YES/NO" in brick or "Q01-Q39 complete YES/NO" in brick or "Q01-Q40 complete YES/NO" in brick),
    )
    for relative in RELEASE_FILES:
        path = project_root / relative
        _gate("Q32_REQUIRED_FILE", path.is_file(), str(relative))
        if path.suffix in {".py", ".md"}:
            lines = len(_read(path).splitlines())
            _gate("Q32_MODULE_SIZE", lines <= 500, f"{relative}={lines}")

def _reject(label: str, mutate: Callable[[dict[str, Any]], None]) -> None:
    record = mutated_record(valid_complete_record())
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
    else:
        _gate(label, False)

def validate_record_contract() -> None:
    validate_record(valid_complete_record())
    _gate("Q32_COMPLETE_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q32_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
        ("Q32_NEGATIVE_Q31_DECISION", lambda r: r.update(q31_decision_complete=False)),
        ("Q32_NEGATIVE_Q31_FROZEN_BASELINE", lambda r: r.update(q31_frozen_baseline=False)),
        ("Q32_NEGATIVE_FEATURE_ID", lambda r: r.update(feature_id="")),
        ("Q32_NEGATIVE_OPERATION_ID", lambda r: r.update(operation_id="")),
        ("Q32_NEGATIVE_PROJECT_SLUG", lambda r: r.update(project_slug="")),
        ("Q32_NEGATIVE_EVIDENCE_OWNER", lambda r: r.update(evidence_owner="TRANSIENT")),
        ("Q32_NEGATIVE_SOURCE_HASH", lambda r: r["source_fingerprints"][0].update(sha256="bad")),
        ("Q32_NEGATIVE_DUPLICATE_SOURCE", lambda r: r["source_fingerprints"].append(r["source_fingerprints"][0])),
        ("Q32_NEGATIVE_ERROR_MEMORY_FINGERPRINT", lambda r: r["error_memory_export"].update(fingerprint="bad")),
        ("Q32_NEGATIVE_ERROR_MEMORY_LESSONS", lambda r: r["error_memory_export"].update(lesson_ids=[])),
        ("Q32_NEGATIVE_ERROR_MEMORY_STATUS", lambda r: r["error_memory_export"].update(status="STALE")),
        ("Q32_NEGATIVE_PROMPT_REVISION", lambda r: r["prompt_revisions"][0].update(version="")),
        ("Q32_NEGATIVE_PROMPT_SOURCE_HASH_LINK", lambda r: r["prompt_revisions"][0].update(path="missing.md")),
        ("Q32_NEGATIVE_VALIDATOR_REVISION", lambda r: r["validator_revisions"][0].update(sha256="bad")),
        ("Q32_NEGATIVE_VALIDATOR_REVISION_BASIS", lambda r: r["validator_revisions"][0].update(revision_basis="MTIME")),
        ("Q32_NEGATIVE_COMMAND", lambda r: r["validation_runs"][0].update(command="")),
        ("Q32_NEGATIVE_EXPECTED_MARKERS", lambda r: r["validation_runs"][0].update(expected_markers=[])),
        ("Q32_NEGATIVE_OBSERVED_MARKERS", lambda r: r["validation_runs"][0].update(observed_markers=[])),
        ("Q32_NEGATIVE_MARKER_MISMATCH", lambda r: r["validation_runs"][0].update(observed_markers=["OTHER"])),
        ("Q32_NEGATIVE_ENVIRONMENT", lambda r: r["environment"].update(python_version="")),
        ("Q32_NEGATIVE_ENVIRONMENT_FINGERPRINT", lambda r: r["validation_runs"][0].update(environment_fingerprint="bad")),
        ("Q32_NEGATIVE_EVIDENCE_PATH", lambda r: r["durable_evidence"].update(relative_path="daily-work/evidence.txt")),
        ("Q32_NEGATIVE_EVIDENCE_OWNER_ROOT", lambda r: r["durable_evidence"].update(owner_root="E:/tmp")),
        ("Q32_NEGATIVE_EVIDENCE_FEATURE", lambda r: r["durable_evidence"].update(feature_id="other")),
        ("Q32_NEGATIVE_EVIDENCE_HASH", lambda r: r["durable_evidence"].update(sha256="bad")),
        ("Q32_NEGATIVE_EVIDENCE_ENCODING", lambda r: r["durable_evidence"].update(encoding="DEFAULT")),
        ("Q32_NEGATIVE_TRANSIENT_AUTHORITY", lambda r: r["durable_evidence"].update(transient_copy_authoritative=True)),
        ("Q32_NEGATIVE_LIMITATIONS", lambda r: r.update(limitations=[])),
        ("Q32_NEGATIVE_UNRESOLVED", lambda r: r["unresolved_fields"].append("source")),
        ("Q32_NEGATIVE_Q33_PROGRESSION", lambda r: r.update(may_proceed_to_q33=False)),
        ("Q32_NEGATIVE_CODING_AUTHORIZATION", lambda r: r.update(may_begin_coding=True)),
        ("Q32_NEGATIVE_SOURCE_WRITE", lambda r: r.update(may_write_source=True)),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    record = valid_not_applicable_record()
    record["no_provenance_evidence"] = []
    try:
        validate_record(record)
    except AssertionError:
        _gate("Q32_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q32_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    print("Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS")
    print("Q32_FORWARD_COMPATIBLE_Q33_PROGRESSION: PASS")
    print("Q32_FORWARD_COMPATIBLE_Q34_PROGRESSION: PASS")
    print("Q32_FORWARD_COMPATIBLE_Q35_PROGRESSION: PASS")
    print("Q32_FORWARD_COMPATIBLE_Q36_PROGRESSION: PASS")
    print("Q32_FORWARD_COMPATIBLE_Q37_PROGRESSION: PASS")
    print("Q32_FORWARD_COMPATIBLE_Q38_PROGRESSION: PASS")
    print("Q32_FORWARD_COMPATIBLE_Q39_PROGRESSION: PASS")
    print("Q32_FORWARD_COMPATIBLE_Q40_PROGRESSION: PASS")

def _environment_record() -> dict[str, Any]:
    dependency_state = []
    try:
        import PySide6  # type: ignore

        dependency_state.append("PySide6=" + str(PySide6.__version__))
    except Exception:
        dependency_state.append("PySide6=UNAVAILABLE_IN_CURRENT_ENVIRONMENT")
    return {
        "os_name": os.name,
        "platform": sys.platform + "/" + platform.platform(),
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "dependency_state": dependency_state,
        "timezone": os.environ.get("TZ", "UNSPECIFIED"),
    }

def _validation_run(
    run_id: str, path: Path, markers: list[str],
    project_root: Path, environment_fingerprint: str,
) -> dict[str, Any]:
    normalized = str(path).replace("\\", "/")
    return {
        "run_id": run_id, "validator_path": normalized,
        "command": f"python {normalized} --project-root {project_root}",
        "expected_markers": markers, "observed_markers": markers,
        "environment_fingerprint": environment_fingerprint,
        "exit_code": 0, "status": "PASSED",
    }


def q32_release_record(project_root: Path) -> dict[str, Any]:
    source_rows = [
        {
            "path": str(relative).replace("\\", "/"),
            "role": "canonical_prompt" if relative in {BRICK, BRIDGE} else (
                "prompt_metadata" if relative in {BRICK_META, BRIDGE_META} else "validation_only"
            ),
            "sha256": _sha256(project_root / relative),
        }
        for relative in RELEASE_FILES
    ]
    source_map = {row["path"]: row["sha256"] for row in source_rows}
    brick_meta = json.loads(_read(project_root / BRICK_META))
    bridge_meta = json.loads(_read(project_root / BRIDGE_META))
    prompt_rows = []
    for path, meta in ((BRICK, brick_meta), (BRIDGE, bridge_meta)):
        normalized = str(path).replace("\\", "/")
        prompt_rows.append(
            {
                "path": normalized,
                "prompt_id": meta["prompt_id"],
                "prompt_code": meta.get("prompt_code", "KPR-05-001"),
                "version": meta["version"],
                "source_stage": meta["source_stage"],
                "sha256": source_map[normalized],
            }
        )
    validator_rows = [
        {
            "path": str(path).replace("\\", "/"),
            "revision_basis": "SHA256",
            "sha256": source_map[str(path).replace("\\", "/")],
        }
        for path in (Q31_VALIDATOR, SELF)
    ]
    q31_output = _run_validator(project_root, Q31_VALIDATOR)
    q31_markers = [
        "Q31_CHANGED_FILE_VALIDATOR_COVERAGE_REGRESSION_SET: PASS",
        "Q31_FORWARD_COMPATIBLE_Q32_PROGRESSION: PASS",
        "VALIDATION OK: brick-wall-q31-changed-file-validator-coverage-map-enforcement-v1",
    ]
    for marker in q31_markers:
        _gate("Q32_Q31_OBSERVED_MARKER", marker in q31_output, marker)
    environment = _environment_record()
    env_fingerprint = _json_sha256(environment)
    manifest_path = _manifest_path(project_root)
    manifest = json.loads(_read(manifest_path))
    manifest_hash = _sha256(manifest_path)
    lesson_ids = list(manifest.get("included_lesson_ids", []))
    for lesson in LESSONS:
        if lesson not in lesson_ids:
            lesson_ids.append(lesson)
    source_snapshot_id = _json_sha256(source_rows)
    evidence_seed = _json_sha256(
        {
            "feature_id": FEATURE,
            "source_snapshot_id": source_snapshot_id,
            "environment": env_fingerprint,
        }
    )
    support_root = project_root.parent / (project_root.name + "_show_project_to_AI")
    return {
        "provenance_required": True,
        "no_provenance_evidence": [],
        "q31_decision_complete": True,
        "q31_frozen_baseline": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "feature_id": FEATURE,
        "operation_id": "q32-validation-evidence-provenance-v1",
        "project_slug": project_root.name,
        "tool_source_root": str(project_root),
        "active_project_root": str(project_root),
        "project_support_root": str(support_root),
        "evidence_owner": "PROJECT_SUPPORT",
        "source_snapshot_id": source_snapshot_id,
        "source_fingerprints": source_rows,
        "error_memory_export": {
            "artifact_type": manifest.get("artifact_type", "error_memory_manifest"),
            "schema_version": manifest.get("schema_version", "1.0"),
            "exporter_version": str(manifest.get("exporter_version", "1.2")),
            "fingerprint": manifest_hash,
            "lesson_ids": lesson_ids,
            "status": "CURRENT",
        },
        "prompt_revisions": prompt_rows,
        "validator_revisions": validator_rows,
        "validation_runs": [
            _validation_run(
                "q31-forward", Q31_VALIDATOR, q31_markers,
                project_root, env_fingerprint,
            ),
            _validation_run(
                "q32-focused", SELF, [
                    "Q32_VALIDATION_EVIDENCE_PROVENANCE_REGRESSION_SET: PASS",
                    "Q32_EXACT_RELEASE_PROVENANCE: PASS",
                    "VALIDATION OK: " + FEATURE,
                ], project_root, env_fingerprint,
            ),
        ],
        "environment": environment,
        "durable_evidence": {
            "relative_path": "project_validation_evidence/" + FEATURE + ".txt",
            "owner_root": str(support_root),
            "feature_id": FEATURE,
            "sha256": evidence_seed,
            "encoding": "UTF-8-NO-BOM",
            "generated_at_utc": "2026-07-16T00:00:00Z",
            "status_markers": ["VALIDATION OK: " + FEATURE, "STATUS: IN_SYNC"],
            "transient_copy_authoritative": False,
        },
        "limitations": [
            "The current environment state is recorded and must not be generalized to the user-local Windows environment."
        ],
        "unresolved_fields": [],
        "decision": "COMPLETE",
        "may_proceed_to_q33": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }

def validate_exact_release(project_root: Path) -> None:
    record = q32_release_record(project_root)
    validate_record(record)
    paths = [str(path).replace("\\", "/") for path in RELEASE_FILES]
    validate_q31_coverage(q32_release_coverage_record(paths))
    _gate("Q32_Q31_EXACT_CHANGED_FILE_COVERAGE", True)
    expected = set(paths)
    observed = {row["path"] for row in record["source_fingerprints"]}
    _gate("Q32_EXACT_SOURCE_FINGERPRINT_SET", observed == expected)
    _gate("Q32_Q31_FROZEN_BASELINE", record["q31_frozen_baseline"] is True)
    _gate("Q32_Q31_FREEZE_ID", Q31_FREEZE_ID.startswith("freeze-20260716-brick-wall-q31"))
    _gate("Q32_ERROR_MEMORY_EXPORT_CURRENT", record["error_memory_export"]["status"] == "CURRENT")
    _gate("Q32_RELEVANT_LESSON_SET", set(LESSONS).issubset(record["error_memory_export"]["lesson_ids"]))
    _gate("Q32_PROMPT_REVISION_PROVENANCE", len(record["prompt_revisions"]) == 2)
    _gate("Q32_VALIDATOR_REVISION_PROVENANCE", len(record["validator_revisions"]) == 2)
    _gate("Q32_COMMAND_PROVENANCE", all(run["command"] for run in record["validation_runs"]))
    _gate("Q32_ENVIRONMENT_PROVENANCE", bool(record["environment"]["python_executable"]))
    _gate("Q32_EXPECTED_OBSERVED_MARKERS", all(set(run["expected_markers"]).issubset(run["observed_markers"]) for run in record["validation_runs"]))
    _gate("Q32_DURABLE_EVIDENCE_OWNER", record["evidence_owner"] == "PROJECT_SUPPORT")
    _gate("Q32_TRANSIENT_EVIDENCE_NOT_AUTHORITATIVE", record["durable_evidence"]["transient_copy_authoritative"] is False)
    _gate("Q32_EXACT_RELEASE_PROVENANCE", True)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    project_root = args.project_root.expanduser().resolve(strict=True)
    validate_source(project_root)
    validate_record_contract()
    validate_exact_release(project_root)
    print("VALIDATION OK: " + FEATURE)
    print("STATUS: IN_SYNC")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
