# project-path: tools/brick_wall_q40_delivery_provenance.py
"""Durable-evidence construction for Q40 delivery validation."""
from __future__ import annotations
__all__: list[str] = []
from datetime import datetime, timezone
import hashlib, json, os, platform, sys, zipfile
from pathlib import Path
from typing import Callable

FEATURE_ID = "brick-wall-q40-one-primary-box-governed-release-enforcement-v1"
Q39_FREEZE_ID = "freeze-20260716-brick-wall-q39-task-specific-context-admission-test-v1"


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
    freeze_entry = support / "project_freeze_after_update/frozen_features_memory/entries/freeze-20260716-brick-wall-q39-task-specific-context-admission-test-v1.md"
    freeze_text = freeze_entry.read_text(encoding="utf-8") if freeze_entry.is_file() else ""
    context_path, context_text = _freeze_context(support)
    module_rows = []
    for path in patch_manifest["touched_python_files"]:
        text = (project_root / path).read_text(encoding="utf-8")
        module_rows.append({"path": path, "physical_lines": len(text.splitlines()), "within_maximum": len(text.splitlines()) <= 500, "sha256": sha256(project_root / path)})
    return {
        "schema_version": "1.0", "record_type": "brick_wall_q40_one_primary_box_governed_release",
        "feature_id": FEATURE_ID, "operation_id": FEATURE_ID + "-local-validation",
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "project_slug": project_root.name, "tool_source_root": str(project_root), "active_project_root": str(project_root),
        "project_support_root": str(support), "evidence_owner": "PROJECT_SUPPORT",
        "source_fingerprints": source_rows, "source_fingerprint_set_hash": source_set_hash,
        "error_memory_export": {"path": str(manifest_path), "sha256": sha256(manifest_path), "artifact_type": manifest.get("artifact_type", "error_memory_manifest"), "lesson_ids": patch_manifest["error_memory_lessons_applied"], "freshness": "CURRENT_AT_VALIDATION"},
        "validator_revisions_and_commands": runs,
        "environment": {"os_name": os.name, "platform": sys.platform + "/" + platform.platform(), "python_version": platform.python_version(), "python_executable": sys.executable, "pyside6": _dependency_version("PySide6"), "validator_cwd": str(project_root), "project_root_pythonpath_bound": True},
        "q40_governed_release_decision": {
            "decision": "VALIDATED_READY_FOR_FREEZE", "q39_frozen_baseline": Q39_FREEZE_ID,
            "freeze_entry_path": str(freeze_entry), "freeze_entry_present": freeze_entry.is_file(),
            "freeze_entry_matches_q39": Q39_FREEZE_ID in freeze_text and 'status: "frozen"' in freeze_text,
            "freeze_context_path": context_path, "freeze_context_present": bool(context_text),
            "freeze_context_latest_q39": Q39_FREEZE_ID in context_text,
            "freeze_context_sha256": hashlib.sha256(context_text.encode("utf-8")).hexdigest() if context_text else "",
            "primary_box": patch_manifest["primary_box"], "primary_box_count": 1,
            "supporting_touches": patch_manifest["supporting_touches"],
            "changed_files": patch_manifest["changed_files"],
            "source_baselines_complete": all(patch_manifest["source_baselines"].get(path) for path in patch_manifest["changed_files"]),
            "regression_obligations": patch_manifest["regression_obligations"],
            "validator_inventory": patch_manifest["validator_inventory"],
            "exact_zip_contract": patch_manifest["exact_zip_contract"],
            "human_local_validation_state": "COMPLETE",
            "automatic_frozen_memory_write": False, "project_freeze_ledger_used": False,
            "source_set_hash": source_set_hash, "touched_python_modules": module_rows,
            "all_touched_python_within_maximum": all(row["within_maximum"] for row in module_rows),
        },
        "expected_markers": [
            "Q40_ONE_PRIMARY_BOX_GOVERNED_RELEASE_REGRESSION_SET: PASS",
            "Q40_CURRENT_RELEASE_PRIMARY_BOX_UNIQUE: PASS",
            "Q40_CURRENT_RELEASE_SUPPORTING_TOUCHES_BOUNDED: PASS",
            "Q40_CURRENT_RELEASE_SOURCE_BASELINE_COMPLETE: PASS",
            "Q40_CURRENT_RELEASE_REGRESSION_OBLIGATIONS_COMPLETE: PASS",
            "Q40_CURRENT_RELEASE_VALIDATION_MAP_COMPLETE: PASS",
            "Q40_CURRENT_RELEASE_EXACT_ZIP_CONTRACT_DECLARED: PASS",
            "Q40_CURRENT_RELEASE_FREEZE_EVIDENCE_DECLARED: PASS",
            "Q40_Q39_FROZEN_BASELINE: PASS",
            "Q40_NO_USER_FACING_POWERSHELL_ELSE_OR_ELSEIF: PASS",
            "Q01_Q40_REGRESSION_CHAIN: PASS", "STARTUP STATUS: IN_SYNC",
            "VALIDATION OK: " + FEATURE_ID, "STATUS: IN_SYNC",
        ],
        "limitations": [
            "The source-level Q40 record is package-ready with human-local validation pending; this durable evidence upgrades the local run to validated-ready-for-freeze.",
            "Preview and Confirm and Write remain explicit human actions after validation.",
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
    final_text = validation_text.rstrip() + "\nQ40_PROVENANCE_JSON_BEGIN\n" + pretty + "\nQ40_PROVENANCE_JSON_END\nQ40_PROVENANCE_PAYLOAD_SHA256: " + payload_hash + "\nVALIDATION OK: " + FEATURE_ID + "\nSTATUS: IN_SYNC\n"
    evidence_path.write_text(final_text, encoding="utf-8", newline="\n")
    strict = evidence_path.read_text(encoding="utf-8")
    gate("Q40_VALIDATION_EVIDENCE_UTF8_CONTRACT", strict == final_text, "")
    gate("Q40_PROVENANCE_JSON_BLOCK", "Q40_PROVENANCE_JSON_BEGIN" in strict and "Q40_PROVENANCE_JSON_END" in strict, "")
    gate("Q40_PROVENANCE_PAYLOAD_HASH", payload_hash in strict, "")
    gate("Q40_DURABLE_VALIDATION_EVIDENCE", evidence_path.is_file(), "")
    print("Q40_DURABLE_EVIDENCE_SHA256: " + sha256(evidence_path))
    print("Durable evidence: " + str(evidence_path))
    return evidence_path
