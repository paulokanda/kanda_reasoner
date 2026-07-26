# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/advanced_quality_review_contract.py
"""Immutable contracts for Advanced Quality Review identity and scenarios."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from pathlib import PurePosixPath
from typing import Iterable

__all__ = [
    "ADVANCED_QUALITY_REVIEW_FOUNDATION_FEATURE_ID",
    "AnalysisExecutionStatus",
    "AnalysisIdentity",
    "AnalyzerAuthorityRole",
    "ArchitectureQualityScenario",
    "QualityDecision",
    "REQUIRED_ARCHITECTURE_QUALITY_SCENARIOS",
    "analysis_identity_matches",
    "build_analysis_identity",
    "validate_architecture_quality_scenarios",
]

ADVANCED_QUALITY_REVIEW_FOUNDATION_FEATURE_ID = (
    "advanced-quality-review-exchange-foundation-v1"
)


class AnalyzerAuthorityRole(str, Enum):
    """Describe how one analyzer may influence authorization."""

    MANDATORY = "MANDATORY"
    CONDITIONAL = "CONDITIONAL"
    ADVISORY = "ADVISORY"


class AnalysisExecutionStatus(str, Enum):
    """Describe analyzer execution independently from quality judgment."""

    NOT_RUN = "NOT_RUN"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    CANCELLED = "CANCELLED"
    UNAVAILABLE = "UNAVAILABLE"
    STALE = "STALE"


class QualityDecision(str, Enum):
    """Describe quality authorization independently from execution status."""

    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    BLOCKED = "BLOCKED"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True)
class AnalysisIdentity:
    """Bind one quality-review run to exact Workbench and analyzer inputs."""

    schema_version: str
    project_card_identity: str
    target_relative_path: str
    baseline_hash: str
    preview_hash: str
    refactor_plan_hash: str
    analyzer_lock_hash: str
    analyzer_config_hash: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-ready immutable identity payload."""
        return asdict(self)

    @property
    def identity_hash(self) -> str:
        """Return the canonical SHA-256 digest for the identity payload."""
        return _canonical_hash(self.to_dict())


@dataclass(frozen=True)
class ArchitectureQualityScenario:
    """Specify one stimulus-response requirement for the subsystem."""

    scenario_id: str
    stimulus: str
    precondition: str
    expected_response: str
    execution_status_effect: str
    quality_decision_effect: str
    persistence_effect: str
    gui_effect: str


REQUIRED_ARCHITECTURE_QUALITY_SCENARIOS = (
    ArchitectureQualityScenario(
        scenario_id="preview_changes_while_running",
        stimulus="The active Preview identity changes while analyzers are running.",
        precondition="A review run is bound to Preview H1.",
        expected_response="Allow bounded cleanup and reject H1 at the acceptance boundary.",
        execution_status_effect="Mark the completed H1 result STALE.",
        quality_decision_effect="H1 cannot authorize H2.",
        persistence_effect="Keep H1 historical evidence with stale authorization state.",
        gui_effect="Keep the GUI responsive and require a new H2 review.",
    ),
    ArchitectureQualityScenario(
        scenario_id="analyzer_unavailable",
        stimulus="A configured analyzer executable is unavailable.",
        precondition="Environment preflight is running.",
        expected_response="Report capability evidence without silent installation.",
        execution_status_effect="Mark the engine UNAVAILABLE.",
        quality_decision_effect="Apply mandatory, conditional, or advisory authority policy.",
        persistence_effect="Persist capability evidence and no synthetic findings.",
        gui_effect="Show the unavailable engine and resulting authorization effect.",
    ),
    ArchitectureQualityScenario(
        scenario_id="analyzer_version_mismatch",
        stimulus="The discovered analyzer version differs from the lock contract.",
        precondition="Environment preflight has an expected version identity.",
        expected_response="Fail the engine precondition and do not analyze under drift.",
        execution_status_effect="Mark the engine FAILED or UNAVAILABLE by policy.",
        quality_decision_effect="Never synthesize PASS from incompatible tooling.",
        persistence_effect="Persist expected and observed version evidence.",
        gui_effect="Show a version compatibility blocker with remediation context.",
    ),
    ArchitectureQualityScenario(
        scenario_id="malformed_machine_output",
        stimulus="An analyzer returns malformed machine-readable output.",
        precondition="The process exited and parser validation starts.",
        expected_response="Reject malformed evidence and preserve raw diagnostics.",
        execution_status_effect="Mark the engine FAILED.",
        quality_decision_effect="Mandatory evidence becomes INDETERMINATE or BLOCKED.",
        persistence_effect="Persist diagnostics without treating malformed output as findings.",
        gui_effect="Show parser failure and engine identity.",
    ),
    ArchitectureQualityScenario(
        scenario_id="analyzer_timeout",
        stimulus="An analyzer exceeds its bounded timeout.",
        precondition="The engine process is running in controlled execution.",
        expected_response="Terminate contained execution and reap descendants.",
        execution_status_effect="Mark the engine TIMED_OUT.",
        quality_decision_effect="Apply authority policy without synthetic PASS.",
        persistence_effect="Persist timeout and cleanup evidence.",
        gui_effect="Show timeout and keep Cancel or retry routes available.",
    ),
    ArchitectureQualityScenario(
        scenario_id="descendant_process_cancel",
        stimulus="The user cancels an analyzer that spawned descendants.",
        precondition="Controlled process-tree containment owns the run.",
        expected_response="Cancel and prove no descendant process survives.",
        execution_status_effect="Mark the engine CANCELLED.",
        quality_decision_effect="The incomplete review cannot authorize progression.",
        persistence_effect="Persist cancellation and cleanup proof.",
        gui_effect="Return controls to a safe retryable state.",
    ),
    ArchitectureQualityScenario(
        scenario_id="baseline_drift",
        stimulus="Canonical baseline source changes during analysis.",
        precondition="The run has a sealed baseline hash.",
        expected_response="Rehash and reject evidence bound to the old baseline.",
        execution_status_effect="Mark the run STALE.",
        quality_decision_effect="No stale baseline comparison may authorize progression.",
        persistence_effect="Retain historical run evidence with stale state.",
        gui_effect="Require re-intake or a new run from current source.",
    ),
    ArchitectureQualityScenario(
        scenario_id="analyzer_input_mutation",
        stimulus="A controlled analyzer input changes unexpectedly during a run.",
        precondition="Input hashes were sealed before execution.",
        expected_response="Raise ANALYZER_MUTATION_DETECTED and fail closed.",
        execution_status_effect="Mark the affected run FAILED.",
        quality_decision_effect="Set overall decision BLOCKED.",
        persistence_effect="Persist before and after hashes plus diagnostics.",
        gui_effect="Show a hard mutation blocker.",
    ),
    ArchitectureQualityScenario(
        scenario_id="mandatory_engine_failure",
        stimulus="A mandatory analyzer fails.",
        precondition="Authority role is MANDATORY.",
        expected_response="Preserve failure and stop authorization.",
        execution_status_effect="Keep the concrete failure status.",
        quality_decision_effect="Set overall decision INDETERMINATE or BLOCKED.",
        persistence_effect="Persist partial evidence without filling the missing dimension.",
        gui_effect="Show incomplete execution separately from quality findings.",
    ),
    ArchitectureQualityScenario(
        scenario_id="advisory_engine_failure",
        stimulus="An advisory analyzer fails.",
        precondition="Authority role is ADVISORY.",
        expected_response="Preserve the failure without inventing advisory findings.",
        execution_status_effect="Keep the concrete failure status.",
        quality_decision_effect="Do not let advisory failure silently become PASS.",
        persistence_effect="Persist engine failure and remaining valid dimensions.",
        gui_effect="Show advisory evidence unavailable.",
    ),
    ArchitectureQualityScenario(
        scenario_id="card_switch_while_running",
        stimulus="The active project card changes while a review owns execution.",
        precondition="A run is bound to card C1 and target T1.",
        expected_response="Reject late C1 results from repopulating C2 state.",
        execution_status_effect="Mark late results STALE for the active card.",
        quality_decision_effect="No cross-card authorization is allowed.",
        persistence_effect="Retain C1 evidence only under C1 ownership.",
        gui_effect="Do not attach C1 output to the C2 view.",
    ),
    ArchitectureQualityScenario(
        scenario_id="durable_persistence_failure",
        stimulus="Writing immutable Project Support evidence fails.",
        precondition="Analysis and cross-check have completed.",
        expected_response="Report persistence failure and do not authorize progression.",
        execution_status_effect="Mark the review FAILED at persistence stage.",
        quality_decision_effect="Set overall decision INDETERMINATE.",
        persistence_effect="Do not pretend the durable record exists.",
        gui_effect="Show persistence failure with retry guidance.",
    ),
    ArchitectureQualityScenario(
        scenario_id="transient_cache_missing",
        stimulus="Transient analyzer cache is deleted between sessions.",
        precondition="Durable Project Support evidence remains intact.",
        expected_response="Regenerate caches without changing durable authority.",
        execution_status_effect="No failure solely from cache absence.",
        quality_decision_effect="Existing immutable evidence remains historical authority.",
        persistence_effect="Keep durable evidence unchanged.",
        gui_effect="Allow regeneration without presenting cache as source truth.",
    ),
)


def build_analysis_identity(
    *,
    project_card_identity: str,
    target_relative_path: str,
    baseline_hash: str,
    preview_hash: str,
    refactor_plan_hash: str,
    analyzer_lock_hash: str,
    analyzer_config_hash: str,
    schema_version: str = "1.0",
) -> AnalysisIdentity:
    """Build one validated identity for a sealed review run."""
    values = {
        "schema_version": schema_version,
        "project_card_identity": project_card_identity,
        "target_relative_path": _normalize_relative_path(target_relative_path),
        "baseline_hash": baseline_hash,
        "preview_hash": preview_hash,
        "refactor_plan_hash": refactor_plan_hash,
        "analyzer_lock_hash": analyzer_lock_hash,
        "analyzer_config_hash": analyzer_config_hash,
    }
    _require_nonempty(values)
    return AnalysisIdentity(**{key: str(value).strip() for key, value in values.items()})


def analysis_identity_matches(left: AnalysisIdentity, right: AnalysisIdentity) -> bool:
    """Return whether two immutable analysis identities are exactly equivalent."""
    return left.identity_hash == right.identity_hash


def validate_architecture_quality_scenarios(
    scenarios: Iterable[ArchitectureQualityScenario] = REQUIRED_ARCHITECTURE_QUALITY_SCENARIOS,
) -> tuple[str, ...]:
    """Return deterministic blockers for incomplete or duplicate scenarios."""
    blockers: list[str] = []
    seen: set[str] = set()
    required_fields = tuple(ArchitectureQualityScenario.__dataclass_fields__)
    materialized = tuple(scenarios)
    if not materialized:
        blockers.append("ARCHITECTURE_QUALITY_SCENARIOS_EMPTY")
    for scenario in materialized:
        scenario_id = str(scenario.scenario_id or "").strip()
        if not scenario_id:
            blockers.append("SCENARIO_ID_EMPTY")
            continue
        if scenario_id in seen:
            blockers.append("SCENARIO_ID_DUPLICATE:" + scenario_id)
        seen.add(scenario_id)
        for field_name in required_fields:
            if not str(getattr(scenario, field_name, "") or "").strip():
                blockers.append(
                    "SCENARIO_FIELD_EMPTY:" + scenario_id + ":" + field_name
                )
    return tuple(sorted(set(blockers)))


def _normalize_relative_path(value: str) -> str:
    """Return one safe POSIX-style relative path for identity payloads."""
    text = str(value or "").replace("\\", "/").strip()
    path = PurePosixPath(text)
    if not text or path.is_absolute() or ".." in path.parts:
        raise ValueError("TARGET_RELATIVE_PATH_INVALID")
    return path.as_posix()


def _require_nonempty(values: dict[str, str]) -> None:
    """Reject incomplete identity payloads before any evidence is accepted."""
    missing = [key for key, value in values.items() if not str(value or "").strip()]
    if missing:
        raise ValueError("ANALYSIS_IDENTITY_FIELDS_EMPTY:" + ",".join(sorted(missing)))


def _canonical_hash(payload: dict[str, str]) -> str:
    """Return canonical SHA-256 for one JSON-serializable identity payload."""
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
