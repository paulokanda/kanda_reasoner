# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/_runtime_runner_part_1_bindings.py
"""Explicit dependency bindings for runtime runner part 1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api import (
    trace_event as runtime_trace_event,
    trace_state_snapshot as runtime_trace_state_snapshot,
)

__all__: list[str] = []


@dataclass(frozen=True, slots=True)
class RuntimeRunnerPart1Bindings:
    """Explicit dependencies consumed by part 1 runtime helpers."""

    trace_event: Callable[..., Any]
    trace_state_snapshot: Callable[..., Any]
    load_static_evidence_json: Callable[..., Any]
    section_from_static_evidence: Callable[..., Any]
    select_runtime_scenario_files: Callable[..., Any]
    summary_from_static_sections: Callable[..., Any]
    qapplication_type: Any


def _unbound_static_evidence_loader(*args: object, **kwargs: object) -> Any:
    """Fail clearly when static-evidence helpers are used before root binding."""
    del args, kwargs
    raise NameError("_load_static_evidence_json is not bound in runtime_runner part 1")


def _unbound_section_from_static_evidence(
    *args: object,
    **kwargs: object,
) -> Any:
    """Fail clearly when section projection is used before root binding."""
    del args, kwargs
    raise NameError("_section_from_static_evidence is not bound in runtime_runner part 1")


def _unbound_select_runtime_scenario_files(
    *args: object,
    **kwargs: object,
) -> Any:
    """Fail clearly when scenario-file selection is used before root binding."""
    del args, kwargs
    raise NameError("_select_runtime_scenario_files is not bound in runtime_runner part 1")


def _unbound_summary_from_static_sections(
    *args: object,
    **kwargs: object,
) -> Any:
    """Fail clearly when summary projection is used before root binding."""
    del args, kwargs
    raise NameError("_summary_from_static_sections is not bound in runtime_runner part 1")


def build_default_runtime_bindings() -> RuntimeRunnerPart1Bindings:
    """Build import-safe defaults before the payload facade binds dependencies."""
    return RuntimeRunnerPart1Bindings(
        trace_event=runtime_trace_event,
        trace_state_snapshot=runtime_trace_state_snapshot,
        load_static_evidence_json=_unbound_static_evidence_loader,
        section_from_static_evidence=_unbound_section_from_static_evidence,
        select_runtime_scenario_files=_unbound_select_runtime_scenario_files,
        summary_from_static_sections=_unbound_summary_from_static_sections,
        qapplication_type=None,
    )


def bindings_from_root_globals(
    root_globals: dict[str, Any],
    *,
    fallback: RuntimeRunnerPart1Bindings,
) -> RuntimeRunnerPart1Bindings:
    """Build explicit bindings from the runtime facade namespace."""
    return RuntimeRunnerPart1Bindings(
        trace_event=root_globals.get(
            "trace_event",
            fallback.trace_event,
        ),
        trace_state_snapshot=root_globals.get(
            "trace_state_snapshot",
            fallback.trace_state_snapshot,
        ),
        load_static_evidence_json=root_globals.get(
            "_load_static_evidence_json",
            fallback.load_static_evidence_json,
        ),
        section_from_static_evidence=root_globals.get(
            "_section_from_static_evidence",
            fallback.section_from_static_evidence,
        ),
        select_runtime_scenario_files=root_globals.get(
            "_select_runtime_scenario_files",
            fallback.select_runtime_scenario_files,
        ),
        summary_from_static_sections=root_globals.get(
            "_summary_from_static_sections",
            fallback.summary_from_static_sections,
        ),
        qapplication_type=root_globals.get(
            "QApplication",
            fallback.qapplication_type,
        ),
    )


def binding_contract_names() -> tuple[str, ...]:
    """Return the exact root names consumed by the binding adapter."""
    return (
        "trace_event",
        "trace_state_snapshot",
        "_load_static_evidence_json",
        "_section_from_static_evidence",
        "_select_runtime_scenario_files",
        "_summary_from_static_sections",
        "QApplication",
    )
