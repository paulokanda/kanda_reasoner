"""Validate bounded legacy consumed-source compatibility for freeze hint intake."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import time
import zipfile

from kanda_reasoner_app.freeze_hint_intake.contract import (
    build_freeze_hint_intake_paths,
    resolve_freeze_hint_autofill_state,
    scan_and_save_latest_freeze_hint,
)

FEATURE_ID = "aqr-correction-session-until-fresh-pass-v1"
FEATURE_TITLE = "AQR Correction Session Until Fresh Pass v1"
PATCH_NAME = "kanda_aqr_correction_session_until_fresh_pass_v1r4"


def _hint() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "kind": "kanda_freeze_hint",
        "feature_id": FEATURE_ID,
        "feature_title": FEATURE_TITLE,
        "primary_box": "large_file_refactor_workbench",
        "box_type": "tool_gui_aqr_correction_session_with_bounded_legacy_consumed_source_matching",
        "patch_name": PATCH_NAME,
        "source_patch_zip": PATCH_NAME + ".zip",
        "validated_files": [
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_aqr_correction_session.py",
            "kanda_reasoner_app/freeze_hint_intake/consumed_hints.py",
        ],
        "generated_files": ["INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"],
        "protected_paths": [
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner",
            "kanda_reasoner_app/freeze_hint_intake",
            "project_freeze_after_update/frozen_features_memory",
        ],
        "do_not_regress_rules": [
            "Anonymous legacy consumed rows must not shadow every future same-feature repair ZIP.",
            "Legacy same-source rows remain compatible when source name can be compared.",
            "Explicit Ignore and confirmed frozen-entry authority remain fail-closed.",
        ],
        "validation_evidence_summary": (
            "ZIP CONTRACT: PASS\n"
            "VALIDATION OK: " + FEATURE_ID + "\n"
            "STATUS: IN_SYNC"
        ),
        "known_warnings": "Controlled legacy consumed-source fixture.",
        "planned_next_step": "Preview and Confirm and Write after human review.",
    }


def _write_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "KANDA_FREEZE_HINT.json",
            json.dumps(_hint(), indent=2, sort_keys=True).encode("utf-8"),
        )


def _fallback() -> dict[str, str]:
    return {
        "feature_title": "Current validated feature - replace with exact feature title",
        "primary_box": "Replace with the primary box for the current feature",
        "box_type": "Replace with the current box type",
        "validated_files": "",
        "generated_files": "",
        "protected_paths": "project_freeze_after_update/frozen_features_memory",
        "do_not_regress_rules": "Do not freeze without current feature validation evidence.",
        "validation_evidence_summary": "",
        "known_warnings": "Starter draft only.",
        "planned_next_step": "Replace placeholders.",
        "notes": "",
    }


def _write_consumed_item(project: Path, item: dict[str, object]) -> None:
    paths = build_freeze_hint_intake_paths(project)
    paths.intake_root.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "kind": "kanda_consumed_freeze_hints",
        "items": [item],
    }
    paths.consumed_hints.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def _base_item() -> dict[str, object]:
    return {
        "consumed_at_utc": "2026-07-08T05:00:00Z",
        "used_freeze_id": "",
        "feature_id": FEATURE_ID,
        "feature_title": FEATURE_TITLE,
    }


def _new_fixture(root: Path, suffix: str) -> tuple[Path, Path, Path]:
    project = root / ("kanda_reasoner_" + suffix)
    staging = root / (project.name + "_delete_after_daily_work")
    project.mkdir()
    staging.mkdir()
    patch_zip = staging / (PATCH_NAME + ".zip")
    _write_zip(patch_zip)
    now = time.time()
    os.utime(patch_zip, (now, now))
    return project, staging, patch_zip


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kanda_freeze_legacy_consumed_source_") as temp:
        root = Path(temp)

        project, staging, patch_zip = _new_fixture(root, "anonymous")
        item = _base_item()
        item["source"] = {}
        _write_consumed_item(project, item)
        result = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert result.get("ok"), result
        print("LEGACY_ANONYMOUS_CONSUMED_ROW_DOES_NOT_BLOCK_COMPLETE_REPAIR: PASS")

        state = resolve_freeze_hint_autofill_state(
            project,
            _fallback(),
            staging_dir=staging,
        )
        form = dict(state.get("form_inputs") or {})
        assert state.get("confirm_write_enabled") is True, state
        assert form.get("feature_title") == FEATURE_TITLE, form
        assert form.get("validated_files"), form
        assert "VALIDATION OK: " + FEATURE_ID in form.get("validation_evidence_summary", ""), form
        print("LEGACY_ANONYMOUS_RECOVERY_AUTOFILL_AVOIDS_STARTER: PASS")

        project, staging, patch_zip = _new_fixture(root, "different_name")
        item = _base_item()
        item["source"] = {"source_path": "legacy_prior_repair.zip"}
        _write_consumed_item(project, item)
        result = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert result.get("ok"), result
        print("LEGACY_DIFFERENT_SOURCE_NAME_DOES_NOT_BLOCK_NEW_REPAIR: PASS")

        project, staging, patch_zip = _new_fixture(root, "same_name")
        item = _base_item()
        item["source"] = {"source_path": patch_zip.name}
        _write_consumed_item(project, item)
        result = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert not result.get("ok"), result
        assert patch_zip.name in result.get("skipped_consumed", []), result
        print("LEGACY_SAME_SOURCE_NAME_REMAINS_BLOCKING: PASS")

        project, staging, patch_zip = _new_fixture(root, "ignored")
        item = _base_item()
        item["used_freeze_id"] = "ignored-by-human"
        item["source"] = {}
        _write_consumed_item(project, item)
        result = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert not result.get("ok"), result
        assert patch_zip.name in result.get("skipped_consumed", []), result
        print("EXPLICIT_HUMAN_IGNORE_WITH_LEGACY_SOURCE_REMAINS_AUTHORITATIVE: PASS")

    print("FREEZE_LEGACY_INCOMPLETE_CONSUMED_SOURCE_SHADOWING_REPAIR: PASS")
    print("VALIDATION OK: freeze-legacy-incomplete-consumed-source-shadowing-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
