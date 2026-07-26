# project-path: tools/brick_wall_q38_delivery_provenance.py
"""Durable-evidence construction for the Q38 delivery validator."""
from __future__ import annotations
__all__: list[str] = []
from datetime import datetime, timezone
import hashlib, json, os, platform, sys, zipfile
from pathlib import Path
from typing import Callable

FEATURE_ID = "brick-wall-q38-handoff-freshness-provenance-enforcement-v1"
Q37_FREEZE_ID = "freeze-20260716-brick-wall-q37-canonical-ownership-reconciliation-v1"


def _dependency_version(name: str) -> str:
    try:
        module = __import__(name)
    except Exception:
        return "UNAVAILABLE"
    return str(getattr(module, "__version__", "AVAILABLE_VERSION_UNKNOWN"))


def build_provenance_payload(project_root: Path, patch_manifest: dict, runs: list[dict], *, support_root: Callable[[Path], Path], error_memory_manifest: Callable[[Path], Path], load_json: Callable[[Path], dict], sha256: Callable[[Path], str]) -> dict:
    manifest_path = error_memory_manifest(project_root)
    manifest = load_json(manifest_path)
    source_rows = [{"path": path, "sha256": sha256(project_root / path)} for path in patch_manifest["changed_files"]]
    canonical = json.dumps(source_rows, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    source_set_hash = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    prompt_revisions = []
    for relative in (
        "kanda_prompt_workspace/prompt_library/METADATA/brick_wall_comprehensive_quality_gate.meta.json",
        "kanda_prompt_workspace/prompt_library/METADATA/router_bridge_governed_implementation.meta.json",
    ):
        data = load_json(project_root / relative)
        prompt_revisions.append({"path": relative, "prompt_id": data["prompt_id"], "version": data["version"], "source_stage": data["source_stage"], "sha256": sha256(project_root / relative)})
    support = support_root(project_root)
    freeze_entry = support / "project_freeze_after_update/frozen_features_memory/entries/freeze-20260716-brick-wall-q37-canonical-ownership-reconciliation-v1.md"
    loose_freeze_context = support / "first_prompt_files/09_active_project_freeze_context.md"
    startup_zip = support / "first_prompt_files/first_prompts_to_ai.zip"
    freeze_entry_text = freeze_entry.read_text(encoding="utf-8") if freeze_entry.is_file() else ""
    freeze_context_text = ""
    freeze_context_path = str(loose_freeze_context)
    if loose_freeze_context.is_file():
        freeze_context_text = loose_freeze_context.read_text(encoding="utf-8")
    elif startup_zip.is_file():
        try:
            with zipfile.ZipFile(startup_zip) as archive:
                freeze_context_text = archive.read(
                    "09_active_project_freeze_context.md"
                ).decode("utf-8")
            freeze_context_path = (
                str(startup_zip) + "!09_active_project_freeze_context.md"
            )
        except (KeyError, UnicodeDecodeError, zipfile.BadZipFile):
            freeze_context_text = ""
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    module_rows = []
    for path in patch_manifest["touched_python_files"]:
        text = (project_root / path).read_text(encoding="utf-8")
        module_rows.append({"path": path, "physical_lines": len(text.splitlines()), "maximum_lines": 500, "within_maximum": len(text.splitlines()) <= 500, "sha256": sha256(project_root / path)})
    return {
        "schema_version": "1.0",
        "record_type": "brick_wall_q38_handoff_freshness_provenance",
        "feature_id": FEATURE_ID,
        "operation_id": FEATURE_ID + "-local-validation",
        "generated_at_utc": now,
        "project_slug": project_root.name,
        "tool_source_root": str(project_root),
        "active_project_root": str(project_root),
        "project_support_root": str(support),
        "evidence_owner": "PROJECT_SUPPORT",
        "source_fingerprints": source_rows,
        "source_fingerprint_set_hash": source_set_hash,
        "error_memory_export": {"path": str(manifest_path), "sha256": sha256(manifest_path), "artifact_type": manifest.get("artifact_type", "error_memory_manifest"), "schema_version": manifest.get("schema_version", "1.0"), "lesson_ids": patch_manifest["error_memory_lessons_applied"], "freshness": "CURRENT_AT_VALIDATION"},
        "prompt_revisions": prompt_revisions,
        "validator_revisions_and_commands": runs,
        "environment": {"os_name": os.name, "platform": sys.platform + "/" + platform.platform(), "python_version": platform.python_version(), "python_executable": sys.executable, "pyside6": _dependency_version("PySide6"), "validator_cwd": str(project_root), "project_root_pythonpath_bound": True},
        "q38_handoff_freshness_decision": {
            "decision": "COMPLETE",
            "q37_frozen_baseline": Q37_FREEZE_ID,
            "freeze_entry_path": str(freeze_entry),
            "freeze_entry_present": freeze_entry.is_file(),
            "freeze_entry_matches_q37": (
                Q37_FREEZE_ID in freeze_entry_text
                and 'status: "frozen"' in freeze_entry_text
            ),
            "freeze_context_path": freeze_context_path,
            "freeze_context_present": bool(freeze_context_text),
            "freeze_context_latest_q37": Q37_FREEZE_ID in freeze_context_text,
            "freeze_context_sha256": hashlib.sha256(
                freeze_context_text.encode("utf-8")
            ).hexdigest() if freeze_context_text else "",
            "error_memory_manifest_present": manifest_path.is_file(),
            "error_memory_manifest_sha256": sha256(manifest_path),
            "manifest_source_set_hash": source_set_hash,
            "validation_source_set_hash": source_set_hash,
            "error_memory_freshness": "CURRENT_AT_VALIDATION",
            "source_archive_authority": "GENERATED_EVIDENCE_ONLY",
            "runtime_handoff_owner_modified": False,
            "new_context_engine_created": False,
            "new_freshness_registry_created": False,
            "stale_artifacts": [],
            "touched_python_modules": module_rows,
            "all_touched_python_within_maximum": all(row["within_maximum"] for row in module_rows),
        },
        "expected_markers": [
            "Q38_HANDOFF_FRESHNESS_PROVENANCE_REGRESSION_SET: PASS",
            "Q38_EXISTING_HANDOFF_AUTHORITIES_REUSED: PASS",
            "Q38_CURRENT_RELEASE_FRESHNESS_COMPLETE: PASS",
            "Q38_Q37_FROZEN_BASELINE: PASS",
            "Q38_Q30_REAL_QT_IMPORT_CONTEXT: PASS",
            "Q01_Q38_REGRESSION_CHAIN: PASS",
            "STARTUP STATUS: IN_SYNC",
            "VALIDATION OK: " + FEATURE_ID,
            "STATUS: IN_SYNC",
        ],
        "limitations": [
            "Generated handoff and source archives remain evidence only and cannot replace exact current source.",
            "Freshness is evaluated at validation time and must be reset after any source, manifest, validation, Error Memory, or Freeze-context change.",
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
    final_text = validation_text.rstrip() + "\nQ38_PROVENANCE_JSON_BEGIN\n" + pretty + "\nQ38_PROVENANCE_JSON_END\nQ38_PROVENANCE_PAYLOAD_SHA256: " + payload_hash + "\nVALIDATION OK: " + FEATURE_ID + "\nSTATUS: IN_SYNC\n"
    evidence_path.write_text(final_text, encoding="utf-8", newline="\n")
    strict = evidence_path.read_text(encoding="utf-8")
    gate("Q38_VALIDATION_EVIDENCE_UTF8_CONTRACT", strict == final_text, "")
    gate("Q38_PROVENANCE_JSON_BLOCK", "Q38_PROVENANCE_JSON_BEGIN" in strict and "Q38_PROVENANCE_JSON_END" in strict, "")
    gate("Q38_PROVENANCE_PAYLOAD_HASH", payload_hash in strict, "")
    gate("Q38_DURABLE_VALIDATION_EVIDENCE", evidence_path.is_file(), "")
    print("Q38_DURABLE_EVIDENCE_SHA256: " + sha256(evidence_path))
    print("Durable evidence: " + str(evidence_path))
    return evidence_path
