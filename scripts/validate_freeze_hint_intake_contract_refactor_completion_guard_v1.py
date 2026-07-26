"""Validate Freeze Hint Intake Contract Refactor Completion Guard v1.

This guard intentionally does not split more files. Under the active v7.2
large-module protocol, the post Train Car 1 freeze_hint_intake package is
already a cohesive helper family: no helper exceeds 500 lines, substantive
helpers sit in a practical size band, and contract.py is a thin public facade.
"""

from __future__ import annotations

import importlib
import json
import sys
import tempfile
import zipfile
from pathlib import Path

__all__: list[str] = []


PROJECT_ROOT = Path(__file__).resolve().parents[1]

def _ensure_project_root_on_path() -> None:
    """Add the project root to sys.path only for direct script execution."""
    root_text = str(PROJECT_ROOT)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)


PACKAGE_ROOT = PROJECT_ROOT / "kanda_reasoner_app" / "freeze_hint_intake"
FEATURE_ID = "freeze-hint-intake-contract-refactor-completion-guard-v1"

EXPECTED_MODULES = {
    "contract.py": {"max": 180, "allow_small": True},
    "models.py": {"max": 220, "allow_small": True},
    "paths_io.py": {"max": 220, "allow_small": False},
    "form_normalization.py": {"max": 400, "allow_small": False},
    "frozen_matching.py": {"max": 320, "allow_small": False},
    "records.py": {"max": 400, "allow_small": False},
    "consumed_hints.py": {"max": 220, "allow_small": False},
    "scanner.py": {"max": 260, "allow_small": False},
    "autofill.py": {"max": 360, "allow_small": False},
}

EXPECTED_PUBLIC = [
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

EXPECTED_COMPAT_PRIVATE = [
    "_safe_slug",
    "_normalize_hint",
    "_find_matching_frozen_feature",
    "_load_consumed",
    "_select_preview_snapshot",
    "_resolve_project_root",
    "_atomic_write_json",
]

EXPECTED_OWNERSHIP = {
    "contract.py": ["Public contract for freeze hint intake records", "__all__"],
    "form_normalization.py": ["_normalize_hint", "_normalize_form_inputs", "_clean_stale_pending_text_after_local_validation"],
    "records.py": ["save_freeze_hint_record", "load_latest_freeze_hint_record", "merge_validation_evidence_into_latest_hint"],
    "consumed_hints.py": ["_remember_consumed_hint", "_is_consumed", "_load_consumed"],
    "scanner.py": ["read_freeze_hint_from_patch_zip", "scan_and_save_latest_freeze_hint"],
    "autofill.py": ["resolve_freeze_hint_autofill_state"],
    "paths_io.py": ["build_freeze_hint_intake_paths", "_atomic_write_json", "_resolve_project_root"],
    "frozen_matching.py": ["_find_matching_frozen_feature", "_find_matching_frozen_feature_in_entry_files"],
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(_read(path).splitlines())


def _assert_v72_line_policy() -> None:
    assert PACKAGE_ROOT.exists(), "freeze_hint_intake package missing"
    for name, policy in EXPECTED_MODULES.items():
        path = PACKAGE_ROOT / name
        assert path.exists(), f"missing expected module: {name}"
        count = _line_count(path)
        assert count <= 500, f"{name} exceeds v7.2 hard maximum: {count} lines"
        assert count <= policy["max"], f"{name} exceeds completion guard target: {count} > {policy['max']}"
        if not policy.get("allow_small"):
            assert count >= 80, f"{name} is below v7.2 substantive-helper lower band: {count} lines"
    all_py = {p.name for p in PACKAGE_ROOT.glob("*.py") if p.name != "__init__.py"}
    assert EXPECTED_MODULES.keys() <= all_py, "expected helper module set not present"


def _assert_no_tiny_helper_sprawl() -> None:
    tiny = []
    for path in PACKAGE_ROOT.glob("*.py"):
        if path.name == "__init__.py":
            continue
        count = _line_count(path)
        if count < 80 and path.name not in {"contract.py"}:
            tiny.append(f"{path.name}:{count}")
    assert not tiny, "unexpected tiny helper modules under v7.2: " + ", ".join(tiny)


def _assert_ownership_markers() -> None:
    for name, markers in EXPECTED_OWNERSHIP.items():
        text = _read(PACKAGE_ROOT / name)
        for marker in markers:
            assert marker in text, f"{name} missing ownership marker/function: {marker}"


def _assert_public_contract_surface() -> None:
    contract = importlib.import_module("kanda_reasoner_app.freeze_hint_intake.contract")
    assert list(contract.__all__) == EXPECTED_PUBLIC, "contract public __all__ changed"
    for name in EXPECTED_PUBLIC:
        assert hasattr(contract, name), f"contract.py missing public API: {name}"
    for name in EXPECTED_COMPAT_PRIVATE:
        assert hasattr(contract, name), f"contract.py missing compatibility private helper: {name}"
    assert contract._safe_slug("Freeze Hint Intake Completion Guard v1") == "freeze-hint-intake-completion-guard-v1"


def _assert_behavior_smoke() -> None:
    contract = importlib.import_module("kanda_reasoner_app.freeze_hint_intake.contract")
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "sample_project"
        project.mkdir()
        hint = {
            "kind": "kanda_freeze_hint",
            "feature_title": "Freeze Hint Intake Contract Refactor Completion Guard v1",
            "primary_box": "kanda_reasoner_app/freeze_hint_intake/contract.py",
            "box_type": "python-freeze-intake-refactor-completion-guard",
            "validated_files": ["kanda_reasoner_app/freeze_hint_intake/contract.py"],
            "protected_paths": ["kanda_reasoner_app/freeze_hint_intake"],
            "do_not_regress_rules": ["Keep freeze hint intake contract facade and helper ownership stable."],
            "validation_evidence_summary": "VALIDATION OK: " + FEATURE_ID + "\nSTATUS: IN_SYNC",
        }
        record = contract.save_freeze_hint_record(
            project,
            hint,
            source_signature={
                "source_name": "completion_guard_patch.zip",
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
            feature_title="Freeze Hint Intake Contract Refactor Completion Guard v1",
        )
        assert merged.get("ok"), merged
        used = contract.mark_latest_freeze_hint_used(
            project,
            freeze_id="freeze-20260630-" + FEATURE_ID,
        )
        assert used.get("ok"), used


def _assert_zip_reader_smoke() -> None:
    contract = importlib.import_module("kanda_reasoner_app.freeze_hint_intake.contract")
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "sample.zip"
        hint = {
            "kind": "kanda_freeze_hint",
            "feature_title": "Completion Guard Zip Reader Smoke",
            "primary_box": "kanda_reasoner_app/freeze_hint_intake/contract.py",
            "box_type": "python-freeze-intake-refactor-completion-guard",
            "validated_files": "kanda_reasoner_app/freeze_hint_intake/contract.py",
            "protected_paths": "kanda_reasoner_app/freeze_hint_intake",
            "do_not_regress_rules": "Keep root freeze hint ZIP reader working.",
            "validation_evidence_summary": "VALIDATION OK: " + FEATURE_ID,
        }
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("KANDA_FREEZE_HINT.json", json.dumps(hint, ensure_ascii=True))
        loaded = contract.read_freeze_hint_from_patch_zip(zip_path)
        assert loaded["feature_id"] == "completion-guard-zip-reader-smoke"
        assert loaded["source"]["source_name"] == "sample.zip"


def main() -> int:
    _ensure_project_root_on_path()
    _assert_v72_line_policy()
    _assert_no_tiny_helper_sprawl()
    _assert_ownership_markers()
    _assert_public_contract_surface()
    _assert_behavior_smoke()
    _assert_zip_reader_smoke()
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
