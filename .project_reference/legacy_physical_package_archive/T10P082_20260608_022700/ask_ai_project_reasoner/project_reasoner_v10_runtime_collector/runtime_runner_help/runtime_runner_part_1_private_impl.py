"""Private helper implementations for runtime runner configuration and scenarios."""

from __future__ import annotations

__all__ = []


# PASS_064H_RUNTIME_HELPER_DEPENDENCIES_BEGIN
import os
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import primary_evidence_json_path

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_JSON = primary_evidence_json_path(DEFAULT_PROJECT_ROOT)
_ENV_PROJECT_ROOT = "PROJECT_REASONER_PROJECT_ROOT"
_ENV_RUNTIME_TRACE_JSON = "PROJECT_REASONER_RUNTIME_TRACE_JSON"
_ENV_RUNTIME_TRACE_OVERWRITE = "PROJECT_REASONER_RUNTIME_TRACE_OVERWRITE"
_ENV_ENTRY_SCRIPT = "PROJECT_REASONER_RUNTIME_ENTRY_SCRIPT"
_ENV_SCENARIO_MODULE = "PROJECT_REASONER_RUNTIME_SCENARIO_MODULE"
_ENV_EXECUTE_ENTRY_SCRIPT = "PROJECT_REASONER_RUNTIME_EXECUTE_ENTRY_SCRIPT"
# PASS_064H_RUNTIME_HELPER_DEPENDENCIES_END
def _bind_root_globals(root_globals):
    globals().update(root_globals)


def _rr__headless_mode_requested_impl() -> bool:
    return bool(os.environ.get(_ENV_RUNTIME_TRACE_JSON, "").strip())


def _rr__resolve_headless_config_impl() -> dict:
    project_root_raw = os.environ.get(_ENV_PROJECT_ROOT, "").strip()
    output_json_raw = os.environ.get(_ENV_RUNTIME_TRACE_JSON, "").strip()
    overwrite_raw = os.environ.get(_ENV_RUNTIME_TRACE_OVERWRITE, "").strip()
    entry_script_raw = os.environ.get(_ENV_ENTRY_SCRIPT, "").strip()
    scenario_module_raw = os.environ.get(_ENV_SCENARIO_MODULE, "").strip()
    execute_entry_script_raw = os.environ.get(_ENV_EXECUTE_ENTRY_SCRIPT, "").strip()

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
    module = __import__(scenario_module, fromlist=["*"])

    candidate_names = [
        "collect_runtime_scenario",
        "run_runtime_scenario",
        "run",
        "main",
    ]

    for name in candidate_names:
        candidate = getattr(module, name, None)
        if not callable(candidate):
            continue

        try:
            candidate(
                project_root=str(project_root),
                entry_script=str(entry_script) if entry_script else "",
                output_json=str(output_json),
            )
            return name
        except TypeError:
            candidate()
            return name

    raise RuntimeError(
        "Scenario module does not expose a supported callable: "
        + scenario_module
    )


def _rr__run_entry_script_impl(entry_script: Path) -> None:
    runpy.run_path(str(entry_script), run_name="__main__")


def _rr__as_mapping_impl(value: object) -> dict:
    """Return value when it is a dict, otherwise an empty dict."""
    return value if isinstance(value, dict) else {}


def _rr__as_list_impl(value: object) -> list:
    """Return value when it is a list, otherwise an empty list."""
    return value if isinstance(value, list) else []


def _rr__safe_len_impl(value: object) -> int:
    """Return len(value) when possible."""
    try:
        return len(value)  # type: ignore[arg-type]
    except Exception:
        return 0


def _rr__build_runtime_symbol_index_impl(files_payload: list[dict]) -> dict:
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
        trace_event(
            event_type="runtime_runner_static_files_payload_missing",
            source_file="runtime_runner.py",
            source_symbol="_build_real_runtime_files_payload",
            message="Static evidence JSON has no files section.",
            extra={"evidence_path": evidence_path},
        )
        return []

    selected = _select_runtime_scenario_files(files_payload)

    trace_state_snapshot(
        label="runtime_runner_static_files_payload",
        state={
            "evidence_path": evidence_path,
            "available_file_count": len(files_payload),
            "selected_file_count": len(selected),
            "files": [item.get("path", "") for item in selected],
        },
    )

    return selected


def _rr__run_builtin_collector_component_scenario_impl(project_root: Path) -> dict:
    """Run collector-component scenario by consuming generated static JSON."""
    trace_event(
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
        trace_state_snapshot(
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

    trace_state_snapshot(
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

    trace_state_snapshot(
        label="runtime_runner_builtin_collector_summary",
        state=summary,
    )

    trace_event(
        event_type="runtime_runner_builtin_collector_scenario_finished",
        source_file="runtime_runner.py",
        source_symbol="_run_builtin_collector_component_scenario",
        message="Built-in collector component scenario finished.",
    )

    return summary


def _rr__ensure_qapplication_impl() -> QApplication:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app

# PASS_065F_RUNTIME_PART1_BINDINGS START
# Grouped runtime-family bindings added by Pass 073B.
import importlib as _pass_065f_importlib
import runpy as runpy
import sys as _pass_065f_sys
import traceback as traceback
from pathlib import Path as Path


def _pass_073b_noop(*args, **kwargs):
    return None


def _pass_073b_import_module(module_name):
    try:
        return _pass_065f_importlib.import_module(module_name)
    except Exception:
        return None


def _pass_073b_import_attr(module_name, attr_name):
    module = _pass_073b_import_module(module_name)
    if module is None:
        return None
    return getattr(module, attr_name, None)


def _pass_073b_import_first_attr(module_names, attr_name):
    for module_name in module_names:
        value = _pass_073b_import_attr(module_name, attr_name)
        if value is not None:
            return value
    return None


def _pass_073b_import_runtime_trace_attr(attr_name):
    value = _pass_073b_import_attr(
        "kanda_reasoner_app.reasoner_runtime_collector.runtime_trace_api",
        attr_name,
    )
    if callable(value):
        return value
    return _pass_073b_noop

QApplication = _pass_073b_import_first_attr(
    ("PySide6.QtWidgets", "PyQt6.QtWidgets"),
    "QApplication",
)

configure_runtime_trace = _pass_073b_import_runtime_trace_attr("configure_runtime_trace")
save_runtime_trace = _pass_073b_import_runtime_trace_attr("save_runtime_trace")
trace_event = _pass_073b_import_runtime_trace_attr("trace_event")
trace_signal_connection = _pass_073b_import_runtime_trace_attr("trace_signal_connection")
trace_state_snapshot = _pass_073b_import_runtime_trace_attr("trace_state_snapshot")


def _pass_065f_part1_root_module():
    names = (
        "__main__",
        "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner",
    )
    for module_name in names:
        module = _pass_065f_sys.modules.get(module_name)
        if module is not None and module is not _pass_065f_sys.modules.get(__name__):
            return module
    try:
        return _pass_065f_importlib.import_module(
            "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner"
        )
    except Exception:
        return None


def _pass_065f_part1_impl_names(public_name):
    if public_name.startswith("_"):
        stem = public_name[1:]
        return (
            "_rr__" + stem + "_impl",
            "_rr_" + stem + "_impl",
            public_name + "_impl",
        )
    return (public_name + "_impl",)


def _pass_065f_part1_call(public_name, *args, **kwargs):
    current_public = globals().get(public_name)
    for impl_name in _pass_065f_part1_impl_names(public_name):
        impl = globals().get(impl_name)
        if callable(impl) and impl is not current_public:
            return impl(*args, **kwargs)
    module = _pass_065f_part1_root_module()
    if module is not None:
        impl = getattr(module, public_name, None)
        if callable(impl) and impl is not current_public:
            return impl(*args, **kwargs)
    raise NameError(public_name + " is not bound in runtime_runner part 1")


def _as_list(*args, **kwargs):
    return _pass_065f_part1_call("_as_list", *args, **kwargs)


def _as_mapping(*args, **kwargs):
    return _pass_065f_part1_call("_as_mapping", *args, **kwargs)


def _build_real_runtime_files_payload(*args, **kwargs):
    return _pass_065f_part1_call("_build_real_runtime_files_payload", *args, **kwargs)


def _build_runtime_symbol_index(*args, **kwargs):
    return _pass_065f_part1_call("_build_runtime_symbol_index", *args, **kwargs)


def _load_static_evidence_json(*args, **kwargs):
    return _pass_065f_part1_call("_load_static_evidence_json", *args, **kwargs)


def _safe_len(*args, **kwargs):
    return _pass_065f_part1_call("_safe_len", *args, **kwargs)


def _section_from_static_evidence(*args, **kwargs):
    return _pass_065f_part1_call("_section_from_static_evidence", *args, **kwargs)


def _select_runtime_scenario_files(*args, **kwargs):
    return _pass_065f_part1_call("_select_runtime_scenario_files", *args, **kwargs)


def _summary_from_static_sections(*args, **kwargs):
    return _pass_065f_part1_call("_summary_from_static_sections", *args, **kwargs)
# PASS_065F_RUNTIME_PART1_BINDINGS END
