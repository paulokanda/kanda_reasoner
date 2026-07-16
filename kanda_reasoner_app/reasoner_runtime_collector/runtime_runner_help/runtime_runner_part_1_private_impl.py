# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/runtime_runner_part_1_private_impl.py
"""Private runtime-runner part 1 facade with explicit safe dependencies."""

from __future__ import annotations

__all__ = []

import os
import runpy
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import (
    primary_evidence_json_path,
)
from ._runtime_runner_part_1_bindings import (
    RuntimeRunnerPart1Bindings,
    bindings_from_root_globals,
    build_default_runtime_bindings,
)
from ._runtime_runner_part_1_scenarios import run_registered_runtime_scenario

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_JSON = primary_evidence_json_path(DEFAULT_PROJECT_ROOT)
_ENV_PROJECT_ROOT = "PROJECT_REASONER_PROJECT_ROOT"
_ENV_RUNTIME_TRACE_JSON = "PROJECT_REASONER_RUNTIME_TRACE_JSON"
_ENV_RUNTIME_TRACE_OVERWRITE = "PROJECT_REASONER_RUNTIME_TRACE_OVERWRITE"
_ENV_ENTRY_SCRIPT = "PROJECT_REASONER_RUNTIME_ENTRY_SCRIPT"
_ENV_SCENARIO_MODULE = "PROJECT_REASONER_RUNTIME_SCENARIO_MODULE"
_ENV_EXECUTE_ENTRY_SCRIPT = "PROJECT_REASONER_RUNTIME_EXECUTE_ENTRY_SCRIPT"

_BINDINGS_HOLDER: list[RuntimeRunnerPart1Bindings] = [
    build_default_runtime_bindings()
]


def _bindings() -> RuntimeRunnerPart1Bindings:
    """Return the currently bound part 1 runtime dependencies."""
    return _BINDINGS_HOLDER[0]


def _bind_root_globals(root_globals):
    """Bind only the explicit root dependencies consumed by part 1."""
    _BINDINGS_HOLDER[0] = bindings_from_root_globals(
        root_globals,
        fallback=_bindings(),
    )


def _rr__headless_mode_requested_impl() -> bool:
    """Return whether direct runtime-trace execution was requested."""
    return bool(os.environ.get(_ENV_RUNTIME_TRACE_JSON, "").strip())


def _rr__resolve_headless_config_impl() -> dict:
    """Resolve the headless runtime configuration from environment variables."""
    project_root_raw = os.environ.get(_ENV_PROJECT_ROOT, "").strip()
    output_json_raw = os.environ.get(_ENV_RUNTIME_TRACE_JSON, "").strip()
    overwrite_raw = os.environ.get(_ENV_RUNTIME_TRACE_OVERWRITE, "").strip()
    entry_script_raw = os.environ.get(_ENV_ENTRY_SCRIPT, "").strip()
    scenario_module_raw = os.environ.get(_ENV_SCENARIO_MODULE, "").strip()
    execute_entry_script_raw = os.environ.get(
        _ENV_EXECUTE_ENTRY_SCRIPT,
        "",
    ).strip()

    project_root = (
        Path(project_root_raw).expanduser().resolve()
        if project_root_raw
        else DEFAULT_PROJECT_ROOT.resolve()
    )
    output_json = (
        Path(output_json_raw).expanduser().resolve()
        if output_json_raw
        else DEFAULT_OUTPUT_JSON.resolve()
    )
    entry_script = (
        Path(entry_script_raw).expanduser().resolve()
        if entry_script_raw
        else None
    )

    return {
        "project_root": project_root,
        "output_json": output_json,
        "overwrite": overwrite_raw == "1",
        "entry_script": entry_script,
        "scenario_module": scenario_module_raw,
        "execute_entry_script": execute_entry_script_raw == "1",
    }


def _rr__run_named_scenario_module_impl(
    scenario_module: str,
    project_root: Path,
    entry_script: Path | None,
    output_json: Path,
) -> str:
    """Run an explicitly registered named runtime scenario."""
    return run_registered_runtime_scenario(
        scenario_module,
        project_root,
        entry_script,
        output_json,
    )


def _rr__run_entry_script_impl(entry_script: Path) -> None:
    """Execute one explicit entry script as ``__main__``."""
    runpy.run_path(str(entry_script), run_name="__main__")


def _rr__as_mapping_impl(value: object) -> dict:
    """Return value when it is a dict, otherwise an empty dict."""
    return value if isinstance(value, dict) else {}


def _rr__as_list_impl(value: object) -> list:
    """Return value when it is a list, otherwise an empty list."""
    return value if isinstance(value, list) else []


def _rr__safe_len_impl(value: object) -> int:
    """Return len(value) when possible, otherwise zero."""
    try:
        return len(value)  # type: ignore[arg-type]
    except Exception:
        return 0


def _rr__build_runtime_symbol_index_impl(files_payload: list[dict]) -> dict:
    """Build the legacy runtime symbol index from file evidence records."""
    out: dict = {}
    for file_record in files_payload:
        path = file_record.get("path", "")
        for fn in file_record.get("functions", []):
            symbol = fn.get("qualname", fn.get("name", ""))
            out[symbol] = {
                "file": path,
                "line": fn.get("lineno"),
                "kind": "function",
            }
        for cls in file_record.get("classes", []):
            cls_name = cls.get("name", "")
            out[cls_name] = {
                "file": path,
                "line": cls.get("lineno"),
                "kind": "class",
            }
            for method in cls.get("methods", []):
                symbol = method.get("qualname", method.get("name", ""))
                out[symbol] = {
                    "file": path,
                    "line": method.get("lineno"),
                    "kind": "method",
                }
    return out


def _rr__build_real_runtime_files_payload_impl(project_root: Path) -> list[dict]:
    """Build scenario file payload from generated static evidence JSON."""
    static_evidence, evidence_path = _load_static_evidence_json(project_root)
    files_payload = _as_list(static_evidence.get("files", []))

    if not files_payload:
        _bindings().trace_event(
            event_type="runtime_runner_static_files_payload_missing",
            source_file="runtime_runner.py",
            source_symbol="_build_real_runtime_files_payload",
            message="Static evidence JSON has no files section.",
            extra={"evidence_path": evidence_path},
        )
        return []

    selected = _select_runtime_scenario_files(files_payload)
    _bindings().trace_state_snapshot(
        label="runtime_runner_static_files_payload",
        state={
            "evidence_path": evidence_path,
            "available_file_count": len(files_payload),
            "selected_file_count": len(selected),
            "files": [item.get("path", "") for item in selected],
        },
    )
    return selected


def _rr__run_builtin_collector_component_scenario_impl(
    project_root: Path,
) -> dict:
    """Run collector-component scenario from generated static JSON."""
    _bindings().trace_event(
        event_type="runtime_runner_builtin_collector_scenario_started",
        source_file="runtime_runner.py",
        source_symbol="_run_builtin_collector_component_scenario",
        message="Built-in collector component scenario started.",
    )

    static_evidence, evidence_path = _load_static_evidence_json(project_root)
    files_payload = _build_real_runtime_files_payload(project_root)

    if not static_evidence:
        summary = {
            "file_count": 0,
            "symbol_count": 0,
            "widget_count": 0,
            "widget_type_count": 0,
            "widgets_with_display_text": 0,
            "widgets_with_layout": 0,
            "qt_signal_record_count": 0,
            "ui_action_count": 0,
            "widget_text_unique_count": 0,
            "widget_layout_count": 0,
            "scenario_status": "skipped",
            "reason": "static_evidence_missing",
        }
        _bindings().trace_state_snapshot(
            label="runtime_runner_builtin_collector_summary",
            state=summary,
        )
        return summary

    symbol_index = _section_from_static_evidence(
        static_evidence,
        "symbol_index",
        _build_runtime_symbol_index(files_payload),
    )
    widget_summary = _as_mapping(
        _section_from_static_evidence(static_evidence, "widget_summary", {})
    )
    widget_text_index = _as_mapping(
        _section_from_static_evidence(static_evidence, "widget_text_index", {})
    )
    widget_layout_index = _as_mapping(
        _section_from_static_evidence(static_evidence, "widget_layout_index", {})
    )
    qt_signal_map = _section_from_static_evidence(
        static_evidence,
        "qt_signal_map",
        [],
    )
    ui_action_summary = _as_mapping(
        _section_from_static_evidence(static_evidence, "ui_action_summary", {})
    )

    _bindings().trace_state_snapshot(
        label="runtime_runner_builtin_collector_input",
        state={
            "evidence_path": evidence_path,
            "file_count": len(files_payload),
            "files": [item.get("path", "") for item in files_payload],
            "symbol_count": _safe_len(symbol_index),
        },
    )

    summary = _summary_from_static_sections(
        files_payload=files_payload,
        symbol_index=symbol_index,
        widget_summary=widget_summary,
        widget_text_index=widget_text_index,
        widget_layout_index=widget_layout_index,
        qt_signal_map=qt_signal_map,
        ui_action_summary=ui_action_summary,
    )
    summary["scenario_status"] = "ok"
    summary["evidence_path"] = evidence_path

    _bindings().trace_state_snapshot(
        label="runtime_runner_builtin_collector_summary",
        state=summary,
    )
    _bindings().trace_event(
        event_type="runtime_runner_builtin_collector_scenario_finished",
        source_file="runtime_runner.py",
        source_symbol="_run_builtin_collector_component_scenario",
        message="Built-in collector component scenario finished.",
    )
    return summary


def _rr__ensure_qapplication_impl() -> QApplication:
    """Return the active QApplication or create one from the bound Qt type."""
    qapplication_type = _bindings().qapplication_type
    app = qapplication_type.instance()
    if app is None:
        app = qapplication_type([])
    return app


def _as_list(*args, **kwargs):
    """Preserve the legacy private wrapper."""
    return _rr__as_list_impl(*args, **kwargs)


def _as_mapping(*args, **kwargs):
    """Preserve the legacy private wrapper."""
    return _rr__as_mapping_impl(*args, **kwargs)


def _build_real_runtime_files_payload(*args, **kwargs):
    """Preserve the legacy private wrapper."""
    return _rr__build_real_runtime_files_payload_impl(*args, **kwargs)


def _build_runtime_symbol_index(*args, **kwargs):
    """Preserve the legacy private wrapper."""
    return _rr__build_runtime_symbol_index_impl(*args, **kwargs)


def _load_static_evidence_json(*args, **kwargs):
    """Dispatch through the explicit root binding."""
    return _bindings().load_static_evidence_json(*args, **kwargs)


def _safe_len(*args, **kwargs):
    """Preserve the legacy private wrapper."""
    return _rr__safe_len_impl(*args, **kwargs)


def _section_from_static_evidence(*args, **kwargs):
    """Dispatch through the explicit root binding."""
    return _bindings().section_from_static_evidence(*args, **kwargs)


def _select_runtime_scenario_files(*args, **kwargs):
    """Dispatch through the explicit root binding."""
    return _bindings().select_runtime_scenario_files(*args, **kwargs)


def _summary_from_static_sections(*args, **kwargs):
    """Dispatch through the explicit root binding."""
    return _bindings().summary_from_static_sections(*args, **kwargs)
