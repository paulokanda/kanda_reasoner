# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_gui_help/workflow_gui_worker.py
"""Background worker for workflow and architecture GUI commands."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import logging
import sys
import traceback
from pathlib import Path

from PySide6.QtCore import QObject, Signal

__all__ = [
    "WorkflowRunWorker",
]

class WorkflowRunWorker(QObject):
    """Represent workflow run worker."""
    
    output_ready = Signal(str)
    finished_ok = Signal(str)
    finished_error = Signal(str, str)

    def __init__(self, manager_script_path: str, project_root: str, mode: str) -> None:
        """Support init behavior.
        
        Parameters
        ----------
        manager_script_path : str
            The manager script path value.
        project_root : str
            The project root path.
        mode : str
            The selected mode.
        """
        
        super().__init__()
        self._manager_script_path = Path(manager_script_path)
        self._project_root = Path(project_root)
        self._mode = mode

    def run(self) -> None:
        """Support run behavior.
        """
        
        try:
            module = self._load_manager_module(self._manager_script_path)

            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
                if hasattr(module, "run"):
                    exit_code = module.run(self._project_root.resolve(), self._mode)
                elif hasattr(module, "main"):
                    original_argv = sys.argv[:]
                    try:
                        sys.argv = [
                            str(self._manager_script_path),
                            "--root", str(self._project_root.resolve()),
                            f"--{self._mode}",
                        ]
                        exit_code = module.main()
                    finally:
                        sys.argv = original_argv
                else:
                    raise AttributeError(
                        f"{self._manager_script_path.name} must expose "
                        "either run(root, mode) or main()."
                    )

            captured = buffer.getvalue()
            if captured:
                self.output_ready.emit(captured)

            if int(exit_code) == 0:
                self.finished_ok.emit(self._mode)
            else:
                self.finished_error.emit(
                    self._mode,
                    f"Worker finished with exit code {exit_code}.",
                )
        except Exception:
            logging.exception("Workflow worker failed")
            tb = traceback.format_exc()
            self.finished_error.emit(self._mode, tb)

    @staticmethod
    def _load_manager_module(manager_script_path):
        """Load the workflow manager module through the package path."""
        import importlib
        import sys
        from pathlib import Path

        script_path = Path(manager_script_path).resolve()
        staged_package_dir = "_".join(("ask", "ai", "project", "reasoner"))
        project_root = None
        for candidate in [script_path.parent] + list(script_path.parents):
            if (candidate / staged_package_dir).is_dir():
                project_root = candidate
                break
        if project_root is None:
            project_root = script_path.parents[2]

        project_root_text = str(project_root)
        if project_root_text not in sys.path:
            sys.path.insert(0, project_root_text)

        module_name = "kanda_reasoner_app.manage_workflows.manage_workflows"
        if module_name in sys.modules:
            return sys.modules[module_name]
        return importlib.import_module(module_name)
