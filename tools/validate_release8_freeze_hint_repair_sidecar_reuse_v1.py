"""Validate same-feature cumulative repair freeze-hint intake selection."""

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
    resolve_freeze_hint_autofill_state,
    save_freeze_hint_record,
    scan_and_save_latest_freeze_hint,
)

FEATURE_ID = "advanced-quality-review-real-gui-integration-v1"
FEATURE_TITLE = "Advanced Quality Review Real GUI Integration v1"


def _hint(patch_name: str) -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "kind": "kanda_freeze_hint",
        "feature_id": FEATURE_ID,
        "feature_title": FEATURE_TITLE,
        "primary_box": "large_file_refactor_workbench",
        "box_type": "tool_gui_integration",
        "patch_name": patch_name,
        "source_patch_zip": patch_name + ".zip",
        "validated_files": [
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_review_gui.py"
        ],
        "generated_files": ["INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"],
        "protected_paths": [
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner",
            "project_freeze_after_update/frozen_features_memory",
        ],
        "do_not_regress_rules": [
            "Keep the current validated AQR GUI behavior.",
            "Keep Preview Freeze Entry read-only.",
        ],
        "validation_evidence_summary": (
            "VALIDATION OK: " + FEATURE_ID + "\n"
            "LOCAL PATCH VALIDATION COMPLETE: PASS\n"
            "STATUS: IN_SYNC"
        ),
        "known_warnings": "Controlled validation fixture.",
        "planned_next_step": "Freeze current validated feature.",
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
    with tempfile.TemporaryDirectory(prefix="kanda_release8_freeze_hint_repair_") as temp:
        root = Path(temp)
        project = root / "kanda_reasoner"
        staging = root / "kanda_reasoner_delete_after_daily_work"
        project.mkdir()
        staging.mkdir()

        old_zip = staging / "kanda_advanced_quality_review_real_gui_integration_v1r1.zip"
        new_zip = staging / "kanda_advanced_quality_review_real_gui_integration_v1r2.zip"
        _write_hint_zip(old_zip, "kanda_advanced_quality_review_real_gui_integration_v1r1")
        old_time = time.time() - 10
        os.utime(old_zip, (old_time, old_time))

        old_hint = _hint("kanda_advanced_quality_review_real_gui_integration_v1r1")
        old_hint["source"] = {
            "source_path": str(old_zip.resolve()),
            "source_mtime_ns": old_zip.stat().st_mtime_ns,
            "source_size_bytes": old_zip.stat().st_size,
        }
        save_freeze_hint_record(project, old_hint)
        used = mark_latest_freeze_hint_used(project, freeze_id="ignored-by-human")
        assert used.get("ok")

        exact_old_scan = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert not exact_old_scan.get("ok")
        assert old_zip.name in exact_old_scan.get("skipped_consumed", [])
        print("EXACT_CONSUMED_ZIP_REMAINS_BLOCKED: PASS")

        _write_hint_zip(new_zip, "kanda_advanced_quality_review_real_gui_integration_v1r2")
        new_time = time.time()
        os.utime(new_zip, (new_time, new_time))

        scan = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert scan.get("ok"), scan
        assert Path(str(scan.get("source_patch_zip"))).name == new_zip.name
        print("NEWER_SAME_FEATURE_REPAIR_ZIP_REMAINS_SELECTABLE: PASS")

        paths = build_freeze_hint_intake_paths(project)
        saved = json.loads(paths.latest_hint.read_text(encoding="utf-8"))
        assert saved.get("used_at_utc") is None
        assert saved["hint"]["patch_name"].endswith("v1r2")
        print("NEWER_REPAIR_REFRESHES_LATEST_HINT_RECORD: PASS")

        state = resolve_freeze_hint_autofill_state(
            project,
            _fallback(),
            staging_dir=staging,
        )
        form = dict(state.get("form_inputs") or {})
        assert state.get("confirm_write_enabled") is True, state
        assert form.get("feature_title") == FEATURE_TITLE
        assert "VALIDATION OK: " + FEATURE_ID in form.get("validation_evidence_summary", "")
        print("CURRENT_REPAIR_AUTOFILL_AVOIDS_STARTER_FALLBACK: PASS")

        from kanda_reasoner_app.freeze_hint_intake.contract import _same_consumed_source

        current_probe = {
            "source": {
                "source_path": str(new_zip.resolve()),
                "source_name": new_zip.name,
                "source_mtime_ns": new_zip.stat().st_mtime_ns,
                "source_size_bytes": new_zip.stat().st_size,
            },
            "feature_id": FEATURE_ID,
            "feature_title": FEATURE_TITLE,
        }
        same_name_legacy = {
            "source": {"source_path": new_zip.name},
            "feature_id": FEATURE_ID,
            "feature_title": FEATURE_TITLE,
        }
        assert _same_consumed_source(same_name_legacy, current_probe)
        print("LEGACY_INCOMPLETE_SAME_SOURCE_FALLBACK_PRESERVED: PASS")

        anonymous_legacy = {
            "source": {},
            "feature_id": FEATURE_ID,
            "feature_title": FEATURE_TITLE,
        }
        assert not _same_consumed_source(anonymous_legacy, current_probe)
        print("LEGACY_ANONYMOUS_RECORD_DOES_NOT_SHADOW_NEW_REPAIR: PASS")

    print("RELEASE8_FREEZE_HINT_REPAIR_SIDECAR_REUSE: PASS")
    print("VALIDATION OK: release8-freeze-hint-repair-sidecar-reuse-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
