"""Validation-only Brick Wall Q29 NO-LEAK runtime trace pilot contract."""
from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Mapping

__all__: list[str] = []
FEATURE_ID = "brick-wall-q29-no-leak-runtime-trace-pilot-decision-enforcement-v1"
ACTIONS = (
    "writes",
    "deletes",
    "replacements",
    "archive_operations",
    "subprocesses",
    "imports",
)
DECISIONS = ("PILOT_RETAINED", "PILOT_REJECTED", "NOT_APPLICABLE", "BLOCKED")
REQUIRED_FIELDS = (
    "pilot_applicable",
    "no_pilot_evidence",
    "q28_decision_complete",
    "primary_box",
    "canonical_owners",
    "runtime_collector_relationship",
    "pilot_kind",
    "dependency_scope",
    "isolation_strategy",
    "replay_strategy",
    "bounds",
    "observed_actions",
    "synthetic_categories",
    "q20_categories",
    "relative_path_attribution_unresolved",
    "relative_path_attribution_runtime_observed",
    "relative_path_attribution_evidence_mode",
    "child_process_side_effects_unobserved",
    "security_sandbox_claimed",
    "application_runtime_integration",
    "unique_meaningful_defects",
    "known_or_duplicate_findings",
    "false_assurance_risks",
    "measurable_gain",
    "operational_cost",
    "broader_adoption_decision",
    "validators",
    "expected_markers",
    "unresolved_fields",
    "decision",
    "may_proceed_to_q30",
    "may_begin_coding",
    "may_write_source",
)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _texts(value: object, *, empty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (empty or bool(value))
        and all(_text(item) for item in value)
    )


def _run_probe(project_root: Path, mode: str, output: Path) -> dict[str, object]:
    probe = project_root / "tools/brick_wall_q29_runtime_trace_probe.py"
    command = [
        sys.executable,
        str(probe),
        "--mode",
        mode,
        "--output",
        str(output),
    ]
    if mode == "q20":
        command.extend(("--project-root", str(project_root)))
    env = dict(os.environ)
    env["PYTHONPATH"] = str(project_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command,
        cwd=str(project_root),
        text=True,
        encoding="utf-8",
        errors="strict",
        capture_output=True,
        env=env,
        timeout=60,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            "Q29 probe failed: " + (result.stdout or "") + (result.stderr or "")
        )
    data = json.loads(output.read_text(encoding="utf-8"))
    if data.get("status") != "PASS":
        raise AssertionError("Q29 probe reported failure")
    return data


def _categories(data: Mapping[str, object]) -> list[str]:
    events = data.get("events")
    if not isinstance(events, list):
        return []
    return sorted(
        {
            str(event.get("category"))
            for event in events
            if isinstance(event, Mapping) and _text(event.get("category"))
        }
    )


def classify_relative_path_attribution(
    runtime_events: object,
    model_events: object,
) -> tuple[bool, bool, str]:
    """Classify deterministic limitation evidence and optional runtime occurrence."""

    def unresolved(events: object) -> bool:
        if not isinstance(events, list):
            return False
        return any(
            isinstance(event, Mapping)
            and (
                event.get("path_attribution")
                == "DIR_FD_RELATIVE_UNRESOLVED"
                or (
                    isinstance(event.get("source"), Mapping)
                    and event["source"].get("path_attribution")
                    == "DIR_FD_RELATIVE_UNRESOLVED"
                )
                or (
                    isinstance(event.get("target"), Mapping)
                    and event["target"].get("path_attribution")
                    == "DIR_FD_RELATIVE_UNRESOLVED"
                )
            )
            for event in events
        )

    modeled = unresolved(model_events)
    runtime_observed = unresolved(runtime_events)
    mode = (
        "RUNTIME_AND_DETERMINISTIC_MODEL"
        if runtime_observed
        else "DETERMINISTIC_MODEL_ONLY_PLATFORM_DEPENDENT_RUNTIME"
    )
    return modeled, runtime_observed, mode


def run_bounded_pilot(project_root: Path) -> dict[str, object]:
    """Run the child-process pilot and return decision-relevant evidence."""
    root = project_root.expanduser().resolve(strict=True)
    with TemporaryDirectory(prefix="kanda_q29_pilot_") as raw:
        temp = Path(raw)
        synthetic = _run_probe(root, "synthetic", temp / "synthetic.json")
        q20 = _run_probe(root, "q20", temp / "q20.json")
        attribution_model = _run_probe(
            root,
            "attribution_model",
            temp / "attribution_model.json",
        )
    q20_events = q20.get("events")
    model_events = attribution_model.get("events")
    modeled, runtime_observed, evidence_mode = classify_relative_path_attribution(
        q20_events,
        model_events,
    )
    return {
        "synthetic_categories": _categories(synthetic),
        "q20_categories": _categories(q20),
        "relative_path_attribution_unresolved": modeled,
        "relative_path_attribution_runtime_observed": runtime_observed,
        "relative_path_attribution_evidence_mode": evidence_mode,
        "child_process_side_effects_unobserved": True,
        "unique_meaningful_defects": [],
        "known_or_duplicate_findings": [
            "Q20 sandbox writes and cleanup were observed but are already protected by Q20 snapshots and containment assertions."
        ],
        "false_assurance_risks": [
            "dir_fd-relative cleanup events cannot be attributed portably to an absolute path",
            "a parent audit hook observes subprocess launch but not every side effect inside the child process",
            "Python audit events are observability evidence and not a security boundary",
        ],
    }


def validate_record(record: Mapping[str, object]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise AssertionError("Q29 record missing fields: " + ", ".join(missing))
    for field in (
        "pilot_applicable",
        "q28_decision_complete",
        "relative_path_attribution_unresolved",
        "relative_path_attribution_runtime_observed",
        "child_process_side_effects_unobserved",
        "security_sandbox_claimed",
        "application_runtime_integration",
        "may_proceed_to_q30",
        "may_begin_coding",
        "may_write_source",
    ):
        if not isinstance(record[field], bool):
            raise AssertionError("Q29 invalid boolean: " + field)
    if record["decision"] not in DECISIONS:
        raise AssertionError("Q29 invalid decision")
    if record["decision"] == "BLOCKED" or record["unresolved_fields"]:
        raise AssertionError("Q29 remains blocked")
    if not record["may_proceed_to_q30"]:
        raise AssertionError("Q30 progression not approved")
    if record["may_begin_coding"] or record["may_write_source"]:
        raise AssertionError("Q29 cannot authorize coding or source writes")
    if record["security_sandbox_claimed"]:
        raise AssertionError("Q29 must not claim a security sandbox")
    if record["application_runtime_integration"]:
        raise AssertionError("Q29 pilot must not integrate with application runtime")
    if not record["pilot_applicable"]:
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("Q29 N/A decision incomplete")
        if not _texts(record["no_pilot_evidence"]):
            raise AssertionError("Q29 N/A evidence incomplete")
        return
    if not record["q28_decision_complete"]:
        raise AssertionError("Q28 baseline incomplete")
    if record["decision"] not in {"PILOT_RETAINED", "PILOT_REJECTED"}:
        raise AssertionError("Q29 applicable decision incomplete")
    if record["no_pilot_evidence"]:
        raise AssertionError("Q29 applicable record carries N/A evidence")
    for field in (
        "primary_box",
        "runtime_collector_relationship",
        "pilot_kind",
        "dependency_scope",
        "isolation_strategy",
        "replay_strategy",
        "measurable_gain",
        "operational_cost",
        "broader_adoption_decision",
        "relative_path_attribution_evidence_mode",
    ):
        if not _text(record[field]):
            raise AssertionError("Q29 text field incomplete: " + field)
    if record["dependency_scope"] != "STANDARD_LIBRARY_VALIDATION_ONLY_NO_RUNTIME_INTEGRATION":
        raise AssertionError("Q29 escaped validation-only scope")
    if set(record["observed_actions"]) != set(ACTIONS):
        raise AssertionError("Q29 action inventory drift")
    if not _texts(record["canonical_owners"]):
        raise AssertionError("Q29 owner inventory incomplete")
    if not _texts(record["synthetic_categories"]):
        raise AssertionError("Q29 synthetic categories missing")
    if not _texts(record["q20_categories"]):
        raise AssertionError("Q29 Q20 categories missing")
    if not _texts(record["validators"]) or not _texts(record["expected_markers"]):
        raise AssertionError("Q29 validation evidence incomplete")
    bounds = record["bounds"]
    if not isinstance(bounds, Mapping):
        raise AssertionError("Q29 bounds missing")
    if int(bounds.get("max_events", 0)) <= 0 or int(bounds.get("max_events", 0)) > 10000:
        raise AssertionError("Q29 event bound invalid")
    if int(bounds.get("timeout_seconds", 0)) <= 0 or int(bounds.get("timeout_seconds", 0)) > 120:
        raise AssertionError("Q29 timeout bound invalid")
    defects = record["unique_meaningful_defects"]
    if not isinstance(defects, list):
        raise AssertionError("Q29 defects must be a list")
    if record["decision"] == "PILOT_RETAINED":
        if not defects:
            raise AssertionError("Q29 retained without unique defect")
        if record["false_assurance_risks"]:
            raise AssertionError("Q29 retained despite unresolved assurance risks")
        if record["broader_adoption_decision"] != "RETAIN_BOUNDED_HIGH_RISK_VALIDATION_ONLY":
            raise AssertionError("Q29 retained scope invalid")
    else:
        if defects:
            raise AssertionError("Q29 rejected despite unique defects")
        if not record["relative_path_attribution_unresolved"]:
            raise AssertionError("Q29 rejected without deterministic attribution limitation evidence")
        if record["relative_path_attribution_evidence_mode"] not in {
            "RUNTIME_AND_DETERMINISTIC_MODEL",
            "DETERMINISTIC_MODEL_ONLY_PLATFORM_DEPENDENT_RUNTIME",
        }:
            raise AssertionError("Q29 attribution evidence mode invalid")
        if not _texts(record["known_or_duplicate_findings"]):
            raise AssertionError("Q29 rejected without duplicate-finding evidence")
        if not _texts(record["false_assurance_risks"]):
            raise AssertionError("Q29 rejected without limitation evidence")
        if record["broader_adoption_decision"] != "REJECT_BROADER_ADOPTION":
            raise AssertionError("Q29 rejection decision invalid")


def _base(result: Mapping[str, object]) -> dict[str, object]:
    return {
        "pilot_applicable": True,
        "no_pilot_evidence": [],
        "q28_decision_complete": True,
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "canonical_owners": [
            "Q20 shared isolated filesystem fixtures",
            "Q21 parametrized negative boundary matrix",
            "NO_LEAK_LOGIC_V1",
        ],
        "runtime_collector_relationship": (
            "The existing application Runtime Collector remains separate and is not reused as a filesystem security owner."
        ),
        "pilot_kind": "STANDARD_LIBRARY_SUBPROCESS_AUDIT_HOOK_PILOT",
        "dependency_scope": "STANDARD_LIBRARY_VALIDATION_ONLY_NO_RUNTIME_INTEGRATION",
        "isolation_strategy": "fresh child processes and disposable OS temporary directories",
        "replay_strategy": "repeat the same synthetic and Q20 fixture probes and compare decision fields",
        "bounds": {"max_events": 5000, "timeout_seconds": 60, "probe_runs": 2},
        "observed_actions": list(ACTIONS),
        "synthetic_categories": list(result["synthetic_categories"]),
        "q20_categories": list(result["q20_categories"]),
        "relative_path_attribution_unresolved": bool(
            result["relative_path_attribution_unresolved"]
        ),
        "relative_path_attribution_runtime_observed": bool(
            result["relative_path_attribution_runtime_observed"]
        ),
        "relative_path_attribution_evidence_mode": str(
            result["relative_path_attribution_evidence_mode"]
        ),
        "child_process_side_effects_unobserved": bool(
            result["child_process_side_effects_unobserved"]
        ),
        "security_sandbox_claimed": False,
        "application_runtime_integration": False,
        "unique_meaningful_defects": list(result["unique_meaningful_defects"]),
        "known_or_duplicate_findings": list(result["known_or_duplicate_findings"]),
        "false_assurance_risks": list(result["false_assurance_risks"]),
        "measurable_gain": "No unique defect beyond Q20/Q21 protection was found.",
        "operational_cost": "Additional child processes, audit-event volume, and platform-specific path attribution complexity.",
        "broader_adoption_decision": "REJECT_BROADER_ADOPTION",
        "validators": [
            "tools/validate_brick_wall_q29_no_leak_runtime_trace_pilot_decision_v1.py",
            "tools/validate_brick_wall_q20_shared_isolated_filesystem_fixtures_v1.py",
        ],
        "expected_markers": [
            "Q29_SYNTHETIC_ACTION_COVERAGE: PASS",
            "Q29_RELATIVE_DIR_FD_ATTRIBUTION_LIMITATION: PASS",
            "Q29_BROADER_ADOPTION_REJECTED: PASS",
        ],
        "unresolved_fields": [],
        "decision": "PILOT_REJECTED",
        "may_proceed_to_q30": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_rejected_record(result: Mapping[str, object]) -> dict[str, object]:
    return _base(result)


def valid_retained_record(result: Mapping[str, object]) -> dict[str, object]:
    record = _base(result)
    record.update(
        unique_meaningful_defects=[
            "synthetic unique no-leak defect for contract validation"
        ],
        known_or_duplicate_findings=[],
        false_assurance_risks=[],
        relative_path_attribution_unresolved=False,
        relative_path_attribution_runtime_observed=False,
        relative_path_attribution_evidence_mode="NOT_APPLICABLE",
        child_process_side_effects_unobserved=False,
        measurable_gain="A unique reproducible side effect escaped existing validators.",
        broader_adoption_decision="RETAIN_BOUNDED_HIGH_RISK_VALIDATION_ONLY",
        decision="PILOT_RETAINED",
    )
    return record


def valid_not_applicable_record(result: Mapping[str, object]) -> dict[str, object]:
    record = _base(result)
    record.update(
        pilot_applicable=False,
        no_pilot_evidence=["No high-risk validation side-effect path is in scope."],
        canonical_owners=[],
        synthetic_categories=[],
        q20_categories=[],
        relative_path_attribution_unresolved=False,
        relative_path_attribution_runtime_observed=False,
        relative_path_attribution_evidence_mode="NOT_APPLICABLE",
        child_process_side_effects_unobserved=False,
        unique_meaningful_defects=[],
        known_or_duplicate_findings=[],
        false_assurance_risks=[],
        measurable_gain="Not applicable.",
        operational_cost="Not applicable.",
        broader_adoption_decision="NOT_APPLICABLE",
        validators=[],
        expected_markers=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record(result: Mapping[str, object]) -> dict[str, object]:
    return deepcopy(valid_rejected_record(result))
