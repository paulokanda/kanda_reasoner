"""Validate that freeze-hint consumption requires real authority evidence."""

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
    save_freeze_hint_record,
    scan_and_save_latest_freeze_hint,
)

FEATURE_ID = "aqr-correction-session-until-fresh-pass-v1"
FEATURE_TITLE = "AQR Correction Session Until Fresh Pass v1"
PATCH_NAME = "kanda_aqr_correction_session_until_fresh_pass_v1r3"


def _hint() -> dict[str, object]:
    return {
        "schema_version": "1.0",
        "kind": "kanda_freeze_hint",
        "feature_id": FEATURE_ID,
        "feature_title": FEATURE_TITLE,
        "primary_box": "large_file_refactor_workbench",
        "box_type": "tool_gui_aqr_correction_session_with_confirmed_freeze_consumption_authority",
        "patch_name": PATCH_NAME,
        "source_patch_zip": PATCH_NAME + ".zip",
        "validated_files": [
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_aqr_correction_session.py",
            "kanda_reasoner_app/freeze_hint_intake/consumed_hints.py",
            "kanda_reasoner_app/freeze_hint_intake/frozen_matching.py",
            "kanda_reasoner_app/freeze_hint_intake/scanner.py",
        ],
        "generated_files": ["INSTALL.ps1", "VALIDATE.ps1", "FREEZE.ps1"],
        "protected_paths": [
            "kanda_reasoner_app/manage_architecture/large_file_refactor_planner",
            "kanda_reasoner_app/freeze_hint_intake",
            "project_freeze_after_update/frozen_features_memory",
        ],
        "do_not_regress_rules": [
            "Only explicit human ignore or a real confirmed frozen entry may authoritatively consume the current hint.",
            "Stale index-only or orphan freeze-id consumption must not suppress a valid current sidecar.",
            "Preview remains read-only and Confirm and Write remains human-confirmed.",
        ],
        "validation_evidence_summary": (
            "ZIP CONTRACT: PASS\n"
            "VALIDATION OK: " + FEATURE_ID + "\n"
            "STATUS: IN_SYNC"
        ),
        "known_warnings": "Controlled freeze-consumption authority fixture.",
        "planned_next_step": "Preview and Confirm and Write after human review.",
    }


def _write_zip(path: Path) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "KANDA_FREEZE_HINT.json",
            json.dumps(_hint(), indent=2, sort_keys=True).encode("utf-8"),
        )


def _signature(path: Path) -> dict[str, object]:
    return {
        "source_path": str(path.resolve()),
        "source_name": path.name,
        "source_mtime_ns": path.stat().st_mtime_ns,
        "source_size_bytes": path.stat().st_size,
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


def _write_frozen_entry(project: Path, freeze_id: str) -> Path:
    paths = build_freeze_hint_intake_paths(project)
    entries = paths.intake_root.parent / "frozen_features_memory" / "entries"
    entries.mkdir(parents=True, exist_ok=True)
    entry = entries / (freeze_id + ".md")
    entry.write_text(
        "---\n"
        f'freeze_id: "{freeze_id}"\n'
        f'feature_title: "{FEATURE_TITLE}"\n'
        'status: "frozen"\n'
        "---\n\n"
        f"# {freeze_id}\n",
        encoding="utf-8",
    )
    return entry


def _write_stale_index_only(project: Path, freeze_id: str) -> None:
    paths = build_freeze_hint_intake_paths(project)
    memory = paths.intake_root.parent / "frozen_features_memory"
    memory.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "freezes": [
            {
                "freeze_id": freeze_id,
                "feature_title": FEATURE_TITLE,
                "status": "frozen",
                "entry": "project_freeze_after_update/frozen_features_memory/entries/"
                + freeze_id
                + ".md",
            }
        ],
    }
    (memory / "freeze_index.json").write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    freeze_id = "freeze-20260708-aqr-correction-session-until-fresh-pass-v1"

    with tempfile.TemporaryDirectory(prefix="kanda_freeze_consumption_authority_") as temp:
        root = Path(temp)

        project, staging, patch_zip = _new_fixture(root, "orphan")
        save_freeze_hint_record(project, _hint(), source_signature=_signature(patch_zip))
        marked = mark_latest_freeze_hint_used(project, freeze_id=freeze_id)
        assert marked.get("ok"), marked
        recovered = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert recovered.get("ok"), recovered
        print("ORPHAN_FREEZE_ID_CONSUMPTION_DOES_NOT_BLOCK_CURRENT_HINT: PASS")

        project, staging, patch_zip = _new_fixture(root, "stale_index")
        save_freeze_hint_record(project, _hint(), source_signature=_signature(patch_zip))
        marked = mark_latest_freeze_hint_used(project, freeze_id=freeze_id)
        assert marked.get("ok"), marked
        _write_stale_index_only(project, freeze_id)
        recovered = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert recovered.get("ok"), recovered
        print("STALE_INDEX_ONLY_MATCH_DOES_NOT_CONSUME_HINT: PASS")

        project, staging, patch_zip = _new_fixture(root, "confirmed")
        save_freeze_hint_record(project, _hint(), source_signature=_signature(patch_zip))
        marked = mark_latest_freeze_hint_used(project, freeze_id=freeze_id)
        assert marked.get("ok"), marked
        _write_frozen_entry(project, freeze_id)
        blocked = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert not blocked.get("ok"), blocked
        assert patch_zip.name in blocked.get("skipped_consumed", []), blocked
        print("CONFIRMED_FROZEN_ENTRY_CONSUMPTION_REMAINS_BLOCKING: PASS")

        project, staging, patch_zip = _new_fixture(root, "ignored")
        save_freeze_hint_record(project, _hint(), source_signature=_signature(patch_zip))
        marked = mark_latest_freeze_hint_used(project, freeze_id="ignored-by-human")
        assert marked.get("ok"), marked
        blocked = scan_and_save_latest_freeze_hint(project, staging_dir=staging)
        assert not blocked.get("ok"), blocked
        assert patch_zip.name in blocked.get("skipped_consumed", []), blocked
        print("EXPLICIT_HUMAN_IGNORE_REMAINS_AUTHORITATIVE: PASS")

    print("FREEZE_CONSUMPTION_REQUIRES_CONFIRMED_ENTRY: PASS")
    print("VALIDATION OK: freeze-consumption-requires-confirmed-entry-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
