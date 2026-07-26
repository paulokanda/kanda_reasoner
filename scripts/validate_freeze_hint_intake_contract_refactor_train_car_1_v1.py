"""Validate Freeze Hint Intake Contract Refactor Train Car 1 v1."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
import tempfile
import zipfile

__all__: list[str] = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)

PACKAGE_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_hint_intake"
CONTRACT = PACKAGE_ROOT / "contract.py"
FEATURE_ID = "freeze-hint-intake-contract-refactor-train-car-1-v1"

REQUIRED_PUBLIC = [
    "build_freeze_form_inputs_from_latest_hint",
    "build_freeze_hint_intake_paths",
    "FreezeHintIntakeError",
    "FreezeHintIntakePaths",
    "load_latest_freeze_hint_record",
    "mark_latest_freeze_hint_used",
    "merge_validation_evidence_into_latest_hint",
    "read_freeze_hint_from_patch_zip",
    "resolve_freeze_hint_autofill_state",
    "save_freeze_hint_record",
    "scan_and_save_latest_freeze_hint",
]

REQUIRED_COMPAT_PRIVATE = [
    "_safe_slug",
    "_normalize_hint",
    "_find_matching_frozen_feature",
    "_load_consumed",
    "_select_preview_snapshot",
    "_resolve_project_root",
    "_atomic_write_json",
]

EXPECTED_MODULES = {
    "contract.py",
    "models.py",
    "paths_io.py",
    "form_normalization.py",
    "frozen_matching.py",
    "records.py",
    "consumed_hints.py",
    "scanner.py",
    "autofill.py",
}


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def _assert_line_policy() -> None:
    assert _line_count(CONTRACT) <= 180, "contract.py must remain a thin compatibility facade"
    for name in EXPECTED_MODULES:
        path = PACKAGE_ROOT / name
        assert path.exists(), f"missing freeze hint intake module: {name}"
        count = _line_count(path)
        assert count <= 500, f"{name} exceeds v7.2 hard maximum: {count} lines"
        if name not in {"contract.py", "models.py"}:
            assert count >= 80, f"{name} is too tiny for v7.2 refactor policy: {count} lines"


def _assert_public_surface() -> None:
    contract = importlib.import_module("kanda_reasoner_app.freeze_hint_intake.contract")
    assert list(contract.__all__) == REQUIRED_PUBLIC, "public __all__ changed"
    for name in REQUIRED_PUBLIC:
        assert hasattr(contract, name), f"missing public API: {name}"
    for name in REQUIRED_COMPAT_PRIVATE:
        assert hasattr(contract, name), f"missing compatibility private helper: {name}"
    assert contract._safe_slug("Freeze ABC_123") == "freeze-abc-123"


def _assert_behavior_smoke() -> None:
    contract = importlib.import_module("kanda_reasoner_app.freeze_hint_intake.contract")
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "sample_project"
        project.mkdir()
        hint = {
            "kind": "kanda_freeze_hint",
            "feature_title": "Freeze Hint Intake Contract Refactor Train Car 1 v1",
            "primary_box": "kanda_reasoner_app/freeze_hint_intake/contract.py",
            "box_type": "python-freeze-intake-refactor",
            "validated_files": ["kanda_reasoner_app/freeze_hint_intake/contract.py"],
            "protected_paths": ["kanda_reasoner_app/freeze_hint_intake"],
            "do_not_regress_rules": ["Keep public freeze hint intake API available."],
            "validation_evidence_summary": "VALIDATION OK: " + FEATURE_ID + "\nSTATUS: IN_SYNC",
        }
        record = contract.save_freeze_hint_record(
            project,
            hint,
            source_signature={
                "source_name": "sample_patch.zip",
                "source_mtime_ns": 1,
                "source_size_bytes": 2,
            },
        )
        assert record["form_inputs"]["feature_title"] == hint["feature_title"]
        loaded = contract.load_latest_freeze_hint_record(project)
        assert loaded.get("ok"), loaded
        fallback = {key: "" for key in contract.FORM_KEYS}
        state = contract.resolve_freeze_hint_autofill_state(project, fallback)
        assert state.get("ok"), state
        assert state.get("confirm_write_enabled"), state
        merged = contract.merge_validation_evidence_into_latest_hint(
            project,
            "VALIDATION OK: " + FEATURE_ID + "\nSTATUS: IN_SYNC",
            feature_id=FEATURE_ID,
        )
        assert merged.get("ok"), merged
        used = contract.mark_latest_freeze_hint_used(
            project,
            freeze_id="freeze-20260630-" + FEATURE_ID,
        )
        assert used.get("ok"), used


def _assert_zip_reader() -> None:
    contract = importlib.import_module("kanda_reasoner_app.freeze_hint_intake.contract")
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "sample.zip"
        hint = {
            "kind": "kanda_freeze_hint",
            "feature_title": "Zip Reader Smoke",
            "primary_box": "kanda_reasoner_app/freeze_hint_intake/contract.py",
            "box_type": "python-freeze-intake-refactor",
            "validated_files": "kanda_reasoner_app/freeze_hint_intake/contract.py",
            "protected_paths": "kanda_reasoner_app/freeze_hint_intake",
            "do_not_regress_rules": "Keep zip sidecar reader working.",
            "validation_evidence_summary": "VALIDATION OK: " + FEATURE_ID,
        }
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, ensure_ascii=True))
        loaded = contract.read_freeze_hint_from_patch_zip(zip_path)
        assert loaded["feature_id"] == "zip-reader-smoke"
        assert loaded["source"]["source_name"] == "sample.zip"


def main() -> int:
    _ensure_project_root_on_path()
    _assert_line_policy()
    _assert_public_surface()
    _assert_behavior_smoke()
    _assert_zip_reader()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
