"""Validate the freeze validation evidence merge paradigm patch."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

FEATURE_ID = "freeze-validation-evidence-merge-paradigm-v1"
FEATURE_TITLE = "Freeze Validation Evidence Merge Paradigm"
PROMPT_MARKER = "PATCH_VALIDATION_EVIDENCE_MERGE_PARADIGM_V1_BEGIN"
SCRIPT_REL = Path("scripts") / "merge_freeze_validation_evidence.py"


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _assert_prompt_markers(project_root: Path) -> None:
    prompt_paths = [
        project_root
        / "kanda_prompt_workspace"
        / "prompt_library"
        / "ACTIVE_PROMPTS"
        / "01_session_start_and_navigation"
        / "daily_patch_delivery_guardrails.md",
        project_root
        / "kanda_prompt_workspace"
        / "prompt_library"
        / "ACTIVE_PROMPTS"
        / "03_governance_freeze_and_handoff"
        / "pre_output_contract_gates.md",
        project_root
        / "kanda_prompt_workspace"
        / "prompt_library"
        / "ACTIVE_PROMPTS"
        / "03_governance_freeze_and_handoff"
        / "freeze_code_intake_and_form_protocol.md",
    ]
    for path in prompt_paths:
        text = _read(path)
        if PROMPT_MARKER not in text:
            raise AssertionError("Prompt marker missing in " + str(path))
        lowered = text.lower()
        required_fragments = [
            "merge_freeze_validation_evidence.py",
            "freeeze_hint_evidence_merge_ok".replace("freeeze", "freeze"),
            "validation ok: <feature_id>",
        ]
        for fragment in required_fragments:
            if fragment not in lowered:
                raise AssertionError("Prompt fragment missing in " + str(path) + ": " + fragment)


def _assert_startup_sync_exposure(project_root: Path) -> None:
    sync_script = project_root / "kanda_prompt_workspace" / "prompt_tools" / "sync_startup_routing_kernel_pack.py"
    if not sync_script.is_file():
        return
    result = subprocess.run(
        [sys.executable, str(sync_script), "--ensure-sync", "--yes"],
        cwd=str(project_root),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError("Startup sync failed:\n" + result.stdout + result.stderr)
    output = result.stdout + result.stderr
    if "STATUS: IN_SYNC" not in output:
        raise AssertionError("Startup sync did not report STATUS: IN_SYNC.")
    first_zip = (
        project_root.parent
        / (project_root.name + "_show_project_to_AI")
        / "first_prompt_files"
        / "first_prompts_to_ai.zip"
    )
    if not first_zip.is_file():
        return
    with zipfile.ZipFile(first_zip, "r") as archive:
        startup_text = archive.read("07_daily_patch_delivery_guardrails.md").decode(
            "utf-8-sig",
            errors="replace",
        )
    if PROMPT_MARKER not in startup_text:
        raise AssertionError("Startup ZIP does not expose the merge paradigm marker.")


def _assert_merge_helper(project_root: Path) -> None:
    helper = project_root / SCRIPT_REL
    if not helper.is_file():
        raise AssertionError("Merge helper missing: " + str(helper))

    sys.path.insert(0, str(project_root))
    from kanda_reasoner_app.freeze_hint_intake import (  # noqa: WPS433
        build_freeze_form_inputs_from_latest_hint,
    )
    from kanda_reasoner_app.freeze_hint_intake.contract import (  # noqa: WPS433
        save_freeze_hint_record,
    )

    with tempfile.TemporaryDirectory() as tmp_name:
        temp_project = Path(tmp_name) / "sample_project"
        temp_project.mkdir()
        hint = {
            "feature_id": FEATURE_ID,
            "feature_title": FEATURE_TITLE,
            "primary_box": "kanda_reasoner_app/freeze_hint_intake",
            "box_type": "validation evidence merge helper",
            "validated_files": [str(SCRIPT_REL).replace("\\", "/")],
            "generated_files": [],
            "protected_paths": [
                "project_freeze_after_update/freeze_hint_intake",
                "project_freeze_after_update/frozen_features_memory",
            ],
            "do_not_regress_rules": [
                "Do not freeze from stale pre-validation sidecar evidence.",
            ],
            "validation_evidence_summary": (
                "Sandbox validation only. Local validation must confirm before freeze."
            ),
            "known_warnings": "Local validation pending before merge.",
            "planned_next_step": "Run local validation.",
            "notes": "Temporary validation fixture.",
        }
        save_freeze_hint_record(temp_project, hint)
        evidence_path = temp_project / "evidence.txt"
        evidence_path.write_text(
            "ZIP CONTRACT: PASS\n"
            f"VALIDATION OK: {FEATURE_ID}\n"
            "VALIDATION COMMAND COMPLETE\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                sys.executable,
                str(helper),
                "--project-root",
                str(temp_project),
                "--feature-id",
                FEATURE_ID,
                "--feature-title",
                FEATURE_TITLE,
                "--evidence-file",
                str(evidence_path),
            ],
            cwd=str(project_root),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError("Merge helper failed:\n" + result.stdout + result.stderr)
        if f"FREEZE_HINT_EVIDENCE_MERGE_OK: {FEATURE_ID}" not in result.stdout:
            raise AssertionError("Merge helper success marker missing.")
        form = build_freeze_form_inputs_from_latest_hint(temp_project, {})
        if not isinstance(form, dict) or not form:
            raise AssertionError("Freeze form build failed: " + json.dumps(form, sort_keys=True))
        evidence = str(form.get("validation_evidence_summary") or "")
        if f"VALIDATION OK: {FEATURE_ID}" not in evidence:
            raise AssertionError("Merged validation evidence missing VALIDATION OK marker.")
        if f"FREEZE_HINT_EVIDENCE_MERGE_OK: {FEATURE_ID}" not in evidence:
            raise AssertionError("Merged validation evidence missing merge marker.")
        if "Local validation must confirm" in evidence:
            raise AssertionError("Stale pending validation text was not removed.")


def main() -> int:
    project_root = _project_root()
    _assert_prompt_markers(project_root)
    _assert_merge_helper(project_root)
    _assert_startup_sync_exposure(project_root)
    print(f"VALIDATION OK: {FEATURE_ID}")
    print(f"FREEZE_HINT_EVIDENCE_MERGE_OK: {FEATURE_ID}")
    print("VALIDATE_CODE_PARADIGM: local evidence merge enforced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
