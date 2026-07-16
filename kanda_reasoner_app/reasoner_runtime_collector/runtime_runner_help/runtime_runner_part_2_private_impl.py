# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/runtime_runner_part_2_private_impl.py
"""Private runtime-runner part 2 facade with explicit safe dependencies."""

from __future__ import annotations

from pathlib import Path

from ._runtime_runner_part_2_bindings import (
    RuntimeRunnerPart2Bindings,
    bindings_from_root_globals,
    build_default_runtime_bindings,
)
from ._runtime_runner_part_2_scenarios import (
    run_builtin_qt_interaction_scenario,
    run_headless_scenario,
    run_rich_automatic_scenario,
)
from ._runtime_runner_part_2_window import (
    append_log,
    browse_output_json,
    browse_project_root,
    build_ui,
    connect_signals,
    start_spinner,
    stop_spinner,
    tick_spinner,
    update_spinner_line,
)

__all__ = []

_BINDINGS_HOLDER: list[RuntimeRunnerPart2Bindings] = [
    build_default_runtime_bindings()
]


def _bindings() -> RuntimeRunnerPart2Bindings:
    """Return the currently bound runtime-runner dependencies."""
    return _BINDINGS_HOLDER[0]


def _bind_root_globals(root_globals):
    """Bind explicit runtime dependencies supplied by the public facade."""
    _BINDINGS_HOLDER[0] = bindings_from_root_globals(
        root_globals,
        fallback=_bindings(),
    )


def _run_builtin_qt_interaction_scenario(*args, **kwargs):
    """Run the built-in Qt scenario through the explicit scenario owner."""
    if args or kwargs:
        return _rr__run_builtin_qt_interaction_scenario_impl(*args, **kwargs)
    return _rr__run_builtin_qt_interaction_scenario_impl()


def _run_rich_automatic_scenario(*args, **kwargs):
    """Run the rich automatic scenario through the explicit scenario owner."""
    return _rr__run_rich_automatic_scenario_impl(*args, **kwargs)


def _rr__run_builtin_qt_interaction_scenario_impl() -> dict:
    """Run the deterministic Qt interaction scenario."""
    return run_builtin_qt_interaction_scenario(_bindings())


def _rr__run_rich_automatic_scenario_impl(
    project_root: Path,
    output_json: Path,
    entry_script: Path | None,
    scenario_module: str,
    execute_entry_script: bool,
) -> str:
    """Run the rich scenario while preserving the legacy call contract."""
    return run_rich_automatic_scenario(
        _bindings(),
        project_root=project_root,
        output_json=output_json,
        entry_script=entry_script,
        scenario_module=scenario_module,
        execute_entry_script=execute_entry_script,
    )


def _rr__run_headless_impl() -> int:
    """Run headless collection through the explicit scenario owner."""
    return run_headless_scenario(_bindings())


def _rr_RuntimeCollectorWindow__build_ui_impl(self) -> None:
    """Build the runtime collector UI."""
    build_ui(_bindings(), self)


def _rr_RuntimeCollectorWindow__connect_signals_impl(self) -> None:
    """Connect runtime collector controls by Qt object-name convention."""
    connect_signals(_bindings(), self)


def _rr_RuntimeCollectorWindow__append_log_impl(self, text: str) -> None:
    """Append one line to the runtime collector log."""
    append_log(self, text)


def _rr_RuntimeCollectorWindow__start_spinner_impl(self) -> None:
    """Start the runtime collector save spinner."""
    start_spinner(self)


def _rr_RuntimeCollectorWindow__tick_spinner_impl(self) -> None:
    """Advance the runtime collector save spinner."""
    tick_spinner(self)


def _rr_RuntimeCollectorWindow__update_spinner_line_impl(self, text: str) -> None:
    """Replace the current spinner line."""
    update_spinner_line(self, text)


def _rr_RuntimeCollectorWindow__stop_spinner_impl(self) -> None:
    """Stop the runtime collector save spinner."""
    stop_spinner(self)


def _rr_RuntimeCollectorWindow__browse_project_root_impl(self) -> None:
    """Browse for and persist a project root."""
    browse_project_root(_bindings(), self)


def _rr_RuntimeCollectorWindow__browse_output_json_impl(self) -> None:
    """Browse for and persist an output JSON path."""
    browse_output_json(_bindings(), self)


def _resolve_headless_config(*args, **kwargs):
    """Preserve the legacy private wrapper for headless configuration."""
    return _bindings().resolve_headless_config(*args, **kwargs)


def _ensure_qapplication(*args, **kwargs):
    """Preserve the legacy private wrapper for QApplication creation."""
    return _bindings().ensure_qapplication(*args, **kwargs)


def _run_builtin_collector_component_scenario(*args, **kwargs):
    """Preserve the legacy private wrapper for collector scenarios."""
    return _bindings().run_builtin_collector_component_scenario(*args, **kwargs)


def _run_entry_script(*args, **kwargs):
    """Preserve the legacy private wrapper for entry-script execution."""
    return _bindings().run_entry_script(*args, **kwargs)


def _run_named_scenario_module(*args, **kwargs):
    """Preserve the legacy private wrapper for named scenarios."""
    return _bindings().run_named_scenario_module(*args, **kwargs)


def _save_prefs(*args, **kwargs):
    """Preserve the legacy private wrapper for preference persistence."""
    return _bindings().save_prefs(*args, **kwargs)


def _rr_run_headless_impl(*args, **kwargs):
    """Preserve the alternate private headless implementation name."""
    if args or kwargs:
        raise TypeError("_rr_run_headless_impl() takes no arguments")
    return _rr__run_headless_impl()
