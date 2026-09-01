# project-path: kanda_reasoner_app/reasoner_tools_shell/runner.py
"""Source-preserving compatibility facade."""

from __future__ import annotations
def _install_deleted_legacy_root_importlib_aliases():
    """Install in-process aliases for deleted legacy payload imports."""
    import importlib
    import sys

    legacy_root_name = "ask_ai" + "_project_reasoner"
    legacy_engine_name = legacy_root_name + ".project_reasoner_v10"

    canonical_root = importlib.import_module("kanda_reasoner_app")
    sys.modules.setdefault(legacy_root_name, canonical_root)

    try:
        canonical_engine = importlib.import_module("kanda_reasoner_app.reasoner_engine")
    except ModuleNotFoundError:
        return

    sys.modules.setdefault(legacy_engine_name, canonical_engine)
    setattr(canonical_root, "project_reasoner_v10", canonical_engine)


_install_deleted_legacy_root_importlib_aliases()


from kanda_reasoner_app.backend_payloads.loader import load_payload

def _install_deleted_legacy_context_collector_aliases():
    """Install aliases for deleted legacy context collector imports."""
    import importlib
    import sys

    legacy_root_name = "ask_ai" + "_project_reasoner"
    legacy_engine_name = legacy_root_name + ".project_reasoner_v10"
    legacy_collector_name = legacy_root_name + ".project_reasoner_v10_data_collector"
    old_canonical_collector_name = "kanda_reasoner_app.project_reasoner_v10_data_collector"

    canonical_root = importlib.import_module("kanda_reasoner_app")
    sys.modules.setdefault(legacy_root_name, canonical_root)

    try:
        canonical_engine = importlib.import_module("kanda_reasoner_app.reasoner_engine")
    except ModuleNotFoundError:
        canonical_engine = None

    if canonical_engine is not None:
        sys.modules.setdefault(legacy_engine_name, canonical_engine)
        setattr(canonical_root, "project_reasoner_v10", canonical_engine)

    canonical_collector = importlib.import_module(
        "kanda_reasoner_app.reasoner_context_collector"
    )
    sys.modules.setdefault(legacy_collector_name, canonical_collector)
    sys.modules.setdefault(old_canonical_collector_name, canonical_collector)
    setattr(canonical_root, "project_reasoner_v10_data_collector", canonical_collector)


_install_deleted_legacy_context_collector_aliases()

def _install_deleted_legacy_runtime_collector_aliases():
    """Install aliases for deleted legacy runtime collector imports."""
    import importlib
    import sys

    legacy_root_name = "ask_ai" + "_project_reasoner"
    legacy_engine_name = legacy_root_name + ".project_reasoner_v10"
    legacy_runtime_collector_name = legacy_root_name + ".project_reasoner_v10_runtime_collector"
    old_canonical_runtime_collector_name = (
        "kanda_reasoner_app.project_reasoner_v10_runtime_collector"
    )

    canonical_root = importlib.import_module("kanda_reasoner_app")
    sys.modules.setdefault(legacy_root_name, canonical_root)

    try:
        canonical_engine = importlib.import_module("kanda_reasoner_app.reasoner_engine")
    except ModuleNotFoundError:
        canonical_engine = None

    if canonical_engine is not None:
        sys.modules.setdefault(legacy_engine_name, canonical_engine)
        setattr(canonical_root, "project_reasoner_v10", canonical_engine)

    canonical_runtime_collector = importlib.import_module(
        "kanda_reasoner_app.reasoner_runtime_collector"
    )
    sys.modules.setdefault(legacy_runtime_collector_name, canonical_runtime_collector)
    sys.modules.setdefault(
        old_canonical_runtime_collector_name,
        canonical_runtime_collector,
    )
    setattr(
        canonical_root,
        "project_reasoner_v10_runtime_collector",
        canonical_runtime_collector,
    )


_install_deleted_legacy_runtime_collector_aliases()

load_payload(__name__, globals(), 'zp')


def _install_show_project_complete_json_process_patch() -> None:
    """Install the source-owned complete JSON Show Project workflow."""
    try:
        from kanda_reasoner_app.reasoner_tools_shell.runner_help import (
            window_process_private_impl as _process_impl,
        )
    except Exception:
        return

    try:
        CollectorRunnerWindow._run_collector = _process_impl._run_collector
        CollectorRunnerWindow._start_collector_process = (
            _process_impl._start_collector_process
        )
        CollectorRunnerWindow._start_complete_json_enrichment_process = (
            _process_impl._start_complete_json_enrichment_process
        )
        CollectorRunnerWindow._start_ai_context_bundle_process = (
            _process_impl._start_ai_context_bundle_process
        )
        CollectorRunnerWindow._on_process_finished = (
            _process_impl._on_process_finished
        )
        CollectorRunnerWindow._on_process_error = _process_impl._on_process_error
    except NameError:
        return


_install_show_project_complete_json_process_patch()

# Green sonar process monitor override. Keep the legacy payload class intact, but
# replace the old text-spinner busy animation with a floating status panel.
def _kanda_show_project_sonar(self):
    """Support kanda show project sonar behavior.
    """
    
    from kanda_reasoner_app.templates.green_sonar_monitor import GreenSonarActivityMonitor

    monitor = getattr(self, "_show_project_sonar_monitor", None)
    if monitor is None:
        monitor = GreenSonarActivityMonitor(self, title="Show Project to AI")
        self._show_project_sonar_monitor = monitor
    return monitor


def _kanda_show_project_details(stage_text: str) -> tuple[str, str, str]:
    """Support kanda show project details behavior.
    
    Parameters
    ----------
    stage_text : str
        The stage text value.
    
    Returns
    -------
    tuple[str, str, str]
        The tuple of values.
    """
    
    stage = str(stage_text or "Running")
    normalized = stage.lower()
    if "runtime" in normalized:
        return (
            "Collecting runtime validation evidence",
            "Preparing trace data for the AI handoff",
            "Generated files stay under Show Project to AI folders",
        )
    if "collector" in normalized:
        return (
            "Building source archive and project maps",
            "Collecting prompt, freeze, and Error Memory context",
            "Second prompt files remain staged until publish succeeds",
        )
    if "enriching" in normalized:
        return (
            "Checking complete JSON evidence sections",
            "Adding deterministic compact context for review",
            "No source files are modified during enrichment",
        )
    if "bundle" in normalized:
        return (
            "Generating the AI context companion bundle",
            "Preparing startup and handoff artifacts",
            "ZIP output remains delivery packaging only",
        )
    if "zipping" in normalized:
        return (
            "Packaging second prompt files for upload",
            "Validating manifest and archive boundaries",
            "Loose JSON files are cleaned only after success",
        )
    return (
        "Running Show Project to AI processing",
        "Preparing source evidence for the next AI handoff",
        "Status details remain visible in the log panel",
    )


def _kanda_start_busy_animation(self, stage_text: str) -> None:
    """Support kanda start busy animation behavior.
    
    Parameters
    ----------
    stage_text : str
        The stage text value.
    """
    
    self._busy_index = 0
    self._active_stage = stage_text
    for attr_name in (
        "run_button",
        "browse_project_button",
        "backup_every_day_button",
        "browse_output_button",
        "create_first_and_second_prompt_files_button",
        "create_first_prompt_files_button",
    ):
        widget = getattr(self, attr_name, None)
        setter = getattr(widget, "setEnabled", None)
        if callable(setter):
            setter(False)
    status = str(stage_text or "Running") + "..."
    self.status_label.setText(status)
    self.setWindowTitle("Project Reasoner v10 - Data Collector")
    _kanda_show_project_sonar(self).start(status, _kanda_show_project_details(stage_text))


def _kanda_stop_busy_animation(self, status_text: str) -> None:
    """Support kanda stop busy animation behavior.
    
    Parameters
    ----------
    status_text : str
        The status text value.
    """
    
    timer = getattr(self, "_busy_timer", None)
    stop = getattr(timer, "stop", None)
    if callable(stop):
        stop()
    for attr_name in (
        "run_button",
        "browse_project_button",
        "backup_every_day_button",
        "browse_output_button",
        "create_first_and_second_prompt_files_button",
        "create_first_prompt_files_button",
    ):
        widget = getattr(self, attr_name, None)
        setter = getattr(widget, "setEnabled", None)
        if callable(setter):
            setter(True)
    status = str(status_text or "Idle")
    self.status_label.setText(status)
    self.setWindowTitle("Project Reasoner v10 - Data Collector")
    monitor = getattr(self, "_show_project_sonar_monitor", None)
    if monitor is not None:
        failed = "fail" in status.lower() or "error" in status.lower()
        details = (
            "Show Project to AI processing stopped",
            "Review the log panel and generated folder state",
            "No additional spinner animation is running",
        )
        if failed:
            monitor.finish_error("Needs review: " + status, details)
        else:
            monitor.finish_success("Complete: " + status, details)
    self._active_stage = ""


def _kanda_tick_busy_animation(self) -> None:
    """Support kanda tick busy animation behavior.
    """
    
    stage_text = getattr(self, "_active_stage", "") or "Running"
    self.status_label.setText(str(stage_text) + "...")


try:
    CollectorRunnerWindow._start_busy_animation = _kanda_start_busy_animation
    CollectorRunnerWindow._stop_busy_animation = _kanda_stop_busy_animation
    CollectorRunnerWindow._tick_busy_animation = _kanda_tick_busy_animation
except NameError:
    pass
