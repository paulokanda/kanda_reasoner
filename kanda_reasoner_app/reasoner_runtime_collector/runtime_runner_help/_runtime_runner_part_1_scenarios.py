# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/_runtime_runner_part_1_scenarios.py
"""Explicit named-scenario registry and execution for runtime runner part 1."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

__all__: list[str] = []

ScenarioCallable = Callable[..., Any]


@dataclass(frozen=True, slots=True)
class RegisteredRuntimeScenario:
    """Explicit callable slots preserving legacy scenario precedence."""

    collect_runtime_scenario: ScenarioCallable | None = None
    run_runtime_scenario: ScenarioCallable | None = None
    run: ScenarioCallable | None = None
    main: ScenarioCallable | None = None


_SCENARIO_REGISTRY: dict[str, RegisteredRuntimeScenario] = {}


def register_runtime_scenario(
    scenario_name: str,
    scenario: RegisteredRuntimeScenario,
) -> None:
    """Register one named scenario under an explicit validated key."""
    normalized_name = str(scenario_name).strip()
    if not normalized_name:
        raise ValueError("scenario_name must be non-empty")
    if not isinstance(scenario, RegisteredRuntimeScenario):
        raise TypeError("scenario must be RegisteredRuntimeScenario")
    _SCENARIO_REGISTRY[normalized_name] = scenario


def unregister_runtime_scenario(scenario_name: str) -> None:
    """Remove one named scenario without affecting unrelated registrations."""
    _SCENARIO_REGISTRY.pop(str(scenario_name).strip(), None)


def clear_runtime_scenario_registry() -> None:
    """Clear explicit scenario registrations for deterministic tests."""
    _SCENARIO_REGISTRY.clear()


def runtime_scenario_registry_snapshot() -> dict[str, RegisteredRuntimeScenario]:
    """Return a shallow registry snapshot without exposing mutable ownership."""
    return dict(_SCENARIO_REGISTRY)


def _ordered_candidates(
    scenario: RegisteredRuntimeScenario,
) -> tuple[tuple[str, ScenarioCallable | None], ...]:
    """Return callable slots in the exact legacy precedence order."""
    return (
        ("collect_runtime_scenario", scenario.collect_runtime_scenario),
        ("run_runtime_scenario", scenario.run_runtime_scenario),
        ("run", scenario.run),
        ("main", scenario.main),
    )


def _invoke_candidate(
    candidate: ScenarioCallable,
    *,
    project_root: Path,
    entry_script: Path | None,
    output_json: Path,
) -> None:
    """Preserve legacy kwargs call then TypeError no-argument fallback."""
    try:
        candidate(
            project_root=str(project_root),
            entry_script=str(entry_script) if entry_script else "",
            output_json=str(output_json),
        )
    except TypeError:
        candidate()


def run_registered_runtime_scenario(
    scenario_name: str,
    project_root: Path,
    entry_script: Path | None,
    output_json: Path,
) -> str:
    """Run one explicitly registered scenario using legacy callable precedence."""
    scenario = _SCENARIO_REGISTRY.get(scenario_name)
    if scenario is None:
        raise RuntimeError(
            "Scenario module is not registered for explicit runtime execution: "
            + scenario_name
        )

    for candidate_name, candidate in _ordered_candidates(scenario):
        if candidate is None:
            continue
        _invoke_candidate(
            candidate,
            project_root=project_root,
            entry_script=entry_script,
            output_json=output_json,
        )
        return candidate_name

    raise RuntimeError(
        "Registered scenario does not expose a supported callable: "
        + scenario_name
    )
