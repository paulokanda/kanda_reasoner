"""Validate freeze delivery refresh for consumed AQR correction-session repairs."""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import time
import zipfile

from kanda_reasoner_app.freeze_hint_intake.contract import (
    build_freeze_hint_intake_paths,
    mark_latest_freeze_hint_used,
    merge_validation_evidence_into_latest_hint,
    resolve_freeze_hint_autofill_state,
    save_freeze_hint_record,
    scan_and_save_latest_freeze_hint,
)

FEATURE_ID = "aqr-correction-session-until-fresh-pass-v1"
FEATURE_TITLE = "AQR Correction Session Until Fresh Pass v1"


def _hint(patch_name: str) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "kind": "kanda_freeze_hint",
        "feature_id": FEATURE_ID,
        "feature_title": FEATURE_TITLE,
        "primary_box": "large_file_refactor_workbench",
        "box_type": "tool_gui_aqr_correction_session_with_noop_rejection_and_fresh_pass_retirement",
        "patch_name": patch_name,
        "source_patch_zip": patch_name + ".zip",
        "validated_files": [
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_aqr_correction_session.py",
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_aqr_snapshot_lifecycle.py",
        ],
        "generated_files": ["INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"],
        "protected_paths": [
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner",
            "project_freeze_after_update/frozen_features_memory",
        ],
        "do_not_regress_rules": [
            "Keep the unresolved AQR correction session active until fresh AQR PASS or PASS_WITH_WARNINGS.",
            "Keep Preview Freeze Entry read-only.",
        ],
        "validation_evidence_summary": (
            "VALIDATION OK: " + FEATURE_ID + "\n"
            "LOCAL PATCH VALIDATION COMPLETE: PASS\n"
            "STATUS: IN_SYNC"
        ),
        "known_warnings": "Controlled delivery-refresh fixture.",
        "planned_next_step": "Freeze the current validated cumulative repair.",
    }


def _write_hint_zip(path: Path, patch_name: str) -> None:
    payload = json.dumps(_hint(patch_name), indent=2, sort_keys=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("KANDA_FREEZE_HINT.json", payload.encode("utf-8"))


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


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="kanda_aqr_session_freeze_delivery_") as temp:
        root = Path(temp)
        project = root / "kanda_reasoner"
        staging = root / "kanda_reasoner_delete_after_daily_work"
        project.mkdir()
        staging.mkdir()

        old_name = "kanda_aqr_correction_session_until_fresh_pass_v1r1"
        new_name = "kanda_aqr_correction_session_until_fresh_pass_v1r2"
        old_zip = staging / (old_name + ".zip")
        new_zip = staging / (new_name + ".zip")

        _write_hint_zip(old_zip, old_name)
        old_time = time.time() - 10
        os.utime(old_zip, (old_time, old_time))
        old_hint = _hint(old_name)
        old_signature = {
            "source_path": str(old_zip.resolve()),
            "source_mtime_ns": old_zip.stat().st_mtime_ns,
            "source_size_bytes": old_zip.stat().st_size,
        }
        save_freeze_hint_record(project, old_hint, source_signature=old_signature)
        used = mark_latest_freeze_hint_used(project, freeze_id="ignored-by-human")
        assert used.get("ok"), used

        exact_old = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert not exact_old.get("ok"), exact_old
        assert old_zip.name in exact_old.get("skipped_consumed", []), exact_old
        print("EXACT_CONSUMED_V1R1_REMAINS_BLOCKED: PASS")

        _write_hint_zip(new_zip, new_name)
        new_time = time.time()
        os.utime(new_zip, (new_time, new_time))

        scan = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert scan.get("ok"), scan
        assert Path(str(scan.get("source_patch_zip"))).name == new_zip.name, scan
        print("NEWER_V1R2_SAME_FEATURE_REMAINS_SELECTABLE: PASS")

        evidence = (
            "ZIP CONTRACT: PASS\n"
            "VALIDATION OK: " + FEATURE_ID + "\n"
            "LOCAL PATCH VALIDATION COMPLETE: PASS\n"
            "STATUS: IN_SYNC\n"
            "VALIDATION_EVIDENCE_UTF8_CONTRACT: PASS"
        )
        merged = merge_validation_evidence_into_latest_hint(
            project,
            evidence,
            feature_id=FEATURE_ID,
            feature_title=FEATURE_TITLE,
        )
        assert merged.get("ok"), merged
        print("V1R2_EVIDENCE_MERGE_RECOGNIZED: PASS")

        state = resolve_freeze_hint_autofill_state(
            project,
            _fallback(),
            staging_dir=staging,
        )
        form = dict(state.get("form_inputs") or {})
        assert state.get("confirm_write_enabled") is True, state
        assert form.get("feature_title") == FEATURE_TITLE, form
        assert "VALIDATION OK: " + FEATURE_ID in form.get("validation_evidence_summary", ""), form
        assert form.get("validated_files"), form
        assert "Current validated feature - replace" not in form.get("feature_title", ""), form
        print("V1R2_AUTOFILL_AVOIDS_STARTER_FALLBACK: PASS")

        paths = build_freeze_hint_intake_paths(project)
        latest = json.loads(paths.latest_hint.read_text(encoding="utf-8"))
        assert latest.get("used_at_utc") is None, latest
        assert latest["hint"]["patch_name"] == new_name, latest
        print("V1R2_LATEST_HINT_REMAINS_UNUSED_UNTIL_CONFIRMED_FREEZE: PASS")

    print("AQR_CORRECTION_SESSION_FREEZE_DELIVERY_REFRESH: PASS")
    print("VALIDATION OK: aqr-correction-session-freeze-delivery-refresh-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
