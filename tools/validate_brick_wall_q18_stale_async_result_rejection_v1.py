"""Validate Brick Wall Q18 stale asynchronous-result rejection."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import json
import re
from pathlib import Path
from typing import Callable, Sequence

from brick_wall_q18_stale_async_result_contract import (
    mutated_record,
    valid_not_applicable_record,
    valid_required_record,
    validate_record,
)

FEATURE_ID = "brick-wall-q18-stale-async-result-rejection-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / (
    "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_REL = PLIB / (
    "ACTIVE_PROMPTS/05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
Q17_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q17_preview_shadow_source_separation_v1.py"
)
Q18_CONTRACT_REL = Path("tools/brick_wall_q18_stale_async_result_contract.py")
Q18_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q18_stale_async_result_rejection_v1.py"
)
PIPELINE_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "main_workbench_pipeline.py"
)
PACKAGE_GUI_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "main_workbench_gui.py"
)
AQR_CONTROLLER_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "advanced_quality_review_qt_controller.py"
)
PLANNER_CANCEL_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "planner_background_cancel.py"
)
LOCAL_AI_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_local_ai_correction_qt_controller.py"
)
HEURISTIC_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_heuristic_correction_qt_controller.py"
)
DIFF_REVIEW_REL = Path(
    "kanda_reasoner_app/manage_architecture/large_file_refactor_planner/"
    "workbench_diff_review_assistant_gui.py"
)
LOCAL_AI_VALIDATOR_REL = Path(
    "tools/validate_workbench_local_ai_correction_qthread_bounded_runtime_v1.py"
)
DIFF_VALIDATOR_REL = Path(
    "tools/validate_workbench_assisted_diff_review_and_ui_cleanup_v1.py"
)
CORRECTION_VALIDATOR_REL = Path(
    "tools/validate_workbench_correction_route_reuse_and_aqr_sonar_v1.py"
)
AQR_GUI_VALIDATOR_REL = Path(
    "tools/validate_advanced_quality_review_gui_integration_v1.py"
)
CARD_VALIDATOR_REL = Path(
    "tools/validate_architecture_review_project_card_lifecycle_v1.py"
)

BRICK_MARKERS = (
    "### Stale asynchronous-result rejection (Q18)",
    "STALE ASYNCHRONOUS-RESULT REJECTION RECORD",
    "request and result identity fields",
    "cancellation revokes result authority",
    "timeout revokes result authority",
    "thread settlement remains distinct from cancel request",
    "stale results cannot mutate state, open gates, write source, write durable evidence, or repopulate current UI",
    "proceed to Q19 real Qt/QSignalSpy decision YES/NO",
    "Q18 never grants coding or source-write authority",
)
BRIDGE_MARKERS = (
    "## Stale asynchronous-result rejection gate (Q18)",
    "Q18 stale asynchronous-result rejection record complete: YES / NO",
    "May proceed to Q19 real Qt/QSignalSpy decision gate: YES / NO",
    "## Stale asynchronous-result rejection bridge",
    "stale result effects blocked",
    "Q18 never grants coding or source-write authority",
)
PIPELINE_MARKERS = (
    '"""Schedule existing Workbench stages and reject stale generations."""',
    "if job is None or job.generation != generation or job.stage != stage:",
    "if not self._accept_generation(generation):",
    "if not self._source_fresh():",
    "return bool(self._running and generation == self._generation)",
)
PACKAGE_MARKERS = (
    '"""Build one complete package off the GUI thread and quarantine stale results."""',
    "or generation != self._generation",
    "or job.generation != generation",
    "if self._cancel_requested:",
)
AQR_MARKERS = (
    '"""Own one QThread worker at a time and reject stale late results."""',
    '"accept_result": True',
    'self._progress_message = "Late result will be ignored."',
    "if generation != self._generation or not job or not job.get(\"accept_result\"):",
    "def _handle_thread_finished(self, generation: int) -> None:",
)
PLANNER_MARKERS = (
    "Cancel active split-plan or Local AI polling and reject late results.",
    "invalidates",
    "Late results will be ignored.",
    "invalidate its current request token",
)
LOCAL_AI_MARKERS = (
    '"accept_result": True',
    '"thread_finished": False',
    "late result will be ignored. No PASS was synthesized and no downstream",
    "if generation != int(",
    'job["accept_result"] = False',
    'job["thread_finished"] = True',
)
HEURISTIC_MARKERS = (
    '"accept_result": True',
    '"thread_finished": False',
    "The current worker result is stale and will be ignored.",
    "if generation != int(",
    'job["accept_result"] = False',
    'job["thread_finished"] = True',
)
DIFF_MARKERS = (
    "evidence_identity = _evidence_identity(evidence)",
    "self.result_ready.emit((self._evidence_identity, result))",
    "if evidence is None or _evidence_identity(evidence) != str(evidence_identity):",
    "The stale result was discarded.",
)
VALIDATOR_MARKERS = {
    LOCAL_AI_VALIDATOR_REL: (
        "LOCAL_AI_CORRECTION_TIMEOUT_CANCEL_LATE_RESULT_DISCARD: PASS",
        "WORKBENCH_LOCAL_AI_CORRECTION_QTHREAD_BOUNDED_RUNTIME: PASS",
    ),
    DIFF_VALIDATOR_REL: (
        "LOCAL_AI_DIFF_REVIEW_QTHREAD_AND_STALE_GUARD: PASS",
        "WORKBENCH_ASSISTED_DIFF_REVIEW_AND_UI_CLEANUP: PASS",
    ),
    CORRECTION_VALIDATOR_REL: (
        "CORRECTION_ROUTE_SWITCH_ABANDONS_PRIOR_WORKER_FAIL_CLOSED",
        "WORKBENCH_CORRECTION_ROUTE_REUSE_AND_AQR_SONAR: PASS",
    ),
    AQR_GUI_VALIDATOR_REL: (
        "AQR_CANCEL_RUNNING_UNTIL_THREAD_SETTLED: PASS",
        "AQR_GUI_CANCEL_LATE_RESULT_DISCARDED: PASS",
    ),
    CARD_VALIDATOR_REL: (
        "ROOT_CHANGE_UNLOADS_AST_PLANNER_WORKBENCH: PASS",
        "RUNNING_AUDIT_BLOCKS_PROJECT_CARD_SWITCH: PASS",
        "ARCHITECTURE_REVIEW_CARD_MACHINE_LIFECYCLE: PASS",
    ),
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        suffix = " - " + detail if detail else ""
        raise AssertionError(label + ": FAIL" + suffix)
    print(label + ": PASS")


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _parse_version(value: object) -> tuple[int, ...]:
    if not isinstance(value, str):
        return ()
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError:
        return ()


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q18_BRICK_WALL_CONTRACT")
    precode = re.search(
        r"After Q(\d+), all applicable pre-code items",
        brick,
    )
    coverage = re.search(r"Q01-Q(\d+) complete YES/NO", brick)
    _gate(
        "Q18_FORWARD_COMPATIBLE_Q19_PRECODE_PROGRESSION",
        precode is not None
        and coverage is not None
        and int(precode.group(1)) >= 18
        and int(coverage.group(1)) >= 18,
    )
    _require(bridge, BRIDGE_MARKERS, "Q18_ROUTER_BRIDGE_CONTRACT")
    _require(_read(root / PIPELINE_REL), PIPELINE_MARKERS, "Q18_MAIN_PIPELINE_GUARDS")
    _require(_read(root / PACKAGE_GUI_REL), PACKAGE_MARKERS, "Q18_PACKAGE_RESULT_GUARDS")
    _require(_read(root / AQR_CONTROLLER_REL), AQR_MARKERS, "Q18_AQR_GENERATION_GUARDS")
    _require(_read(root / PLANNER_CANCEL_REL), PLANNER_MARKERS, "Q18_PLANNER_CANCEL_GUARDS")
    _require(_read(root / LOCAL_AI_REL), LOCAL_AI_MARKERS, "Q18_LOCAL_AI_GENERATION_GUARDS")
    _require(_read(root / HEURISTIC_REL), HEURISTIC_MARKERS, "Q18_HEURISTIC_GENERATION_GUARDS")
    _require(_read(root / DIFF_REVIEW_REL), DIFF_MARKERS, "Q18_EVIDENCE_IDENTITY_GUARD")
    for rel, markers in VALIDATOR_MARKERS.items():
        _require(_read(root / rel), markers, "Q18_EXISTING_VALIDATOR_CONTRACT")
    _gate("Q18_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (2, 8))
    _gate("Q18_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (3, 2))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q18_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)
    q17 = _read(root / Q17_VALIDATOR_REL)
    _gate(
        "Q17_FORWARD_COMPATIBLE_Q18_PROGRESSION",
        "proceed to Q18 stale async-result rejection YES/NO" in q17
        and '_parse_version(brick_meta.get("version")) >= (2, 7)' in q17
        and '_parse_version(bridge_meta.get("version")) >= (3, 1)' in q17,
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q17_VALIDATOR_REL,
        Q18_CONTRACT_REL,
        Q18_VALIDATOR_REL,
        PIPELINE_REL,
        PACKAGE_GUI_REL,
        AQR_CONTROLLER_REL,
        LOCAL_AI_REL,
        HEURISTIC_REL,
        DIFF_REVIEW_REL,
    ):
        lines = len(_read(root / rel).splitlines())
        _gate("Q18_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


def _reject(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
        return
    _gate(label, False, "invalid record was accepted")


def validate_semantics() -> None:
    validate_record(valid_required_record())
    _gate("Q18_REQUIRED_ASYNC_RECORD_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q18_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        (
            "Q18_NEGATIVE_DUPLICATE_ROUTE",
            lambda record: record["routes"].append(dict(record["routes"][0])),
        ),
        (
            "Q18_NEGATIVE_REQUEST_IDENTITY_INCOMPLETE",
            lambda record: record["routes"][0]["request_identity_fields"].remove(
                "active_project_root"
            ),
        ),
        (
            "Q18_NEGATIVE_RESULT_IDENTITY_INCOMPLETE",
            lambda record: record["routes"][0]["result_identity_fields"].remove(
                "source_fingerprint"
            ),
        ),
        (
            "Q18_NEGATIVE_GENERATION_MISSING",
            lambda record: record["routes"][0].update(worker_generation=0),
        ),
        (
            "Q18_NEGATIVE_ACCEPTANCE_PREDICATE_INCOMPLETE",
            lambda record: record["routes"][0].update(
                acceptance_predicate="worker_generation and accept_result"
            ),
        ),
        (
            "Q18_NEGATIVE_CANCEL_AUTHORITY_RETAINED",
            lambda record: record["routes"][0].update(
                cancellation_revokes_authority=False
            ),
        ),
        (
            "Q18_NEGATIVE_TIMEOUT_AUTHORITY_RETAINED",
            lambda record: record["routes"][0].update(
                timeout_revokes_authority=False
            ),
        ),
        (
            "Q18_NEGATIVE_THREAD_SETTLEMENT_UNTRACKED",
            lambda record: record["routes"][0].update(
                thread_settlement_tracked=False
            ),
        ),
        (
            "Q18_NEGATIVE_LATE_RESULT_ACCEPTED",
            lambda record: record["routes"][0].update(
                late_result_action="APPLY"
            ),
        ),
        (
            "Q18_NEGATIVE_STALE_STATE_MUTATION",
            lambda record: record["routes"][0]["stale_effects_blocked"].remove(
                "state_mutation"
            ),
        ),
        (
            "Q18_NEGATIVE_STALE_GATE_OPEN",
            lambda record: record["routes"][0]["stale_effects_blocked"].remove(
                "gate_open"
            ),
        ),
        (
            "Q18_NEGATIVE_STALE_SOURCE_WRITE",
            lambda record: record["routes"][0]["stale_effects_blocked"].remove(
                "source_write"
            ),
        ),
        (
            "Q18_NEGATIVE_STALE_EVIDENCE_WRITE",
            lambda record: record["routes"][0]["stale_effects_blocked"].remove(
                "durable_evidence_write"
            ),
        ),
        (
            "Q18_NEGATIVE_STALE_UI_REPOPULATION",
            lambda record: record["routes"][0]["stale_effects_blocked"].remove(
                "current_ui_repopulation"
            ),
        ),
        (
            "Q18_NEGATIVE_Q19_PROGRESSION",
            lambda record: record.update(may_proceed_to_q19=False),
        ),
        (
            "Q18_NEGATIVE_CODING_AUTHORIZATION",
            lambda record: record.update(may_begin_coding=True),
        ),
        (
            "Q18_NEGATIVE_SOURCE_WRITE_AUTHORIZATION",
            lambda record: record.update(may_write_source=True),
        ),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    invalid = valid_not_applicable_record()
    invalid["no_async_evidence"] = []
    try:
        validate_record(invalid)
    except AssertionError:
        _gate("Q18_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q18_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    _gate("Q18_STALE_ASYNC_RESULT_REJECTION_REGRESSION_SET", True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()
    validate_source(root)
    validate_semantics()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
