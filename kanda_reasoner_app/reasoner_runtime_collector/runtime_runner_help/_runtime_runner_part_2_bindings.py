# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/_runtime_runner_part_2_bindings.py
"""Explicit dependency bindings for runtime runner part 2."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from kanda_reasoner_app.project_analysis_evidence_paths import (
    primary_evidence_json_path,
)
from kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api import (
    configure_runtime_trace as runtime_configure_trace,
    save_runtime_trace as runtime_save_trace,
    trace_event as runtime_trace_event,
    trace_signal_connection as runtime_trace_signal_connection,
    trace_state_snapshot as runtime_trace_state_snapshot,
)
from kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help import (
    runtime_runner_part_1_private_impl as _part_1,
)

__all__: list[str] = []

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_JSON = primary_evidence_json_path(DEFAULT_PROJECT_ROOT)


@dataclass(frozen=True, slots=True)
class RuntimeRunnerPart2Bindings:
    """Explicit callable and path dependencies used by part 2 helpers."""

    configure_runtime_trace: Callable[..., Any]
    save_runtime_trace: Callable[..., Any]
    trace_event: Callable[..., Any]
    trace_signal_connection: Callable[..., Any]
    trace_state_snapshot: Callable[..., Any]
    resolve_headless_config: Callable[..., Any]
    ensure_qapplication: Callable[..., Any]
    run_builtin_collector_component_scenario: Callable[..., Any]
    run_entry_script: Callable[..., Any]
    run_named_scenario_module: Callable[..., Any]
    save_prefs: Callable[..., Any]
    default_project_root: Path
    default_output_json: Path


def _noop_save_prefs(*args: object, **kwargs: object) -> None:
    """Provide the import-safe pre-bind preference behavior."""
    del args, kwargs
    return None


def _resolve_headless_config_default(*args: object, **kwargs: object) -> Any:
    """Call the part 1 implementation used before public-facade binding."""
    del args, kwargs
    return _part_1._rr__resolve_headless_config_impl()


def _ensure_qapplication_default(*args: object, **kwargs: object) -> Any:
    """Call the part 1 QApplication implementation."""
    del args, kwargs
    return _part_1._rr__ensure_qapplication_impl()


def _run_builtin_collector_default(*args: object, **kwargs: object) -> Any:
    """Call the part 1 built-in collector implementation."""
    return _part_1._rr__run_builtin_collector_component_scenario_impl(
        *args,
        **kwargs,
    )


def _run_entry_script_default(*args: object, **kwargs: object) -> Any:
    """Call the part 1 entry-script implementation."""
    return _part_1._rr__run_entry_script_impl(*args, **kwargs)


def _run_named_scenario_default(*args: object, **kwargs: object) -> Any:
    """Call the part 1 named-scenario implementation."""
    return _part_1._rr__run_named_scenario_module_impl(*args, **kwargs)


def build_default_runtime_bindings() -> RuntimeRunnerPart2Bindings:
    """Build import-safe defaults before the public runtime facade binds."""
    return RuntimeRunnerPart2Bindings(
        configure_runtime_trace=runtime_configure_trace,
        save_runtime_trace=runtime_save_trace,
        trace_event=runtime_trace_event,
        trace_signal_connection=runtime_trace_signal_connection,
        trace_state_snapshot=runtime_trace_state_snapshot,
        resolve_headless_config=_resolve_headless_config_default,
        ensure_qapplication=_ensure_qapplication_default,
        run_builtin_collector_component_scenario=_run_builtin_collector_default,
        run_entry_script=_run_entry_script_default,
        run_named_scenario_module=_run_named_scenario_default,
        save_prefs=_noop_save_prefs,
        default_project_root=DEFAULT_PROJECT_ROOT,
        default_output_json=DEFAULT_OUTPUT_JSON,
    )


def bindings_from_root_globals(
    root_globals: dict[str, Any],
    *,
    fallback: RuntimeRunnerPart2Bindings,
) -> RuntimeRunnerPart2Bindings:
    """Build explicit bindings from the public runtime facade namespace."""
    return RuntimeRunnerPart2Bindings(
        configure_runtime_trace=root_globals.get(
            "configure_runtime_trace",
            fallback.configure_runtime_trace,
        ),
        save_runtime_trace=root_globals.get(
            "save_runtime_trace",
            fallback.save_runtime_trace,
        ),
        trace_event=root_globals.get(
            "trace_event",
            fallback.trace_event,
        ),
        trace_signal_connection=root_globals.get(
            "trace_signal_connection",
            fallback.trace_signal_connection,
        ),
        trace_state_snapshot=root_globals.get(
            "trace_state_snapshot",
            fallback.trace_state_snapshot,
        ),
        resolve_headless_config=root_globals.get(
            "_resolve_headless_config",
            fallback.resolve_headless_config,
        ),
        ensure_qapplication=root_globals.get(
            "_ensure_qapplication",
            fallback.ensure_qapplication,
        ),
        run_builtin_collector_component_scenario=root_globals.get(
            "_run_builtin_collector_component_scenario",
            fallback.run_builtin_collector_component_scenario,
        ),
        run_entry_script=root_globals.get(
            "_run_entry_script",
            fallback.run_entry_script,
        ),
        run_named_scenario_module=root_globals.get(
            "_run_named_scenario_module",
            fallback.run_named_scenario_module,
        ),
        save_prefs=root_globals.get(
            "_save_prefs",
            fallback.save_prefs,
        ),
        default_project_root=root_globals.get(
            "DEFAULT_PROJECT_ROOT",
            fallback.default_project_root,
        ),
        default_output_json=root_globals.get(
            "DEFAULT_OUTPUT_JSON",
            fallback.default_output_json,
        ),
    )


def binding_contract_names() -> tuple[str, ...]:
    """Return explicit root names consumed by the binding adapter."""
    return (
        "configure_runtime_trace",
        "save_runtime_trace",
        "trace_event",
        "trace_signal_connection",
        "trace_state_snapshot",
        "_resolve_headless_config",
        "_ensure_qapplication",
        "_run_builtin_collector_component_scenario",
        "_run_entry_script",
        "_run_named_scenario_module",
        "_save_prefs",
        "DEFAULT_PROJECT_ROOT",
        "DEFAULT_OUTPUT_JSON",
    )
