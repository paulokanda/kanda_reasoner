"""Validate Brick Wall Q11 observer-only MCard lifecycle enforcement."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Mapping

__all__: list[str] = []

FEATURE_ID = "brick-wall-q11-mcard-observer-lifecycle-enforcement-v2"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/brick_wall_comprehensive_quality_gate.md"
MCARD_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/architecture_review_project_card_machine_canon.md"
BOUNDARY_REL = PLIB / "ACTIVE_PROMPTS/12_generalized_project_canons/project_tool_boundary_canon.md"
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
MCARD_META_REL = PLIB / "METADATA/architecture_review_project_card_machine_canon.meta.json"

VALID_TRANSITIONS = {
    ("EMPTY", "CARD_INSERTED"),
    ("CARD_INSERTED", "CARD_READ"),
    ("CARD_READ", "OBSERVED"),
    ("OBSERVED", "ANALYSIS_READY"),
    ("ANALYSIS_READY", "REPORT_READY"),
    ("CARD_INSERTED", "CARD_EJECTED"),
    ("CARD_READ", "CARD_EJECTED"),
    ("OBSERVED", "CARD_EJECTED"),
    ("ANALYSIS_READY", "CARD_EJECTED"),
    ("REPORT_READY", "CARD_EJECTED"),
}
OBSERVER_STATES = {
    "EMPTY", "CARD_INSERTED", "CARD_READ", "OBSERVED",
    "ANALYSIS_READY", "REPORT_READY", "CARD_EJECTED",
}
RETIRED_EXTERNAL_PROJECT_STATES = {
    "AUTHORIZED", "APPLYING", "APPLIED_NOT_VERIFIED",
    "ROLLBACK_REQUESTED", "ROLLBACK_VERIFIED", "VERIFIED_TERMINAL",
}


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError("missing file: " + str(path))
    return path.read_text(encoding="utf-8-sig", errors="strict")


def _load(path: Path) -> dict[str, object]:
    data = json.loads(_read(path))
    if not isinstance(data, dict):
        raise AssertionError("JSON root must be object: " + str(path))
    return data


def _version(value: object) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError:
        return ()


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise AssertionError(label + ": FAIL" + (" - " + detail if detail else ""))
    print(label + ": PASS" + (" - " + detail if detail else ""))


def transition_allowed(before: str, after: str) -> bool:
    return (before, after) in VALID_TRANSITIONS


def validate_record(record: Mapping[str, object]) -> None:
    required = {
        "mcard_applicable", "current_lifecycle_phase", "transition_from",
        "transition_to", "transition_allowed", "lifecycle_generation_current",
        "async_generation_current", "project_source_write_requested",
        "project_release_authority_requested", "kanda_dependency_required",
        "project_results_retained_after_eject", "decision",
        "may_proceed_to_q12", "may_begin_coding",
    }
    missing = sorted(required - set(record))
    if missing:
        raise AssertionError("record missing fields: " + ", ".join(missing))
    if record["decision"] not in {"COMPLETE", "NOT_APPLICABLE", "BLOCKED"}:
        raise AssertionError("invalid decision")
    if record["may_begin_coding"]:
        raise AssertionError("Q11 cannot authorize coding")
    if not record["mcard_applicable"]:
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("non-applicable record must be NOT_APPLICABLE")
        return
    before = str(record["transition_from"])
    after = str(record["transition_to"])
    expected = transition_allowed(before, after)
    if bool(record["transition_allowed"]) != expected:
        raise AssertionError("transition decision drift")
    if not record["lifecycle_generation_current"] or not record["async_generation_current"]:
        if record["decision"] != "BLOCKED":
            raise AssertionError("stale generation must block observation result")
        return
    if record["project_source_write_requested"]:
        raise AssertionError("external Project source write is unsupported")
    if record["project_release_authority_requested"]:
        raise AssertionError("KANDA cannot own external Project release authority")
    if record["kanda_dependency_required"]:
        raise AssertionError("external Project development cannot require KANDA")
    if after == "CARD_EJECTED" and not record["project_results_retained_after_eject"]:
        raise AssertionError("card eject cannot destroy Project-owned results")
    if not expected or record["decision"] != "COMPLETE" or not record["may_proceed_to_q12"]:
        raise AssertionError("applicable observer record incomplete")


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    mcard = _read(root / MCARD_REL)
    boundary = _read(root / BOUNDARY_REL)
    for marker in (
        "### MCard applicability and lifecycle (Q11)",
        "MCard observer lifecycle enforcement",
        "no Project apply/rollback",
    ):
        _gate("Q11_BRICK_MARKER", marker in brick, marker)
    for marker in (
        "## Observer lifecycle state machine",
        "CARD_INSERTED", "CARD_READ", "OBSERVED", "ANALYSIS_READY",
        "REPORT_READY", "CARD_EJECTED", "No Project source rollback",
        "Project development remains possible when KANDA is closed",
    ):
        _gate("Q11_MCARD_MARKER", marker in mcard, marker)
    for retired in RETIRED_EXTERNAL_PROJECT_STATES:
        _gate("Q11_RETIRED_STATE_NOT_ACTIVE", ("-> " + retired) not in mcard, retired)
    for marker in (
        "KANDA_OBSERVER_ACTOR", "PROJECT_ACTOR",
        "never request KANDA Tool source or `kanda_reasoner__source_archive_partXX_of_YY.zip`",
        "scripts/validate_patch_zip.py",
    ):
        _gate("Q11_BOUNDARY_MARKER", marker in boundary, marker)
    _gate("Q11_BRICK_WITHIN_LIMIT", len(brick.splitlines()) <= 500)
    _gate("Q11_MCARD_WITHIN_LIMIT", len(mcard.splitlines()) <= 500)
    brick_meta = _load(root / BRICK_META_REL)
    mcard_meta = _load(root / MCARD_META_REL)
    _gate("Q11_BRICK_VERSION", _version(brick_meta.get("version")) >= (3, 23))
    _gate("Q11_MCARD_VERSION", _version(mcard_meta.get("version")) >= (3, 0))


def run_validation(root: Path) -> None:
    validate_source(root)
    good = {
        "mcard_applicable": True,
        "current_lifecycle_phase": "OBSERVED",
        "transition_from": "OBSERVED",
        "transition_to": "ANALYSIS_READY",
        "transition_allowed": True,
        "lifecycle_generation_current": True,
        "async_generation_current": True,
        "project_source_write_requested": False,
        "project_release_authority_requested": False,
        "kanda_dependency_required": False,
        "project_results_retained_after_eject": True,
        "decision": "COMPLETE",
        "may_proceed_to_q12": True,
        "may_begin_coding": False,
    }
    validate_record(good)
    _gate("Q11_OBSERVER_RECORD_ACCEPTED", True)
    for field in ("project_source_write_requested", "project_release_authority_requested", "kanda_dependency_required"):
        bad = dict(good)
        bad[field] = True
        try:
            validate_record(bad)
        except AssertionError:
            _gate("Q11_NEGATIVE_" + field.upper(), True)
        else:
            _gate("Q11_NEGATIVE_" + field.upper(), False)
    print("MCARD_OBSERVER_LIFECYCLE: PASS")
    print("EXTERNAL_PROJECT_KANDA_DEPENDENCY: DENIED")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    run_validation(args.project_root.expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
