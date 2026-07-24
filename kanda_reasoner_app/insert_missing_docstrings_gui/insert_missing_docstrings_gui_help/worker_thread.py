# project-path: kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/worker_thread.py
# ------------------------------------------------------
# MODULE ORIGIN : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py
# MANIFEST      : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help.json
# HELP FOLDER   : kanda_reasoner_app/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/
# PURPOSE       : Run backend scan, diff, and write work inside a Qt worker object.
# EXPORTS       : DocstringRunWorker
# DEPENDS ON    : none
# REFACTOR DATE : 2026-05-02
# ------------------------------------------------------
"""Qt worker object for missing-docstrings runs."""

from __future__ import annotations

import logging
import inspect
import threading

import contextlib
import importlib
import io
import sys
import traceback
from pathlib import Path

from PySide6.QtCore import QObject, Signal

__all__ = ["DocstringRunWorker"]


class DocstringRunWorker(QObject):
    """Represent docstring run worker."""
    
    output_ready = Signal(str)
    progress_ready = Signal(dict)
    finished_ok = Signal(str)
    finished_error = Signal(str, str)

    def __init__(
        self,
        worker_script_path: str,
        project_root: str,
        mode: str,
        include_module: bool,
        include_classes: bool,
        include_functions: bool,
        insert_file_address_at_top: bool = False,
        ai_enabled: bool = False,
        ai_config_path: str = "default",
        ai_api_key: str = "",
        include_private: bool = True,
        min_confidence: str = "low",
        no_uncertain: bool = False,
        workers: int = 1,
        report_path: str | None = None,
        target_module: str | None = None,
        target_package: str | None = None,
    ) -> None:
        """Handle init.
        
        Parameters
        ----------
        worker_script_path : str
            TODO: describe worker_script_path.
        project_root : str
            TODO: describe project_root.
        mode : str
            TODO: describe mode.
        include_module : bool
            TODO: describe include_module.
        include_classes : bool
            TODO: describe include_classes.
        include_functions : bool
            TODO: describe include_functions.
        ai_enabled : bool, optional
            TODO: describe ai_enabled.
        ai_config_path : str, optional
            TODO: describe ai_config_path.
        include_private : bool, optional
            TODO: describe include_private.
        min_confidence : str, optional
            TODO: describe min_confidence.
        no_uncertain : bool, optional
            TODO: describe no_uncertain.
        workers : int, optional
            TODO: describe workers.
        report_path : str | None, optional
            TODO: describe report_path.
        target_module : str | None, optional
            TODO: describe target_module.
        target_package : str | None, optional
            TODO: describe target_package.
        """
        
        super().__init__()
        self._worker_script_path = Path(worker_script_path)
        self._project_root = Path(project_root)
        self._mode = mode
        self._include_module = include_module
        self._include_classes = include_classes
        self._include_functions = include_functions
        self._insert_file_address_at_top = insert_file_address_at_top
        self._ai_enabled = ai_enabled
        self._ai_config_path = ai_config_path
        self._ai_api_key = str(ai_api_key or "")
        self._include_private = include_private
        self._min_confidence = min_confidence
        self._no_uncertain = no_uncertain
        self._workers = max(1, workers)
        self._report_path = report_path
        self._target_module = target_module
        self._target_package = target_package
        self._stop_event = threading.Event()

    def stop(self) -> None:
        """Request a cooperative stop for the active run."""
        self._stop_event.set()

    def stop_requested(self) -> bool:
        """Return whether a cooperative stop was requested."""
        return self._stop_event.is_set()

    def _call_run(self, module, run_kwargs: dict[str, object]) -> int:
        """Call the backend run function with stop support when available."""
        run_func = module.run
        try:
            signature = inspect.signature(run_func)
        except (TypeError, ValueError):
            signature = None
        if signature is not None and "stop_requested" in signature.parameters:
            run_kwargs["stop_requested"] = self.stop_requested
        if signature is not None and "progress_callback" in signature.parameters:
            run_kwargs["progress_callback"] = self._emit_progress
        if signature is not None and "ai_api_key" in signature.parameters:
            run_kwargs["ai_api_key"] = self._ai_api_key
        return run_func(self._project_root.resolve(), self._mode, **run_kwargs)


    def _emit_progress(self, payload: dict[str, object]) -> None:
        """Emit one best-effort audit-progress payload."""
        if not isinstance(payload, dict):
            return
        self.progress_ready.emit(dict(payload))

    def run(self) -> None:
        """Handle run.
        """
        
        try:
            if self.stop_requested():
                self.finished_error.emit(self._mode, "Run stopped before work started.")
                return
            module = self._load_worker_module(self._worker_script_path)
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                if hasattr(module, "run"):
                    run_kwargs = dict(
                        include_module=self._include_module,
                        include_classes=self._include_classes,
                        include_functions=self._include_functions,
                        insert_file_address_at_top=self._insert_file_address_at_top,
                    )
                    run_kwargs["workers"] = self._workers
                    if self._ai_enabled:
                        run_kwargs["ai_config_path"] = self._ai_config_path or "default"
                        run_kwargs["include_private"] = self._include_private
                        run_kwargs["min_confidence"] = self._min_confidence
                        run_kwargs["no_uncertain"] = self._no_uncertain
                    if self._report_path:
                        run_kwargs["report_path"] = self._report_path
                    if self._target_module:
                        run_kwargs["target_module"] = self._target_module
                    if self._target_package:
                        run_kwargs["target_package"] = self._target_package
                    exit_code = self._call_run(module, run_kwargs)
                elif hasattr(module, "main"):
                    original_argv = sys.argv[:]
                    try:
                        sys.argv = [
                            str(self._worker_script_path),
                            "--root",
                            str(self._project_root.resolve()),
                            f"--{self._mode}",
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
                        if self._target_module:
                            sys.argv += ["--module", self._target_module]
                        if self._target_package:
                            sys.argv += ["--package", self._target_package]
                        exit_code = module.main()
                    finally:
                        sys.argv = original_argv
                else:
                    raise AttributeError("insert_missing_docstrings.py must expose either run(root, mode, ...) or main().")

            captured = buffer.getvalue()
            if captured:
                self.output_ready.emit(captured)

            if int(exit_code) == 0:
                self.finished_ok.emit(self._mode)
            elif self.stop_requested() or int(exit_code) == 130:
                self.finished_error.emit(self._mode, "Stopped by user after current safe checkpoint.")
            else:
                self.finished_error.emit(self._mode, f"Worker finished with exit code {exit_code}.")
        except Exception:
            logging.exception("Boundary failure in run")
            self.finished_error.emit(self._mode, traceback.format_exc())

    def _load_worker_module(self, script_path: Path):
        """Handle load worker module.
        
        Parameters
        ----------
        script_path : Path
            TODO: describe script_path.
        """
        
        del script_path
        return importlib.import_module(
            "kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings"
        )
