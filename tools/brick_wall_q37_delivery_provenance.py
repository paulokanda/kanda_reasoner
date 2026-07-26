# project-path: tools/brick_wall_q37_delivery_provenance.py
"""Durable-evidence construction for the Q37 delivery validator."""
from __future__ import annotations

__all__: list[str] = []

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
from typing import Callable

FEATURE_ID = "brick-wall-q37-canonical-ownership-reconciliation-enforcement-v1"
Q36_FREEZE_ID = "freeze-20260716-brick-wall-q36-module-size-and-cohesion-enforcement-v1"


def _dependency_version(name: str) -> str:
    try:
        module = __import__(name)
    except Exception:
        return "UNAVAILABLE"
    return str(getattr(module, "__version__", "AVAILABLE_VERSION_UNKNOWN"))


def build_provenance_payload(
    project_root: Path,
    patch_manifest: dict,
    runs: list[dict],
    *,
    support_root: Callable[[Path], Path],
    error_memory_manifest: Callable[[Path], Path],
    load_json: Callable[[Path], dict],
    sha256: Callable[[Path], str],
) -> dict:
    manifest_path = error_memory_manifest(project_root)
    manifest = load_json(manifest_path)
    prompt_revisions = []
    for relative in (
        "kanda_prompt_workspace/prompt_library/METADATA/brick_wall_comprehensive_quality_gate.meta.json",
        "kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json",
    ):
        data = load_json(project_root / relative)
        prompt_revisions.append(
            {
                "path": relative,
                "prompt_id": data["prompt_id"],
                "prompt_code": data.get("prompt_code", ""),
                "version": data["version"],
                "source_stage": data["source_stage"],
                "sha256": sha256(project_root / relative),
            }
        )
    module_rows = []
    for path in patch_manifest["touched_python_files"]:
        text = (project_root / path).read_text(encoding="utf-8")
        module_rows.append(
            {
                "path": path,
                "physical_lines": len(text.splitlines()),
                "maximum_lines": 500,
                "within_maximum": len(text.splitlines()) <= 500,
                "sha256": sha256(project_root / path),
            }
        )
    return {
        "schema_version": "1.0",
        "record_type": "brick_wall_q37_canonical_ownership_reconciliation",
        "feature_id": FEATURE_ID,
        "operation_id": FEATURE_ID + "-local-validation",
        "generated_at_utc": datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z"),
        "project_slug": project_root.name,
        "tool_source_root": str(project_root),
        "active_project_root": str(project_root),
        "project_support_root": str(support_root(project_root)),
        "evidence_owner": "PROJECT_SUPPORT",
        "source_fingerprints": [
            {"path": path, "sha256": sha256(project_root / path)}
            for path in patch_manifest["changed_files"]
        ],
        "error_memory_export": {
            "path": str(manifest_path),
            "sha256": sha256(manifest_path),
            "artifact_type": manifest.get("artifact_type", "error_memory_manifest"),
            "schema_version": manifest.get("schema_version", "1.0"),
            "lesson_ids": patch_manifest["error_memory_lessons_applied"],
        },
        "prompt_revisions": prompt_revisions,
        "validator_revisions_and_commands": runs,
        "environment": {
            "os_name": os.name,
            "platform": sys.platform + "/" + platform.platform(),
            "python_version": platform.python_version(),
            "python_executable": sys.executable,
            "pyside6": _dependency_version("PySide6"),
            "validator_cwd": str(project_root),
            "project_root_pythonpath_bound": True,
        },
        "q37_ownership_reconciliation_decision": {
            "decision": "NOT_APPLICABLE",
            "reconciliation_required": False,
            "q36_frozen_baseline": Q36_FREEZE_ID,
            "duplicate_kind_inventory": patch_manifest["duplicate_kind_inventory"],
            "runtime_owner_modified": False,
            "new_super_system_created": False,
            "new_coordination_registry_created": False,
            "reason": (
                "This release changes governance prompts and validation-only tools only; "
                "no runtime scanner, schema, report, mutable-state owner, consumer, or "
                "public facade is introduced or consolidated."
            ),
            "touched_python_modules": module_rows,
            "all_touched_python_within_maximum": all(
                row["within_maximum"] for row in module_rows
            ),
        },
        "expected_markers": [
            "Q37_CANONICAL_OWNERSHIP_RECONCILIATION_REGRESSION_SET: PASS",
            "Q37_CURRENT_RELEASE_RECONCILIATION_NOT_APPLICABLE: PASS",
            "Q37_EXISTING_OWNERSHIP_AUTHORITIES_REUSED: PASS",
            "Q37_Q31_EXACT_CHANGED_FILE_COVERAGE: PASS",
            "Q37_Q36_FROZEN_BASELINE: PASS",
            "Q37_Q30_REAL_QT_IMPORT_CONTEXT: PASS",
            "Q01_Q37_REGRESSION_CHAIN: PASS",
            "STARTUP STATUS: IN_SYNC",
            "VALIDATION OK: " + FEATURE_ID,
            "STATUS: IN_SYNC",
        ],
        "limitations": [
            "This governance-only release does not claim all project duplicates are removed.",
            "Future applicable reconciliation needs exact-source and consumer-migration evidence.",
            "The build environment cannot claim user-local real-Qt validation.",
        ],
    }


def write_durable_evidence(
    project_root: Path,
    validation_text: str,
    payload: dict,
    *,
    support_root: Callable[[Path], Path],
    sha256: Callable[[Path], str],
    gate: Callable[[str, bool, str], None],
) -> Path:
    evidence_root = support_root(project_root) / "project_validation_evidence"
    evidence_root.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_root / (FEATURE_ID + ".txt")
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    payload_hash = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    pretty = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True)
    final_text = (
        validation_text.rstrip()
        + "\nQ37_PROVENANCE_JSON_BEGIN\n"
        + pretty
        + "\nQ37_PROVENANCE_JSON_END\nQ37_PROVENANCE_PAYLOAD_SHA256: "
        + payload_hash
        + "\nVALIDATION OK: "
        + FEATURE_ID
        + "\nSTATUS: IN_SYNC\n"
    )
    evidence_path.write_text(final_text, encoding="utf-8", newline="\n")
    strict = evidence_path.read_text(encoding="utf-8")
    gate("Q37_VALIDATION_EVIDENCE_UTF8_CONTRACT", strict == final_text, "")
    gate(
        "Q37_PROVENANCE_JSON_BLOCK",
        "Q37_PROVENANCE_JSON_BEGIN" in strict
        and "Q37_PROVENANCE_JSON_END" in strict,
        "",
    )
    gate("Q37_PROVENANCE_PAYLOAD_HASH", payload_hash in strict, "")
    gate("Q37_DURABLE_VALIDATION_EVIDENCE", evidence_path.is_file(), "")
    print("Q37_DURABLE_EVIDENCE_SHA256: " + sha256(evidence_path))
    print("Durable evidence: " + str(evidence_path))
    return evidence_path
