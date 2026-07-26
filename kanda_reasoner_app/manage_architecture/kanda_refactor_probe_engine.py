# project-path: kanda_reasoner_app/manage_architecture/kanda_refactor_probe_engine.py
"""Behavior characterization and structured comparison for AST-safe refactors.

This module supplies reusable probe profiles and deterministic comparison
mechanics.  It never invents architecture, generates random inputs, or claims
behavior equivalence without explicit semantic probe cases supplied by AI/human
reasoning or a focused validator.
"""
from __future__ import annotations

import dataclasses
import enum
import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "ProbeComparison",
    "ProbeObservation",
    "available_probe_profiles",
    "capture_probe",
    "compare_probe_sets",
    "probe_profile",
    "run_paired_probe_cases",
    "write_probe_evidence",
]

PROFILE_CASES: dict[str, tuple[str, ...]] = {
    "CONTRACT_MODULE": (
        "default_build",
        "safe_probe",
        "accepted_mode",
        "missing_dependency",
        "each_blocker_category",
        "false_capability_values",
        "invalid_policy_invariant",
        "invalid_decision_invariant",
        "exception_type",
        "exception_message",
        "repeated_call_determinism",
    ),
    "COLLECTOR_MODULE": (
        "empty_project",
        "single_source_file",
        "excluded_path_policy",
        "parse_failure_tolerance",
        "stable_ordering",
        "idempotent_write",
        "existing_payload_preservation",
        "error_contract",
    ),
    "PURE_MAPPING_MODULE": (
        "empty_input",
        "nominal_input",
        "boundary_input",
        "unknown_key",
        "stable_ordering",
        "repeated_call_determinism",
        "error_contract",
    ),
    "SERIALIZATION_MODULE": (
        "empty_payload",
        "nominal_payload",
        "unicode_payload",
        "stable_key_order",
        "round_trip",
        "invalid_payload_error",
        "repeated_serialization_determinism",
    ),
    "GUI_STATE_MODULE": (
        "initial_state",
        "safe_transition",
        "blocked_transition",
        "target_change_reset",
        "button_enablement",
        "single_window_contract",
        "no_hidden_shared_host_state",
    ),
    "CLI_MODULE": (
        "help_contract",
        "default_invocation",
        "compact_output",
        "invalid_argument",
        "exit_code_success",
        "exit_code_failure",
        "stderr_contract",
    ),
    "CUSTOM": (),
}


@dataclass(frozen=True)
class ProbeObservation:
    """Serializable result of one explicit semantic probe case."""

    name: str
    ok: bool
    value: Any
    exception_type: str
    exception_message: str

    def as_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-compatible observation."""
        return {
            "name": self.name,
            "ok": self.ok,
            "value": self.value,
            "exception_type": self.exception_type,
            "exception_message": self.exception_message,
        }


@dataclass(frozen=True)
class ProbeComparison:
    """Baseline/candidate comparison record for one semantic probe."""

    name: str
    equivalent: bool
    baseline: ProbeObservation
    candidate: ProbeObservation
    differences: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        """Return a deterministic JSON-compatible comparison."""
        return {
            "name": self.name,
            "equivalent": self.equivalent,
            "differences": list(self.differences),
            "baseline": self.baseline.as_dict(),
            "candidate": self.candidate.as_dict(),
        }


def available_probe_profiles() -> tuple[str, ...]:
    """Return the stable names of supported characterization scaffolds."""
    return tuple(sorted(PROFILE_CASES))


def probe_profile(name: str) -> dict[str, Any]:
    """Return one advisory scaffold without pretending cases are executable tests."""
    normalized = str(name or "").strip().upper()
    if normalized not in PROFILE_CASES:
        raise ValueError("Unknown probe profile: " + normalized)
    return {
        "profile": normalized,
        "suggested_semantic_cases": list(PROFILE_CASES[normalized]),
        "authority": "scaffold_only_ai_human_must_define_executable_cases",
    }


def _normalize_mapping(value: Mapping[Any, Any]) -> dict[str, Any]:
    """Normalize mappings recursively with stable string keys."""
    output: dict[str, Any] = {}
    for key in sorted(value, key=lambda item: str(item)):
        output[str(key)] = normalize_probe_value(value[key])
    return output


def _normalize_sequence(value: Sequence[Any]) -> list[Any]:
    """Normalize list/tuple-like values while preserving order."""
    return [normalize_probe_value(item) for item in value]


def normalize_probe_value(value: Any) -> Any:
    """Convert common behavior outputs into deterministic JSON-compatible data."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, enum.Enum):
        return {
            "__enum__": value.__class__.__name__,
            "name": value.name,
            "value": normalize_probe_value(value.value),
        }
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return {
            "__dataclass__": value.__class__.__name__,
            "fields": _normalize_mapping(dataclasses.asdict(value)),
        }
    if isinstance(value, Mapping):
        return _normalize_mapping(value)
    if isinstance(value, (list, tuple)):
        return _normalize_sequence(value)
    if isinstance(value, set):
        normalized = [normalize_probe_value(item) for item in value]
        return sorted(normalized, key=lambda item: json.dumps(item, sort_keys=True, default=str))
    if isinstance(value, Path):
        return {"__path__": value.as_posix()}
    return {
        "__type__": value.__class__.__name__,
        "__repr__": repr(value),
    }


def capture_probe(name: str, case: Callable[[], Any]) -> ProbeObservation:
    """Execute one explicit semantic probe and capture observable outcome."""
    try:
        result = case()
    except Exception as exc:
        return ProbeObservation(
            name=name,
            ok=False,
            value=None,
            exception_type=exc.__class__.__name__,
            exception_message=str(exc),
        )
    return ProbeObservation(
        name=name,
        ok=True,
        value=normalize_probe_value(result),
        exception_type="",
        exception_message="",
    )


def _compare_observations(
    baseline: ProbeObservation,
    candidate: ProbeObservation,
) -> ProbeComparison:
    """Compare one baseline/candidate observation including exact error text."""
    differences: list[str] = []
    if baseline.ok != candidate.ok:
        differences.append("ok")
    if baseline.value != candidate.value:
        differences.append("value")
    if baseline.exception_type != candidate.exception_type:
        differences.append("exception_type")
    if baseline.exception_message != candidate.exception_message:
        differences.append("exception_message")
    return ProbeComparison(
        name=baseline.name,
        equivalent=not differences,
        baseline=baseline,
        candidate=candidate,
        differences=tuple(differences),
    )


def compare_probe_sets(
    baseline: Mapping[str, ProbeObservation],
    candidate: Mapping[str, ProbeObservation],
) -> dict[str, Any]:
    """Compare named observation sets and fail closed on missing semantic cases."""
    baseline_names = set(baseline)
    candidate_names = set(candidate)
    missing_candidate = sorted(baseline_names - candidate_names)
    unexpected_candidate = sorted(candidate_names - baseline_names)
    comparisons: list[ProbeComparison] = []
    for name in sorted(baseline_names & candidate_names):
        comparisons.append(_compare_observations(baseline[name], candidate[name]))
    failures = [item.name for item in comparisons if not item.equivalent]
    passed = not missing_candidate and not unexpected_candidate and not failures
    return {
        "schema_version": "1.0",
        "kind": "ast_safe_refactor_behavior_equivalence",
        "missing_candidate_cases": missing_candidate,
        "unexpected_candidate_cases": unexpected_candidate,
        "non_equivalent_cases": failures,
        "comparisons": [item.as_dict() for item in comparisons],
        "pass": passed,
    }


def _capture_case_map(cases: Mapping[str, Callable[[], Any]]) -> dict[str, ProbeObservation]:
    """Execute a stable mapping of explicit semantic probe cases."""
    output: dict[str, ProbeObservation] = {}
    for name in sorted(cases):
        output[name] = capture_probe(name, cases[name])
    return output


def run_paired_probe_cases(
    baseline_cases: Mapping[str, Callable[[], Any]],
    candidate_cases: Mapping[str, Callable[[], Any]],
    *,
    profile_name: str = "CUSTOM",
) -> dict[str, Any]:
    """Run explicit baseline/candidate probes and return structured comparison."""
    profile = probe_profile(profile_name)
    baseline = _capture_case_map(baseline_cases)
    candidate = _capture_case_map(candidate_cases)
    comparison = compare_probe_sets(baseline, candidate)
    comparison["profile"] = profile
    comparison["baseline_observations"] = {
        name: observation.as_dict()
        for name, observation in sorted(baseline.items())
    }
    comparison["candidate_observations"] = {
        name: observation.as_dict()
        for name, observation in sorted(candidate.items())
    }
    return comparison


def write_probe_evidence(path: Path | str, payload: dict[str, Any]) -> Path:
    """Persist explicit UTF-8 behavior evidence to a caller-selected path."""
    output = Path(path).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return output


def _demo_cases() -> tuple[dict[str, Callable[[], Any]], dict[str, Callable[[], Any]]]:
    """Return deterministic internal smoke cases for focused validator use."""
    baseline = {
        "value": lambda: {"accepted": True, "status": "safe"},
        "error": lambda: _raise_value_error("contract violation"),
    }
    candidate = {
        "value": lambda: {"accepted": True, "status": "safe"},
        "error": lambda: _raise_value_error("contract violation"),
    }
    return baseline, candidate


def _raise_value_error(message: str) -> None:
    """Raise one deterministic validation error for smoke evidence."""
    raise ValueError(message)


def main() -> int:
    """Run a small deterministic behavior-equivalence smoke demonstration."""
    baseline, candidate = _demo_cases()
    result = run_paired_probe_cases(baseline, candidate, profile_name="CUSTOM")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
