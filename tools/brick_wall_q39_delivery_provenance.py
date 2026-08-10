# project-path: tools/brick_wall_q39_delivery_provenance.py
"""Durable-evidence construction for Q39 delivery validation."""
from __future__ import annotations
__all__: list[str] = []
from datetime import datetime, timezone
import hashlib
import json
import os
import platform
import sys
import zipfile
from pathlib import Path
from typing import Callable

FEATURE_ID = "brick-wall-q39-task-specific-context-admission-enforcement-v1"
Q38_FREEZE_ID = "freeze-20260716-brick-wall-q38-handoff-freshness-and-provenance-v1"


def _dependency_version(name: str) -> str:
    try:
        module = __import__(name)
    except Exception:
        return "UNAVAILABLE"
    return str(getattr(module, "__version__", "AVAILABLE_VERSION_UNKNOWN"))


def _freeze_context(support: Path) -> tuple[str, str]:
    loose = support / "first_prompt_files/09_active_project_freeze_context.md"
    startup_zip = support / "first_prompt_files/first_prompts_to_ai.zip"
    if loose.is_file():
        return str(loose), loose.read_text(encoding="utf-8")
    if startup_zip.is_file():
        try:
            with zipfile.ZipFile(startup_zip) as archive:
                text = archive.read("09_active_project_freeze_context.md").decode("utf-8")
            return str(startup_zip) + "!09_active_project_freeze_context.md", text
        except (KeyError, UnicodeDecodeError, zipfile.BadZipFile):
            return str(startup_zip), ""
    return str(loose), ""


def build_provenance_payload(project_root: Path, patch_manifest: dict, runs: list[dict], *, support_root: Callable[[Path], Path], error_memory_manifest: Callable[[Path], Path], load_json: Callable[[Path], dict], sha256: Callable[[Path], str]) -> dict:
    support = support_root(project_root)
    manifest_path = error_memory_manifest(project_root)
    manifest = load_json(manifest_path)
    source_rows = [{"path": path, "sha256": sha256(project_root / path)} for path in patch_manifest["changed_files"]]
    canonical = json.dumps(source_rows, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    source_set_hash = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    freeze_entry = support / "project_freeze_after_update/frozen_features_memory/entries/freeze-20260716-brick-wall-q38-handoff-freshness-and-provenance-v1.md"
    freeze_text = freeze_entry.read_text(encoding="utf-8") if freeze_entry.is_file() else ""
    context_path, context_text = _freeze_context(support)
    module_rows = []
    for path in patch_manifest["touched_python_files"]:
        text = (project_root / path).read_text(encoding="utf-8")
        module_rows.append({"path": path, "physical_lines": len(text.splitlines()), "within_maximum": len(text.splitlines()) <= 500, "sha256": sha256(project_root / path)})
    return {
        "schema_version": "1.0", "record_type": "brick_wall_q39_task_specific_context_admission",
        "feature_id": FEATURE_ID, "operation_id": FEATURE_ID + "-local-validation",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "project_slug": project_root.name, "tool_source_root": str(project_root), "active_project_root": str(project_root),
        "project_support_root": str(support), "evidence_owner": "PROJECT_SUPPORT",
        "source_fingerprints": source_rows, "source_fingerprint_set_hash": source_set_hash,
        "error_memory_export": {"path": str(manifest_path), "sha256": sha256(manifest_path), "artifact_type": manifest.get("artifact_type", "error_memory_manifest"), "lesson_ids": patch_manifest["error_memory_lessons_applied"], "freshness": "CURRENT_AT_VALIDATION"},
        "validator_revisions_and_commands": runs,
        "environment": {"os_name": os.name, "platform": sys.platform + "/" + platform.platform(), "python_version": platform.python_version(), "python_executable": sys.executable, "pyside6": _dependency_version("PySide6"), "validator_cwd": str(project_root), "project_root_pythonpath_bound": True},
        "q39_context_admission_decision": {
            "decision": "NOT_APPLICABLE", "q38_frozen_baseline": Q38_FREEZE_ID,
            "freeze_entry_path": str(freeze_entry), "freeze_entry_present": freeze_entry.is_file(),
            "freeze_entry_matches_q38": Q38_FREEZE_ID in freeze_text and 'status: "frozen"' in freeze_text,
            "freeze_context_path": context_path, "freeze_context_present": bool(context_text),
            "freeze_context_latest_q38": Q38_FREEZE_ID in context_text,
            "freeze_context_sha256": hashlib.sha256(context_text.encode("utf-8")).hexdigest() if context_text else "",
            "new_context_proposed": False, "controlled_task_comparison_required": False,
            "runtime_context_owner_modified": False, "new_context_engine_created": False,
            "new_intelligence_system_created": False, "new_context_registry_created": False,
            "current_context_owners_reused": True, "source_set_hash": source_set_hash,
            "touched_python_modules": module_rows, "all_touched_python_within_maximum": all(row["within_maximum"] for row in module_rows),
        },
        "expected_markers": [
            "Q39_TASK_SPECIFIC_CONTEXT_ADMISSION_REGRESSION_SET: PASS",
            "Q39_EXISTING_CONTEXT_AUTHORITIES_REUSED: PASS",
            "Q39_CURRENT_RELEASE_CONTEXT_NOT_APPLICABLE: PASS",
            "Q39_Q38_FROZEN_BASELINE: PASS",
            "Q39_NO_USER_FACING_POWERSHELL_ELSE_OR_ELSEIF: PASS",
            "Q01_Q39_REGRESSION_CHAIN: PASS", "STARTUP STATUS: IN_SYNC",
            "VALIDATION OK: " + FEATURE_ID, "STATUS: IN_SYNC",
        ],
        "limitations": [
            "No new context artifact is proposed by this release; controlled comparison becomes mandatory only for a future proposal.",
            "Generated handoff and source archives remain evidence only and cannot replace current source.",
            "The build environment cannot claim user-local real-Qt validation.",
        ],
    }


def write_durable_evidence(project_root: Path, validation_text: str, payload: dict, *, support_root: Callable[[Path], Path], sha256: Callable[[Path], str], gate: Callable[[str, bool, str], None]) -> Path:
    evidence_root = support_root(project_root) / "project_validation_evidence"
    evidence_root.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_root / (FEATURE_ID + ".txt")
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    payload_hash = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    pretty = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True)
    final_text = validation_text.rstrip() + "\nQ39_PROVENANCE_JSON_BEGIN\n" + pretty + "\nQ39_PROVENANCE_JSON_END\nQ39_PROVENANCE_PAYLOAD_SHA256: " + payload_hash + "\nVALIDATION OK: " + FEATURE_ID + "\nSTATUS: IN_SYNC\n"
    evidence_path.write_text(final_text, encoding="utf-8", newline="\n")
    strict = evidence_path.read_text(encoding="utf-8")
    gate("Q39_VALIDATION_EVIDENCE_UTF8_CONTRACT", strict == final_text, "")
    gate("Q39_PROVENANCE_JSON_BLOCK", "Q39_PROVENANCE_JSON_BEGIN" in strict and "Q39_PROVENANCE_JSON_END" in strict, "")
    gate("Q39_PROVENANCE_PAYLOAD_HASH", payload_hash in strict, "")
    gate("Q39_DURABLE_VALIDATION_EVIDENCE", evidence_path.is_file(), "")
    print("Q39_DURABLE_EVIDENCE_SHA256: " + sha256(evidence_path))
    print("Durable evidence: " + str(evidence_path))
    return evidence_path
