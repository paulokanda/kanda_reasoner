"""Validate distinct repair feature identity after an older feature is consumed."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.freeze_hint_intake import (  # noqa: E402
    load_latest_freeze_hint_record,
    mark_latest_freeze_hint_used,
    merge_validation_evidence_into_latest_hint,
    read_freeze_hint_from_patch_zip,
    resolve_freeze_hint_autofill_state,
    scan_and_save_latest_freeze_hint,
)
from kanda_reasoner_app.freeze_hint_intake.contract import (  # noqa: E402
    save_freeze_hint_record,
)

OLD_FEATURE_ID = "advanced-quality-review-blocked-stage-correction-lane-v1"
NEW_FEATURE_ID = "advanced-quality-review-heuristic-strategy-atomic-reload-repair-v1"
NEW_FEATURE_TITLE = "Advanced Quality Review Heuristic Strategy and Atomic Reload Repair v1"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-zip", required=True)
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    patch_zip = Path(args.patch_zip).resolve()
    project_root = Path(args.project_root).resolve()
    work_root = project_root.parent / (project_root.name + "_delete_after_daily_work")
    fixture_root = work_root / "validate_freeze_repair_distinct_feature_identity_v1"
    fixture_project = fixture_root / "fixture_project"
    staging = fixture_root / "staging"

    if fixture_root.exists():
        shutil.rmtree(fixture_root)
    fixture_project.mkdir(parents=True)
    staging.mkdir(parents=True)

    new_hint = read_freeze_hint_from_patch_zip(patch_zip)
    assert new_hint["feature_id"] == NEW_FEATURE_ID
    assert new_hint["feature_title"] == NEW_FEATURE_TITLE
    assert new_hint["feature_id"] != OLD_FEATURE_ID

    old_hint = dict(new_hint)
    old_hint["feature_id"] = OLD_FEATURE_ID
    old_hint["feature_title"] = "Advanced Quality Review Blocked Stage Correction Lane v1"
    old_hint["patch_name"] = "kanda_advanced_quality_review_blocked_stage_correction_lane_v1r1"
    old_hint["source_patch_zip"] = old_hint["patch_name"] + ".zip"

    save_freeze_hint_record(
        fixture_project,
        old_hint,
        source_signature={
            "source_path": str(staging / "old_correction_lane.zip"),
            "source_mtime_ns": 1,
            "source_size_bytes": 100,
            "source_name": "old_correction_lane.zip",
        },
    )
    used = mark_latest_freeze_hint_used(
        fixture_project,
        freeze_id="freeze-20260708-advanced-quality-review-blocked-stage-correction-lane-v1",
    )
    assert used.get("ok"), used

    old_zip = staging / "old_correction_lane.zip"
    _write_hint_zip(old_zip, old_hint)
    new_zip = staging / patch_zip.name
    shutil.copy2(patch_zip, new_zip)
    os.utime(old_zip, ns=(1_000_000_000, 1_000_000_000))
    os.utime(new_zip, ns=(2_000_000_000, 2_000_000_000))

    scan = scan_and_save_latest_freeze_hint(fixture_project, staging_dir=staging)
    assert scan.get("ok"), scan
    latest = load_latest_freeze_hint_record(fixture_project)
    assert latest.get("ok"), latest
    record = latest["record"]
    assert record["hint"]["feature_id"] == NEW_FEATURE_ID

    evidence = (
        "ZIP CONTRACT: PASS\n"
        f"VALIDATION OK: {NEW_FEATURE_ID}\n"
        "STATUS: IN_SYNC\n"
        "VALIDATION_EVIDENCE_UTF8_CONTRACT: PASS"
    )
    merged = merge_validation_evidence_into_latest_hint(
        fixture_project,
        evidence,
        feature_id=NEW_FEATURE_ID,
        feature_title=NEW_FEATURE_TITLE,
    )
    assert merged.get("ok"), merged

    fallback = {
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
    state = resolve_freeze_hint_autofill_state(
        fixture_project,
        fallback,
        staging_dir=staging,
    )
    assert state.get("source_kind") != "starter_fallback", state
    assert state["form_inputs"]["feature_title"] == NEW_FEATURE_TITLE
    assert state["validation_evidence_status"] == "recognized"
    assert state["confirm_write_enabled"] is True

    print("OLD_CORRECTION_LANE_IDENTITY_CONSUMED: PASS")
    print("DISTINCT_REPAIR_FEATURE_IDENTITY_SELECTABLE: PASS")
    print("DISTINCT_REPAIR_VALIDATION_EVIDENCE_MERGES: PASS")
    print("DISTINCT_REPAIR_AUTOFILL_AVOIDS_STARTER_FALLBACK: PASS")
    print("VALIDATION OK: freeze-repair-distinct-feature-identity-v1")
    print("STATUS: IN_SYNC")


def _write_hint_zip(path: Path, hint: dict[str, object]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "KANDA_FREEZE_HINT.json",
            json.dumps(hint, ensure_ascii=True, indent=2) + "\n",
        )


if __name__ == "__main__":
    main()
