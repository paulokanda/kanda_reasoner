#!/usr/bin/env python3
"""Validate Error Memory packaged lesson schema guard v2."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

FEATURE_ID = "error-memory-packaged-lesson-schema-guard-v2"
EXPECTED_MARKER = "VALIDATION OK: " + FEATURE_ID
CANON_MARKER = "KANDA_ADDENDUM:active_ready_error_memory_packaged_lesson_contract:v1"
DAILY_MARKER = "KANDA_ADDENDUM:daily_guardrail_error_memory_active_ready_packaging:v1"
BUNDLE_MARKER = "KANDA_ADDENDUM:bundle_error_memory_packaged_lesson_gate:v1"
PIR_MARKER = "PIR-006 - Error Memory packaged lesson missing active-ready metadata"

REQUIRED_CANON_TOKENS = [
    "Active-ready packaged Error Memory lesson contract",
    "redaction.applied",
    "redaction.export_safe",
    "exception",
    "fingerprint",
    "raw_error_snapshot_scrubbed",
    "prevention_triggers",
    "validation_evidence",
    "KANDA_ERROR_LESSON_JSON_BEGIN",
    "payload/error_memory_receive_blocks/KANDA_ERROR_LESSON_JSON_",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def show_project_first_prompt_dir(project_root: Path) -> Path:
    candidates = [
        project_root.parent / (project_root.name + "_show_project_to_AI") / "first_prompt_files",
        Path(project_root.anchor) / (project_root.name + "_show_project_to_AI") / "first_prompt_files",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def run_startup_sync(project_root: Path) -> None:
    tool = project_root / "kanda_prompt_workspace" / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    if not tool.is_file():
        raise AssertionError("startup sync tool missing: " + str(tool))
    cwd = project_root / "kanda_prompt_workspace"
    result = subprocess.run(
        [sys.executable, str(tool), "--ensure-sync", "--yes"],
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = result.stdout or ""
    if result.returncode != 0:
        print(output)
        raise AssertionError("startup sync failed with code " + str(result.returncode))
    if "STATUS: IN_SYNC" not in output and "IN_SYNC" not in output:
        print(output)
        raise AssertionError("startup sync did not report IN_SYNC")


def validate_startup_artifacts(project_root: Path) -> None:
    output_dir = show_project_first_prompt_dir(project_root)
    startup_zip = output_dir / "first_prompts_to_ai.zip"
    prompt_library_zip = output_dir / "prompt_library.zip"
    require(startup_zip.is_file(), "missing first_prompts_to_ai.zip: " + str(startup_zip))
    require(prompt_library_zip.is_file(), "missing prompt_library.zip: " + str(prompt_library_zip))
    with zipfile.ZipFile(startup_zip) as zf:
        require("12_error_memory_ai_formulary_startup_canon.md" in zf.namelist(), "startup zip missing error memory canon")
        startup_text = zf.read("12_error_memory_ai_formulary_startup_canon.md").decode("utf-8", errors="replace")
        require(CANON_MARKER in startup_text, "startup zip missing active-ready error lesson marker")
    with zipfile.ZipFile(prompt_library_zip) as zf:
        path = "ACTIVE_PROMPTS/01_session_start_and_navigation/error_memory_ai_formulary_startup_canon.md"
        require(path in zf.namelist(), "prompt_library.zip missing error memory canon")
        library_text = zf.read(path).decode("utf-8", errors="replace")
        require(CANON_MARKER in library_text, "prompt_library.zip missing active-ready error lesson marker")
        manifest_path = "PROMPT_LIBRARY_ZIP_MANIFEST.json"
        require(manifest_path in zf.namelist(), "prompt_library.zip missing manifest")
        manifest = json.loads(zf.read(manifest_path).decode("utf-8", errors="replace"))
        require(manifest.get("kind") == "prompt_library_zip_manifest", "prompt library manifest kind mismatch")


def main() -> int:
    project_root = Path.cwd().resolve()
    canon = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "error_memory_ai_formulary_startup_canon.md"
    daily = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "daily_patch_delivery_guardrails.md"
    pir = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "patch_install_delivery_error_register.md"
    bundle = project_root / "kanda_prompt_workspace" / "prompt_library" / "ACTIVE_PROMPTS" / "05_patch_delivery_and_validation" / "bundle_gated_development_workflow.md"
    meta = project_root / "kanda_prompt_workspace" / "prompt_library" / "METADATA" / "error_memory_ai_formulary_startup_canon.meta.json"

    for path in [canon, daily, pir, bundle, meta]:
        require(path.is_file(), "missing required file: " + str(path))

    canon_text = read_text(canon)
    require(CANON_MARKER in canon_text, "canon addendum marker missing")
    for token in REQUIRED_CANON_TOKENS:
        require(token in canon_text, "canon missing token: " + token)

    require(DAILY_MARKER in read_text(daily), "daily guardrail marker missing")
    pir_text = read_text(pir)
    require(PIR_MARKER in pir_text, "patch error register entry missing")
    require("<!-- " + PIR_MARKER + " -->" in pir_text, "patch error register safe upsert marker missing")
    require(BUNDLE_MARKER in read_text(bundle), "bundle workflow marker missing")

    meta_data = json.loads(read_text(meta))
    triggers = meta_data.get("trigger_phrases", [])
    require("active-ready packaged Error Memory lesson" in triggers, "metadata trigger missing")
    do_not_regress = "\n".join(meta_data.get("do_not_regress", []))
    require("redaction" in do_not_regress and "fingerprint" in do_not_regress, "metadata do_not_regress missing active-ready fields")

    run_startup_sync(project_root)
    validate_startup_artifacts(project_root)

    print(EXPECTED_MARKER)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
