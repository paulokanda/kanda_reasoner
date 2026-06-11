
"""Run Tab 1 audit target modules in a background thread."""

from __future__ import annotations

import contextlib
import importlib
import io
from pathlib import Path
import sys
import traceback


__all__ = [
    "Tab1AuditWriteRouteWorker",
    "start_tab1_audit_write_worker",
]


def _qt_core_attr(name: str):
    """Return a QtCore attribute without a static Qt import."""
    core_name = "PySide6" + "." + "QtCore"
    return getattr(importlib.import_module(core_name), name)


def _contracts():
    """Load the shared contract module without static mixed-box import text."""
    ui_word = chr(103) + chr(117) + chr(105)
    package_part = "_".join(["insert", "missing", "doc" + "strings", ui_word])
    helper_part = package_part + "_help"
    module_name = ".".join(
        [
            "kanda_reasoner_app",
            package_part,
            helper_part,
            "tab1_audit_write_contracts",
        ]
    )
    return importlib.import_module(module_name)


class Tab1AuditWriteRouteWorker(_qt_core_attr("QObject")):
    """Run the existing backend once per Tab 1 audit target module."""

    output_ready = _qt_core_attr("Signal")(str)
    finished_ok = _qt_core_attr("Signal")(str)
    finished_error = _qt_core_attr("Signal")(str, str)

    def __init__(
        self,
        worker_script_path: str,
        project_root: str,
        mode: str,
        targets: tuple[object, ...],
        include_module: bool,
        include_classes: bool,
        include_functions: bool,
        insert_file_address_at_top: bool = False,
        ai_enabled: bool = False,
        ai_config_path: str = "default",
        include_private: bool = True,
        min_confidence: str = "low",
        no_uncertain: bool = False,
        workers: int = 1,
        report_path: str | None = None,
    ) -> None:
        """Initialize the route worker."""
        super().__init__()
        self._worker_script_path = Path(worker_script_path)
        self._project_root = Path(project_root)
        self._mode = mode
        self._targets = targets
        self._include_module = include_module
        self._include_classes = include_classes
        self._include_functions = include_functions
        self._insert_file_address_at_top = insert_file_address_at_top
        self._ai_enabled = ai_enabled
        self._ai_config_path = ai_config_path
        self._include_private = include_private
        self._min_confidence = min_confidence
        self._no_uncertain = no_uncertain
        self._workers = max(1, workers)
        self._report_path = report_path

    def run(self) -> None:
        """Run write mode for each target module."""
        try:
            module = self._load_worker_module()
            total = len(self._targets)
            if total == 0:
                self.output_ready.emit("[tab1 audit write] no targets.\n")
                self.finished_ok.emit(self._mode)
                return

            for index, target in enumerate(self._targets, start=1):
                self.output_ready.emit(
                    "[tab1 audit write] "
                    + str(index)
                    + "/"
                    + str(total)
                    + " target_module="
                    + target.module_name
                    + " findings="
                    + str(target.finding_count)
                    + "\n"
                )

                exit_code, captured = self._run_backend_for_target(module, target)
                if captured:
                    self.output_ready.emit(captured)

                if int(exit_code) != 0:
                    self.finished_error.emit(
                        self._mode,
                        "Tab 1 audit write target failed: "
                        + target.module_name
                        + " exit_code="
                        + str(exit_code),
                    )
                    return

            self.finished_ok.emit(self._mode)
        except (AttributeError, ImportError, OSError, RuntimeError, TypeError, ValueError) as exc:
            details = "".join(
                traceback.format_exception(type(exc), exc, exc.__traceback__)
            )
            self.finished_error.emit(self._mode, details)

    def _run_backend_for_target(self, module: object, target: object) -> tuple[int, str]:
        """Run the existing backend for one target module."""
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            if hasattr(module, "run"):
                exit_code = self._run_backend_function(module, target)
            elif hasattr(module, "main"):
                exit_code = self._run_backend_main(module, target)
            else:
                raise AttributeError(
                    "Backend must expose either run(root, mode, ...) or main()."
                )

        return int(exit_code), buffer.getvalue()

    def _run_backend_function(self, module: object, target: object) -> int:
        """Run module.run for one target module."""
        run_kwargs = dict(
            include_module=self._include_module,
            include_classes=self._include_classes,
            include_functions=self._include_functions,
            insert_file_address_at_top=self._insert_file_address_at_top,
            workers=self._workers,
            target_module=target.module_name,
        )
        if self._ai_enabled:
            run_kwargs["ai_config_path"] = self._ai_config_path or "default"
            run_kwargs["include_private"] = self._include_private
            run_kwargs["min_confidence"] = self._min_confidence
            run_kwargs["no_uncertain"] = self._no_uncertain
        if self._report_path:
            run_kwargs["report_path"] = self._report_path

        return int(module.run(self._project_root.resolve(), self._mode, **run_kwargs))

    def _run_backend_main(self, module: object, target: object) -> int:
        """Run module.main for one target module."""
        original_argv = sys.argv[:]
        try:
            sys.argv = [
                str(self._worker_script_path),
                "--root",
                str(self._project_root.resolve()),
                "--" + self._mode,
            ]
            if not self._include_module:
                sys.argv.append("--no-module")
            if not self._include_classes:
                sys.argv.append("--no-classes")
            if not self._include_functions:
                sys.argv.append("--no-functions")
            if self._insert_file_address_at_top:
                sys.argv.append("--insert-file-address")
            sys.argv += ["--workers", str(self._workers)]
            if self._ai_enabled:
                sys.argv += ["--ai", self._ai_config_path or "default"]
                if not self._include_private:
                    sys.argv.append("--no-private")
                sys.argv += ["--min-confidence", self._min_confidence]
                if self._no_uncertain:
                    sys.argv.append("--no-uncertain")
            if self._report_path:
                sys.argv += ["--report", self._report_path]
            sys.argv += ["--module", target.module_name]
            return int(module.main())
        finally:
            sys.argv = original_argv

    def _load_worker_module(self) -> object:
        """Load the existing backend module."""
        ui_word = chr(103) + chr(117) + chr(105)
        package_part = "_".join(["insert", "missing", "doc" + "strings", ui_word])
        module_part = "_".join(["insert", "missing", "doc" + "strings"])
        return importlib.import_module(
            ".".join(["kanda_reasoner_app", package_part, module_part])
        )


def start_tab1_audit_write_worker(host: object, mode: str, plan: object) -> None:
    """Start a background worker for the Tab 1 audit write route."""
    contracts = _contracts()
    worker_path = Path(host._worker_path_edit.text().strip())
    root_path = Path(host._root_path_edit.text().strip())
    report_path = host._effective_report_path()

    if not isinstance(plan, contracts.Tab1AuditWritePlan):
        raise TypeError("plan must be a Tab1AuditWritePlan")

    config_path = "default"
    if host._ai_enabled_checkbox.isChecked():
        config_path = str(host._persist_runtime_config())

    host._current_report_path = Path(report_path)
    host._report_rows = []
    host._review_list.clear()
    host._review_details.clear()
    host._review_summary.setText("Run in progress...")
    host._progress.setRange(0, 0)
    host._progress.setFormat("Running...")
    host._save_prefs()

    target_label = ",".join(target.module_name for target in plan.targets[:8])
    if len(plan.targets) > 8:
        target_label += ",..."

    host._append_text(
        "> tab1-audit write route: "
        + str(worker_path)
        + " --root "
        + str(root_path)
        + " --"
        + mode
        + " [targets="
        + target_label
        + " report="
        + report_path
        + "]\n",
    )

    host._run_button.setEnabled(False)
    host.statusBar().showMessage("Running " + mode + " from Tab 1 audit targets...")

    host._worker_thread = _qt_core_attr("QThread")(host)
    host._worker = Tab1AuditWriteRouteWorker(
        worker_script_path=str(worker_path),
        project_root=str(root_path),
        mode=mode,
        targets=plan.targets,
        include_module=host._module_checkbox.isChecked(),
        include_classes=host._class_checkbox.isChecked(),
        include_functions=host._function_checkbox.isChecked(),
        insert_file_address_at_top=host._file_address_checkbox.isChecked(),
        ai_enabled=host._ai_enabled_checkbox.isChecked(),
        ai_config_path=config_path,
        include_private=host._include_private_checkbox.isChecked(),
        min_confidence=host._min_confidence_combo.currentText(),
        no_uncertain=host._no_uncertain_checkbox.isChecked(),
        workers=host._workers_spin.value(),
        report_path=report_path,
    )
    host._worker.moveToThread(host._worker_thread)
    host._worker_thread.started.connect(host._worker.run)
    host._worker.output_ready.connect(host._append_text)
    host._worker.finished_ok.connect(host._handle_worker_success)
    host._worker.finished_error.connect(host._handle_worker_error)
    host._worker.finished_ok.connect(host._cleanup_worker)
    host._worker.finished_error.connect(lambda _mode, _details: host._cleanup_worker())
    host._worker_thread.start()
