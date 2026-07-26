# project-path: kanda_reasoner_app/reasoner_runtime_collector/runtime_runner_help/_runtime_runner_part_2_scenarios.py
"""Scenario and headless execution logic for runtime runner part 2."""

from __future__ import annotations

import json
import sys
import traceback
from os import unlink
from pathlib import Path
from typing import Any

from ._runtime_runner_part_2_bindings import RuntimeRunnerPart2Bindings

__all__: list[str] = []

def _no_op_slot(*types: object):
    """Provide an import-safe no-op slot decorator when Qt is absent."""
    del types

    def decorate(function):
        return function

    return decorate


def _load_qt_bindings() -> tuple[object, ...]:
    """Load one supported Qt family without rebinding imported symbols."""
    try:
        import PySide6.QtCore as pyside_core
        import PySide6.QtWidgets as pyside_widgets
    except ImportError:
        try:
            import PyQt6.QtCore as pyqt_core
            import PyQt6.QtWidgets as pyqt_widgets
        except ImportError:
            return (None, _no_op_slot, None, None, None, None, object)
        return (
            pyqt_core.QMetaObject,
            pyqt_core.pyqtSlot,
            pyqt_widgets.QLabel,
            pyqt_widgets.QLineEdit,
            pyqt_widgets.QPushButton,
            pyqt_widgets.QVBoxLayout,
            pyqt_widgets.QWidget,
        )
    return (
        pyside_core.QMetaObject,
        pyside_core.Slot,
        pyside_widgets.QLabel,
        pyside_widgets.QLineEdit,
        pyside_widgets.QPushButton,
        pyside_widgets.QVBoxLayout,
        pyside_widgets.QWidget,
    )


(
    QMetaObject,
    Slot,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
) = _load_qt_bindings()


class _RuntimeScenarioHost(QWidget):
    """Own scenario widgets and auto-connected deterministic callbacks."""

    def __init__(self, bindings: RuntimeRunnerPart2Bindings) -> None:
        super().__init__()
        self._bindings = bindings
        self.state = {
            "text_change_count": 0,
            "button_click_count": 0,
            "close_click_count": 0,
            "last_text": "",
            "label_text": "Idle",
        }
        self.setObjectName("runtime_runner_probe_window")
        layout = QVBoxLayout(self)
        self.label = QLabel("Idle")
        self.label.setObjectName("runtime_runner_probe_label")
        self.line_edit = QLineEdit()
        self.line_edit.setObjectName("runtime_runner_probe_line_edit")
        self.apply_button = QPushButton("Apply")
        self.apply_button.setObjectName("runtime_runner_probe_apply_button")
        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("runtime_runner_probe_close_button")
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.close_button)
        if QMetaObject is None:
            raise RuntimeError("Qt bindings are required for the built-in Qt scenario.")
        QMetaObject.connectSlotsByName(self)
        self._trace_connection_contract()

    def _trace_connection_contract(self) -> None:
        """Emit the same connection evidence as the legacy explicit wiring."""
        trace = self._bindings.trace_signal_connection
        trace(
            sender_type="QLineEdit",
            sender_name=self.line_edit.objectName(),
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
        trace(
            sender_type="QPushButton",
            sender_name=self.apply_button.objectName(),
            signal_name="clicked",
            receiver_type="function",
            receiver_name="runtime_runner.py",
            slot_name="on_apply_clicked",
            source_file="runtime_runner.py",
            extra={
                "source_symbol": "_run_builtin_qt_interaction_scenario",
                "button_text": self.apply_button.text(),
            },
        )
        trace(
            sender_type="QPushButton",
            sender_name=self.close_button.objectName(),
            signal_name="clicked",
            receiver_type="function",
            receiver_name="runtime_runner.py",
            slot_name="on_close_clicked",
            source_file="runtime_runner.py",
            extra={
                "source_symbol": "_run_builtin_qt_interaction_scenario",
                "button_text": self.close_button.text(),
            },
        )

    @Slot(str)
    def on_runtime_runner_probe_line_edit_textChanged(self, text: str) -> None:
        """Record text changes using Qt auto-connect naming."""
        self.state["text_change_count"] += 1
        self.state["last_text"] = text
        self._bindings.trace_event(
            event_type="runtime_runner_probe_text_changed",
            source_file="runtime_runner.py",
            source_symbol="on_text_changed",
            message="Probe line edit text changed to: " + text,
            object_name=self.line_edit.objectName(),
            object_type="QLineEdit",
            extra={"text": text},
        )

    @Slot()
    def on_runtime_runner_probe_apply_button_clicked(self) -> None:
        """Apply current text using Qt auto-connect naming."""
        self.state["button_click_count"] += 1
        self.label.setText("Applied: " + self.line_edit.text())
        self.state["label_text"] = self.label.text()
        self._bindings.trace_event(
            event_type="runtime_runner_probe_apply_clicked",
            source_file="runtime_runner.py",
            source_symbol="on_apply_clicked",
            message="Probe apply button clicked.",
            object_name=self.apply_button.objectName(),
            object_type="QPushButton",
            extra={
                "current_text": self.line_edit.text(),
                "label_text": self.label.text(),
            },
        )

    @Slot()
    def on_runtime_runner_probe_close_button_clicked(self) -> None:
        """Record and close the scenario host."""
        self.state["close_click_count"] += 1
        self._bindings.trace_event(
            event_type="runtime_runner_probe_close_clicked",
            source_file="runtime_runner.py",
            source_symbol="on_close_clicked",
            message="Probe close button clicked.",
            object_name=self.close_button.objectName(),
            object_type="QPushButton",
        )
        self.close()


def run_builtin_qt_interaction_scenario(
    bindings: RuntimeRunnerPart2Bindings,
) -> dict[str, Any]:
    """Run the deterministic built-in Qt interaction scenario."""
    app = bindings.ensure_qapplication()
    bindings.trace_event(
        event_type="runtime_runner_builtin_qt_scenario_started",
        source_file="runtime_runner.py",
        source_symbol="_run_builtin_qt_interaction_scenario",
        message="Built-in Qt interaction scenario started.",
    )
    host = _RuntimeScenarioHost(bindings)
    bindings.trace_state_snapshot(
        label="runtime_runner_builtin_qt_widgets_created",
        state={
            "host_object_name": host.objectName(),
            "label_object_name": host.label.objectName(),
            "line_edit_object_name": host.line_edit.objectName(),
            "apply_button_object_name": host.apply_button.objectName(),
            "close_button_object_name": host.close_button.objectName(),
        },
    )
    host.line_edit.setText("alpha")
    app.processEvents()
    host.apply_button.click()
    app.processEvents()
    host.line_edit.setText("beta")
    app.processEvents()
    host.apply_button.click()
    app.processEvents()
    host.close_button.click()
    app.processEvents()
    bindings.trace_state_snapshot(
        label="runtime_runner_builtin_qt_summary",
        state=host.state,
    )
    bindings.trace_event(
        event_type="runtime_runner_builtin_qt_scenario_finished",
        source_file="runtime_runner.py",
        source_symbol="_run_builtin_qt_interaction_scenario",
        message="Built-in Qt interaction scenario finished.",
    )
    return host.state


def run_rich_automatic_scenario(
    bindings: RuntimeRunnerPart2Bindings,
    *,
    project_root: Path,
    output_json: Path,
    entry_script: Path | None,
    scenario_module: str,
    execute_entry_script: bool,
) -> str:
    """Run named, entry-script, or built-in runtime scenarios."""
    bindings.trace_event(
        event_type="runtime_runner_automatic_scenario_started",
        source_file="runtime_runner.py",
        source_symbol="_run_rich_automatic_scenario",
        message="Automatic runtime scenario started.",
    )
    bindings.trace_state_snapshot(
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
        callable_name = bindings.run_named_scenario_module(
            scenario_module=scenario_module,
            project_root=project_root,
            entry_script=entry_script,
            output_json=output_json,
        )
        bindings.trace_event(
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
        bindings.run_entry_script(entry_script)
        bindings.trace_event(
            event_type="runtime_runner_entry_script_executed",
            source_file="runtime_runner.py",
            source_symbol="_run_rich_automatic_scenario",
            message="Entry script executed by runtime runner.",
        )
    else:
        scenario_mode = "built_in_project_scenario"
        collector_summary = bindings.run_builtin_collector_component_scenario(
            project_root
        )
        qt_summary = run_builtin_qt_interaction_scenario(bindings)
        bindings.trace_state_snapshot(
            label="runtime_runner_built_in_project_scenario_summary",
            state={
                "scenario_mode": scenario_mode,
                "collector_summary": collector_summary,
                "qt_summary": qt_summary,
            },
        )
        bindings.trace_event(
            event_type="runtime_runner_built_in_project_scenario_executed",
            source_file="runtime_runner.py",
            source_symbol="_run_rich_automatic_scenario",
            message="Built-in project scenario executed.",
        )
    bindings.trace_event(
        event_type="runtime_runner_automatic_scenario_finished",
        source_file="runtime_runner.py",
        source_symbol="_run_rich_automatic_scenario",
        message="Automatic runtime scenario finished.",
    )
    return scenario_mode


def run_headless_scenario(bindings: RuntimeRunnerPart2Bindings) -> int:
    """Run headless collection while preserving payload and error behavior."""
    try:
        config = bindings.resolve_headless_config()
        project_root = config["project_root"]
        output_json = config["output_json"]
        overwrite = config["overwrite"]
        entry_script = config["entry_script"]
        scenario_module = config["scenario_module"]
        execute_entry_script = config["execute_entry_script"]
        output_json.parent.mkdir(parents=True, exist_ok=True)
        existed_before = output_json.exists()
        if overwrite and existed_before:
            unlink(output_json)
        bindings.configure_runtime_trace(
            project_root=str(project_root),
            output_path=str(output_json),
            entry_script=str(entry_script) if entry_script else "",
        )
        scenario_mode = run_rich_automatic_scenario(
            bindings,
            project_root=project_root,
            output_json=output_json,
            entry_script=entry_script,
            scenario_module=scenario_module,
            execute_entry_script=execute_entry_script,
        )
        saved_path = bindings.save_runtime_trace()
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
            "size": final_output_path.stat().st_size
            if final_output_path.exists()
            else 0,
            "scenario_mode": scenario_mode,
        }
        print(json.dumps(payload), flush=True)
        return 0
    except Exception:
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        return 1
