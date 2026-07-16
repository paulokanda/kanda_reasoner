"""Private helper implementations for runtime runner headless and Qt scenarios."""
from __future__ import annotations
__all__ = []
# PASS_064I_RUNTIME_PART2_DEPENDENCIES_START
import sys
import traceback
import json
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import primary_evidence_json_path
DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_JSON = primary_evidence_json_path(DEFAULT_PROJECT_ROOT)
_ENV_PROJECT_ROOT = 'PROJECT_REASONER_PROJECT_ROOT'
_ENV_RUNTIME_TRACE_JSON = 'PROJECT_REASONER_RUNTIME_TRACE_JSON'
_ENV_RUNTIME_TRACE_OVERWRITE = 'PROJECT_REASONER_RUNTIME_TRACE_OVERWRITE'
_ENV_ENTRY_SCRIPT = 'PROJECT_REASONER_RUNTIME_ENTRY_SCRIPT'
_ENV_SCENARIO_MODULE = 'PROJECT_REASONER_RUNTIME_SCENARIO_MODULE'
_ENV_EXECUTE_ENTRY_SCRIPT = 'PROJECT_REASONER_RUNTIME_EXECUTE_ENTRY_SCRIPT'
_SPINNER_FRAMES = ["-", "\\", "|", "/"]
def _run_builtin_qt_interaction_scenario(*args, **kwargs):
    return _rr__run_builtin_qt_interaction_scenario_impl(*args, **kwargs)
def _run_rich_automatic_scenario(*args, **kwargs):
    return _rr__run_rich_automatic_scenario_impl(*args, **kwargs)
# PASS_064I_RUNTIME_PART2_DEPENDENCIES_END
def _bind_root_globals(root_globals):
    globals().update(root_globals)
def _rr__run_builtin_qt_interaction_scenario_impl() -> dict:
    app = _ensure_qapplication()
    trace_event(
        event_type="runtime_runner_builtin_qt_scenario_started",
        source_file="runtime_runner.py",
        source_symbol="_run_builtin_qt_interaction_scenario",
        message="Built-in Qt interaction scenario started.",
    )
    state = {
        "text_change_count": 0,
        "button_click_count": 0,
        "close_click_count": 0,
        "last_text": "",
        "label_text": "Idle",
    }
    host = QWidget()
    host.setObjectName("runtime_runner_probe_window")
    layout = QVBoxLayout(host)
    label = QLabel("Idle")
    label.setObjectName("runtime_runner_probe_label")
    line_edit = QLineEdit()
    line_edit.setObjectName("runtime_runner_probe_line_edit")
    apply_button = QPushButton("Apply")
    apply_button.setObjectName("runtime_runner_probe_apply_button")
    close_button = QPushButton("Close")
    close_button.setObjectName("runtime_runner_probe_close_button")
    layout.addWidget(label)
    layout.addWidget(line_edit)
    layout.addWidget(apply_button)
    layout.addWidget(close_button)
    def on_text_changed(text: str) -> None:
        state["text_change_count"] += 1
        state["last_text"] = text
        trace_event(
            event_type="runtime_runner_probe_text_changed",
            source_file="runtime_runner.py",
            source_symbol="on_text_changed",
            message="Probe line edit text changed to: " + text,
            object_name=line_edit.objectName(),
            object_type="QLineEdit",
            extra={
                "text": text,
            },
        )
    def on_apply_clicked() -> None:
        state["button_click_count"] += 1
        label.setText("Applied: " + line_edit.text())
        state["label_text"] = label.text()
        trace_event(
            event_type="runtime_runner_probe_apply_clicked",
            source_file="runtime_runner.py",
            source_symbol="on_apply_clicked",
            message="Probe apply button clicked.",
            object_name=apply_button.objectName(),
            object_type="QPushButton",
            extra={
                "current_text": line_edit.text(),
                "label_text": label.text(),
            },
        )
    def on_close_clicked() -> None:
        state["close_click_count"] += 1
        trace_event(
            event_type="runtime_runner_probe_close_clicked",
            source_file="runtime_runner.py",
            source_symbol="on_close_clicked",
            message="Probe close button clicked.",
            object_name=close_button.objectName(),
            object_type="QPushButton",
        )
        host.close()
    line_edit.textChanged.connect(on_text_changed)
    trace_signal_connection(
        sender_type="QLineEdit",
        sender_name=line_edit.objectName(),
        signal_name="textChanged",
        receiver_type="function",
        receiver_name="runtime_runner.py",
        slot_name="on_text_changed",
        source_file="runtime_runner.py",
        extra={
            "source_symbol": "_run_builtin_qt_interaction_scenario",
            "widget_text": "",
        },
    )
    apply_button.clicked.connect(on_apply_clicked)
    trace_signal_connection(
        sender_type="QPushButton",
        sender_name=apply_button.objectName(),
        signal_name="clicked",
        receiver_type="function",
        receiver_name="runtime_runner.py",
        slot_name="on_apply_clicked",
        source_file="runtime_runner.py",
        extra={
            "source_symbol": "_run_builtin_qt_interaction_scenario",
            "button_text": apply_button.text(),
        },
    )
    close_button.clicked.connect(on_close_clicked)
    trace_signal_connection(
        sender_type="QPushButton",
        sender_name=close_button.objectName(),
        signal_name="clicked",
        receiver_type="function",
        receiver_name="runtime_runner.py",
        slot_name="on_close_clicked",
        source_file="runtime_runner.py",
        extra={
            "source_symbol": "_run_builtin_qt_interaction_scenario",
            "button_text": close_button.text(),
        },
    )
    trace_state_snapshot(
        label="runtime_runner_builtin_qt_widgets_created",
        state={
            "host_object_name": host.objectName(),
            "label_object_name": label.objectName(),
            "line_edit_object_name": line_edit.objectName(),
            "apply_button_object_name": apply_button.objectName(),
            "close_button_object_name": close_button.objectName(),
        },
    )
    line_edit.setText("alpha")
    app.processEvents()
    apply_button.click()
    app.processEvents()
    line_edit.setText("beta")
    app.processEvents()
    apply_button.click()
    app.processEvents()
    close_button.click()
    app.processEvents()
    trace_state_snapshot(
        label="runtime_runner_builtin_qt_summary",
        state=state,
    )
    trace_event(
        event_type="runtime_runner_builtin_qt_scenario_finished",
        source_file="runtime_runner.py",
        source_symbol="_run_builtin_qt_interaction_scenario",
        message="Built-in Qt interaction scenario finished.",
    )
    return state
def _rr__run_rich_automatic_scenario_impl(
    project_root: Path,
    output_json: Path,
    entry_script: Path | None,
    scenario_module: str,
    execute_entry_script: bool,
) -> str:
    trace_event(
        event_type="runtime_runner_automatic_scenario_started",
        source_file="runtime_runner.py",
        source_symbol="_run_rich_automatic_scenario",
        message="Automatic runtime scenario started.",
    )
    trace_state_snapshot(
        label="runtime_runner_automatic_scenario_context",
        state={
            "project_root": str(project_root),
            "output_json": str(output_json),
            "entry_script": str(entry_script) if entry_script else "",
            "entry_script_exists": bool(entry_script and entry_script.exists()),
            "scenario_module": scenario_module,
            "execute_entry_script": execute_entry_script,
        },
    )
    if scenario_module:
        scenario_mode = "scenario_module"
        callable_name = _run_named_scenario_module(
            scenario_module=scenario_module,
            project_root=project_root,
            entry_script=entry_script,
            output_json=output_json,
        )
        trace_event(
            event_type="runtime_runner_scenario_module_executed",
            source_file="runtime_runner.py",
            source_symbol="_run_rich_automatic_scenario",
            message=(
                "Scenario module executed: "
                + scenario_module
                + " via "
                + callable_name
            ),
        )
    elif execute_entry_script and entry_script and entry_script.exists():
        scenario_mode = "entry_script"
        _run_entry_script(entry_script)
        trace_event(
            event_type="runtime_runner_entry_script_executed",
            source_file="runtime_runner.py",
            source_symbol="_run_rich_automatic_scenario",
            message="Entry script executed by runtime runner.",
        )
    else:
        scenario_mode = "built_in_project_scenario"
        collector_summary = _run_builtin_collector_component_scenario(project_root)
        qt_summary = _run_builtin_qt_interaction_scenario()
        trace_state_snapshot(
            label="runtime_runner_built_in_project_scenario_summary",
            state={
                "scenario_mode": scenario_mode,
                "collector_summary": collector_summary,
                "qt_summary": qt_summary,
            },
        )
        trace_event(
            event_type="runtime_runner_built_in_project_scenario_executed",
            source_file="runtime_runner.py",
            source_symbol="_run_rich_automatic_scenario",
            message="Built-in project scenario executed.",
        )
    trace_event(
        event_type="runtime_runner_automatic_scenario_finished",
        source_file="runtime_runner.py",
        source_symbol="_run_rich_automatic_scenario",
        message="Automatic runtime scenario finished.",
    )
    return scenario_mode
def _rr__run_headless_impl() -> int:
    try:
        config = _resolve_headless_config()
        project_root = config["project_root"]
        output_json = config["output_json"]
        overwrite = config["overwrite"]
        entry_script = config["entry_script"]
        scenario_module = config["scenario_module"]
        execute_entry_script = config["execute_entry_script"]
        output_json.parent.mkdir(parents=True, exist_ok=True)
        existed_before = output_json.exists()
        if overwrite and existed_before:
            try:
                output_json.unlink()
            except Exception:
                pass
        configure_runtime_trace(
            project_root=str(project_root),
            output_path=str(output_json),
            entry_script=str(entry_script) if entry_script else "",
        )
        scenario_mode = _run_rich_automatic_scenario(
            project_root=project_root,
            output_json=output_json,
            entry_script=entry_script,
            scenario_module=scenario_module,
            execute_entry_script=execute_entry_script,
        )
        saved_path = save_runtime_trace()
        final_output_path = (
            Path(saved_path).expanduser().resolve()
            if saved_path is not None
            else output_json
        )
        payload = {
            "ok": True,
            "runtime_trace_json": str(final_output_path),
            "overwrote_existing": existed_before and overwrite,
            "exists": final_output_path.exists(),
            "size": final_output_path.stat().st_size if final_output_path.exists() else 0,
            "scenario_mode": scenario_mode,
        }
        print(json.dumps(payload), flush=True)
        return 0
    except Exception:
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        return 1
def _rr_RuntimeCollectorWindow__build_ui_impl(self) -> None:
    central = QWidget()
    self.setCentralWidget(central)
    main_layout = QVBoxLayout(central)
    grid = QGridLayout()
    grid.addWidget(QLabel("Project root:"), 0, 0)
    grid.addWidget(self.project_root_edit, 0, 1)
    grid.addWidget(self.browse_project_button, 0, 2)
    grid.addWidget(QLabel("Output JSON:"), 1, 0)
    grid.addWidget(self.output_json_edit, 1, 1)
    grid.addWidget(self.browse_output_button, 1, 2)
    grid.addWidget(QLabel("Entry script:"), 2, 0)
    grid.addWidget(self.entry_script_edit, 2, 1)
    grid.addWidget(self.browse_entry_button, 2, 2)
    button_row = QHBoxLayout()
    button_row.addStretch()
    button_row.addWidget(self.configure_button)
    button_row.addWidget(self.save_button)
    button_row.addWidget(self.close_button)
    main_layout.addLayout(grid)
    main_layout.addLayout(button_row)
    main_layout.addWidget(QLabel("Log:"))
    main_layout.addWidget(self.log_box)
def _rr_RuntimeCollectorWindow__connect_signals_impl(self) -> None:
    self.browse_project_button.clicked.connect(self._browse_project_root)
    self.browse_output_button.clicked.connect(self._browse_output_json)
    self.browse_entry_button.clicked.connect(self._browse_entry_script)
    self.configure_button.clicked.connect(self._configure_trace)
    self.save_button.clicked.connect(self._save_trace)
    self.close_button.clicked.connect(self.close)
def _rr_RuntimeCollectorWindow__append_log_impl(self, text: str) -> None:
    self.log_box.appendPlainText(str(text))
    scroll_bar = self.log_box.verticalScrollBar()
    scroll_bar.setValue(scroll_bar.maximum())
def _rr_RuntimeCollectorWindow__start_spinner_impl(self) -> None:
    self._append_log("")
    doc = self.log_box.document()
    self._spinner_line = doc.blockCount() - 1
    self._spinner_frame = 0
    self._spinner_timer.start()
def _rr_RuntimeCollectorWindow__tick_spinner_impl(self) -> None:
    frame = _SPINNER_FRAMES[self._spinner_frame % len(_SPINNER_FRAMES)]
    self._spinner_frame += 1
    self._update_spinner_line(f"{frame}  Saving trace...")
def _rr_RuntimeCollectorWindow__update_spinner_line_impl(self, text: str) -> None:
    doc = self.log_box.document()
    block = doc.findBlockByNumber(self._spinner_line)
    cursor = self.log_box.textCursor()
    cursor.setPosition(block.position())
    cursor.movePosition(cursor.MoveOperation.EndOfBlock, cursor.MoveMode.KeepAnchor)
    cursor.insertText(text)
def _rr_RuntimeCollectorWindow__stop_spinner_impl(self) -> None:
    self._spinner_timer.stop()
    if self._spinner_line >= 0:
        self._update_spinner_line("[OK] Trace saved.")
        self._spinner_line = -1
def _rr_RuntimeCollectorWindow__browse_project_root_impl(self) -> None:
    folder = QFileDialog.getExistingDirectory(
        self,
        "Select project root",
        self.project_root_edit.text().strip() or str(DEFAULT_PROJECT_ROOT),
    )
    if folder:
        self.project_root_edit.setText(folder)
        _save_prefs(
            folder,
            self.output_json_edit.text().strip(),
            self.entry_script_edit.text().strip(),
        )
def _rr_RuntimeCollectorWindow__browse_output_json_impl(self) -> None:
    file_path, _ = QFileDialog.getSaveFileName(
        self,
        "Select output JSON",
        self.output_json_edit.text().strip() or str(DEFAULT_OUTPUT_JSON),
        "JSON Files (*.json)",
    )
    if file_path:
        self.output_json_edit.setText(file_path)
        _save_prefs(
            self.project_root_edit.text().strip(),
            file_path,
            self.entry_script_edit.text().strip(),
        )
# PASS_065F_RUNTIME_PART2_BINDINGS START
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

QFileDialog = _pass_073b_import_first_attr(("PySide6.QtWidgets", "PyQt6.QtWidgets"), "QFileDialog")
QGridLayout = _pass_073b_import_first_attr(("PySide6.QtWidgets", "PyQt6.QtWidgets"), "QGridLayout")
QHBoxLayout = _pass_073b_import_first_attr(("PySide6.QtWidgets", "PyQt6.QtWidgets"), "QHBoxLayout")
QLabel = _pass_073b_import_first_attr(("PySide6.QtWidgets", "PyQt6.QtWidgets"), "QLabel")
QLineEdit = _pass_073b_import_first_attr(("PySide6.QtWidgets", "PyQt6.QtWidgets"), "QLineEdit")
QPushButton = _pass_073b_import_first_attr(("PySide6.QtWidgets", "PyQt6.QtWidgets"), "QPushButton")
QVBoxLayout = _pass_073b_import_first_attr(("PySide6.QtWidgets", "PyQt6.QtWidgets"), "QVBoxLayout")
QWidget = _pass_073b_import_first_attr(("PySide6.QtWidgets", "PyQt6.QtWidgets"), "QWidget")

configure_runtime_trace = _pass_073b_import_runtime_trace_attr("configure_runtime_trace")
save_runtime_trace = _pass_073b_import_runtime_trace_attr("save_runtime_trace")
trace_event = _pass_073b_import_runtime_trace_attr("trace_event")
trace_signal_connection = _pass_073b_import_runtime_trace_attr("trace_signal_connection")
trace_state_snapshot = _pass_073b_import_runtime_trace_attr("trace_state_snapshot")

_pass_065f_part1 = _pass_073b_import_module(
    "kanda_reasoner_app.reasoner_runtime_collector.runtime_runner_help.runtime_runner_part_1_private_impl"
)


def _pass_065f_part2_impl_names(public_name):
    if public_name.startswith("_"):
        stem = public_name[1:]
        return (
            "_rr__" + stem + "_impl",
            "_rr_" + stem + "_impl",
            public_name + "_impl",
        )
    return (public_name + "_impl",)
def _pass_065f_part2_local_call(public_name, *args, **kwargs):
    current_public = globals().get(public_name)
    for impl_name in _pass_065f_part2_impl_names(public_name):
        impl = globals().get(impl_name)
        if callable(impl) and impl is not current_public:
            return impl(*args, **kwargs)
    raise NameError(public_name + " has no local implementation in runtime_runner part 2")
def _pass_065f_part2_part1_call(public_name, *args, **kwargs):
    if _pass_065f_part1 is not None:
        for impl_name in _pass_065f_part2_impl_names(public_name):
            impl = getattr(_pass_065f_part1, impl_name, None)
            if callable(impl):
                return impl(*args, **kwargs)
        impl = getattr(_pass_065f_part1, public_name, None)
        if callable(impl):
            return impl(*args, **kwargs)
    raise NameError(public_name + " is not bound through runtime_runner part 1")
def _resolve_headless_config(*args, **kwargs):
    return _pass_065f_part2_part1_call("_resolve_headless_config", *args, **kwargs)
def _ensure_qapplication(*args, **kwargs):
    return _pass_065f_part2_part1_call("_ensure_qapplication", *args, **kwargs)
def _run_builtin_collector_component_scenario(*args, **kwargs):
    return _pass_065f_part2_part1_call("_run_builtin_collector_component_scenario", *args, **kwargs)
def _run_entry_script(*args, **kwargs):
    return _pass_065f_part2_part1_call("_run_entry_script", *args, **kwargs)
def _run_named_scenario_module(*args, **kwargs):
    return _pass_065f_part2_part1_call("_run_named_scenario_module", *args, **kwargs)
def _save_prefs(*args, **kwargs):
    return None
def _run_rich_automatic_scenario(*args, **kwargs):
    return _pass_065f_part2_local_call("_run_rich_automatic_scenario", *args, **kwargs)
def _run_builtin_qt_interaction_scenario(*args, **kwargs):
    return _pass_065f_part2_local_call("_run_builtin_qt_interaction_scenario", *args, **kwargs)
def _rr_run_headless_impl(*args, **kwargs):
    return _pass_065f_part2_local_call("_run_headless", *args, **kwargs)
# PASS_065F_RUNTIME_PART2_BINDINGS END
